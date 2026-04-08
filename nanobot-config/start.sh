#!/bin/bash
# Start NanoBot with Telegram + Anthropic Claude Sonnet
# Make sure ANTHROPIC_API_KEY and TELEGRAM_BOT_TOKEN are set before running.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="/home/runner/workspace/.pythonlibs/bin/python3"
CONFIG="$SCRIPT_DIR/config.json"

if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "ERROR: OPENROUTER_API_KEY is not set."
  exit 1
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN is not set."
  exit 1
fi

echo "Starting NanoBot (Telegram + Anthropic Claude Sonnet)..."
"$PYTHON" -m nanobot gateway --config "$CONFIG"
