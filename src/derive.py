"""Derived metrics. Four-hour performance is never present in the
source data and must be computed (BUSINESS_PROBLEM.md Section 4)."""
import pandas as pd


def derive_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rule 2: derive Type 1 four-hour performance.
    Performance is NA (not zero) where a provider has no Type 1
    activity: zero would falsely mean '0% seen in time'.
    """
    att = df["A&E attendances Type 1"].fillna(0)
    over = df["Attendances over 4hrs Type 1"].fillna(0)
    df["type1_attendances"] = att.astype(int)
    df["type1_over_4hrs"] = over.astype(int)
    df["type1_perf_pct"] = ((att - over) / att * 100).where(att > 0).round(1)
    df["dta_12hr_waits"] = (
        df["Patients who have waited 12+ hrs from DTA to admission"]
        .fillna(0)
        .astype(int)
    )
    return df


def flag_trend_population(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rule 3: trend comparisons must be like for like, so flag orgs
    reporting Type 1 activity in every month of the period.
    """
    n_months = df["month"].nunique()
    active = df[df["type1_attendances"] > 0]
    counts = active.groupby("Org Code")["month"].nunique()
    consistent = set(counts[counts == n_months].index)
    df["in_trend_population"] = df["Org Code"].isin(consistent)
    return df
