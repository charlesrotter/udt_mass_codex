#!/usr/bin/env python3
"""Fail-closed verifier for the full-coframe stratified first-jet atlas."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "d666cbabc236d1a2271b30cffc0894d2df842e04"
OUTCOME = (
    "DERIVED_FULL_METRIC_FIRST_JET_SURJECTION__"
    "DERIVED_JOINT_RECIPROCAL_ANGULAR_CAUSAL_STRATA__"
    "NORMALIZED_REDUCTION_HAS_NO_UNIVERSAL_STRATIFIED_EXTENSION__"
    "NO_KINEMATIC_EVOLUTION_RETURN"
)
TRANSITION_RULINGS = {
    "T01": "FULL_40_DIRECTION_FIRST_JET_NONSELECTION",
    "T02": "CLASSIFIES_WITHOUT_SELECTING",
    "T03": "NO_UNIVERSAL_NULL_OR_ZERO_EXTENSION",
    "T04": "FINITE_ACROSS_NONZERO_NULL_NONSELECTION",
    "T05": "PROJECTOR_SIMPLE_POLE_LINE_SURVIVES",
    "T06": "NORMALIZED_LIMIT_PATH_DEPENDENT",
    "T07": "FULL_METRIC_DEGENERATES_NO_CANONICAL_LORENTZ_CONTINUATION",
    "T08": "INVERSE_AND_LEVI_CIVITA_LOST_ADJUGATE_MAY_REMAIN",
    "T09": "SO3_SO12_ISO2_SO13_TYPES_NONSELECTION",
    "T10": "NO_FIRST_JET_EVOLUTION_CONSTRAINT",
    "T11": "MIXING_OR_UNIT_AREA_SHEAR_CHANGES_S_PHI_CLASS",
    "T12": "CIRCULAR_PARENT_LAW_REQUIRED",
}
HYPOTHESIS_RULINGS = {
    "H1": "REFUTED_EXACT",
    "H2": "SUPPORTED_DERIVED",
    "H3": "SUPPORTED_DERIVED",
    "H4": "REFUTED_EXACT",
    "H5": "REFUTED_IN_REGISTERED_METRIC_ARCHITECTURE",
    "H6": "SUPPORTED_DERIVED",
    "H7": "REFUTED_IN_REGISTERED_OPERATION_UNIVERSE",
}


def read_tsv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_blob(path: str):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def validate(
    result,
    independent,
    source_rows,
    sector_rows,
    stratum_rows,
    observable_rows,
    operation_universe_rows,
    premise_rows,
    transition_rows,
    hypothesis_rows,
):
    checks = []
    assert result["outcome"] == OUTCOME, "outcome mismatch"
    assert result["sympy_version"] == "1.13.1", "SymPy version drift"
    checks.append("outcome_and_environment_exact")

    first = result["first_jet"]
    assert first["full_coframe_jet_components"] == 64, "coframe first-jet count changed"
    assert first["full_metric_jet_components"] == 40, "metric first-jet count changed"
    assert first["full_rank"] == 40 and first["full_nullity"] == 24, "full first-jet rank changed"
    assert len(first["per_direction"]) == 4, "a derivative direction was frozen"
    assert all(row["rank"] == 10 and row["nullity"] == 6 for row in first["per_direction"]), "per-direction rank changed"
    assert [row["direction"] for row in first["per_direction"]] == [0, 1, 2, 3], "direction census changed"
    assert first["spatial_and_time_directions_equally_released"], "spatial jet frozen"
    assert first["metric_basis_rank"] == 10, "metric basis incomplete"
    assert first["metric_basis_category_counts"] == {"founded_reciprocal": 1, "other_base": 2, "screen": 3, "mixing": 4}, "basis categories changed"
    assert first["Lorentz_gauge_basis_dimension"] == 6 and first["Lorentz_gauge_tangents_zero"], "Lorentz gauge promoted or lost"
    assert first["first_jet_kinematic_constraint_count"] == 0, "kinematic constraint invented"
    checks.append("full_first_jet_surjection_and_basis_exact")

    joint = result["joint_causal"]
    assert joint["block_inverse_identity_exact"] and joint["causal_formula_identity_exact"], "block identity failed"
    assert joint["same_coordinate_dphi"] == [1, 0, 1, 0], "coordinate dphi witness changed"
    assert joint["mixing_witness_s_phi"] == {"timelike": -3, "null": 0, "spacelike": 1}, "mixing witness changed"
    assert joint["unit_determinant_screen_shear_witness_s_phi"] == {"timelike": "-3/4", "null": 0, "spacelike": 3}, "shear witness changed"
    assert joint["screen_shear_determinants"] == [1, 1, 1], "screen area was not held fixed"
    assert joint["all_three_causal_classes_from_mixing"], "mixing dependence erased"
    assert joint["all_three_causal_classes_from_unit_area_shear"], "shear dependence erased"
    checks.append("joint_reciprocal_angular_causal_formula_and_witnesses")

    causal = result["causal_transitions"]
    null = causal["nonzero_null_crossing"]
    assert null["s_phi"] == "lambda**2 - 1" and null["ds_dlambda_at_plus_one"] == 2, "null path changed"
    assert null["dphi_nonzero_at_plus_one"] and null["unnormalized_outer_at_plus_one_nonzero"], "null survivor lost"
    assert null["normalized_projector_has_simple_pole"], "projector pole erased"
    zero = causal["zero_gradient_crossing"]
    assert not zero["limits_equal"] and not zero["path_independent_normalized_projector_extension"], "zero projector extension promoted"
    assert causal["unnormalized_dphi_and_sharp_remain_finite_at_nonzero_null"], "unnormalized survivor erased"
    checks.append("null_and_zero_gradient_transition_exact")

    ranks = result["rank_transitions"]
    assert ranks["coframe_determinant"] == "lambda" and ranks["metric_determinant"] == "-lambda**2", "rank determinant changed"
    assert ranks["det_g_equals_det_eta_times_det_theta_squared"], "determinant identity failed"
    assert ranks["inverse_metric_33"] == "lambda**(-2)" and ranks["inverse_diverges_at_rank_loss"], "inverse divergence erased"
    assert ranks["metric_adjugate_limit_at_zero"] == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1]], "adjugate limit changed"
    assert ranks["coframe_rank_variety_codimensions_rank_leq_3_2_1_0"] == [1, 4, 9, 16], "coframe codimensions changed"
    assert ranks["screen_rank_variety_codimensions_rank_leq_1_0"] == [1, 4], "screen codimensions changed"
    assert ranks["factorized_det_E_equals_det_Q"], "screen/full rank join erased"
    assert ranks["finite_phi_pair_determinant"] == -1 and not ranks["finite_phi_rank_loss"], "finite phi rank loss invented"
    assert not ranks["canonical_Lorentzian_continuation_from_rank_loss"], "rank continuation invented"
    checks.append("coframe_screen_rank_and_finite_phi_boundaries_exact")

    stabilizers = result["stabilizers"]["rows"]
    expected_stabilizers = [
        ("timelike", 3, 3, [0, 3, 0], "so(3)"),
        ("spacelike", 3, 3, [2, 1, 0], "so(1,2)"),
        ("nonzero_null", 3, 1, [0, 1, 2], "iso(2)"),
        ("zero", 6, 6, [3, 3, 0], "so(1,3)"),
    ]
    actual_stabilizers = [(row["stratum"], row["dimension"], row["Killing_rank"], row["Killing_inertia_positive_negative_zero"], row["algebra_type"]) for row in stabilizers]
    assert actual_stabilizers == expected_stabilizers, "stabilizer atlas changed"
    assert all(row["closed_under_commutator"] for row in stabilizers), "stabilizer closure failed"
    checks.append("Lorentz_stabilizer_algebra_types_exact")

    assert result["maurer_cartan"]["first_jet_constraint_count"] == 0, "first-jet evolution constraint invented"
    assert result["maurer_cartan"]["identity_uses_derivatives_of_first_jet_or_second_jet"], "Maurer-Cartan order changed"
    assert not result["physical_time_evolution_derived"], "configuration path promoted to physical evolution"
    assert not result["native_complete_return_derived"], "native return promoted"
    checks.append("no_kinematic_evolution_or_return_promotion")

    ind_first = independent["first_jet"]
    assert (ind_first["full_rank"], ind_first["full_nullity"], ind_first["metric_basis_rank"]) == (40, 24, 10), "independent first-jet mismatch"
    assert (ind_first["per_direction_rank"], ind_first["per_direction_nullity"], ind_first["Lorentz_gauge_dimension"]) == (10, 6, 6), "independent direction mismatch"
    assert independent["joint_causal"]["mixing"] == joint["mixing_witness_s_phi"], "independent mixing mismatch"
    assert independent["joint_causal"]["unit_area_shear"] == joint["unit_determinant_screen_shear_witness_s_phi"], "independent shear mismatch"
    assert independent["rank_transitions"]["coframe_codimensions"] == ranks["coframe_rank_variety_codimensions_rank_leq_3_2_1_0"], "independent coframe codimension mismatch"
    assert independent["rank_transitions"]["adjugate_limit"] == ranks["metric_adjugate_limit_at_zero"], "independent adjugate mismatch"
    independent_stabilizers = [(row["stratum"], row["dimension"], row["Killing_rank"], row["Killing_inertia_positive_negative_zero"]) for row in independent["stabilizers"]]
    assert independent_stabilizers == [row[:4] for row in expected_stabilizers], "independent stabilizer mismatch"
    assert not independent["physical_time_evolution_derived"] and not independent["native_complete_return_derived"], "independent promotion"
    checks.append("independent_rational_replay_matches")

    assert len(source_rows) == 26 and [row["source_id"] for row in source_rows] == [f"S{i:02d}" for i in range(1, 27)], "source universe changed"
    for row in source_rows:
        assert hashlib.sha256(git_blob(row["path"])).hexdigest() == row["sha256"], f"source hash mismatch: {row['path']}"
    checks.append("base_source_hashes_26_exact")

    assert len(sector_rows) == 15 and [row["sector_id"] for row in sector_rows] == [f"J{i:02d}" for i in range(1, 16)], "sector universe changed"
    assert len(stratum_rows) == 15 and {row["stratum_id"] for row in stratum_rows} == {"P00", "P01", "P02", "P03", "C04", "C03", "C02", "C01", "C00", "Q02", "Q01", "Q00", "A00", "A01", "A02"}, "stratum universe changed"
    assert len(observable_rows) == 17 and [row["observable_id"] for row in observable_rows] == [f"O{i:02d}" for i in range(1, 18)], "observable universe changed"
    assert len(operation_universe_rows) == 12 and [row["operation_id"] for row in operation_universe_rows] == [f"T{i:02d}" for i in range(1, 13)], "operation universe changed"
    assert len(premise_rows) == 20 and [row["premise_id"] for row in premise_rows] == [f"P{i:02d}" for i in range(1, 21)], "premise universe changed"
    premises = {row["premise_id"]: row["status"] for row in premise_rows}
    assert premises["P06"] == "FREE_AND_EXPLORED" and premises["P07"] == "FREE_AND_EXPLORED", "first jets frozen"
    assert premises["P11"] == "NOT_ASSUMED", "path promoted to physical time"
    assert premises["P13"] == "OPEN_NOT_SUPPLIED" and premises["P14"] == "OPEN_NOT_SUPPLIED", "parent law smuggled"
    assert premises["P16"] == "INACTIVE" and premises["P18"] == "POSIT_UNUSED", "inactive premise promoted"
    checks.append("frozen_sector_stratum_observable_operation_and_premise_universes")

    assert len(transition_rows) == 12, "transition ledger count changed"
    assert {row["operation_id"]: row["physical_ruling"] for row in transition_rows} == TRANSITION_RULINGS, "transition rulings changed"
    by_transition = {row["operation_id"]: row for row in transition_rows}
    assert by_transition["T12"]["metric_native_status"] == "UNDEFINED_WITHOUT_PARENT_LAW", "parent-law circularity erased"
    assert len(hypothesis_rows) == 7 and {row["hypothesis_id"]: row["ruling"] for row in hypothesis_rows} == HYPOTHESIS_RULINGS, "hypothesis rulings changed"
    checks.append("transition_and_hypothesis_ledgers_exact")

    report_text = "\n".join((HERE / name).read_text(encoding="utf-8") for name in ["EXACT_DERIVATION.md", "COMPLETENESS_MAP.md", "LAY_REPORT.md", "AUDIT_REPORT.md"])
    for forbidden in ["PHYSICAL_TIME_EVOLUTION_DERIVED", "NATIVE_ACTION_DERIVED", "BOOTSTRAP_RETURN_DERIVED", "MATTER_SOURCE_DERIVED", "RANK_LOSS_REJECTED", "STRONG_CSN_ACTIVE"]:
        assert forbidden not in report_text, f"forbidden promotion: {forbidden}"
    checks.append("semantic_scope_guards")
    return checks


def expect_caught(mutation_id, description, mutate, baseline):
    trial = copy.deepcopy(baseline)
    mutate(*trial)
    try:
        validate(*trial)
    except (AssertionError, KeyError) as exc:
        return {"mutation_id": mutation_id, "description": description, "status": "CAUGHT", "reason": str(exc)}
    raise AssertionError(f"mutation escaped: {mutation_id} {description}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    fresh_result = json.loads(subprocess.check_output(["python3", str(HERE / "derive_stratified_first_jet.py"), "--no-write"], cwd=ROOT, text=True))
    fresh_independent = json.loads(subprocess.check_output(["python3", str(HERE / "independent_stratified_first_jet.py"), "--no-write"], cwd=ROOT, text=True))
    assert fresh_result == result, "fresh primary replay mismatch"
    assert fresh_independent == independent, "fresh independent replay mismatch"

    baseline = [
        result,
        independent,
        read_tsv(HERE / "SOURCE_ADJUDICATION.tsv"),
        read_tsv(HERE / "SECTOR_UNIVERSE.tsv"),
        read_tsv(HERE / "STRATUM_UNIVERSE.tsv"),
        read_tsv(HERE / "OBSERVABLE_UNIVERSE.tsv"),
        read_tsv(HERE / "OPERATION_UNIVERSE.tsv"),
        read_tsv(HERE / "PREMISE_LEDGER.tsv"),
        read_tsv(HERE / "TRANSITION_LEDGER.tsv"),
        read_tsv(HERE / "HYPOTHESIS_LEDGER.tsv"),
    ]
    checks = validate(*baseline)
    checks.append("fresh_primary_and_independent_replays_match_saved_results")

    mutations = [
        ("M01", "wrong outcome", lambda r, *_: r.update(outcome="CLOSED")),
        ("M02", "full metric-jet rank reduced", lambda r, *_: r["first_jet"].update(full_rank=39)),
        ("M03", "spatial direction frozen", lambda r, *_: r["first_jet"]["per_direction"][2].update(rank=9)),
        ("M04", "Lorentz gauge promoted", lambda r, *_: r["first_jet"].update(Lorentz_gauge_tangents_zero=False)),
        ("M05", "metric basis direction deleted", lambda r, *_: r["first_jet"].update(metric_basis_rank=9)),
        ("M06", "mixing dependence erased", lambda r, *_: r["joint_causal"].update(all_three_causal_classes_from_mixing=False)),
        ("M07", "screen shear dependence erased", lambda r, *_: r["joint_causal"].update(all_three_causal_classes_from_unit_area_shear=False)),
        ("M08", "null projector pole erased", lambda r, *_: r["causal_transitions"]["nonzero_null_crossing"].update(normalized_projector_has_simple_pole=False)),
        ("M09", "zero-gradient limits made equal", lambda r, *_: r["causal_transitions"]["zero_gradient_crossing"].update(limits_equal=True)),
        ("M10", "rank-loss continuation invented", lambda r, *_: r["rank_transitions"].update(canonical_Lorentzian_continuation_from_rank_loss=True)),
        ("M11", "finite phi rank loss invented", lambda r, *_: r["rank_transitions"].update(finite_phi_rank_loss=True)),
        ("M12", "null little algebra semisimplified", lambda r, *_: r["stabilizers"]["rows"][2].update(Killing_rank=3)),
        ("M13", "configuration path promoted to physical evolution", lambda r, *_: r.update(physical_time_evolution_derived=True)),
        ("M14", "native return promoted", lambda r, *_: r.update(native_complete_return_derived=True)),
        ("M15", "source hash corrupted", lambda r, i, s, *_: s[0].update(sha256="0" * 64)),
        ("M16", "sector deleted", lambda r, i, s, sectors, *_: sectors.pop()),
        ("M17", "stratum deleted", lambda r, i, s, sectors, strata, *_: strata.pop()),
        ("M18", "observable deleted", lambda r, i, s, sectors, strata, observables, *_: observables.pop()),
        ("M19", "operation universe deleted", lambda r, i, s, sectors, strata, observables, operations, *_: operations.pop()),
        ("M20", "path premise promoted", lambda r, i, s, sectors, strata, observables, operations, premises, *_: next(row for row in premises if row["premise_id"] == "P11").update(status="DERIVED_PHYSICAL_TIME")),
        ("M21", "bulk operator smuggled", lambda r, i, s, sectors, strata, observables, operations, premises, *_: next(row for row in premises if row["premise_id"] == "P13").update(status="DERIVED")),
        ("M22", "parent-law circularity erased", lambda r, i, s, sectors, strata, observables, operations, premises, transitions, *_: next(row for row in transitions if row["operation_id"] == "T12").update(metric_native_status="DERIVED")),
        ("M23", "native return hypothesis promoted", lambda r, i, s, sectors, strata, observables, operations, premises, transitions, hypotheses: next(row for row in hypotheses if row["hypothesis_id"] == "H7").update(ruling="SUPPORTED_DERIVED")),
    ]
    catches = [expect_caught(mid, description, mutate, baseline) for mid, description, mutate in mutations]
    verification = {
        "schema": "udt.full_coframe_first_jet_stratified_transition.verification.v1",
        "status": "PASS",
        "checks_passed": len(checks),
        "checks": checks,
        "mutations_caught": len(catches),
        "catch_proofs": catches,
        "source_adjudication_sha256": hashlib.sha256((HERE / "SOURCE_ADJUDICATION.tsv").read_bytes()).hexdigest(),
    }
    rendered = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        (HERE / "VERIFICATION_RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
