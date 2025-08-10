import os
import json
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from utils.data_fetch import fetch_incidents
from utils.parser import normalize_incidents
from utils.map_plotter import create_incident_map

load_dotenv()

st.set_page_config(page_title="Incident & Roadworks Notifier", layout="wide")
st.title("🚗 Incident & Roadworks Notifier — Local Demo")

st.sidebar.header("Data & Filters")
use_live = st.sidebar.checkbox("Try live API (if configured)", value=False)
source_choice = st.sidebar.selectbox("Default sample source", ["QLD sample", "NSW sample"])

# Time filters
days = st.sidebar.slider("Show last N days", 1, 30, 7)
min_severity = st.sidebar.selectbox("Minimum severity", ["any", "low", "medium", "high"])

st.sidebar.markdown("---")
if st.sidebar.button("Reload data"):
    st.experimental_rerun()

# Upload support
uploaded_files = st.sidebar.file_uploader("Upload incident JSON files (optional)", type=["json"], accept_multiple_files=True)

@st.cache_data(ttl=120)
def load_data(use_live, source_choice, uploaded_files):
    # Try uploaded files first
    combined = []
    if uploaded_files:
        for up in uploaded_files:
            try:
                j = json.load(up)
                combined.extend(j if isinstance(j, list) else [j])
            except Exception:
                continue
    else:
        # fetch (tries live if requested, otherwise sample)
        combined = fetch_incidents(use_live=use_live, prefer=source_choice)
    return combined

raw = load_data(use_live, source_choice, uploaded_files)

if not raw:
    st.warning("No data loaded — try unchecking 'Try live API' or upload a sample JSON file.")
    st.stop()

# Normalize
df = normalize_incidents(raw)
if df.empty:
    st.warning("Parsed data is empty after normalization.")
    st.stop()

# Apply filters
now = datetime.utcnow()
start_ts = now - pd.Timedelta(days=days)

# ensure date column is datetime
if "start" in df.columns:
    df["start"] = pd.to_datetime(df["start"], errors="coerce")
else:
    df["start"] = pd.NaT

df_filtered = df.copy()
if min_severity != "any":
    df_filtered = df_filtered[df_filtered["severity"].str.lower().isin([min_severity])]

if "start" in df_filtered.columns:
    df_filtered = df_filtered[(df_filtered["start"].isna()) | (df_filtered["start"] >= start_ts)]

st.sidebar.markdown(f"**Loaded events:** {len(df)} — Showing: {len(df_filtered)}")

# Layout
col1, col2 = st.columns((1, 2))

with col1:
    st.subheader("Filters & Table")
    if st.checkbox("Show raw DataFrame"):
        st.dataframe(df_filtered)

    csv = df_filtered.to_csv(index=False)
    st.download_button("Export CSV", data=csv, file_name="incidents.csv", mime="text/csv")

    st.markdown("---")
    st.subheader("Top event types")
    st.bar_chart(df_filtered["type"].value_counts())

with col2:
    st.subheader("Map")
    folium_map = create_incident_map(df_filtered)
    from streamlit_folium import folium_static
    folium_static(folium_map, width=900)

st.markdown("---")
st.subheader("Notes")
st.markdown("App uses sample JSON data if no live API configured. Drop JSON files exported from your source to test multiple-file parsing.")
