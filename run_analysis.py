"""
NHS A&E Performance Analysis: SQL analysis entry point.

Runs every query in sql/analysis_questions.sql against the clean
dataset using DuckDB and writes results to reports/sql_answers.md.

Usage: python run_analysis.py  (after python run_pipeline.py)
"""
from pathlib import Path

import duckdb

from src import config

SQL_FILE = Path("sql/analysis_questions.sql")
OUT_FILE = Path("reports/sql_answers.md")

TITLES = [
    "Q1: National monthly trend and the January dip",
    "Q2: Trusts that deteriorated most into January (min 3,000 Jan attendances)",
    "Q3: Regional winter deterioration",
    "Q4: Concentration of January 12-hour DTA waits",
    "Q5: Does attendance volume explain the January deterioration?",
]


def main() -> None:
    if not config.CLEAN_FILE.exists():
        raise FileNotFoundError("Run `python run_pipeline.py` first.")

    con = duckdb.connect()
    con.execute(
        f"CREATE VIEW ae_clean AS SELECT * FROM read_csv_auto('{config.CLEAN_FILE}')"
    )

    # Strip comment lines first, then split into statements on ';'.
    # Splitting before stripping would break on semicolons inside comments.
    sql_text = "\n".join(
        line for line in SQL_FILE.read_text().splitlines()
        if not line.strip().startswith("--")
    )
    statements = [s.strip() for s in sql_text.split(";") if s.strip()]

    OUT_FILE.parent.mkdir(exist_ok=True)
    sections = ["# SQL Analysis Answers\n"]
    for title, stmt in zip(TITLES, statements):
        df = con.execute(stmt).df()
        sections.append(f"## {title}\n\n{df.to_markdown(index=False)}\n")
        print(f"\n=== {title}")
        print(df.to_string(index=False))

    OUT_FILE.write_text("\n".join(sections))
    print(f"\nAnswers written to {OUT_FILE}")


if __name__ == "__main__":
    main()
