from decision_engine.control.control_action import create_control_action


def test_pipeline_control_action():
    decision = {
        "depot": "Eldoret",
        "product": "AGO",
        "recommended_action": "PIPELINE_BATCH",
        "recommended_volume_m3": 10000,
        "priority": "CRITICAL",
    }

    result = create_control_action(decision)

    assert result["event_type"] == "PIPELINE_BATCH_REQUEST"
    assert result["depot"] == "Eldoret"
    assert result["product"] == "AGO"
    assert result["volume_m3"] == 10000
    assert result["status"] == "SIMULATED"
    assert result["execution_type"] == "SIMULATED_PIPELINE_BATCH"


def test_truck_control_action():
    decision = {
        "depot": "Nakuru",
        "product": "PMS",
        "recommended_action": "EMERGENCY_TRUCK",
        "recommended_volume_m3": 5000,
        "priority": "HIGH",
    }

    result = create_control_action(decision)

    assert result["event_type"] == "TRUCK_DISPATCH_REQUEST"
    assert result["execution_type"] == "SIMULATED_TRUCK_DISPATCH"
    assert result["status"] == "SIMULATED"


def test_no_action():
    decision = {
        "depot": "Nairobi",
        "product": "AGO",
        "recommended_action": "NO_ACTION",
        "recommended_volume_m3": 0,
        "priority": "LOW",
    }

    result = create_control_action(decision)

    assert result["event_type"] == "NO_ACTION"
    assert result["execution_type"] == "NO_EXECUTION"
    assert result["status"] == "SIMULATED"