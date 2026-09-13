def calculate_days_of_cover(
    current_stock_m3: float,
    expected_daily_demand_m3: float
) -> float:
    """
    Calculate how many days the current inventory can cover.

    Formula:
        Days of Cover = Current Stock / Expected Daily Demand
    """

    if current_stock_m3 < 0:
        raise ValueError("Current stock cannot be negative.")

    if expected_daily_demand_m3 < 0:
        raise ValueError("Expected daily demand cannot be negative.")

    if expected_daily_demand_m3 == 0:
        return float("inf")

    return current_stock_m3 / expected_daily_demand_m3