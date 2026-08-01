#!/usr/bin/env bash
# Serialised launcher shared by the cron entry points: runs a bot script under a
# non-blocking flock, so a cron tick landing on a still-running pass is skipped
# instead of doubling the request rate against the LCD APIs.
#
# usage: run_locked.sh <python-script> <log-file-name> <lock-file-name>
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "usage: $(basename "$0") <python-script> <log-file-name> <lock-file-name>" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SCRIPT="$1"
LOGFILE="${ROOT}/$2"
LOCKFILE="${ROOT}/$3"

exec 9>"$LOCKFILE"
# `if ! flock` would reset $? to 0, so capture the status on the failure branch itself.
status=0
flock -n 9 || status=$?

if [ "$status" -eq 1 ]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) skipped $SCRIPT: another instance holds $LOCKFILE" >> "$LOGFILE"
  exit 0
elif [ "$status" -ne 0 ]; then
  # e.g. 127 when flock is not installed: never report this to cron as a healthy run
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) flock failed with status $status" >> "$LOGFILE"
  exit "$status"
fi

# Log size is capped by logrotate (scripts/logrotate.govbot), not here: rotating from
# this script would swap the inode under a concurrent skip append and lose that record.
python3 "$SCRIPT" >> "$LOGFILE" 2>&1
