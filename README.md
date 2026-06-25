# DNA Rates Across NHS England — GP Appointment Analysis

**Author:** David Kamande  
**Project title:** The GP Appointment Squeeze  
**Tool:** SQLite (DB Browser for SQLite)

## The problem

NHS England estimates missed GP appointments cost over £1 billion a year, with Did Not Attend (DNA) rates running above 5% nationally. Most commentary on this assumes deprivation and lack of access drive the problem. This analysis tests that assumption against 200,000+ appointment records across 96 Sub-ICB locations and 7 NHS regions (July 2022 - December 2024), and finds it doesn't hold.

Three questions structure the analysis:

1. Where are DNA rates highest, and is the variation structural or random?
2. Does appointment mode (face-to-face, telephone, video/online) affect attendance?
3. Does area-level deprivation predict DNA rates?

## Key finding

Face-to-face appointments have a DNA rate of 10.65%, over five times higher than video/online (1.94%) and nearly double telephone (5.77%), consistently across all seven NHS regions. The likely mechanism is cancellation friction: a remote appointment is easy to quietly ignore, while a face-to-face booking carries enough social commitment that people cancel ahead of time instead of just not showing up.

A second result cuts against the access-inequality narrative directly: the least deprived areas (IMD bands 9-10) average a higher DNA rate (7.40%) than the most deprived areas analysed (6.12%). Deprivation alone doesn't predict DNA rates at Sub-ICB level - appointment mode mix and urban density look like stronger drivers than patient demographics.

## What's included

**Live dashboard:** [View interactive analysis](https://ngatho1.github.io/DNA-Rates-Across-NHS-England/outputs/nhs_dna_dashboard.html)  
**Case study:** [Read detailed methodology and findings](./outputs/GP%20DNA%20Portfolio%20Case%20Study.pdf)  
**Data pipeline:** [Reproducible SQL analysis](./GP%20DNA%20SQL%20Queries.sql)

## Getting started

1. Install [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `GP DNA.db`
3. Run **Step 1** of `GP DNA SQL Queries.sql` to create the raw table schemas
4. Import each CSV via *File > Import > Table from CSV*, naming tables exactly as shown in Step 1
5. Run Steps 2-8 in order

### `GP DNA.db`
The SQLite database containing all raw and cleaned tables. Import the source CSVs (see below) using DB Browser for SQLite before running the SQL queries.

| Table | Source | Rows | Description |
|---|---|---|---|
| `national_overview_raw` | National_Overview.csv | ~49,703 | National appointment counts by status, mode, and HCP type — no geography, 30 months |
| `pcn_granular_raw` | PCN_GRANULAR.csv | ~154,002 | Sub-ICB level counts with full geography embedded, 21 months |
| `deprivation_raw` | IMD 2019 File 7 (gov.uk) | ~33,000 | LSOA-level deprivation scores, ranks, and deciles |

### `GP DNA SQL Queries.md.sql`
The full analysis pipeline in eight steps:

| Step | Purpose |
|---|---|
| 1 | Raw table schemas — run once to create tables before importing CSVs |
| 2 | Sense checks on raw data (row counts, date ranges, null checks) |
| 3 | Data cleaning — casts TEXT columns to numeric, creates `_clean` tables |
| 4 | Post-cleaning sense checks |
| 5 | **Q1 analysis** — DNA rates by region and Sub-ICB (league table) |
| 6 | **Q2 analysis** — appointment mode shift over time (national) |
| 7 | **Q3 analysis** — DNA rate by IMD deprivation decile |
| 8 | Export queries used to feed the Excel dashboard |

### `GP DNA Data/` — Exported Analysis Results (CSV)

These CSVs are the outputs of the Step 8 export queries, used directly by the Excel dashboard and HTML dashboard.

| File | Feeds |
|---|---|
| `National DNA Trend Over TIme (from National Overview).csv` | Q2 national trend chart |
| `Mode mix shift over time — national overview.csv` | Q2 mode breakdown chart |
| `DNA rate by Region — high-level story.csv` | Q1 regional summary |
| `DNA rate by Sub-ICB — ranked league table.csv` | Q1 full Sub-ICB ranking |
| `Top 10 and Bottom 10 Sub-ICBs.csv` | Q1 highlight table |
| `DNA rate by appointment mode — from PCN granular.csv` | Q1/Q2 cross-cut |
| `DNA rate by mode AND region — cross-cut.csv` | Q1/Q2 regional mode breakdown |
| `Average DNA rate by Deprivation band.csv` | Q3 inequality chart |

### `GP DNA Portfolio Dashboard.xlsx`
Excel workbook with charts and pivot tables built from the CSV exports above. Used for the portfolio case study presentation.

### `GP DNA Portfolio Case Study.docx`
Written case study documenting the analytical approach, key findings, and recommendations. References charts from the Excel dashboard.

### `nhs_dna_dashboard.html`
Self-contained interactive HTML dashboard presenting the same findings as the Excel file, suitable for sharing without requiring Excel.

---

## How the pieces fit together

```
Raw CSVs (NHS England + gov.uk)
        ↓
GP DNA.db  ←  GP DNA SQL Queries.md.sql
        ↓ (Step 8 exports)
GP DNA Data/*.csv
        ↓
GP DNA Portfolio Dashboard.xlsx   →   GP DNA Portfolio Case Study.docx
nhs_dna_dashboard.html
```

---

## Data sources

- [NHS England GP Appointments in General Practice](https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice) — national overview and PCN granular datasets
- [English Indices of Deprivation 2019, File 7](https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019) — LSOA-level IMD scores
