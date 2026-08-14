from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT / "udt_observed_angular_pattern_raw_restart_2026-08-12"
    / "run_r4_empirical_relation_atlas.py"
)
SPEC = importlib.util.spec_from_file_location("r4_relation", MODULE_PATH)
R4 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(R4)


def test_identical_vector_descriptors_and_lags():
    x = np.linspace(-1.0, 2.0, R4.NBIN, dtype=np.float64) ** 3
    values, raw_lag, diff_lag, raw_deg, diff_deg = R4.norm_descriptors(x, x.copy())
    assert values["raw_rms_difference"] == 0.0
    assert values["raw_relative_l2"] == 0.0
    assert np.isclose(values["centered_cosine"], 1.0, atol=1e-15)
    assert np.isclose(values["difference_cosine"], 1.0, atol=1e-15)
    assert np.isclose(raw_lag[118], 1.0, atol=1e-15)
    assert np.isclose(diff_lag[117], 1.0, atol=1e-15)
    assert raw_deg == 0 and diff_deg == 0


def test_constant_vector_degeneracy_is_retained():
    a = np.ones(R4.NBIN)
    b = np.full(R4.NBIN, 2.0)
    values, raw_lag, diff_lag, raw_deg, diff_deg = R4.norm_descriptors(a, b)
    assert values["centered_degenerate"] == 1
    assert values["difference_degenerate"] == 1
    assert raw_deg == 1 and diff_deg == 1
    assert np.array_equal(raw_lag, np.zeros(237))
    assert np.array_equal(diff_lag, np.zeros(235))


def test_lag_direction_convention():
    a = np.zeros(R4.NBIN)
    b = np.zeros(R4.NBIN)
    a[40] = 1.0
    b[43] = 1.0
    _, raw_lag, _, _, _ = R4.norm_descriptors(a, b)
    lag_bins = np.arange(-118, 119)
    assert lag_bins[int(np.argmax(raw_lag))] == -3


def test_frozen_relation_census_total():
    assert R4.RELATION_COUNTS == {
        "RANDOM_DENSITY": 1552,
        "WEIGHT_LANE": 1746,
        "CAP": 1164,
        "ADJACENT_SHELL": 2184,
        "COARSE_FINE_CONTAINMENT": 2640,
    }
    assert sum(R4.RELATION_COUNTS.values()) == 9286
