# Development Plan

## V1 Goal

Build a local desktop application that lets a user type a natural-language scheduling request, converts it into structured event data with AI, validates the data, asks the user for confirmation, and creates the event in Google Calendar.

## V1 Data Contract

```json
{
  "action": "create_event",
  "title": "Boxing",
  "start": "2026-09-25T19:00:00",
  "end": "2026-09-25T20:00:00",
  "timezone": "America/Boise",
  "reminder_minutes": 30
}
```

## Default Rules

- Allowed action: `create_event`
- Default event duration: 1 hour
- AI output is treated as untrusted input
- Validation happens before user confirmation
- User confirmation happens before Google Calendar execution
- Confirmation state is controlled by the application, not the AI

## Planned Build Order

1. Set up Python environment
2. Create the basic PySide6 desktop window
3. Accept text input from the user
4. Define the event data structure
5. Build deterministic validation
6. Add AI parsing
7. Show parsed event in the UI
8. Add user confirmation
9. Add Google OAuth 2.0
10. Create Google Calendar events
11. Add tests
12. Polish README and demo
