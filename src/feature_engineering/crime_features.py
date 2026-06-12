import pandas as pd


def categorize_crime(desc) -> str:
    if pd.isna(desc):
        return "Other"

    desc = desc.lower()

    if any(x in desc for x in ["homicide", "murder"]):
        return "Violent Crime"

    if any(x in desc for x in ["assault", "battery", "robbery"]):
        return "Violent Crime"

    if any(x in desc for x in ["burglary", "theft", "larceny"]):
        return "Property Crime"

    if any(x in desc for x in ["vehicle", "motor vehicle", "auto theft"]):
        return "Vehicle Crime"

    if any(x in desc for x in ["sexual", "rape", "incest"]):
        return "Sexual Crime"

    if any(x in desc for x in ["fraud", "identity", "forgery", "embezzlement"]):
        return "Financial Crime"

    if any(x in desc for x in ["drug", "narcotic", "controlled substance"]):
        return "Drug Crime"

    if any(x in desc for x in ["riot", "disorder", "disperse"]):
        return "Public Order"

    if any(x in desc for x in ["weapon", "firearm", "gun", "knife"]):
        return "Weapon Crime"

    return "Other"


def add_crime_features(df: pd.DataFrame) -> pd.DataFrame:
    print("  [crime] Categorizing crime descriptions...")
    df["crime_category"] = df["crime_code_description"].apply(categorize_crime)

    other_pct = (df["crime_category"] == "Other").mean()
    print(f"  [crime] Distribution:\n{df['crime_category'].value_counts()}")
    print(f"  [crime] 'Other' coverage: {other_pct:.1%}")

    return df