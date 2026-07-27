#!/usr/bin/env python3
from __future__ import annotations

import copy
import csv
import json
import re
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27"

EXPECTED_STAMPS = {
    "COPRESENCE": "WORKING_INTERPRETIVE_FRAME",
    "METRIC_CAUSAL_STRUCTURE": "DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS": "NOT_DERIVED",
    "COMPLETE_WHOLE_SOLUTION_LAW": "OPEN",
}
EXPECTED_PRIMARY = (
    "ALL_GATE_INTRINSIC_PAIR_CONFIGURATIONS_CONTAIN_OPEN_C3_NEIGHBORHOODS_AROUND_"
    "C01_TO_C06_IN_THE_FIXED_COMPLETE_S3_FAMILY__STRUCTURAL_AVAILABILITY_IS_NOT_"
    "FINE_TUNED_WITHIN_THIS_CONFIGURATION_TOPOLOGY__NO_EXPLICIT_RADIUS_OR_PHYSICAL_"
    "SELECTION_IS_DERIVED"
)


def independent_f(q1: int, q2: int, q3: int) -> int:
    return (
        q1 + 2 * q2 + 3 * q3
        + q1 * q2 + 2 * q2 * q3 + 3 * q3 * q1
        + 2 * q1**2 - 3 * q2**2 + 5 * q3**2
        + q1 * q2 * q3 + 2 * q1**3 - q2**3 + 3 * q3**3
    )


def load_parent_exact() -> dict[str, Fraction]:
    with (PARENT / "CANDIDATE_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return {
        row["candidate_id"]: Fraction(row["gradient_determinant"])
        for row in rows
        if row["candidate_id"] in {f"C0{i}" for i in range(1, 7)}
    }


def validation_errors(payload: dict[str, object], parent: dict[str, Fraction]) -> list[str]:
    errors: list[str] = []
    if payload.get("premise_stamps") != EXPECTED_STAMPS:
        errors.append("premise_stamps")
    topology = payload.get("configuration_topology", {})
    if not isinstance(topology, dict) or topology.get("profile") != "C3(S3)":
        errors.append("C3_topology")
    evidence = payload.get("base_evidence", [])
    if not isinstance(evidence, list) or len(evidence) != 6:
        errors.append("base_count")
    else:
        seen: set[str] = set()
        for item in evidence:
            if not isinstance(item, dict):
                errors.append("evidence_shape")
                continue
            cid = str(item.get("candidate_id"))
            seen.add(cid)
            if item.get("exact_format") != "RATIONAL_FRACTION":
                errors.append(f"exact_format_{cid}")
                continue
            try:
                observed = Fraction(str(item.get("gradient_determinant")))
            except (ValueError, ZeroDivisionError):
                errors.append(f"determinant_parse_{cid}")
                continue
            if cid not in parent or observed != parent[cid] or observed == 0 or item.get("nonzero") is not True:
                errors.append(f"determinant_{cid}")
        if seen != set(parent):
            errors.append("candidate_identity_set")
    certs = payload.get("continuity_certificates", {})
    if not isinstance(certs, dict) or certs.get("curvature_rank") != "CONTINUOUS_IN_C3":
        errors.append("rank_continuity")
    if not isinstance(certs, dict) or certs.get("joint") != "FINITE_INTERSECTION_OPEN":
        errors.append("joint_intersection")
    if not isinstance(certs, dict) or certs.get("slice") != "CONTINUOUS_IN_C0_X_a_X_POSITIVE_R":
        errors.append("slice_scale_continuity")
    margins = payload.get("exact_margins", {})
    expected_margins = {
        "depth_oscillation_lower_bound": "3/25",
        "absolute_a_kappa": "1/32",
        "slice_margin_lower_bound": "4015/331776",
    }
    if margins != expected_margins:
        errors.append("exact_margins")
    if payload.get("all_gate_open_neighborhoods") is not True:
        errors.append("joint_open")
    if payload.get("all_six_centers_certified") is not True:
        errors.append("all_centers")
    if payload.get("explicit_joint_radius_certified") is not False or payload.get("curvature_rank_radius_certified") is not False:
        errors.append("invented_radius")
    for flag in ["generic_dense_or_measure_claim", "physical_selection_claim", "on_shell_claim", "lambda_selected", "profile_selected", "endpoint_or_path_selected", "instantaneous_access_claim"]:
        if payload.get(flag) is not False:
            errors.append(flag)
    physics = payload.get("physics_inferences", {})
    if not isinstance(physics, dict) or any(value is not False for value in physics.values()):
        errors.append("physics_inference")
    meanings = payload.get("degeneration_semantics", {})
    if not isinstance(meanings, dict) or any(value is not False for value in meanings.values()):
        errors.append("degeneration_overclaim")
    if payload.get("axis_count") != 6 or payload.get("axis_ids") != [f"A0{i}" for i in range(1, 7)]:
        errors.append("axis_count")
    if payload.get("stratum_count") != 7 or payload.get("stratum_ids") != [f"S0{i}" for i in range(1, 8)]:
        errors.append("stratum_count")
    if payload.get("primary_conclusion") != EXPECTED_PRIMARY:
        errors.append("primary")
    if payload.get("preregistration_correction_commit") != "0162ba7":
        errors.append("preregistration_correction")
    return errors


