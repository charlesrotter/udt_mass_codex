#!/usr/bin/env python3
"""Dependency-free, read-only package replay verifier for G183."""

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
REQUIRED = [
    "PREREGISTRATION.md",
    "PREREGISTRATION_SOURCE_SCOPE_NOTE.md",
    "PREREGISTRATION_SCOPE_CLARIFICATION.md",
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "WITNESS_ATLAS.tsv",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "derive_pair_strata.py",
    "verify_pair_strata_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
]
SCRIPTS = ["derive_pair_strata.py", "verify_pair_strata_independent.py", "run_catch_proofs.py"]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_hashes():
    return {path.name: sha256(path) for path in ROOT.iterdir() if path.is_file()}


def run():
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    source_failures = []
    for row in rows:
        path = REPO / row["path"]
        if not path.is_file():
            path = REPO / "sources" / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            source_failures.append(row["path"])

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())

    before = package_hashes()
    replay = {}
    env = dict(os.environ)
    env["UDT_READ_ONLY_REPLAY"] = "1"
    for script in SCRIPTS:
        completed = subprocess.run(
            [sys.executable, "-I", "-S", script],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        replay[script] = {
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    after = package_hashes()

    checks = {
        "files_present": not missing,
        "eight_immutable_sources": len(rows) == 8 and not source_failures,
        "production_pass": production.get("trials") == 12000 and production.get("assertions") == 72115,
        "independent_pass": independent.get("status") == "PASS" and independent.get("trials") == 20000,
        "independent_assertions": independent.get("assertions") == 220034,
        "twenty_eight_catches": catches.get("executable_catch_count") == 28 and not catches.get("failed_executable_catches"),
        "twelve_semantic_guards": catches.get("semantic_guard_count") == 12,
        "all_replays_pass": all(item["returncode"] == 0 for item in replay.values()),
        "read_only_replays": before == after,
        "landing_matches": production.get("landing_candidate")
        == "PAIR_STRATA_SEPARATED__REGULAR_MULTIBRANCH_KERNEL_REMAINS_BRANCH_LABELLED",
    }
    external_path = ROOT / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md"
    review_state = "PENDING"
    if external_path.is_file():
        review_state = (
            "ACCEPTED"
            if "G183_ACCEPTED_WITH_STATED_BOUNDS" in external_path.read_text(encoding="utf-8")
            else "NOT_ACCEPTED"
        )
        checks["external_review_accepted"] = review_state == "ACCEPTED"

    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "audit": "G183",
        "status": status,
        "external_review": review_state,
        "checks": checks,
        "missing_files": missing,
        "source_hash_failures": source_failures,
        "replays": replay,
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    run()
