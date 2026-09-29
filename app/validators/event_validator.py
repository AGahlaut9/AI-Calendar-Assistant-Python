"""
Name: event_validator.py

Responsibility:
- Apply deterministic rules to AI-generated event data
- Validate event information before it reaches the frontend/calendar
"""

from datetime import datetime, timedelta

from Model.event_schema import InputSchema

"""
This function is what needs to be applied to the data tht comes back from the AI model, and is verified with the defualt end time
"""
def apply_default_end_time(event_data: InputSchema) -> InputSchema:

    # Only apply the default if the request does not need clarification
    if event_data["needs_clarification" == True]:
        return event_data

    # If the user already supplied an end time, do not change it
    if event_data["end"] is not None:
        return event_data

    # We cannot calculate an end time without a start time
    if event_data["start"] is None:
        return event_data

    start_time = datetime.fromisoformat(event_data["start"])

    end_time = start_time + timedelta(hours=1)

    event_data["end"] = end_time.isoformat()

    return event_data