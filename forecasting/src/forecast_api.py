
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="KPC Demand Forecast Service", version="1.0")

# Loaded once at startup: trained model bundle + feature table
with open("forecast_model_bundle.pkl", "rb") as f:
    import pickle
    BUNDLE = pickle.load(f)

MODEL = BUNDLE["model"]
LOWER_MODEL = BUNDLE["lower_model"]
UPPER_MODEL = BUNDLE["upper_model"]
MODEL_KIND = BUNDLE["model_kind"]
MODEL_NAME = BUNDLE["model_name"]
FEATURE_COLS_NUMERIC = BUNDLE["feature_cols_numeric"]
ALL_FEATURES = BUNDLE["all_features"]
CONFIDENCE_LEVEL = BUNDLE["confidence_level"]
FEATURES_TABLE = pd.read_parquet("forecasting_features_snapshot.parquet")


class ForecastRequest(BaseModel):
    depot: str
    product: str
    date: str
    forecast_horizon_hours: Optional[int] = 24


class ForecastResponse(BaseModel):
    depot: str
    product: str
    forecast_date: str
    forecast_demand_m3: float
    lower_bound_m3: float
    upper_bound_m3: float
    confidence: float
    model_version: str
    forecast_timestamp: str


@app.post("/forecast", response_model=ForecastResponse)
def forecast(req: ForecastRequest):
    date = pd.to_datetime(req.date)
    row = FEATURES_TABLE[
        (FEATURES_TABLE.depot == req.depot)
        & (FEATURES_TABLE["product"] == req.product)
        & (FEATURES_TABLE.date == date)
    ]
    if row.empty:
        raise HTTPException(status_code=404, detail="No feature row for that depot/product/date.")
    row = row.copy()
    row["depot"] = row["depot"].astype("category")
    row["product"] = row["product"].astype("category")
    if row[FEATURE_COLS_NUMERIC].isna().any(axis=1).iloc[0]:
        raise HTTPException(status_code=422, detail="Insufficient history to forecast this date.")

    X_row = row[ALL_FEATURES]
    if MODEL_KIND == "rf":
        X_row = X_row.assign(depot=X_row["depot"].cat.codes, product=X_row["product"].cat.codes)

    point = max(float(MODEL.predict(X_row)[0]), 0.0)
    lower = max(min(float(LOWER_MODEL.predict(X_row)[0]), point), 0.0)
    upper = max(float(UPPER_MODEL.predict(X_row)[0]), point)

    return ForecastResponse(
        depot=req.depot,
        product=req.product,
        forecast_date=date.strftime("%Y-%m-%d"),
        forecast_demand_m3=round(point, 2),
        lower_bound_m3=round(lower, 2),
        upper_bound_m3=round(upper, 2),
        confidence=CONFIDENCE_LEVEL,
        model_version=f"{MODEL_NAME.lower().replace(chr(32), chr(95))}_v1",
        forecast_timestamp=datetime.utcnow().isoformat() + "Z",
    )


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}
