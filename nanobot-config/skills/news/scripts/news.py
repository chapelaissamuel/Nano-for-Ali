#!/usr/bin/env python3
"""
news.py — Fetch news via NewsAPI.

Usage:
  python3 news.py search "<query>" [lang]
  python3 news.py headlines [category] [country]

Requires: NEWSAPI_KEY environment variable.
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta


BASE_URL = "https://newsapi.org/v2"


def api_get(endpoint: str, params: dict) -> dict:
    api_key = os.environ.get("NEWSAPI_KEY", "")
    if not api_key:
        return {"error": "La clé NEWSAPI_KEY n'est pas configurée."}

    params["apiKey"] = api_key
    url = f"{BASE_URL}/{endpoint}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "NanoAUM/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read())
            return {"error": err.get("message", str(e))}
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def fmt_articles(articles: list, title: str) -> str:
    lines = [f"📰 {title}\n"]
    for i, a in enumerate(articles[:5], 1):
        art_title = a.get("title", "Sans titre") or "Sans titre"
        source = a.get("source", {}).get("name", "?")
        desc = (a.get("description") or "").strip()
        url = a.get("url", "")
        pub = (a.get("publishedAt") or "")[:10]

        if len(desc) > 200:
            desc = desc[:200].rsplit(" ", 1)[0] + "..."

        lines.append(f"{i}. **{art_title}**\n   {source} · {pub}\n   {desc}\n   🔗 {url}")

    return "\n\n".join(lines)


def search(query: str, lang: str = "fr") -> str:
    from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
    data = api_get("everything", {
        "q": query,
        "language": lang,
        "from": from_date,
        "sortBy": "relevancy",
        "pageSize": "5",
    })

    if "error" in data:
        return f"NewsAPI error: {data['error']}"

    articles = data.get("articles", [])
    if not articles:
        if lang == "fr":
            return search(query, "en")
        return f"Aucun article trouvé pour : {query}"

    return fmt_articles(articles, f"Actualités : {query}")


def headlines(category: str = "general", country: str = "fr") -> str:
    data = api_get("top-headlines", {
        "country": country,
        "category": category,
        "pageSize": "5",
    })

    if "error" in data:
        return f"NewsAPI error: {data['error']}"

    articles = data.get("articles", [])
    if not articles:
        return f"Aucune actualité trouvée ({category}, {country})."

    return fmt_articles(articles, f"Top actualités — {category} ({country.upper()})")


def main():
    if len(sys.argv) < 2:
        print("Usage: news.py <search|headlines> [args]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: news.py search <query> [lang]", file=sys.stderr)
            sys.exit(1)
        query = sys.argv[2]
        lang = sys.argv[3] if len(sys.argv) >= 4 else "fr"
        print(search(query, lang))

    elif cmd == "headlines":
        category = sys.argv[2] if len(sys.argv) >= 3 else "general"
        country = sys.argv[3] if len(sys.argv) >= 4 else "fr"
        print(headlines(category, country))

    else:
        print(f"Commande inconnue : '{cmd}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
