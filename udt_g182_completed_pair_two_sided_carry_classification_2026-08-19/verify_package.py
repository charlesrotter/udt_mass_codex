#!/usr/bin/env python3
"""Package-level, dependency-free and read-only replay verifier for G182."""

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
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "WITNESS_ATLAS.tsv",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "derive_two_sided_carry.py",
    "verify_two_sided_carry_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
    "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "TRANSMISSION_RECORD.md",
]
SCRIPTS = [
    "derive_two_sided_carry.py",
    "verify_two_sided_carry_independent.py",
    "run_catch_proofs.py",
]


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
    source_failures = []
    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = REPO / row["path"]
        if not path.is_file():
            path = REPO / "sources" / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            source_failures.append(row["path"])

    derivation = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    external_review = (ROOT / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_text(encoding="utf-8")

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
        "seven_sources": len(rows) == 7 and not source_failures,
        "production_pass": derivation.get("trials") == 12000 and derivation.get("assertions") == 96025,
        "independent_pass": independent.get("status") == "PASS" and independent.get("trials") == 20000,
        "independent_assertions": independent.get("assertions") == 240100,
        "twenty_thousand_gram_fibers": independent.get("distinct_equal_gram_witnesses") == 20000,
        "twenty_two_executable_catches": catches.get("executable_catch_count") == 22 and not catches.get("failed_executable_catches"),
        "eight_semantic_guards": catches.get("semantic_guard_count") == 8,
        "all_replays_pass": all(item["returncode"] == 0 for item in replay.values()),
        "read_only_replays": before == after,
        "landing_matches": derivation.get("landing_candidate") == "TWO_SIDED_PAIR_METRIC_CARRY_CLASSIFIED__FULL_GERM_JETS_REQUIRED_FOR_IMMERSION_CARRY",
        "external_review_accepted": "G182_ACCEPTED_WITH_STATED_BOUNDS" in external_review,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "audit": "G182",
        "status": status,
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
