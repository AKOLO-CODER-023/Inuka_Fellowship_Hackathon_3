"""
decision_engine/schemas/decision_schema.py

Data contracts for the Inventory Optimisation & Autonomous Control module
(Member 2) of the KPC Autonomous Supply Chain & Executive Control Plane.

These models define the AGREED INTERFACE between:

    Member 1 (Forecasting)   -->  provides forecast_demand_m3 / demand_std_m3
    Member 2 (this module)   -->  DecisionRequest in, AutonomousDecisionResponse out
    Member 4 (Backend/API)   -->  wraps engine.make_autonomous_decision() in
                                   POST /replenishment using these models
    Member 3 (Dashboard)     -->  consumes AutonomousDecisionResponse JSON

Nothing in this file talks to real KPC infrastructure. Every action produced
by the decision engine is explicitly marked SIMULATED — see
IMPORTANT SAFETY AND DEMONSTRATION PRINCIPLE in the project brief.

Requires: pydantic>=2.0
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# Enumerations — keep these in sync with rules/risk_rules.py,
# optimisation/replenishment_method.py and optimisation/dispatch_priority.py
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    """Inventory risk classification, driven by days of cover."""
    SAFE = "SAFE"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ReplenishmentAction(str, Enum):
    """Recommended / preferred replenishment mode."""
    PIPELINE_BATCH = "PIPELINE_BATCH"
    EMERGENCY_TRUCK = "EMERGENCY_TRUCK"
    NO_ACTION = "NO_ACTION"


class DispatchPriority(str, Enum):
    """Operational urgency assigned to a replenishment action."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ExecutionStatus(str, Enum):
    """
    Status of the decision itself. Always SIMULATED in this hackathon
    prototype — the platform never claims live control of KPC systems.
    """
    SIMULATED = "SIMULATED"


class ControlEventType(str, Enum):
    """Event type recorded on the simulated control-plane event log."""
    PIPELINE_BATCH_REQUEST = "PIPELINE_BATCH_REQUEST"
    TRUCK_DISPATCH_REQUEST = "TRUCK_DISPATCH_REQUEST"
    NO_ACTION = "NO_ACTION"


class ExecutionType(str, Enum):
    """How the control action would be carried out — always simulated."""
    SIMULATED_PIPELINE_BATCH = "SIMULATED_PIPELINE_BATCH"
    SIMULATED_TRUCK_DISPATCH = "SIMULATED_TRUCK_DISPATCH"
    NO_EXECUTION = "NO_EXECUTION"


# ---------------------------------------------------------------------------
# Request model — what Member 2's engine needs, and therefore what
# Member 4's backend must supply (sourced from Member 1's forecast output
# plus daily_operations.csv / depot_capacities.csv).
# ---------------------------------------------------------------------------

class DecisionRequest(BaseModel):
    """
    Input contract for engine.make_inventory_decision() /
    engine.make_autonomous_decision().

    depot / product identify the row. current_stock_m3, expected_receipts_m3,
    tank_capacity_m3 and pipeline/truck availability come from
    daily_operations.csv + depot_capacities.csv. forecast_demand_m3,
    average_daily_demand_m3 and demand_std_m3 come from Member 1's
    forecasting output (forecast_demand_m3 maps directly to the
    /forecast response; the other two are computed from recent history).
    """

    depot: str = Field(..., examples=["Eldoret"])
    product: str = Field(..., examples=["AGO", "PMS"])

    current_stock_m3: float = Field(..., ge=0)
    expected_receipts_m3: float = Field(..., ge=0)
    forecast_demand_m3: float = Field(..., ge=0)
    average_daily_demand_m3: float = Field(..., ge=0)
    demand_std_m3: float = Field(..., ge=0)
    lead_time_days: float = Field(..., ge=0)

    pipeline_available: bool
    truck_available: bool

    tank_capacity_m3: float = Field(..., gt=0)
    standard_batch_volume_m3: float = Field(default=10000, gt=0)

    # Optional pass-through so the forecast's own uncertainty can be
    # displayed on the dashboard alongside the decision (not used in
    # the calculation itself).
    forecast_confidence: Optional[float] = Field(default=None, ge=0, le=1)

    @model_validator(mode="after")
    def _check_stock_within_capacity(self) -> "DecisionRequest":
        if self.current_stock_m3 > self.tank_capacity_m3:
            raise ValueError(
                "current_stock_m3 cannot exceed tank_capacity_m3"
            )
        return self


# ---------------------------------------------------------------------------
# Response models — what Member 2 hands back to Member 4 (API) and,
# through it, to Member 3 (dashboard).
# ---------------------------------------------------------------------------

class DecisionResponse(BaseModel):
    """
    Mirrors the dict returned by engine.make_inventory_decision().
    This is the canonical "decision" object referenced throughout the
    project brief, e.g.:

        {
          "depot": "Eldoret",
          "product": "AGO",
          "risk_level": "CRITICAL",
          "recommended_action": "PIPELINE_BATCH",
          "recommended_volume_m3": 10000,
          "priority": "HIGH"
        }
    """

    depot: str
    product: str

    risk_level: RiskLevel
    stockout_probability: float = Field(..., ge=0, le=1)

    current_stock_m3: float = Field(..., ge=0)
    projected_stock_m3: float
    days_of_cover: float = Field(..., ge=0)
    safety_stock_m3: float = Field(..., ge=0)
    reorder_point_m3: float = Field(..., ge=0)

    required_replenishment_m3: float = Field(..., ge=0)
    recommended_action: ReplenishmentAction
    preferred_mode: ReplenishmentAction
    recommended_volume_m3: float = Field(..., ge=0)
    priority: DispatchPriority

    decision_reason: str
    execution_status: ExecutionStatus = ExecutionStatus.SIMULATED


class ControlEvent(BaseModel):
    """
    Mirrors the dict returned by control/event_log.create_event_record(),
    i.e. what gets appended to control_plane_events / events.json.
    """

    event_id: str
    event_type: ControlEventType

    depot: str
    product: str
    action: ReplenishmentAction
    volume_m3: float = Field(..., ge=0)
    priority: DispatchPriority

    execution_type: ExecutionType
    status: ExecutionStatus = ExecutionStatus.SIMULATED

    logged_at: datetime


class AutonomousDecisionResponse(BaseModel):
    """
    Mirrors the dict returned by engine.make_autonomous_decision().
    This is the single object Member 4 should return from
    POST /replenishment, and the single object Member 3's dashboard
    should consume for the "recent control-plane actions" panel.
    """

    decision: DecisionResponse
    control_event: ControlEvent