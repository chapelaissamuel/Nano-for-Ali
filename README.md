# Nano-for-Ali

Personal AI assistant powered by [nanobot](https://github.com/HKUDS/nanobot),
using **Anthropic Claude Sonnet** via **OpenRouter** and **Telegram** as the channel.

## Setup

### 1. Set your secrets

| Variable             | Where to get it                |
|----------------------|-------------------------------|
| `OPENROUTER_API_KEY` | https://openrouter.ai/keys     |
| `TELEGRAM_BOT_TOKEN` | @BotFather on Telegram         |

Set them as Replit Secrets or environment variables — **never hardcode them**.

### 2. Install nanobot

```bash
pip install -e .
```

### 3. Start the bot

```bash
bash nanobot-config/start.sh
```

## Configuration

`nanobot-config/config.json` holds all bot settings.  
API keys are injected at runtime via `${OPENROUTER_API_KEY}` and `${TELEGRAM_BOT_TOKEN}`.

- **LLM**: `anthropic/claude-sonnet-4-5` via OpenRouter  
- **Channel**: Telegram (long-polling, streaming enabled)

## Project structure

```
nanobot/                  ← nanobot source (pip install -e .)
nanobot-config/
  config.json             ← bot config (no hardcoded secrets)
  start.sh                ← startup script with pre-flight checks
  .env.example            ← template for required env vars
README.md
```
