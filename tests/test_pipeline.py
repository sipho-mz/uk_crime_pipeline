"""
test_pipeline.py — Basic checks that the pipeline works.
Run with: python -m pytest tests/ -v
"""
import os
import sys

from src.uk_crime_pipeline.config import BRONZE_DIR, SILVER_DIR, GOLD_DIR

def test_bronze_has_files():
    """Bronze should have at least 9 JSON files (3 cities x 3 months)."""
    files = [f for f in os.listdir(BRONZE_DIR) if f.endswith(".json")]
    assert len(files) >= 9, f"Expected >= 9 bronze files, got {len(files)}"

def test_silver_csv_exists_and_has_rows():
    """Silver CSV should exist and have data."""
    silver_path =  os.path.join(SILVER_DIR, "crimes_clean.csv")
    assert os.path.exists(silver_path), "Silver CSV not found"

    with open(silver_path, "r") as f:
        lines = f.readlines()
    assert len(lines) > 1, f"Silver CSV only has {len(lines)} lines"

def test_gold_tables_exist():
    """All four Gold tables should exist."""
    for name in ["crimes_by_category.csv", "monthly_trends.csv",
                 "outcome_summary.csv", "top_streets.csv"]:
        path = os.path.join(GOLD_DIR, name)
        assert os.path.exists(path), f"Gold table missing: {name}"

def test_silver_has_expected_columns():
    """Silver CSV should have the columns we defined."""
    silver_path = os.path.join(SILVER_DIR, "crimes_clean.csv")
    with open(silver_path) as f:
        header = f.readline().strip()

    expected_cols = {"category", "latitude", "longitude", "street_name",
                     "outcome_category", "outcome_date", "month", "quarter"}
    actual_cols = set(header.split(","))
    missing = expected_cols - actual_cols
    assert not missing, f"Missing columns: {missing}"