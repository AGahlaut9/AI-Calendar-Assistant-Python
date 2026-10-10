"""
This is the controller file
Name: Main.py
Description:
"""

import sys

from PySide6.QtWidgets import QApplication

from validators.event_validator import apply_default_end_time
from ui.main_window import MainWindow
from services.ai_service import parse_requested_info
from services.calendar_service import create_event


app = QApplication(sys.argv)
window = MainWindow()

# Stores the event while we wait for the user to confirm it.
pending_event = None


def handle_user_request():
    global pending_event

    print("1. Parse button clicked")

    user_request = window.get_user_request()
    print("2. User typed:", user_request)

    event_data = parse_requested_info(user_request)
    print("3. AI returned:", event_data)

    event_data = apply_default_end_time(event_data)
    print("4. Backend processed:", event_data)

    pending_event = event_data

    window.display_event(event_data)


def handle_confirm_event():
    global pending_event

    if pending_event is None:
        print("No event available to confirm.")
        return

    print("5. Confirm button clicked")

    created_event = create_event(pending_event)

    print("6. Google Calendar event created:")
    print(created_event)


window.parse_button.clicked.connect(handle_user_request)
window.confirm_button.clicked.connect(handle_confirm_event)

window.show()

sys.exit(app.exec())