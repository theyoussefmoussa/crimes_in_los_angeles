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
| 5 | EDA | In Progress |
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
├── docs/
│   ├── data_cleaning.md                          # Cleaning decisions and pipeline details
│   ├── feature_engineering.md                   # Feature definitions and engineering logic
│   └── eda.md                                   # EDA findings and observations
├── notebooks/
│   ├── 2_data_cleaning.ipynb                     # Phase 3: Data Cleaning
│   ├── 3_feature_engineering.ipynb               # Phase 4: Oriented Feature Engineering
│   └── 4_eda_univariate.ipynb                   # Phase 5: Univariate Analysis
├── outputs/
│   └── eda_univariate/                           # Saved EDA figures (PNG)
├── src/
│   ├── data_cleaning/
│   │   ├── load_data.py                          # Load CSV, rename columns, drop DR_NO
│   │   ├── clean_basic.py                        # Dates, types, duplicates, crime columns
│   │   ├── clean_victims.py                      # Victim age, sex, descent
│   │   ├── clean_location.py                     # Premise, weapon, location, coordinates
│   │   └── export.py                             # Save cleaned data to parquet
│   ├── feature_engineering/
│   │   ├── time_features.py                      # Temporal indicators and date components
│   │   ├── spatial_features.py                   # Geo bins, area crime rate, crime count
│   │   ├── victim_features.py                    # Age group, weapon flag
│   │   ├── crime_features.py                     # Crime category classification
│   │   └── premise_features.py                   # Premise grouping
│   └── eda/
│       └── eda_univariate.py                     # Univariate analysis script
├── config/
│   └── .env                                      # DATA_PATH and DATA_PATH_CLEANED variables
├── main.py                                       # Pipeline entry point
├── .gitignore
└── README.md
```

---

## Documentation

- [Data Cleaning](docs/data_cleaning.md)
- [Feature Engineering](docs/feature_engineering.md)
- [EDA](docs/eda.md)

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

# Run pipeline + EDA
python3 main.py --eda
```

---

## Author

**Youssef Moussa**
<br>
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/theyoussefmoussa)
[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/theyoussefmoussa)
[![X](https://img.shields.io/badge/X-000000?logo=x&logoColor=white)](https://x.com/theyosefmusa)
[![Portfolio](https://img.shields.io/badge/Portfolio-4CAF50?logo=google-chrome&logoColor=white)](https://theyoussefmoussa.github.io)