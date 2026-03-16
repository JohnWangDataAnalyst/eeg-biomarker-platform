"""
LOCF (Linear Observer Control Framework) biomarker extraction.

The LOCF fits a linear state-space model to EEG data:
    x_{t+1} = A x_t + K e_t          (state update with Kalman gain K)
    y_t      = C x_t + e_t            (observation equation)
    x_hat_t  = x_hat_{t-1} + L (y_t - C x_hat_{t-1})   (observer update with gain L)

Biomarkers are derived from the fitted K and L matrices.
"""
import numpy as np
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LOCFResult:
    A: np.ndarray          # state transition matrix
    C: np.ndarray          # observation matrix
    K: np.ndarray          # Kalman gain matrix
    L: np.ndarray          # observer gain matrix
    K_norm: float = 0.0
    L_norm: float = 0.0
    converged: bool = False
    n_iter: int = 0


def fit_locf(
    data: np.ndarray,
    n_states: Optional[int] = None,
    max_iter: int = 1000,
    tol: float = 1e-6,
) -> LOCFResult:
    """
    Fit the LOCF model to EEG window data.

    Parameters
    ----------
    data : np.ndarray
        Shape (n_channels, n_times). Single window of EEG data.
    n_states : int, optional
        Number of latent states. Defaults to n_channels.
    max_iter : int
    tol : float

    Returns
    -------
    LOCFResult
    """
    n_channels, n_times = data.shape
    if n_states is None:
        n_states = n_channels

    # --- Placeholder: subspace identification / EM fitting ---
    # TODO: implement full LOCF fitting (subspace ID or EM)
    # This stub returns random matrices with correct shapes for structural testing.
    rng = np.random.default_rng(0)
    A = rng.standard_normal((n_states, n_states)) * 0.1
    C = rng.standard_normal((n_channels, n_states))
    K = rng.standard_normal((n_states, n_channels)) * 0.1
    L = rng.standard_normal((n_states, n_channels)) * 0.1

    result = LOCFResult(
        A=A, C=C, K=K, L=L,
        K_norm=float(np.linalg.norm(K)),
        L_norm=float(np.linalg.norm(L)),
        converged=True,
        n_iter=0,
    )
    return result


def extract_biomarkers(epochs_data: np.ndarray, config: dict) -> dict:
    """
    Run LOCF fitting on each window and aggregate biomarkers.

    Parameters
    ----------
    epochs_data : np.ndarray
        Shape (n_epochs, n_channels, n_times).
    config : dict
        LOCF config section from biomarkers.yaml.

    Returns
    -------
    dict with window-level and subject-level biomarker arrays.
    """
    n_epochs, n_channels, n_times = epochs_data.shape
    n_states = config.get("n_states", None)

    K_norms = np.zeros(n_epochs)
    L_norms = np.zeros(n_epochs)

    for i, window in enumerate(epochs_data):
        result = fit_locf(window, n_states=n_states,
                          max_iter=config.get("max_iter", 1000),
                          tol=config.get("tol", 1e-6))
        K_norms[i] = result.K_norm
        L_norms[i] = result.L_norm

    return {
        # window-level
        "K_norm": K_norms,
        "L_norm": L_norms,
        # subject-level summaries
        "K_norm_mean": float(np.nanmean(K_norms)),
        "L_norm_mean": float(np.nanmean(L_norms)),
        "K_norm_std": float(np.nanstd(K_norms)),
        "L_norm_std": float(np.nanstd(L_norms)),
    }
