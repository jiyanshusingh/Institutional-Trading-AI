from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from feature_engine.feature_engine import FeatureEngine
from research.target_builder import TargetBuilder
from research.target_definitions import TARGET_DEFINITIONS
from research.feature_audit import FeatureAudit

# ------------------------------------------------------
# CHANGE THIS PATH
# ------------------------------------------------------

CSV_PATH = Path(
    "historical_data/normalized/ACUTAAS_1m.csv"
)

# ------------------------------------------------------
# Load
# ------------------------------------------------------

print("=" * 60)
print("STEP 1 : LOAD CSV")
print("=" * 60)

df = pd.read_csv(
    CSV_PATH,
    parse_dates=["timestamp"],
)

print(df.head())
print()
print(df.shape)

# ------------------------------------------------------
# Feature Engine
# ------------------------------------------------------

print()
print("=" * 60)
print("STEP 2 : FEATURE ENGINE")
print("=" * 60)

engine = FeatureEngine()

feature_df = engine.run(df)

print(feature_df.head())

print()
print("Columns :", len(feature_df.columns))

# ------------------------------------------------------
# Target Builder
# ------------------------------------------------------

print()
print("=" * 60)
print("STEP 3 : TARGET BUILDER")
print("=" * 60)

feature_df = TargetBuilder.build(
    feature_df,
    list(TARGET_DEFINITIONS),
)
print()
print("=" * 60)
print("STEP 4 : FEATURE AUDIT")
print("=" * 60)

audit_df = FeatureAudit.audit(
    feature_df,
    output_path="research/results/feature_audit.csv",
)

print(audit_df.head())

print()
print(f"Audited Features : {len(audit_df)}")

print()
print("PASS :", (audit_df["status"] == "PASS").sum())
print("FAIL :", (audit_df["status"] == "FAIL").sum())

print(feature_df.head())
feature_df.to_csv(
    "research/results/feature_dataset.csv",
    index=False,
)
print()

print("Columns :", len(feature_df.columns))

print()

print("Done.")
RESULTS_DIR = Path("research/results")
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

feature_df.to_csv(
    RESULTS_DIR / "feature_dataset.csv",
    index=False,
)

print()
print("Feature dataset saved to:")
print(RESULTS_DIR / "feature_dataset.csv")