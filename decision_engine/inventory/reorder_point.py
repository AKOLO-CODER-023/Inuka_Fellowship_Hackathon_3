def calculate_reorder_point(
    average_daily_demand_m3: float,
    lead_time_days: float,
    safety_stock_m3: float
) -> float:
    """
    Calculate the inventory reorder point.

    Formula:
        Reorder Point =
        (Average Daily Demand × Lead Time) + Safety Stock
    """

    if average_daily_demand_m3 < 0:
        raise ValueError("Average daily demand cannot be negative.")

    if lead_time_days < 0:
        raise ValueError("Lead time cannot be negative.")

    if safety_stock_m3 < 0:
        raise ValueError("Safety stock cannot be negative.")

    reorder_point = (
        average_daily_demand_m3 * lead_time_days
        + safety_stock_m3
    )

    return reorder_point