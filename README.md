# UK Crime Data Pipeline

A Python data lakehouse pipeline implemented using a **Medallion Architecture**. It automates the extraction, processing, and transformation of public UK crime data from raw API payloads into clean assets ready for business intelligence.

## 🏗️ Architecture & Data Flow


* **`src/uk_crime_pipeline/ingest.py` (Bronze Layer):** Fetches raw data from the public UK Crime API and saves it directly to disk as `.json` files.
* **`src/uk_crime_pipeline/process.py` (Silver Layer):** Reads the raw JSON files, flattens/normalises the data structures, and writes the output as optimized `.parquet` files.
* **`src/uk_crime_pipeline/transform.py` (Gold Layer):** Mounts the Parquet files into **DuckDB** to execute analytical SQL transformations, exporting final reporting metrics into `.csv` files.

---

## 🚀 Quick Start

### Installation
This project manages dependencies via `pyproject.toml`. Install the package and its requirements using your preferred package manager (e.g., `pip`, `poetry`, or `uv`):

```bash
pip install .
```

### Execution
Run the stages sequentially to process the data:

```bash
python -m src.uk_crime_pipeline.run_pipeline
```