def rejected(mutant: dict[str, object], parent: dict[str, Fraction]) -> bool:
    return bool(validation_errors(mutant, parent))


def imports_production_module(source: str) -> bool:
    pattern = re.compile(
        r"^\s*(?:import\s+derive_deformation_neighborhood\b|"
        r"from\s+derive_deformation_neighborhood\s+import\b)",
        re.MULTILINE,
    )
    return bool(pattern.search(source))


def main() -> int:
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    parent = load_parent_exact()
    assert list(sorted(parent)) == [f"C0{i}" for i in range(1, 7)]
    assert all(value != 0 for value in parent.values())
    assert independent_f(1, 0, 0) == 5
    assert independent_f(-1, 0, 0) == -1
    assert Fraction(independent_f(1, 0, 0) - independent_f(-1, 0, 0), 50) == Fraction(3, 25)
    assert abs(Fraction(1, 64) * -2) == Fraction(1, 32)
    assert Fraction(1, 81) - Fraction(1, 4096) == Fraction(4015, 331776) > 0
    assert not validation_errors(payload, parent), validation_errors(payload, parent)

    catches: list[tuple[str, bool, str]] = []

    def mutate(catch_id: str, change, expected: str) -> None:
        mutant = copy.deepcopy(payload)
        change(mutant)
        catches.append((catch_id, rejected(mutant, parent), expected))

    mutate("F01", lambda x: x.__setitem__("instantaneous_access_claim", True), "instant_access_rejected")
    mutate("F02", lambda x: x["premise_stamps"].pop("COPRESENCE"), "stamp_loss_rejected")
    mutate("F03", lambda x: x["base_evidence"][0].__setitem__("gradient_determinant", "0"), "zero_determinant_rejected")
    mutate("F04", lambda x: x["base_evidence"][0].__setitem__("exact_format", "FLOAT"), "float_evidence_rejected")
    mutate("F05", lambda x: x["configuration_topology"].__setitem__("profile", "C2(S3)"), "weak_topology_rejected")
    mutate("F06", lambda x: x["continuity_certificates"].__setitem__("curvature_rank", "UNPROVED"), "missing_continuity_rejected")
    mutate("F07", lambda x: x["exact_margins"].__setitem__("depth_oscillation_lower_bound", "0"), "constant_depth_rejected")
    mutate("F08", lambda x: x["exact_margins"].__setitem__("absolute_a_kappa", "0"), "zero_twist_rejected")
    mutate("F09", lambda x: x["continuity_certificates"].__setitem__("slice", "CONTINUOUS_IN_C0_X_a"), "missing_R_slice_dependence_rejected")
    mutate("F10", lambda x: x["continuity_certificates"].__setitem__("joint", "NOT_TESTED"), "missing_intersection_rejected")
    mutate("F11", lambda x: x["degeneration_semantics"].__setitem__("D_zero_proves_clock_absent", True), "clock_no_go_rejected")
    mutate("F12", lambda x: x["degeneration_semantics"].__setitem__("D_zero_proves_extra_symmetry", True), "symmetry_overclaim_rejected")
    mutate("F13", lambda x: x["degeneration_semantics"].__setitem__("slice_boundary_proves_spacetime_singularity", True), "singularity_overclaim_rejected")
    mutate("F14", lambda x: x.__setitem__("stratum_count", 6), "missing_stratum_rejected")
    mutate("F15", lambda x: x.__setitem__("explicit_joint_radius_certified", True), "invented_radius_rejected")
    mutate("F16", lambda x: x.__setitem__("generic_dense_or_measure_claim", True), "genericity_overclaim_rejected")
    mutate("F17", lambda x: x.__setitem__("physical_selection_claim", True), "physical_selection_rejected")
    mutate("F18", lambda x: x.__setitem__("lambda_selected", True), "lambda_selection_rejected")
    mutate("F19", lambda x: x.__setitem__("endpoint_or_path_selected", True), "semantic_selection_rejected")
    mutate("F20", lambda x: x["physics_inferences"].__setitem__("bootstrap", True), "physics_inference_rejected")
    own_source = Path(__file__).read_text(encoding="utf-8")
    assert not imports_production_module(own_source)
    catches.append(("F21", imports_production_module("import derive_deformation_neighborhood\n"), "production_import_scanner_exercised"))
    mutate("F22", lambda x: x.__setitem__("axis_count", 5), "axis_mutation_rejected")
    assert len(catches) == 22
    assert all(passed for _, passed, _ in catches)

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "result", "exercise"])
        for catch_id, passed, exercise in catches:
            writer.writerow([catch_id, "PASS" if passed else "FAIL", exercise])

    result = {
        "independent_method": "stdlib_exact_reparse_without_production_import",
        "parent_determinants_nonzero": len(parent),
        "exact_depth_margin": "3/25",
        "exact_twist_margin": "1/32",
        "exact_slice_margin_lower_bound": "4015/331776",
        "production_payload_valid": True,
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
        "external_model_verifier": False,
        "grade_ceiling": "VERIFIED_WITH_CAVEATS",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS independent_parent_determinants 6/6")
    print("PASS independent_exact_margins 3/3")
    print("PASS production_payload_validation")
    print("PASS catch_proofs 22/22")
    print("CAVEAT no_fresh_external_model_verifier")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
