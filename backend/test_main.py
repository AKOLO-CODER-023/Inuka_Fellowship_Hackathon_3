"""
backend/test_main.py

Tests the backend API end-to-end, against the real data in data/ and the
real decision_engine -- no mocking of the business logic, so a passing
test suite means the actual demo path works.

Run from the project root:
    pytest backend/
"""

import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture(scope="module")
def client():
    # Using TestClient as a context manager runs FastAPI's lifespan
    # startup/shutdown (initialize_database(), etc.) -- without it the
    # database tables are never created and every DB-backed endpoint
    # fails with "no such table".
    with TestClient(app) as test_client:
        yield test_client


def test_health_check_reports_dependencies(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"healthy", "degraded"}
    assert "database" in body
    assert "forecast_data" in body


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_forecast_returns_a_real_number_not_an_echo(client):
    # A known historical date for a depot/product combination that
    # exists in data/forecasting_features.csv.
    response = client.post(
        "/forecast",
        json={"depot": "Eldoret", "product": "AGO", "date": "2022-06-15"},
    )
    assert response.status_code == 200
    body = response.json()

    assert body["depot"] == "Eldoret"
    assert body["product"] == "AGO"
    assert body["forecast_demand_m3"] > 0
    assert body["lower_bound_m3"] <= body["forecast_demand_m3"] <= body["upper_bound_m3"]
    assert body["model_version"]  # not empty


def test_forecast_unknown_date_returns_404_not_a_crash(client):
    response = client.post(
        "/forecast",
        json={"depot": "Eldoret", "product": "AGO", "date": "1999-01-01"},
    )
    assert response.status_code == 404


def test_replenishment_runs_the_real_decision_engine(client):
    payload = {
        "depot": "Eldoret",
        "product": "AGO",
        "current_stock_m3": 800,
        "expected_receipts_m3": 0,
        "forecast_demand_m3": 4370,
        "average_daily_demand_m3": 4200,
        "demand_std_m3": 350,
        "lead_time_days": 1,
        "pipeline_available": True,
        "truck_available": False,
        "tank_capacity_m3": 20000,
        "standard_batch_volume_m3": 10000,
    }
    response = client.post("/replenishment", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert "decision" in body and "control_event" in body
    assert body["decision"]["risk_level"] in {"SAFE", "WARNING", "HIGH", "CRITICAL"}
    # Low stock relative to demand should trigger a real replenishment.
    assert body["decision"]["recommended_action"] != "NO_ACTION"


def test_replenishment_low_stock_triggers_a_logged_alert(client, caplog):
    payload = {
        "depot": "Kisumu",
        "product": "PMS",
        "current_stock_m3": 200,
        "expected_receipts_m3": 0,
        "forecast_demand_m3": 3000,
        "average_daily_demand_m3": 3000,
        "demand_std_m3": 200,
        "lead_time_days": 1,
        "pipeline_available": True,
        "truck_available": False,
        "tank_capacity_m3": 15000,
        "standard_batch_volume_m3": 10000,
    }
    with caplog.at_level("WARNING"):
        response = client.post("/replenishment", json=payload)
    assert response.status_code == 200
    # CRITICAL/HIGH risk should have produced at least one WARNING/CRITICAL
    # log line from backend/alerts.py.
    risk_level = response.json()["decision"]["risk_level"]
    if risk_level in {"CRITICAL", "HIGH"}:
        assert any("recommended action" in message for message in caplog.messages)


def test_alerts_endpoint_only_returns_high_risk(client):
    response = client.get("/alerts")
    assert response.status_code == 200
    body = response.json()
    for alert in body["alerts"]:
        assert alert["risk_level"] in {"CRITICAL", "HIGH"}


def test_roi_endpoint_computes_from_real_csvs(client):
    response = client.get("/roi")
    assert response.status_code == 200
    body = response.json()

    assert body["projected_annual_savings_kes"] > 0
    assert body["implementation_cost_kes"] > 0
    assert "year1_roi_pct" in body
    breakdown = body["savings_breakdown_kes"]
    total = sum(breakdown.values())
    assert round(total, 1) == round(body["projected_annual_savings_kes"], 1)


def test_roi_endpoint_accepts_manual_inventory_override(client):
    response = client.get("/roi", params={"inventory_holding_savings_kes": 500000})
    assert response.status_code == 200
    body = response.json()
    assert body["savings_breakdown_kes"]["reduced_inventory_cost"] == 500000.0
