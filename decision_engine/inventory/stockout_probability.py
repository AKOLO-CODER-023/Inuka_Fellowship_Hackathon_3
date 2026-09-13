import math


def calculate_stockout_probability(
    projected_stock_m3: float,
    demand_std_m3: float
) -> float:
    """
    Estimate the probability that demand will exceed
    projected inventory.

    This is a simplified probabilistic estimate for the
    synthetic hackathon environment.

    Returns a value between 0 and 1.
    """

    if projected_stock_m3 < 0:
        raise ValueError("Projected stock cannot be negative.")

    if demand_std_m3 < 0:
        raise ValueError("Demand standard deviation cannot be negative.")

    if demand_std_m3 == 0:
        return 1.0 if projected_stock_m3 <= 0 else 0.0

    # Standard normal cumulative distribution function.
    z_score = projected_stock_m3 / demand_std_m3

    probability = 0.5 * (
        1 - math.erf(z_score / math.sqrt(2))
    )

    return max(0.0, min(1.0, probability))