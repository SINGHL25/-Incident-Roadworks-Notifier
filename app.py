import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from utils.api import fetch_qld_incidents, fetch_qld_roadworks
from utils.parser import unify_incidents_to_df

# -----------------------------
# Streamlit page config
# -----------------------------
st.set_page_config(
    page_title="🚦 Incident & Roadworks Notifier",
    layout="wide"
)

st.title("🚦 Incident & Roadworks Notifier — QLD Live + Sample Data")
st.markdown(
    "Push notifications for accidents, diversions, or planned maintenance. "
    "Data from QLD Gov Open Data feeds."
)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

# Default date range: last 7 days
today = datetime.today()
default_start = today - timedelta(days=7)
default_end = today

start_date = st.sidebar.date_input("Start date", default_start)
end_date = st.sidebar.date_input("End date", default_end)

min_severity = st.sidebar.selectbox(
    "Minimum severity",
    options=["any", "Low", "Moderate", "High", "Severe"],
    index=0
)

data_source_choice = st.sidebar.multiselect(
    "Data sources",
    ["Incidents", "Roadworks"],
    default=["Incidents", "Roadworks"]
)

# Convert to datetime for filtering
start_ts = datetime.combine(start_date, datetime.min.time())
end_ts = datetime.combine(end_date, datetime.max.time())

# -----------------------------
# Data fetching
# -----------------------------
st.info("Fetching data...")
alerts_dict = {}

try:
    if "Incidents" in data_source_choice:
        alerts_dict["Incidents"] = fetch_qld_incidents()
    if "Roadworks" in data_source_choice:
        alerts_dict["Roadworks"] = fetch_qld_roadworks()
except Exception as e:
    st.error(f"Live fetch failed: {e} — using sample data.")
    # Fallback to local sample files
    try:
        if "Incidents" in data_source_choice:
            alerts_dict["Incidents"] = json.load(open("sample_data/sample_incidents.json"))
        if "Roadworks" in data_source_choice:
            alerts_dict["Roadworks"] = json.load(open("sample_data/sample_roadworks.json"))
    except FileNotFoundError as fe:
        st.error(f"Sample data missing: {fe}")
        alerts_dict = {}

# -----------------------------
# Data parsing
# -----------------------------
if alerts_dict:
    df = unify_incidents_to_df(alerts_dict)

    # Ensure datetime columns are parsed safely
    for col in ["start", "end", "date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Filter by date range
    df_filtered = df.copy()
    if "start" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["start"].isna()) | (df_filtered["start"] >= start_ts)
        ]
    if "end" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["end"].isna()) | (df_filtered["end"] <= end_ts)
        ]

    # Filter by severity
    if min_severity != "any" and "severity" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["severity"] == min_severity]

    # -----------------------------
    # Summary section
    # -----------------------------
    st.subheader("Summary of Alerts")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Files processed", len(alerts_dict))
    col2.metric("Total alerts", len(df_filtered))
    col3.metric("Unique areas", df_filtered["location"].nunique() if "location" in df_filtered else 0)
    col4.metric("Data period", f"{start_date} to {end_date}")

    # -----------------------------
    # Event details
    # -----------------------------
    st.subheader("Event Details Table")
    st.dataframe(df_filtered, use_container_width=True)

    # -----------------------------
    # Charts
    # -----------------------------
    if not df_filtered.empty:
        st.subheader("Top Event Counts")
        if "category" in df_filtered.columns:
            st.bar_chart(df_filtered["category"].value_counts())
        elif "type" in df_filtered.columns:
            st.bar_chart(df_filtered["type"].value_counts())

        st.subheader("Events Over Time")
        if "date" in df_filtered.columns:
            df_time = df_filtered.groupby(df_filtered["date"].dt.date).size()
            st.line_chart(df_time)
    else:
        st.warning("No alerts match the selected filters.")
else:
    st.warning("No data to display. Please check your data sources or sample files.")

