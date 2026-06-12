import pandas as pd


def categorize_time(hour: int) -> str:
    if 0 <= hour < 6:
        return "Late Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    print("  [time] Adding reporting delay...")
    df["reporting_delay_days"] = (df["reported_date"] - df["date_occurrence"]).dt.days

    print("  [time] Extracting date components...")
    df["year_occurrence"]       = df["date_occurrence"].dt.year
    df["month_occurrence"]      = df["date_occurrence"].dt.month
    df["day_of_week_num"]       = df["date_occurrence"].dt.dayofweek
    df["quarter_occurrence"]    = df["date_occurrence"].dt.quarter
    df["is_weekend_occurrence"] = (df["date_occurrence"].dt.dayofweek >= 5).astype(int)

    print("  [time] Adding night flag and time period...")
    df["is_night_occurrence"]   = (df["hour_occurrence"] < 6).astype(int)
    df["time_period_occurrence"] = df["hour_occurrence"].apply(categorize_time)

    return df