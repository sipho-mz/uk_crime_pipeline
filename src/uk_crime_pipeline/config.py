#config.py - Central setting for pipeline

import os 

# API Settings

BASE_API_URL = "https://data.police.uk/api"

LOCATIONS = {
    "leicester": {"lat": 52.629729, "lng": -1.131592},
    "birmingham": {"lat": 52.486243, "lng": -1.890401},
    "liverpool": {"lat": 53.408371, "lng": -2.991570},
}

# Months to fetch (the API requires YYYY-MM format).
MONTHS = ["2025-04", "2025-05", "2025-06"]

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BRONZE_DIR = os.path.join(DATA_DIR, "bronze")
SILVER_DIR = os.path.join(DATA_DIR, "silver")
GOLD_DIR = os.path.join(DATA_DIR, "gold")