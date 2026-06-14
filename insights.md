# EDA Insights — LA Crimes (2020–2024)

Key findings from the univariate analysis of 1,004,894 crime records.

---

## Time

- Midday (12:00) is the peak crime hour — crime is a daytime phenomenon, not nocturnal.
- Early morning (01:00–07:00) is the safest window across the entire day.
- Friday is the highest-crime day (~150K), Tuesday the lowest (~138K) — but the gap is small.
- January leads monthly with ~90K crimes; the remaining months cluster around 80K with no strong seasonal pattern.
- 2022 was the peak year (~225K); 2024 appears lowest (~125K) but is likely incomplete data.
- 71.4% of crimes occur on weekdays — crime follows the working week.

---

## Location

- Crime is heavily concentrated in three premise types: Residential (~352K), Outdoor (~324K), and Commercial (~235K) — together over 900K incidents.
- Central has the highest area crime share (~0.068) — a clear outlier among the 21 LAPD divisions.
- 19 of 21 areas sit above 0.04 share, meaning crime is fairly distributed across the city outside of Central.
- The densest geographic cluster sits at (34.1–34.3, -118.5 to -118.6); a separated western arm suggests a secondary hotspot worth investigating.

---

## Victim

- Most victims are young-to-middle adults — 70% fall between ages 16 and 48, peaking at 40.
- Crime risk drops sharply after 56; almost no victims under 16 or above 88.
- Males make up 40.2% of victims, females 35.8%, with 24% unknown — reporting quality is inconsistent.
- Hispanic/Latin/Mexican is the largest victim descent group (~295K), followed by Unknown (~248K) and White (~200K).
- Unknown descent at ~248K means 1 in 5 records lacks descent info — a meaningful data quality gap.

---

## Crime Type

- Property Crime dominates at ~410K — 1.7× Violent Crime and 3.4× Vehicle Crime.
- Three frequency tiers exist: Property/Violent/Other on top, Vehicle in the middle, everything else near zero.
- 60% of crimes are Part 1 (serious offenses) — the dataset skews toward high-severity cases.
- 71.8% of crimes involve a known weapon; 28.2% have unknown or no weapon recorded.
- Investigation Continued accounts for ~80% of court statuses — most cases remain open.
- Juvenile Arrest and Juvenile Other are completely absent from court status — a data quality issue worth investigating.
- Half of all crimes are reported same-day; reports drop sharply after day 2.