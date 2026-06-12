import pandas as pd


def categorize_age(age) -> str:
    if pd.isna(age) or age == 0:
        return "Unknown"
    elif age <= 18:
        return "0-18"
    elif age <= 30:
        return "19-30"
    elif age <= 50:
        return "31-50"
    else:
        return "51+"


def add_victim_features(df: pd.DataFrame) -> pd.DataFrame:
    print("  [victim] Adding age group...")
    df["age_group"] = df["victim_age"].apply(categorize_age)

    print("  [victim] Adding weapon flag...")
    df["weapon_flag"] = (
        df["weapon_description"].notna() &
        (df["weapon_description"].str.upper() != "UNKNOWN")
    ).astype(int)

    return df