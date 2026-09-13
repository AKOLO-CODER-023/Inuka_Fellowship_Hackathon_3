from decision_engine.control.control_action import create_control_action
from decision_engine.control.event_log import create_event_record
from decision_engine.control.event_store import save_event


def process_inventory_decision(decision: dict) -> dict:
    """
    Process an inventory decision through the simulated
    autonomous control plane and persist the resulting event.
    """

    control_action = create_control_action(decision)

    event_record = create_event_record(control_action)

    save_event(event_record)

    return event_record