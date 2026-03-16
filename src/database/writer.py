"""Write biomarker tables to the database."""
import pandas as pd
from pathlib import Path


def write_biomarkers(
    subject_id: str,
    session: str,
    biomarkers: dict,
    output_dir: str,
    level: str = "subject",
):
    """
    Save biomarker results to parquet.

    Parameters
    ----------
    subject_id : str
    session : str
    biomarkers : dict
        Output from extract_biomarkers().
    output_dir : str
    level : str
        'subject' or 'window'.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if level == "subject":
        row = {"subject_id": subject_id, "session": session}
        row.update({k: v for k, v in biomarkers.items() if not hasattr(v, "__len__") or isinstance(v, (float, int))})
        df = pd.DataFrame([row])
    elif level == "window":
        import numpy as np
        n = len(next(v for v in biomarkers.values() if hasattr(v, "__len__")))
        df = pd.DataFrame({"subject_id": subject_id, "session": session, "window": range(n)})
        for k, v in biomarkers.items():
            if hasattr(v, "__len__") and len(v) == n:
                df[k] = v
    else:
        raise ValueError(f"Unknown level: {level}")

    fname = out / f"{subject_id}_{session}_{level}_biomarkers.parquet"
    df.to_parquet(fname, index=False)
    return fname
