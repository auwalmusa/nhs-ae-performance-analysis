"""Validation report: states what was read, what was excluded, and
reproduces the national summary so a reviewer can eyeball-check it."""
from pathlib import Path

import pandas as pd


def build_validation_report(
    clean: pd.DataFrame, n_raw: int, n_totals: int, out_path: Path
) -> str:
    trend = clean[clean["in_trend_population"]]
    trend_orgs = trend["Org Code"].nunique()
    nat = trend.groupby("month")[
        ["type1_attendances", "type1_over_4hrs", "dta_12hr_waits"]
    ].sum()
    nat["perf_pct"] = (
        (nat["type1_attendances"] - nat["type1_over_4hrs"])
        / nat["type1_attendances"] * 100
    ).round(1)

    lines = [
        "VALIDATION REPORT: ae_monthly_clean.csv",
        f"Raw rows read: {n_raw}",
        f"Aggregate (TOTAL) rows excluded: {n_totals}",
        f"Clean rows written: {len(clean)}",
        f"Months covered: {clean['month'].min():%b %Y} to {clean['month'].max():%b %Y}",
        f"Orgs in trend population (Type 1 in all months): {trend_orgs}",
        "",
        "National Type 1 monthly summary (trend population):",
        nat[["type1_attendances", "perf_pct", "dta_12hr_waits"]].to_string(),
    ]
    report = "\n".join(lines)
    out_path.write_text(report)
    return report
