---
name: news
description: Fetch latest news articles using NewsAPI. Requires NEWSAPI_KEY.
metadata: {"nanobot":{"emoji":"📰","requires":{"bins":["python3"]}}}
---

# News

Fetch current news headlines and articles from NewsAPI.

## When to use

Use this skill when the user asks for:
- Latest news on a topic
- Recent headlines
- News from specific sources or countries

Examples:
- "dernières news sur l'IA"
- "actualité Bretagne aujourd'hui"
- "news about prediction markets"
- "quoi de neuf en archéologie cette semaine ?"

## How to use

### Search by keyword

```bash
python3 /app/nanobot-config/skills/news/scripts/news.py search "<query>" [lang]
```

- `lang`: `fr` (default) or `en`

### Top headlines by category

```bash
python3 /app/nanobot-config/skills/news/scripts/news.py headlines [category] [country]
```

- `category`: general, science, technology, business, health, entertainment, sports
- `country`: `fr` (default) or `us`, `gb`, etc.

### Example calls

```bash
python3 /app/nanobot-config/skills/news/scripts/news.py search "archaeoacoustics" en
python3 /app/nanobot-config/skills/news/scripts/news.py search "marchés prédictifs" fr
python3 /app/nanobot-config/skills/news/scripts/news.py headlines science fr
```

## Output interpretation

- Present 3–5 articles with title, source, and a 1-sentence summary.
- Include publication date for time-sensitive topics.
- Summarise in the user's language regardless of article language.

## Environment variable required

`NEWSAPI_KEY` must be set in Railway Variables.

## Rules

- One call per query. No retry loops.
- If the API key is missing, say: "La clé NEWSAPI_KEY n'est pas configurée."
- NewsAPI free tier: articles up to 1 month old, 100 requests/day.
