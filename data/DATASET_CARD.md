# KPC Synthetic Downstream Operations Dataset v1.0

## Purpose
This dataset supports the KPC Inuka Fellowship Hackathon 3 use case: downstream demand forecasting, inventory replenishment, autonomous batch/dispatch decisions, monitoring, and executive ROI demonstration.

## Important disclosure
This is a **synthetic scenario dataset**. It does not contain confidential or actual KPC operational transaction records. Published KPC/EPRA statistics are used only as calibration anchors and hard constraints.

## Coverage
- Dates: 2021-01-01 to 2026-12-31
- Simulated-history cutoff: 2026-09-12
- Dates after 2026-09-12 are explicitly labelled `SCENARIO_FUTURE`
- Depots: Nairobi, Nakuru, Kisumu, Eldoret
- Products: PMS, AGO, DPK, JET_A1 where KPC publishes storage capacity
- Random seed: 20260912

## Official calibration anchors
1. KPC published depot/product storage capacities and pipeline flow rates: https://www.kpc.co.ke/wp-content/uploads/2026/01/Kenya_Pipeline_Company_IPO-4.pdf
2. EPRA annual domestic petroleum demand totals and FY2024/25 monthly demand seasonality: https://www.epra.go.ke/sites/default/files/2025-09/Statistics-Report-June-2025-Web.pdf
3. EPRA 2025/26 biannual statistics used only to inform the 2026 synthetic scenario: https://www.epra.go.ke/sites/default/files/2026-03/Biannual%20Statistics%20Report%202025-2026_0.pdf

## Core integrity constraints
- Closing stock = opening stock + pipeline receipts + emergency receipts - dispatch
- Stock cannot exceed published tank capacity
- Unsupported product/depot combinations are excluded
- Replenishment batches are constrained by a corridor flow-rate limit
- Operational failures, demand spikes, orders, rainfall and costs are synthetic

## Recommended ML target
`customer_orders_m3`

## Recommended train/test split
- Train: 2021-01-01 to 2024-12-31
- Validation: 2025-01-01 to 2025-12-31
- Test/demo: 2026-01-01 to 2026-09-12
- Scenario-only future: after 2026-09-12

## Limitations
This dataset is intended for prototyping, hackathon evaluation and architecture demonstrations. It must not be represented as actual KPC operations or used for real operational decisions without replacement by governed production data.
