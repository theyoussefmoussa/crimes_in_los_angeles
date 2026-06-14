# Feature Engineering

**Pipeline:** `main.py` → `src/feature_engineering/time_features.py` → `src/feature_engineering/spatial_features.py` → `src/feature_engineering/victim_features.py` → `src/feature_engineering/crime_features.py` → `src/feature_engineering/premise_features.py`  
**Notebook:** `notebooks/3_feature_engineering.ipynb`  
**Input:** `data/processed/cleaned_crime_data.parquet`  
**Output:** `data/processed/feature_engineered_crime_data.parquet`

---

## Temporal Features

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

---

## Spatial Features

| Column | Description |
|--------|-------------|
| `area_crime_share` | Proportion of total crimes occurring in each LAPD area |
| `lat_bin` | Latitude binned at 0.005° grid (~500m resolution) |
| `lon_bin` | Longitude binned at 0.005° grid (~500m resolution) |
| `crime_count` | Number of crimes in the same geo-bin cell |

---

## Victim Features

| Column | Description |
|--------|-------------|
| `age_group` | Victim age bucketed: `0-18`, `19-30`, `31-50`, `51+`, `Unknown` |
| `weapon_flag` | `1` if a known weapon was used, else `0` |

---

## Crime Features

| Column | Description |
|--------|-------------|
| `crime_category` | High-level crime type: `Violent Crime`, `Property Crime`, `Vehicle Crime`, `Sexual Crime`, `Financial Crime`, `Drug Crime`, `Public Order`, `Weapon Crime`, `Other` |
| `crime_frequency_tier` | Frequency tier: `High_Frequency`, `Mid_Frequency`, `Low_Frequency` |

---

## Premise Features

| Column | Description |
|--------|-------------|
| `premise_group` | Grouped premise type: `Residential`, `Commercial`, `Outdoor`, `Transit`, `Education`, `Healthcare`, `Government`, `Entertainment`, `Digital`, `Unknown`, `Other` |

### Premise Grouping Logic

Premise descriptions were mapped to 11 groups using a lookup dictionary built at module level for O(1) per-row lookup. MTA entries (50+ variations) are handled via `str.startswith('MTA')` to avoid listing each individually.

| Group | Examples |
|-------|---------|
| Residential | Single family dwelling, apartment, hotel, motel, dorm |
| Commercial | Stores, restaurants, banks, offices, gas stations |
| Outdoor | Street, sidewalk, park, beach, parking lot, freeway |
| Transit | MTA lines, bus stops, train stations, taxi, Amtrak |
| Education | Schools, colleges, libraries, day care |
| Healthcare | Hospital, clinic, nursing home, pharmacy |
| Government | Police facility, fire station, jail, government buildings |
| Entertainment | Theatre, sports arena, nightclub, museum, places of worship |
| Digital | Cyberspace, website |
| Unknown | Explicitly unknown entries |
| Other | Anything unclassifiable |