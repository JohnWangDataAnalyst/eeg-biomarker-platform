#!/usr/bin/env python3
"""Aggregate all subject biomarker parquet files into a cohort summary."""
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.reader import read_cohort_summary
from src.utils.config import load_paths


def main():
    paths = load_paths()
    bm_dir = Path(paths["outputs_root"]) / "biomarkers"
    cohort_dir = Path(paths["outputs_root"]) / "cohort"
    cohort_dir.mkdir(parents=True, exist_ok=True)

    for level in ["subject", "window"]:
        try:
            df = read_cohort_summary(str(bm_dir), level=level)
            out = cohort_dir / f"cohort_{level}_biomarkers.parquet"
            df.to_parquet(out, index=False)
            print(f"Saved {level} cohort table: {out} ({len(df)} rows)")
        except FileNotFoundError as e:
            print(f"Warning: {e}")


if __name__ == "__main__":
    main()
