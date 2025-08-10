import requests
import json
import os

BOM_API_URL = "https://www.data.qld.gov.au/api/3/action/datastore_search"
BOM_RESOURCE_ID = "3d4d3f1b-62f5-4c8f-85cd-3e4e1f7f4cf6"  # QLD incidents dataset

def fetch_bom_incidents():
    try:
        url = f"{BOM_API_URL}?resource_id={BOM_RESOURCE_ID}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        records = data.get("result", {}).get("records", [])
        return records
    except Exception as e:
        print(f"Live fetch failed: {e} — using sample data.")
        sample_file = "sample_data/sample_bom.json"
        if os.path.exists(sample_file):
            with open(sample_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

