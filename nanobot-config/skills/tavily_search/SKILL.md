---
name: tavily_search
description: Web search using Tavily AI Search API. Returns clean, relevant results optimized for AI agents. Requires TAVILY_API_KEY.
metadata: {"nanobot":{"emoji":"🔍","requires":{"bins":["python3"]}}}
---

# Tavily Search

AI-optimized web search. Returns clean, relevant excerpts — not raw HTML.

## When to use

Use this skill for general web searches when the user needs:
- Recent information (news, events, publications)
- Research on a topic not covered by Wikipedia
- Source verification or fact-checking
- Academic or scientific papers

Examples:
- "cherche des infos sur l'archéoacoustique et granite"
- "dernières news sur les marchés prédictifs"
- "recherche web : synchronisation Kuramoto piezoelectric caves"

## How to use

```bash
python3 /app/nanobot-config/skills/tavily_search/scripts/tavily_search.py "<query>" [max_results]
```

- `max_results`: optional, default 5, max 10

### Example calls

```bash
python3 /app/nanobot-config/skills/tavily_search/scripts/tavily_search.py "Barabar caves granite piezoelectricity" 5
python3 /app/nanobot-config/skills/tavily_search/scripts/tavily_search.py "Kuramoto synchronization archaeoacoustics" 5
```

## Output interpretation

- Summarise the top 3–5 results in 2–3 sentences each.
- Include source URLs for any claim the user might want to verify.
- If results are in English and user asked in French, summarise in French.

## Environment variable required

`TAVILY_API_KEY` must be set in Railway Variables.

## Rules

- One search per query. No retry loops.
- If the API key is missing, say: "La clé TAVILY_API_KEY n'est pas configurée."
- If no results found, suggest rephrasing or trying brave_search.
