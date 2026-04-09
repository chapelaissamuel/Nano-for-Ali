#!/bin/sh
# Write token to file before nanobot starts.
# Required because nanobot's shell tool strips env vars from subprocesses.
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo -n "$TELEGRAM_BOT_TOKEN" > /tmp/.tg_token
    chmod 600 /tmp/.tg_token
fi
exec nanobot "$@"
