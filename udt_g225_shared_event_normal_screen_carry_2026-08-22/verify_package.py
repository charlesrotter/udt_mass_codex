#!/usr/bin/env python3
"""Fail-closed aggregate verifier for G225 with true no-write replay."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.resolve()
SOURCE_ROOT = (REPO / "frozen_sources").resolve() if (REPO / "frozen_sources").is_dir() else REPO
LANDING = (
    "METRIC_AND_SHARED_CLOCK_DEFINE_POSITIVE_INCIDENT_SCREEN_PLANES"
    "__CANONICAL_LEAST_TURNING_DIRECT_SCREEN_ISOMETRY_EXISTS_OFF_ANTIPODES"
    "__THREE_DIRECTION_COMPOSITION_RETAINS_FINITE_O2_HOLONOMY_AND_NO_GLOBAL_ENDPOINT_ONLY_FLAT_SCREEN_CARRY_EXISTS"
    "__G188_JACOBI_TRANSPORT_REMAINS_SEPARATE"
)

REQUIRED = (
    "MAP.md",
    "OBSERVATION.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_shared_event_normal_screen_carry.py",
    "verify_shared_event_normal_screen_independent.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CONTROL_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "verify_package.py",
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def load_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def validate_payloads(production: dict, independent: dict, catch: dict, final: dict) -> None:
    require(production["status"] == "PASS", "production status")
    require(production["symbolic_checks"] == 39, "symbolic count")
    require(production["screen_planes_metric_derived"] is True, "screen planes")
    require(production["least_turning_direct_isometry_nonantipodal"] is True, "direct isometry")
    require(not production["direct_isometry_exact_vertex_cocycle"], "false endpoint cocycle")
    require(production["finite_composition_holonomy"] is True, "holonomy")
    require(not production["antipodal_least_turning_extension_unique"], "antipodal promotion")
    require(not production["global_endpoint_only_flat_screen_carry"], "global flat carry")
    require(production["G224_scalar_carry_retained"] is True, "G224 scalar")
    require(not production["G188_Jacobi_replaced"], "G188 collapse")
    require(not production["pointwise_direct_map_physical_transport_selected"], "physical transport")
    require(not production["independent_direct_relation_constrained"], "direct relation")
    require(not production["universal_null_protocol_selected"], "protocol selection")
    require(not production["physical_history_selected"], "history selection")
    require(production["landing"] == LANDING, "production landing")

    require(independent["status"] == "PASS", "independent status")
    require(independent["seed"] == 2250822, "seed")
    require(independent["cases"] == 20000, "case count")
    require(independent["exact_rational_assertions"] == 580013, "assertion count")
    require(independent["nontrivial_composition_defects"] == 19922, "defect count")
    require(not independent["production_code_imported"], "production imported")
    require(not independent["sympy_imported"], "SymPy imported")
    require(independent["fixed_great_circle_control"] is True, "great-circle control")
    require(independent["fixed_octant_holonomy"] is True, "octant control")
    require(independent["antipodal_least_turning_nonuniqueness"] is True, "antipodal control")
    require(independent["passive_O3_covariance"] is True, "covariance control")
    require(independent["G224_scalar_composition"] is True, "scalar control")
    require(independent["landing"] == LANDING, "independent landing")

    require(catch["status"] == "PASS", "catch status")
    require(catch["payload_mutations_rejected"] == 21, "payload mutation count")
    require(catch["algorithm_mutations_rejected"] == 4, "algorithm mutation count")
    require(catch["total_contract_mutations"] == 25, "total mutation count")

    require(final["status"] == "PASS", "final status")
    require(
        final["grade"] == "DERIVED_CONDITIONAL__INTERNALLY_VERIFIED__FRESH_EXTERNAL_REVIEW_PENDING",
        "final grade",
    )
    require(final["preregistration_commit"] == "24a8f8a4", "preregistration commit")
    require(final["source_count"] == 9, "source count")
    require(final["symbolic_checks"] == 39, "final symbolic count")
    require(final["independent_cases"] == 20000, "final case count")
    require(final["exact_rational_assertions"] == 580013, "final assertion count")
    require(final["nontrivial_composition_defects"] == 19922, "final defect count")
    require(final["contract_mutations"] == 25, "final mutation count")
    require(final["screen_planes_metric_derived"] is True, "final screen planes")
    require(final["least_turning_direct_isometry_nonantipodal"] is True, "final direct isometry")
    require(final["finite_composition_holonomy"] is True, "final holonomy")
    require(not final["global_endpoint_only_flat_screen_carry"], "final global flat carry")
    require(not final["antipodal_least_turning_extension_unique"], "final antipodal promotion")
    require(final["G224_scalar_carry_retained"] is True, "final scalar")
    require(not final["G188_Jacobi_replaced"], "final Jacobi collapse")
    require(not final["pointwise_direct_map_physical_transport_selected"], "final physical transport")
    require(not final["independent_direct_relation_constrained"], "final direct relation")
    require(not final["universal_null_protocol_selected"], "final protocol")
    require(not final["physical_history_selected"], "final history")
    require(final["fresh_external_review"] == "PENDING", "external review status")
    require(final["read_only_replay"] is True, "read-only replay")
    require(final["manifest_path_containment"] is True, "manifest containment")
    require(final["landing"] == LANDING, "final landing")


def manifest_rows() -> list[dict[str, str]]:
    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_manifest() -> list[Path]:
    rows = manifest_rows()
    require(len(rows) == 9, "manifest source count")
    paths: list[Path] = []
    for row in rows:
        candidate = (SOURCE_ROOT / row["path"]).resolve()
        require(candidate.is_relative_to(SOURCE_ROOT), "manifest path escape")
        require(candidate.is_file(), f"missing source: {row['path']}")
        digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        require(digest == row["sha256"], f"source hash mismatch: {row['path']}")
        paths.append(candidate)
    return paths


def tree_hashes(source_paths: list[Path]) -> dict[str, str]:
    paths = [path for path in ROOT.iterdir() if path.is_file()]
    paths.extend(source_paths)
    return {
        str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(set(paths), key=lambda item: str(item))
    }


def replay(script: str, timeout: int = 120) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return json.loads(completed.stdout)


def main() -> None:
    for name in REQUIRED:
        require((ROOT / name).is_file(), f"missing package evidence: {name}")

    sources = validate_manifest()
    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    catch = load_json("CATCH_PROOF_RESULT.json")
    final = load_json("VERIFICATION_RESULT.json")
    validate_payloads(production, independent, catch, final)

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in (*LANDING.split("__"), "hairy-ball", "antipodal", "G188", "G224"):
        require(token in exact, f"exact derivation lacks {token}")
    for token in LANDING.split("__"):
        require(token in audit, f"audit landing segment missing: {token}")
    require("24a8f8a4" in audit, "audit preregistration missing")
    require("B_LOCAL_DIRECT_ISOMETRY_WITH_NONTRIVIAL_COMPOSITION_HOLONOMY" in exact, "outcome absent")
    require("No alternative will be added" in prereg, "frozen alternatives absent")

    before = tree_hashes(sources)
    require(replay("derive_shared_event_normal_screen_carry.py") == production, "production replay drift")
    require(
        replay("verify_shared_event_normal_screen_independent.py") == independent,
        "independent replay drift",
    )
    require(replay("run_catch_proofs.py") == catch, "catch replay drift")
    after = tree_hashes(sources)
    require(after == before, "replay wrote evidence bytes")

    print(
        "PASS: G225 package; 9 sources; 39 symbolic checks; 20,000 independent cases; "
        "580,013 exact-rational assertions; 19,922 nontrivial defects; 25 contract mutations; "
        "true no-write replay"
    )


if __name__ == "__main__":
    main()
