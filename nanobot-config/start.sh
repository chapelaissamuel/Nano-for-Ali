#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$SCRIPT_DIR/config.json"

if [ -z "$GEMINI_API_KEY" ]; then
  echo "ERROR: GEMINI_API_KEY is not set."
  exit 1
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN is not set."
  exit 1
fi

echo -n "$TELEGRAM_BOT_TOKEN" > /tmp/.tg_token
chmod 600 /tmp/.tg_token

echo "Starting NanoBot (gemini-2.5-flash via Google AI)..."
python3 -m nanobot gateway --config "$CONFIG"
