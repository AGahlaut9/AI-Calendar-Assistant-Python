"""
Name: calendar_service.py

Responsibility:
- Authenticate the user with Google Calendar
- Create confirmed calendar events
"""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Permission our app requests from Google.
# This allows creating/editing calendar events,
# without giving the app broader Google account access.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


# Find the root project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


def authenticate_google():
    credentials = None

    # If the user has already logged in before,
    # try using the saved token.
    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # If there are no valid credentials, authenticate again.
    if not credentials or not credentials.valid:

        # Refresh an expired access token when possible.
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # Otherwise open Google's login/permission page.
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            credentials = flow.run_local_server(port=0)

        # Save the authorization for future runs.
        TOKEN_FILE.write_text(credentials.to_json())

    return build(
        "calendar",
        "v3",
        credentials=credentials
    )


def format_google_datetime(iso_datetime, timezone_name=None):
    date_time = datetime.fromisoformat(iso_datetime)

    # Your AI currently returns times such as:
    # 2026-10-11T19:00:00
    #
    # Google needs timezone-aware RFC3339 timestamps.
    if date_time.tzinfo is None:

        if timezone_name:
            date_time = date_time.replace(
                tzinfo=ZoneInfo(timezone_name)
            )
        else:
            # Use the computer's local timezone.
            date_time = date_time.astimezone()

    return date_time.isoformat()


def create_event(event_data):
    service = authenticate_google()

    timezone = event_data["timezone"]

    event = {
        "summary": event_data["title"],

        "start": {
            "dateTime": format_google_datetime(
                event_data["start"],
                timezone
            )
        },

        "end": {
            "dateTime": format_google_datetime(
                event_data["end"],
                timezone
            )
        }
    }

    # Add explicit timezone if the user provided one.
    if timezone:
        event["start"]["timeZone"] = timezone
        event["end"]["timeZone"] = timezone

    reminder_minutes = event_data["reminder_minutes"]

    if reminder_minutes is None:
        event["reminders"] = {
            "useDefault": True
        }
    else:
        event["reminders"] = {
            "useDefault": False,
            "overrides": [
                {
                    "method": "popup",
                    "minutes": reminder_minutes
                }
            ]
        }

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event
        )
        .execute()
    )

    return created_event