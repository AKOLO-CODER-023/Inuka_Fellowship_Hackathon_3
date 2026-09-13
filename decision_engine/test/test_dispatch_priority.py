from decision_engine.optimisation.dispatch_priority import (
    calculate_dispatch_priority
)


def test_critical_priority():
    result = calculate_dispatch_priority(
        risk_level="CRITICAL",
        days_of_cover=0.9
    )

    assert result == "CRITICAL"


def test_high_priority():
    result = calculate_dispatch_priority(
        risk_level="HIGH",
        days_of_cover=1.8
    )

    assert result == "HIGH"


def test_medium_priority_for_warning():
    result = calculate_dispatch_priority(
        risk_level="WARNING",
        days_of_cover=4
    )

    assert result == "MEDIUM"


def test_low_priority_for_safe_inventory():
    result = calculate_dispatch_priority(
        risk_level="SAFE",
        days_of_cover=7
    )

    assert result == "LOW"


def test_invalid_risk_level():
    try:
        calculate_dispatch_priority(
            risk_level="UNKNOWN",
            days_of_cover=2
        )
        assert False
    except ValueError:
        assert True