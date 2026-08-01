#!/usr/bin/env bash
# Cron entry point for PostScan. Locking behaviour lives in run_locked.sh.
set -euo pipefail
exec "$(cd "$(dirname "$0")" && pwd)/run_locked.sh" PostScan.py cosmos-posts-scan-bot.log .postscan.lock
