#!/usr/bin/env python3
"""Fail-closed self-consistency/regression verifier for the native Hopfion topology audit."""

from __future__ import annotations

import argparse
import ast
import copy
import csv
import hashlib
import json
import pathlib
import platform
import re
import subprocess
import sys
import tempfile
from typing import Any

import sympy as sp


EXPECTED_STATUS = {
    "T01": "NO_HOPF_SECTOR_FROM_SCALAR_ALONE",
    "T02": "CONDITIONAL_CANDIDATE_NOT_GENERIC",
    "T03": "CONDITIONAL_DERIVED_FIBER",
    "T04": "OPEN",
    "T05": "WORKING_POSIT_REOPENED",
    "T06": "CONDITIONAL_HOPF_DOMAIN_AVAILABLE",
    "T07": "OPEN",
    "T08": "FULL_3D_HOPF_CAPABLE",
    "T09": "OBSERVED_CARRIER_CONDITIONAL",
    "T10": "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
    "T11": "UNAVAILABLE_FROM_REGISTERED_FOUNDATION",
    "T12": "EXISTING_3D_HOPFION_NOT_MISSED_HOPF_STRUCTURE_CARRIER_CONDITIONAL",
}

BASE = "28628be883dd37b0982dfb8ceeb41e46f1aa0d9b"
FILENAME_RE = re.compile(r"hopf|skyr|topolog|winding|charge|carrier|nonull|(^|[/_.-])s2([/_.-]|$)", re.I)
TEXT_RE = r"Hopf|pi_3|S\^3|S\^2|Skyrme|winding|topological charge|boundary|compactif|carrier"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def read_tsv(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_ledger(rows: list[dict[str, str]]) -> None:
    if len(rows) != 12:
        raise AssertionError(f"ledger rows {len(rows)} != 12")
    ids = [row["claim_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate claim identity")
    if set(ids) != set(EXPECTED_STATUS):
        raise AssertionError("missing or extra claim identity")
    for row in rows:
        if row["status"] != EXPECTED_STATUS[row["claim_id"]]:
            raise AssertionError(f"status promotion/mutation {row['claim_id']}: {row['status']}")
        if not row["load_bearing_basis"] or not row["dependency_or_limit"] or not row["maximum_claim"]:
            raise AssertionError(f"incomplete premise row {row['claim_id']}")


def validate_inventory(root: pathlib.Path, rows: list[dict[str, str]]) -> None:
    if len(rows) != 20:
        raise AssertionError(f"inventory rows {len(rows)} != 20")
    paths = [row["current_path"] for row in rows]
    if len(paths) != len(set(paths)):
        raise AssertionError("duplicate source inventory path")
    for row in rows:
        path = root / row["current_path"]
        if not path.is_file():
            raise AssertionError(f"missing source {row['current_path']}")
        if sha256(path) != row["sha256"]:
            raise AssertionError(f"source sha mismatch {row['current_path']}")
        if git(root, "hash-object", "--", row["current_path"]) != row["git_blob"]:
            raise AssertionError(f"source blob mismatch {row['current_path']}")
        if int(row["size_bytes"]) != path.stat().st_size:
            raise AssertionError(f"source size mismatch {row['current_path']}")


def validate_candidate_census(root: pathlib.Path, rows: list[dict[str, str]]) -> None:
    tracked = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE], cwd=root, text=True
    ).splitlines()
    filename_matches = {path for path in tracked if FILENAME_RE.search(path)}
    grep = subprocess.run(
        ["git", "grep", "-Il", "-E", TEXT_RE, BASE, "--"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if grep.returncode not in (0, 1):
        raise AssertionError(grep.stderr)
    prefix = BASE + ":"
    text_matches = {
        line[len(prefix):] if line.startswith(prefix) else line
        for line in grep.stdout.splitlines() if line
    }
    expected = filename_matches | text_matches
    actual = [row["path"] for row in rows]
    if len(actual) != len(set(actual)):
        raise AssertionError("duplicate candidate census path")
    if set(actual) != expected:
        raise AssertionError("candidate census does not equal preregistered discovery union")
    allowed = {
        "LOAD_BEARING_SOURCE",
        "EXCLUDED_HISTORICAL_OR_REORG",
        "EXCLUDED_FROZEN_PACKAGE_COMPANION",
        "EXCLUDED_OPAQUE_OR_NON_TEXT_ROLE",
        "SUPPORTING_NOT_LOAD_BEARING",
    }
    for row in rows:
        if row["base"] != BASE or row["disposition"] not in allowed or not row["reason"]:
            raise AssertionError(f"invalid candidate disposition {row['path']}")
        if git(root, "rev-parse", f"{BASE}:{row['path']}") != row["git_blob"]:
            raise AssertionError(f"candidate blob mismatch {row['path']}")


def validate_source_semantics(root: pathlib.Path, overrides: dict[str, str] | None = None) -> None:
    overrides = overrides or {}
    def source(rel: str) -> str:
        return overrides.get(rel, (root / rel).read_text(encoding="utf-8"))

    c1 = source("UDT_NATIVE_ACTION_COLD_PACKET.md")
    required_c1 = [
        "**WORKING / POSIT**",
        "The round `S^2` carrier is not fixed",
        "\\mathbf n:\\mathbb R^3\\to S^2",
        "This three-dimensional functional supplies no unique time-derivative sector",
        "does not select the action's boundary functional",
        "every other field, or a conserved charge",
    ]
    if any(token not in c1 for token in required_c1):
        raise AssertionError("C1 carrier/open-boundary disclosure missing")

    clarification = source("UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")
    if "HISTORICAL WORKING POSIT, now REOPENED" not in clarification:
        raise AssertionError("owner carrier reopening missing")

    line_report = source("reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md")
    for token in ("does not choose one line", "CIRCULAR_OR_EXTRA_FIELD", "UNDERDETERMINED"):
        if token not in line_report:
            raise AssertionError("line-selector limit missing")

    fs = source("hopfion_arc_scripts_2026-07-05/fs_hopfion.py")
    ast.parse(fs)
    for token in (
        "torch.meshgrid(x, x, x, indexing='ij')",
        "def hopf_seed",
        "def toroidal_seed",
        "def hopf_charge",
        "X, Y, Z",
        "range(3)",
        "S^3->S^2",
    ):
        if token not in fs:
            raise AssertionError(f"3D Hopf representation token missing: {token}")

    no_null = source("noNull_energy.py")
    ast.parse(no_null)
    for token in ("_ORIENTS", "s0, s1, s2", "range(3)", "same continuum functional"):
        if token not in no_null:
            raise AssertionError(f"no-null 3D/operator token missing: {token}")

    h3 = source("node_H3_hopfion_solve_results.md")
    for token in ("localized torus", "0.985", "0.992", "N=256", "Q_H=1"):
        if token not in h3:
            raise AssertionError(f"H3 evidence disclosure missing: {token}")


def validate_algebra(result: dict[str, Any]) -> None:
    checks = result["checks"]
    exact = {
        "canonical_hopf_charge": "1",
        "chern_simons_integral": "-4*pi**2",
        "unit_s2_area_chern_simons_integral": "-16*pi**2",
        "unit_s2_area_hopf_charge": "1",
        "hedgehog_s2_flux": "4*pi",
        "canonical_hopf_charge_is_one": True,
        "unit_s2_area_hopf_charge_is_one": True,
        "hopf_target_identity_zero": True,
        "normalized_gradient_frobenius_zero": True,
        "projective_null_fiber_is_s2": True,
        "csn_preserves_null_condition": True,
    }
    for key, expected in exact.items():
        if checks.get(key) != expected:
            raise AssertionError(f"algebra mismatch {key}: {checks.get(key)}")

    # Independent route: integrate the registered density directly and recompute the charge.
    eta = sp.symbols("eta", real=True)
    independent_integral = sp.integrate(-sp.sin(2 * eta), (eta, 0, sp.pi / 2)) * (2 * sp.pi) ** 2
    if sp.simplify(independent_integral + 4 * sp.pi**2) != 0:
        raise AssertionError("independent Hopf integral failed")
    if sp.simplify(-independent_integral / (4 * sp.pi**2) - 1) != 0:
        raise AssertionError("independent Hopf charge failed")


def validate_report(report: str) -> None:
    required = [
        "EXISTING_3D_HOPFION_NOT_MISSED",
        "CARRIER_CONDITIONAL_HOPF_SECTOR_AVAILABLE",
        "projective null-line cone",
        "celestial topological/conformal `S2`",
        "a sphere fiber is not a chosen field",
        "raw fields were not freshly replayed here",
        "No native carrier or Hopfion has been derived from C0/C1",
        "Global/time-live persistence",
        "OPEN",
    ]
    if any(token not in report for token in required):
        raise AssertionError("report scope/disclosure missing")
    forbidden = [
        "raw field freshly verified",
        "NATIVE_HOPF_SECTOR_DERIVED is accepted",
        "co-presence proves",
        "the metric uniquely selects the S2 carrier",
    ]
    if any(token in report for token in forbidden):
        raise AssertionError("report contains forbidden promotion")


def expect_reject(name: str, fn) -> dict[str, str]:
    try:
        fn()
    except Exception as exc:  # catch-proof records the fail-closed rejection
        return {"name": name, "result": "PASS", "caught": type(exc).__name__}
    raise AssertionError(f"catch-proof failed to reject: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    root = package.parent

    ledger = read_tsv(package / "TOPOLOGY_STATUS_LEDGER.tsv")
    inventory = read_tsv(package / "SOURCE_INVENTORY.tsv")
    candidates = read_tsv(package / "CANDIDATE_CENSUS.tsv")
    derivation = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")

    validate_ledger(ledger)
    validate_inventory(root, inventory)
    validate_candidate_census(root, candidates)
    validate_source_semantics(root)
    validate_algebra(derivation)
    validate_report(report)

    # Replay the exact algebra script into an isolated temporary path; this is a deterministic
    # computation replay, not an independent semantic/topology derivation.
    with tempfile.TemporaryDirectory(prefix="hopf_topology_replay_") as temp_dir:
        replay_path = pathlib.Path(temp_dir) / "DERIVATION_RESULT.json"
        process = subprocess.run(
            [sys.executable, str(package / "derive_topology.py"), "--output", str(replay_path)],
            cwd=root,
            text=True,
            capture_output=True,
        )
        if process.returncode != 0 or process.stderr != "":
            raise AssertionError("derivation replay failed")
        if replay_path.read_bytes() != (package / "DERIVATION_RESULT.json").read_bytes():
            raise AssertionError("derivation replay output mismatch")

    catches = []
    for claim_id, bad_status, name in [
        ("T05", "NATIVE_DERIVED", "carrier_posit_promoted_native"),
        ("T07", "DERIVED_PHYSICAL_BOUNDARY", "open_physical_boundary_promoted"),
        ("T08", "RADIAL_ONLY", "full_3d_representation_demoted"),
        ("T03", "DERIVED_UNCONDITIONAL", "null_s2_condition_dropped"),
        ("T04", "DERIVED_SECTION", "fiber_mislabeled_selected_section"),
        ("T09", "FRESH_RAW_FIELD_VERIFIED", "banked_configuration_overclaimed"),
    ]:
        mutated = copy.deepcopy(ledger)
        next(row for row in mutated if row["claim_id"] == claim_id)["status"] = bad_status
        catches.append(expect_reject(name, lambda rows=mutated: validate_ledger(rows)))

    duplicate_inventory = copy.deepcopy(inventory) + [copy.deepcopy(inventory[0])]
    catches.append(expect_reject("duplicate_source_inventory", lambda: validate_inventory(root, duplicate_inventory)))
    bad_inventory = copy.deepcopy(inventory)
    bad_inventory[0]["sha256"] = "0" * 64
    catches.append(expect_reject("source_hash_mutation", lambda: validate_inventory(root, bad_inventory)))
    missing_candidate = copy.deepcopy(candidates)[1:]
    catches.append(expect_reject("candidate_census_missing_path", lambda: validate_candidate_census(root, missing_candidate)))

    bad_c1 = (root / "UDT_NATIVE_ACTION_COLD_PACKET.md").read_text(encoding="utf-8").replace("**WORKING / POSIT**", "**DERIVED**")
    catches.append(expect_reject(
        "carrier_provenance_disclosure_removed",
        lambda: validate_source_semantics(root, {"UDT_NATIVE_ACTION_COLD_PACKET.md": bad_c1}),
    ))
    fs = (root / "hopfion_arc_scripts_2026-07-05/fs_hopfion.py").read_text(encoding="utf-8")
    catches.append(expect_reject(
        "three_dimensional_mesh_removed",
        lambda: validate_source_semantics(root, {"hopfion_arc_scripts_2026-07-05/fs_hopfion.py": fs.replace("torch.meshgrid(x, x, x, indexing='ij')", "torch.meshgrid(x, x, indexing='ij')")}),
    ))
    bad_derivation = copy.deepcopy(derivation)
    bad_derivation["checks"]["canonical_hopf_charge"] = "0"
    catches.append(expect_reject("hopf_charge_mutation", lambda: validate_algebra(bad_derivation)))
    bad_report = report.replace("raw fields were not freshly replayed here", "raw field freshly verified")
    catches.append(expect_reject("raw_field_replay_overclaim", lambda: validate_report(bad_report)))

    result = {
        "status": "PASS_SELF_CONSISTENCY",
        "verification_class": "DETERMINISTIC_REPLAY_REGRESSION_AND_CATCH_PROOFS; NOT_EXTERNAL_SEMANTIC_INDEPENDENCE",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "exact_checks": {
            "ledger_rows": len(ledger),
            "source_inventory_rows": len(inventory),
            "candidate_census_rows": len(candidates),
            "source_hashes_and_blobs": len(inventory),
            "algebra_load_bearing_checks": 11,
            "derivation_script_replay": "PASS_BYTE_IDENTICAL",
            "source_token_regression_groups": 6,
            "report_scope_gate": "PASS",
        },
        "catch_proofs": catches,
        "catch_proof_count": len(catches),
        "preregistration_sha256": sha256(package / "PREREGISTRATION.md"),
        "derivation_result_sha256": sha256(package / "DERIVATION_RESULT.json"),
        "source_inventory_sha256": sha256(package / "SOURCE_INVENTORY.tsv"),
        "candidate_census_sha256": sha256(package / "CANDIDATE_CENSUS.tsv"),
        "status_ledger_sha256": sha256(package / "TOPOLOGY_STATUS_LEDGER.tsv"),
        "audit_report_sha256": sha256(package / "AUDIT_REPORT.md"),
        "verdict": "EXISTING_3D_HOPFION_NOT_MISSED; HOPF_STRUCTURE_CARRIER_CONDITIONAL; METRIC_NULL_S2_FIBER_CONDITIONAL; SECTION_AND_BOUNDARY_SELECTOR_OPEN",
    }
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("VERIFIER PASS_SELF_CONSISTENCY")
    print(f"source_inventory={len(inventory)}/20 candidates={len(candidates)} ledger={len(ledger)}/12 algebra=11/11 replay=PASS")
    print(f"catch_proofs={len(catches)}/{len(catches)}")
    print(result["verdict"])


if __name__ == "__main__":
    main()
