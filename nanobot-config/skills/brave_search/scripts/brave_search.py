#!/usr/bin/env python3
"""
brave_search.py — Web search via Brave Search API.

Usage:
  python3 brave_search.py "<query>" [count]

Requires: BRAVE_API_KEY environment variable.
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import urllib.error


def search(query: str, count: int = 5) -> str:
    api_key = os.environ.get("BRAVE_API_KEY", "")
    if not api_key:
        return "La clé BRAVE_API_KEY n'est pas configurée."

    params = urllib.parse.urlencode({
        "q": query,
        "count": min(count, 20),
        "result_filter": "web",
    })
    url = f"https://api.search.brave.com/res/v1/web/search?{params}"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            # Handle gzip if needed
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                raw = gzip.decompress(raw)
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read())
            return f"Brave Search error: {err}"
        except Exception:
            return f"Brave Search HTTP error: {e}"
    except Exception as e:
        return f"Erreur réseau : {e}"

    web_results = data.get("web", {}).get("results", [])
    if not web_results:
        return f"Aucun résultat Brave Search pour : {query}"

    lines = [f"🦁 Résultats Brave Search pour : {query}\n"]
    for i, r in enumerate(web_results[:count], 1):
        title = r.get("title", "Sans titre")
        url_r = r.get("url", "")
        desc = (r.get("description") or "").strip()
        if len(desc) > 250:
            desc = desc[:250].rsplit(" ", 1)[0] + "..."
        lines.append(f"{i}. **{title}**\n   {desc}\n   🔗 {url_r}")

    return "\n\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: brave_search.py <query> [count]", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) >= 3 else 5

    print(search(query, count))


if __name__ == "__main__":
    main()
