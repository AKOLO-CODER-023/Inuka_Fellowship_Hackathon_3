from decision_engine.inventory.reorder_point import calculate_reorder_point


def test_reorder_point():
    result = calculate_reorder_point(
        average_daily_demand_m3=3950,
        lead_time_days=2,
        safety_stock_m3=1160.66
    )

    assert round(result, 2) == 9060.66


def test_zero_safety_stock():
    result = calculate_reorder_point(
        average_daily_demand_m3=3950,
        lead_time_days=2,
        safety_stock_m3=0
    )

    assert result == 7900


def test_negative_demand():
    try:
        calculate_reorder_point(
            average_daily_demand_m3=-100,
            lead_time_days=2,
            safety_stock_m3=500
        )
        assert False
    except ValueError:
        assert True