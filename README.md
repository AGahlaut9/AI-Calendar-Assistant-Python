# AI Calendar Assistant

AI Calendar Assistant is a desktop-first application that converts natural-language scheduling requests into validated Google Calendar events.

The initial version will run locally as a standalone desktop program written in Python. Future versions may expand to Android, macOS, and iPhone.

## Project Goal

The user should be able to type a request such as:

> Add boxing Friday at 7 PM and remind me 30 minutes before.

The application will:

1. Receive the user's natural-language request.
2. Send the request to an AI model for interpretation.
3. Convert the request into structured calendar data.
4. Validate the AI-generated data locally.
5. Display the interpreted event to the user.
6. Require user confirmation.
7. Create the event through the Google Calendar API.

The long-term goal is to also support voice input so a user can speak a scheduling request instead of typing it.

---

## V1 Architecture

```text
User
  ↓
Python Desktop Application
  ↓
AI Service
  ↓
Structured Event Data
  ↓
Local Validation
  ↓
User Confirmation
  ↓
Google Calendar Service
  ↓
Google Calendar API
```

V1 does not require its own application server.

The application logic runs locally on the user's computer and communicates directly with external services such as the AI provider and Google Calendar.

---

## Planned Technology Stack

* Python
* PySide6
* OpenAI API
* Google Calendar API
* Google OAuth 2.0
* JSON
* Git
* GitHub

---

## Why Python?

Python will be used for the main application logic.

Python was selected because it is:

* readable and easy to maintain
* widely used for AI applications
* well suited for API communication
* strong for data validation and processing
* easy to test
* useful for cybersecurity and automation projects
* appropriate for building the core logic of the application

Using Python also makes it easier to understand and explain how the AI, validation, authentication, and calendar components work.

---

## Why PySide6?

PySide6 will be used to create the desktop interface.

PySide6 is the official Python binding for the Qt framework and allows the application to run as a normal desktop program rather than requiring a web browser.

The desktop interface will initially contain:

* a text input field
* a submit button
* an event preview
* a confirmation button
* error and status messages

Future versions may include:

* microphone input
* calendar previews
* settings
* authentication controls
* scheduling conflict warnings

---

## Project Structure

```text
AI-Calendar-Assistant/
│
├── app/
│   ├── main.py
│   │
│   ├── ui/
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   └── calendar_service.py
│   │
│   └── validators/
│       └── event_validator.py
│
├── tests/
│
├── requirements.txt
├── README.md
├── plan.md
└── .gitignore
```

### Folder Responsibilities

#### `app/`

Contains the main application code.

#### `main.py`

Starts the desktop application and connects the major components.

#### `ui/`

Contains the PySide6 desktop interface.

This layer is responsible for what the user sees and interacts with.

#### `services/`

Contains code that communicates with external services.

Examples:

* `ai_service.py` communicates with the AI model.
* `calendar_service.py` communicates with Google Calendar.

#### `validators/`

Contains deterministic validation logic.

The validator checks AI-generated data before any calendar operation is allowed.

#### `tests/`

Contains automated tests for the application's logic.

---

## V1 Event Structure

The AI should convert natural-language input into structured event data similar to:

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

---

## Event Fields

### `action`

Defines the requested calendar operation.

For V1, the only allowed action is:

```text
create_event
```

### `title`

The name of the calendar event.

Example:

```text
Boxing
```

### `start`

The event's starting date and time.

Example:

```text
2026-09-25T19:00:00
```

### `end`

The event's ending date and time.

If the user does not provide an ending time, the application will automatically create a one-hour event.

Example:

```text
Start: 7:00 PM
End:   8:00 PM
```

### `timezone`

The event timezone using an IANA timezone identifier.

Example:

```text
America/Boise
```

### `reminder_minutes`

The number of minutes before the event that the user should receive a reminder.

Example:

```text
30
```

---

## V1 Rules

The initial version will follow these rules:

* Only `create_event` is supported.
* Every event must have a title.
* Every event must have a valid start date and time.
* If no end time is provided, the event defaults to one hour.
* Timezones must use valid timezone identifiers.
* AI-generated data must be validated locally.
* Unsupported actions must be rejected.
* The AI cannot directly modify Google Calendar.
* The user must confirm the interpreted event before it is created.
* Calendar operations are only executed after successful validation and confirmation.

