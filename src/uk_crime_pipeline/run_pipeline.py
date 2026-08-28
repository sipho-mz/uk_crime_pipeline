"""
run_pipeline.py — Run all stages in sequence.
"""
from src.uk_crime_pipeline.ingest import run_ingest
from src.uk_crime_pipeline.process import run_process
from src.uk_crime_pipeline.transform import run_transform


def main():
    print("=" * 60)
    print("  UK CRIME DATA PIPELINE")
    print("=" * 60)

    print("\n── Stage 1: Ingest (Bronze) ──")
    run_ingest()

    print("\n── Stage 3: Process (Silver) ──")
    run_process()

    print("\n── Stage 4: Transform (Gold) ──")
    run_transform()

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()