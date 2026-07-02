"""Cleaning rules. Each function implements one numbered rule from
BUSINESS_PROBLEM.md Section 5, so documentation and code tell the
same story."""
import pandas as pd


def exclude_aggregate_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Rule 1: exclude pre-computed England total rows, which double-count
    everything if loaded. Two variants occur in the wild:
    Parent Org = 'TOTAL' in some files, Period = 'TOTAL' in others.
    Returns the filtered frame and the number of rows removed.
    """
    is_total = (
        df["Parent Org"].str.strip().eq("TOTAL")
        | df["Period"].str.strip().eq("TOTAL")
    )
    return df.loc[~is_total].copy(), int(is_total.sum())


def parse_period(df: pd.DataFrame) -> pd.DataFrame:
    """Turn 'MSitAE-MARCH-2026' into a proper month-start date."""
    parts = df["Period"].str.strip().str.split("-", expand=True)
    df["month"] = pd.to_datetime(
        parts[1] + " " + parts[2], format="%B %Y", errors="raise"
    )
    return df
