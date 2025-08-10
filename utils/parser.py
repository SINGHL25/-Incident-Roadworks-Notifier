import pandas as pd

def unify_incidents_to_df(alerts_dict):
    """
    Convert incidents/roadworks JSON dict to a unified DataFrame.
    Ensures all date fields are proper datetime objects.
    """
    dfs = []
    for src, data in alerts_dict.items():
        if not data:
            continue
        try:
            records = data.get("result", {}).get("records", [])
        except AttributeError:
            records = data  # Already a list

        if not isinstance(records, list) or not records:
            continue

        df = pd.DataFrame(records)
        df["source"] = src

        # Convert potential date fields
        for col in ["created", "last_updated", "start", "end"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Standardize main date column
        if "created" in df.columns:
            df["date"] = df["created"]
        elif "last_updated" in df.columns:
            df["date"] = df["last_updated"]
        else:
            df["date"] = pd.NaT

        # Fill missing fields
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

    # Final safety: ensure all datetime fields are datetime
    for col in ["date", "start", "end"]:
        if col in df_all.columns:
            df_all[col] = pd.to_datetime(df_all[col], errors="coerce")

    return df_all

