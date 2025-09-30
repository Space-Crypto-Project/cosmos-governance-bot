#!/usr/bin/python3

'''
SpaceStake | January 3th, 2025
- Twitter bot to monitor and report on COSMOS governance proposals
- Discord webhook to post proposals 
- Discord Threads to allow for discussion of new proposals 
- Email notifications for new proposals

Instructions:
- Install Python 3.10+
- Install requirements:
    pip3 install -r requirements.txt
    or
    pip install -r requirements.txt
- Execute the script:
    python3 GovBot.py
    or
    python GovBot.py


*Get REST lcd's in chain.json from https://github.com/cosmos/chain-registry
'''

import datetime
import discord
import json
import os
import requests
import schedule
import time
import tweepy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from discord import SyncWebhook

from ChainApis import chainAPIs, customExplorerLinks, DAOs

# == Configuration ==

# If false, it is up to you to schedule via crontab -e such as: */30 * * * * cd /root/twitterGovBot && python3 twitterGovernanceBot.py
USE_PYTHON_RUNNABLE = False
LOG_RUNS = False


USE_CUSTOM_LINKS = True
if USE_CUSTOM_LINKS:
    customLinks = customExplorerLinks

# Don't touch below --------------------------------------------------

proposals = {}
DISCORD_API = "https://discord.com/api/v9"
IS_FIRST_RUN = False
BOOSTED_DISCORD_THREAD_TIME_TIERS = {0: 1440,1: 4320,2: 10080,3: 10080}

