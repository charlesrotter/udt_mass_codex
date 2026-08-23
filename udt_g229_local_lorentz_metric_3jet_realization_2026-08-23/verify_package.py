#!/usr/bin/env python3
"""Aggregate no-write certification for the bounded G229 package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from derive_metric_3jet_realization import derive as derive_production
from hostile_mutation_tests import run as derive_hostile
from verify_g227_g228_projection_recovery import run as derive_projection
from verify_metric_3jet_independent import run as derive_independent


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREREG_COMMIT = "7ce01c20"


def git_file(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def verify(require_saved: bool = True) -> dict[str, object]:
    production = derive_production()
    independent = derive_independent()
    hostile = derive_hostile()
    projection = derive_projection()

    shared_hashes = independent["shared_matrix_hash_matches_production"]
    source_hashes_match = True
    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        frozen = git_file(PREREG_COMMIT, row["path"])
        if hashlib.sha256(frozen).hexdigest() != row["sha256"]:
            source_hashes_match = False
            break

    prereg_hash = hashlib.sha256(
        git_file(PREREG_COMMIT, f"{ROOT.name}/PREREGISTRATION.md")
    ).hexdigest()
    frozen_hash_row = next(
        csv.DictReader(
            (ROOT / "PREREGISTRATION_HASHES.tsv").open(newline="", encoding="utf-8"),
            delimiter="\t",
        )
    )

    saved_match = True
    saved_checked = False
    if require_saved:
        saved_checked = True
        saved_match = (
            json.loads((ROOT / "exact_results.json").read_text(encoding="utf-8")) == production
            and json.loads((ROOT / "independent_verification.json").read_text(encoding="utf-8"))
            == independent
            and json.loads((ROOT / "hostile_results.json").read_text(encoding="utf-8")) == hostile
            and json.loads((ROOT / "projection_recovery.json").read_text(encoding="utf-8"))
            == projection
        )

    premise_text = (ROOT / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    report_text = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    evidence_text = (ROOT / "EVIDENCE_GATES.md").read_text(encoding="utf-8")
    normalized_report = " ".join(report_text.split())
    checks = {
        "production_exact_alternative_A": (
            production["all_exact_checks_pass"]
            and production["landing"]
            == "FULL_LOCAL_3JET_REALIZATION__COORDINATE_KERNELS_80_AND_140"
        ),
        "independent_full_21_84_slot_replay": independent["all_checks_pass"],
        "shared_gauge_and_normal_hashes_match": all(shared_hashes.values()),
        "hostile_mutations_9_of_9": hostile["all_caught"] and hostile["count"] == 9,
        "g188_g227_g228_projection_recovery": projection["all_checks_pass"],
        "g188_nonzero_jacobi_sign_bridge": (
            projection["g188_jacobi_sign_bridge"]["nonzero_sign_witness"]
            and projection["g188_jacobi_sign_bridge"]["lower_left_block_equals_minus_tide"]
        ),
        "normal_slices_uniquely_fix_coordinate_gauge": (
            production["ranks"]["normal2_on_cubic_gauge"] == 80
            and production["ranks"]["normal3_on_quartic_gauge"] == 140
        ),
        "smooth_witness_is_data_dependent_local_only": (
            "data-dependent open neighborhood" in production["finite_polynomial_witness"]["signature_statement"]
            and "radial coordinate lines" in production["finite_polynomial_witness"]["radial_normal_coordinate_identity"]
        ),
        "fixed_tangent_frame_scope_guard": (
            "event_and_tangent_frame\tSUPPLIED_CONDITIONAL" in premise_text
            and "The tangent frame is fixed" in normalized_report
        ),
        "value_history_nonpromotion_guard": (
            "does not generate curvature values" in normalized_report
            and "does not select a metric history" in normalized_report
            and "Point-jet theorem" in evidence_text
        ),
        "preregistration_hash_frozen": prereg_hash == frozen_hash_row["sha256"],
        "source_manifest_hashes_match_prereg_commit": source_hashes_match,
        "saved_machine_artifacts_match_replay": saved_match,
    }
    return {
        "landing": production["landing"],
        "checks": checks,
        "passed": sum(bool(value) for value in checks.values()),
        "total": len(checks),
        "all_pass": all(bool(value) for value in checks.values()),
        "saved_artifacts_checked": saved_checked,
        "preregistration_commit": PREREG_COMMIT,
        "scope": "one supplied event, fixed tangent frame, metric through cubic Taylor order",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--skip-saved", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "verification_results.json")
    args = parser.parse_args()
    result = verify(require_saved=not args.skip_saved)
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    elif args.output.exists():
        saved = json.loads(args.output.read_text(encoding="utf-8"))
        if saved != result:
            raise SystemExit("saved verification_results.json does not match no-write replay")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
