"""Load raw EEG data for a subject from the LEMON dataset."""
import mne
from pathlib import Path


def load_subject(subject_id: str, lemon_root: str, session: str = "rest") -> mne.io.Raw:
    """
    Load raw EEG for a given subject.

    Parameters
    ----------
    subject_id : str
        Subject identifier, e.g. "sub-0001".
    lemon_root : str
        Path to the LEMON dataset root.
    session : str
        Session label (default "rest").

    Returns
    -------
    mne.io.Raw
        Raw EEG object.
    """
    root = Path(lemon_root)
    # LEMON BIDS structure: sub-<id>/ses-<session>/eeg/
    eeg_dir = root / subject_id / f"ses-{session}" / "eeg"
    candidates = list(eeg_dir.glob("*.vhdr")) + list(eeg_dir.glob("*.edf"))
    if not candidates:
        raise FileNotFoundError(f"No EEG file found for {subject_id} in {eeg_dir}")
    raw = mne.io.read_raw(str(candidates[0]), preload=True)
    return raw
