"""
backend/forecast_service.py

Serves demand forecasts for a depot/product/date.

WHY THIS FILE EXISTS:
Member 1's forecasting/src/forecast_api.py expects a trained model file,
forecast_model_bundle.pkl, that has not been committed to the repo yet
(forecasting/model/ is still an empty placeholder). Rather than block the
backend on that file existing, this service:

  1. Tries to load the real trained model bundle, if it's ever added.
  2. Falls back to a naive baseline forecast computed live from
     data/forecasting_features.csv -- which already has a precomputed
     baseline_forecast_m3 column (a 7-day rolling average), plus lag
     features, for every historical and scenario date in the dataset.

This means /forecast returns a REAL, data-driven number today, and
upgrades automatically to Member 1's trained model the moment that file
is added -- no endpoint code needs to change.
"""

import logging
import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger("inuka-api")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODEL_BUNDLE_PATH = Path(__file__).resolve().parent.parent / "forecasting" / "model" / "forecast_model_bundle.pkl"
FEATURES_PATH = DATA_DIR / "forecasting_features.csv"

_FEATURES_TABLE: Optional[pd.DataFrame] = None
_RESIDUAL_STD: Optional[pd.Series] = None
_MODEL_BUNDLE: Optional[dict] = None


def _load_features() -> pd.DataFrame:
    """Load and lightly prepare forecasting_features.csv, once."""
    global _FEATURES_TABLE, _RESIDUAL_STD

    if _FEATURES_TABLE is not None:
        return _FEATURES_TABLE

    df = pd.read_csv(FEATURES_PATH, parse_dates=["date"])
    _FEATURES_TABLE = df

    # Historical residual of the naive baseline vs actual orders, per
    # depot/product -- used to build a real (not guessed) confidence band.
    known = df.dropna(subset=["baseline_forecast_m3"]).copy()
    known["error"] = known["customer_orders_m3"] - known["baseline_forecast_m3"]
    _RESIDUAL_STD = known.groupby(["depot", "product"])["error"].std()

    logger.info("Forecast baseline table loaded: %d rows.", len(df))
    return df


def _load_trained_model() -> Optional[dict]:
    """
    Try to load Member 1's trained model bundle. Returns None if it
    doesn't exist yet -- this is expected until forecasting/model/ is
    populated, and is not treated as an error.
    """
    global _MODEL_BUNDLE

    if _MODEL_BUNDLE is not None:
        return _MODEL_BUNDLE

    if not MODEL_BUNDLE_PATH.exists():
        return None

    try:
        with open(MODEL_BUNDLE_PATH, "rb") as f:
            _MODEL_BUNDLE = pickle.load(f)
        logger.info("Trained forecast model loaded: %s", _MODEL_BUNDLE.get("model_name"))
        return _MODEL_BUNDLE
    except Exception:
        logger.exception("Trained model bundle exists but failed to load; using baseline instead.")
        return None


def get_forecast(depot: str, product: str, date: str) -> dict:
    """
    Return a forecast for one depot/product/date.

    Tries the trained model first; falls back to the data-driven naive
    baseline if no trained model is available, or if the trained model
    fails to load or has no row for this depot/product/date.
    """
    target_date = pd.to_datetime(date)

    bundle = _load_trained_model()
    if bundle is not None:
        try:
            return _forecast_from_trained_model(bundle, depot, product, target_date)
        except _NoTrainedForecast:
            pass  # fall through to baseline below

    return _forecast_from_baseline(depot, product, target_date)


class _NoTrainedForecast(Exception):
    """Raised internally when the trained model has no usable row."""


def _forecast_from_trained_model(bundle: dict, depot: str, product: str, target_date: pd.Timestamp) -> dict:
    features_table = bundle["features_table"]
    row = features_table[
        (features_table.depot == depot) & (features_table["product"] == product) & (features_table.date == target_date)
    ]
    if row.empty:
        raise _NoTrainedForecast()

    row = row.copy()
    row["depot"] = row["depot"].astype("category")
    row["product"] = row["product"].astype("category")

    model = bundle["model"]
    lower_model = bundle["lower_model"]
    upper_model = bundle["upper_model"]
    all_features = bundle["all_features"]

    X_row = row[all_features]
    if bundle.get("model_kind") == "rf":
        X_row = X_row.assign(depot=X_row["depot"].cat.codes, product=X_row["product"].cat.codes)

    point = max(float(model.predict(X_row)[0]), 0.0)
    lower = max(min(float(lower_model.predict(X_row)[0]), point), 0.0)
    upper = max(float(upper_model.predict(X_row)[0]), point)

    return {
        "depot": depot,
        "product": product,
        "forecast_date": target_date.strftime("%Y-%m-%d"),
        "forecast_demand_m3": round(point, 2),
        "lower_bound_m3": round(lower, 2),
        "upper_bound_m3": round(upper, 2),
        "confidence": bundle.get("confidence_level", 0.9),
        "model_version": f"{bundle.get('model_name', 'trained').lower().replace(' ', '_')}_v1",
        "forecast_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _forecast_from_baseline(depot: str, product: str, target_date: pd.Timestamp) -> dict:
    df = _load_features()

    row = df[(df.depot == depot) & (df["product"] == product) & (df.date == target_date)]
    if row.empty:
        raise ValueError(
            f"No feature row for depot={depot!r}, product={product!r}, date={target_date.date()}."
        )

    row = row.iloc[0]
    point = row["baseline_forecast_m3"]
    if pd.isna(point):
        # Not enough history for the rolling baseline yet (first ~7 days
        # of the dataset) -- fall back to the most recent lag we have.
        point = row["demand_lag_1_m3"]
        if pd.isna(point):
            raise ValueError(
                f"Insufficient history to forecast depot={depot!r}, product={product!r}, date={target_date.date()}."
            )

    std = _RESIDUAL_STD.get((depot, product), point * 0.1) if _RESIDUAL_STD is not None else point * 0.1
    if pd.isna(std):
        std = point * 0.1

    lower = max(point - 1.64 * std, 0.0)  # ~90% band, naive-normal approximation
    upper = point + 1.64 * std

    return {
        "depot": depot,
        "product": product,
        "forecast_date": target_date.strftime("%Y-%m-%d"),
        "forecast_demand_m3": round(float(point), 2),
        "lower_bound_m3": round(float(lower), 2),
        "upper_bound_m3": round(float(upper), 2),
        "confidence": 0.90,
        "model_version": "naive_7day_baseline_v1",
        "forecast_timestamp": datetime.now(timezone.utc).isoformat(),
    }
