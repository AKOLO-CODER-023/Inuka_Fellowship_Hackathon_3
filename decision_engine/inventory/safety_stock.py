import math


def calculate_safety_stock(
    demand_std_m3: float,
    lead_time_days: float,
    service_level_z: float = 1.645
) -> float:
    """
    Calculate safety stock based on demand variability and lead time.

    Formula:
        Safety Stock =
        Z × Demand Standard Deviation × √Lead Time
    """

    if demand_std_m3 < 0:
        raise ValueError("Demand standard deviation cannot be negative.")

    if lead_time_days < 0:
        raise ValueError("Lead time cannot be negative.")

    if service_level_z <= 0:
        raise ValueError("Service-level Z value must be positive.")

    safety_stock = (
        service_level_z
        * demand_std_m3
        * math.sqrt(lead_time_days)
    )

    return safety_stock