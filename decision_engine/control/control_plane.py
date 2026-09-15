"""
decision_engine/control/control_plane.py

Simulated autonomous control plane.

This module receives an inventory decision,
converts it into a simulated control action,
creates an auditable event and persists it.

IMPORTANT:
No real KPC infrastructure is controlled.
"""

from decision_engine.control.control_action import create_control_action
from decision_engine.control.event_log import create_event_record
from decision_engine.control.event_store import save_event


def process_inventory_decision(decision: dict) -> dict:
    """
    Process an inventory decision through the
    simulated autonomous control plane.

    Flow:

        Inventory decision
              ↓
        Control action
              ↓
        Event record
              ↓
        Persistent event log
    """

    # ---------------------------------------------------------
    # 1. Validate the decision object
    # ---------------------------------------------------------

    if not isinstance(decision, dict):
        raise TypeError("Inventory decision must be a dictionary.")

    # ---------------------------------------------------------
    # 2. Convert the decision into a simulated action
    # ---------------------------------------------------------

    control_action = create_control_action(decision)

    # ---------------------------------------------------------
    # 3. Create an auditable event record
    # ---------------------------------------------------------

    event_record = create_event_record(control_action)

    # ---------------------------------------------------------
    # 4. Persist the event
    # ---------------------------------------------------------

    save_event(event_record)

    # ---------------------------------------------------------
    # 5. Return the event to the caller
    # ---------------------------------------------------------

    return event_record
