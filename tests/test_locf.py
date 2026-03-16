"""Smoke tests for LOCF biomarker extraction."""
import numpy as np
import pytest
from src.biomarkers.locf import fit_locf, extract_biomarkers


def make_dummy_data(n_channels=10, n_times=500, n_epochs=5):
    rng = np.random.default_rng(42)
    return rng.standard_normal((n_epochs, n_channels, n_times))


def test_fit_locf_shapes():
    data = make_dummy_data()[0]  # single window: (n_channels, n_times)
    result = fit_locf(data)
    n_ch = data.shape[0]
    assert result.K.shape[1] == n_ch
    assert result.L.shape[1] == n_ch
    assert isinstance(result.K_norm, float)
    assert isinstance(result.L_norm, float)


def test_fit_locf_finite():
    data = make_dummy_data()[0]
    result = fit_locf(data)
    assert np.isfinite(result.K_norm)
    assert np.isfinite(result.L_norm)


def test_extract_biomarkers_keys():
    data = make_dummy_data()
    config = {"n_states": None, "max_iter": 100, "tol": 1e-6}
    bm = extract_biomarkers(data, config)
    for key in ["K_norm", "L_norm", "K_norm_mean", "L_norm_mean", "K_norm_std", "L_norm_std"]:
        assert key in bm, f"Missing key: {key}"


def test_extract_biomarkers_window_length():
    n_epochs = 7
    data = make_dummy_data(n_epochs=n_epochs)
    config = {}
    bm = extract_biomarkers(data, config)
    assert len(bm["K_norm"]) == n_epochs
    assert len(bm["L_norm"]) == n_epochs
