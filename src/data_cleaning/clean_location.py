import pandas as pd


def clean_location(df: pd.DataFrame) -> pd.DataFrame:

    # ── premise_code ───────────────────────────────────────────────────────────
    print(f"Missing premise_code: {df['premise_code'].isna().sum():,}")
    df = df.dropna(subset=['premise_code']).copy()
    df['premise_code'] = df['premise_code'].astype('int16')

    # ── premise_description ────────────────────────────────────────────────────
    df['premise_description'] = df['premise_description'].fillna('Unknown')
    df['premise_description'] = df['premise_description'].astype('string[pyarrow]')

    # ── weapon_used_code ───────────────────────────────────────────────────────
    df['weapon_used_code'] = df['weapon_used_code'].fillna(-1).astype('int16')

    # ── weapon_description ─────────────────────────────────────────────────────
    df['weapon_description'] = df['weapon_description'].fillna('Unknown | N/A')
    df['weapon_description'] = df['weapon_description'].astype('string[pyarrow]')

    # ── location ───────────────────────────────────────────────────────────────
    df['location'] = df['location'].str.strip().str.lower()
    df['location'] = df['location'].str.replace(r'\s+', ' ', regex=True)
    df['location'] = df['location'].astype('category')

    # ── cross_street ───────────────────────────────────────────────────────────
    df.drop(columns=['cross_street'], inplace=True)

    # ── coordinates ───────────────────────────────────────────────────────────
    df['latitude']  = df['latitude'].astype('float32')
    df['longitude'] = df['longitude'].astype('float32')

    before = len(df)
    df = df[
        df['latitude'].between(33, 35) &
        df['longitude'].between(-119, -117)
    ]
    print(f"Rows removed (out of LA bounds): {before - len(df):,}")

    zero_coords = df[(df['latitude'] == 0.0) | (df['longitude'] == 0.0)]
    print(f"Zero-coordinate rows remaining: {len(zero_coords):,}")

    print(f"clean_location done. Shape: {df.shape}")
    return df