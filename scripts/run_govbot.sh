#!/usr/bin/env bash
# Cron entry point for GovBot. Locking behaviour lives in run_locked.sh.
set -euo pipefail
exec "$(cd "$(dirname "$0")" && pwd)/run_locked.sh" GovBot.py cosmos-governance-bot.log .govbot.lock
