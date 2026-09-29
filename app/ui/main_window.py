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

        self.output_label = QLabel("Parsed event will appear here.") # a label on where the parsed info should be

        layout.addWidget(self.title_label)
        layout.addWidget(self.request_input)
        layout.addWidget(self.parse_button)
        layout.addWidget(self.output_label)

        self.setLayout(layout)


    def get_user_request(self):
        return self.request_input.toPlainText()
        