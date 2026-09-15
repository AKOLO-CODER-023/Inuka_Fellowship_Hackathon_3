import pandas as pd
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_PATH / "data"


def load_roi_comparison():

    return pd.read_csv(
        DATA_PATH / "roi_comparison_2026.csv"
    )


def load_cost_parameters():

    return pd.read_csv(
        DATA_PATH / "cost_parameters.csv"
    )


def load_daily_operations():

    return pd.read_csv(
        DATA_PATH / "daily_operations.csv"
    )


def load_pipeline_batches():

    return pd.read_csv(
        DATA_PATH / "pipeline_batches.csv"
    )


def load_truck_operations():

    return pd.read_csv(
        DATA_PATH / "truck_operations_daily.csv"
    )


def load_control_events():

    return pd.read_csv(
        DATA_PATH / "control_plane_events.csv"
    )