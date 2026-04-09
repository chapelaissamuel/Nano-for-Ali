#!/bin/bash
# Start NanoBot with Telegram + OpenRouter (Claude Sonnet)
# Make sure OPENROUTER_API_KEY and TELEGRAM_BOT_TOKEN are set before running.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="/usr/local/bin/python3"
CONFIG="$SCRIPT_DIR/config.json"

if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "ERROR: OPENROUTER_API_KEY is not set."
  exit 1
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN is not set."
  exit 1
fi

# Write token to file so scripts called by the agent can read it
# (nanobot strips env vars from subprocesses for security)
echo -n "$TELEGRAM_BOT_TOKEN" > /tmp/.tg_token
chmod 600 /tmp/.tg_token

echo "Starting NanoBot (Telegram + OpenRouter Claude Sonnet)..."
"$PYTHON" -m nanobot gateway --config "$CONFIG"
