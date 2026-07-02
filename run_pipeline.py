"""
NHS A&E Performance Analysis: pipeline entry point.

One command reproduces everything:
    python run_pipeline.py

Stages: ingest -> clean -> derive -> validate -> write outputs.
"""
from src import config
from src.ingest import load_raw_files
from src.clean import exclude_aggregate_rows, parse_period
from src.derive import derive_metrics, flag_trend_population
from src.validate import build_validation_report


def main() -> None:
    config.CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_raw_files(config.RAW_DIR)
    df, n_totals = exclude_aggregate_rows(raw)
    df = parse_period(df)
    df = derive_metrics(df)
    df = flag_trend_population(df)

    clean = (
        df[config.OUTPUT_COLUMNS]
        .sort_values(["month", "Org Code"])
        .reset_index(drop=True)
    )
    clean.to_csv(config.CLEAN_FILE, index=False)

    report = build_validation_report(
        clean, n_raw=len(raw), n_totals=n_totals, out_path=config.VALIDATION_FILE
    )
    print(report)
    print(f"\nClean file written to {config.CLEAN_FILE}")


if __name__ == "__main__":
    main()
