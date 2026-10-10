"""
Name: main_window.py
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton
    
)
from datetime import datetime



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Calendar Assistant")
        self.resize(500, 350)

        layout = QVBoxLayout()

        self.title_label = QLabel("AI Calendar Assistant")


     

        self.request_input = QTextEdit() #this variable holds the string of whatever the user type within the input box
        self.request_input.setPlaceholderText(
            "Example: Add boxing Friday at 7 PM and remind me 30 minutes before."
        )

        self.parse_button = QPushButton("Parse Event") #this creates a button

        self.confirm_button = QPushButton("Confirm Event")
        self.cancel_button = QPushButton("Cancel")
        self.confirm_button.setEnabled(False)

        self.output_label = QLabel("Parsed event will appear here.") # a label on where the parsed info should be

        layout.addWidget(self.title_label)
        layout.addWidget(self.request_input)
        layout.addWidget(self.parse_button)
        layout.addWidget(self.output_label)

        layout.addWidget(self.confirm_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def get_user_request(self):
        return self.request_input.toPlainText()
    
    def format_datetime(self, iso_datetime):
        if iso_datetime is None:
            return "None chosen"

        date_time = datetime.fromisoformat(iso_datetime)

        date_part = date_time.strftime("%A, %B %d, %Y")
        time_part = date_time.strftime("%I:%M %p").lstrip("0")

        return f"{date_part} at {time_part}"

    def display_event(self, event_data):

        start_time = self.format_datetime(event_data["start"])
        end_time = self.format_datetime(event_data["end"])

        timezone = event_data["timezone"] or "None chosen"
        reminder = event_data["reminder_minutes"]

        if reminder is None:
            reminder = "None chosen"

        event_text = (
                f"Event Name: {event_data['title']}\n"
                f"Start Time: {start_time}\n"
                f"End Time: {end_time}\n"
                f"Timezone: {timezone}\n"
                f"Reminder: {reminder} minutes before"
            )
        self.output_label.setText(event_text)
        self.confirm_button.setEnabled(True)

                

        
        