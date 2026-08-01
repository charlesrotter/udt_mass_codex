#!/usr/bin/env python3
"""Fail-closed verifier for the whole-configuration Reciprocity audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


EXPECTED_INTERPRETATIONS = {
    "I01": "DERIVED_DESCRIPTION_GROUPOID_EQUIVALENCE",
    "I02": "DERIVED_EQUIVARIANT_ACTION_NOT_FIXEDNESS",
    "I03": "DERIVED_ABSTRACT_COCYCLE_RECONSTRUCTION_NOT_SELECTION",
    "I04": "NOT_DERIVED_FIXEDNESS_IS_EXTRA_PREMISE",
    "I05": "NOT_DERIVED_REQUIRES_MEASURE_OR_PROJECTION",
    "I06": "PAIRING_DERIVED_ON_2D_PAIR_NO_FULL_RESPONSE_COVECTOR",
    "I07": "CONDITIONAL_PARTIAL_ADMISSIBILITY_NO_COMPLETE_RETURN",
    "I08": "NO_JOIN_GRAPH_REMAINS_NONSELECTION",
    "I09": "CONSTRAINED_EQUIVARIANT_FAMILY_NOT_UNIQUE",
    "I10": "NO_OTHER_FOUNDED_RETURN_FOUND",
}

EXPECTED_NATURALITY = {
    "N01": "DERIVED_ABSTRACT_AND_CONDITIONAL_COMPLETE_ACTION",
    "N02": "PARTIAL_CONDITIONAL",
    "N03": "TYPED_BY_COMPONENT_NOT_ONE_COMPLETE_O",
    "N04": "DERIVED_REQUIREMENT_GIVEN_A",
    "N05": "DERIVED_REQUIREMENT_GIVEN_ZERO_PRESERVING_sigma",
    "N06": "NOT_DERIVED",
    "N07": "NOT_DERIVED",
    "N08": "OPEN_NOT_DERIVED",
}


def interpretation_ok(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("candidate_id") for row in rows]
    if len(rows) != 10 or len(ids) != len(set(ids)) or set(ids) != set(EXPECTED_INTERPRETATIONS):
        return False
    by_id = {row["candidate_id"]: row for row in rows}
    return all(
        by_id[key].get("status") == status
        and by_id[key].get("return_gate", "").startswith("FAIL_")
        and by_id[key].get("whole_configuration_content")
        for key, status in EXPECTED_INTERPRETATIONS.items()
    )


def naturality_ok(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("obligation_id") for row in rows]
    if len(rows) != 8 or len(ids) != len(set(ids)) or set(ids) != set(EXPECTED_NATURALITY):
        return False
    by_id = {row["obligation_id"]: row for row in rows}
    return all(by_id[key].get("status") == status and by_id[key].get("consequence") for key, status in EXPECTED_NATURALITY.items())


def result_ok(data: dict) -> bool:
    return data == {
        "complete_action_on_U_full": False,
        "complete_native_return_A": False,
        "equivariance_requirement_derived": True,
        "fixedness_entailed": False,
        "gpu_used": False,
        "interpretations": 10,
        "naturality_obligations": 8,
        "outcome": "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY",
        "passing_native_return_interpretations": 0,
        "solve_authorized": False,
        "source_anchors": 15,
        "source_paths_verified": 1384,
        "zero_set_orbit_saturation_derived_given_A_and_zero_preserving_codomain_action": True,
    }


def algebra_ok(data: dict) -> bool:
    return (
        data.get("orbit_size") == 2
        and data.get("witness_is_fixed") is False
        and data.get("fixed_locus_constraint_rank") == 1
        and data.get("equivariant_return_survivor_counts")
        == {"A_difference_zero_diagonal": 2, "A_identity_zero_origin": 1, "A_product_zero_axes": 3}
        and data.get("equivariance_checks") == 5
        and data.get("equivariance_failures") == 0
        and data.get("affine_sigma_equivariant") is True
        and data.get("affine_sigma_invertible") is True
        and data.get("affine_sigma_fixes_zero") is False
        and data.get("affine_zero_set_orbit_saturated") is False
        and data.get("incidence_rank") == 3
        and data.get("incidence_nullity") == 1
        and data.get("sorted_triangle_witness_checks") == 12
        and data.get("triangle_failures") == 0
        and data.get("comparison_graph_rank") == 6
        and data.get("comparison_graph_nullity") == data.get("comparison_graph_configuration_dimension") == 4
        and data.get("dual_pairing_preservation_checks") == 3
        and data.get("dual_pairing_preservation_failures") == 0
    )


def main() -> None:
    checks: list[tuple[str, bool]] = []
    inventory = tsv("SOURCE_INVENTORY.tsv")
    checks.append(("source_count_1384", len(inventory) == 1384))
    checks.append(("source_unique_sorted", len({r["path"] for r in inventory}) == 1384 and [r["path"] for r in inventory] == sorted(r["path"] for r in inventory)))
    checks.append(("source_bytes_match", all((ROOT / r["path"]).is_file() and sha256(ROOT / r["path"]) == r["sha256"] for r in inventory)))

    anchors = tsv("SOURCE_AUTHORITY_LEDGER.tsv")
    checks.append(("anchors_15", len(anchors) == 15 and len({r["anchor_id"] for r in anchors}) == 15))
    checks.append(("anchor_bytes_match", all(sha256(ROOT / r["path"]) == r["sha256"] for r in anchors)))
    conflicts = tsv("SOURCE_CONFLICT_LEDGER.tsv")
    checks.append(("five_source_conflicts_resolved", len(conflicts) == 5 and all(r["ruling"] and r["effect_on_reciprocity_audit"] for r in conflicts)))
    checks.append(("csn_not_reactivated", next(r for r in conflicts if r["conflict_id"] == "C01")["ruling"] == "SUPERSEDED_FOR_CURRENT_USE__CSN_INACTIVE_CHALLENGED"))
    checks.append(("three_reciprocities_separate", next(r for r in conflicts if r["conflict_id"] == "C05")["ruling"] == "THREE_OBJECTS_SEPARATE"))

    generated = [
        "SOURCE_AUTHORITY_LEDGER.tsv",
        "SOURCE_CONFLICT_LEDGER.tsv",
        "INTERPRETATION_OUTCOMES.tsv",
        "WHOLE_LAW_NATURALITY_LEDGER.tsv",
        "ALGEBRA_RESULT.json",
        "STATUS_LEDGER.tsv",
        "RESULT.json",
    ]
    before = {name: sha256(PKG / name) for name in generated}
    proc = subprocess.run(
        [sys.executable, str(PKG / "derive_whole_configuration_reciprocity.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    after = {name: sha256(PKG / name) for name in generated}
    checks.append(("derivation_exit_0", proc.returncode == 0))
    checks.append(("deterministic_replay", before == after))

    interpretations = tsv("INTERPRETATION_OUTCOMES.tsv")
    naturality = tsv("WHOLE_LAW_NATURALITY_LEDGER.tsv")
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    algebra = json.loads((PKG / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    checks.append(("interpretations_exact", interpretation_ok(interpretations)))
    checks.append(("naturality_exact", naturality_ok(naturality)))
    checks.append(("result_exact", result_ok(result)))
    checks.append(("algebra_exact", algebra_ok(algebra)))
    checks.append(("status_ceiling", tsv("STATUS_LEDGER.tsv")[-1]["status"] == "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY"))

    catches: list[tuple[str, bool]] = []
    catches.append(("missing_interpretation", not interpretation_ok(interpretations[:-1])))
    catches.append(("duplicate_interpretation", not interpretation_ok(interpretations + [copy.deepcopy(interpretations[0])])))
    mutated = copy.deepcopy(interpretations)
    next(r for r in mutated if r["candidate_id"] == "I02")["status"] = "DERIVED_GLOBAL_FIXED_CONFIGURATION"
    catches.append(("equivariance_to_fixedness", not interpretation_ok(mutated)))
    mutated = copy.deepcopy(interpretations)
    next(r for r in mutated if r["candidate_id"] == "I03")["status"] = "DERIVED_REALIZED_PHI_PROFILE"
    catches.append(("cocycle_to_realization", not interpretation_ok(mutated)))
    mutated = copy.deepcopy(interpretations)
    next(r for r in mutated if r["candidate_id"] == "I05")["status"] = "DERIVED_CANONICAL_ORBIT_AVERAGE"
    catches.append(("unselected_average", not interpretation_ok(mutated)))
    mutated = copy.deepcopy(interpretations)
    next(r for r in mutated if r["candidate_id"] == "I06")["status"] = "DERIVED_COMPLETE_RESPONSE_COVECTOR"
    catches.append(("pairing_promotion", not interpretation_ok(mutated)))
    mutated = copy.deepcopy(interpretations)
    next(r for r in mutated if r["candidate_id"] == "I07")["status"] = "DERIVED_COMPLETE_BOUNDARY_RETURN"
    catches.append(("finite_cell_splice", not interpretation_ok(mutated)))
    mutated = copy.deepcopy(interpretations)
    next(r for r in mutated if r["candidate_id"] == "I08")["status"] = "DERIVED_BOOTSTRAP_JOIN"
    catches.append(("graph_to_feedback", not interpretation_ok(mutated)))
    mutated = copy.deepcopy(interpretations)
    next(r for r in mutated if r["candidate_id"] == "I09")["status"] = "SELECTED_P4_RESPONSE_LAW"
    catches.append(("permitted_to_selected_P4", not interpretation_ok(mutated)))
    mutated = copy.deepcopy(naturality)
    next(r for r in mutated if r["obligation_id"] == "N06")["status"] = "DERIVED"
    catches.append(("fixedness_smuggle", not naturality_ok(mutated)))
    mutated = copy.deepcopy(naturality)
    next(r for r in mutated if r["obligation_id"] == "N08")["status"] = "DERIVED_UNIQUE"
    catches.append(("naturality_to_law", not naturality_ok(mutated)))
    mutated = copy.deepcopy(naturality)
    next(r for r in mutated if r["obligation_id"] == "N05")["status"] = "DERIVED_REQUIREMENT_GIVEN_INVERTIBLE_sigma"
    catches.append(("invertibility_without_zero_preservation", not naturality_ok(mutated)))
    mutated = copy.deepcopy(result); mutated["passing_native_return_interpretations"] = 1
    catches.append(("false_return_pass", not result_ok(mutated)))
    mutated = copy.deepcopy(result); mutated["fixedness_entailed"] = True
    catches.append(("false_fixedness", not result_ok(mutated)))
    mutated = copy.deepcopy(result); mutated["complete_action_on_U_full"] = True
    catches.append(("false_complete_action", not result_ok(mutated)))
    mutated = copy.deepcopy(result); mutated["solve_authorized"] = True
    catches.append(("unauthorized_solve", not result_ok(mutated)))
    mutated = copy.deepcopy(algebra); mutated["witness_is_fixed"] = True
    catches.append(("orbit_fixed_confusion", not algebra_ok(mutated)))
    mutated = copy.deepcopy(algebra); mutated["comparison_graph_nullity"] = 0
    catches.append(("graph_called_selection", not algebra_ok(mutated)))
    mutated = copy.deepcopy(algebra); mutated["incidence_nullity"] = 0
    catches.append(("common_offset_erased", not algebra_ok(mutated)))
    mutated = copy.deepcopy(algebra); mutated["dual_pairing_preservation_failures"] = 1
    catches.append(("dual_pair_failure_ignored", not algebra_ok(mutated)))
    mutated = copy.deepcopy(algebra); mutated["affine_sigma_fixes_zero"] = True
    catches.append(("affine_counterexample_erased", not algebra_ok(mutated)))
    checks.extend((f"catch_{name}", passed) for name, passed in catches)

    for name in ["AUDIT_REPORT.md", "EXACT_DERIVATION.md", "COMPLETENESS_MAP.md", "LAY_REPORT.md"]:
        checks.append((f"present_{name}", (PKG / name).is_file()))
    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks.append(("report_outcome", "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY" in report))
    checks.append(("report_no_fixedness", "does not imply that a configuration is fixed" in report))
    checks.append(("report_zero_preserving_scope", "sigma_g(0)=0" in report))
    checks.append(("report_stop_line", "No new premise search" in report))

    failed = [name for name, passed in checks if not passed]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "checks_passed": sum(passed for _, passed in checks),
        "checks_total": len(checks),
        "catch_proofs_passed": sum(passed for _, passed in catches),
        "catch_proofs_total": len(catches),
        "failed": failed,
        "derivation_stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "derivation_stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "failure_class", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows([
            {"catch_id": f"C{i:02d}", "failure_class": name, "result": "REJECTED" if passed else "MISSED"}
            for i, (name, passed) in enumerate(catches, 1)
        ])
    print(f"{'PASS' if not failed else 'FAIL'} Reciprocity verification: {payload['checks_passed']}/{payload['checks_total']}; catches={payload['catch_proofs_passed']}/{payload['catch_proofs_total']}")
    if failed:
        print("failed=" + ",".join(failed), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
