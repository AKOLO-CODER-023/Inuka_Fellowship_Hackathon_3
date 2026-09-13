def classify_inventory_risk(days_of_cover: float) -> str:
    """
    Classify inventory risk based on days of cover.

    Risk levels:
        SAFE:      5 or more days
        WARNING:   3 to less than 5 days
        HIGH:      1.5 to less than 3 days
        CRITICAL:  less than 1.5 days
    """

    if days_of_cover < 0:
        raise ValueError("Days of cover cannot be negative.")

    if days_of_cover < 1.5:
        return "CRITICAL"

    if days_of_cover < 3:
        return "HIGH"

    if days_of_cover < 5:
        return "WARNING"

    return "SAFE"