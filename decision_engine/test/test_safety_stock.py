from decision_engine.inventory.safety_stock import calculate_safety_stock


def test_safety_stock():
    result = calculate_safety_stock(
        demand_std_m3=500,
        lead_time_days=2,
        service_level_z=1.645
    )

    assert round(result, 2) == 1163.19


def test_zero_variability():
    result = calculate_safety_stock(
        demand_std_m3=0,
        lead_time_days=2
    )

    assert result == 0


def test_negative_demand_std():
    try:
        calculate_safety_stock(
            demand_std_m3=-500,
            lead_time_days=2
        )
        assert False
    except ValueError:
        assert True