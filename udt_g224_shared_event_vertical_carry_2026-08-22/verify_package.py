#!/usr/bin/env python3
"""Verify the complete bounded pre-review G224 evidence package."""

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
    "SHARED_MIDDLE_EVENT_AND_METRIC_UNIT_CLOCK_CANONICALLY_IDENTIFY_INCIDENT_FUTURE_NULL_VERTICAL_LINES"
    "__VERTICAL_SCALAR_CARRY_IS_THE_INVERSE_REPRESENTATION_OF_THE_ACTUAL_CLOCK_RATE_CHAIN"
    "__DISTINCT_EVENT_NORMALIZATION_IS_ABSTRACTLY_AVAILABLE_BUT_NOT_A_COMPOSABLE_VERTEX_RELATION"
    "__NO_SCREEN_MAP_OR_INDEPENDENT_DIRECT_RELATION_IS_DERIVED"
)
REQUIRED = (
    "MAP.md",
    "OBSERVATION.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_shared_event_vertical_carry.py",
    "verify_shared_event_vertical_independent.py",
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
    "build_review_intake.py",
)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained_source_path(raw: str) -> Path:
    rel = Path(raw)
    require(not rel.is_absolute(), f"absolute source path: {raw}")
    require(".." not in rel.parts, f"parent-escaping source path: {raw}")
    path = (REPO / rel).resolve()
    require(path.is_relative_to(REPO.resolve()), f"source escapes verifier root: {raw}")
    return path


def tree_hashes() -> dict[str, str]:
    paths = [p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            paths.append(contained_source_path(row["path"]))
    return {str(p.resolve()): sha256(p) for p in paths}


def validate_payloads(
    derivation: dict[str, Any], independent: dict[str, Any], final: dict[str, Any]
) -> None:
    require(derivation["status"] == "PASS", "derivation status")
    require(
        derivation["preregistered_outcome"] == "A_WITH_DISTINCT_EVENT_SCOPE_CORRECTION",
        "preregistered outcome",
    )
    require(derivation["symbolic_checks"] == 24, "symbolic count")
    require(derivation["metric_clock_pairing_nondegenerate"] is True, "metric pairing")
    require(derivation["shared_event_vertical_switch_unique"] is True, "unique switch")
    require(derivation["independent_affine_rescaling_invariant"] is True, "affine covariance")
    require(derivation["common_clock_recalibration_invariant"] is True, "clock covariance")
    require(derivation["vertex_identity_inverse_cocycle"] is True, "vertex cocycle")
    require(derivation["vertical_carry_inverse_clock_representation"] is True, "inverse carry")
    require(derivation["actual_composite_closes"] is True, "actual composite")
    require(derivation["independent_direct_relation_constrained"] is False, "direct promotion")
    require(derivation["ambient_null_directions_identified"] is False, "direction promotion")
    require(derivation["screen_map_derived"] is False, "screen promotion")
    require(
        derivation["distinct_event_abstract_line_normalization_possible"] is True,
        "distinct-event normalization",
    )
    require(
        derivation["distinct_event_physical_composition_derived"] is False,
        "distinct-event composition promotion",
    )
    require(derivation["landing"] == LANDING, "derivation landing")

    require(independent["status"] == "PASS", "independent status")
    require(independent["cases"] == 20000, "independent cases")
    require(independent["exact_rational_assertions"] == 220003, "assertion count")
    require(independent["affine_rescaling_invariant"] is True, "independent affine")
    require(independent["clock_recalibration_invariant"] is True, "independent clock")
    require(independent["vertex_cocycle"] is True, "independent vertex")
    require(independent["inverse_clock_path_carry"] is True, "independent path")
    require(independent["independent_direct_edge_counterexample"] is True, "direct control")
    require(independent["different_null_direction_control"] is True, "direction control")

    require(final["status"] == "PASS", "final status")
    require(
        final["grade"]
        == "DERIVED_CONDITIONAL__INTERNALLY_VERIFIED__FRESH_EXTERNAL_REVIEW_PENDING",
        "final grade",
    )
    require(final["preregistration_commit"] == "a6b75622", "preregistration commit")
    require(final["source_count"] == 8, "source count")
    require(final["symbolic_checks"] == 24, "final symbolic count")
    require(final["independent_cases"] == 20000, "final case count")
    require(final["exact_rational_assertions"] == 220003, "final assertion count")
    require(final["contract_mutations"] == 21, "mutation count")
    require(final["shared_event_vertical_switch_unique"] is True, "final switch")
    require(final["vertical_carry_inverse_clock_representation"] is True, "final inverse carry")
    require(final["independent_direct_relation_constrained"] is False, "final direct boundary")
    require(final["ambient_null_directions_identified"] is False, "final direction boundary")
    require(final["screen_map_derived"] is False, "final screen boundary")
    require(
        final["distinct_event_abstract_line_normalization_possible"] is True,
        "final distinct normalization",
    )
    require(final["distinct_event_physical_composition_derived"] is False, "final composition")
    require(final["fresh_external_review"] == "PENDING", "review status")
    require(final["read_only_replay"] is True, "read-only replay")
    require(final["manifest_path_containment"] is True, "manifest containment")
    require(final["landing"] == LANDING, "final landing")


def main() -> None:
    for name in REQUIRED:
        require((ROOT / name).is_file(), f"missing package file: {name}")

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    require(len(rows) == 8, "source manifest count")
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
    require(catch["mutations_rejected"] == 21, "catch mutation count")
    require(catch["manifest_path_mutations_rejected"] == 2, "manifest path mutation count")

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    require("S_{+\\leftarrow-}=\\mu_+^{-1}\\circ\\mu_-" in exact, "switch proof missing")
    require("A_WITH_DISTINCT_EVENT_SCOPE_CORRECTION" in exact, "scope correction missing")
    require("independently supplied direct" in exact, "direct relation boundary missing")
    require("does not supply" in exact, "screen ceiling missing")

    before = tree_hashes()
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for script in (
        "derive_shared_event_vertical_carry.py",
        "verify_shared_event_vertical_independent.py",
    ):
        subprocess.run(
            [sys.executable, str(ROOT / script), "--check-only"],
            cwd=REPO,
            env=env,
            check=True,
        )
    after = tree_hashes()
    require(before == after, "registered replay changed package or sources")

    print(
        "PASS: G224 package; 8 sources; 24 symbolic checks; 20,000 independent cases; "
        "220,003 exact-rational assertions; 21 contract mutations; true no-write replay"
    )


if __name__ == "__main__":
    main()
