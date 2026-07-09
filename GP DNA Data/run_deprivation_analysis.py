"""
GP DNA Project — Corrected Deprivation Analysis (Export F)
==========================================================
Replaces the original text-based Sub-ICB name match with the
correct ONS LSOA (2011) -> Sub-ICB Location lookup.

INPUTS REQUIRED:
  1. IMD 2019 File 7 CSV  -> update IMD_FILE path below
  2. LSOA lookup CSV      -> already in your project folder
  3. Sub-ICB DNA rates    -> Export E, already in your project folder

OUTPUT:
  - Average DNA rate by Deprivation band -- CORRECTED.csv
  - Sub-ICB DNA rate with deprivation -- CORRECTED.csv  (detail)

HOW TO RUN:
  Open a terminal in the GP DNA Data folder and run:
  python run_deprivation_analysis.py
"""

import pandas as pd
import os
import sys

# =============================================================
# PATHS — update IMD_FILE to wherever you saved File 7
# =============================================================

BASE = os.path.dirname(os.path.abspath(__file__))

IMD_FILE = r"C:\Users\ngath\Downloads\File_7_ID_2019_All_ranks__deciles_and_scores_for_the_Indices_of_Deprivation_2019.csv"

LSOA_LOOKUP = os.path.join(
    BASE, "..", "..",
    "LSOA_(2011)_to_Sub_ICB_Locations_(July_2022)_Lookup_in_England.csv"
)

EXPORT_E = os.path.join(
    BASE,
    "DNA rate by Sub-ICB — ranked league table.csv"
)

OUTPUT_DIR = BASE

# =============================================================
# STEP 1 -- Load IMD 2019 File 7
# =============================================================
print("=" * 60)
print("STEP 1: Loading IMD 2019 File 7...")

if not os.path.exists(IMD_FILE):
    print(f"\nERROR: IMD file not found at:\n  {IMD_FILE}")
    print("\nUpdate the IMD_FILE path at the top of this script")
    print("to wherever you saved File 7 from gov.uk.")
    sys.exit(1)

imd_raw = pd.read_csv(IMD_FILE, encoding="latin-1")
print(f"  Loaded {len(imd_raw):,} rows, {len(imd_raw.columns)} columns")

# Detect column names regardless of exact formatting
lsoa_col = next(
    c for c in imd_raw.columns
    if "lsoa" in c.lower() and "code" in c.lower()
)
score_col = next(
    c for c in imd_raw.columns
    if "imd" in c.lower() and "score" in c.lower()
    and "income" not in c.lower() and "rank" not in c.lower()
)
decile_col = next(c for c in imd_raw.columns if "decile" in c.lower())

print(f"  LSOA column  : '{lsoa_col}'")
print(f"  Score column : '{score_col}'")
print(f"  Decile column: '{decile_col}'")

imd = imd_raw[[lsoa_col, score_col, decile_col]].copy()
imd.columns = ["LSOA11CD", "IMD_SCORE", "IMD_DECILE"]
imd["LSOA11CD"]   = imd["LSOA11CD"].str.strip().str.upper()
imd["IMD_SCORE"]  = pd.to_numeric(imd["IMD_SCORE"],  errors="coerce")
imd["IMD_DECILE"] = pd.to_numeric(imd["IMD_DECILE"], errors="coerce")
imd = imd.dropna(subset=["LSOA11CD"])
imd = imd[imd["IMD_DECILE"].between(1, 10)]
print(f"  Clean rows   : {len(imd):,}")

# =============================================================
# STEP 2 -- Load LSOA -> Sub-ICB Lookup
# =============================================================
print("\nSTEP 2: Loading LSOA (2011) -> Sub-ICB lookup...")
lookup = pd.read_csv(LSOA_LOOKUP, encoding="utf-8-sig")
lookup["LSOA11CD"]   = lookup["LSOA11CD"].str.strip().str.upper()
lookup["SICBL22CDH"] = lookup["SICBL22CDH"].str.strip().str.upper()
lookup["SICBL22NM"]  = lookup["SICBL22NM"].str.strip()
print(f"  Loaded {len(lookup):,} rows")
print(f"  Distinct Sub-ICBs in lookup: {lookup['SICBL22CDH'].nunique()}")

# =============================================================
# STEP 3 -- Join IMD to Lookup -> deprivation per Sub-ICB
# =============================================================
print("\nSTEP 3: Joining IMD scores to Sub-ICB codes...")
joined = imd.merge(
    lookup[["LSOA11CD", "SICBL22CDH", "SICBL22NM"]],
    on="LSOA11CD",
    how="inner"
)
match_rate = len(joined) / len(imd) * 100
print(f"  Matched {len(joined):,} of {len(imd):,} IMD LSOAs ({match_rate:.1f}%)")

