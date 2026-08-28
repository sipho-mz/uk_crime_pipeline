"""
Stage 3 — PROCESS & COMPUTE (Silver layer)
Read the raw JSON from Bronze, flatten nested structures,
fix data types, and write a single clean CSV to Silver.
"""
import glob
import json
import os

import pandas as pd

from src.uk_crime_pipeline.config import BRONZE_DIR, SILVER_DIR


def load_bronze():
    """Load every JSON file in Bronze and return one big list of dicts."""
    all_records = []
    json_files = sorted(glob.glob(os.path.join(BRONZE_DIR, "*.json")))

    for filepath in json_files:
        with open(filepath) as f:
            records = json.load(f)
            all_records.extend(records)

    print(f"    Loaded {len(all_records)} raw records from {len(json_files)} files  ")
    return all_records

def flatten_record(record):
    """Flatten one nested crime record into a simple flat dict."""
    location = record.get("location") or {}
    street = record.get("street") or {}
    outcome = record.get("outcome_status") or {}

    return {
        "category": record.get("category", ""),
        "latitude": float(location.get("latitude") or 0),
        "longitude": float(location.get("longitude") or 0),
        "street_name": street.get("name", ""),
        "outcome_category": outcome.get("category", "No outcome recorded"),
        "outcome_date": outcome.get("date", ""),
        "month": record.get("month", ""),
    }

def clean_data(df):
    """Apply data-quality rules."""
    # 1. Drop rows with no category
    df = df[df["category"] != ""].copy()

    # 2. Convert "2025-06" string → proper date
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m")

    # 3. Derive a quarter column: "2025-Q2"
    df["quarter"] = df["month"].dt.to_period("Q").astype(str)

    df = df.reset_index(drop=True)
    return df

def run_process():
    """Main entry point — read Bronze, clean, write Silver."""
    os.makedirs(SILVER_DIR, exist_ok=True)

    raw = load_bronze()

    # Flatten every record (list comprehension)
    flat_records = [flatten_record(r) for r in raw]

    # Convert list of dicts → pandas DataFrame (think: spreadsheet)
    df = pd.DataFrame(flat_records)
    print(f"DataFrame shape before cleaning: {df.shape}")

    df = clean_data(df)
    print(f"DataFrame shape after cleaning: {df.shape}")

    silver_path = os.path.join(SILVER_DIR, "crimes_clean.parquet")
    df.to_parquet(silver_path, engine="pyarrow", compression="zstd")
    print(f"    Silver layer written -> {silver_path}")

    return df 

if __name__ == "__main__":
    run_process()


    