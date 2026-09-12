# KPC Autonomous Supply Chain & Executive Control Plane - Synthetic Data Package

Start with `daily_operations.csv` for the operational control-plane model and `forecasting_features.csv` for demand forecasting.

Useful files:
- `daily_operations.csv`: primary autonomous-policy operational dataset
- `forecasting_features.csv`: lagged/model-ready demand features
- `pipeline_batches.csv`: autonomous replenishment batch events
- `control_plane_events.csv`: actionable alerts/actions for API/demo streaming
- `roi_comparison_2026.csv`: baseline vs autonomous scenario metrics
- `KPC_Synthetic_Control_Plane_Data.xlsx`: formatted workbook with documentation, validation and ROI formulas
- `generate_kpc_dataset.py`: reproducibility script

All operational records are synthetic. See `DATASET_CARD.md` before using the data.
