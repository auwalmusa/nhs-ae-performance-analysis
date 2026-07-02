"""Ingestion: read raw NHS England monthly CSVs and stack them."""
from pathlib import Path

import pandas as pd

from src.config import REQUIRED_COLUMNS


def load_raw_files(raw_dir: Path) -> pd.DataFrame:
    """
    Read every CSV in raw_dir into one DataFrame.

    Fails loudly if the folder is empty or a file is missing an
    expected column, rather than producing silently wrong numbers.
    """
    files = sorted(raw_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir.resolve()}")

    frames = []
    for f in files:
        df = pd.read_csv(f, encoding="utf-8-sig")
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"{f.name} is missing expected columns: {missing}")
        df["source_file"] = f.name
        frames.append(df)

    return pd.concat(frames, ignore_index=True)
