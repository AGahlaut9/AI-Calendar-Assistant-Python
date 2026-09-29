"""
Name: event_schema.py
@Author: AGahlaut9
Description: This does 2 things, tells the event validator file what data format (JSON) in a dictionary we want
and it tells us what format the AI Model must parse data in
"""

from typing import Optional, TypedDict # this means from the "Typing" modules call the "TypedDict" and "Optional" tools

class InputSchema(TypedDict):
    action: str
    title: Optional[str]
    start: Optional[str]
    end: Optional[str]
    timezone: Optional[str]
    reminder_minutes: Optional[int]
    needs_clarification: bool
    clarification_questions: list[str]
    
INPUT_SCHEMA_FORMAT = {
    "type": "object",
    "properties": {
        "action": {
        "type": "string",
        "enum": ["create_event"]
        },
        "title": {
            "type": ["string", "null"]
        },
        "start": {
            "type": ["string", "null"]
        },
        "end": {
            "type": ["string", "null"]
        },
        "timezone": {
            "type": ["string", "null"]
        },
        "reminder_minutes": {
            "type": ["integer", "null"]
        },
        "needs_clarification": {
            "type": "boolean"
        },
        "clarification_questions": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [
        "action",
        "title",
        "start",
        "end",
        "timezone",
        "reminder_minutes",
        "needs_clarification",
        "clarification_questions"
    ]
}