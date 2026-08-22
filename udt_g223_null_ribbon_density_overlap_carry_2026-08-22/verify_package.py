#!/usr/bin/env python3
"""Verify the complete bounded G223 evidence package and frozen sources."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = (
    "METRIC_OWNS_NONDEGENERATE_CLOCK_RULER_LINE_PAIRING_ON_SUPPLIED_NULL_RIBBON"
    "__RULER_DENSITY_HAS_EXACT_INVERSE_CLOCK_OVERLAP_WEIGHT"
    "__LOCAL_FIBER_COORDINATE_EXISTS_BUT_GLOBAL_SCALAR_NEEDS_TRIVIALIZATION_AND_CECH_PERIOD_GATES"
    "__G216_CLOCK_COMPOSITION_DOES_NOT_BY_ITSELF_SUPPLY_CROSS_RIBBON_VERTICAL_CARRY"
)
REQUIRED = (
    "MAP.md",
    "OBSERVATION.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_null_ribbon_density_carry.py",
    "verify_null_ribbon_density_independent.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CONTROL_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "VERIFICATION_RESULT.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "FRESH_ADVERSARIAL_REVIEW.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_IMPLEMENTATION.md",
    "REPAIR_FOLLOWUP_REVIEW_REQUEST.md",
    "build_review_intake.py",
)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hashes() -> dict[str, str]:
    paths = [p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            paths.append(REPO / row["path"])
    return {str(p.resolve()): sha256(p) for p in paths}


def contained_source_path(raw: str) -> Path:
    rel = Path(raw)
    require(not rel.is_absolute(), f"absolute source path: {raw}")
    require(".." not in rel.parts, f"parent-escaping source path: {raw}")
    path = (REPO / rel).resolve()
    require(path.is_relative_to(REPO.resolve()), f"source escapes verifier root: {raw}")
    return path


def validate_payloads(derivation: dict[str, Any], independent: dict[str, Any], final: dict[str, Any]) -> None:
    require(derivation["status"] == "PASS", "derivation status")
    require(derivation["symbolic_checks"] == 21, "symbolic count")
    require(derivation["metric_mixed_pairing_canonical"] is True, "mixed pairing")
    require(derivation["vertical_density_inverse_clock_weight"] is True, "clock weight")
    require(derivation["oriented_area_form_invariant"] is True, "area form")
    require(derivation["chosen_full_representative_closedness_invariant"] is False, "closedness type")
    require(derivation["local_interval_fiber_coordinate_exists"] is True, "local coordinate")
    require(derivation["global_scalar_coordinate_unconditional"] is False, "global scalar promotion")
    require(derivation["G216_clock_chain_supplies_vertical_gluing"] is False, "vertical gluing promotion")
    require(derivation["landing"] == LANDING, "derivation landing")

    require(independent["status"] == "PASS", "independent status")
    require(independent["cases"] == 20000, "independent cases")
    require(independent["exact_rational_assertions"] == 361001, "assertion count")
    require(independent["same_metric_closedness_counterexample"] is True, "closedness counterexample")
    require(independent["local_fiber_integration_control"] is True, "fiber integration")
    require(independent["clock_weight_cocycle"] is True, "clock cocycle")
    require(independent["cross_ribbon_vertical_gluing_derived"] is False, "cross-ribbon promotion")

    require(final["status"] == "PASS", "final status")
    require(final["preregistration_commit"] == "f48c7d6b", "preregistration commit")
    require(final["source_count"] == 7, "source count")
    require(final["symbolic_checks"] == 21, "final symbolic count")
    require(final["independent_cases"] == 20000, "final case count")
    require(final["exact_rational_assertions"] == 361001, "final assertion count")
    require(final["contract_mutations"] == 14, "mutation count")
    require(final["metric_mixed_pairing_canonical"] is True, "final mixed pairing")
    require(final["vertical_density_inverse_clock_weight"] is True, "final clock weight")
    require(final["oriented_area_form_invariant"] is True, "final area")
    require(final["chosen_full_representative_closedness_invariant"] is False, "final closedness")
    require(final["local_interval_fiber_coordinate_exists"] is True, "final local coordinate")
    require(final["global_scalar_coordinate_unconditional"] is False, "final global scalar")
    require(final["G216_clock_chain_supplies_vertical_gluing"] is False, "final gluing")
    require(final["fresh_external_review"] == "ACCEPT_WITH_REPAIRS", "review grade")
    require(final["repair_followup_review"] == "PENDING_AUTHORIZATION", "repair review grade")
    require(final["read_only_replay"] is True, "read-only replay")
    require(final["manifest_path_containment"] is True, "manifest containment")
    require(final["independent_fiber_control_nonvacuous"] is True, "fiber control")
    require(final["landing"] == LANDING, "final landing")


def main() -> None:
    for name in REQUIRED:
        require((ROOT / name).is_file(), f"missing package file: {name}")

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    require(len(rows) == 7, "source manifest count")
    for row in rows:
        path = contained_source_path(row["path"])
        require(path.is_file(), f"missing source: {row['path']}")
        require(sha256(path) == row["sha256"], f"source hash mismatch: {row['path']}")

    derivation = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    final = json.loads((ROOT / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    catch = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    validate_payloads(derivation, independent, final)
    require(catch["status"] == "PASS", "catch status")
    require(catch["mutations_rejected"] == 14, "catch mutation count")
    require(catch["manifest_path_mutations_rejected"] == 2, "manifest mutation count")

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    require("Q^*\\otimes V^*" in exact, "mixed pairing proof missing")
    require("d\\rho_j=-dy\\wedge d\\lambda_i" in exact, "closedness control missing")
    require("vertical gluing" in exact, "vertical gluing boundary missing")
    require("ACCEPT_WITH_REPAIRS__REPAIR_REVIEW_PENDING" in audit, "bounded grade missing")

    before = tree_hashes()
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for script in ("derive_null_ribbon_density_carry.py", "verify_null_ribbon_density_independent.py"):
        subprocess.run(
            [sys.executable, str(ROOT / script), "--check-only"],
            cwd=REPO,
            env=env,
            check=True,
        )
    after = tree_hashes()
    require(before == after, "registered replay changed package or sources")

    print(
        "PASS: G223 package; 7 sources; 21 symbolic checks; 20,000 independent cases; "
        "361,001 exact-rational assertions; 14 contract mutations; true read-only replay; "
        "manifest-contained sources"
    )


if __name__ == "__main__":
    main()
