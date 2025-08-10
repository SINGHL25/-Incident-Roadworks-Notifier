# utils/api.py
import requests

def fetch_bom_incidents():
    """
    Fetch live BOM QLD Road Incidents.
    Falls back to raising exception if HTTP error occurs.
    """
    BOM_INCIDENTS_URL = "https://www.data.qld.gov.au/api/3/action/datastore_search"
    RESOURCE_ID = "3d4d3f1b-62f5-4c8f-85cd-3e4e1f7f4cf6"  # QLD Road Incidents
    params = {
        "resource_id": RESOURCE_ID,
        "limit": 500
    }

    resp = requests.get(BOM_INCIDENTS_URL, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    if not data.get("success") or "result" not in data:
        raise ValueError("Invalid response from BOM API")

    return data["result"]["records"]

