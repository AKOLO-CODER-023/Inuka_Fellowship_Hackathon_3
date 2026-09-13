from decision_engine.control.control_plane import (
    process_inventory_decision
)


def test_control_plane_pipeline():
    decision = {
        "depot": "Eldoret",
        "product": "AGO",
        "recommended_action": "PIPELINE_BATCH",
        "recommended_volume_m3": 10000,
        "priority": "CRITICAL",
    }

    result = process_inventory_decision(decision)

    assert result["event_type"] == "PIPELINE_BATCH_REQUEST"
    assert result["depot"] == "Eldoret"
    assert result["product"] == "AGO"
    assert result["action"] == "PIPELINE_BATCH"
    assert result["volume_m3"] == 10000
    assert result["priority"] == "CRITICAL"
    assert result["execution_type"] == "SIMULATED_PIPELINE_BATCH"
    assert result["status"] == "SIMULATED"
    assert "event_id" in result
    assert "logged_at" in result