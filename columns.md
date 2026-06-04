# Dataset Columns — LA Crime Data (2020–2024)

Complete reference for all **25 columns** after transformation and type optimization.

---

## Temporal

| Column              | Type           | Description                                     |
| ------------------- | -------------- | ----------------------------------------------- |
| `reported_date`     | datetime64[ns] | Date the crime was reported to police.          |
| `date_occurrence`   | datetime64[ns] | Date the crime actually occurred.               |
| `hour_occurrence`   | Int8           | Hour of occurrence extracted from time field.   |
| `minute_occurrence` | Int8           | Minute of occurrence extracted from time field. |

---

## Geography

| Column                     | Type     | Description                                 |
| -------------------------- | -------- | ------------------------------------------- |
| `area_code`                | Int16    | Numeric code for LAPD divisions (1–21).     |
| `area_name`                | category | Name of policing division.                  |
| `reported_district_number` | int32    | Sub-division reporting district identifier. |
| `location`                 | category | Block-level anonymized address.             |
| `latitude`                 | float32  | Latitude coordinate.                        |
| `longitude`                | float32  | Longitude coordinate.                       |

---

## Crime Classification

| Column                   | Type   | Description                                                   |
| ------------------------ | ------ | ------------------------------------------------------------- |
| `crime_part`             | bool   | True = serious crime (Part 1), False = less serious (Part 2). |
| `crime_code`             | int64  | LAPD crime code identifier.                                   |
| `crime_code_description` | string | Human-readable crime description.                             |
| `Mocodes`                | object | Modus operandi codes describing how the crime was committed.  |

---

## Victim Information

| Column              | Type     | Description                                                 |
| ------------------- | -------- | ----------------------------------------------------------- |
| `victim_age`        | Int8     | Age of victim (nullable/cleaned).                           |
| `victim_sex`        | category | Sex of victim (F, M, X).                                    |
| `victim_descent`    | category | Ethnic background code.                                     |
| `victim_age_status` | category | Derived age status feature (e.g., valid, missing, invalid). |

---

## Premises

| Column                | Type   | Description                                              |
| --------------------- | ------ | -------------------------------------------------------- |
| `premise_code`        | int16  | Code identifying type of location.                       |
| `premise_description` | string | Description of premise type (e.g., STREET, PARKING LOT). |

---

## Weapon

| Column               | Type   | Description                                      |
| -------------------- | ------ | ------------------------------------------------ |
| `weapon_used_code`   | int16  | Weapon code (often 0 or placeholder if missing). |
| `weapon_description` | string | Description of weapon used.                      |

---

## Case Status

| Column               | Type     | Description                                |
| -------------------- | -------- | ------------------------------------------ |
| `status`             | category | Case status code (IC, AA, AO, JA, JO, CC). |
| `status_description` | category | Human-readable status description.         |

---

## Secondary Crime Codes

| Column         | Type  | Description                    |
| -------------- | ----- | ------------------------------ |
| `crime_code_1` | int16 | Primary additional crime code. |

---

## Source

https://catalog.data.gov/dataset/crime-data-from-2020-to-present
