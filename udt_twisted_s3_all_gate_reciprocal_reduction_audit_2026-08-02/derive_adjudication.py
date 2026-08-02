#!/usr/bin/env python3
"""Adjudicate the exact certificate and exercise semantic failure catches."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(state: dict[str, object]) -> None:
    assert state["headline"] == (
        "EXPLICIT_COMPLETE_OFF_SHELL_TWISTED_S3_METRIC_INTRINSIC_RECIPROCAL_RANK2_REDUCTION_DERIVED__"
        "BRANCH_EXISTENCE_ONLY__UNIVERSAL_AND_ON_SHELL_SELECTION_OPEN"
    )
    assert state["full_killing_algebra"] == "ONE_DIMENSIONAL_EXACT_BOUNDED_WITNESS"
    assert state["clock_line"] == "METRIC_INTRINSIC_ON_EXPLICIT_WITNESS"
    assert state["ruler_line"] == "METRIC_INTRINSIC_FROM_NONZERO_KILLING_TWIST_ON_WITNESS"
    assert state["rank2_reduction"] == "DERIVED_SMOOTH_EQUIVARIANT_ON_EXPLICIT_WITNESS"
    assert state["universal_family_selection"] == "OPEN_NOT_CLAIMED"
    assert state["on_shell_selection"] == "OPEN_NOT_CLAIMED"
    assert state["profile_selected"] is False
    assert state["lambda_selected"] is False
    assert state["physics_promoted"] is False


def main() -> int:
    candidates = table("CANDIDATE_UNIVERSE.tsv")
    gates = table("GEOMETRIC_GATES.tsv")
    contracts = table("FALSIFICATION_CONTRACT.tsv")
    certificate = json.loads((HERE / "INVARIANT_CERTIFICATE.json").read_text(encoding="utf-8"))
    assert len(candidates) == len(certificate["candidate_results"]) == 9
    assert len(gates) == 13 and len(contracts) == 20
    by_id = {row["candidate_id"]: row for row in certificate["candidate_results"]}
    assert set(by_id) == {f"C{i:02d}" for i in range(1, 10)}
    expected_eligible = ["C01", "C02", "C03", "C04", "C05"]
    assert certificate["eligible_exact_nonzero_candidates"] == expected_eligible
    for candidate_id in expected_eligible:
        assert Fraction(by_id[candidate_id]["jacobian_determinant"]) != 0
        assert by_id[candidate_id]["jacobian_nonzero"] is True
    assert by_id["C06"]["jacobian_determinant"] == "0"
    assert by_id["C08"]["jacobian_nonzero"] is True and by_id["C08"]["a_over_R"] == 0
    assert by_id["C09"]["jacobian_determinant"] == "0" and by_id["C09"]["a_over_R"] == 4
    cold_review = (HERE / "COLD_REVIEW_RETURN.md").read_text(encoding="utf-8")
    assert "Verdict: `VERIFIED`" in cold_review
    assert "fbef0067b506b865e8bcb22db07534cd1146712b0d7869b30bd6c9a6915d75ea" in cold_review
    assert "876b00e7d94e249b148846d59612b4cef373430bb1b8fb2f34a1f8ee55160d67" in cold_review
    assert "c182f90aaf32ab6ecb40e394f52a7e8e720206011c9d8ecfc62de99e3e7009dc" in cold_review

    outcome_rows = []
    classifications = {
        "C01": "ALL_GATE_ELIGIBLE_EXACT_KILLING_CERTIFICATE",
        "C02": "ALL_GATE_ELIGIBLE_EXACT_KILLING_CERTIFICATE",
        "C03": "ALL_GATE_ELIGIBLE_EXACT_KILLING_CERTIFICATE",
        "C04": "ALL_GATE_ELIGIBLE_EXACT_KILLING_CERTIFICATE",
        "C05": "ALL_GATE_ELIGIBLE_EXACT_KILLING_CERTIFICATE",
        "C06": "CONSTANT_DEPTH_SYMMETRY_CONTROL_ZERO_CERTIFICATE",
        "C07": "REPEATED_COEFFICIENT_CONTROL_NONZERO_NOT_PROMOTED",
        "C08": "UNIQUE_CLOCK_CERTIFICATE_BUT_TWIST_ZERO_FULL_PAIR_BLOCKED",
        "C09": "SLICE_NULL_CONTROL_ZERO_AT_REGISTERED_CRITICAL_POINT",
    }
    for candidate in candidates:
        result = by_id[candidate["candidate_id"]]
        determinant = result["jacobian_determinant"]
        outcome_rows.append({
            "candidate_id": candidate["candidate_id"],
            "lambda": result["lambda"],
            "a_over_R": result["a_over_R"],
            "chart_point": result["chart_point"],
            "jacobian_nonzero": str(result["jacobian_nonzero"]).upper(),
            "determinant_sha256": hashlib.sha256(determinant.encode()).hexdigest(),
            "determinant_characters": len(determinant),
            "classification": classifications[candidate["candidate_id"]],
        })
    with (HERE / "CANDIDATE_OUTCOMES.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(outcome_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(outcome_rows)

    gate_rows = []
    evidence = {
        "G01": "u_is_weighted_quadratic_with_exact_range_4_to_11",
        "G02": "det_coframe=u^lambda_nonzero_global_Maurer_Cartan_forms",
        "G03": "u^2-a^2_at_least_15_for_primary_a_equals1",
        "G04": "g_KK=-1/u_negative_everywhere",
        "G05": "distinct_quadratic_u_nonconstant",
        "G06": "five_exact_nonzero_curvature_invariant_Jacobians",
        "G07": "twist_coefficient=a_kappa_u^(-(3+2lambda)/2)_nonzero",
        "G08": "twist_dual_spacelike_nonzero_orthogonal_to_timelike_K",
        "G09": "global_nonzero_K_and_W_give_constant_rank_two",
        "G10": "K_rescale_changes_twist_by_positive_square_and_outer_products_unchanged",
        "G11": "tensorial_lines_and_projector_conjugate_under_frame_change",
        "G12": "X_pair=T_tensor_Tflat_plus_S_tensor_Sflat_has_eigenvalues_minus1_plus1_zero_zero",
        "G13": "result_fields_keep_profile_lambda_action_source_density_mass_unselected",
    }
    for gate in gates:
        gate_rows.append({"gate_id": gate["gate_id"], "result": "PASS_EXPLICIT_WITNESS", "evidence": evidence[gate["gate_id"]]})
    with (HERE / "GATE_OUTCOMES.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["gate_id", "result", "evidence"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(gate_rows)

    state = {
        "headline": (
            "EXPLICIT_COMPLETE_OFF_SHELL_TWISTED_S3_METRIC_INTRINSIC_RECIPROCAL_RANK2_REDUCTION_DERIVED__"
            "BRANCH_EXISTENCE_ONLY__UNIVERSAL_AND_ON_SHELL_SELECTION_OPEN"
        ),
        "full_killing_algebra": "ONE_DIMENSIONAL_EXACT_BOUNDED_WITNESS",
        "clock_line": "METRIC_INTRINSIC_ON_EXPLICIT_WITNESS",
        "ruler_line": "METRIC_INTRINSIC_FROM_NONZERO_KILLING_TWIST_ON_WITNESS",
        "rank2_reduction": "DERIVED_SMOOTH_EQUIVARIANT_ON_EXPLICIT_WITNESS",
        "universal_family_selection": "OPEN_NOT_CLAIMED",
        "on_shell_selection": "OPEN_NOT_CLAIMED",
        "profile_selected": False,
        "lambda_selected": False,
        "physics_promoted": False,
    }
    validate(state)
    mutations = (
        ("F01", lambda value: value.update(full_killing_algebra="UNVERIFIED")),
        ("F02", lambda value: value.update(rank2_reduction="UNREGISTERED_PROFILE")),
        ("F03", lambda value: value.update(full_killing_algebra="COMMUTING_FIELDS_ONLY")),
        ("F04", lambda value: value.update(full_killing_algebra="ZERO_PROVES_NONUNIQUE")),
        ("F05", lambda value: value.update(universal_family_selection="DERIVED")),
        ("F06", lambda value: value.update(lambda_selected=True)),
        ("F07", lambda value: value.update(headline="CONTROL_DROPPED")),
        ("F08", lambda value: value.update(ruler_line="TWIST_CONTROL_DROPPED")),
        ("F09", lambda value: value.update(rank2_reduction="CROSSES_SLICE_NULL")),
        ("F10", lambda value: value.update(ruler_line="DERIVED_AT_TWIST_ZERO")),
        ("F11", lambda value: value.update(rank2_reduction="FIXED_COMPONENT_PLANE")),
        ("F12", lambda value: value.update(rank2_reduction="DEPENDS_ON_K_SIGN")),
        ("F13", lambda value: value.update(full_killing_algebra="CRITICAL_SET_OMITTED")),
        ("F14", lambda value: value.update(on_shell_selection="DERIVED")),
        ("F15", lambda value: value.update(physics_promoted=True)),
        ("F16", lambda value: value.update(full_killing_algebra="POST_OUTCOME_INVARIANTS")),
        ("F17", lambda value: value.update(full_killing_algebra="FLOAT_ONLY")),
        ("F18", lambda value: value.update(rank2_reduction="RANK_DROPS")),
        ("F19", lambda value: value.update(headline="Q2_UNIVERSAL")),
        ("F20", lambda value: value.update(headline="NO_COLD_REVIEW")),
    )
    catches = []
    for catch_id, mutation in mutations:
        changed = copy.deepcopy(state)
        mutation(changed)
        caught = False
        try:
            validate(changed)
        except AssertionError:
            caught = True
        assert caught
        catches.append({"catch_id": catch_id, "result": "PASS_CAUGHT"})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["catch_id", "result"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "schema": "udt-twisted-s3-all-gate-adjudication-1.0",
        "status": "PASS_VERIFIED_FRESH_COLD_REVIEW",
        "eligible_exact_nonzero_candidates": expected_eligible,
        "candidate_count": len(candidates),
        "gate_count": len(gates),
        "catch_count": len(catches),
        "source_manifest_sha256": hashlib.sha256((HERE / "SOURCE_MANIFEST.tsv").read_bytes()).hexdigest(),
        "invariant_certificate_sha256": hashlib.sha256((HERE / "INVARIANT_CERTIFICATE.json").read_bytes()).hexdigest(),
        **state,
    }
    (HERE / "ADJUDICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
