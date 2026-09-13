def calculate_batch_size(
    required_replenishment_m3: float,
    standard_batch_volume_m3: float,
    projected_stock_m3: float,
    tank_capacity_m3: float
) -> float:
    """
    Determine an operationally feasible replenishment batch size.

    The batch should:
    - cover the required replenishment volume
    - use the standard pipeline batch size when possible
    - never exceed available tank capacity
    """

    if required_replenishment_m3 < 0:
        raise ValueError("Required replenishment cannot be negative.")

    if standard_batch_volume_m3 <= 0:
        raise ValueError("Standard batch volume must be greater than zero.")

    if projected_stock_m3 < 0:
        raise ValueError("Projected stock cannot be negative.")

    if tank_capacity_m3 <= 0:
        raise ValueError("Tank capacity must be greater than zero.")

    if projected_stock_m3 > tank_capacity_m3:
        raise ValueError("Projected stock cannot exceed tank capacity.")

    if required_replenishment_m3 == 0:
        return 0

    available_capacity = tank_capacity_m3 - projected_stock_m3

    if available_capacity <= 0:
        return 0

    # Use the standard batch if it can fit in the available capacity.
    if standard_batch_volume_m3 >= required_replenishment_m3:
        if standard_batch_volume_m3 <= available_capacity:
            return standard_batch_volume_m3

    # If the standard batch cannot fit, use the largest feasible volume.
    return min(required_replenishment_m3, available_capacity)