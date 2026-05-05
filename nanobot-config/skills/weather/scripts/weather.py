#!/usr/bin/env python3
"""
weather.py — Fetch weather via wttr.in or Open-Meteo.

Usage:
  python3 weather.py wttr <city>
  python3 weather.py forecast <city>
"""

import sys
import json
import urllib.request
import urllib.parse


def wttr(city: str) -> str:
    city_enc = urllib.parse.quote(city)
    url = f"https://wttr.in/{city_enc}?format=3"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8").strip()
    except Exception as e:
        return f"Erreur wttr.in : {e}"


def geocode(city: str):
    """Return (lat, lon) for a city using Open-Meteo geocoding."""
    city_enc = urllib.parse.quote(city)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_enc}&count=1&language=fr&format=json"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())
    results = data.get("results")
    if not results:
        return None, None
    r = results[0]
    return r["latitude"], r["longitude"]


def forecast(city: str) -> str:
    lat, lon = geocode(city)
    if lat is None:
        return f"Ville '{city}' introuvable."

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode"
        f"&current_weather=true"
        f"&timezone=Europe%2FParis"
        f"&forecast_days=7"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())

    cw = data.get("current_weather", {})
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    t_max = daily.get("temperature_2m_max", [])
    t_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])

    wmo_codes = {
        0: "Ciel dégagé", 1: "Peu nuageux", 2: "Partiellement nuageux", 3: "Couvert",
        45: "Brouillard", 48: "Brouillard givrant",
        51: "Bruine légère", 53: "Bruine modérée", 55: "Bruine dense",
        61: "Pluie légère", 63: "Pluie modérée", 65: "Pluie forte",
        71: "Neige légère", 73: "Neige modérée", 75: "Neige forte",
        80: "Averses légères", 81: "Averses modérées", 82: "Averses violentes",
        95: "Orage", 96: "Orage avec grêle", 99: "Orage violent",
    }
    wcodes = daily.get("weathercode", [])

    lines = [f"📍 {city.title()} — Prévisions 7 jours\n"]
    lines.append(f"Maintenant : {cw.get('temperature', '?')}°C, vent {cw.get('windspeed', '?')} km/h\n")
    for i, d in enumerate(dates):
        cond = wmo_codes.get(wcodes[i] if i < len(wcodes) else 0, "?")
        prc = precip[i] if i < len(precip) else 0
        lines.append(
            f"{d} : {t_min[i] if i < len(t_min) else '?'}–{t_max[i] if i < len(t_max) else '?'}°C, "
            f"{cond}, pluie {prc}mm"
        )
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: weather.py <wttr|forecast> <city>", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1].lower()
    city = " ".join(sys.argv[2:])

    if mode == "wttr":
        print(wttr(city))
    elif mode == "forecast":
        print(forecast(city))
    else:
        print(f"Mode inconnu : '{mode}'. Utilise 'wttr' ou 'forecast'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
