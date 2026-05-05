---
name: brave_search
description: Web search using Brave Search API. Privacy-focused, independent index. Requires BRAVE_API_KEY.
metadata: {"nanobot":{"emoji":"🦁","requires":{"bins":["python3"]}}}
---

# Brave Search

Privacy-focused web search with an independent index. Good complement to Tavily.

## When to use

Use this skill when:
- Tavily search returns no results or poor results
- User explicitly asks for a web search
- Looking for recent or niche content not indexed by typical search engines

Examples:
- "recherche brave : synchronisation Kuramoto grottes"
- "trouve moi des articles sur la piézoélectricité des roches granitiques"
- "search: AUM NEXUS prediction markets"

## How to use

```bash
python3 /app/nanobot-config/skills/brave_search/scripts/brave_search.py "<query>" [count]
```

- `count`: number of results, default 5, max 20

### Example calls

```bash
python3 /app/nanobot-config/skills/brave_search/scripts/brave_search.py "Barabar caves acoustic resonance" 5
python3 /app/nanobot-config/skills/brave_search/scripts/brave_search.py "podcast archéoacoustique France" 5
```

## Output interpretation

- Present top 3–5 results with title, URL, and a 1–2 sentence description.
- Summarise findings in the user's language.
- Include URLs for sources the user may want to explore.

## Environment variable required

`BRAVE_API_KEY` must be set in Railway Variables.
Get your key at: https://search.brave.com/app/keys

## Rules

- One search per query. No retry loops.
- If the API key is missing, say: "La clé BRAVE_API_KEY n'est pas configurée."
- If results are sparse, suggest trying tavily_search instead.
