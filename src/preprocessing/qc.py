"""QC summary utilities."""
import pandas as pd
from pathlib import Path


def save_qc(qc: dict, output_dir: str, subject_id: str):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([qc])
    df.to_csv(out / f"{subject_id}_qc.csv", index=False)
