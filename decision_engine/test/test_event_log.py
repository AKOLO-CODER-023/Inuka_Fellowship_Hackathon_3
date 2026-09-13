from decision_engine.control.event_log import create_event_record


def test_event_record():
    control_action = {
        "event_id": "test-event-001",
        "event_type": "PIPELINE_BATCH_REQUEST",
        "depot": "Eldoret",
        "product": "AGO",
        "action": "PIPELINE_BATCH",
        "volume_m3": 10000,
        "priority": "CRITICAL",
        "execution_type": "SIMULATED_PIPELINE_BATCH",
        "status": "SIMULATED",
    }

    result = create_event_record(control_action)

    assert result["event_id"] == "test-event-001"
    assert result["event_type"] == "PIPELINE_BATCH_REQUEST"
    assert result["depot"] == "Eldoret"
    assert result["product"] == "AGO"
    assert result["volume_m3"] == 10000
    assert result["priority"] == "CRITICAL"
    assert result["status"] == "SIMULATED"
    assert "logged_at" in result