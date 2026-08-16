#!/usr/bin/env python3
"""Verify the complete G108 package, source hashes, and deterministic replays."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes() -> dict[str, bool]:
    checks = {}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            checks[row["path"]] = sha256(ROOT / row["path"]) == row["sha256"]
    return checks


def run(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv",
        "derive_screen_propagation.py",
        "verify_screen_propagation_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "G68_ENDPOINT_RATE_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "STATUS.md",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "build_review_intake.py",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "REVIEW_DISPATCH.md",
        "FOLLOWUP_REVIEW_REQUEST.md",
        "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
    ]
    required_checks = {name: (HERE / name).is_file() for name in required}
    hashes = source_hashes()

    saved_derivation = (HERE / "DERIVATION_RESULT.json").read_bytes()
    saved_independent = (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
    saved_atlas = (HERE / "G68_ENDPOINT_RATE_ATLAS.tsv").read_bytes()
    production_run = run("derive_screen_propagation.py")
    independent_run = run("verify_screen_propagation_independent.py")
    production_replay = (
        saved_derivation == (HERE / "DERIVATION_RESULT.json").read_bytes()
        and saved_atlas == (HERE / "G68_ENDPOINT_RATE_ATLAS.tsv").read_bytes()
    )
    independent_replay = saved_independent == (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    exact = derivation["exact"]
    exact_checks = {
        "constant_recovers_a": exact["constant_extension"]["recovers_a"],
        "rotation_drops_from_area": exact["constant_extension"]["rotation_drops_from_area"],
        "factorization_product": exact["factorization"]["W_equals_QN"],
        "factorization_rates_add": exact["factorization"]["rates_add"],
        "screen_rotation_area": exact["screen_rotation"]["area_rate_unchanged"],
        "analytic_controls": all(
            row["jacobi_residual_zero"] and row["rates_equal"]
            for row in exact["analytic_controls"].values()
        ),
        "G68_rows": derivation["g68_saved_replay"]["row_count"] == 21,
        "G68_finite": derivation["g68_saved_replay"]["all_rates_finite"],
    }

    status = (HERE / "STATUS.md").read_text()
    report = (HERE / "AUDIT_REPORT.md").read_text()
    semantic_checks = {
        "status_not_overpromoted": "REPAIRS_VERIFIED__ORIGINAL_G108_LANDING_STANDS" in status,
        "history_open": "metric history" in report.lower() and "still do not select" in report.lower(),
        "no_observational_promotion": "No BAO/CMB/SNe outcome" in report,
        "query_tie_explicit": "WHEN_QUERY_IDENTIFIES_THE_COMPLETE_PAIR_SCREEN_WITH_THE_JACOBI_MAP" in report,
        "followup_verified": "REPAIRS_VERIFIED__ORIGINAL_G108_LANDING_STANDS"
        in (HERE / "EXTERNAL_FOLLOWUP_REVIEW_RAW.md").read_text(),
    }

    result = {
        "schema": "UDT_G108_PACKAGE_VERIFICATION_V1",
        "required_files": required_checks,
        "all_required_files_present": all(required_checks.values()),
        "source_hashes": hashes,
        "all_source_hashes_match": all(hashes.values()),
        "production_returncode": production_run.returncode,
        "independent_returncode": independent_run.returncode,
        "production_replay_matches_saved": production_replay,
        "independent_replay_matches_saved": independent_replay,
        "exact_checks": exact_checks,
        "all_exact_checks_pass": all(exact_checks.values()),
        "independent_checks_pass": independent["all_checks_pass"],
        "semantic_checks": semantic_checks,
        "all_semantic_checks_pass": all(semantic_checks.values()),
    }
    result["all_checks_pass"] = all(
        [
            result["all_required_files_present"],
            result["all_source_hashes_match"],
            production_run.returncode == 0,
            independent_run.returncode == 0,
            production_replay,
            independent_replay,
            result["all_exact_checks_pass"],
            result["independent_checks_pass"],
            result["all_semantic_checks_pass"],
        ]
    )
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if production_run.returncode:
        print(production_run.stdout)
        print(production_run.stderr, file=sys.stderr)
    if independent_run.returncode:
        print(independent_run.stdout)
        print(independent_run.stderr, file=sys.stderr)
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
