def calculate_projected_stock(
    current_stock_m3: float,
    expected_receipts_m3: float,
    forecast_demand_m3: float
) -> float:
    """
    Calculate projected inventory after expected demand and receipts.

    Formula:
        Projected Stock =
        Current Stock + Expected Receipts - Forecast Demand
    """

    if current_stock_m3 < 0:
        raise ValueError("Current stock cannot be negative.")

    if expected_receipts_m3 < 0:
        raise ValueError("Expected receipts cannot be negative.")

    if forecast_demand_m3 < 0:
        raise ValueError("Forecast demand cannot be negative.")

    projected_stock = (
        current_stock_m3
        + expected_receipts_m3
        - forecast_demand_m3
    )

    return projected_stock