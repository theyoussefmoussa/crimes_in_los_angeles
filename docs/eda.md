# Exploratory Data Analysis

**Notebook:** `notebooks/4_eda_univariate.ipynb`  
**Script:** `src/eda/eda_univariate.py`  
**Input:** `data/processed/feature_engineered_crime_data.parquet`  
**Saved Figures:** `outputs/eda_univariate/`

---

## Transformations Applied Before Analysis

| Column | Transformation | Reason |
|--------|---------------|--------|
| `reporting_delay_days` | `log1p` | Heavy right skew — same-day reporting dominates |
| `crime_count` | `log1p` | Wide range across geo-bins compresses variance |

---

## 1. Numerical Features

### Victim Age
- Most victims are young-to-middle adults, peaking at age 40 (~125K).
- 70% of victims fall between 16 and 48 — crime risk drops sharply after 56.
- Almost no victims under 16 or above 88.

### Hour of Occurrence
- Midday (12:00) is the most dangerous hour with ~68K crimes.
- Early morning (01:00–07:00) is the safest window.
- Crime builds steadily from 08:00 onward — this is a daytime phenomenon, not a nighttime one.

### Is Night Occurrence
- Most crimes happen during the day, consistent with the hour distribution above.

### Lat/Lon
- The densest crime zone sits in the lower-right cluster (34.1–34.3, -118.5 to -118.6).
- A separated western arm suggests a distinct geographic hotspot worth investigating.

### Reporting Delay
- Half of all crimes are reported same-day.
- Reports drop sharply after day 2 — delayed reporting beyond a week is rare.

### Area Crime Share
- Central leads with ~0.068 share — the clear outlier.
- 19 of 21 areas cluster tightly above 0.04, meaning crime is spread fairly evenly across the city.

---

## 2. Outlier Detection

IQR method applied across all numeric columns. Columns with detected outliers are printed at runtime.

---

## 3. Categorical Features

### Weekday vs Weekend
- 71.4% of crimes happen on weekdays — crime follows the working week.

### Weapon Flag
- 71.8% of crimes involve a known weapon.
- Only 28.2% have unknown or no weapon recorded.

### Year of Occurrence
- 2022 was the peak year (~225K crimes).
- 2023 was close behind with a slight drop.
- 2024 is the lowest (~125K) — likely incomplete data, not a real decline.

### Day of Week
- Friday sees the most crimes (~150K), Tuesday the least (~138K).
- The difference across days is small — no single day stands out dramatically.

### Month of Year
- January leads with ~90K crimes, March follows at ~86K.
- The remaining months cluster around 80K — no strong seasonal pattern.

### Crime Part
- 60% are Part 1 crimes — the dataset skews toward serious offenses.
- Non-Part 1 crimes still make up a substantial 40%.

### Crime Category
- Property Crime dominates at ~410K — 1.7× Violent Crime and 3.4× Vehicle Crime.
- Three tiers are visible: Property/Violent/Other on top, Vehicle in the middle, everything else near zero.
- The bottom five categories combined are smaller than Vehicle Crime alone.

### Victim Descent
- Hispanic/Latin/Mexican is the largest group (~295K), followed by Unknown (~248K) and White (~200K).
- Over half the descent categories have fewer than 5K victims each — a long sparse tail.
- Unknown at ~248K means 1 in 5 records has no descent info — a meaningful data quality gap.

### Victim Sex
- Males are 40.2%, females 35.8%, unknown 24%.
- The high unknown rate mirrors the descent field — reporting quality is inconsistent.

### Premise Group
- Residential (~352K) and Outdoor (~324K) account for most crimes, followed by Commercial.
- These three combined exceed 900K — the remaining eight groups total under 100K.
- Unknown premise is nearly zero — this field is well recorded.

### Court Status
- Investigation Continued dominates with ~800K cases — 80% of all records are still open.
- Juvenile Arrest and Juvenile Other are completely absent — likely filtered out or stored separately, worth investigating before modeling.
- Only Adult Arrest (~85K) and Adult Other (~105K) represent resolved cases — less than 20% of the dataset.
- A binary Open vs. Closed target is more practical than multiclass given this imbalance.

---

## Saved Figures

| File | Description |
|------|-------------|
| `weekday_vs_weekend.png` | Pie chart — weekday vs weekend crime split |
| `victim_sex.png` | Pie chart — victim sex distribution |
| `crime_part.png` | Pie chart — Part 1 vs Non-Part 1 crimes |
| `weapon_flag.png` | Pie chart — known vs unknown weapon |
| `crimes_per_month.png` | Bar chart — crime count by month |
| `crimes_by_day.png` | Bar chart — crime count by day of week |
| `victim_descent.png` | Bar chart — victim descent distribution |
| `court_status.png` | Bar chart — court status distribution |