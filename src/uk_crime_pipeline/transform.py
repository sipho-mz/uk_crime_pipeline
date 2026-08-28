"""
Stage 4 — TRANSFORM & MODEL (Gold layer)
Load the Silver CSV into DuckDB, run SQL to create
business-ready aggregated tables, save as CSV in Gold.
"""
import os

import duckdb

from src.uk_crime_pipeline.config import GOLD_DIR, SILVER_DIR


def create_connection(silver_csv):
    """Open DuckDB and load the Silver CSV as a table called 'crimes'."""
    con = duckdb.connect()
    con.execute(f"""
        CREATE TABLE crimes AS
        SELECT * FROM read_csv_auto('{silver_csv}')
    """)

    count = con.execute("SELECT COUNT(*) FROM crimes").fetchone()[0]
    print(f"    Loaded {count:,} rows into DuckDB")
    return con

def build_crimes_by_category(con):
    """How many crimes of each type, per quarter?"""
    return con.execute("""
        SELECT
            quarter, 
            category,
            COUNT(*) AS crime_count
        From crimes
        GROUP BY quarter, category
        ORDER BY quarter, crime_count DESC
    """).fetchdf()

def build_monthly_trends(con):
    """Month-over-month crime counts by category."""
    return con.execute("""
        SELECT 
            month,
            category,
            COUNT(*) AS crime_count
        FROM crimes
        GROUP BY month, category
        ORDER BY month, crime_count DESC
    """).fetchdf()

def build_outcome_summary(con):
    """What happens after a crime is reported?"""
    return con.execute("""
        SELECT 
            category, 
            outcome_category,
            COUNT(*) AS count
        FROM crimes
        GROUP BY category, outcome_category
        ORDER BY category, count DESC
    """).fetchdf()

def build_top_streets(con):
    """Which streets have the most crime?"""
    return con.execute("""
        SELECT 
            street_name,
            category,
            COUNT(*) AS crime_count
        FROM crimes
        WHERE street_name != ''
        GROUP BY street_name, category
        ORDER BY crime_count DESC
        LIMIT 20
    """).fetchdf()

def run_transform():
    """Main entry point — run all Gold-layer SQL and save results."""
    os.makedirs(GOLD_DIR, exist_ok=True)
    silver_csv = os.path.join(SILVER_DIR, "crimes_clean.csv")

    con = create_connection(silver_csv)

    tables = {
        "crimes_by_category.csv": build_crimes_by_category(con),
        "monthly_trends.csv": build_monthly_trends(con),
        "outcome_summary.csv": build_outcome_summary(con),
        "top_streets.csv": build_top_streets(con),
    }

    for filename, df in tables.items():
        filepath = os.path.join(GOLD_DIR, filename)
        df.to_csv(filepath, index=False)
        print(f"    {filename}: {len(df)} rows → {filepath}")

        con.close()
        print("\nTransform complete. Gold layer ready for reporting.")

if __name__ == "__main__":
    run_transform()