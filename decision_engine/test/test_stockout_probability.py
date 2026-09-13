from decision_engine.inventory.stockout_probability import (
    calculate_stockout_probability
)


def test_stockout_probability_is_between_zero_and_one():
    result = calculate_stockout_probability(
        projected_stock_m3=800,
        demand_std_m3=500
    )

    assert 0 <= result <= 1


def test_zero_projected_stock():
    result = calculate_stockout_probability(
        projected_stock_m3=0,
        demand_std_m3=500
    )

    assert result == 0.5


def test_zero_demand_variability_with_stock():
    result = calculate_stockout_probability(
        projected_stock_m3=800,
        demand_std_m3=0
    )

    assert result == 0.0


def test_negative_projected_stock():
    try:
        calculate_stockout_probability(
            projected_stock_m3=-100,
            demand_std_m3=500
        )
        assert False
    except ValueError:
        assert True