
"""
backend/schemas.py
Data validation models for the Inuka backend.
"""

try:
    from pydantic import BaseModel, Field  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    from pydantic.v1 import BaseModel, Field  # type: ignore[import-not-found,no-redef]


class ForecastRequest(BaseModel):
    depot: str
    product: str
    forecast_demand_m3: float = Field(..., ge=0)


class InventoryItem(BaseModel):
    depot: str
    product: str
    current_stock_m3: float = Field(..., ge=0)
    average_daily_demand_m3: float = Field(..., ge=0)
    tank_capacity_m3: float = Field(..., gt=0)


class ReplenishmentRequest(BaseModel):
    depot: str
    product: str

    current_stock_m3: float = Field(..., ge=0)
    expected_receipts_m3: float = Field(..., ge=0)
    forecast_demand_m3: float = Field(..., ge=0)
    average_daily_demand_m3: float = Field(..., ge=0)
    demand_std_m3: float = Field(..., ge=0)

    lead_time_days: float = Field(..., ge=0)
    pipeline_available: bool = False
    truck_available: bool = False
    tank_capacity_m3: float = Field(..., gt=0)

    standard_batch_volume_m3: float = Field(
        default=10000,
        gt=0
    )


class ForecastResponse(BaseModel):
    depot: str
    product: str
    forecast_demand_m3: float


class HealthResponse(BaseModel):
    status: str
    service: str