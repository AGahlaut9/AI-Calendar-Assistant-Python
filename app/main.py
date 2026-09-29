"""
This is the controller file
Name: Main.py
Description:
"""
import sys
from validators.event_validator import apply_default_end_time
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from services.ai_service import parse_requested_info


app = QApplication(sys.argv)

window = MainWindow()



window.show()

def handle_user_request():
    print("1. Parse button clicked")

    user_request = window.get_user_request()
    print("2. User typed:", user_request)

    event_data = parse_requested_info(user_request)

    print("3. AI returned:", event_data)

    event_data = apply_default_end_time(event_data)

    print("4. Backend processed:", event_data)

    window.parse_button.clicked.connect(handle_user_request)


sys.exit(app.exec())