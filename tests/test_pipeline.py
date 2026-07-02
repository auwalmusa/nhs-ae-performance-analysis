"""Unit tests for the cleaning and derivation rules.

Each test targets one documented rule, using tiny synthetic data so
the tests run instantly and the expected numbers are obvious.
Run with: pytest
"""
import pandas as pd
import pytest

from src.clean import exclude_aggregate_rows, parse_period
from src.derive import derive_metrics, flag_trend_population


def make_row(period="MSitAE-MARCH-2026", parent="NHS ENGLAND LONDON",
             org="R00", att=100, over=25, dta=5):
    return {
        "Period": period,
        "Org Code": org,
        "Parent Org": parent,
        "Org name": f"TRUST {org}",
        "A&E attendances Type 1": att,
        "Attendances over 4hrs Type 1": over,
        "Patients who have waited 12+ hrs from DTA to admission": dta,
    }


class TestRule1AggregateExclusion:
    def test_excludes_parent_org_total_variant(self):
        df = pd.DataFrame([make_row(), make_row(parent="TOTAL", org="XX")])
        out, n = exclude_aggregate_rows(df)
        assert n == 1
        assert "XX" not in out["Org Code"].values

    def test_excludes_period_total_variant(self):
        df = pd.DataFrame([make_row(), make_row(period="TOTAL", org="XX")])
        out, n = exclude_aggregate_rows(df)
        assert n == 1
        assert "XX" not in out["Org Code"].values

    def test_handles_whitespace_around_total(self):
        df = pd.DataFrame([make_row(parent="TOTAL ", org="XX")])
        out, n = exclude_aggregate_rows(df)
        assert n == 1 and out.empty


class TestPeriodParsing:
    def test_parses_month_and_year(self):
        df = parse_period(pd.DataFrame([make_row(period="MSitAE-JANUARY-2026")]))
        assert df.loc[0, "month"] == pd.Timestamp("2026-01-01")

    def test_malformed_period_fails_loudly(self):
        with pytest.raises(Exception):
            parse_period(pd.DataFrame([make_row(period="GARBAGE")]))


class TestRule2DerivedMetrics:
    def test_performance_formula(self):
        df = derive_metrics(pd.DataFrame([make_row(att=100, over=25)]))
        assert df.loc[0, "type1_perf_pct"] == 75.0

    def test_no_activity_gives_na_not_zero(self):
        df = derive_metrics(pd.DataFrame([make_row(att=0, over=0)]))
        assert pd.isna(df.loc[0, "type1_perf_pct"])


class TestRule3TrendPopulation:
    def test_org_missing_a_month_is_excluded(self):
        rows = [
            make_row(period="MSitAE-JANUARY-2026", org="AAA"),
            make_row(period="MSitAE-FEBRUARY-2026", org="AAA"),
            make_row(period="MSitAE-JANUARY-2026", org="BBB"),
            make_row(period="MSitAE-FEBRUARY-2026", org="BBB", att=0, over=0),
        ]
        df = flag_trend_population(derive_metrics(parse_period(pd.DataFrame(rows))))
        by_org = df.groupby("Org Code")["in_trend_population"].all()
        assert bool(by_org["AAA"]) is True
        assert bool(by_org["BBB"]) is False
