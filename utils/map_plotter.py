import folium
from folium.plugins import MarkerCluster


def create_incident_map(df):
    # choose center
    if not df.empty and df["lat"].notna().any() and df["lon"].notna().any():
        avg_lat = df.loc[df["lat"].notna(), "lat"].astype(float).mean()
        avg_lon = df.loc[df["lon"].notna(), "lon"].astype(float).mean()
    else:
        # fallback to Australia center
        avg_lat, avg_lon = -25.0, 134.0

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)
    cluster = MarkerCluster().add_to(m)

    for _, r in df.iterrows():
        lat = r.get("lat")
        lon = r.get("lon")
        if lat is None or lon is None or pd.isna(lat) or pd.isna(lon):
            continue
        popup = folium.Popup(f"<b>{r.get('title')}</b><br/>{r.get('description')}<br/><i>Severity: {r.get('severity')}</i>", max_width=350)
        color = "orange"
        sev = str(r.get("severity") or "").lower()
        if "high" in sev or "warning" in sev:
            color = "red"
        elif "low" in sev or "info" in sev:
            color = "green"

        folium.CircleMarker(location=[lat, lon], radius=6, color=color, fill=True, fill_opacity=0.8, popup=popup).add_to(cluster)

    return m
