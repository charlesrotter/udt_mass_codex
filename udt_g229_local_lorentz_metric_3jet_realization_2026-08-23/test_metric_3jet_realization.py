#!/usr/bin/env python3
"""Artifact-level regression tests for G229."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_production_landing_and_exact_checks():
    result = load("exact_results.json")
    assert result["all_exact_checks_pass"]
    assert result["landing"] == "FULL_LOCAL_3JET_REALIZATION__COORDINATE_KERNELS_80_AND_140"


def test_complete_curvature_and_derivative_ranks():
    ranks = load("exact_results.json")["ranks"]
    assert ranks["c2"] == 20
    assert ranks["c3"] == 60
    assert ranks["differential_bianchi"] == 20


def test_coordinate_kernels_are_complete():
    result = load("exact_results.json")
    assert result["ranks"]["cubic_gauge"] == 80
    assert result["ranks"]["quartic_gauge"] == 140
    assert result["checks"]["cubic_gauge_in_c2_kernel"]
    assert result["checks"]["quartic_gauge_in_c3_kernel"]


def test_normal_slices_and_unique_gauge_fix():
    result = load("exact_results.json")
    assert result["ranks"]["normal2_slice"] == 20
    assert result["ranks"]["normal3_slice"] == 60
    assert result["ranks"]["normal2_on_cubic_gauge"] == 80
    assert result["ranks"]["normal3_on_quartic_gauge"] == 140


def test_complete_inverse_formulas():
    checks = load("exact_results.json")["checks"]
    assert checks["h_inverse_is_right_inverse"] and checks["h_inverse_is_normal"]
    assert checks["k_inverse_realizes_compatible_basis"] and checks["k_inverse_is_normal"]


def test_independent_full_slot_replay():
    result = load("independent_verification.json")
    assert result["all_checks_pass"]
    assert result["ranks"]["c2_full21"] == 20
    assert result["ranks"]["c3_full84"] == 60
    assert result["ranks"]["combined_D_constraints"] == 24


def test_hostile_controls():
    result = load("hostile_results.json")
    assert result["all_caught"]
    assert result["count"] == 9


def test_projection_and_nonzero_sign_bridge():
    result = load("projection_recovery.json")
    assert result["all_checks_pass"]
    assert result["g227"]["null_tide_map_rank_after_metric_realization"] == 19
    assert result["g227"]["timelike_augmented_rank_after_metric_realization"] == 20
    assert result["g188_jacobi_sign_bridge"]["lower_left_block_equals_minus_tide"]


def test_preregistration_hash_is_frozen():
    expected = "610eac53da7ace52dae4630895eec25cb44025d3be3fd644edf5bab111dd0280"
    assert hashlib.sha256((ROOT / "PREREGISTRATION.md").read_bytes()).hexdigest() == expected


def test_aggregate_verification_and_scope_ceiling():
    verification = load("verification_results.json")
    exact = load("exact_results.json")
    assert verification["all_pass"] and verification["passed"] == verification["total"] == 13
    assert "does not generate values" in exact["scope_ceiling"]
    assert "global history" in exact["scope_ceiling"]
