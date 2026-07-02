"""
Central configuration.
Every path and constant lives here so no module hard-codes anything.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
CLEAN_FILE = CLEAN_DIR / "ae_monthly_clean.csv"
VALIDATION_FILE = CLEAN_DIR / "validation_report.txt"

# Columns we rely on, exactly as named by NHS England.
REQUIRED_COLUMNS = [
    "Period",
    "Org Code",
    "Parent Org",
    "Org name",
    "A&E attendances Type 1",
    "Attendances over 4hrs Type 1",
    "Patients who have waited 12+ hrs from DTA to admission",
]

OUTPUT_COLUMNS = [
    "month", "Org Code", "Org name", "Parent Org",
    "type1_attendances", "type1_over_4hrs", "type1_perf_pct",
    "dta_12hr_waits", "in_trend_population", "source_file",
]
