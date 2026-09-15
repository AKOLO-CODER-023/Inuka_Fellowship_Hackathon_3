from pathlib import Path
import pandas as pd


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


def load_control_events():
    return pd.read_csv(
        DATA_PATH / "control_plane_events.csv"
    )


def load_truck_operations():
    return pd.read_csv(
        DATA_PATH / "truck_operations_daily.csv"
    )