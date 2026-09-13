from decision_engine.control.control_plane import process_inventory_decision
from decision_engine.inventory.projection import calculate_projected_stock
from decision_engine.inventory.days_of_cover import calculate_days_of_cover
from decision_engine.inventory.safety_stock import calculate_safety_stock
from decision_engine.inventory.reorder_point import calculate_reorder_point
from decision_engine.inventory.stockout_probability import (
    calculate_stockout_probability
)
from decision_engine.rules.risk_rules import classify_inventory_risk

from decision_engine.optimisation.replenishment import (
    calculate_replenishment_volume
)

from decision_engine.optimisation.replenishment_method import (
    choose_replenishment_method
)

from decision_engine.optimisation.batch_sizing import (
    calculate_batch_size
)

from decision_engine.optimisation.dispatch_priority import (
    calculate_dispatch_priority
)


def make_inventory_decision(
    depot: str,
    product: str,
    current_stock_m3: float,
    expected_receipts_m3: float,
    forecast_demand_m3: float,
    average_daily_demand_m3: float,
    demand_std_m3: float,
    lead_time_days: float,
    pipeline_available: bool,
    truck_available: bool,
    tank_capacity_m3: float,
    standard_batch_volume_m3: float = 10000
) -> dict:
    """
    Combine inventory calculations and optimisation rules
    into one integration-ready inventory decision.

    This function does not execute a real operational action.
    It only generates a simulated recommendation.
    """

    # ---------------------------------------------------------
    # 1. Project future inventory
    # ---------------------------------------------------------
    projected_stock_m3 = calculate_projected_stock(
        current_stock_m3=current_stock_m3,
        expected_receipts_m3=expected_receipts_m3,
        forecast_demand_m3=forecast_demand_m3
    )

    stockout_probability = calculate_stockout_probability(
    projected_stock_m3=projected_stock_m3,
    demand_std_m3=demand_std_m3
    )
    # ---------------------------------------------------------
    # 2. Calculate days of inventory coverage
    # ---------------------------------------------------------
    days_of_cover = calculate_days_of_cover(
        current_stock_m3=current_stock_m3,
        expected_daily_demand_m3=average_daily_demand_m3
    )

    # ---------------------------------------------------------
    # 3. Calculate safety stock
    # ---------------------------------------------------------
    safety_stock_m3 = calculate_safety_stock(
        demand_std_m3=demand_std_m3,
        lead_time_days=lead_time_days
    )

    # ---------------------------------------------------------
    # 4. Calculate reorder point
    # ---------------------------------------------------------
    reorder_point_m3 = calculate_reorder_point(
        average_daily_demand_m3=average_daily_demand_m3,
        lead_time_days=lead_time_days,
        safety_stock_m3=safety_stock_m3
    )

    # ---------------------------------------------------------
# 5. Classify inventory risk
# ---------------------------------------------------------
    projected_days_of_cover = calculate_days_of_cover(
    current_stock_m3=projected_stock_m3,
    expected_daily_demand_m3=average_daily_demand_m3
)

    risk_level = classify_inventory_risk(
    days_of_cover=projected_days_of_cover
    )

    # ---------------------------------------------------------
    # 6. Calculate replenishment requirement
    # ---------------------------------------------------------
    replenishment_volume_m3 = calculate_replenishment_volume(
        projected_stock_m3=projected_stock_m3,
        safety_stock_m3=safety_stock_m3,
        average_daily_demand_m3=average_daily_demand_m3,
        replenishment_horizon_days=1,
        tank_capacity_m3=tank_capacity_m3
    )

    # ---------------------------------------------------------
    # 7. Select replenishment method
    # ---------------------------------------------------------
    replenishment_method = choose_replenishment_method(
        replenishment_volume_m3=replenishment_volume_m3,
        pipeline_available=pipeline_available,
        truck_available=truck_available
    )

    # ---------------------------------------------------------
    # 8. Determine operational batch size
    # ---------------------------------------------------------
    batch_size_m3 = calculate_batch_size(
        required_replenishment_m3=replenishment_volume_m3,
        standard_batch_volume_m3=standard_batch_volume_m3,
        projected_stock_m3=projected_stock_m3,
        tank_capacity_m3=tank_capacity_m3
    )

    # ---------------------------------------------------------
    # 9. Determine dispatch priority
    # ---------------------------------------------------------
    priority = calculate_dispatch_priority(
        risk_level=risk_level,
        days_of_cover=days_of_cover
    )

    # ---------------------------------------------------------
    # 10. Determine recommended action
    # ---------------------------------------------------------
    if replenishment_method == "NO_ACTION":
        recommended_action = "NO_ACTION"
    else:
        recommended_action = replenishment_method

    # ---------------------------------------------------------
    # 11. Generate human-readable reason
    # ---------------------------------------------------------
    if recommended_action == "NO_ACTION":
        decision_reason = (
            "Inventory is currently sufficient and no replenishment "
            "action is required."
        )
    else:
        decision_reason = (
            f"Inventory risk is {risk_level} with "
            f"{days_of_cover:.2f} days of cover. "
            f"Replenishment of approximately "
            f"{batch_size_m3:.0f} m3 is recommended."
        )

    # ---------------------------------------------------------
    # 12. Return integration-ready decision
    # ---------------------------------------------------------
    return {
        "depot": depot,
        "product": product,
        "risk_level": risk_level,
        "stockout_probability": round(stockout_probability, 4),
        "current_stock_m3": current_stock_m3,
        "projected_stock_m3": round(projected_stock_m3, 2),
        "days_of_cover": round(days_of_cover, 2),
        "safety_stock_m3": round(safety_stock_m3, 2),
        "reorder_point_m3": round(reorder_point_m3, 2),
        "required_replenishment_m3": round(
            replenishment_volume_m3, 2
        ),
        "recommended_action": recommended_action,
        "preferred_mode": replenishment_method,
        "recommended_volume_m3": round(batch_size_m3, 2),
        "priority": priority,
        "decision_reason": decision_reason,
        "execution_status": "SIMULATED"
    }
def make_autonomous_decision(**kwargs) -> dict:
    """
    Generate an inventory decision and pass it through
    the simulated autonomous control plane.
    """

    decision = make_inventory_decision(**kwargs)

    control_event = process_inventory_decision(decision)

    return {
        "decision": decision,
        "control_event": control_event,
    }