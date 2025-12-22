# Cosmos Governance Bot - AI Coding Agent Instructions

## Project Overview
Multi-platform notification bot monitoring Cosmos blockchain governance proposals. Sends notifications via Twitter, Discord (with threaded discussions), and email when new proposals enter voting period.

## Architecture

### Core Components
- **GovBot.py**: Main orchestrator - polls chain APIs, tracks proposal state, dispatches notifications
- **ChainApis.py**: Configuration registry mapping chain tickers to REST endpoints, explorer URLs, and Twitter handles
- **PostScan.py**: Standalone scanner for Discord/Twitter post monitoring with keyword-based email alerts

### Data Flow
1. Scheduled polling → Chain REST APIs (v1 or v1beta1 endpoints)
2. Proposal comparison → `chains.json` (persistent state: `{ticker: last_seen_proposal_id}`)
3. New proposals → Multi-channel notification dispatch
4. Error tracking → `errors.json` (consecutive failure counter per chain)

### Configuration System
- **secrets.json**: Feature toggles, API credentials, notification targets
- **chains.json**: Generated runtime state (auto-created on first run)
- Environment modes: `IN_PRODUCTION` (real notifications) vs test mode (dry run)

## Critical Patterns

### Dual API Version Support
Cosmos gov module has breaking changes between v1beta1 and v1:
```python
# v1: status is string "PROPOSAL_STATUS_VOTING_PERIOD"
# v1beta1: status may be integer 2 or string
if 'v1beta1' in link:
    version = 'v1beta'
    prop_id = prop['proposal_id']  # Note: underscore
else:
    version = 'v1'
    prop_id = prop['id']  # No underscore
```
**Always check API version in endpoint URL before parsing proposal structure.**

### Fallback Proposal Fetching
When bulk endpoint fails with runtime errors, individual proposal polling kicks in:
- `getAllProposalsWithFallback()` → tries bulk first, falls back to individual IDs
- Incremental scanning from `last_known_id + 1` until 5 consecutive 404s
- Immediately updates `chains.json` to prevent re-polling failed proposals

### Discord Integration (No Bot Process)
Uses Discord REST API directly via bot token - **no async client loop**:
1. Post webhook message → extract message_id from channel history
2. Create thread via `/channels/{id}/messages/{message_id}/threads`
3. Add reactions via PUT to `/channels/{id}/messages/{message_id}/reactions/{emoji}/@me`

Thread auto-archive duration respects server boost level (60/1440/4320/10080 minutes).

### First-Run Initialization
`updateChainsToNewestProposalsIfThisIsTheFirstTimeRunning()`:
- Detects missing `chains.json`, populates with current proposal IDs
- Runs in dry-run mode to avoid spamming all historical proposals
- **Must be completed before production use**

### Explorer URL Resolution
`get_explorer_link()` priority:
1. Custom links from `customExplorerLinks` (e.g., DIG, Terra with native UIs)
2. User's preferred explorer from `secrets.json` (ping/mintscan/keplr)
3. Fallback to first available explorer if preferred unavailable

## Development Workflows

### Adding New Chains
1. Get REST LCD endpoint from [cosmos/chain-registry](https://github.com/cosmos/chain-registry)
2. Add to `chainAPIs` dict in [ChainApis.py](ChainApis.py):
   ```python
   'ticker': [
       'https://api.example.com/cosmos/gov/v1/proposals',  # v1 or v1beta1
       {
           "ping": 'https://explorer.example.com/ticker/gov',
           "mintscan": 'https://mintscan.io/ticker/proposals'
       },
       '@TwitterHandle'
   ]
   ```
3. Test with `TICKERS_TO_ANNOUNCE: ["ticker"]` in secrets.json

### Testing Changes
```bash
# Dry run (no notifications, logs to console)
python3 GovBot.py  # Set IN_PRODUCTION: false in secrets.json

# Test last 2 proposals for all chains
# Set FETCH_LAST_PROP: true in secrets.json

# Filter specific chains
# Set TICKERS_TO_ANNOUNCE: ["osmo", "juno"] in secrets.json
```

### Deployment Options
**Cron (recommended)**:
```bash
*/30 * * * * cd /path/to/cosmos-governance-bot && python3 GovBot.py
```

**Python scheduler** (requires screen/daemon):
```bash
# Set USE_PYTHON_RUNNABLE: true in secrets.json
screen -S bot python3 GovBot.py
```

**Docker**:
```bash
docker build -t cosmos-gov-bot:0.0.1 .
docker run -it --rm --name gov-bot cosmos-gov-bot
```

## Common Pitfalls

1. **Encoding Errors**: Chain APIs may return invalid Unicode in proposal descriptions - fallback continues polling
2. **Runtime Errors**: Some chains' bulk endpoints fail with nil pointer - triggers individual proposal fetching
3. **Rate Limiting**: Discord reactions limited to 0.1s intervals (`REACTION_RATE_LIMIT`)
4. **Upgrade Proposals**: Extract `cosmovisor_folder` from `messages[0].plan.name` for v1 or `content.plan.name` for v1beta1
5. **State File Corruption**: `chains.json` must be valid JSON - missing/corrupt file triggers first-run mode

## Key Files Reference
- [secrets.sample.json](secrets.sample.json) - Complete configuration template
- [chains.sample.json](chains.sample.json) - Example state file structure  
- [ChainApis.py](ChainApis.py) lines 1-40 - Configuration structure documentation
- [GovBot.py](GovBot.py) lines 330-430 - Fallback fetching logic
- [README.md](README.md) - Discord bot setup + thread configuration

## Dependencies
Core: `discord.py>=2.0.0`, `tweepy==4.15.0`, `requests==2.27.1`, `schedule==1.1.0`
