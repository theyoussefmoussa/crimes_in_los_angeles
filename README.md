# Crime Data Analysis — Los Angeles (2020–2024)

An end-to-end data science project analyzing over **1,004,894 crime records** across **28 features** from Los Angeles. The project covers the full lifecycle from raw data ingestion to predictive modeling using Random Forest.

---

## Project Workflow

| # | Phase | Status |
|---|-------|--------|
| 1 | Data Collection | Done |
| 2 | Business & Data Understanding | Done |
| 3 | Data Cleaning & Preprocessing | Done |
| 4 | Exploratory Data Analysis (EDA) | Upcoming |
| 5 | Feature Engineering | Upcoming |
| 6 | Modeling (Random Forest) | Upcoming |
| 7 | Optimization & Deployment | Upcoming |

---

## Project Structure

```
crime-la-analysis/
├── data/
│   ├── raw/                        # Raw CSV (excluded from version control)
│   └── processed/                  # Cleaned parquet output
├── notebooks/
│   └── crime_data_cleaning.ipynb   # Phase 3: Data Cleaning
├── src/
│   └── data/
│       └── data_clean.py           # Production cleaning script
├── config/
│   └── .env                        # DATA_PATH environment variable
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

## 3. Data Cleaning & Preprocessing

**Script:** `src/data/data_clean.py`  
**Notebook:** `notebooks/crime_data_cleaning.ipynb`  
**Output:** `data/processed/crime_data_cleaned.parquet`

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
- `time_occurrence` (HHMM integer) split into `hour_occurrence` and `minute_occurrence`, both as `int8`.

### Missing & Invalid Value Handling

| Column | Issue | Resolution |
|--------|-------|------------|
| `victim_age` | 26.8% with age ≤ 0 | Replaced with `NaN`; flagged in `victim_age_status`. For victim crimes, imputed using per-crime-type median. Crimes where ≥90% of records have no age (e.g. vehicle theft) left as `NaN`. |
| `victim_sex` | `H`, `X`, `-`, and `NaN` | Unified as `'Unknown'` |
| `victim_descent` | `-` and `NaN` (144,643 rows) | Mapped to `'X'` (official LAPD Unknown code) |
| `premise_code` | 16 missing rows | Dropped |
| `premise_description` | ~500 missing rows | Filled with `'Unknown'` |
| `weapon_used_code` | 67.44% missing | Filled with `-1` (no weapon sentinel) |
| `weapon_description` | 67.44% missing | Filled with `'Unknown | N/A'` |
| `crime_code_1` | 11 missing rows | Dropped |
| `status_description` | Abbreviated values | Expanded to full labels via mapping |

### dtype Optimization

All columns were cast to their most memory-efficient types:

| Column | dtype |
|--------|-------|
| `area_code` | `int8` |
| `reported_district_number` | `int32` |
| `crime_code_1` | `int16` |
| `premise_code` | `int16` |
| `weapon_used_code` | `int16` |
| `hour_occurrence`, `minute_occurrence` | `int8` |
| `victim_age` | `Int8` (nullable) |
| `latitude`, `longitude` | `float32` |
| `area_name`, `victim_sex`, `victim_descent`, `status`, `status_description`, `victim_age_status` | `category` |
| `crime_code_description`, `premise_description`, `weapon_description` | `string[pyarrow]` |
| `location` | `category` |
| `crime_part` | `bool` |
| `reported_date`, `date_occurrence` | `datetime64` |

---

## Next Steps

- [ ] **EDA:** Geographic hotspotting, temporal trends (hourly, monthly, seasonal), and victim demographic distributions.
- [ ] **Feature Engineering:** Domain-specific indicators (e.g. weekend flags, shift periods), target variable selection.
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

# Set the data path in your .env file
echo "DATA_PATH=/your/path/to/data" > config/.env

# Run the cleaning pipeline
python src/data/data_clean.py
```

---

## Author

**Youssef Moussa**
- [LinkedIn](https://linkedin.com/in/theyoussefmoussa)
- [GitHub](https://github.com/theyoussefmoussa)
- [Twitter](https://x.com/theyosefmusa)
- [Portfolio](https://theyoussefmoussa.github.io)