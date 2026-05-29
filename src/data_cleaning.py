# Setup & Load Data

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")

pd.set_option("display.max_columns", None)

file_path = Path(DATA_PATH) / "Crime_Data_from_2020_to_2024.csv"  # type: ignore

df = pd.read_csv(file_path)

print(df.info())

# ── Column Renaming ────────────────────────────────────────────────────────────

columns_to_rename = {
    'Date Rptd':      'reported_date',
    'DATE OCC':       'date_occurrence',
    'TIME OCC':       'time_occurrence',
    'AREA':           'area_code',
    'AREA NAME':      'area_name',
    'Part 1-2':       'crime_part',
    'Rpt Dist No':    'reported_district_number',
    'Crm Cd':         'crime_code',
    'Crm Cd Desc':    'crime_code_description',
    'Premis Cd':      'premise_code',
    'Premis Desc':    'premise_description',
    'Weapon Used Cd': 'weapon_used_code',
    'Weapon Desc':    'weapon_description',
    'Status':         'status',
    'Status Desc':    'status_description',
    'Crm Cd 1':       'crime_code_1',
    'Crm Cd 2':       'crime_code_2',
    'Crm Cd 3':       'crime_code_3',
    'Crm Cd 4':       'crime_code_4',
    'Vict Age':       'victim_age',
    'Vict Sex':       'victim_sex',
    'Vict Descent':   'victim_descent',
    'LOCATION':       'location',
    'Cross Street':   'cross_street',
    'LAT':            'latitude',
    'LON':            'longitude',
}

df.rename(columns=columns_to_rename, inplace=True)

# ── Drop Identifier Column ─────────────────────────────────────────────────────

df.drop(columns=['DR_NO'], inplace=True)

# ── Parse & Validate Date Columns ─────────────────────────────────────────────

df['reported_date'] = pd.to_datetime(df['reported_date'], format='mixed')
df['date_occurrence'] = pd.to_datetime(df['date_occurrence'], format='mixed')

invalid_dates = df[df['reported_date'] < df['date_occurrence']]
print(f"Invalid date records: {len(invalid_dates)}")

# ── area_code → int8 ───────────────────────────────────────────────────────────

df['area_code'] = df['area_code'].astype('int8')

# ── Split time_occurrence into hour & minute ───────────────────────────────────

df['time_occurrence'] = df['time_occurrence'].apply(lambda x: f"{int(x):04d}")
df['hour_occurrence'] = df['time_occurrence'].str[:2].astype('int8')
df['minute_occurrence'] = df['time_occurrence'].str[2:].astype('int8')
df.drop(columns=['time_occurrence'], inplace=True)

# ── area_name → category ───────────────────────────────────────────────────────

df['area_name'] = df['area_name'].astype('category')

# ── crime_part → boolean ───────────────────────────────────────────────────────
# True = Part 1 (serious), False = Part 2

df['crime_part'] = df['crime_part'] == 1

# ── reported_district_number → int32 ──────────────────────────────────────────

df['reported_district_number'] = df['reported_district_number'].astype('int32')

# ── Drop duplicates ────────────────────────────────────────────────────────────

print(f"Duplicates before: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Duplicates after:  {df.duplicated().sum()}")

# ── Normalize crime_code_description ──────────────────────────────────────────

df['crime_code_description'] = df['crime_code_description'].str.lower()
df['crime_code_description'] = df['crime_code_description'].astype('string[pyarrow]')

# ── Split Mocodes ──────────────────────────────────────────────────────────────

df['Mocodes'] = df['Mocodes'].fillna('').str.split(' ')
df['Mocodes'] = df['Mocodes'].apply(
    lambda x: np.nan if x == [''] or x == [] else x
)

# ── Handle Invalid victim_age ──────────────────────────────────────────────────

df['victim_age'] = df['victim_age'].astype('Int8')

invalid_mask = df['victim_age'] <= 0
print(f"Invalid victim_age: {(invalid_mask.sum() * 100 / len(df)):.2f}%")

df.loc[invalid_mask, 'victim_age'] = np.nan

df['victim_age_status'] = 'valid'
df.loc[df['victim_age'].isna(), 'victim_age_status'] = 'N/A'
df['victim_age_status'] = df['victim_age_status'].astype('category')

