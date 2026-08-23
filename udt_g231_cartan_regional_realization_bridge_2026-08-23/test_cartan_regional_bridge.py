"""Focused exact and evidence tests for G231."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


production = load_module("g231_production_test", "derive_cartan_regional_bridge.py")
independent = load_module("g231_independent_test", "verify_cartan_bridge_independent.py")
hostile = load_module("g231_hostile_test", "hostile_mutation_tests.py")


def test_exact_saved_landing_and_ranks():
    result = json.loads((ROOT / "exact_results.json").read_text(encoding="utf-8"))
    assert result["landing"] == (
        "CARTAN_REGIONAL_BRIDGE__BARE_R_NOT_CLOSED__CLASSIFYING_DERIVATIVE_DATA_REQUIRED"
    )
    assert result["ranks"] == {
        "algebraic_bianchi": 16,
        "differential_bianchi": 20,
        "differentiated_bianchi": 80,
        "commutator": 120,
        "combined_second_prolongation": 194,
    }


def test_exact_dimensions_match_g227_g228_g230():
    result = json.loads((ROOT / "exact_results.json").read_text(encoding="utf-8"))
    assert result["dimensions"] == {
        "cartan_curvature_source": 36,
        "algebraic_curvature_kernel": 20,
        "first_curvature_derivative": 80,
        "first_derivative_compatible": 60,
        "ordered_second_curvature_derivative": 320,
        "second_derivative_affine_translation": 126,
    }


def test_schema_classifier_catches_missing_carry():
    complete = {field: True for field in production.REALIZATION_CONDITIONS}
    assert production.classify_input_schema({"R_typed_as_Lorentz_tensor": True}) == "INCOMPLETE"
    for missing in (
        "horizontal_derivative_law",
        "vertical_action_fixed_by_principal_SO13_action",
        "full_G_structure_algebroid_identities",
        "SO13_equivariance_and_action_conditions",
    ):
        mutated = dict(complete)
        mutated[missing] = False
        assert production.classify_input_schema(mutated) == "INCOMPLETE"


def test_schema_classifier_separates_evaluator_and_realization_problem():
    assert (
        production.classify_input_schema(
            {"theta": True, "omega": True, "R": True}, metric_preowned=True
        )
        == "EVALUATIVE_ALREADY_HAS_METRIC"
    )
    complete = {field: True for field in production.REALIZATION_CONDITIONS}
    assert (
        production.classify_input_schema(complete)
        == "TYPED_CARTAN_REALIZATION_PROBLEM"
    )


def test_independent_no_write_derivation_passes():
    result = independent.derive()
    assert result["all_checks_pass"] is True
    for row in result["ranks_by_prime"].values():
        assert row["combined_second_prolongation"] == 194
    assert result["witness"]["first_nonzero"] == "-1"
    assert result["direct_polynomial_metric_sign_anchor"] == {
        "correct_sign_residual_nonzero_count": 0,
        "differentiated_Bianchi_residual_nonzero_count": 0,
        "reversed_sign_residual_nonzero_count": 2,
    }
    assert result["independent_vertical_action"]["basis_kernel_preserved"] is True
    assert result["independent_vertical_action"]["explicit_transform_matches"] is True


def test_constant_and_nonlinear_controls_are_distinct():
    result = production.derive()
    assert result["constant_curvature_control"]["commutator_rhs_nonzero_count"] == 0
    assert all(
        count == 0
        for count in result["constant_curvature_control"]["closure_residual_counts"].values()
    )
    assert result["nonlinear_witness"]["commutator_rhs_nonzero_count"] > 0


def test_all_vertical_generators_act_nontrivially_on_witness():
    result = production.derive()
    assert all(
        count > 0
        for count in result["vertical_frame_control"]["nonzero_counts_by_Lorentz_generator"]
    )


def test_hostile_suite_catches_every_mutation():
    result = hostile.derive()
    assert result["count"] == 17
    assert result["all_caught"] is True
    assert all(result["catches"].values())


def test_report_preserves_local_and_value_boundaries():
    report = " ".join((ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    assert "does not claim generic smooth or global existence" in report
    assert "does not supply curvature values" in report
    assert "does not choose the curvature profile" in report


def test_claim_scope_is_live_and_rejects_promotions():
    assert production.validate_claim_scope(production.BASELINE_SCOPE)
    for field, promoted in (
        ("curvature_values", "DERIVED"),
        ("classifying_law", "SELECTED"),
        ("generic_smooth", "DERIVED"),
        ("global", "DERIVED"),
        ("physical_history", "DERIVED"),
    ):
        mutation = dict(production.BASELINE_SCOPE)
        mutation[field] = promoted
        assert production.validate_claim_scope(mutation) is False


def test_theorem_boundary_separates_G_realization_from_coframe_only():
    result = production.derive()["theorem_boundary"]
    assert result["finite_type_classifying_data"].startswith("CONDITIONAL_LOCAL_G_REALIZATION")
    assert "COFRAME" in result["infinite_type_PDE_data"]
    assert "DESCENT_OPEN" in result["infinite_type_PDE_data"]
