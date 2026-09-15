import streamlit as st

from services.data_loader import load_daily_operations


def show_operations():

    st.header("Operations Control Room")

    df = load_daily_operations()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Depots",
        df["depot"].nunique()
    )

    col2.metric(
        "Products",
        df["product"].nunique()
    )

    col3.metric(
        "Stockout Events",
        df["stockout"].sum()
    )


    st.subheader("Depot Inventory")

    st.dataframe(
        df.head(20)
    )