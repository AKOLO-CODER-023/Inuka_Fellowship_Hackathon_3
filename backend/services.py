"""
backend/services.py

Business logic connecting the FastAPI backend
to Member 2's inventory decision engine and
the simulated autonomous control plane.
"""

from decision_engine.engine import make_inventory_decision
from decision_engine.control.control_plane import process_inventory_decision

from backend.database import save_decision


def generate_replenishment_decision(data: dict) -> dict:
    """
    Generate a replenishment recommendation.

    Flow:

        API request
            ↓
        Member 2 decision engine
            ↓
        Save decision to SQLite
            ↓
        Simulated autonomous control plane
            ↓
        Save auditable event
            ↓
        Return result to API
    """

    # ---------------------------------------------------------
    # 1. Generate the inventory decision
    # ---------------------------------------------------------

    decision = make_inventory_decision(
        depot=data["depot"],
        product=data["product"],
        current_stock_m3=data["current_stock_m3"],
        expected_receipts_m3=data["expected_receipts_m3"],
        forecast_demand_m3=data["forecast_demand_m3"],
        average_daily_demand_m3=data["average_daily_demand_m3"],
        demand_std_m3=data["demand_std_m3"],
        lead_time_days=data["lead_time_days"],
        pipeline_available=data["pipeline_available"],
        truck_available=data["truck_available"],
        tank_capacity_m3=data["tank_capacity_m3"],
        standard_batch_volume_m3=data["standard_batch_volume_m3"],
    )

    # ---------------------------------------------------------
    # 2. Make sure depot and product are present
    # ---------------------------------------------------------

    decision["depot"] = data["depot"]
    decision["product"] = data["product"]

    # ---------------------------------------------------------
    # 3. Save the decision to SQLite
    # ---------------------------------------------------------

    save_decision(decision)

    # ---------------------------------------------------------
    # 4. Send the decision through the simulated
    #    autonomous control plane
    # ---------------------------------------------------------

    control_event = process_inventory_decision(decision)

    # ---------------------------------------------------------
    # 5. Return both the decision and control event
    # ---------------------------------------------------------

    return {
        "decision": decision,
        "control_event": control_event,
    }
