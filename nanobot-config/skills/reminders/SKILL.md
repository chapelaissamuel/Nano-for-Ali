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

Default timezone: `Europe/Paris` (matches the bot's configured timezone).
Override only if the user explicitly specifies a different location.

## How to schedule

### One-time reminder (specific time today or a given date)

Use `cron_expr` + `tz` for timezone-aware one-time scheduling:

```
cron(action="add", message="Rappel : manger", cron_expr="59 22 8 4 *", tz="Europe/Paris")
```

Or use `at` with a naive ISO datetime (interpreted in the bot's default timezone, Europe/Paris):

```
cron(action="add", message="Rappel : manger", at="2026-04-08T22:59:00")
```

Note: `tz` cannot be combined with `at` — use `cron_expr` + `tz` for explicit timezone control.

### Recurring reminder (every day at a fixed time)

```
cron(action="add", message="Rappel : manger", cron_expr="59 22 * * *", tz="Europe/Paris")
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

Use the user's phrasing for the reminder text.

## At trigger time

When the cron fires, send the reminder message directly to the user. Keep it short:

```
⏰ Rappel : manger
```

## Rules

- Always confirm the scheduled time in Europe/Paris local time.
- If the time has already passed today, schedule for the next occurrence and say so.
- If scheduling fails, report the error clearly and ask the user to rephrase.
- NEVER silently drop a reminder request.
