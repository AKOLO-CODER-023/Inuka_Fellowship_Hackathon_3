def choose_replenishment_method(
    replenishment_volume_m3: float,
    pipeline_available: bool,
    truck_available: bool
) -> str:
    """
    Choose the preferred replenishment method.

    Priority:
        1. Pipeline batch when pipeline is available.
        2. Emergency truck when pipeline is unavailable
           but trucks are available.
        3. No action when neither option is available.
    """

    if replenishment_volume_m3 < 0:
        raise ValueError("Replenishment volume cannot be negative.")

    if replenishment_volume_m3 == 0:
        return "NO_ACTION"

    if pipeline_available:
        return "PIPELINE_BATCH"

    if truck_available:
        return "EMERGENCY_TRUCK"

    return "NO_ACTION"