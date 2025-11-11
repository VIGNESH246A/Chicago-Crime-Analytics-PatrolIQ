"""
split_500k_into_two_250k.py
---------------------------------
Splits the 500k processed dataset into two 250k CSVs
for EDA and validation.
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "data" / "processed" / "sample_500000_rows.csv"
OUT_1 = BASE_DIR / "data" / "processed" / "sample_250000_rows_01.csv"
OUT_2 = BASE_DIR / "data" / "processed" / "sample_250000_rows_02.csv"

print(f"Loading: {INPUT_PATH}")

if not INPUT_PATH.exists():
    raise FileNotFoundError(f"❌ File not found: {INPUT_PATH}")

# Read CSV
df = pd.read_csv(INPUT_PATH)
print(f"Total rows: {len(df):,}")

# Split into two halves
midpoint = len(df) // 2
df_1 = df.iloc[:midpoint].copy()
df_2 = df.iloc[midpoint:].copy()

# Save outputs
OUT_1.parent.mkdir(parents=True, exist_ok=True)
df_1.to_csv(OUT_1, index=False)
df_2.to_csv(OUT_2, index=False)

print(f"✅ Wrote:\n  {OUT_1} ({len(df_1):,})\n  {OUT_2} ({len(df_2):,})")
