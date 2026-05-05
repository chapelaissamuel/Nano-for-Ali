---
name: wikipedia
description: Search and fetch article summaries from Wikipedia (French and English). No API key required.
metadata: {"nanobot":{"emoji":"📚","requires":{"bins":["python3"]}}}
---

# Wikipedia

Search Wikipedia and retrieve article summaries or full extracts.

## When to use

Use this skill when the user asks about a topic, concept, person, place, or event and needs factual background information.
Examples:
- "c'est quoi la piézoélectricité ?"
- "wiki sur les grottes Barabar"
- "qui est Kuramoto ?"
- "wikipedia archaeoacoustics"

## How to use

### Search + summary (default)

```bash
python3 /app/nanobot-config/skills/wikipedia/scripts/wikipedia.py "<query>" [lang]
```

- `lang`: `fr` (default) or `en`
- Returns: article title + first 3–5 paragraphs

### Example calls

```bash
python3 /app/nanobot-config/skills/wikipedia/scripts/wikipedia.py "grottes Barabar" fr
python3 /app/nanobot-config/skills/wikipedia/scripts/wikipedia.py "piezoelectricity" en
python3 /app/nanobot-config/skills/wikipedia/scripts/wikipedia.py "Kuramoto model" en
```

## Output interpretation

- Present the summary in the user's language (French or English).
- If the article is long, give the key points in 3–5 sentences and offer to go deeper.
- If no article is found in `fr`, automatically retry in `en` and note the language.
- Always cite the Wikipedia article title.

## Rules

- One search per query. No retry loops unless switching language.
- If the topic is ambiguous, present the top result and ask if it's the right one.