sub_icb_dep = (
    joined
    .groupby(["SICBL22CDH", "SICBL22NM"])
    .agg(
        avg_imd_score  = ("IMD_SCORE",  "mean"),
        avg_imd_decile = ("IMD_DECILE", "mean"),
        lsoa_count     = ("LSOA11CD",   "count"),
    )
    .reset_index()
    .rename(columns={"SICBL22CDH": "SUB_ICB_CODE", "SICBL22NM": "SUB_ICB_NAME"})
    .round({"avg_imd_score": 2, "avg_imd_decile": 2})
)
print(f"  Sub-ICBs with deprivation scores: {len(sub_icb_dep)}")

# =============================================================
# STEP 4 -- Load Sub-ICB DNA Rates (Export E)
# =============================================================
print("\nSTEP 4: Loading Sub-ICB DNA rates (Export E)...")
dna = pd.read_csv(EXPORT_E, encoding="utf-8-sig")
dna["SUB_ICB_LOCATION_CODE"] = dna["SUB_ICB_LOCATION_CODE"].str.strip().str.upper()
print(f"  Loaded {len(dna)} Sub-ICBs")

# =============================================================
# STEP 5 -- Join DNA rates to deprivation scores
# =============================================================
print("\nSTEP 5: Joining DNA rates to deprivation scores...")
result = dna.merge(
    sub_icb_dep,
    left_on  = "SUB_ICB_LOCATION_CODE",
    right_on = "SUB_ICB_CODE",
    how="left"
)

matched   = result["avg_imd_decile"].notna().sum()
unmatched = result["avg_imd_decile"].isna().sum()
print(f"  Matched  : {matched} Sub-ICBs")
print(f"  Unmatched: {unmatched} Sub-ICBs")
if unmatched > 0:
    print("  Unmatched Sub-ICB codes:")
    print(result[result["avg_imd_decile"].isna()][
        ["SUB_ICB_LOCATION_CODE", "SUB_ICB_LOCATION_NAME"]
    ].to_string(index=False))

# =============================================================
# STEP 6 -- Assign deprivation bands and produce Export F
# =============================================================
print("\nSTEP 6: Assigning deprivation bands...")

BAND_ORDER = [
    "1-2 (Most Deprived)",
    "3-4",
    "5-6 (Mid)",
    "7-8",
    "9-10 (Least Deprived)",
]

def assign_band(decile):
    if pd.isna(decile):  return "Unmatched"
    if decile <= 2:      return "1-2 (Most Deprived)"
    if decile <= 4:      return "3-4"
    if decile <= 6:      return "5-6 (Mid)"
    if decile <= 8:      return "7-8"
    return "9-10 (Least Deprived)"

result["deprivation_band"] = result["avg_imd_decile"].apply(assign_band)
matched_result = result[result["deprivation_band"] != "Unmatched"].copy()

export_f = (
    matched_result
    .groupby("deprivation_band")
    .agg(
        area_count       = ("SUB_ICB_LOCATION_CODE", "count"),
        avg_dna_rate_pct = ("dna_rate_pct",          "mean"),
        min_dna_rate_pct = ("dna_rate_pct",           "min"),
        max_dna_rate_pct = ("dna_rate_pct",           "max"),
    )
    .reset_index()
    .round({"avg_dna_rate_pct": 2, "min_dna_rate_pct": 2, "max_dna_rate_pct": 2})
)

export_f["_sort"] = export_f["deprivation_band"].map(
    {b: i for i, b in enumerate(BAND_ORDER)}
)
export_f = export_f.sort_values("_sort").drop("_sort", axis=1)

# =============================================================
# RESULTS
# =============================================================
print("\n" + "=" * 60)
print("NEW EXPORT F -- DNA Rate by Deprivation Band (CORRECTED)")
print("=" * 60)
print(export_f.to_string(index=False))
print("=" * 60)

# Save Export F summary
out_f = os.path.join(
    OUTPUT_DIR,
    "Average DNA rate by Deprivation band -- CORRECTED.csv"
)
export_f.to_csv(out_f, index=False)
print(f"\nSaved: {out_f}")

# Save Sub-ICB detail file
detail_cols = [
    "SUB_ICB_LOCATION_CODE", "SUB_ICB_LOCATION_NAME", "REGION_NAME",
    "dna_rate_pct", "avg_imd_score", "avg_imd_decile", "deprivation_band"
]
out_detail = os.path.join(
    OUTPUT_DIR,
    "Sub-ICB DNA rate with deprivation -- CORRECTED.csv"
)
(
    matched_result[detail_cols]
    .sort_values("avg_imd_decile")
    .reset_index(drop=True)
    .to_csv(out_detail, index=False)
)
print(f"Saved: {out_detail}")
print("\nDone. Update the case study with figures from the CORRECTED files.")
