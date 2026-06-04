import pandas as pd
import numpy as np


def clean_victims(df: pd.DataFrame) -> pd.DataFrame:

    # ── victim_age → Int8 ──────────────────────────────────────────────────────
    df['victim_age'] = pd.to_numeric(df['victim_age'], errors='coerce').astype('Int8')

    invalid_mask = df['victim_age'] <= 0
    print(f"Invalid victim_age (<=0): {invalid_mask.sum():,} ({invalid_mask.sum() * 100 / len(df):.2f}%)")
    df.loc[invalid_mask, 'victim_age'] = pd.NA

    # ── victim_age_status ──────────────────────────────────────────────────────
    df['victim_age_status'] = np.where(
        df['victim_age'].isna(), 'N/A', 'valid'
    )
    df['victim_age_status'] = df['victim_age_status'].astype('category')

    # ── Impute victim_age by crime-group median (victim crimes only) ───────────
    null_rate = (
        df.groupby('crime_code_description')['victim_age']
        .apply(lambda x: x.isna().mean())
    )
    no_victim_crimes = null_rate[null_rate >= 0.90].index
    no_victim_mask   = df['crime_code_description'].isin(no_victim_crimes)

    crime_group_median = (
        df[~no_victim_mask]
        .groupby('crime_code_description')['victim_age']
        .transform('median')
        .round()
        .astype('Int8')
    )
    df.loc[~no_victim_mask, 'victim_age'] = (
        df.loc[~no_victim_mask, 'victim_age'].fillna(crime_group_median)
    )

    print(f"NaN remaining — victim crimes:    {df.loc[~no_victim_mask, 'victim_age'].isna().sum():,}")
    print(f"NaN remaining — no-victim crimes: {df.loc[no_victim_mask,  'victim_age'].isna().sum():,}")

    # ── victim_sex ─────────────────────────────────────────────────────────────
    df['victim_sex'] = df['victim_sex'].replace({'H': 'Unknown', 'X': 'Unknown', '-': 'Unknown'})
    df['victim_sex'] = df['victim_sex'].fillna('Unknown')
    df['victim_sex'] = df['victim_sex'].astype('category')

    # ── victim_descent ─────────────────────────────────────────────────────────
    df['victim_descent'] = df['victim_descent'].replace({'-': 'X'})
    df['victim_descent'] = df['victim_descent'].fillna('X')
    df['victim_descent'] = df['victim_descent'].astype('category')

    print(f"clean_victims done. Shape: {df.shape}")
    return df