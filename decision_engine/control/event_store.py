import json
from pathlib import Path


EVENT_LOG_FILE = Path("decision_engine/control/events.json")


def save_event(event: dict) -> None:
    """
    Save an event to the local JSON event log.
    Creates the file and parent directory if they do not exist.
    """

    EVENT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    events = []

    if EVENT_LOG_FILE.exists():
        try:
            with open(EVENT_LOG_FILE, "r", encoding="utf-8") as file:
                events = json.load(file)

            if not isinstance(events, list):
                events = []

        except (json.JSONDecodeError, OSError):
            events = []

    events.append(event)

    with open(EVENT_LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=2)


def load_events() -> list:
    """
    Load all persisted events from the local JSON event log.
    """

    if not EVENT_LOG_FILE.exists():
        return []

    try:
        with open(EVENT_LOG_FILE, "r", encoding="utf-8") as file:
            events = json.load(file)

        return events if isinstance(events, list) else []

    except (json.JSONDecodeError, OSError):
        return []