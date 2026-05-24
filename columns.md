# Dataset Columns — LA Crime Data (2020–2024)

Complete reference for all **28 columns** in the dataset.

---

## Identification

| Column | Type | Description |
|--------|------|-------------|
| `DR_NO` | int64 | Unique identifier for each crime report (Division of Records Number). |

---

## Temporal

| Column | Type | Description |
|--------|------|-------------|
| `Date Rptd` | object | The date the crime was **reported** to the police. May differ from the actual occurrence date. |
| `DATE OCC` | object | The date the crime **actually occurred**. Primary date column for time-series analysis. |
| `TIME OCC` | int64 | Time of occurrence in **military format** (e.g., 845 = 08:45, 1845 = 18:45). |

---

## Geography

| Column | Type | Description |
|--------|------|-------------|
| `AREA` | int64 | Numeric code (1–21) for one of LA's 21 policing divisions. |
| `AREA NAME` | object | Human-readable name of the policing division (e.g., Hollywood, Wilshire, Van Nuys). |
| `Rpt Dist No` | int64 | Sub-division of each area into smaller **reporting districts** for granular police mapping. |
| `LOCATION` | object | Block-level street address where the crime occurred. Anonymized to the nearest hundred block for privacy. |
| `Cross Street` | object | Nearest cross street for intersection-based crimes. Only ~15% of records have this populated. |
| `LAT` | float64 | Latitude coordinate of the crime location. |
| `LON` | float64 | Longitude coordinate of the crime location. |

---

## Crime Classification

| Column | Type | Description |
|--------|------|-------------|
| `Part 1-2` | int64 | Severity classification. **1** = serious crimes (Homicide, Rape, Robbery, Burglary). **2** = less serious (Simple Assault, Fraud, Drug Offense, Vandalism). |
| `Crm Cd` | int64 | LAPD numeric crime code. Each code maps 1-to-1 with `Crm Cd Desc`. |
| `Crm Cd Desc` | object | Human-readable crime name (e.g., `VEHICLE - STOLEN`, `BURGLARY`, `THEFT OF IDENTITY`). |
| `Mocodes` | object | Space-separated numeric codes describing **how** the crime was committed (Modus Operandi). A single crime can have multiple codes. Requires a separate lookup table for interpretation. |

---

## Victim Information

| Column | Type | Description |
|--------|------|-------------|
| `Vict Age` | int64 | Age of the victim. **Note:** ~25% of values are `0` (used as placeholder for unknown or no direct victim); 137 records have **negative** age values — both to be handled in cleaning. |
| `Vict Sex` | object | Sex of the victim. Values: `F` (Female), `M` (Male), `X` (Unknown / Non-binary). |
| `Vict Descent` | object | Ethnic background of the victim using single-letter codes. See table below. |

**Victim Descent Codes:**

| Code | Meaning |
|------|---------|
| A | Other Asian |
| B | Black |
| C | Chinese |
| D | Cambodian |
| F | Filipino |
| G | Guamanian |
| H | Hispanic / Latin / Mexican |
| I | American Indian / Alaskan Native |
| J | Japanese |
| K | Korean |
| L | Laotian |
| O | Other |
| P | Pacific Islander |
| S | Samoan |
| U | Hawaiian |
| V | Vietnamese |
| W | White |
| X | Unknown |
| Z | Asian Indian |

---

## Premises

| Column | Type | Description |
|--------|------|-------------|
| `Premis Cd` | float64 | Numeric code identifying the **type of location** where the crime occurred (e.g., 501 = Single Family Dwelling, 101 = Street). |
| `Premis Desc` | object | Human-readable description of the premise type (e.g., `STREET`, `PARKING LOT`, `SINGLE FAMILY DWELLING`). |

---

## Weapon

| Column | Type | Description |
|--------|------|-------------|
| `Weapon Used Cd` | float64 | Numeric code for the weapon used in the crime. **~67% null** — expected for non-violent crimes (theft, fraud, etc.). |
| `Weapon Desc` | object | Human-readable weapon description (e.g., `HAND GUN`, `KNIFE WITH BLADE 6INCHES OR LESS`). Same null rate as `Weapon Used Cd`. |

---

## Case Status

| Column | Type | Description |
|--------|------|-------------|
| `Status` | object | Short code for the current case status. Values: `IC`, `AA`, `AO`, `JA`, `JO`, `CC`. |
| `Status Desc` | object | Human-readable status description. See table below. |

**Status Codes:**

| Code | Description |
|------|-------------|
| IC | Invest Cont — Investigation Continued |
| AA | Adult Arrest |
| AO | Adult Other — adult involved but not arrested (witness, suspect, citation, referral) |
| JA | Juvenile Arrest |
| JO | Juvenile Other |
| CC | Case Closed |

---

## Secondary Crime Codes

A single incident can involve multiple charges. `Crm Cd 1` is the primary charge; codes 2–4 are supplementary and increasingly sparse.

| Column | Type | Non-Null Count | Description |
|--------|------|---------------|-------------|
| `Crm Cd 1` | float64 | 1,004,883 | Primary charge code. Nearly complete. |
| `Crm Cd 2` | float64 | 69,154 | Secondary charge code. Present when a second offense was recorded. |
| `Crm Cd 3` | float64 | 2,314 | Tertiary charge code. Very sparse. |
| `Crm Cd 4` | float64 | 64 | Quaternary charge code. Near-empty — rarely used. |

---

*Source: [data.gov — Crime Data from 2020 to Present](http://catalog.data.gov/dataset/crime-data-from-2020-to-present)*