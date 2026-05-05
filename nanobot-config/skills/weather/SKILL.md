---
name: weather
description: Get current weather and forecasts using wttr.in and Open-Meteo. No API key required.
metadata: {"nanobot":{"emoji":"🌤️","requires":{"bins":["python3"]}}}
---

# Weather

Fetch current weather or forecasts for any city.

## When to use

Use this skill when the user asks about weather, temperature, forecast, rain, wind, or conditions for any location.
Examples:
- "quel temps fait-il à Rennes ?"
- "météo Brest demain"
- "will it rain in Paris this week?"
- "température actuelle à Vannes"

## Tools available

### 1. wttr.in — quick one-line summary

```bash
python3 /app/nanobot-config/skills/weather/scripts/weather.py wttr <city>
```

Returns a compact one-line summary (condition, temperature, wind).
Use this for quick "what's the weather now" questions.

### 2. Open-Meteo — detailed forecast

```bash
python3 /app/nanobot-config/skills/weather/scripts/weather.py forecast <city>
```

Returns hourly/daily forecast data for the next 7 days.
Use this for "will it rain tomorrow", "forecast this week", or multi-day questions.

## Output interpretation

- Present temperature in °C (Sam is in France).
- Always mention the city name in the response.
- Keep the answer short — 2-3 lines max for a simple query.
- For multi-day forecasts, summarise trends rather than listing every hour.

## Rules

- One call per query. No retry loops.
- If the city is not found, ask the user to rephrase or provide a nearby major city.
- Default location: Rennes, Bretagne (if user says "ici" or "chez moi" without context).
