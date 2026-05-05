#!/usr/bin/env python3
"""
polymarket.py — Fetch prediction market data from Polymarket Gamma API.

Usage:
  python3 polymarket.py search "<query>"
  python3 polymarket.py top
  python3 polymarket.py market "<slug_or_id>"
"""

import sys
import json
import urllib.request
import urllib.parse

BASE_URL = "https://gamma-api.polymarket.com"


def api_get(path: str, params: dict = None) -> dict:
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def fmt_market(m: dict) -> str:
    title = m.get("question", m.get("title", "?"))
    slug = m.get("slug", "")
    volume = m.get("volume", 0)
    end = m.get("endDate", m.get("end_date", ""))[:10] if m.get("endDate") or m.get("end_date") else "?"
    url = f"https://polymarket.com/event/{slug}" if slug else ""

    outcomes = m.get("outcomes", [])
    prices = m.get("outcomePrices", [])

    lines = [f"📊 **{title}**"]
    if isinstance(outcomes, list) and isinstance(prices, list):
        for i, outcome in enumerate(outcomes[:4]):
            try:
                pct = round(float(prices[i]) * 100, 1) if i < len(prices) else "?"
            except (ValueError, TypeError):
                pct = "?"
            lines.append(f"  • {outcome}: {pct}%")
    elif isinstance(outcomes, str):
        try:
            out_list = json.loads(outcomes)
            price_list = json.loads(prices) if isinstance(prices, str) else prices
            for i, outcome in enumerate(out_list[:4]):
                try:
                    pct = round(float(price_list[i]) * 100, 1) if i < len(price_list) else "?"
                except (ValueError, TypeError):
                    pct = "?"
                lines.append(f"  • {outcome}: {pct}%")
        except Exception:
            pass

    if volume:
        try:
            lines.append(f"  Volume: ${float(volume):,.0f}")
        except (ValueError, TypeError):
            pass
    lines.append(f"  Clôture: {end}")
    if url:
        lines.append(f"  🔗 {url}")
    return "\n".join(lines)


def search(query: str) -> str:
    try:
        data = api_get("/markets", {"_search": query, "active": "true", "closed": "false", "_limit": "5"})
    except Exception as e:
        return f"Erreur Polymarket API : {e}"

    if not data:
        return f"Aucun marché trouvé pour : {query}"

    markets = data if isinstance(data, list) else data.get("data", data.get("markets", []))
    if not markets:
        return f"Aucun marché trouvé pour : {query}"

    results = [fmt_market(m) for m in markets[:5]]
    return "\n\n".join(results)


def top() -> str:
    try:
        data = api_get("/markets", {"active": "true", "closed": "false", "_limit": "5", "_order": "volume"})
    except Exception as e:
        return f"Erreur Polymarket API : {e}"

    markets = data if isinstance(data, list) else data.get("data", data.get("markets", []))
    if not markets:
        return "Impossible de récupérer les marchés actifs."

    results = [fmt_market(m) for m in markets[:5]]
    return "🔝 Top marchés Polymarket\n\n" + "\n\n".join(results)


def market(slug_or_id: str) -> str:
    try:
        data = api_get(f"/markets/{urllib.parse.quote(slug_or_id)}")
    except Exception as e:
        return f"Erreur Polymarket API : {e}"

    if not data:
        return f"Marché introuvable : {slug_or_id}"

    return fmt_market(data)


def main():
    if len(sys.argv) < 2:
        print("Usage: polymarket.py <search|top|market> [args]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: polymarket.py search <query>", file=sys.stderr)
            sys.exit(1)
        print(search(" ".join(sys.argv[2:])))

    elif cmd == "top":
        print(top())

    elif cmd == "market":
        if len(sys.argv) < 3:
            print("Usage: polymarket.py market <slug_or_id>", file=sys.stderr)
            sys.exit(1)
        print(market(sys.argv[2]))

    else:
        print(f"Commande inconnue : '{cmd}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
