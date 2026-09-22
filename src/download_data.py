from pathlib import Path

import pandas as pd
import requests


DATASET_ID = "5zyy-y8am"
DOWNLOAD_URL = (
    f"https://data.cityofnewyork.us/api/views/"
    f"{DATASET_ID}/rows.csv?accessType=DOWNLOAD"
)

project_root = Path(__file__).resolve().parents[1]
raw_data_directory = project_root / "data" / "raw"
output_path = raw_data_directory / "nyc_building_energy.csv"

raw_data_directory.mkdir(parents=True, exist_ok=True)

print("Downloading NYC building energy data...")



with requests.get(DOWNLOAD_URL, stream=True, timeout=180) as response:
    response.raise_for_status()

    with output_path.open("wb") as output_file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                output_file.write(chunk)

file_size_mb = output_path.stat().st_size / (1024 * 1024)
sample = pd.read_csv(output_path, nrows=5, low_memory=False)

print(f"Saved data to: {output_path}")
print(f"File size: {file_size_mb:.2f} MB")
print(f"Number of columns: {len(sample.columns)}")
print("\nFirst 20 column names:")
print(sample.columns[:20].tolist())