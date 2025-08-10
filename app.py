import os
import json
import streamlit as st
import pandas as pd
from utils.api import fetch_bom_incidents
from utils.parser import unify_incidents_to_df

st.set_page_config(page_title="Incident & Roadworks Notifier", layout="wide")

st.title("🚗 Incident & Roadworks Notifier")

# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start date", pd.to_datetime("today") - pd.Timedelta(days=3))
end_date = st.sidebar.date_input("End date", pd.to_datetime("today"))
min_severity = st.sidebar.selectbox("Minimum severity", ["any", "Low", "Moderate", "High"])

# Load data
alerts_dict = {}

try:
    st.write("Fetching live BOM incidents...")
    alerts_dict["BOM"] = fetch_bom_incidents()
except Exception as e:
    st.warning(f"Live fetch failed: {e} — using sample data.")
    with open("sample_data/sample_bom.json", "r", encoding="utf-8") as f:
        alerts_dict["BOM"] = json.load(f)

# Convert to DataFrame
df = unify_incidents_to_df(alerts_dict)

if df.empty:
    st.error("No incidents found in the data.")
    st.stop()

# ✅ Ensure datetime columns are parsed before filtering
for col in ["date", "start", "end"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Convert date inputs to Timestamps
start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1)  # inclusive

# Apply filters
df_filtered = df[
    (df["start"].isna() | (df["start"] >= start_ts)) &
    (df["start"].isna() | (df["start"] <= end_ts))
]

if min_severity != "any" and "severity" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["severity"].str.lower() == min_severity.lower()]

# Display summary
st.subheader("Summary")
st.metric("Files processed", len(alerts_dict))
st.metric("Total incidents", len(df_filtered))
if "severity" in df_filtered.columns:
    st.metric("High severity incidents", (df_filtered["severity"].str.lower() == "high").sum())

# Data table
st.subheader("Incident Details")
st.dataframe(df_filtered)

# Plot
if not df_filtered.empty and "category" in df_filtered.columns:
    st.subheader("Incident Counts by Category")
    st.bar_chart(df_filtered["category"].value_counts())
else:
    st.info("No category data to plot.")


