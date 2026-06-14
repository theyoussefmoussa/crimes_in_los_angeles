# Data Cleaning

**Pipeline:** `main.py` → `src/data_cleaning/load_data.py` → `src/data_cleaning/clean_basic.py` → `src/data_cleaning/clean_victims.py` → `src/data_cleaning/clean_location.py` → `src/data_cleaning/export.py`  
**Notebook:** `notebooks/2_data_cleaning.ipynb`  
**Output:** `data/processed/cleaned_crime_data.parquet`

---

## Data Understanding

The raw dataset contains 28 features detailing reported criminal activity across Los Angeles.

| Column | Description |
|--------|-------------|
| `DR_NO` | Unique LAPD record identifier (dropped in cleaning) |
| `Date Rptd` | Date the crime was reported |
| `DATE OCC` | Date the crime occurred |
| `TIME OCC` | Time of occurrence in military format (HHMM) |
| `AREA / AREA NAME` | LAPD area code and name (21 geographic divisions) |
| `Rpt Dist No` | Reporting district number |
| `Part 1-2` | Crime severity: Part 1 = serious, Part 2 = less serious |
| `Crm Cd / Crm Cd Desc` | Crime type code and description |
| `Mocodes` | Space-separated Modus Operandi codes |
| `Vict Age / Sex / Descent` | Victim demographic profile |
| `Premis Cd / Premis Desc` | Premise code and location type |
| `Weapon Used Cd / Weapon Desc` | Weapon code and description (if applicable) |
| `Status / Status Desc` | Investigation status code and full description |
| `Crm Cd 1–4` | Primary and additional crime codes |
| `LOCATION / Cross Street` | Street address and nearby cross street |
| `LAT / LON` | Geographic coordinates |

---

## Column Renaming

All 28 raw LAPD column names were renamed to clean `snake_case` format (e.g. `Crm Cd Desc` → `crime_code_description`, `Vict Age` → `victim_age`).

---

## Columns Dropped

| Column | Reason |
|--------|--------|
| `DR_NO` | Administrative identifier, no analytical value |
| `time_occurrence` | Replaced by `hour_occurrence` and `minute_occurrence` |
| `cross_street` | 84.65% missing values |
| `crime_code_2` | 93.11% missing values |
| `crime_code_3` | 99.77% missing values |
| `crime_code_4` | 99.99% missing values |

Rows with coordinates outside Los Angeles bounds (lat 33–35, lon −119 to −117) were also removed to eliminate zero-coordinate and out-of-area records.

---

## Columns Added

| Column | Description |
|--------|-------------|
| `hour_occurrence` | Hour extracted from `time_occurrence` (0–23) |
| `minute_occurrence` | Minute extracted from `time_occurrence` (0–59) |
| `victim_age_status` | Flag indicating `'valid'` or `'N/A'` age records |

---

## Duplicate Removal

**2,965 duplicate rows** were identified and removed out of 1,004,894 total records.

---

## Date & Time Handling

- `reported_date` and `date_occurrence` converted from `object` to `datetime64`.
- Validated that no record has `reported_date < date_occurrence`.
- `time_occurrence` (HHMM integer) split into `hour_occurrence` and `minute_occurrence`, both as `Int8`.

---

## Missing & Invalid Value Handling

| Column | Issue | Resolution |
|--------|-------|------------|
| `victim_age` | 26.64% with age ≤ 0 | Replaced with `NaN`; flagged in `victim_age_status`. For victim crimes, imputed using per-crime-type median. Crimes where ≥90% of records have no age (e.g. vehicle theft) left as `NaN`. |
| `victim_sex` | `H`, `X`, `-`, and `NaN` | Unified as `'Unknown'` |
| `victim_descent` | `-` and `NaN` | Mapped to `'X'` (official LAPD Unknown code) |
| `premise_code` | 16 missing rows | Dropped |
| `premise_description` | Missing rows | Filled with `'Unknown'` |
| `weapon_used_code` | 67.44% missing | Filled with `-1` (no weapon sentinel) |
| `weapon_description` | 67.44% missing | Filled with `'Unknown \| N/A'` |
| `crime_code_1` | 11 missing rows | Dropped |
| `status_description` | Abbreviated values | Expanded to full labels via mapping |

---

## dtype Optimization

| Column | dtype |
|--------|-------|
| `area_code` | `Int16` |
| `reported_district_number` | `int32` |
| `crime_code_1` | `int16` |
| `premise_code` | `int16` |
| `weapon_used_code` | `int16` |
| `hour_occurrence`, `minute_occurrence` | `Int8` |
| `victim_age` | `Int8` (nullable) |
| `latitude`, `longitude` | `float32` |
| `area_name`, `victim_sex`, `victim_descent`, `status`, `status_description`, `victim_age_status` | `category` |
| `crime_code_description`, `premise_description`, `weapon_description` | `string[pyarrow]` |
| `location` | `category` |
| `crime_part` | `bool` |
| `reported_date`, `date_occurrence` | `datetime64` |