"""Parse LEMON dataset metadata into a subject registry."""
import pandas as pd
from pathlib import Path


def parse_metadata(lemon_root: str) -> pd.DataFrame:
    """
    Build a subject registry from LEMON participants.tsv.

    Parameters
    ----------
    lemon_root : str
        Path to the LEMON dataset root.

    Returns
    -------
    pd.DataFrame
        Subject registry with available sessions and metadata.
    """
    tsv_path = Path(lemon_root) / "participants.tsv"
    if not tsv_path.exists():
        raise FileNotFoundError(f"participants.tsv not found at {tsv_path}")
    df = pd.read_csv(tsv_path, sep="\t")
    return df