# ── Impute victim_age by crime-group median (victim crimes only) ───────────────

null_rate = (
    df.groupby('crime_code_description')['victim_age']
    .apply(lambda x: x.isna().mean())
)

no_victim_crimes = null_rate[null_rate >= 0.90].index
no_victim_mask = df['crime_code_description'].isin(no_victim_crimes)

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

print(f"NaN in victim crimes:    {df.loc[~no_victim_mask, 'victim_age'].isna().sum()}")
print(f"NaN in no-victim crimes: {df.loc[no_victim_mask, 'victim_age'].isna().sum()}")

# ── Clean victim_sex ───────────────────────────────────────────────────────────

df['victim_sex'] = df['victim_sex'].replace({'H': 'Unknown', 'X': 'Unknown', '-': 'Unknown'})
df['victim_sex'] = df['victim_sex'].fillna('Unknown')
df['victim_sex'] = df['victim_sex'].astype('category')

# ── Fill Missing victim_descent ────────────────────────────────────────────────

df['victim_descent'] = df['victim_descent'].replace({'-': 'X'})
df['victim_descent'] = df['victim_descent'].fillna('X')
df['victim_descent'] = df['victim_descent'].astype('category')

# ── Premise Code ───────────────────────────────────────────────────────────────

print(f"Missing premise_code: {df['premise_code'].isna().sum()}")
df = df.dropna(subset=['premise_code'])
df['premise_code'] = df['premise_code'].astype('int16')

# ── Premise Description ────────────────────────────────────────────────────────

df['premise_description'] = df['premise_description'].fillna('Unknown')
df['premise_description'] = df['premise_description'].astype('string[pyarrow]')

# ── Weapon Used Code ───────────────────────────────────────────────────────────

df['weapon_used_code'] = df['weapon_used_code'].fillna(-1).astype('int16')

# ── Weapon Description ─────────────────────────────────────────────────────────

df['weapon_description'] = df['weapon_description'].fillna('Unknown | N/A')
df['weapon_description'] = df['weapon_description'].astype('string[pyarrow]')

# ── Status ─────────────────────────────────────────────────────────────────────

df['status'] = df['status'].astype('category')

# ── Status Description ─────────────────────────────────────────────────────────

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

# ── Crime Code 1 ───────────────────────────────────────────────────────────────

df = df.dropna(subset=['crime_code_1', 'premise_code'])
df['crime_code_1'] = df['crime_code_1'].astype('int16')

# ── Drop Crime Codes 2, 3, 4 ──────────────────────────────────────────────────

df.drop(columns=['crime_code_2', 'crime_code_3', 'crime_code_4'], inplace=True)

# ── Location ───────────────────────────────────────────────────────────────────

df['location'] = df['location'].str.strip().str.lower()
df['location'] = df['location'].str.replace(r'\s+', ' ', regex=True)
df['location'] = df['location'].astype('category')

# ── Drop Cross Street ──────────────────────────────────────────────────────────

df.drop(columns=['cross_street'], inplace=True)

# ── Longitude ──────────────────────────────────────────────────────────────────

df['longitude'] = df['longitude'].astype('float32')

# ── Latitude ───────────────────────────────────────────────────────────────────

df['latitude'] = df['latitude'].astype('float32')

# Filter to Los Angeles bounds
df = df[
    df['latitude'].between(33, 35) &
    df['longitude'].between(-119, -117)
]

# Verify zero coordinates excluded
zero_coords = df[(df['latitude'] == 0.0) | (df['longitude'] == 0.0)]
print(f"Zero-coordinate rows remaining: {len(zero_coords)}")

# ── Drop victim_age_valid duplicate ───────────────────────────────────────────
# Safety drop — created in some notebook runs, redundant with victim_age

if 'victim_age_valid' in df.columns:
    df.drop(columns=['victim_age_valid'], inplace=True)

# ── Final Info ─────────────────────────────────────────────────────────────────

print(df.info())

# ── Save Cleaned Dataset ───────────────────────────────────────────────────────

output_path = Path("data/processed") / "cleaned_crime_data.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)
print(f"Cleaned dataset saved to: {output_path}")