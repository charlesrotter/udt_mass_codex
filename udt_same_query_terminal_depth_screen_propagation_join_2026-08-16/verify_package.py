#!/usr/bin/env python3
"""Verify G109 source hashes and deterministic production/independent replays."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_source(relative: str) -> Path:
    repository_source = ROOT / relative
    sealed_source = ROOT / "declared_sources" / relative
    if repository_source.is_file():
        return repository_source
    if sealed_source.is_file():
        return sealed_source
    raise FileNotFoundError(relative)


def run(script: str, package: Path, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(package / script)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-result",
        action="store_true",
        help="write PACKAGE_VERIFICATION_RESULT.json in the source package",
    )
    args = parser.parse_args()
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv",
        "derive_same_query_join.py",
        "verify_same_query_join_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CONTROL_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS.md",
        "STATUS_LEDGER.tsv",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REVIEW_FOLLOWUP_RAW.md",
        "REVIEW_DISPATCH.md",
        "build_review_intake.py",
    ]
    required_checks = {name: (HERE / name).is_file() for name in required}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    hashes = {
        row["path"]: sha256(resolve_source(row["path"])) == row["sha256"]
        for row in source_rows
    }

    saved_derivation = (HERE / "DERIVATION_RESULT.json").read_bytes()
    saved_independent = (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
    saved_atlas = (HERE / "CONTROL_ATLAS.tsv").read_bytes()
    with tempfile.TemporaryDirectory(prefix="udt_g109_verify_") as temp_name:
        temp_root = Path(temp_name)
        temp_package = temp_root / HERE.name
        shutil.copytree(HERE, temp_package)
        for row in source_rows:
            target = temp_root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resolve_source(row["path"]), target)
        production = run("derive_same_query_join.py", temp_package, temp_root)
        independent = run("verify_same_query_join_independent.py", temp_package, temp_root)
        production_replay = saved_derivation == (
            temp_package / "DERIVATION_RESULT.json"
        ).read_bytes()
        atlas_replay = saved_atlas == (temp_package / "CONTROL_ATLAS.tsv").read_bytes()
        independent_replay = saved_independent == (
            temp_package / "INDEPENDENT_VERIFICATION.json"
        ).read_bytes()
        derivation = json.loads((temp_package / "DERIVATION_RESULT.json").read_text())
        independent_result = json.loads(
            (temp_package / "INDEPENDENT_VERIFICATION.json").read_text()
        )
    report = (HERE / "AUDIT_REPORT.md").read_text()
    status = (HERE / "STATUS.md").read_text()
    semantic = {
        "conditional_landing": "CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED" in report,
        "history_open": "does not select the physical history" in report,
        "matched_calibration_explicit": "matched query/calibration" in report,
        "zero_rate_boundary": "dot(phi_pair)=0" in report,
        "external_review_passed": "EXTERNALLY_VERIFIED_WITH_CAVEATS" in status,
        "repair_followup_passed": "Repair 4 is effective"
        in (HERE / "EXTERNAL_REVIEW_FOLLOWUP_RAW.md").read_text(),
        "read_only_verifier": "TemporaryDirectory" in (HERE / "verify_package.py").read_text()
        and "--write-result" in (HERE / "verify_package.py").read_text(),
        "no_outcome_promotion": "no bao cmb sne or xmax conclusion"
        in (HERE / "STATUS_LEDGER.tsv").read_text().lower(),
    }
    result = {
        "schema": "UDT_G109_PACKAGE_VERIFICATION_V1",
        "required_files": required_checks,
        "all_required_files_present": all(required_checks.values()),
        "source_hashes": hashes,
        "all_source_hashes_match": all(hashes.values()),
        "production_returncode": production.returncode,
        "independent_returncode": independent.returncode,
        "production_replay_matches_saved": production_replay,
        "atlas_replay_matches_saved": atlas_replay,
        "independent_replay_matches_saved": independent_replay,
        "derivation_checks_pass": derivation["all_checks_pass"],
        "independent_checks_pass": independent_result["all_checks_pass"],
        "semantic_checks": semantic,
        "all_semantic_checks_pass": all(semantic.values()),
    }
    result["all_checks_pass"] = all(
        [
            result["all_required_files_present"],
            result["all_source_hashes_match"],
            production.returncode == 0,
            independent.returncode == 0,
            production_replay,
            atlas_replay,
            independent_replay,
            result["derivation_checks_pass"],
            result["independent_checks_pass"],
            result["all_semantic_checks_pass"],
        ]
    )
    if args.write_result:
        (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    if production.returncode:
        print(production.stdout)
        print(production.stderr, file=sys.stderr)
    if independent.returncode:
        print(independent.stdout)
        print(independent.stderr, file=sys.stderr)
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
