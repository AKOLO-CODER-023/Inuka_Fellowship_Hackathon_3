from decision_engine.inventory.days_of_cover import calculate_days_of_cover


def test_days_of_cover():
    result = calculate_days_of_cover(
        current_stock_m3=8700,
        expected_daily_demand_m3=3950
    )

    assert round(result, 2) == 2.20


def test_zero_demand():
    result = calculate_days_of_cover(
        current_stock_m3=8700,
        expected_daily_demand_m3=0
    )

    assert result == float("inf")