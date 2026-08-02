#!/usr/bin/env python3
"""Fail-closed semantic and mutation verification for the general-screen audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> None:
    rows = read_tsv("SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 48
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert hashlib.sha256(content).hexdigest() == row["sha256"]
    assert sha256(HERE / "SOURCE_MANIFEST.tsv") == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()


def build_state() -> dict[str, object]:
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    geometry_rows = read_tsv("GEOMETRIC_ATLAS.tsv")
    result_rows = read_tsv("RESULT_ATLAS.tsv")
    invariant = json.loads((HERE / "INVARIANT_CERTIFICATE.json").read_text())
    geometric = json.loads((HERE / "GEOMETRIC_RESULT.json").read_text())
    adjudication = json.loads((HERE / "ADJUDICATION_RESULT.json").read_text())
    cold = json.loads((HERE / "COLD_REVIEW_RESULT.json").read_text())
    post_repair = json.loads((HERE / "POST_REPAIR_RECHECK_RESULT.json").read_text())
    killing_lemma = json.loads((HERE / "KILLING_LEMMA_CERTIFICATE.json").read_text())
    environment = json.loads((HERE / "RUN_ENVIRONMENT.json").read_text())
    point_nonzero = {}
    point_hashes = {}
    for path in sorted((HERE / "invariant_points").glob("C??_p?.json")):
        row = json.loads(path.read_text())
        key = f"{row['candidate_id']}:{row['point_id']}"
        point_nonzero[key] = row["jacobian_nonzero"]
        point_hashes[key] = sha256(path)
    details = {row["candidate_id"]: row for row in geometric["details"]}
    alternating_point_nonzero = {
        candidate_id: any(
            any(sp.Rational(value) != 0 for value in values)
            for values in row["point_coefficients_xy_xz_yz"].values()
        )
        for candidate_id, row in details.items()
        if row["point_coefficients_xy_xz_yz"]
    }
    return {
        "candidate_ids": [row["candidate_id"] for row in candidates],
        "candidate_universe_sha256": sha256(HERE / "CANDIDATE_UNIVERSE.tsv"),
        "expected_candidate_universe_sha256": adjudication["candidate_universe_sha256"],
        "point_nonzero": point_nonzero,
        "point_hashes": point_hashes,
        "curvature": {row["candidate_id"]: row for row in invariant["candidate_results"]},
        "geometry": {row["candidate_id"]: row for row in geometry_rows},
        "results": {row["candidate_id"]: row for row in result_rows},
        "alternating_point_nonzero": alternating_point_nonzero,
        "killing_route_covers_time_dependent_coefficients": killing_lemma["covers_time_dependent_candidate_coefficients"],
        "projector_reconstructed_after_frame_change": geometric["exact_controls"]["full_frame_tensor_contractions_preserved_after_reconstruction"],
        "T_S_sign_invariant": geometric["exact_controls"]["T_S_sign_invariant"],
        "K_constant_rescale_invariant": geometric["exact_controls"]["K_positive_constant_rescale_invariant"],
        "formula_QT": geometric["formula_QT"],
        "formula_QS": geometric["formula_QS"],
        "formula_Q": geometric["formula_Q"],
        "formula_Phi_contact": geometric["formula_Phi_contact"],
        "alternating_formula": geometric["alternating_formula"],
        "screen_shape_determinant": geometric["screen_shape_determinant"],
        "screen_metric_determinant": geometric["screen_metric_determinant"],
        "screen_metric_tangent_rank": geometric["screen_metric_tangent_rank"],
        "nonzero_scope": adjudication["nonzero_scope"],
        "simple_rank_term_is_exterior_not_matrix_rank": geometric["exact_controls"]["nonzero_simple_means_decomposable_two_form_matrix_rank_two"],
        "explicit_epsilon_witness_candidates": adjudication["full_screen_primary_intrinsic_nonzero_candidates"],
        "neighborhood_parent_J_nonzero": all(point_nonzero[f"{candidate_id}:p1"] for candidate_id in ("C01", "C02", "C03")),
        "neighborhood_finite_jet_C3_continuity": cold["stationary_C3_neighborhood_logic_verified"],
        "open_neighborhood_scope": adjudication["open_neighborhood_scope"],
        "universal_full_screen_claimed": adjudication["universal_full_screen_claimed"],
        "on_shell_claimed": adjudication["on_shell_claimed"],
        "physics_promoted": adjudication["physics_promoted"],
        "GPU_or_fit_used": environment["gpu_used"],
        "independent_shared_production_functions": cold["independent_shared_production_functions"],
        "full_GL2_or_time_live_exhausted": adjudication["full_GL2_or_time_live_exhausted"],
        "initial_cold_review_grade": cold["grade"],
        "cold_review_grade": post_repair["grade"],
    }


def validate(state: dict[str, object]) -> None:
    expected_ids = [f"C{i:02d}" for i in range(1, 19)]
    assert state["candidate_ids"] == expected_ids
    assert state["candidate_universe_sha256"] == state["expected_candidate_universe_sha256"]
    assert len(state["point_nonzero"]) == len(state["point_hashes"]) == 34
    for candidate_id in ("C01", "C02", "C03"):
        assert state["point_nonzero"][f"{candidate_id}:p1"]
        assert state["point_nonzero"][f"{candidate_id}:p2"]
    for candidate_id in [f"C{i:02d}" for i in range(1, 18) if i != 14]:
        any_nonzero = state["point_nonzero"][f"{candidate_id}:p1"] or state["point_nonzero"][f"{candidate_id}:p2"]
        assert any_nonzero
        assert state["curvature"][candidate_id]["curvature_status"] == "UNIQUE_KILLING_LINE_CERTIFIED_DENSE_OPEN"
    assert not state["point_nonzero"]["C14:p1"] and not state["point_nonzero"]["C14:p2"]
    assert state["curvature"]["C14"]["curvature_status"] == "SYMMETRY_ENHANCED_BY_EXACT_GLOBAL_CONTROL"
    assert state["results"]["C14"]["killing_line_status"] == "NOT_UNIQUE_SYMMETRY_ENHANCED"
    assert state["killing_route_covers_time_dependent_coefficients"]
    assert state["projector_reconstructed_after_frame_change"]
    assert state["T_S_sign_invariant"]
    assert state["K_constant_rescale_invariant"]
    assert state["formula_QT"] == "4*a^2/(u*D^2)"
    assert state["formula_QS"] == "4*u/D^2"
    assert state["formula_Q"] == "4*(u-a^2/u)/D^2"
    assert state["formula_Phi_contact"] == "phi-(1/2)*log(abs(a))"
    assert state["results"]["C15"]["pair_projector_status"] == "BLOCKED_TWIST_LINE_ABSENT"
    assert state["results"]["C14"]["intrinsic_contact_alternating_status"] == "BLOCKED_PAIR_PROJECTOR_NOT_INTRINSIC"
    assert state["results"]["C15"]["intrinsic_contact_alternating_status"] == "BLOCKED_TWIST_LINE_ABSENT"
    assert state["alternating_formula"] == "dphi_wedge_dsigma=(du_wedge_dV)/(2*u*V)"
    for candidate_id in ("C01", "C02", "C03", "C05", "C06", "C07", "C11", "C12", "C13", "C14"):
        assert state["geometry"][candidate_id]["configuration_alternating_class"] == "ZERO_IDENTICALLY"
    assert state["alternating_point_nonzero"]["C04"]
    assert state["screen_shape_determinant"] == "1"
    assert state["screen_metric_determinant"] == "u^(2 lambda) V^2"
    assert state["screen_metric_tangent_rank"] == 3
    assert state["nonzero_scope"] == "OPEN_DENSE_WITH_EXACT_ZERO_LOCUS_RETAINED"
    assert state["simple_rank_term_is_exterior_not_matrix_rank"]
    assert state["geometry"]["C16"]["causal_strata"] == "Q_ZERO_AT_U4__Q_POSITIVE_FOR_U_GT_4"
    assert state["geometry"]["C17"]["causal_strata"] == "Q_NEGATIVE_U4_TO_LT5__Q_ZERO_U5__Q_POSITIVE_U_GT5"
    assert state["geometry"]["C16"]["four_metric_status"] == "LORENTZIAN_NONDEGENERATE"
    assert state["curvature"]["C18"]["curvature_status"] == "SKIPPED_METRIC_DEGENERATE"
    assert state["explicit_epsilon_witness_candidates"] == ["C08", "C09", "C10"]
    assert state["neighborhood_parent_J_nonzero"] and state["neighborhood_finite_jet_C3_continuity"]
    assert state["open_neighborhood_scope"] == "STATIONARY_BLOCK_SCREEN_SUBSPACE_RETAINING_K_ONLY"
    assert not state["universal_full_screen_claimed"]
    assert not state["on_shell_claimed"]
    assert not state["physics_promoted"]
    assert not state["GPU_or_fit_used"]
    assert not state["independent_shared_production_functions"]
    assert not state["full_GL2_or_time_live_exhausted"]
    assert state["cold_review_grade"] in {"PASS", "PASS_WITH_CAVEATS"}


def mutate(state: dict[str, object], gate_id: str) -> None:
    if gate_id == "F01": state["candidate_ids"] = state["candidate_ids"][:-1]
    elif gate_id == "F02": state["candidate_universe_sha256"] = "0" * 64
    elif gate_id == "F03": state["point_nonzero"]["C01:p1"] = state["point_nonzero"]["C01:p2"] = False
    elif gate_id == "F04": state["point_nonzero"]["C08:p1"] = state["point_nonzero"]["C08:p2"] = False
    elif gate_id == "F05": state["curvature"]["C14"]["curvature_status"] = "EXTRA_SYMMETRY_FROM_TWO_ZERO_SAMPLES"
    elif gate_id == "F06": state["results"]["C14"]["killing_line_status"] = "UNIQUE_TIMELIKE_KILLING_LINE_DENSE_OPEN"
    elif gate_id == "F07": state["killing_route_covers_time_dependent_coefficients"] = False
    elif gate_id == "F08": state["projector_reconstructed_after_frame_change"] = False
    elif gate_id == "F09": state["T_S_sign_invariant"] = False
    elif gate_id == "F10": state["K_constant_rescale_invariant"] = False
    elif gate_id == "F11": state["formula_Q"] = "4*(u+a^2/u)/D^2"
    elif gate_id == "F12": state["results"]["C15"]["pair_projector_status"] = "METRIC_INTRINSIC_ON_REGISTERED_BRANCH"
    elif gate_id == "F13": state["alternating_formula"] = "dphi_wedge_dsigma=du_wedge_dV"
    elif gate_id == "F14": state["geometry"]["C11"]["configuration_alternating_class"] = "NONZERO_SIMPLE_OPEN_DENSE_WITH_ZERO_LOCUS_RETAINED"
    elif gate_id == "F15": state["alternating_point_nonzero"]["C04"] = False
    elif gate_id == "F16":
        state["screen_metric_determinant"] = "u^(2 lambda) V^2 r^2"
        state["screen_metric_tangent_rank"] = 2
    elif gate_id == "F17": state["nonzero_scope"] = "GLOBAL_NOWHERE_ZERO"
    elif gate_id == "F18": state["simple_rank_term_is_exterior_not_matrix_rank"] = False
    elif gate_id == "F19": state["geometry"]["C16"]["causal_strata"] = "Q_POSITIVE_EVERYWHERE"
    elif gate_id == "F20": state["geometry"]["C17"]["causal_strata"] = "Q_ZERO_ONLY"
    elif gate_id == "F21": state["geometry"]["C16"]["four_metric_status"] = "DEGENERATE"
    elif gate_id == "F22": state["curvature"]["C18"]["curvature_status"] = "UNIQUE_KILLING_LINE_CERTIFIED_DENSE_OPEN"
    elif gate_id == "F23": state["explicit_epsilon_witness_candidates"] = []
    elif gate_id == "F24": state["neighborhood_finite_jet_C3_continuity"] = False
    elif gate_id == "F25": state["universal_full_screen_claimed"] = True
    elif gate_id == "F26": state["on_shell_claimed"] = True
    elif gate_id == "F27": state["physics_promoted"] = True
    elif gate_id == "F28": state["GPU_or_fit_used"] = True
    elif gate_id == "F29": state["independent_shared_production_functions"] = True
    elif gate_id == "F30": state["full_GL2_or_time_live_exhausted"] = True
    else: raise AssertionError(gate_id)


def proof_class(gate_id: str) -> str:
    number = int(gate_id[1:])
    if number in {1, 2, 3, 4, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23}:
        return "EXACT_OUTPUT_OR_ALGEBRA_GUARD"
    if number in {24, 29}:
        return "EVIDENCE_BACKED_SEMANTIC_GUARD"
    return "SEMANTIC_SCOPE_GUARD"


def main() -> int:
    verify_sources()
    contract = read_tsv("FALSIFICATION_CONTRACT.tsv")
    assert [row["gate_id"] for row in contract] == [f"F{i:02d}" for i in range(1, 31)]
    baseline = build_state()
    validate(copy.deepcopy(baseline))
    catches = []
    for row in contract:
        state = copy.deepcopy(baseline)
        mutate(state, row["gate_id"])
        try:
            validate(state)
        except AssertionError as error:
            catches.append({
                "gate_id": row["gate_id"],
                "result": "CAUGHT",
                "proof_class": proof_class(row["gate_id"]),
                "mutation_or_failure": row["mutation_or_failure"],
                "exception": str(error) or "AssertionError",
            })
        else:
            raise AssertionError(f"mutation escaped: {row['gate_id']}")
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["gate_id", "result", "proof_class", "mutation_or_failure", "exception"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "schema": "udt-general-screen-semantic-verification-1.0",
        "status": "PASS",
        "baseline_validation": "PASS",
        "mutation_catches": len(catches),
        "catch_classes": {
            "EXACT_OUTPUT_OR_ALGEBRA_GUARD": sum(row["proof_class"] == "EXACT_OUTPUT_OR_ALGEBRA_GUARD" for row in catches),
            "EVIDENCE_BACKED_SEMANTIC_GUARD": sum(row["proof_class"] == "EVIDENCE_BACKED_SEMANTIC_GUARD" for row in catches),
            "SEMANTIC_SCOPE_GUARD": sum(row["proof_class"] == "SEMANTIC_SCOPE_GUARD" for row in catches),
        },
        "source_manifest_sha256": sha256(HERE / "SOURCE_MANIFEST.tsv"),
        "candidate_universe_sha256": sha256(HERE / "CANDIDATE_UNIVERSE.tsv"),
        "result_atlas_sha256": sha256(HERE / "RESULT_ATLAS.tsv"),
        "initial_independent_review_grade": baseline["initial_cold_review_grade"],
        "independent_review_grade": baseline["cold_review_grade"],
    }
    (HERE / "SEMANTIC_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
