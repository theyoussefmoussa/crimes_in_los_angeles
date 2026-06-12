import pandas as pd
from pathlib import Path


def load_data(file_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    print(f"Loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

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
    df.drop(columns=['DR_NO'], inplace=True)

    print(f"Columns renamed. DR_NO dropped.")
    return df