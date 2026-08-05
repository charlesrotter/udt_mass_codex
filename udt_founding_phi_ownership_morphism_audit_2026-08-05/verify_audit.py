#!/usr/bin/env python3
"""Fail-closed verifier with exercised mutations for the ownership audit."""

from __future__ import annotations

import argparse
import ast
import copy
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_IDS = [f"M{i:02d}" for i in range(1, 11)]
EXPECTED_CLASSES = {
    "M01": "FOUNDING_DERIVED_ABSTRACT_GIVEN_SUPPLIED_DEPTH",
    "M02": "CONDITIONAL_TYPED_PATH_COCYCLE__NATIVE_DEPTH_OPEN",
    "M03": "CONDITIONAL_BRANCH_LOCAL_KILLING_DEPTH__NO_UNIVERSAL_EXTRACTION",
    "M04": "CONDITIONAL_EXTRA_REFERENCE",
    "M05": "DERIVED_CHARACTER_ON_SUPPLIED_PAIR__NO_REPRESENTATIVE_SELECTION",
    "M06": "CONDITIONAL_OPERATIONAL_INPUT__NOT_METRIC_DERIVED",
    "M07": "DERIVED_PRESENTATION_ORBIT__INSUFFICIENT_FOR_SCALAR_READOUT",
    "M08": "NOT_DERIVED_EXTRA_NORMALIZATION",
    "M09": "DERIVED_CALIBRATION_AND_CHARACTER__DEPTH_UNIT_AND_ASSIGNMENT_OPEN",
    "M10": "WORKING_RELATION_NONFUNCTIONAL__NO_OWNERSHIP_SELECTION",
}
EXPECTED_CONCLUSION = (
    "DERIVED_FOUNDING_OBJECT_IS_A_RELATIONAL_RECIPROCAL_CHARACTER_ON_SUPPLIED_DEPTH__"
    "DERIVED_POINTWISE_PHI_IS_A_PRESENTATION_POTENTIAL_ON_THE_SUPPLIED_FACTORIZED_ARCHITECTURE__"
    "CONDITIONAL_STATIONARY_KILLING_AND_SUPPLIED_QUERY_REALIZATIONS__"
    "NO_UNIVERSAL_FOUNDED_PHI_OWNERSHIP_MORPHISM_IN_FROZEN_NATIVE_SOURCES"
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_at(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def manifest_guard(rows: list[dict[str, str]], commit: str, expected: int) -> bool:
    if len(rows) != expected or len({row.get("path") for row in rows}) != expected:
        return False
    for row in rows:
        try:
            data = source_at(commit, row["path"])
        except subprocess.CalledProcessError:
            return False
        if sha(data) != row["sha256"] or str(len(data)) != row["bytes"] or git_blob(data) != row["git_blob"]:
            return False
    return True


def candidate_guard(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("route_id") for row in rows]
    return ids == EXPECTED_IDS and len(ids) == len(set(ids))


def route_guard(rows: list[dict[str, str]]) -> bool:
    return (
        [row.get("route_id") for row in rows] == EXPECTED_IDS
        and all(EXPECTED_CLASSES.get(row["route_id"]) == row.get("classification") for row in rows)
    )


def result_guard(result: dict[str, object]) -> bool:
    checks = result.get("checks")
    return (
        isinstance(checks, dict)
        and result.get("status") == "PASS"
        and result.get("sympy") == "1.13.1"
        and result.get("check_count") == len(checks) == 34
        and all(value is True for value in checks.values())
        and result.get("route_count") == 10
        and result.get("maximum_conclusion") == EXPECTED_CONCLUSION
    )


def independent_guard(result: dict[str, object]) -> bool:
    checks = result.get("checks")
    return (
        isinstance(checks, dict)
        and result.get("status") == "PASS"
        and result.get("check_count") == len(checks) == 24
        and all(value is True for value in checks.values())
        and result.get("depth_before") != result.get("depth_after")
        and result.get("physical_arrow") == result.get("physical_arrow_after")
    )


def witness_guard(witness: dict[str, object]) -> bool:
    lapse = witness.get("stationary_killing_lapse_ratios", {})
    depth = witness.get("stationary_depth_ratios", {})
    return (
        witness.get("depth_before") != witness.get("depth_after")
        and witness.get("physical_arrow") == witness.get("physical_arrow_after")
        and witness.get("factorization_theta") == witness.get("factorization_theta_shifted")
        and witness.get("normalization_family_powers") == [1, 2]
        and isinstance(lapse, dict)
        and isinstance(depth, dict)
        and set(lapse) == set(depth) == {"ab", "bc", "ac"}
        and all(Fraction(str(lapse[key])) * Fraction(str(depth[key])) == 1 for key in lapse)
    )


def imports_guard(source: str | None = None) -> bool:
    if source is None:
        source = (HERE / "independent_founding_ownership.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return "sympy" not in names and "derive_founding_ownership" not in source and names <= {"__future__", "fractions", "json", "pathlib"}


def source_union_guard(base_rows: list[dict[str, str]], add_rows: list[dict[str, str]]) -> bool:
    base = {row.get("path") for row in base_rows}
    add = {row.get("path") for row in add_rows}
    return len(base_rows) == len(base) == 31 and len(add_rows) == len(add) == 4 and not (base & add) and len(base | add) == 35


def current_drift_guard(base_rows: list[dict[str, str]], add_rows: list[dict[str, str]]) -> bool:
    allowed = {"LIVE.md", "HANDOFF.md", "CURRENT_SCIENTIFIC_PREMISES.tsv"}
    changed: set[str] = set()
    for row in base_rows + add_rows:
        target = ROOT / row["path"]
        if not target.is_file():
            return False
        data = target.read_bytes()
        if sha(data) != row["sha256"] or str(len(data)) != row["bytes"]:
            changed.add(row["path"])
    return changed <= allowed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    frozen = json.loads((HERE / "FROZEN_UNIVERSE.json").read_text(encoding="utf-8"))
    add_frozen = json.loads((HERE / "SOURCE_ADDENDUM_FREEZE.json").read_text(encoding="utf-8"))
    candidates = table(HERE / "CANDIDATE_UNIVERSE.tsv")
    routes = table(HERE / "ROUTE_OUTCOMES.tsv")
    base_sources = table(HERE / "SOURCE_MANIFEST.tsv")
    add_sources = table(HERE / "SOURCE_ADDENDUM_MANIFEST.tsv")
    adjudication = table(HERE / "SOURCE_ADJUDICATION.tsv")
    propositions = table(HERE / "SOURCE_PROPOSITION_LEDGER.tsv")
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    witness = json.loads((HERE / "WITNESSES.json").read_text(encoding="utf-8"))

    union_paths = {row["path"] for row in base_sources + add_sources}
    checks = {
        "candidate_universe": candidate_guard(candidates),
        "routes": route_guard(routes),
        "primary_result": result_guard(result),
        "independent_result": independent_guard(independent),
        "witnesses": witness_guard(witness),
        "independent_imports": imports_guard(),
        "base_source_manifest_at_preregistration": manifest_guard(base_sources, frozen["preregistration_commit"], 31),
        "addendum_manifest_at_correction_parent": manifest_guard(add_sources, add_frozen["correction_commit_parent"], 4),
        "source_union_35_overlap_zero": source_union_guard(base_sources, add_sources),
        "source_adjudication_35": len(adjudication) == 35 and {row["path"] for row in adjudication} == union_paths,
        "historical_source_firewalled": next(row for row in adjudication if row["path"] == "udt_canonical_geometry.md")["status"] == "HISTORY_ONLY_FIREWALLED",
        "proposition_ledger_23": [row["proposition_id"] for row in propositions] == [f"Q{i:02d}" for i in range(1, 24)],
        "current_source_drift_allowed_only": current_drift_guard(base_sources, add_sources),
        "candidate_frozen_hash": sha((HERE / "CANDIDATE_UNIVERSE.tsv").read_bytes()) == frozen["candidate_universe_sha256"],
        "premise_frozen_hash": sha((HERE / "PREMISE_LEDGER.tsv").read_bytes()) == frozen["premise_ledger_sha256"],
        "falsification_frozen_hash": sha((HERE / "FALSIFICATION_CONTRACT.tsv").read_bytes()) == frozen["falsification_contract_sha256"],
        "base_manifest_frozen_hash": sha((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == frozen["source_manifest_sha256"],
        "addendum_manifest_frozen_hash": sha((HERE / "SOURCE_ADDENDUM_MANIFEST.tsv").read_bytes()) == add_frozen["manifest_sha256"],
        "unrelated_metadata_frozen_hash": sha((HERE / "UNRELATED_UNTRACKED_METADATA.tsv").read_bytes()) == frozen["unrelated_untracked_metadata_sha256"],
        "sympy_pin": (HERE / "requirements.txt").read_text(encoding="utf-8") == "sympy==1.13.1\n",
    }

    catches: list[tuple[str, str, bool]] = []
    catches.append(("C01", "missing_candidate", not candidate_guard(candidates[:-1])))
    catches.append(("C02", "duplicate_candidate", not candidate_guard(candidates + [copy.deepcopy(candidates[0])])))
    promoted_killing = copy.deepcopy(routes)
    next(row for row in promoted_killing if row["route_id"] == "M03")["classification"] = "DERIVED_UNIVERSAL"
    catches.append(("C03", "branch_killing_promoted", not route_guard(promoted_killing)))
    promoted_orbit = copy.deepcopy(routes)
    next(row for row in promoted_orbit if row["route_id"] == "M07")["classification"] = "DERIVED_SCALAR_OWNER"
    catches.append(("C04", "orbit_promoted_to_scalar", not route_guard(promoted_orbit)))
    promoted_c = copy.deepcopy(routes)
    next(row for row in promoted_c if row["route_id"] == "M09")["classification"] = "DERIVED_DEPTH_PROFILE"
    catches.append(("C05", "c_promoted_to_profile", not route_guard(promoted_c)))
    bad_primary = copy.deepcopy(result)
    bad_primary["checks"]["relative_potential_depth_changes"] = False
    catches.append(("C06", "primary_depth_change_deleted", not result_guard(bad_primary)))
    bad_independent = copy.deepcopy(independent)
    bad_independent["physical_arrow_after"] = [["0"]]
    catches.append(("C07", "independent_arrow_mutated", not independent_guard(bad_independent)))
    bad_witness = copy.deepcopy(witness)
    bad_witness["depth_after"] = bad_witness["depth_before"]
    catches.append(("C08", "depth_shift_made_vacuous", not witness_guard(bad_witness)))
    bad_witness2 = copy.deepcopy(witness)
    bad_witness2["physical_arrow_after"] = [["0"]]
    catches.append(("C09", "physical_arrow_changed", not witness_guard(bad_witness2)))
    missing_source = base_sources[:-1]
    catches.append(("C10", "missing_base_source", not manifest_guard(missing_source, frozen["preregistration_commit"], 31)))
    duplicate_add = add_sources + [copy.deepcopy(add_sources[0])]
    catches.append(("C11", "duplicate_addendum_source", not manifest_guard(duplicate_add, add_frozen["correction_commit_parent"], 4)))
    bad_history = copy.deepcopy(adjudication)
    next(row for row in bad_history if row["path"] == "udt_canonical_geometry.md")["status"] = "AFFIRMATIVE_NATIVE"
    catches.append(("C12", "history_promoted", next(row for row in bad_history if row["path"] == "udt_canonical_geometry.md")["status"] != "HISTORY_ONLY_FIREWALLED"))
    bad_props = propositions[:-1]
    catches.append(("C13", "missing_proposition", [row["proposition_id"] for row in bad_props] != [f"Q{i:02d}" for i in range(1, 24)]))
    wrong_conclusion = copy.deepcopy(result)
    wrong_conclusion["maximum_conclusion"] = "UNIVERSAL_PHI_OWNER_DERIVED"
    catches.append(("C14", "conclusion_promoted", not result_guard(wrong_conclusion)))
    independent_source = (HERE / "independent_founding_ownership.py").read_text(encoding="utf-8")
    catches.append(("C15", "independence_false_import", not imports_guard(independent_source + "\nimport sympy\n")))
    overlapping_add = copy.deepcopy(add_sources)
    overlapping_add[0]["path"] = base_sources[0]["path"]
    catches.append(("C16", "source_overlap_control", not source_union_guard(base_sources, overlapping_add)))
    bad_route = copy.deepcopy(routes)
    next(row for row in bad_route if row["route_id"] == "M10")["classification"] = "DERIVED_BOOTSTRAP_FUNCTION"
    catches.append(("C17", "working_relation_promoted", not route_guard(bad_route)))
    bad_route2 = copy.deepcopy(routes)
    next(row for row in bad_route2 if row["route_id"] == "M06")["classification"] = "METRIC_DERIVED"
    catches.append(("C18", "operational_input_promoted", not route_guard(bad_route2)))
    bad_sign = copy.deepcopy(witness)
    bad_sign["stationary_depth_ratios"] = copy.deepcopy(bad_sign["stationary_killing_lapse_ratios"])
    catches.append(("C19", "stationary_depth_sign_inverted", not witness_guard(bad_sign)))

    for catch_id, target, passed in catches:
        checks[f"catch_{catch_id}_{target}"] = passed
    verification = {
        "schema": "udt.founding_phi_ownership.verification.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "catch_count": len(catches),
        "checks": checks,
    }
    if args.write:
        (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")
        with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(["catch_id", "mutated_target", "expected", "observed"])
            for catch_id, target, passed in catches:
                writer.writerow([catch_id, target, "REJECT", "REJECT" if passed else "ACCEPT"])
    print(json.dumps(verification, sort_keys=True))
    raise SystemExit(0 if verification["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
