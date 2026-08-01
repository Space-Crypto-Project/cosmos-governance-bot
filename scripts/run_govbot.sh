#!/usr/bin/env bash
# Cron-safe GovBot launcher: skips if a previous run still holds the lock.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LOCKFILE="${ROOT}/.govbot.lock"
LOGFILE="${ROOT}/cosmos-governance-bot.log"
MAX_LOG_LINES=20000

exec 9>"$LOCKFILE"
# `if ! flock` would reset $? to 0, so capture the status on the failure branch itself.
status=0
flock -n 9 || status=$?

if [ "$status" -eq 1 ]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) skipped: another GovBot instance holds $LOCKFILE" >> "$LOGFILE"
  exit 0
elif [ "$status" -ne 0 ]; then
  # e.g. 127 when flock is not installed: never report this to cron as a healthy run
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) flock failed with status $status" >> "$LOGFILE"
  exit "$status"
fi

if [ -f "$LOGFILE" ] && [ "$(wc -l < "$LOGFILE")" -gt "$MAX_LOG_LINES" ]; then
  tail -n "$MAX_LOG_LINES" "$LOGFILE" > "${LOGFILE}.trim" && mv "${LOGFILE}.trim" "$LOGFILE"
fi

python3 GovBot.py >> "$LOGFILE" 2>&1