---

## AI Design

The AI acts only as an interpretation layer.

It receives natural-language input such as:

```text
Add boxing Friday at 7 PM and remind me 30 minutes before.
```

and converts it into structured data.

The AI does not receive authority to directly execute calendar actions.

```text
Natural Language
      ↓
AI Interpretation
      ↓
Structured JSON
```

The structured result is then handled by the application's own validation logic.

---

## Validation Design

AI output is treated as untrusted input.

The application will validate the AI-generated structure before allowing it to continue.

Validation may include:

* checking required fields
* checking supported actions
* verifying date formats
* verifying time formats
* verifying timezone values
* checking that the end time occurs after the start time
* rejecting unexpected actions
* rejecting malformed AI output

For example, if V1 receives:

```json
{
  "action": "delete_all_events"
}
```

the validator must reject it because V1 only allows:

```text
create_event
```

The application does not rely on another AI model as its primary security validator.

Validation should use deterministic program logic wherever possible.

---

## Confirmation Design

Validation and confirmation serve different purposes.

### Validation

Answers:

> Is this data technically valid and allowed?

### User Confirmation

Answers:

> Is this actually what the user intended?

For example, the AI might return a technically valid event:

```text
Boxing
Friday
7:00 AM - 8:00 AM
```

but the user may have intended 7:00 PM.

The application therefore displays the interpreted event before creation.

```text
AI Interpretation
      ↓
Validation
      ↓
Event Preview
      ↓
User Confirms
      ↓
Google Calendar API
```

Confirmation state is controlled by the application, not by the AI.

---

## Security Principle

The most important architectural rule is:

```text
AI = Interpretation

Application = Authority

User = Final Confirmation
```

The AI proposes an action.

The Python application decides whether that action is valid.

The user decides whether the interpreted event is correct.

Only then can the Google Calendar API be called.

---

## Google Calendar Integration

The application will use Google OAuth 2.0 to request permission to access the user's Google Calendar.

After authentication, the application will use the Google Calendar API to create validated events.

For V1:

```text
User Confirms Event
        ↓
calendar_service.py
        ↓
Google Calendar API
        ↓
Event Created
```

Future versions may support:

* reading events
* updating events
* deleting events
* recurring events
* conflict detection
* automatic schedule optimization

---

## Development Roadmap

### Phase 1 — Desktop V1

Build the core working application.

Features:

* Python desktop application
* PySide6 interface
* natural-language event input
* AI event parsing
* structured event data
* local validation
* one-hour default event duration
* user confirmation
* Google OAuth authentication
* Google Calendar event creation

---

### Phase 2 — Desktop Improvements

Add additional calendar functionality.

Potential features:

* update existing events
* delete events
* read upcoming events
* recurring events
* scheduling conflict detection
* improved validation
* improved error handling
* user settings
* calendar selection

---

### Phase 3 — Voice Input

Allow users to speak scheduling instructions.

Example:

```text
"Schedule cybersecurity study tomorrow at 5 PM."
```

Possible flow:

```text
Microphone
   ↓
Speech-to-Text
   ↓
AI Event Parser
   ↓
Validation
   ↓
Confirmation
   ↓
Google Calendar
```

---

### Phase 4 — Android

Develop a mobile version for Android.

The goal will be to reuse the application's core concepts and data structures wherever practical.

---

### Phase 5 — Apple Platforms

Expand support to:

* macOS
* iPhone

The underlying AI parsing, validation rules, and calendar architecture should remain conceptually consistent across platforms even if some platform-specific code must be rewritten.

---

## Long-Term Vision

The long-term goal is to create a cross-platform AI scheduling assistant where users can naturally type or speak instructions such as:

```text
"Schedule my cybersecurity study session tomorrow at 6."

"Add boxing Friday at 7 and remind me 30 minutes before."

"Move my workout to Saturday morning."

"Find me two free hours this week to study."
```

The application should interpret the request, safely validate it, confirm the intended action, and perform the appropriate calendar operation.

The project is designed around a simple principle:

> Natural-language convenience should not remove deterministic validation or user control.
