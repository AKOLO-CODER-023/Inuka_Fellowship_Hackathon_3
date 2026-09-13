def calculate_replenishment_volume(
    projected_stock_m3: float,
    safety_stock_m3: float,
    average_daily_demand_m3: float,
    replenishment_horizon_days: float,
    tank_capacity_m3: float
) -> float:
    """
    Calculate the recommended replenishment volume.

    Target stock is calculated as:

        Safety Stock
        + Expected Demand During Replenishment Horizon

    Recommended replenishment is then limited by the
    available storage capacity.
    """

    if projected_stock_m3 < 0:
        raise ValueError("Projected stock cannot be negative.")

    if safety_stock_m3 < 0:
        raise ValueError("Safety stock cannot be negative.")

    if average_daily_demand_m3 < 0:
        raise ValueError("Average daily demand cannot be negative.")

    if replenishment_horizon_days < 0:
        raise ValueError("Replenishment horizon cannot be negative.")

    if tank_capacity_m3 <= 0:
        raise ValueError("Tank capacity must be greater than zero.")

    if projected_stock_m3 > tank_capacity_m3:
        raise ValueError("Projected stock cannot exceed tank capacity.")

    expected_horizon_demand = (
        average_daily_demand_m3
        * replenishment_horizon_days
    )

    target_stock = (
        safety_stock_m3
        + expected_horizon_demand
    )

    required_replenishment = (
        target_stock
        - projected_stock_m3
    )

    available_capacity = (
        tank_capacity_m3
        - projected_stock_m3
    )

    recommended_volume = min(
        max(required_replenishment, 0),
        available_capacity
    )

    return recommended_volume