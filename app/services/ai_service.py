"""
Name: ai_service.py

Current responsibility:
- Receive the user's raw natural-language request
- Send that request and our required schema to the AI model
- Receive structured event data
- Convert the AI response into a Python dictionary
- Return that dictionary to main.py
"""

# TODO: Add AI integration later.import json

import json
from ollama import chat

from Model.event_schema import InputSchema, INPUT_SCHEMA_FORMAT
from services.command_layer import CALENDAR_PARSER_COMMAND

"""
This methods takes in the entier user query as a string, and then send the command and user request together to the chatbot. Then the output of the chatbot is turned into
a json file which will be used later to figure out individual components and parse categories for event validation
"""
from datetime import datetime

def parse_requested_info(user_text: str) -> InputSchema:

    current_date = datetime.now().strftime("%Y-%m-%d")

    response = chat(
        model="qwen3.5:2b",
        messages=[
            {
                "role": "system",
                "content": (
                    CALENDAR_PARSER_COMMAND
                    + f"\nCurrent date: {current_date}"
                    + "\nReturn start and end as ISO 8601 datetime strings."
                    + "\nExample: 2026-10-05T19:00:00"
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        format=INPUT_SCHEMA_FORMAT,
        think=False,
        options={
            "temperature": 0
        }
    )

    raw_content = response.message.content

    print("RAW OLLAMA RESPONSE:", repr(raw_content))

    if not raw_content:
        raise ValueError("Ollama returned an empty response.")

    parsed_data = json.loads(raw_content)

    raw_content = response.message.content
    raw_thinking = response.message.thinking

    print("RAW OLLAMA CONTENT:", repr(raw_content))
    print("RAW OLLAMA THINKING:", repr(raw_thinking))

    return parsed_data

   