#!/usr/bin/env python3
"""
wikipedia.py — Search Wikipedia and return article summaries.

Usage:
  python3 wikipedia.py "<query>" [lang]
  lang: fr (default) or en
"""

import sys
import json
import urllib.request
import urllib.parse


def search_and_fetch(query: str, lang: str = "fr") -> str:
    # Step 1: search for the article
    search_url = (
        f"https://{lang}.wikipedia.org/w/api.php"
        f"?action=query&list=search&srsearch={urllib.parse.quote(query)}"
        f"&format=json&utf8=1&srlimit=1"
    )
    with urllib.request.urlopen(search_url, timeout=10) as resp:
        search_data = json.loads(resp.read())

    results = search_data.get("query", {}).get("search", [])
    if not results:
        return None

    title = results[0]["title"]

    # Step 2: fetch the extract
    extract_url = (
        f"https://{lang}.wikipedia.org/w/api.php"
        f"?action=query&prop=extracts&exintro=1&explaintext=1"
        f"&titles={urllib.parse.quote(title)}"
        f"&format=json&utf8=1"
    )
    with urllib.request.urlopen(extract_url, timeout=10) as resp:
        extract_data = json.loads(resp.read())

    pages = extract_data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))
    extract = page.get("extract", "").strip()

    if not extract:
        return None

    # Truncate to ~2000 chars
    if len(extract) > 2000:
        extract = extract[:2000].rsplit(".", 1)[0] + "."

    wiki_url = f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
    return f"📚 **{title}** (Wikipedia {lang.upper()})\n\n{extract}\n\n🔗 {wiki_url}"


def main():
    if len(sys.argv) < 2:
        print("Usage: wikipedia.py <query> [lang]", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) >= 3 else "fr"

    result = search_and_fetch(query, lang)

    if result is None and lang == "fr":
        # Retry in English
        result = search_and_fetch(query, "en")
        if result:
            result = "[Article trouvé en anglais]\n\n" + result

    if result is None:
        print(f"Aucun article Wikipedia trouvé pour : {query}")
        sys.exit(0)

    print(result)


if __name__ == "__main__":
    main()
