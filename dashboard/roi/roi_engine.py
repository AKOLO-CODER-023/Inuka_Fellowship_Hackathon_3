import pandas as pd


def extract_assumptions(cost_df: pd.DataFrame):

    return dict(
        zip(
            cost_df["parameter"],
            cost_df["value"]
        )
    )


def calculate_roi(
    roi_df: pd.DataFrame,
    cost_df: pd.DataFrame
):

    assumptions = extract_assumptions(cost_df)


    # Avoided stockout impact
    stockout_savings = (
        roi_df["stockout_m3_avoided"].sum()
        *
        assumptions[
            "stockout_value_at_risk_per_m3_kes"
        ]
    )


    # Reduced emergency transportation cost
    emergency_logistics_savings = (
        roi_df["emergency_m3_avoided"].sum()
        *
        assumptions[
            "emergency_logistics_premium_per_m3_kes"
        ]
    )


    # Reduced manual intervention
    manual_actions_reduced = (
        roi_df["baseline_batch_actions"].sum()
        -
        roi_df["autonomous_batch_actions"].sum()
    )

    manual_productivity_savings = (
        manual_actions_reduced
        *
        assumptions[
            "manual_intervention_cost_per_action_kes"
        ]
    )


    total_savings = (
        stockout_savings
        +
        emergency_logistics_savings
        +
        manual_productivity_savings
    )


    total_investment = (
        assumptions[
            "implementation_cost_kes"
        ]
        +
        assumptions[
            "annual_support_cost_kes"
        ]
    )


    net_benefit = (
        total_savings
        -
        total_investment
    )


    roi_percentage = (
        net_benefit
        /
        total_investment
    ) * 100


    return {
        "stockout_savings_kes": stockout_savings,
        "emergency_logistics_savings_kes": emergency_logistics_savings,
        "manual_productivity_savings_kes": manual_productivity_savings,
        "total_savings_kes": total_savings,
        "investment_kes": total_investment,
        "net_benefit_kes": net_benefit,
        "roi_percentage": roi_percentage
    }
