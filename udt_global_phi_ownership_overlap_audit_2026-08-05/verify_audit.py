#!/usr/bin/env python3
"""Fail-closed verifier and exercised mutation catches for the ownership audit."""

from __future__ import annotations

import argparse
import ast
import copy
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_ROUTE_IDS = [f"O{i:02d}" for i in range(1, 13)]
EXPECTED_CONCLUSION = (
    "DERIVED_GLOBAL_FACTORIZATION_GROUPOID_FREEDOM_ON_THE_SUPPLIED_SMOOTH_COVER__"
    "DERIVED_COCYCLE_CLASS_AND_PERIOD_INVARIANTS_DO_NOT_SELECT_A_SECTION__"
    "CONDITIONAL_REDUCTIONS_REQUIRE_UNOWNED_REFERENCE_DEPTH_OR_BRANCH_SECTION_DATA__"
    "NO_GLOBAL_PHI_OWNERSHIP_SELECTION"
)
EXPECTED_CLASSIFICATIONS = {
    "O01": "DERIVED_PRESENTATION_FREEDOM",
    "O02": "CONDITIONAL_REDUCTION",
    "O03": "DERIVED_NONSELECTION",
    "O04": "OPEN_ARCHITECTURE_NONSELECTION",
    "O05": "DERIVED_CLASS_DATA_NOT_SECTION",
    "O06": "DERIVED_EQUIVARIANCE_NONSELECTION",
    "O07": "CONDITIONAL_REDUCTION_MOD_CONSTANT",
    "O08": "DERIVED_NONSELECTION",
    "O09": "DERIVED_PERIOD_INVARIANCE_NONSELECTION",
    "O10": "DERIVED_PHYSICAL_GLUE__FACTORIZATION_NONSELECTION",
    "O11": "BRANCH_LOCAL_CONDITIONAL_OWNERSHIP",
    "O12": "NOT_FOUNDED_PERIOD_RESTRICTION_ONLY",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def candidate_guard(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("route_id", "") for row in rows]
    return ids == EXPECTED_ROUTE_IDS and len(ids) == len(set(ids))


def premise_guard(rows: list[dict[str, str]]) -> bool:
    statuses = {row.get("premise_id"): row.get("status") for row in rows}
    required = {
        "P06": "OPEN",
        "P08": "OPEN_ARCHITECTURE",
        "P10": "OPEN_OR_CONDITIONAL",
        "P12": "NOT_FOUNDED_EXTRA",
        "P13": "BRANCH_LOCAL_CONDITIONAL",
        "P14": "INACTIVE",
    }
    return all(statuses.get(key) == value for key, value in required.items())


def result_guard(result: dict[str, object]) -> bool:
    checks = result.get("checks")
    return (
        isinstance(checks, dict)
        and result.get("check_count") == len(checks)
        and len(checks) >= 50
        and all(value is True for value in checks.values())
        and result.get("route_count") == 12
        and result.get("sympy") == "1.13.1"
        and result.get("maximum_conclusion") == EXPECTED_CONCLUSION
    )


def independent_guard(result: dict[str, object]) -> bool:
    checks = result.get("checks")
    return (
        isinstance(checks, dict)
        and result.get("check_count") == len(checks)
        and len(checks) >= 40
        and all(value is True for value in checks.values())
        and result.get("status") == "PASS"
        and result.get("reference_transition_changed") is True
        and result.get("seam_reference_changed") is True
        and result.get("seam_relation_preserved") is True
        and result.get("seam_reference_before") != result.get("seam_reference_after")
        and len(set(result.get("nonconstant_shift_witness", []))) >= 3
    )


def classification_guard(rows: list[dict[str, str]]) -> bool:
    if [row.get("route_id") for row in rows] != EXPECTED_ROUTE_IDS:
        return False
    return all(EXPECTED_CLASSIFICATIONS.get(row["route_id"]) == row.get("classification") for row in rows)


def witness_guard(witness: dict[str, object]) -> bool:
    shifts = witness.get("chart_shift_values", [])
    return (
        witness.get("complete_coframes_unchanged") is True
        and len(shifts) == 3
        and len(set(shifts)) == 3
        and witness.get("fixed_depth_stabilizer_dimension") == 1
        and len(set(witness.get("global_scalar_shift_samples", []))) == 2
        and len(witness.get("affine_cocycles", [])) == 2
        and witness.get("seam_reference_changed") is True
        and witness.get("seam_relation_preserved") is True
        and witness.get("seam_reference_before") != witness.get("seam_reference_after")
        and isinstance(witness.get("seam_physical_transition"), list)
    )


def source_bytes_at(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def git_blob_id(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def sources_guard(manifest: list[dict[str, str]], commit: str) -> bool:
    """Verify the fixed source universe at its preregistration commit.

    LIVE/HANDOFF/frontier are themselves frozen inputs, but must later advance to route the banked
    result. Comparing the manifest to the current worktree would therefore conflate fixed-base
    evidence with current navigation.
    """
    if len(manifest) != 23 or len({row["path"] for row in manifest}) != 23:
        return False
    for row in manifest:
        try:
            data = source_bytes_at(commit, row["path"])
        except subprocess.CalledProcessError:
            return False
        if (
            hashlib.sha256(data).hexdigest() != row["sha256"]
            or str(len(data)) != row["bytes"]
            or git_blob_id(data) != row["git_blob"]
        ):
            return False
    return True


def current_source_drift_guard(manifest: list[dict[str, str]]) -> bool:
    allowed = {"LIVE.md", "HANDOFF.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"}
    changed: set[str] = set()
    for row in manifest:
        path = ROOT / row["path"]
        if not path.is_file():
            return False
        if sha256(path) != row["sha256"] or str(path.stat().st_size) != row["bytes"]:
            changed.add(row["path"])
    return changed == allowed


def imports_guard() -> bool:
    source = (HERE / "independent_global_ownership.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return "sympy" not in names and "derive_global_ownership" not in source and names <= {"__future__", "fractions", "json", "pathlib"}


def mutate_check(result: dict[str, object], name: str) -> dict[str, object]:
    mutated = copy.deepcopy(result)
    mutated["checks"][name] = False  # type: ignore[index]
    return mutated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    frozen = json.loads((HERE / "FROZEN_UNIVERSE.json").read_text())
    candidates = read_tsv(HERE / "CANDIDATE_UNIVERSE.tsv")
    premises = read_tsv(HERE / "PREMISE_LEDGER.tsv")
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    adjudication = read_tsv(HERE / "SOURCE_ADJUDICATION.tsv")
    classifications = read_tsv(HERE / "ROUTE_CLASSIFICATION.tsv")
    result = json.loads((HERE / "RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    witness = json.loads((HERE / "WITNESSES.json").read_text())

    checks = {
        "candidate_universe": candidate_guard(candidates),
        "premise_statuses": premise_guard(premises),
        "source_manifest_at_preregistration_commit": sources_guard(manifest, frozen["preregistration_commit"]),
        "current_source_drift_navigation_only": current_source_drift_guard(manifest),
        "source_adjudication_one_per_source": len(adjudication) == 23 and {row["path"] for row in adjudication} == {row["path"] for row in manifest},
        "source_manifest_frozen_hash": sha256(HERE / "SOURCE_MANIFEST.tsv") == frozen["source_manifest_sha256"],
        "source_adjudication_frozen_hash": sha256(HERE / "SOURCE_ADJUDICATION.tsv") == frozen["source_adjudication_sha256"],
        "candidate_frozen_hash": sha256(HERE / "CANDIDATE_UNIVERSE.tsv") == frozen["candidate_universe_sha256"],
        "premise_frozen_hash": sha256(HERE / "PREMISE_LEDGER.tsv") == frozen["premise_ledger_sha256"],
        "falsification_frozen_hash": sha256(HERE / "FALSIFICATION_CONTRACT.tsv") == frozen["falsification_contract_sha256"],
        "unrelated_metadata_frozen_hash": sha256(HERE / "UNRELATED_UNTRACKED_METADATA.tsv") == frozen["unrelated_untracked_metadata_sha256"],
        "primary_result": result_guard(result),
        "independent_result": independent_guard(independent),
        "independent_imports": imports_guard(),
        "classifications": classification_guard(classifications),
        "witnesses": witness_guard(witness),
        "sympy_pin": (HERE / "requirements.txt").read_text() == "sympy==1.13.1\n",
    }

    catches: list[tuple[str, str, bool]] = []
    missing = candidates[:-1]
    catches.append(("C01", "missing_candidate", not candidate_guard(missing)))
    duplicate = candidates + [copy.deepcopy(candidates[0])]
    catches.append(("C02", "duplicate_candidate", not candidate_guard(duplicate)))
    promoted = copy.deepcopy(premises)
    next(row for row in promoted if row["premise_id"] == "P06")["status"] = "DERIVED"
    catches.append(("C03", "open_depth_promoted", not premise_guard(promoted)))
    loop_promoted = copy.deepcopy(premises)
    next(row for row in loop_promoted if row["premise_id"] == "P12")["status"] = "DERIVED"
    catches.append(("C04", "loop_identity_promoted", not premise_guard(loop_promoted)))
    missing_witness = copy.deepcopy(witness)
    missing_witness["chart_shift_values"] = ["7", "7", "7"]
    catches.append(("C05", "nonconstant_witness_deleted", not witness_guard(missing_witness)))
    catches.append(("C06", "local_identity_broken", not result_guard(mutate_check(result, "local_factorization_identity_1"))))
    catches.append(("C07", "coboundary_order_broken", not result_guard(mutate_check(result, "reference_coboundary_12"))))
    catches.append(("C08", "physical_coframe_mutated", not result_guard(mutate_check(result, "complete_coframe_unchanged_2"))))
    catches.append(("C09", "affine_sign_broken", not result_guard(mutate_check(result, "shifted_affine_cocycle_reversal_twisted"))))
    catches.append(("C10", "triangle_complex_broken", not result_guard(mutate_check(result, "triangle_annihilates_coboundaries"))))
    catches.append(("C11", "free_edge_control_deleted", not result_guard(mutate_check(result, "free_edge_non_coboundary_fails"))))
    catches.append(("C12", "period_invariance_broken", not result_guard(mutate_check(result, "loop_period_gauge_invariant"))))
    catches.append(("C13", "query_basicness_conflated", not result_guard(mutate_check(result, "query_reset_changes_plane_action"))))
    bad_seam_witness = copy.deepcopy(witness)
    bad_seam_witness["seam_reference_after"] = bad_seam_witness["seam_reference_before"]
    bad_seam_witness["seam_reference_changed"] = False
    catches.append(("C14", "seam_witness_made_vacuous", not witness_guard(bad_seam_witness)))
    wrong_class = copy.deepcopy(classifications)
    next(row for row in wrong_class if row["route_id"] == "O07")["classification"] = "DERIVED_GLOBAL_OWNERSHIP"
    catches.append(("C15", "conditional_route_promoted", not classification_guard(wrong_class)))
    bad_independent = copy.deepcopy(independent)
    bad_independent["reference_transition_changed"] = False
    catches.append(("C16", "independent_witness_vacuous", not independent_guard(bad_independent)))

    for catch_id, target, passed in catches:
        checks[f"catch_{catch_id}_{target}"] = passed
    verification = {
        "catch_count": len(catches),
        "check_count": len(checks),
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    if args.write:
        with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(["catch_id", "mutated_target", "expected", "observed"])
            for catch_id, target, passed in catches:
                writer.writerow([catch_id, target, "REJECT", "REJECT" if passed else "ACCEPT"])
        (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")
    print(json.dumps(verification, sort_keys=True))
    raise SystemExit(0 if verification["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
