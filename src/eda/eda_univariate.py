import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend — no window opened
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PATHS & IMPORTS
# ─────────────────────────────────────────────

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from utils.visualization_utils import *

load_dotenv()

DATA_PATH_CLEANED = os.getenv("DATA_PATH_CLEANED")
file_path = Path(DATA_PATH_CLEANED) / "feature_engineered_crime_data.parquet"
df = pd.read_parquet(file_path)

set_plot_style()

FIGURES_DIR = project_root / "outputs/eda_univariate"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# PREPROCESSING (log transforms)
# ─────────────────────────────────────────────

df['reporting_delay_days'] = np.log1p(df['reporting_delay_days'])
df['crime_count']          = np.log1p(df['crime_count'])

# ─────────────────────────────────────────────
# 1. NUMERICAL FEATURES
# ─────────────────────────────────────────────

# Victim Age
counts = df["victim_age"].value_counts().sort_index()
colors = get_highlight_colors(counts.values)
plt.bar(counts.index, counts.values, color=colors)
setup_axes("Age Distribution", "Age", "Frequency")
plt.tight_layout()
save_figure("victim_age.png", path=FIGURES_DIR)
plt.close()
print("  [saved] victim_age.png")

# Hour of Occurrence
counts = df['hour_occurrence'].value_counts().sort_index()
colors = get_highlight_colors(counts.values)
plt.bar(counts.index, counts.values, color=colors)
setup_axes("Crime Occurrences by Hour", "Hour of Occurrence", "Count")
plt.xticks(range(0, 24))
plt.tight_layout()
save_figure("hour_occurrence.png", path=FIGURES_DIR)
plt.close()
print("  [saved] hour_occurrence.png")

# Is Night Occurrence
counts = df['is_night_occurrence'].value_counts()
colors = [PALETTE[3], PALETTE[0]]
plt.pie(counts, labels=['Day', 'Night'], autopct='%1.1f%%', colors=colors)
setup_axes("Night vs Day Crimes Occurrence")
plt.legend()
plt.tight_layout()
save_figure("night_vs_day.png", path=FIGURES_DIR)
plt.close()
print("  [saved] night_vs_day.png")

# Lat/Lon Scatter
plt.scatter(df['lat_bin'], df['lon_bin'])
plt.title('Crime Incidents by Location')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
save_figure("crime_locations.png", path=FIGURES_DIR)
plt.close()
print("  [saved] crime_locations.png")

# Reporting Delay
counts = df['reporting_delay_days'].value_counts().sort_index()
colors = get_highlight_colors(counts.values)
plt.bar(counts.index, counts.values, color=colors)
setup_axes("Reporting Delay Distribution", "Reporting Delay (Days)", "Count")
plt.xlim(0, 5)
plt.xticks(range(0, 5))
plt.tight_layout()
save_figure("reporting_delay.png", path=FIGURES_DIR)
plt.close()
print("  [saved] reporting_delay.png")

# Area Crime Share
area_stats = df.groupby('area_name')['area_crime_share'].mean()
colors = get_highlight_colors(area_stats.values)
plt.bar(area_stats.index, area_stats.values, color=colors)
plt.xticks(rotation=45, ha="right")
setup_axes("Crime Share by Area", "Area", "Crime Share")
plt.tight_layout()
save_figure("area_crime_share.png", path=FIGURES_DIR)
plt.close()
print("  [saved] area_crime_share.png")

# Crimes per Year
year_counts = df['year_occurrence'].value_counts().sort_index()
colors = get_highlight_colors(year_counts.values, highlight=WARNING_COLOR)
plt.bar(year_counts.index, year_counts.values, color=colors)
plt.yticks(range(0, 300000, 25000))
setup_axes("Crimes per Year", "Year", "Count")
plt.tight_layout()
save_figure("crimes_per_year.png", path=FIGURES_DIR)
plt.close()
print("  [saved] crimes_per_year.png")

# ─────────────────────────────────────────────
# 2. OUTLIER DETECTION
# ─────────────────────────────────────────────

print("\n--- Outlier Detection ---")
numeric_cols = df.select_dtypes(include='number').columns
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    n_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    if n_outliers > 0:
        print(f"  {col}: {n_outliers:,} outliers")

# ─────────────────────────────────────────────
# 3. CATEGORICAL FEATURES
# ─────────────────────────────────────────────

# Weekday vs Weekend
counts = df['is_weekend_occurrence'].value_counts()
plt.pie(counts, labels=counts.index.map({0: 'Weekday', 1: 'Weekend'}), autopct='%1.1f%%')
plt.title("Weekday vs Weekend Occurrence")
plt.legend()
plt.tight_layout()
save_figure("weekday_vs_weekend.png", path=FIGURES_DIR)
plt.close()
print("  [saved] weekday_vs_weekend.png")

# Victim Sex
sex_counts = df['victim_sex'].value_counts()
plt.pie(sex_counts, labels=sex_counts.index.map({'M': 'Male', 'F': 'Female', 'Unknown': 'Unknown'}), autopct='%1.1f%%')
plt.title("Victim Sex Percentage")
plt.legend()
plt.tight_layout()
save_figure("victim_sex.png", path=FIGURES_DIR)
plt.close()
print("  [saved] victim_sex.png")

