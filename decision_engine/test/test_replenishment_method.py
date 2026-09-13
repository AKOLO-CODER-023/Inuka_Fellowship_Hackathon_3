from decision_engine.optimisation.replenishment_method import (
    choose_replenishment_method
)


def test_pipeline_preferred():
    result = choose_replenishment_method(
        replenishment_volume_m3=10000,
        pipeline_available=True,
        truck_available=True
    )

    assert result == "PIPELINE_BATCH"


def test_truck_used_when_pipeline_unavailable():
    result = choose_replenishment_method(
        replenishment_volume_m3=10000,
        pipeline_available=False,
        truck_available=True
    )

    assert result == "EMERGENCY_TRUCK"


def test_no_action_when_no_replenishment_needed():
    result = choose_replenishment_method(
        replenishment_volume_m3=0,
        pipeline_available=True,
        truck_available=True
    )

    assert result == "NO_ACTION"


def test_no_action_when_no_supply_method_available():
    result = choose_replenishment_method(
        replenishment_volume_m3=10000,
        pipeline_available=False,
        truck_available=False
    )

    assert result == "NO_ACTION"


def test_negative_volume():
    try:
        choose_replenishment_method(
            replenishment_volume_m3=-100,
            pipeline_available=True,
            truck_available=True
        )
        assert False
    except ValueError:
        assert True