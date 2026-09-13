def calculate_dispatch_priority(
    risk_level: str,
    days_of_cover: float
) -> str:
    """
    Determine the urgency of a replenishment dispatch.

    Priority is based on inventory risk and days of cover.

    CRITICAL risk -> CRITICAL priority
    HIGH risk with low cover -> HIGH priority
    WARNING risk -> MEDIUM priority
    SAFE inventory -> LOW priority
    """

    valid_risk_levels = {
        "SAFE",
        "WARNING",
        "HIGH",
        "CRITICAL"
    }

    if risk_level not in valid_risk_levels:
        raise ValueError(
            f"Invalid risk level: {risk_level}"
        )

    if days_of_cover < 0:
        raise ValueError(
            "Days of cover cannot be negative."
        )

    if risk_level == "CRITICAL":
        return "CRITICAL"

    if risk_level == "HIGH":
        if days_of_cover < 2:
            return "HIGH"
        return "MEDIUM"

    if risk_level == "WARNING":
        return "MEDIUM"

    return "LOW"