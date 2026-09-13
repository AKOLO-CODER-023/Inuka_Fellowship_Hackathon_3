from decision_engine.rules.risk_rules import classify_inventory_risk


def test_critical_risk():
    result = classify_inventory_risk(1.2)
    assert result == "CRITICAL"


def test_high_risk():
    result = classify_inventory_risk(2.0)
    assert result == "HIGH"


def test_warning_risk():
    result = classify_inventory_risk(4.0)
    assert result == "WARNING"


def test_safe_risk():
    result = classify_inventory_risk(7.0)
    assert result == "SAFE"


def test_negative_days_of_cover():
    try:
        classify_inventory_risk(-1)
        assert False
    except ValueError:
        assert True