#!/usr/bin/env bash
# Cron-safe GovBot launcher: skips if a previous run still holds the lock.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LOCKFILE="${ROOT}/.govbot.lock"
LOGFILE="${ROOT}/cosmos-governance-bot.log"

exec 9>"$LOCKFILE"
if ! flock -n 9; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) skipped: another GovBot instance holds $LOCKFILE" >> "$LOGFILE"
  exit 0
fi

python3 GovBot.py > "$LOGFILE" 2>&1
