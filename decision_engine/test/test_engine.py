from decision_engine.engine import make_inventory_decision


def test_critical_inventory_decision():
    decision = make_inventory_decision(
        depot="Eldoret",
        product="AGO",
        current_stock_m3=8700,
        expected_receipts_m3=0,
        forecast_demand_m3=7900,
        average_daily_demand_m3=3950,
        demand_std_m3=500,
        lead_time_days=2,
        pipeline_available=True,
        truck_available=True,
        tank_capacity_m3=20000,
        standard_batch_volume_m3=10000
    )

    assert decision["depot"] == "Eldoret"
    assert decision["product"] == "AGO"
    assert decision["projected_stock_m3"] == 800
    assert decision["risk_level"] == "CRITICAL"
    assert decision["recommended_action"] == "PIPELINE_BATCH"
    assert decision["priority"] == "CRITICAL"
    assert decision["execution_status"] == "SIMULATED"
    assert "stockout_probability" in decision
    assert 0 <= decision["stockout_probability"] <= 1


def test_autonomous_decision_creates_control_event():
    from decision_engine.engine import make_autonomous_decision

    result = make_autonomous_decision(
        depot="Eldoret",
        product="AGO",
        current_stock_m3=8700,
        expected_receipts_m3=0,
        forecast_demand_m3=7900,
        average_daily_demand_m3=3950,
        demand_std_m3=500,
        lead_time_days=2,
        pipeline_available=True,
        truck_available=True,
        tank_capacity_m3=20000,
        standard_batch_volume_m3=10000
    )

    assert "decision" in result
    assert "control_event" in result

    assert result["decision"]["depot"] == "Eldoret"

    assert (
        result["control_event"]["event_type"]
        == "PIPELINE_BATCH_REQUEST"
    )

    assert (
        result["control_event"]["status"]
        == "SIMULATED"
    )