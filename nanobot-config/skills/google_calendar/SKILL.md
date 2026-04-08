---
name: google_calendar
description: Read, create, and update Google Calendar events via the Google Calendar MCP server.
metadata: {"nanobot":{"emoji":"📅"}}
---

# Google Calendar

Interact with the user's Google Calendar using the `google-calendar` MCP server tools.

## When to use

Use this skill when the user asks to:
- See their schedule, agenda, or upcoming events
- Create, add, or book an event or meeting
- Update, move, or reschedule an event
- Delete or cancel an event
- Check availability at a specific time

## Available MCP tools

The `google-calendar` MCP server exposes these tools — call them directly:

| Tool | When to use |
|------|-------------|
| `list_events` | Show upcoming or scheduled events |
| `create_event` | Add a new event to the calendar |
| `update_event` | Modify an existing event (time, title, description) |
| `delete_event` | Remove an event |
| `get_event` | Fetch details of a specific event |

## Common workflows

### Show agenda

```
list_events(timeMin="<now ISO>", timeMax="<end of day ISO>", maxResults=10)
```

Present results in a clean list: time, title, location (if any).

### Create an event

```
create_event(
  summary="Réunion avec Ali",
  start={"dateTime": "2026-04-09T14:00:00", "timeZone": "Europe/Paris"},
  end={"dateTime": "2026-04-09T15:00:00", "timeZone": "Europe/Paris"},
  description="..."
)
```

Confirm with: `✅ Événement créé : Réunion avec Ali — jeudi 9 avril à 14h00`

### Update an event

Fetch the event ID first with `list_events` or `get_event`, then:

```
update_event(eventId="<id>", summary="Nouveau titre", start={...}, end={...})
```

Confirm with: `✅ Événement mis à jour.`

### Delete an event

```
delete_event(eventId="<id>")
```

Confirm with: `✅ Événement supprimé.`

## Rules

- Always use `Europe/Paris` as the default timezone unless the user specifies otherwise.
- Confirm every write action (create/update/delete) with a short French confirmation.
- If an MCP tool call fails, report the error in one sentence and suggest retrying or checking permissions.
- NEVER invent event IDs — always retrieve them first.
- For ambiguous times ("tomorrow afternoon"), ask for clarification before creating.
