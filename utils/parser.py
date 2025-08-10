import pandas as pd

def unify_incidents_to_df(alerts_dict):
    """
    Convert incidents/roadworks JSON dict to a unified DataFrame.
    Expected format: { "Incidents": {...}, "Roadworks": {...} }
    """
    dfs = []
    for src, data in alerts_dict.items():
        if not data:
            continue
        try:
            # Queensland data is in result.records
            records = data.get("result", {}).get("records", [])
        except AttributeError:
            records = data  # If it's already a list

        if not isinstance(records, list):
            continue

        df = pd.DataFrame(records)

        # Normalize columns
        df["source"] = src
        if "created" in df.columns:
            df["date"] = pd.to_datetime(df["created"], errors="coerce")
        elif "last_updated" in df.columns:
            df["date"] = pd.to_datetime(df["last_updated"], errors="coerce")
        else:
            df["date"] = pd.NaT

        if "start" not in df.columns:
            df["start"] = df["date"]

        if "location" not in df.columns and "region" in df.columns:
            df["location"] = df["region"]

        if "category" not in df.columns and "event_type" in df.columns:
            df["category"] = df["event_type"]

        if "severity" not in df.columns:
            df["severity"] = "Unknown"

        dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    df_all = pd.concat(dfs, ignore_index=True)
    return df_all

