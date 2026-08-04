#!/usr/bin/env python3
"""Fail-closed verifier for the factorized whole-spacetime skeleton audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

OBJECT_IDS = {f"O{i:02d}" for i in range(1, 34)}
SYMBOL_IDS = {f"V{i:02d}" for i in range(1, 41)}
ENTRY_IDS = {*(f"F{i:02d}" for i in range(1, 5)), *(f"D{i:02d}" for i in range(1, 5)), *(f"G{i:02d}" for i in range(1, 9)), *(f"C{i:02d}" for i in range(1, 8)), "A01", *(f"L{i:02d}" for i in range(1, 8))}
OPEN_IDS = {f"L{i:02d}" for i in range(1, 9)}
REDUCTION_IDS = {f"R{i:02d}" for i in range(1, 12)}
CONSTRAINT_CLASSES = {"DEFINED", "IDENTITY_CONSTRAINED", "CONDITIONAL_EQUATION", "OPEN_LAW_SLOT", "OBSERVATIONAL_ANCHOR"}
ENTRY_CLASSES = {"FOUNDED_IDENTITY", "DEFINITION", "GEOMETRIC_IDENTITY", "CONDITIONAL_EQUATION", "OBSERVATIONAL_ANCHOR", "OPEN_LAW_SLOT"}


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


def unique_exact(rows: list[dict[str, str]], field: str, expected: set[str]) -> None:
    values = [row[field] for row in rows]
    assert len(values) == len(set(values)), f"duplicate {field}"
    assert set(values) == expected, f"{field} coverage mismatch"


def sources(rows: list[dict[str, str]], field: str, manifest_paths: set[str]) -> None:
    for row in rows:
        source = row[field]
        assert source in manifest_paths, f"unmanifested source: {source}"
        assert (ROOT / source).is_file(), f"missing source: {source}"


def validate_objects(rows: list[dict[str, str]], manifest_paths: set[str]) -> None:
    unique_exact(rows, "object_id", OBJECT_IDS)
    sources(rows, "controlling_source", manifest_paths)
    by = {row["object_id"]: row for row in rows}
    assert by["O06"]["status"] == "NATIVE_DERIVED_ALGEBRA__PHYSICAL_ASSIGNMENT_OPEN"
    assert by["O09"]["status"] == "OPEN_GLOBAL_REALIZATION"
    assert by["O12"]["status"] == "DERIVED_POINTWISE_CLASS"
    assert by["O28"]["status"] == "OPEN_GLOBAL_CONFIGURATION_DOMAIN"
    assert by["O29"]["status"] == "OPEN_LAW_SLOT"
    assert by["O31"]["status"] == "WORKING_ON_SHELL_ONLY"
    assert by["O33"]["status"] == "OPEN_DOWNSTREAM"


def validate_symbols(rows: list[dict[str, str]], manifest_paths: set[str]) -> None:
    unique_exact(rows, "slot_id", SYMBOL_IDS)
    sources(rows, "controlling_source", manifest_paths)
    assert all(row["constraint_class"] in CONSTRAINT_CLASSES for row in rows)
    by = {row["slot_id"]: row for row in rows}
    assert by["V04"]["local_status"] == "NATIVE_DERIVED_ALGEBRA__PHYSICAL_ASSIGNMENT_OPEN"
    assert by["V04"]["selected_physical_dof_count"] == "ZERO_INDEPENDENT_EXTRA_FIELD_DIRECTIONS"
    assert by["V11"]["selected_physical_dof_count"] == "3_CHART_DIRECTIONS_NOT_MODE_COUNT"
    assert by["V13"]["selected_physical_dof_count"] == "4_CHART_DIRECTIONS_NOT_MODE_COUNT"
    assert int(by["V11"]["selected_physical_dof_count"].split("_", 1)[0]) + int(by["V13"]["selected_physical_dof_count"].split("_", 1)[0]) == 7
    assert by["V14"]["selected_physical_dof_count"] == "SEVEN_EXTENSION_CHART_DIRECTIONS_NOT_MODE_COUNT"
    assert by["V35"]["constraint_class"] == "OPEN_LAW_SLOT" and by["V35"]["local_status"] == "ABSENT"
    assert not any(row["selected_physical_dof_count"].startswith(("7_PROPAGATING", "SEVEN_PROPAGATING")) for row in rows)


def validate_identities(rows: list[dict[str, str]], manifest_paths: set[str]) -> None:
    unique_exact(rows, "entry_id", ENTRY_IDS)
    sources(rows, "controlling_source", manifest_paths)
    assert all(row["entry_class"] in ENTRY_CLASSES for row in rows)
    by = {row["entry_id"]: row for row in rows}
    assert by["F02"]["status"] == "DERIVED"
    assert by["G03"]["what_it_does_not_imply"] == "a native field equation"
    assert by["C05"]["entry_class"] == "CONDITIONAL_EQUATION" and "CONDITIONAL" in by["C05"]["status"]
    assert by["C06"]["status"] == "CONDITIONAL_NOT_SELECTED"
    assert by["C07"]["status"] == "CONDITIONAL_CARRIER_BRANCH"
    assert by["L03"]["entry_class"] == "OPEN_LAW_SLOT" and by["L03"]["status"] == "OPEN"


def validate_open(rows: list[dict[str, str]], manifest_paths: set[str]) -> None:
    unique_exact(rows, "slot_id", OPEN_IDS)
    sources(rows, "controlling_source", manifest_paths)
    by = {row["slot_id"]: row for row in rows}
    assert by["L03"]["status"] == "OPEN"
    assert by["L04"]["upstream_gate"] == "L03"
    assert "L03" in by["L05"]["upstream_gate"]
    assert by["L06"]["status"] == "WORKING_NOT_DERIVED"
    assert by["L08"]["status"] == "OPEN"


def validate_reductions(rows: list[dict[str, str]], manifest_paths: set[str]) -> None:
    unique_exact(rows, "reduction_id", REDUCTION_IDS)
    sources(rows, "controlling_source", manifest_paths)
    assert all(row["role"] == "CONSISTENCY_CHECK_ONLY" for row in rows)
    by = {row["reduction_id"]: row for row in rows}
    assert "unchanged transverse metric plus no mixing" == by["R02"]["premises_not_in_parent"]
    assert "stationarity" in by["R06"]["premises_not_in_parent"]
    assert "not selected universe" in by["R11"]["premises_not_in_parent"]


def validate_current_premises(rows: list[dict[str, str]]) -> None:
    by = {row["premise_id"]: row for row in rows}
    assert by["G01"]["current_status"] == "DERIVED_ADDITIVE_LOG_DEPTH_OF_RECIPROCAL_PAIR"
    assert by["G04"]["current_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED"
    assert by["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES"
    assert by["G09"]["current_status"] == "POSIT"
    assert by["G12"]["current_status"] == "WORKING_ON_SHELL_ADMISSIBILITY"
    assert by["G16"]["current_status"] == "OPEN"


def validate_manifest() -> set[str]:
    rows = table(HERE / "SOURCE_MANIFEST.tsv")
    listed = [line.strip() for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
    assert len(listed) == len(set(listed))
    assert [row["path"] for row in rows] == listed
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file()
        assert str(path.stat().st_size) == row["bytes"]
        assert sha(path) == row["sha256"]
        assert git_blob(row["path"]) == row["git_blob"]
    return set(listed)


def validate_sparse_results() -> None:
    production = json.loads((HERE / "SPARSE_SKELETON_RESULT.json").read_text())
    independent = json.loads((HERE / "SPARSE_SKELETON_INDEPENDENT_RESULT.json").read_text())
    pin = (HERE / "requirements.txt").read_text().strip().split("==", 1)[1]
    assert production["status"] == "PASS" and production["check_count"] == 26
    assert len(production["checks"]) == 26 and set(production["checks"].values()) == {"PASS"}
    assert production["sympy_version"] == pin
    assert independent["status"] == "PASS" and independent["check_count"] == 15
    assert len(independent["checks"]) == 15 and set(independent["checks"].values()) == {"PASS"}
    assert independent["production_imported"] is False and independent["third_party_packages"] == []


def catch_proofs(objects, symbols, identities, opens, reductions, premises, manifest_paths):
    result = {}

    def must_fail(name, fn):
        try:
            fn()
        except (AssertionError, KeyError, ValueError):
            result[name] = "PASS"
        else:
            raise AssertionError(f"catch proof did not fail: {name}")

    must_fail("missing_object", lambda: validate_objects(objects[:-1], manifest_paths))
    must_fail("duplicate_symbol", lambda: validate_symbols(symbols + [dict(symbols[0])], manifest_paths))
    bad = [dict(row) for row in symbols]
    next(row for row in bad if row["slot_id"] == "V35")["constraint_class"] = "IDENTITY_CONSTRAINED"
    must_fail("native_law_disguised_as_identity", lambda: validate_symbols(bad, manifest_paths))
    bad = [dict(row) for row in symbols]
    next(row for row in bad if row["slot_id"] == "V14")["selected_physical_dof_count"] = "SEVEN_PROPAGATING_MODES"
    must_fail("chart_directions_promoted_to_modes", lambda: validate_symbols(bad, manifest_paths))
    bad = [dict(row) for row in identities]
    next(row for row in bad if row["entry_id"] == "C05")["status"] = "NATIVE_DERIVED"
    must_fail("conditional_Bach_promoted", lambda: validate_identities(bad, manifest_paths))
    bad = [dict(row) for row in reductions]
    next(row for row in bad if row["reduction_id"] == "R02")["role"] = "PARENT_SELECTOR"
    must_fail("spectator_reduction_promoted_to_selector", lambda: validate_reductions(bad, manifest_paths))
    bad = [dict(row) for row in reductions]
    next(row for row in bad if row["reduction_id"] == "R06")["premises_not_in_parent"] = ""
    must_fail("hidden_stationarity_control", lambda: validate_reductions(bad, manifest_paths))
    must_fail("missing_open_transition_slot", lambda: validate_open(opens[1:], manifest_paths))
    bad = [dict(row) for row in opens]
    next(row for row in bad if row["slot_id"] == "L04")["upstream_gate"] = "NONE"
    must_fail("time_live_before_native_law", lambda: validate_open(bad, manifest_paths))
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["premise_id"] == "G04")["active_use"] = "ACTIVE"
    must_fail("strong_CSN_reactivated", lambda: validate_current_premises(bad))
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["premise_id"] == "G09")["current_status"] = "DERIVED"
    must_fail("S2_carrier_promoted", lambda: validate_current_premises(bad))
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["premise_id"] == "G01")["current_status"] = "UNDEFINED_PLACEHOLDER"
    must_fail("founded_phi_demoted", lambda: validate_current_premises(bad))
    bad = [dict(row) for row in objects]
    next(row for row in bad if row["object_id"] == "O09")["status"] = "NATIVE_DERIVED_UNIQUE"
    must_fail("unique_complete_embedding_invented", lambda: validate_objects(bad, manifest_paths))
    return result


def main() -> None:
    required = [
        "WHOLE_SPACETIME_SKELETON.md", "OBJECT_GRAPH.tsv", "SYMBOL_AND_DOF_LEDGER.tsv",
        "IDENTITY_LAW_SEPARATION.tsv", "OPEN_EQUATION_SLOTS.tsv", "REDUCTION_MAP.tsv",
        "AUDIT_REPORT.md", "SOURCE_MANIFEST.tsv", "SPARSE_SKELETON_RESULT.json",
        "SPARSE_SKELETON_INDEPENDENT_RESULT.json", "IMPLEMENTATION_CORRECTION.md",
        "REPOSITORY_GATES.json", "REPOSITORY_TEST_STDOUT.txt",
        "UNRELATED_UNTRACKED_METADATA.tsv", "RUN_ENVIRONMENT.json",
    ]
    for name in required:
        assert (HERE / name).is_file(), f"missing deliverable: {name}"

    manifest_paths = validate_manifest()
    objects = table(HERE / "OBJECT_GRAPH.tsv")
    symbols = table(HERE / "SYMBOL_AND_DOF_LEDGER.tsv")
    identities = table(HERE / "IDENTITY_LAW_SEPARATION.tsv")
    opens = table(HERE / "OPEN_EQUATION_SLOTS.tsv")
    reductions = table(HERE / "REDUCTION_MAP.tsv")
    premises = table(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    validate_objects(objects, manifest_paths)
    validate_symbols(symbols, manifest_paths)
    validate_identities(identities, manifest_paths)
    validate_open(opens, manifest_paths)
    validate_reductions(reductions, manifest_paths)
    validate_current_premises(premises)
    validate_sparse_results()
    catches = catch_proofs(objects, symbols, identities, opens, reductions, premises, manifest_paths)

    result = {
        "schema": "udt-factorized-whole-spacetime-audit-verification-1.0",
        "status": "PASS",
        "object_rows": len(objects),
        "symbol_rows": len(symbols),
        "identity_law_rows": len(identities),
        "open_equation_slots": len(opens),
        "reduction_rows": len(reductions),
        "source_manifest_rows": len(manifest_paths),
        "production_sparse_checks": 26,
        "independent_rational_checks": 15,
        "catch_proofs": catches,
        "deliverable_sha256": {name: sha(HERE / name) for name in required},
        "maximum_conclusion": "COHERENT_FACTORIZED_CONFIGURATION_SKELETON_WITH_EXPLICIT_OPEN_LAW_SLOTS_ONLY",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
