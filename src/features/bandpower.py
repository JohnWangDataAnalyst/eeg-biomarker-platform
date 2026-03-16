"""Bandpower feature extraction."""
import numpy as np
import mne
from mne.time_frequency import psd_array_welch


def compute_bandpower(epochs: mne.Epochs, bands: dict, sfreq: float, normalize: bool = True) -> dict:
    """
    Compute bandpower per epoch per channel.

    Parameters
    ----------
    epochs : mne.Epochs
    bands : dict
        e.g. {"alpha": [8, 13], "beta": [13, 30]}
    sfreq : float
        Sampling frequency.
    normalize : bool
        Normalize each band by total power.

    Returns
    -------
    dict mapping band name -> array (n_epochs, n_channels)
    """
    data = epochs.get_data()  # (n_epochs, n_channels, n_times)
    psds, freqs = psd_array_welch(data, sfreq=sfreq, fmin=1, fmax=sfreq / 2)

    results = {}
    total_power = psds.sum(axis=-1)

    for band_name, (fmin, fmax) in bands.items():
        freq_mask = (freqs >= fmin) & (freqs <= fmax)
        band_power = psds[..., freq_mask].mean(axis=-1)
        if normalize:
            band_power = band_power / (total_power + 1e-12)
        results[band_name] = band_power  # (n_epochs, n_channels)

    return results
