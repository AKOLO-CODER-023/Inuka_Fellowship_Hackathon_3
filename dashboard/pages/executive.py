import streamlit as st
import pandas as pd
import plotly.express as px

from roi.roi_engine import calculate_roi

def show_executive():

    st.title("Executive Command Center")

    st.caption(
        "KPC Autonomous Supply Chain Control Plane | "
        "ROI values are based on synthetic scenario assumptions."
    )


    # Load data

    roi_df = pd.read_csv(
        "data/roi_comparison_2026.csv"
    )

    cost_df = pd.read_csv(
        "data/cost_parameters.csv"
    )


    # Calculate ROI

    roi_result = calculate_roi(
        roi_df,
        cost_df
    )


    # ------------------------
    # KPI SECTION
    # ------------------------

    st.subheader("Business Impact Overview")


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Projected Annual Savings",
        f"KES {roi_result['total_savings_kes']:,.0f}"
    )


    col2.metric(
        "Year 1 ROI",
        f"{roi_result['roi_percentage']:.1f}%"
    )


    col3.metric(
        "Net Benefit",
        f"KES {roi_result['net_benefit_kes']:,.0f}"
    )


    col4, col5, col6 = st.columns(3)


    stockouts_prevented = (
        roi_df["baseline_stockout_days"].sum()
        -
        roi_df["autonomous_stockout_days"].sum()
    )


    emergency_reduction = (
        roi_df["emergency_m3_avoided"].sum()
    )


    service_improvement = (
        roi_df["service_level_autonomous_pct"].mean()
        -
        roi_df["service_level_baseline_pct"].mean()
    )


    col4.metric(
        "Stockout Days Avoided",
        f"{stockouts_prevented:.0f}"
    )


    col5.metric(
        "Emergency Volume Avoided",
        f"{emergency_reduction:,.0f} m³"
    )


    col6.metric(
        "Service Level Improvement",
        f"{service_improvement*100:.1f}%"
    )


    st.divider()


    # ------------------------
    # SAVINGS BREAKDOWN
    # ------------------------

    st.subheader("Savings Contribution")


    savings_df = pd.DataFrame({

        "Category": [
            "Stockout Prevention",
            "Emergency Logistics",
            "Manual Productivity"
        ],

        "KES Saved": [
            roi_result["stockout_savings_kes"],
            roi_result["emergency_logistics_savings_kes"],
            roi_result["manual_productivity_savings_kes"]
        ]

    })


    fig = px.bar(
        savings_df,
        x="Category",
        y="KES Saved",
        title="Annual Savings Breakdown"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ------------------------
    # SERVICE PERFORMANCE
    # ------------------------

    st.subheader(
        "Baseline vs Autonomous Service Performance"
    )


    service_df = pd.DataFrame({

        "Scenario": [
            "Baseline",
            "Autonomous"
        ],

        "Service Level (%)": [

            roi_df[
                "service_level_baseline_pct"
            ].mean()*100,

            roi_df[
                "service_level_autonomous_pct"
            ].mean()*100
        ]

    })


    fig2 = px.bar(
        service_df,
        x="Scenario",
        y="Service Level (%)",
        title="Service Level Improvement"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # ------------------------
    # MONTHLY TREND
    # ------------------------

    st.subheader(
        "Monthly Operational Improvement"
    )


    trend_df = roi_df[
        [
            "month_key",
            "service_level_baseline_pct",
            "service_level_autonomous_pct"
        ]
    ]


    trend_df = trend_df.melt(
        id_vars="month_key",
        var_name="Scenario",
        value_name="Service Level"
    )


    trend_df["Service Level"] = (
        trend_df["Service Level"] * 100
    )


    fig3 = px.line(
        trend_df,
        x="month_key",
        y="Service Level",
        color="Scenario",
        markers=True,
        title="Service Level Trend"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )