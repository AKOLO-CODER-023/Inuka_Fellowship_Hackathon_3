from decision_engine.optimisation.batch_sizing import calculate_batch_size


def test_standard_batch_covers_requirement():
    result = calculate_batch_size(
        required_replenishment_m3=7650,
        standard_batch_volume_m3=10000,
        projected_stock_m3=800,
        tank_capacity_m3=20000
    )

    assert result == 10000


def test_batch_cannot_exceed_available_capacity():
    result = calculate_batch_size(
        required_replenishment_m3=9000,
        standard_batch_volume_m3=10000,
        projected_stock_m3=15000,
        tank_capacity_m3=20000
    )

    assert result == 5000


def test_no_batch_when_no_replenishment_needed():
    result = calculate_batch_size(
        required_replenishment_m3=0,
        standard_batch_volume_m3=10000,
        projected_stock_m3=8000,
        tank_capacity_m3=20000
    )

    assert result == 0