with open('secrets.json', 'r') as f:
    secrets = json.load(f)

    IN_PRODUCTION = secrets.get('IN_PRODUCTION', True)
    FETCH_LAST_PROP = secrets.get('FETCH_LAST_PROP', False)
    TWITTER = secrets['TWITTER']['ENABLED']
    DISCORD = secrets['DISCORD']['ENABLED']
    EMAIL_ENABLED = secrets['EMAIL']['ENABLED']
    DISCORD_THREADS_AND_REACTIONS = secrets['DISCORD_THREADS']['ENABLE_THREADS_AND_REACTIONS']

    explorer = secrets.get('EXPLORER_DEFAULT', "mintscan") # ping, mintscan, keplr
    TICKERS_TO_ANNOUNCE = secrets.get('TICKERS_TO_ANNOUNCE', [])
    TICKERS_TO_IGNORE = secrets.get('TICKERS_TO_IGNORE', [])
    # print(f"Ignoring: {TICKERS_TO_IGNORE}")

    filename = secrets['FILENAME']
    filename_dao = 'chains_dao.json'

    if TWITTER:
        twitSecrets = secrets['TWITTER']
        APIKEY = twitSecrets['APIKEY']
        APIKEYSECRET = twitSecrets['APIKEYSECRET']
        ACCESS_TOKEN = twitSecrets['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = twitSecrets['ACCESS_TOKEN_SECRET']  
        # Authenticate to Twitter & Get API
        auth = tweepy.OAuth1UserHandler(APIKEY, APIKEYSECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)      

    if DISCORD:
        discSecrets = secrets['DISCORD']
        WEBHOOK_URL = discSecrets['WEBHOOK_URL']
        USERNAME = discSecrets['USERNAME']
        AVATAR_URL = discSecrets['AVATAR_URL']
        HEX_COLOR = int(discSecrets['HEX_COLOR'], 16)
        REACTION_RATE_LIMIT = 0.1

        if DISCORD_THREADS_AND_REACTIONS:
            discTreads = secrets['DISCORD_THREADS']
            CHANNEL_ID = int(discTreads['CHANNEL_ID'][0])
            GUILD_ID = int(discTreads['GUILD-SERVER_ID'])
            DO_ARCHIVE_THREADS = bool(discTreads['ARCHIVE_THREADS'])
            THREAD_ARCHIVE_MINUTES = int(discTreads['THREAD_ARCHIVE_MINUTES'])
            BOT_TOKEN = discTreads['BOT_TOKEN']                 
            BOT_TOKEN_HEADERS_FOR_API = {
                "Content-Type": "application/json",
                "authorization": "Bot " + BOT_TOKEN,    
            }
    
    if EMAIL_ENABLED:
        emailSecrets = secrets['EMAIL']
        SSL = emailSecrets['SSL']
        EMAIL_HOST = emailSecrets['HOST']
        EMAIL_PORT = emailSecrets['PORT']
        EMAIL_USERNAME = emailSecrets['USERNAME']
        EMAIL_PASSWORD = emailSecrets['PASSWORD']
        EMAIL_FROM = emailSecrets['FROM']
        EMAIL_TO = emailSecrets['TO']
        EMAIL_FETCHING_ERROR_NOTIFICATION = emailSecrets['FETCHING_ERROR_NOTIFICATION'] # Send email if proposals fetching error occurs

# Loads normal proposals (ticker -> id) dict
def load_proposals_from_file() -> dict:
    global proposals
    with open(filename, 'r') as f:
        proposals = json.load(f)       
    return proposals
def save_proposals() -> None:
    if len(proposals) > 0:
        with open(filename, 'w') as f:
            json.dump(proposals, f)
def update_proposal_value(ticker: str, newPropNumber: int):
    global proposals
    proposals[ticker] = newPropNumber
    save_proposals()
#

def _SetMaxArchiveDurationLength() -> int:
    global THREAD_ARCHIVE_MINUTES

    if DISCORD_THREADS_AND_REACTIONS == False:
        return 0

    # Archive lengths are 1 or 24 hours for level 0 boosted servers, 3 days for level 1, and 7 days for level 2
    # Returns max time user
    v = requests.get(f"{DISCORD_API}/guilds/{GUILD_ID}", headers=BOT_TOKEN_HEADERS_FOR_API).json()    
    # print(v)
    
    if 'message' in v.keys() and v['message'] == '401: Unauthorized':
        print("Discord API Error: 401 Unauthorized. Please ensure you have the correct BOT_TOKEN set in secrets.json")
        exit()

    guildBoostLevel = int(v['premium_tier'])
    max_len = BOOSTED_DISCORD_THREAD_TIME_TIERS[guildBoostLevel]
    
    if THREAD_ARCHIVE_MINUTES not in [60, 1440, 4320, 10080]:
        THREAD_ARCHIVE_MINUTES = max_len
        print(f"\nInvalid thread archive length: {THREAD_ARCHIVE_MINUTES}")
        print(f"Using {max_len} minutes. Other options: [60, 1440, 4320, 10080]")
    elif THREAD_ARCHIVE_MINUTES > max_len:
        THREAD_ARCHIVE_MINUTES = max_len
        print(f"\nWARNING: THREAD_ARCHIVE_MINUTES is greater than the max archive length for this server. Setting to {max_len}")
        print(f"You need a higher boost level to use 4320 & 100080 sadly :(")

    return max_len

def discord_create_thread(message_id, thread_name):
    global DO_ARCHIVE_THREADS
    data = { # https://discord.com/developers/docs/resources/channel#allowed-mentions-object-json-params-thread
        "name": thread_name,
        "archived": DO_ARCHIVE_THREADS,
        "auto_archive_duration": THREAD_ARCHIVE_MINUTES, # set via _SetMaxArchiveDurationLength on main() based on server boost level
        "locked": False,
        "invitable": False,
        "rate_limit_per_user": 5,
    }
    # print(data)
    # https://discord.com/developers/docs/topics/gateway#thread-create
    return requests.post(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages/{message_id}/threads", json=data, headers=BOT_TOKEN_HEADERS_FOR_API).json()    

def _getLastMessageID():
    # gets last message from channel that the webhook just sent too. This way we can make thread from it without bot running all the time
    # https://discord.com/developers/docs/resources/channel#get-channel-messages
    res = requests.get(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages?limit=1", headers=BOT_TOKEN_HEADERS_FOR_API).json()
    # print(res)
    return res[0]['id']

def discord_post_to_channel(ticker, propID, title, description, voteLink):
    # Auto replace description's <br> & \n ?
    if len(description) > 4096:
        description = description[:4090] + "....."

    embed = discord.Embed(
            title=f"${str(ticker).upper()} #{propID} | {title}",
            description=description,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            color=HEX_COLOR
    )
    embed.add_field(name="Link", value=f"{voteLink}")
    embed.set_thumbnail(url=AVATAR_URL)

    # Use SyncWebhook for sending messages
    webhook = SyncWebhook.from_url(WEBHOOK_URL)
    webhook.send(username=USERNAME, embed=embed)

def discord_add_reacts(message_id): # needs READ_MESSAGE_HISTORY & ADD_REACTIONS
    # https://discord.com/developers/docs/resources/channel#create-reaction
    # https://discord.com/developers/docs/resources/emoji    
    for emoji in ["✅", "❌", "⭕", "🚫"]:
        # print("PUT request for emoji: " + emoji) # DEBUGGING
        r = requests.put(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages/{message_id}/reactions/{emoji}/@me", headers=BOT_TOKEN_HEADERS_FOR_API)
        if r.text != "":
            print(r.text)
        time.sleep(REACTION_RATE_LIMIT) # rate limit

def send_email(subject, body):
    if not EMAIL_ENABLED:
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        if SSL:
            server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        else:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_explorer_link(ticker, propId):
    if ticker in customLinks:
        return f"{customLinks[ticker]}/{propId}"

    # pingpub, mintscan, keplr
    possibleExplorers = chainAPIs[ticker][1]

    explorerToUse = explorer
    if explorerToUse not in possibleExplorers: # If it doesn't have a mintscan, default to ping.pub (index 0)
        explorerToUse = list(possibleExplorers.keys())[0]

    # keplr new website changed this
    # if explorerToUse == "keplr":
    #     # https://wallet.keplr.app/#/gravity-bridge/governance?detailId={propid}
    #     return f"{chainAPIs[ticker][1][explorerToUse]}{propId}"
    # else:
    return f"{chainAPIs[ticker][1][explorerToUse]}/{propId}"

# This is so messy, make this more OOP related
def post_update(ticker, propID, title, description="", cosmovisor_folder="not-defined", isDAO=False, DAOVoteLink=""):
    chainExploreLink = DAOVoteLink
    if isDAO == False:
        chainExploreLink = get_explorer_link(ticker, propID)

    message = f"${str(ticker).upper()} | Proposal #{propID} | {description} | Cosmovisor Folder: '{cosmovisor_folder}' | VOTING | {title} | {chainExploreLink}"
    twitterAt = ""

    if isDAO == True:
        if "twitter" in DAOs[ticker]:
            twitterAt = DAOs[ticker]["twitter"]
    else:
        twitterAt = chainAPIs[ticker][2] # @'s blockchains official twitter
    
    if len(twitterAt) > 1:
        twitterAt = f'@{twitterAt}' if not twitterAt.startswith('@') else twitterAt
        message += f" | {twitterAt}"
    print(message)

    if IN_PRODUCTION:
        if TWITTER:
            try:
                tweet = api.update_status(message)
                print(f"Tweet sent for {tweet.id}: {message}")
            except Exception as err:
                print("Tweet failed due to being duplicate OR " + str(err)) 
        if DISCORD:
            try:
                # Add cosmosvisor folder to description if it is not "not-defined"
                if cosmovisor_folder != "not-defined":
                    description = description + f" Cosmovisor folder: {cosmovisor_folder}\n"
                discord_post_to_channel(ticker, propID, title, description, chainExploreLink)
                if DISCORD_THREADS_AND_REACTIONS:
                    # Threads must be enabled for reacts bc bot token
                    discord_add_reacts(_getLastMessageID())
                    discord_create_thread(_getLastMessageID(), f"{ticker}-{propID}") 
                    pass
            except Exception as err:
                print("Discord post failed: " + str(err))
        if EMAIL_ENABLED:
            try:
                send_email(f"New Proposal for {ticker}", message)
            except Exception as err:
                print("Email notification failed: " + str(err))
      
# Initialize a dictionary to keep track of consecutive failures for each ticker
# Load failure counter from JSON file
def load_failure_counter():
    try:
        with open('errors.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save failure counter to JSON file
def save_failure_counter(counter):
    with open('errors.json', 'w') as f:
        json.dump(counter, f)

failure_counter = load_failure_counter()

def getAllProposalsWithFallback(ticker) -> list:
    # First try the normal bulk fetch
    props = getAllProposals(ticker)
    
    # If we got proposals or it's not a runtime error, return as normal
    if len(props) > 0:
        return props
    
    # Check if this ticker had a specific runtime error that indicates we should try individual proposal fetching
    if ticker in failure_counter and failure_counter[ticker] > 0:
        print(f"Bulk fetch failed for {ticker}, trying individual proposal fetching...")
        return getAllProposalsIndividually(ticker)
    
    return props

def getAllProposalsIndividually(ticker) -> list:
    """
    Fallback method to check proposals individually starting from last known + 1
    """
    props = []
    
    # Get last known proposal ID for this ticker
    lastPropID = 0
    if ticker in proposals:
        lastPropID = int(proposals[ticker])
    
    link = chainAPIs[ticker][0]
    # Remove the proposals endpoint and prepare for individual proposal checks
    base_link = link.replace('/proposals', '/proposals/')
    
    # Check if link contains /v1/ or /v1beta1/ to determine version
    if 'v1beta1' in link:
        version = 'v1beta'
    else:
        version = 'v1'
    
    current_check_id = lastPropID + 1
    consecutive_not_found = 0
    max_consecutive_not_found = 5  # Stop after 5 consecutive "doesn't exist"
    
    print(f"Starting individual proposal check for {ticker} from proposal #{current_check_id}")
    
    while consecutive_not_found < max_consecutive_not_found:
        try:
            individual_url = f"{base_link}{current_check_id}"
            print(f"Checking individual proposal: {individual_url}")
            
            response = requests.get(individual_url, headers={
                'accept': 'application/json', 
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
            })
            
            response_json = response.json()
            
            if 'code' in response_json:
                error_message = response_json.get('message', '').lower()
                if "doesn't exist" in error_message or "not found" in error_message:
                    print(f"Proposal #{current_check_id} doesn't exist for {ticker}")
                    consecutive_not_found += 1
                    current_check_id += 1
                    continue
                else:
                    if "encoding" in error_message or "decode" in error_message or "unicode" in error_message:
                        print(f"Encoding error for proposal #{current_check_id} for {ticker}: {response_json['message']}, continuing to next proposal")
                        current_check_id += 1
                        # Don't increment consecutive_not_found for encoding errors
                        continue
                    else:
                        print(f"Error fetching proposal #{current_check_id} for {ticker}: {response_json['message']}")
                        break
            
            # Reset consecutive not found counter since we found a proposal
            consecutive_not_found = 0
            
            # Extract the proposal from response
            proposal = response_json.get('proposal', {})
            if not proposal:
                current_check_id += 1
                continue
            
            # Check proposal status
            status = proposal.get('status', '')
            
            # For v1 API, status is a string like "PROPOSAL_STATUS_VOTING_PERIOD"
            # For v1beta1, status might be a number where 2 = voting period
            is_voting = False
            # Both v1 and v1beta1 APIs use the same status string format
            is_voting = status == "PROPOSAL_STATUS_VOTING_PERIOD"
            
            if is_voting:
                print(f"Found voting proposal #{current_check_id} for {ticker}")
                props.append(proposal)
                # Update the chains.json immediately for this proposal
                update_proposal_value(ticker, current_check_id)
            else:
                print(f"Proposal #{current_check_id} for {ticker} is not in voting period (status: {status})")
                # Still update chains.json to track that we've seen this proposal
                if current_check_id > lastPropID:
                    update_proposal_value(ticker, current_check_id)
            
            current_check_id += 1
            
        except Exception as e:
            print(f"Error checking individual proposal #{current_check_id} for {ticker}: {e}")
            current_check_id += 1
            consecutive_not_found += 1
    
    print(f"Finished individual proposal check for {ticker}. Found {len(props)} voting proposals.")
    return props

def getAllProposals(ticker) -> list:
    # Makes request to API & gets JSON reply in form of a list
    props = []
    version = ''

    if FETCH_LAST_PROP:
        print(f"Getting last proposal for {ticker}")
    else:
        print(f"Getting live (voting period) proposals for {ticker}")
    
    try:
        link = chainAPIs[ticker][0]
        #check if link contains /v1/ or /v1beta1/ to determine which version of the API to use
        if 'v1beta1' in link:
            version = 'v1beta'
        else:
            version = 'v1'

        if (FETCH_LAST_PROP): # if we want to fetch the last proposal (testing purposes)
            PARAMS = {'pagination.limit': 2, 'pagination.reverse': 'true'}
        else:
            PARAMS = {'proposal_status': '2'} # 2 = voting period

        response = requests.get(link, headers={
            'accept': 'application/json', 
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}, 
            params=PARAMS) 
        
        response_json = response.json()
        #print(response_json)
        if 'code' in response_json:
            error = f"Error fetching proposals for {ticker}: {response_json['message']}"
            # add link to error
            error += f"\nLink: {link}"
            print(error)

            # Increment the failure counter for the ticker
            if ticker in failure_counter:
                failure_counter[ticker] += 1
            else:
                failure_counter[ticker] = 1

             # Check if this is a runtime error that indicates we should try individual fetching
            if "runtime error" in response_json.get('message', '').lower() or "nil pointer" in response_json.get('message', '').lower():
                print(f"Runtime error detected for {ticker}, will try individual proposal fetching")
                # Don't send email immediately for runtime errors, let the fallback handle it
                save_failure_counter(failure_counter)
                return props  # Return empty list to trigger fallback

            # If the failure counter reaches 3, send an email notification
            if failure_counter[ticker] >= 3:
                if EMAIL_FETCHING_ERROR_NOTIFICATION:
                    error += f"\nLink: {link}"
                    send_email(f"Error fetching proposals for {ticker}", error)
                # Reset the counter after sending the email
                failure_counter[ticker] = 0

            # Save the updated failure counter to the JSON file
            save_failure_counter(failure_counter)
        else:
            # Reset the failure counter on successful fetch
            failure_counter[ticker] = 0
            props = response_json['proposals']
                        
            save_failure_counter(failure_counter)
    except Exception as e:
        error = f"Issue with request to {ticker}: {e}"
        print(error)

        # Increment the failure counter for the ticker
        if ticker in failure_counter:
            failure_counter[ticker] += 1
        else:
            failure_counter[ticker] = 1

        if failure_counter[ticker] >= 3:    
            if EMAIL_FETCHING_ERROR_NOTIFICATION:
                error += f"\nLink: {link}"
                send_email(f"Error fetching proposals for {ticker}", error)
            failure_counter[ticker] = 0

        save_failure_counter(failure_counter)
    return props

def checkIfNewerDAOProposalIsOut(daoTicker):
    print(f"Checking if new DAO proposal is out for {daoTicker}")
    # https://rest-juno.ecostake.com/cosmwasm/wasm/v1/contract/juno1eqfqxc2ff6ywf8t278ls3h3rdk7urmawyrthagl6dyac29r7c5vqtu0zlf/smart/eyJsaXN0X3Byb3Bvc2FscyI6e319?encoding=base64
    token = DAOs[daoTicker]
    props = requests.get(f"{token['proposals']}").json()['data']['proposals']

    for prop in props:
        current_prop_id = int(prop['id'])
        current_id_str = str(current_prop_id)
        # print(f"{daoTicker} | {current_prop_id}")

        proposal_title = prop['proposal']['title']
        proposer = prop['proposal']['proposer']

        status = prop['proposal']['status']
        if status != "open": # executed, or maybe no deposit yet.
            # print(f"Proposal {current_prop_id} is not open for voting yet, skipping")
            continue

        if daoTicker not in list(proposals.keys()):
            proposals[daoTicker] = 0 #; print('token not in dict, adding')

        # check if this proposal has been submitted before based on the # id
        if current_prop_id <= proposals[daoTicker]:
            print(f"Proposal {current_prop_id} was already posted for this id ({current_prop_id})")
            continue

        print(f"{daoTicker} has not been posted before as: {current_prop_id} | {proposal_title}")

        if IS_FIRST_RUN == False: # we only write DAO proposals to discord / twitter when its not the first run or it would spam ALL proposals on start
            # print(f"Proposal {current_prop_id} exists")
            # Announce it as live
            # title = f"{token['name']} Proposal #{current_prop_id}"
            post_update(
                ticker=daoTicker,
                propID=current_prop_id, 
                title=proposal_title, 
                description=f"from {proposer}", # for discord embeds
                cosmovisor_folder="not-defined", # for discord embeds
                isDAO=True,
                DAOVoteLink=f"{token['vote']}/{current_prop_id}" # https://www.rawdao.zone/vote/#
            )

        if IS_FIRST_RUN or IN_PRODUCTION:      
            # save to proposals dict & to file (so we don't post again), unless its the first run                                 
            update_proposal_value(daoTicker, current_prop_id)
        else:
            print("DAO: Not in production, not writing to file.")


def checkIfNewestProposalIDIsGreaterThanLastTweet(ticker):
    # get our last tweeted proposal ID (that was in voting period), if it exists
    # if not, 0 is the value so we search through all proposals
    lastPropID = 0
    if ticker in proposals:
        lastPropID = int(proposals[ticker])

    link = chainAPIs[ticker][0]
    #check if link contains /v1/ or /v1beta1/ to determine which version of the API to use
    if 'v1beta1' in link:
        version = 'v1beta'
    else:
        version = 'v1'

    # Use the new fallback method
    props = getAllProposalsWithFallback(ticker)
    if len(props) == 0:
        return "No proposals found for this ticker."

    # loop through out last stored voted prop ID & newest proposal ID
    for prop in props:
        if version == 'v1':
            current_prop_id = int(prop['id'])
        elif version == 'v1beta':
            current_prop_id = int(prop['proposal_id'])

        #print(f"Last prop id: {lastPropID}")
        # If this is a new proposal which is not the last one we tweeted for
        if current_prop_id > lastPropID:   
            print(f"Newest prop ID {current_prop_id} is greater than last prop ID {lastPropID}")
            
            if IS_FIRST_RUN or IN_PRODUCTION:      
                # save to proposals dict & to file (so we don't post again), unless its the first run                                 
                update_proposal_value(ticker, current_prop_id)

            else:
                print("Not in production, not writing to file.")

            title = ""
            description = ""
            cosmovisor_folder = "not-defined" # default value

            if version == 'v1':
                if 'messages' in prop and len(prop['messages']) > 0:
                    if 'content' in prop['messages'][0]:
                        title = prop['messages'][0]['content'].get('title', "")
                        description = prop['messages'][0]['content'].get('description', "")
                    # Check for MsgSoftwareUpgrade directly in messages
                    if '@type' in prop['messages'][0] and prop['messages'][0]['@type'] == '/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade':
                        # Extract cosmovisor folder from the plan name
                        if 'plan' in prop['messages'][0] and 'name' in prop['messages'][0]['plan']:
                            title = prop['title']
                            description = prop['summary']
                            cosmovisor_folder = prop['messages'][0]['plan']['name']
                            print(f"Found upgrade plan: {cosmovisor_folder}")

                            description += f" Upgrade scheduled at height {prop['messages'][0]['plan'].get('height', 'unknown')}."
                        else:
                            cosmovisor_folder = "not-defined"
                    if 'title' in prop and 'summary' in prop and title == "" and description == "": 
                        title = prop['title']
                        description = prop['summary']
                    if 'metadata' in prop and title == "" and description == "" and prop['metadata'].strip():
                        try:
                            metadata = json.loads(prop['metadata'])
                            title = metadata.get('title', "title not found")
                            description = metadata.get('summary', "description not found")
                        except json.JSONDecodeError:
                            print(f"Invalid JSON in metadata, title and description not found for for {ticker} proposal #{current_prop_id}.")
                            title = f"Proposal #{current_prop_id}"
                            description = "No title and description found."

            elif version == 'v1beta':
                try:
                    # Extract title and description
                    if 'content' in prop:
                        content = prop['content']
                        if '@type' in content and content['@type'] == '/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade':
                            # Use the plan name as the title if it's a software upgrade proposal
                            if 'plan' in content and 'name' in content['plan']:
                                title = content.get('title', f"Proposal #{current_prop_id}")
                                description = content.get('description', f"Upgrade scheduled at height {content['plan'].get('height', 'unknown')}.")
                                cosmovisor_folder = content['plan']['name']  # Set cosmovisor_folder here
                            else:
                                title = content.get('title', f"Proposal #{current_prop_id}")
                                description = content.get('description', f"Upgrade scheduled at height {content['plan'].get('height', 'unknown')}.")
                                cosmovisor_folder = "not-defined"
                        else:
                            title = content.get('title', f"Proposal #{current_prop_id}")
                            description = content.get('description', f"Upgrade scheduled at height {content['plan'].get('height', 'unknown')}.")
                            cosmovisor_folder = "not-defined"
                    else:
                        title = f"Proposal #{current_prop_id}"
                        description = "No description available."
                        cosmovisor_folder = "not-defined"
                except KeyError:
                    print(f"Title and description not found for proposal #{current_prop_id}. Try to change the LCD endpoint for {ticker} from 'v1beta1' to 'v1'")
                    title = f"Proposal #{current_prop_id}"
                    description = f"No title and description found. Try to change the Bot LCD endpoint for {ticker} from 'v1beta1' to 'v1'"
                    cosmovisor_folder = "not-defined"  # Fallback if no plan name is found

            
            post_update(
                ticker=ticker,
                propID=current_prop_id, 
                title=title, 
                description=description, # for discord embeds
                cosmovisor_folder=cosmovisor_folder
            )

def logRun():
    if LOG_RUNS:
        with open("logs.txt", 'a') as flog:
            flog.write(str(time.ctime() + "\n"))

def runChecks():   
    print("Running checks...") 
    for chain in chainAPIs.keys():
        try:
            if  len(TICKERS_TO_ANNOUNCE) > 0 and chain not in TICKERS_TO_ANNOUNCE:
                continue
            if len(TICKERS_TO_IGNORE) > 0 and chain in TICKERS_TO_IGNORE:
                # print(f"Ignoring {chain} as it is in the ignore list.")
                continue # ignore chains like terra we don't want to announce

            checkIfNewestProposalIDIsGreaterThanLastTweet(chain)
        except Exception as e:
            print(f"{chain} checkProp failed: {e}")


    # loop through DAOs
    for dao in DAOs.keys():
        try:
            if dao not in TICKERS_TO_ANNOUNCE and TICKERS_TO_ANNOUNCE != []:
                continue
            checkIfNewerDAOProposalIsOut(dao)
        except Exception as e:
            print(f"{dao} checkProp failed {e}")

    logRun()
    print(f"All chains checked {time.ctime()}, waiting")


def updateChainsToNewestProposalsIfThisIsTheFirstTimeRunning():
    global IN_PRODUCTION, IS_FIRST_RUN
    '''
    Updates JSON file to the newest proposals provided this is the first time running
    '''
    if os.path.exists(filename):
        print(f"{filename} exists, not first run")
        return

    IS_FIRST_RUN = True
    if IN_PRODUCTION:
        IN_PRODUCTION = False
        
    print("Updating chains to newest values since you have not run this before, these will not be posted")
    runChecks()
    save_proposals()
    print("Run this again now, chains have been populated")
    exit(0)

if __name__ == "__main__":        
    updateChainsToNewestProposalsIfThisIsTheFirstTimeRunning()

    load_proposals_from_file()    
    _SetMaxArchiveDurationLength()

    # informs user & setups of length of time between runs
    if IN_PRODUCTION:
        SCHEDULE_SECONDS = 30*60
        print("[!] BOT IS RUNNING IN PRODUCTION MODE [!]")
        time.sleep(1)

        output = "[!] Running "
        if TICKERS_TO_ANNOUNCE == []:
            output += "all in 2 seconds"
        else:
            output += f"{TICKERS_TO_ANNOUNCE} in 2 seconds"
        print(output)
        time.sleep(2)
    else:
        SCHEDULE_SECONDS = 3
        print("Bot is in test mode...")

    if DISCORD:
        print("DISCORD module enabled")
    if TWITTER:
        print("TWITTER module enabled")
    if FETCH_LAST_PROP:
        print("Fetching last 2 proposals for each chain...")
    

    runChecks()

    # If user does not use a crontab, this can be run in a screen/daemon session
    if USE_PYTHON_RUNNABLE:      
        schedule.every(SCHEDULE_SECONDS).seconds.do(runChecks)  
        while True:
            print("Running runnable then waiting...")
            schedule.run_pending()
            time.sleep(SCHEDULE_SECONDS)
            

    
