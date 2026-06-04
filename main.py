import os
from pathlib import Path
from dotenv import load_dotenv

from src.load_data      import load_data
from src.clean_basic    import clean_basic
from src.clean_victims  import clean_victims
from src.clean_location import clean_location
from src.export         import export_data

load_dotenv()

DATA_PATH   = os.getenv("DATA_PATH")
INPUT_FILE  = Path(DATA_PATH) / "Crime_Data_from_2020_to_2024.csv" # type: ignore
OUTPUT_FILE = Path("data/processed/cleaned_crime_data.parquet")


def run_pipeline():
    print("\n── Load ──────────────────────────────────────────")
    df = load_data(INPUT_FILE)

    print("\n── Clean Basic ───────────────────────────────────")
    df = clean_basic(df)

    print("\n── Clean Victims ─────────────────────────────────")
    df = clean_victims(df)

    print("\n── Clean Location ────────────────────────────────")
    df = clean_location(df)

    print("\n── Export ────────────────────────────────────────")
    export_data(df, OUTPUT_FILE)

    print("\nPipeline complete.")


if __name__ == "__main__":
    run_pipeline()