import os, json

sample_file = "sample_data/sample_bom.json"

if os.path.exists(sample_file):
    with open(sample_file, "r", encoding="utf-8") as f:
        sample_bom_data = json.load(f)
else:
    sample_bom_data = []
    print("⚠️ No sample BOM data found. Running without sample incidents.")
