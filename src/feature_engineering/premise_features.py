import pandas as pd


def group_premise(x) -> str:
    x = str(x).lower()

    if "street" in x:
        return "Public Space"
    elif "residence" in x:
        return "Residential"
    elif "store" in x or "market" in x:
        return "Commercial"
    elif "parking" in x:
        return "Parking Area"
    else:
        return "Other"


def add_premise_features(df: pd.DataFrame) -> pd.DataFrame:
    print("  [premise] Grouping premise descriptions...")
    df["premise_group"] = df["premise_description"].apply(group_premise)

    other_pct = (df["premise_group"] == "Other").mean()
    print(f"  [premise] Distribution:\n{df['premise_group'].value_counts()}")
    print(f"  [premise] 'Other' coverage: {other_pct:.1%}")

    return df