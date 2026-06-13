# Crime Data Analysis — Los Angeles (2020–2024)

An end-to-end data science project analyzing over **1,004,894 crime records** across **28 features** from Los Angeles. The project covers the full lifecycle from raw data ingestion to predictive modeling using Random Forest.

---

## Project Workflow

| # | Phase | Status |
|---|-------|--------|
| 1 | Data Collection | Done |
| 2 | Business & Data Understanding | Done |
| 3 | Data Cleaning | Done |
| 4 | Oriented Feature Engineering | Done |
| 5 | EDA | Upcoming |
| 6 | Modeling (Random Forest) | Upcoming |
| 7 | Optimization & Deployment | Upcoming |

---

## Project Structure

```
crime-la-analysis/
├── data/
│   ├── raw/                                      # Raw CSV (excluded from version control)
│   └── processed/
│       ├── cleaned_crime_data.parquet            # Output of Phase 3
│       └── feature_engineered_crime_data.parquet # Output of Phase 4
├── notebooks/
│   ├── 2_data_cleaning.ipynb                     # Phase 3: Data Cleaning
│   └── 3_feature_engineering.ipynb               # Phase 4: Oriented Feature Engineering
├── src/
│   ├── data_cleaning/
│   │   ├── load_data.py                          # Load CSV, rename columns, drop DR_NO
│   │   ├── clean_basic.py                        # Dates, types, duplicates, crime columns
│   │   ├── clean_victims.py                      # Victim age, sex, descent
│   │   ├── clean_location.py                     # Premise, weapon, location, coordinates
│   │   └── export.py                             # Save cleaned data to parquet
│   └── feature_engineering/
│       ├── time_features.py                      # Temporal indicators and date components
│       ├── spatial_features.py                   # Geo bins, area crime rate, crime count
│       ├── victim_features.py                    # Age group, weapon flag
│       ├── crime_features.py                     # Crime category classification
│       └── premise_features.py                   # Premise grouping
├── config/
│   └── .env                                      # DATA_PATH and DATA_PATH_CLEANED variables
├── main.py                                       # Pipeline entry point
├── .gitignore
└── README.md
```

---

## 1. Data Collection

- **Source:** Los Angeles Open Data — City of LA
- **First Published:** February 10, 2020
- **Last Updated:** March 4, 2026
- **Raw data storage:** `data/raw/` (excluded from version control via `.gitignore`)

---

## 2. Data Understanding

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

## 3. Data Cleaning

**Pipeline:** `main.py` → `src/data_cleaning/load_data.py` → `src/data_cleaning/clean_basic.py` → `src/data_cleaning/clean_victims.py` → `src/data_cleaning/clean_location.py` → `src/data_cleaning/export.py`  
**Notebook:** `notebooks/2_data_cleaning.ipynb`  
**Output:** `data/processed/cleaned_crime_data.parquet`

### Column Renaming

All 28 raw LAPD column names were renamed to clean `snake_case` format (e.g. `Crm Cd Desc` → `crime_code_description`, `Vict Age` → `victim_age`).

### Columns Dropped

| Column | Reason |
|--------|--------|
| `DR_NO` | Administrative identifier, no analytical value |
| `time_occurrence` | Replaced by `hour_occurrence` and `minute_occurrence` |
| `cross_street` | 84.65% missing values |
| `crime_code_2` | 93.11% missing values |
| `crime_code_3` | 99.77% missing values |
| `crime_code_4` | 99.99% missing values |

Rows with coordinates outside Los Angeles bounds (lat 33–35, lon −119 to −117) were also removed to eliminate zero-coordinate and out-of-area records.

### Columns Added

| Column | Description |
|--------|-------------|
| `hour_occurrence` | Hour extracted from `time_occurrence` (0–23) |
| `minute_occurrence` | Minute extracted from `time_occurrence` (0–59) |
| `victim_age_status` | Flag indicating `'valid'` or `'N/A'` age records |

### Duplicate Removal

**2,965 duplicate rows** were identified and removed out of 1,004,894 total records.

### Date & Time Handling

- `reported_date` and `date_occurrence` converted from `object` to `datetime64`.
- Validated that no record has `reported_date < date_occurrence`.
- `time_occurrence` (HHMM integer) split into `hour_occurrence` and `minute_occurrence`, both as `Int8`.

### Missing & Invalid Value Handling

