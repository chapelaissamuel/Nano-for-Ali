---
name: reminders
description: Schedule one-time or recurring reminders for the user using nanobot's built-in cron system.
metadata: {"nanobot":{"emoji":"⏰"}}
---

# Reminders

Schedule reminders using the built-in `cron` tool.

## When to use

Use this skill when the user says anything like:
- "rappelle moi à 22h59 de manger"
- "remind me at 8am to take my pills"
- "every day at 7h30 send me a motivational message"
- "dans 30 minutes, rappelle moi d'appeler Ali"

## Timezone

Default timezone: `Africa/Abidjan` (UTC+0).
If the user's location implies a different timezone, use the correct IANA name (e.g. `Europe/Paris`, `America/New_York`).

## How to schedule

### One-time reminder (specific time today or a given date)

Compute the full ISO datetime from the current time, then:

```
cron(action="add", message="Rappel : manger", at="2026-04-08T22:59:00", tz="Africa/Abidjan")
```

Note: `tz` cannot be used with `at` — convert the local time to UTC manually when using `at`.
Use `cron_expr` + `tz` instead for timezone-aware one-time scheduling via a date-specific cron expression.

### Recurring reminder (every day at a fixed time)

```
cron(action="add", message="Rappel : manger", cron_expr="59 22 * * *", tz="Africa/Abidjan")
```

### Relative reminder (in N minutes/hours)

Compute the ISO datetime = now + offset, then:

```
cron(action="add", message="Rappel : appeler Ali", at="<computed ISO datetime>")
```

### List scheduled reminders

```
cron(action="list")
```

### Cancel a reminder

```
cron(action="remove", job_id="<id from list>")
```

## Confirmation message

After successfully scheduling, always confirm with the exact time and message:

```
✅ Rappel programmé pour 22h59 : manger
```

Use the user's phrasing for the reminder text. Include the timezone if it differs from the default.

## At trigger time

When the cron fires, send the reminder message directly to the user. Keep it short:

```
⏰ Rappel : manger
```

## Rules

- Always confirm the scheduled time in the user's local time, not UTC.
- If the time has already passed today, schedule for the next occurrence and say so.
- If scheduling fails, report the error clearly and ask the user to rephrase.
- NEVER silently drop a reminder request.
