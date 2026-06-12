import os
from pathlib import Path
from dotenv import load_dotenv

from src.data_cleaning.load_data      import load_data
from src.data_cleaning.clean_basic    import clean_basic
from src.data_cleaning.clean_victims  import clean_victims
from src.data_cleaning.clean_location import clean_location
from src.data_cleaning.export         import export_data

from src.feature_engineering.time_features    import add_time_features
from src.feature_engineering.spatial_features import add_spatial_features
from src.feature_engineering.victim_features  import add_victim_features
from src.feature_engineering.crime_features   import add_crime_features
from src.feature_engineering.premise_features import add_premise_features

load_dotenv()

DATA_PATH   = os.getenv("DATA_PATH")
INPUT_FILE  = Path(DATA_PATH) / "Crime_Data_from_2020_to_2024.csv" # type: ignore
CLEAN_FILE  = Path("data/processed/cleaned_crime_data.parquet")
FE_FILE     = Path("data/processed/feature_engineered_crime_data.parquet")


def run_pipeline():
    print("\n── Load ──────────────────────────────────────────")
    df = load_data(INPUT_FILE)

    print("\n── Clean Basic ───────────────────────────────────")
    df = clean_basic(df)

    print("\n── Clean Victims ─────────────────────────────────")
    df = clean_victims(df)

    print("\n── Clean Location ────────────────────────────────")
    df = clean_location(df)

    print("\n── Export Cleaned ────────────────────────────────")
    export_data(df, CLEAN_FILE)

    print("\n── Feature Engineering ───────────────────────────")
    df = add_time_features(df)
    df = add_spatial_features(df)
    df = add_victim_features(df)
    df = add_crime_features(df)
    df = add_premise_features(df)

    print("\n── Export Feature Engineered ─────────────────────")
    export_data(df, FE_FILE)

    print("\nPipeline complete.")


if __name__ == "__main__":
    run_pipeline()