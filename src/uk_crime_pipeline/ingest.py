"""
Stage 1 - INGEST 
Fetch raw street-crime data from th UK Police API nad save it
to the Bronze Layer aas JSON files (one file pre city per month)
"""
import json
import os
import time

import requests

from src.uk_crime_pipeline.config import BASE_API_URL, BRONZE_DIR, LOCATIONS, MONTHS

def fetch_crimes(lat, lng, date):
    """Call UK Police API  for one location + month. Returns a list of crimes dicts."""
    url = f"{BASE_API_URL}/crimes-street/all-crimes"
    params = {"lat": lat, "lng": lng, "date": date}
    response = requests.get(url, params=params, timeout=30)

    return response.json()

def save_raw(data, city, month):
    """Save a list of crime records to the Bronze Layer as Json."""
    filename = f"{city}_{month}.json"
    filepath = os.path.join(BRONZE_DIR, filename)

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    except PermissionError:
        print("Permission Error")
        raise

    return filepath

def run_ingest():
    """Main entry point - fetch and save data for evry city/month combo."""
    os.makedirs(BRONZE_DIR, exist_ok=True)
    total_records = 0

    for city_name, coords in LOCATIONS.items():
        for month in MONTHS:
            print(f"  Fetching {city_name} — {month} ...", end=" ")

            data = fetch_crimes(coords["lat"], coords["lng"], month)
            filepath = save_raw(data, city_name, month)

            print(f"{len(data)} records → {filepath}")
            total_records += len(data)

            time.sleep(1)  # be polite to the free API

    print(f"\nIngest complete. Total records saved: {total_records}")


if __name__ == "__main__":
    run_ingest()