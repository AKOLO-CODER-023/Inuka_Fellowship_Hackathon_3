import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPC Control Plane", layout="wide")

roi = pd.read_csv("../data/roi_comparison_2026.csv")
costs = pd.read_csv("../data/cost_parameters.csv")

st.title("KPC Executive Control Plane")
st.dataframe(roi.head()) 