| Column | Issue | Resolution |
|--------|-------|------------|
| `victim_age` | 26.64% with age ≤ 0 | Replaced with `NaN`; flagged in `victim_age_status`. For victim crimes, imputed using per-crime-type median. Crimes where ≥90% of records have no age (e.g. vehicle theft) left as `NaN`. |
| `victim_sex` | `H`, `X`, `-`, and `NaN` | Unified as `'Unknown'` |
| `victim_descent` | `-` and `NaN` | Mapped to `'X'` (official LAPD Unknown code) |
| `premise_code` | 16 missing rows | Dropped |
| `premise_description` | Missing rows | Filled with `'Unknown'` |
| `weapon_used_code` | 67.44% missing | Filled with `-1` (no weapon sentinel) |
| `weapon_description` | 67.44% missing | Filled with `'Unknown | N/A'` |
| `crime_code_1` | 11 missing rows | Dropped |
| `status_description` | Abbreviated values | Expanded to full labels via mapping |

### dtype Optimization

All columns were cast to their most memory-efficient types:

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

---

## 4. Oriented Feature Engineering

**Pipeline:** `main.py` → `src/feature_engineering/time_features.py` → `src/feature_engineering/spatial_features.py` → `src/feature_engineering/victim_features.py` → `src/feature_engineering/crime_features.py` → `src/feature_engineering/premise_features.py`  
**Notebook:** `notebooks/3_feature_engineering.ipynb`  
**Input:** `data/processed/cleaned_crime_data.parquet`  
**Output:** `data/processed/feature_engineered_crime_data.parquet`

### Temporal Features

| Column | Description |
|--------|-------------|
| `reporting_delay_days` | Days between `date_occurrence` and `reported_date` |
| `year_occurrence` | Year extracted from `date_occurrence` |
| `month_occurrence` | Month extracted from `date_occurrence` (1–12) |
| `day_of_week_num` | Day of week as integer (0=Monday, 6=Sunday) |
| `quarter_occurrence` | Quarter extracted from `date_occurrence` (1–4) |
| `is_weekend_occurrence` | `1` if Saturday or Sunday, else `0` |
| `is_night_occurrence` | `1` if `hour_occurrence` < 6, else `0` |
| `time_period_occurrence` | Categorical period: `Late Night`, `Morning`, `Afternoon`, `Evening` |

### Spatial Features

| Column | Description |
|--------|-------------|
| `area_crime_share` | Proportion of total crimes occurring in each LAPD area |
| `lat_bin` | Latitude binned at 0.005° grid (~500m resolution) |
| `lon_bin` | Longitude binned at 0.005° grid (~500m resolution) |
| `crime_count` | Number of crimes in the same geo-bin cell |

### Victim Features

| Column | Description |
|--------|-------------|
| `age_group` | Victim age bucketed: `0-18`, `19-30`, `31-50`, `51+`, `Unknown` |
| `weapon_flag` | `1` if a known weapon was used, else `0` |

### Crime Features

| Column | Description |
|--------|-------------|
| `crime_category` | High-level crime type: `Violent Crime`, `Property Crime`, `Vehicle Crime`, `Sexual Crime`, `Financial Crime`, `Drug Crime`, `Public Order`, `Weapon Crime`, `Other` |

### Premise Features

| Column | Description |
|--------|-------------|
| `premise_group` | Grouped premise type: `Public Space`, `Residential`, `Commercial`, `Parking Area`, `Other` |

---

## Next Steps

- [ ] **EDA:** Geographic hotspotting, temporal trends (hourly, monthly, seasonal), and victim demographic distributions.
- [ ] **Modeling:** Train and validate a Random Forest classifier/regressor for the chosen target variable.
- [ ] **Deployment:** Production-ready model stored and documented on GitHub.

---

## Setup

```bash
# Clone the repository
git clone https://github.com/theyoussefmoussa/crimes_in_los_angeles.git
cd crimes_in_los_angeles

# Install dependencies
pip install -r requirements.txt

# Set the data paths in your .env file
echo "DATA_PATH=/your/path/to/raw/data" > config/.env
echo "DATA_PATH_CLEANED=/your/path/to/processed/data" >> config/.env

# Run the full pipeline
python3 main.py
```

---

## Author

**Youssef Moussa**
<br>
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/theyoussefmoussa)
[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/theyoussefmoussa)
[![X](https://img.shields.io/badge/X-000000?logo=x&logoColor=white)](https://x.com/theyosefmusa)
[![Portfolio](https://img.shields.io/badge/Portfolio-4CAF50?logo=google-chrome&logoColor=white)](https://theyoussefmoussa.github.io)