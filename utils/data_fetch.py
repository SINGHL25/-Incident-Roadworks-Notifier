import os
import json
from dotenv import load_dotenv

load_dotenv()

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data")

# Example stub: try reading live API URL from env (not enabled by default)


def _load_sample(name="qld"):
    fname = f"sample_{name}.json"
    fp = os.path.join(SAMPLE_DIR, fname)
    try:
        with open(fp, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return []


def fetch_incidents(use_live=False, prefer="QLD sample"):
    """Return list of event dicts. If use_live is True and API configured, try to fetch.
    Otherwise return sample JSON.
    prefer: string hint which sample to return when not using uploaded files.
    """
    if use_live:
        # Implementers: add API calls to state transport services here.
        # For demo we fall back to samples.
        pass

    # choose sample
    if "QLD" in prefer:
        return _load_sample("qld")
    elif "NSW" in prefer:
        return _load_sample("nsw")
    else:
        return _load_sample("qld")
