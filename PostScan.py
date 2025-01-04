# exec:
# python3 PostScan.py

import json
import tweepy
import schedule
import time
import discord
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone

from ChainApis import chainAPIs, customExplorerLinks, DAOs

with open('secrets.json', 'r') as f:
    secrets = json.load(f)

    TWITTER_SCAN = secrets['TWITTER']['ENABLE_POST_SCAN']
    DISCORD_SCAN = secrets['DISCORD_THREADS']['ENABLE_POST_SCAN']
    POST_NOTIFICATION = secrets['EMAIL']['POST_NOTIFICATION']


    if TWITTER_SCAN:
        # Twitter API credentials
        twitSecrets = secrets['TWITTER']

        APIKEY = twitSecrets['APIKEY']
        APIKEYSECRET = twitSecrets['APIKEYSECRET']
        ACCESS_TOKEN = twitSecrets['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = twitSecrets['ACCESS_TOKEN_SECRET']  

        # Authenticate to Twitter & Get API
        auth = tweepy.OAuth1UserHandler(APIKEY, APIKEYSECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True)

        def search_tweets(ticker):
            # Retrieve the @username from chainAPIs
            username = chainAPIs[ticker][2]

            # Define the search keyword and the number of tweets to retrieve
            search_keyword = f"from:{username}"
            num_tweets = 1

            # Search for tweets
            tweets = tweepy.Cursor(api.search_tweets, q=search_keyword, lang="en").items(num_tweets)

            # Print the tweets
            for tweet in tweets:
                print(f"Tweet by @{tweet.user.screen_name}: {tweet.text}\n")

        # Example usage: search tweets for a specific ticker
        ticker = 'juno'  # Replace with the desired ticker
        search_tweets(ticker)

    if DISCORD_SCAN:
        # Discord API credentials
        DISCORD_TOKEN = secrets['DISCORD_THREADS']['BOT_TOKEN']
        CHANNEL_IDS = secrets['DISCORD_THREADS']['CHANNEL_ID']
        POST_KEYWORDS = secrets['DISCORD_THREADS']['POST_KEYWORDS']

        EMAIL_ENABLED = secrets['EMAIL']['ENABLED']
        EMAIL_HOST = secrets['EMAIL']['HOST']
        EMAIL_PORT = secrets['EMAIL']['PORT']
        EMAIL_USERNAME = secrets['EMAIL']['USERNAME']
        EMAIL_PASSWORD = secrets['EMAIL']['PASSWORD']
        EMAIL_FROM = secrets['EMAIL']['FROM']
        EMAIL_TO = secrets['EMAIL']['TO']
        SSL = secrets['EMAIL']['SSL']

        intents = discord.Intents.default()
        intents.messages = True  # Enable message-related events
        client = discord.Client(intents=intents)

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

        async def scan_channel(channel_id):
            await client.wait_until_ready()

            # Get the channel
            channel = client.get_channel(channel_id)
            if channel is None:
                print(f"Channel with ID {channel_id} not found.")
                return

            try:
                # Fetch the last 100 messages
                messages = await channel.history(limit=100).flatten()
                print(f"Fetched {len(messages)} messages from channel {channel.name}.")

                # Check for keywords in messages
                keywords = POST_KEYWORDS
                now = datetime.now(timezone.utc)
                x_hours_ago = now - timedelta(hours=4)

                for message in messages:
                    # Ensure message.created_at is timezone-aware
                    message_time = message.created_at.replace(tzinfo=timezone.utc)
                    # Skip messages older than X hours
                    if message_time < x_hours_ago:
                        continue

                    if any(keyword in message.content.lower() for keyword in keywords):
                        # show which keyword was found    
                        for keyword in keywords:
                            if keyword in message.content.lower():
                                print(f"Keyword '{keyword}' found in message by {message.author} - {message.created_at}")
                                if POST_NOTIFICATION:
                                    subject = f"Keyword '{keyword}' found in Discord message"
                                    body = (f"Keyword '{keyword}' found in message by {message.author}:\n\n"
                                            f"Date: {message.created_at}\n"
                                            f"Content: {message.content}")
                                    send_email(subject, body)
                    # else:
                        # print(f"No keywords found in message by {message.author}: {message.content}")
            except discord.Forbidden:
                print("Bot lacks permissions to read messages in the channel.")
            except Exception as e:
                print(f"Error while fetching messages: {e}")

        async def scan_channels():
            await client.wait_until_ready()
            tasks = [scan_channel(channel_id) for channel_id in CHANNEL_IDS]
            await asyncio.gather(*tasks)
            await client.close()

        # Run the Discord bot
        loop = asyncio.get_event_loop()
        loop.create_task(scan_channels())
        client.run(DISCORD_TOKEN)