"""Preprocessing pipeline: filtering, bad channel detection, ICA, epoching/windowing."""
import mne
import numpy as np
from pathlib import Path
from ..utils.logging import get_logger

logger = get_logger(__name__)


def run_preprocessing(raw: mne.io.Raw, config: dict, output_dir: str, subject_id: str) -> dict:
    """
    Run full preprocessing pipeline on a raw EEG recording.

    Parameters
    ----------
    raw : mne.io.Raw
    config : dict
        Loaded from configs/preprocessing.yaml
    output_dir : str
        Where to save preprocessed output and QC.
    subject_id : str

    Returns
    -------
    dict with keys: 'raw_clean', 'epochs' or 'windows', 'qc'
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    qc = {"subject_id": subject_id}

    # --- Filtering ---
    logger.info(f"[{subject_id}] Filtering {config['l_freq']}-{config['h_freq']} Hz")
    raw.filter(config["l_freq"], config["h_freq"])
    raw.notch_filter(config["notch_freq"])

    # --- Resampling ---
    logger.info(f"[{subject_id}] Resampling to {config['resample_freq']} Hz")
    raw.resample(config["resample_freq"])

    # --- Bad channel detection ---
    logger.info(f"[{subject_id}] Detecting bad channels")
    # Placeholder: implement RANSAC or other method
    qc["n_bad_channels"] = len(raw.info["bads"])
    qc["bad_channels"] = raw.info["bads"]

    # --- ICA ---
    if config.get("run_ica", True):
        logger.info(f"[{subject_id}] Running ICA")
        ica = mne.preprocessing.ICA(
            n_components=config["ica_n_components"],
            method=config["ica_method"],
            random_state=42,
        )
        ica.fit(raw)
        # Placeholder: auto-detect EOG/ECG components
        qc["ica_components_excluded"] = []

    # --- Windowing (resting-state) ---
    logger.info(f"[{subject_id}] Creating windows")
    window_len = config["window_length"]
    overlap = config["window_overlap"]
    step = window_len * (1 - overlap)
    events = mne.make_fixed_length_events(raw, duration=window_len, overlap=window_len * overlap)
    epochs = mne.Epochs(raw, events, tmin=0, tmax=window_len, baseline=None, preload=True)
    qc["n_windows"] = len(epochs)

    # --- Save ---
    epochs.save(out / f"{subject_id}_preprocessed-epo.fif", overwrite=config.get("overwrite", False))
    logger.info(f"[{subject_id}] Done. {len(epochs)} windows saved.")

    return {"epochs": epochs, "qc": qc}
