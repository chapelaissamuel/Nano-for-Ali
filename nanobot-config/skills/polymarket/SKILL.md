---
name: polymarket
description: Fetch prediction market data from Polymarket Gamma API. No API key required.
metadata: {"nanobot":{"emoji":"📊","requires":{"bins":["python3"]}}}
---

# Polymarket

Fetch prediction market probabilities and market data from Polymarket via the Gamma API.

## When to use

Use this skill when the user asks about:
- Prediction market odds or probabilities
- "What does Polymarket say about X?"
- Political, economic, or event probability questions
- "Chances de X selon les marchés ?"

Examples:
- "polymarket trump 2024"
- "proba selon les marchés que X arrive"
- "quelles sont les cotes sur Polymarket pour [événement]"

## How to use

### Search markets

```bash
python3 /app/nanobot-config/skills/polymarket/scripts/polymarket.py search "<query>"
```

### Get top active markets

```bash
python3 /app/nanobot-config/skills/polymarket/scripts/polymarket.py top
```

### Get specific market by ID or slug

```bash
python3 /app/nanobot-config/skills/polymarket/scripts/polymarket.py market "<slug_or_id>"
```

## Output interpretation

- Present probabilities as percentages (e.g. "67% de chances").
- Include market volume and end date when relevant.
- Keep the answer factual and neutral — these are crowd-sourced probabilities, not predictions.
- Always note that Polymarket odds reflect market consensus, not certainty.

## Rules

- One call per query. No retry loops.
- If no matching market is found, report clearly and suggest a rephrased query.
- Gamma API base URL: `https://gamma-api.polymarket.com`
