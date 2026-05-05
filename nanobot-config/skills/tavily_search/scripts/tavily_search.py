#!/usr/bin/env python3
"""
tavily_search.py — Web search via Tavily AI Search API.

Usage:
  python3 tavily_search.py "<query>" [max_results]

Requires: TAVILY_API_KEY environment variable.
"""

import sys
import os
import json
import urllib.request
import urllib.error


def search(query: str, max_results: int = 5) -> str:
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        return "La clé TAVILY_API_KEY n'est pas configurée."

    payload = json.dumps({
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "include_raw_content": False,
        "max_results": min(max_results, 10),
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read())
            return f"Tavily error: {err.get('detail', str(e))}"
        except Exception:
            return f"Tavily HTTP error: {e}"
    except Exception as e:
        return f"Erreur réseau : {e}"

    lines = [f"🔍 Résultats Tavily pour : {query}\n"]

    answer = data.get("answer")
    if answer:
        lines.append(f"**Réponse directe :** {answer}\n")

    results = data.get("results", [])
    for i, r in enumerate(results[:max_results], 1):
        title = r.get("title", "Sans titre")
        url = r.get("url", "")
        content = r.get("content", "").strip()
        if len(content) > 300:
            content = content[:300].rsplit(" ", 1)[0] + "..."
        lines.append(f"{i}. **{title}**\n   {content}\n   🔗 {url}")

    if not results:
        lines.append("Aucun résultat trouvé.")

    return "\n\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: tavily_search.py <query> [max_results]", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 5

    print(search(query, max_results))


if __name__ == "__main__":
    main()
