import pandas as pd
from typing import List, Dict


def normalize_incidents(raw: List[Dict]) -> pd.DataFrame:
    """Normalize a list of incident dicts into a DataFrame with columns:
    id, title, description, lat, lon, severity, start, end, type, source
    This function includes heuristics for the sample schemas.
    """
    rows = []
    for i, e in enumerate(raw):
        # try common fields first
        title = e.get("title") or e.get("event") or e.get("description") or e.get("msg") or ""
        desc = e.get("description") or e.get("details") or e.get("msg") or ""
        lat = e.get("lat") or e.get("latitude") or e.get("y")
        lon = e.get("lon") or e.get("longitude") or e.get("x")
        severity = str(e.get("severity") or e.get("level") or e.get("urgency") or "unknown").lower()
        st = e.get("start_time") or e.get("start") or e.get("time") or e.get("timestamp")
        end = e.get("end_time") or e.get("end")
        typ = e.get("type") or e.get("category") or e.get("event_type") or "incident"
        source = e.get("source") or e.get("feed") or e.get("system") or "sample"

        # some samples might embed lat/lon in a 'location' object
        if not lat and isinstance(e.get("location"), dict):
            lat = e.get("location", {}).get("lat")
            lon = e.get("location", {}).get("lon")

        # ensure numeric coords
        try:
            lat = float(lat) if lat is not None else None
        except Exception:
            lat = None
        try:
            lon = float(lon) if lon is not None else None
        except Exception:
            lon = None

        rows.append({
            "id": e.get("id") or f"sample-{i}",
            "title": title,
            "description": desc,
            "lat": lat,
            "lon": lon,
            "severity": severity,
            "start": st,
            "end": end,
            "type": typ,
            "source": source,
        })

    df = pd.DataFrame(rows)
    # normalize datetimes
    if "start" in df.columns:
        df["start"] = pd.to_datetime(df["start"], errors="coerce")
    if "end" in df.columns:
        df["end"] = pd.to_datetime(df["end"], errors="coerce")

    # fill missing lat/lon with NaN
    if "lat" not in df.columns:
        df["lat"] = None
    if "lon" not in df.columns:
        df["lon"] = None

    return df
