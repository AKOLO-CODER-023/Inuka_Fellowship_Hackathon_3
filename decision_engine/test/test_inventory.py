from decision_engine.inventory.projection import calculate_projected_stock


def test_projected_stock():
    result = calculate_projected_stock(
        current_stock_m3=8700,
        expected_receipts_m3=0,
        forecast_demand_m3=7900
    )

    assert result == 800