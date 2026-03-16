"""Connectivity feature extraction."""
import numpy as np
import mne
from mne.connectivity import spectral_connectivity_epochs


def compute_connectivity(epochs: mne.Epochs, method: str = "coherence", fmin: float = 1.0, fmax: float = 40.0) -> np.ndarray:
    """
    Compute pairwise connectivity across channels.

    Parameters
    ----------
    epochs : mne.Epochs
    method : str
        Connectivity method (e.g. 'coh', 'plv', 'pli').
    fmin, fmax : float
        Frequency band of interest.

    Returns
    -------
    np.ndarray
        Connectivity matrix (n_channels, n_channels).
    """
    con = spectral_connectivity_epochs(
        epochs,
        method=method,
        fmin=fmin,
        fmax=fmax,
        faverage=True,
        verbose=False,
    )
    # Average over frequencies; shape: (n_channels, n_channels)
    return con.get_data(output="dense")[..., 0]
