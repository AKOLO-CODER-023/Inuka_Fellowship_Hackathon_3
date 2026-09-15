import streamlit as st

from pages.executive import show_executive


st.set_page_config(
    page_title="KPC Autonomous Control Plane",
    layout="wide"
)


page = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Executive Command Center"
    ]
)


if page == "Executive Command Center":
    show_executive()