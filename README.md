# DNA Rates Across NHS England — GP Appointment Analysis

**Author:** David Kamande  
**Project title:** The GP Appointment Squeeze  
**Tool:** SQLite (DB Browser for SQLite)

## The Problem

NHS GP Did Not Attend (DNA) rates have climbed sharply post-pandemic, costing the NHS an estimated £1B annually and disrupting appointment access. Understanding *where* rates are highest and *why* is critical for targeted resource planning—yet current public data lacks the detailed geographic and demographic breakdown needed for intervention.

## This Analysis

This project answers three critical questions across 200,000+ appointment records spanning 96 Sub-ICB locations and 7 NHS regions, July 2022 to December 2024:

1. **Where are DNA rates highest?** — Regional and Sub-ICB league table to identify hotspots
2. **How has appointment mode shifted?** — Trend analysis of face-to-face vs telephone vs online capacity choices
3. **Is there an inequality pattern?** — DNA risk by deprivation decile (IMD 2019) to reveal vulnerable populations

## Key Finding

Face-to-face GP appointments have a DNA rate of 10.65%, over five times higher than video/online appointments (1.94%) and nearly twice the telephone rate (5.77%). This pattern holds consistently across all seven NHS regions. The most plausible explanation is cancellation friction: remote appointments are easier to quietly ignore, while face-to-face bookings carry a stronger social commitment that makes patients more likely to cancel in advance rather than simply not show up. This challenges the common assumption that remote appointments are harder to attend.

A second counterintuitive result: the least deprived areas (IMD bands 9–10) show the highest average DNA rate (7.40%), compared to 6.12% in the most deprived areas analysed. Deprivation alone is not a reliable predictor of GP DNA rates at Sub-ICB level, suggesting appointment mode mix and urban density are stronger drivers than patient demographics.

## What's Included

**Live dashboard:** [View interactive analysis](./outputs/nhs_dna_dashboard.html)  
**Case study:** [Read detailed methodology and findings](./outputs/GP%20DNA%20Portfolio%20Case%20Study.docx)  
**Data pipeline:** [Reproducible SQL analysis](./GP%20DNA%20SQL%20Queries.sql)

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
