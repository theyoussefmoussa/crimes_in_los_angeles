# The Analysis of Crimes in Los Angeles from 2020:2024
The Analysis of Crimes in LA from 2020:2024 with more than 1004894 crimes in total, 
and have 28 featuers to work on.
The Project workflow: Data Collection, Business Understanding, Data Cleaning, EDA, Modeling, Optimization, and Deployment.
------
1. Data Collection: 
[Source of Data](http://catalog.data.gov/dataset/crime-data-from-2020-to-present?from_hint=eyJzb3J0IjoicG9wdWxhcml0eSJ9)
Dataset first published was on 10/Feb/2020 and last update was on 4/Mar/2026
Downloaded as csv file in data/raw in project root.

2. Data Understanding: 
The 28 Features:
1. DR_N0: The Unique identifier of each crime.
2. Date_Rptd: The Reported date of the crime.
3. DATE OCC: the occurance date of the crime (When The Crime Actually happened)
4. AREA: All Crimes are in LA, so we have 21 areas of Los Angeles.
5. AREA NAME: The name of each area of 21 areas in LA.
6. Rpt Dist No: Each Area is divided into small reporting districts for easy mapping to the police.
7. Part 1-2: Classification of how serious the crime is, 1: more serious like: Rape, Robbery, Homicide, while 2: less serious like: Simple Assault, Drug Offense, Fraud, Vandalism.
8. Crm Cd: it referes to LA Crime Code for each crime, for example 510: Vehicle Theft.
9. Crm Cd Desc: The name of the Charge, for example Vehicle Theft : 510.
10. Mocodes: represent how the crimes was done. 
11. Vict Age: The Age of the victim (has many missing values)
12. Vict Sex: The sex of the victim, F: Female, M: Male, X: Non Binary.
13. Vict Descent: the code of the victim, for example B: Black, C: Chinese.
14. Premis Cd: refers to a numeric code that identifies the type of location where the crime occurred, for example 501: 
15. Premis Desc: Human readable description for the place type, for example, 101:Street.
16. Weapon Used Cd: the code of weapon used in the crime.
17. Weapon Desc: the weapon description that used.
18. Status: The Status code ['IC' 'AO' 'AA' 'JA' 'JO' 'CC' nan].
19. Status Desc: the description for the charge, for example: Adult Other: An adult involved in a category other than arrest (e.g. witness, suspect, citation, referral).
20. Crm Cd 1: the code of the first crime, for example 187: Murder.
21. Crm Cd 2: the code of the second crime, for example 211: Robbery.
22. Crm Cd 3: the code of the third crime, for example 459: Burglary.
23. Crm Cd 4: the code of the fourth crime, for example 487: Petty Theft.
24. Location: Location where the crime occurred.
25. Cross Street: The street where the crime occurred.
26. LON: The Longitiude of the location.
27. LAT: The Latitude of the location.

Resources to Understand Data: 
[Crimes by Code Section in LA](https://www.losangelescriminallawyer.pro/crimes-by-code-section.html)


## Initial Observations

- TIME OCC uses military time format.
- CRM CD represents crime categories using numeric codes.
- MO Codes require a lookup table for interpretation.
- Premis Cd corresponds to Premis Desc.
- Crimes are classified into Part 1 and Part 2 offenses.

---

## Next Steps
- Data Cleaning (Upcoming)
- Exploratory Data Analysis (EDA) Upcoming


Made By Youssef Moussa


[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/theyoussefmoussa/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/theyoussefmoussa)

[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/theyosefmusa)
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=website&logoColor=white)](https://theyoussefmoussa.github.io/)