# Crime Part
crime_part_counts = df['crime_part'].value_counts()
labels = crime_part_counts.index.map({1: "Part 1 Crime", 0: "Not Part 1 Crime"})
plt.figure(figsize=(6, 6))
plt.pie(crime_part_counts.values, labels=labels, autopct='%1.1f%%', startangle=90,
        colors=[PALETTE[0], PALETTE[1]], textprops={'fontsize': 10})
plt.title("Part 1 vs Non-Part 1 Crimes")
plt.legend(labels, loc="best")
plt.tight_layout()
save_figure("crime_part.png", path=FIGURES_DIR)
plt.close()
print("  [saved] crime_part.png")

# Weapon Flag
counts = df['weapon_flag'].value_counts()
plt.pie(counts, autopct='%1.1f%%',
        labels=counts.index.map({0: "Unknown Weapon", 1: "Known Weapon"}),
        colors=[PALETTE[0], PALETTE[1]])
plt.title("Is A Weapon Used In The Crime")
plt.legend()
plt.tight_layout()
save_figure("weapon_flag.png", path=FIGURES_DIR)
plt.close()
print("  [saved] weapon_flag.png")

# Month of Year
months_counts = df['month_occurrence'].value_counts()
colors = get_highlight_colors(months_counts.values)
months_map = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun",
              7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
plt.bar(months_counts.index, months_counts.values, color=colors)
setup_axes("Crimes Per Month", "Month", "Frequency")
plt.xticks(ticks=months_counts.index, labels=[months_map.get(i, str(i)) for i in months_counts.index], rotation=45, ha="right")
plt.yticks(range(0, 100000, 10000))
plt.tight_layout()
save_figure("crimes_per_month.png", path=FIGURES_DIR)
plt.close()
print("  [saved] crimes_per_month.png")

# Day of Week
counts = df['day_of_week_num'].value_counts().sort_index()
colors = get_highlight_colors(counts.values)
day_of_week_map = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
plt.bar(counts.index, counts.values, color=colors)
plt.xticks(ticks=counts.index, labels=[day_of_week_map[i] for i in counts.index], rotation=45, ha="right")
setup_axes("Crimes by Day of Week", "Day", "Count")
plt.tight_layout()
save_figure("crimes_by_day_of_week.png", path=FIGURES_DIR)
plt.close()
print("  [saved] crimes_by_day_of_week.png")

# Victim Descent
victim_descent_counts = df['victim_descent'].value_counts().sort_index()
color = get_highlight_colors(victim_descent_counts.values)
victim_descent_map = {
    "A": "Other Asian", "B": "Black", "C": "Chinese", "D": "Cambodian",
    "F": "Filipino", "G": "Guamanian", "H": "Hispanic/Latin/Mexican",
    "I": "American Indian/Alaska Native", "J": "Japanese", "K": "Korean",
    "L": "Laotian", "O": "Other", "P": "Pacific Islander", "S": "Samoan",
    "U": "Hawaiian", "V": "Vietnamese", "W": "White", "X": "Unknown", "Z": "Asian Indian"
}
sns.barplot(x=victim_descent_counts.index, y=victim_descent_counts.values, palette=color)
setup_axes("Victim Descent Counts", "Victim Descent", "Frequency")
plt.xticks(ticks=range(len(victim_descent_counts)),
           labels=[victim_descent_map[i] for i in victim_descent_counts.index],
           rotation=90, ha="right")
plt.tight_layout()
save_figure("victim_descent.png", path=FIGURES_DIR)
plt.close()
print("  [saved] victim_descent.png")

# Court Status
court_status_map = {
    "IC": "Investigation Continued", "AO": "Adult Other", "AA": "Adult Arrest",
    "JA": "Juvenile Arrest", "JO": "Juvenile Other", "CC": "Complaint Closed"
}
court_status_counts = df['status'].value_counts().sort_index()
sns.barplot(x=court_status_counts.index, y=court_status_counts.values,
            palette=get_highlight_colors(court_status_counts.values))
setup_axes("Court Status", "Status", "Frequency")
plt.xticks(ticks=range(len(court_status_counts)),
           labels=court_status_counts.index.map(court_status_map),
           rotation=45, ha='right')
plt.tight_layout()
save_figure("court_status.png", path=FIGURES_DIR)
plt.close()
print("  [saved] court_status.png")

# Crime Category
crime_counts = df['crime_category'].value_counts()
colors = get_highlight_colors(crime_counts.values)
sns.barplot(x=crime_counts.index, y=crime_counts.values, palette=colors)
setup_axes("Crime Category Occurrence Counts", "Crime Category", "Frequency of Occurrence")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_figure("crime_category.png", path=FIGURES_DIR)
plt.close()
print("  [saved] crime_category.png")

# Premise Group
premise_counts = df['premise_group'].value_counts().sort_index()
color = get_highlight_colors(premise_counts.values)
sns.barplot(x=premise_counts.index, y=premise_counts.values, palette=color)
plt.xticks(rotation=45, ha='right')
setup_axes("Premise Group Frequencies", "Premise Group", "Frequency")
plt.tight_layout()
save_figure("premise_group.png", path=FIGURES_DIR)
plt.close()
print("  [saved] premise_group.png")

print("\nDone. Saved figures →", FIGURES_DIR)