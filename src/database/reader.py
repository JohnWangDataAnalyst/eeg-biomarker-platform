"""Read biomarker tables from the database."""
import pandas as pd
from pathlib import Path
import glob


def read_biomarkers(subject_id: str, session: str, output_dir: str, level: str = "subject") -> pd.DataFrame:
    path = Path(output_dir) / f"{subject_id}_{session}_{level}_biomarkers.parquet"
    return pd.read_parquet(path)


def read_cohort_summary(output_dir: str, level: str = "subject") -> pd.DataFrame:
    files = list(Path(output_dir).glob(f"*_{level}_biomarkers.parquet"))
    if not files:
        raise FileNotFoundError(f"No {level}-level biomarker files in {output_dir}")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
