"""
decision_engine/control/event_store.py

Persistent local JSON event store.

The event store provides a lightweight audit trail
for the simulated autonomous control plane.
"""

import json
from pathlib import Path


# ---------------------------------------------------------
# EVENT LOG LOCATION
# ---------------------------------------------------------

# Resolve the project root from this file instead of relying
# on the current terminal working directory.

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EVENT_LOG_FILE = (
    PROJECT_ROOT
    / "decision_engine"
    / "control"
    / "events.json"
)

# Backup file used if the main event log becomes corrupted.
EVENT_BACKUP_FILE = (
    PROJECT_ROOT
    / "decision_engine"
    / "control"
    / "events_backup.json"
)


# ---------------------------------------------------------
# LOAD EVENTS
# ---------------------------------------------------------

def load_events() -> list:
    """
    Load all persisted events from the local JSON event log.

    If the main event file is corrupted, the function attempts
    to recover events from the backup file.

    If neither file can be read, an empty list is returned.
    """

    # -----------------------------------------------------
    # Try the main event log first
    # -----------------------------------------------------

    if EVENT_LOG_FILE.exists():

        try:
            with open(
                EVENT_LOG_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                events = json.load(file)

            if isinstance(events, list):
                return events

        except (json.JSONDecodeError, OSError):
            pass

    # -----------------------------------------------------
    # Try the backup event log
    # -----------------------------------------------------

    if EVENT_BACKUP_FILE.exists():

        try:
            with open(
                EVENT_BACKUP_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                events = json.load(file)

            if isinstance(events, list):
                return events

        except (json.JSONDecodeError, OSError):
            pass

    # -----------------------------------------------------
    # No usable event history found
    # -----------------------------------------------------

    return []


# ---------------------------------------------------------
# SAVE EVENT
# ---------------------------------------------------------

def save_event(event: dict) -> None:
    """
    Save one event to the local JSON event log.

    The function:

    1. Validates the event.
    2. Creates the directory if necessary.
    3. Loads existing events.
    4. Creates a backup of the existing log.
    5. Appends the new event.
    6. Writes the updated event list.

    This is still a simulated local event store.
    It does not communicate with real infrastructure.
    """

    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    if not isinstance(event, dict):
        raise TypeError("Event must be a dictionary.")

    # -----------------------------------------------------
    # Ensure the directory exists
    # -----------------------------------------------------

    EVENT_LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # Load existing events
    # -----------------------------------------------------

    events = load_events()

    # -----------------------------------------------------
    # Create a backup before modifying the main file
    # -----------------------------------------------------

    if EVENT_LOG_FILE.exists():

        try:
            EVENT_BACKUP_FILE.write_text(
                EVENT_LOG_FILE.read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8"
            )

        except OSError:
            # Backup failure should not prevent the system
            # from attempting to save the new event.
            pass

    # -----------------------------------------------------
    # Add the new event
    # -----------------------------------------------------

    events.append(event)

    # -----------------------------------------------------
    # Write the updated event log
    # -----------------------------------------------------

    temporary_file = EVENT_LOG_FILE.with_suffix(".tmp")

    try:

        with open(
            temporary_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                events,
                file,
                indent=2
            )

        # Replace the old event log only after the new file
        # has been successfully written.
        temporary_file.replace(EVENT_LOG_FILE)

    except OSError:

        # Clean up the temporary file if writing failed.
        if temporary_file.exists():
            try:
                temporary_file.unlink()
            except OSError:
                pass

        raise
