import requests
import json

# Queensland Gov open data URLs
INCIDENTS_URL = "https://data.qld.gov.au/api/3/action/datastore_search?resource_id=3d4d3f1b-62f5-4c8f-85cd-3e4e1f7f4cf6"
ROADWORKS_URL = "https://data.qld.gov.au/api/3/action/datastore_search?resource_id=d07c8e6e-4130-4c8f-8bfc-21ffbf3d6b65"

def fetch_qld_incidents():
    """Fetch live traffic incidents from Queensland Open Data."""
    try:
        resp = requests.get(INCIDENTS_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        raise RuntimeError(f"BOM QLD Incidents fetch failed: {e}")

def fetch_qld_roadworks():
    """Fetch live roadworks from Queensland Open Data."""
    try:
        resp = requests.get(ROADWORKS_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        raise RuntimeError(f"BOM QLD Roadworks fetch failed: {e}")
