"""Smoke tests for database write/read."""
import numpy as np
import pandas as pd
import pytest
import tempfile
from src.database.writer import write_biomarkers
from src.database.reader import read_biomarkers, read_cohort_summary


def make_biomarkers(n=5):
    return {
        "K_norm": np.random.rand(n),
        "L_norm": np.random.rand(n),
        "K_norm_mean": 0.5,
        "L_norm_mean": 0.4,
        "K_norm_std": 0.1,
        "L_norm_std": 0.1,
    }


def test_write_read_subject():
    with tempfile.TemporaryDirectory() as tmpdir:
        bm = make_biomarkers()
        write_biomarkers("sub-0001", "rest", bm, tmpdir, level="subject")
        df = read_biomarkers("sub-0001", "rest", tmpdir, level="subject")
        assert "K_norm_mean" in df.columns
        assert len(df) == 1


def test_write_read_window():
    with tempfile.TemporaryDirectory() as tmpdir:
        bm = make_biomarkers(n=10)
        write_biomarkers("sub-0001", "rest", bm, tmpdir, level="window")
        df = read_biomarkers("sub-0001", "rest", tmpdir, level="window")
        assert "K_norm" in df.columns
        assert len(df) == 10


def test_cohort_summary():
    with tempfile.TemporaryDirectory() as tmpdir:
        for sid in ["sub-0001", "sub-0002", "sub-0003"]:
            write_biomarkers(sid, "rest", make_biomarkers(), tmpdir, level="subject")
        df = read_cohort_summary(tmpdir, level="subject")
        assert len(df) == 3
        assert "subject_id" in df.columns
