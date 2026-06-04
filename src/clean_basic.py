import pandas as pd


def clean_basic(df: pd.DataFrame) -> pd.DataFrame:

    # ── Dates ──────────────────────────────────────────────────────────────────
    df['reported_date']   = pd.to_datetime(df['reported_date'], format="mixed", errors='coerce')
    df['date_occurrence'] = pd.to_datetime(df['date_occurrence'], format="mixed", errors='coerce')

    invalid_dates = df[df['reported_date'] < df['date_occurrence']]
    print(f"Invalid date records (reported < occurred): {len(invalid_dates):,}")

    # ── Time → hour & minute ───────────────────────────────────────────────────
    df['time_occurrence'] = pd.to_numeric(df['time_occurrence'], errors='coerce')
    df['hour_occurrence']   = (df['time_occurrence'] // 100).astype('Int8')
    df['minute_occurrence'] = (df['time_occurrence'] % 100).astype('Int8')
    df.drop(columns=['time_occurrence'], inplace=True)

    # ── area_code → Int16 ──────────────────────────────────────────────────────
    df['area_code'] = pd.to_numeric(df['area_code'], errors='coerce').astype('Int16')

    # ── area_name → category ───────────────────────────────────────────────────
    df['area_name'] = df['area_name'].astype('category')

    # ── crime_part → boolean ───────────────────────────────────────────────────
    df['crime_part'] = df['crime_part'] == 1

    # ── reported_district_number → int32 ──────────────────────────────────────
    df['reported_district_number'] = df['reported_district_number'].astype('int32')

    # ── Duplicates ─────────────────────────────────────────────────────────────
    before = df.duplicated().sum()
    df = df.drop_duplicates().copy()
    print(f"Duplicates dropped: {before:,} → 0")

    # ── crime_code_description ─────────────────────────────────────────────────
    df['crime_code_description'] = df['crime_code_description'].str.lower()
    df['crime_code_description'] = df['crime_code_description'].astype('string[pyarrow]')

    # ── Mocodes → list ─────────────────────────────────────────────────────────
    df['Mocodes'] = df['Mocodes'].str.split()

    # ── status → category ──────────────────────────────────────────────────────
    df['status'] = df['status'].astype('category')

    # ── status_description ─────────────────────────────────────────────────────
    status_mapping = {
        'Invest Cont':  'Investigation Continues',
        'Adult Other':  'Adult Other',
        'Adult Arrest': 'Adult Arrest',
        'Juv Arrest':   'Juvenile Arrest',
        'Juv Other':    'Juvenile Other',
        'UNK':          'Unknown',
    }
    df['status_description'] = df['status_description'].replace(status_mapping)
    df['status_description'] = df['status_description'].astype('category')

    # ── crime_code_1 ───────────────────────────────────────────────────────────
    df = df.dropna(subset=['crime_code_1'])
    df['crime_code_1'] = df['crime_code_1'].astype('int16')

    # ── Drop crime_code 2, 3, 4 ───────────────────────────────────────────────
    df.drop(columns=['crime_code_2', 'crime_code_3', 'crime_code_4'], inplace=True)

    print(f"clean_basic done. Shape: {df.shape}")
    return df