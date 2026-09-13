from datetime import datetime, timezone
from uuid import uuid4


def create_control_action(decision: dict) -> dict:
    """
    Convert an inventory decision into a simulated
    autonomous control-plane action.

    This function does NOT communicate with real KPC
    infrastructure. It only creates a simulated event.
    """

    if not isinstance(decision, dict):
        raise TypeError("Decision must be a dictionary.")

    required_fields = {
        "depot",
        "product",
        "recommended_action",
        "recommended_volume_m3",
        "priority",
    }

    missing_fields = required_fields - decision.keys()

    if missing_fields:
        raise ValueError(
            f"Decision is missing required fields: {missing_fields}"
        )

    action = decision["recommended_action"]

    if action == "PIPELINE_BATCH":
        execution_type = "SIMULATED_PIPELINE_BATCH"
        event_type = "PIPELINE_BATCH_REQUEST"

    elif action == "EMERGENCY_TRUCK":
        execution_type = "SIMULATED_TRUCK_DISPATCH"
        event_type = "TRUCK_DISPATCH_REQUEST"

    else:
        execution_type = "NO_EXECUTION"
        event_type = "NO_ACTION"

    return {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "depot": decision["depot"],
        "product": decision["product"],
        "action": action,
        "volume_m3": decision["recommended_volume_m3"],
        "priority": decision["priority"],
        "execution_type": execution_type,
        "status": "SIMULATED",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }