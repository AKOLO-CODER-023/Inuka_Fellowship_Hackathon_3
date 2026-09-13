from decision_engine.optimisation.replenishment import (
    calculate_replenishment_volume
)


def test_replenishment_needed():
    result = calculate_replenishment_volume(
        projected_stock_m3=800,
        safety_stock_m3=4500,
        average_daily_demand_m3=3950,
        replenishment_horizon_days=1,
        tank_capacity_m3=20000
    )

    assert result == 7650


def test_no_replenishment_when_stock_is_healthy():
    result = calculate_replenishment_volume(
        projected_stock_m3=10000,
        safety_stock_m3=4500,
        average_daily_demand_m3=3950,
        replenishment_horizon_days=1,
        tank_capacity_m3=20000
    )

    assert result == 0


def test_replenishment_cannot_exceed_capacity():
    result = calculate_replenishment_volume(
        projected_stock_m3=15000,
        safety_stock_m3=10000,
        average_daily_demand_m3=5000,
        replenishment_horizon_days=2,
        tank_capacity_m3=18000
    )

    assert result == 3000