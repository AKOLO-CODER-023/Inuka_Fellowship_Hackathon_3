from datetime import datetime, timezone


def create_event_record(control_action: dict) -> dict:
    """
    Create an auditable control-plane event record.

    This function records a simulated autonomous action.
    It does not execute any real operational action.
    """

    if not isinstance(control_action, dict):
        raise TypeError("Control action must be a dictionary.")

    required_fields = {
        "event_id",
        "event_type",
        "depot",
        "product",
        "action",
        "volume_m3",
        "priority",
        "execution_type",
        "status",
    }

    missing_fields = required_fields - control_action.keys()

    if missing_fields:
        raise ValueError(
            f"Control action is missing required fields: {missing_fields}"
        )

    return {
        "event_id": control_action["event_id"],
        "event_type": control_action["event_type"],
        "depot": control_action["depot"],
        "product": control_action["product"],
        "action": control_action["action"],
        "volume_m3": control_action["volume_m3"],
        "priority": control_action["priority"],
        "execution_type": control_action["execution_type"],
        "status": control_action["status"],
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }