import pandas as pd


GRID_SIZE = 0.005  # ~500m resolution


def add_spatial_features(df: pd.DataFrame) -> pd.DataFrame:
    print("  [spatial] Adding area crime rate...")
    area_counts = df["area_name"].value_counts()
    area_crime_share = area_counts / len(df)
    df["area_crime_share"] = df["area_name"].map(area_crime_share)

    print("  [spatial] Binning coordinates...")
    df["lat_bin"] = (df["latitude"]  // GRID_SIZE) * GRID_SIZE
    df["lon_bin"] = (df["longitude"] // GRID_SIZE) * GRID_SIZE

    print("  [spatial] Merging crime count by location...")
    crime_count_by_location = (
        df.groupby(["lat_bin", "lon_bin"])
        .size()
        .reset_index(name="crime_count")
    )
    df = df.merge(crime_count_by_location, on=["lat_bin", "lon_bin"], how="left")

    return df