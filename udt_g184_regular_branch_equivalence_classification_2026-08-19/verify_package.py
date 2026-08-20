#!/usr/bin/env python3
"""Dependency-free, read-only package replay verifier for G184."""

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
    "PREREGISTRATION_TERMINOLOGY_CLARIFICATION.md",
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "WITNESS_ATLAS.tsv",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "derive_branch_equivalence.py",
    "verify_branch_equivalence_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "DEFAULT_ENTRYPOINT_VERIFICATION.json",
    "verify_default_read_only_entrypoint.py",
]
BASE_SCRIPTS = [
    "derive_branch_equivalence.py",
    "verify_branch_equivalence_independent.py",
    "run_catch_proofs.py",
]
LANDING = (
    "TYPED_REALIZATION_ISOMORPHISM_CLASSIFIES_REGULAR_BRANCH_EQUIVALENCE__"
    "KERNEL_IS_NOT_A_COMPLETE_REALIZATION_INVARIANT"
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_hashes():
    return {path.name: sha256(path) for path in ROOT.iterdir() if path.is_file()}


def run():
    skip_default = os.environ.get("G184_SKIP_DEFAULT_CHECK") == "1"
    required = [name for name in REQUIRED if not (skip_default and name == "DEFAULT_ENTRYPOINT_VERIFICATION.json")]
    missing = [name for name in required if not (ROOT / name).is_file()]

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    source_failures = []
    for row in rows:
        path = REPO / row["path"]
        if not path.is_file():
            path = REPO / "sources" / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            source_failures.append(row["path"])

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    before = package_hashes()
    replay = {}
    env = dict(os.environ)
    env["UDT_READ_ONLY_REPLAY"] = "1"
    scripts = list(BASE_SCRIPTS)
    if not skip_default:
        scripts.append("verify_default_read_only_entrypoint.py")
    for script in scripts:
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
        "production_pass": production.get("trials") == 12000 and production.get("assertions") == 121544,
        "independent_pass": independent.get("status") == "PASS" and independent.get("trials") == 20000,
        "independent_assertions": independent.get("assertions") == 145709,
        "orientation_populations_complete": (
            independent.get("orientation_preserving_jacobians", 0)
            + independent.get("orientation_reversing_jacobians", 0)
            == 20000
        ),
        "thirty_catches": catches.get("executable_catch_count") == 30 and not catches.get("failed_executable_catches"),
        "twelve_semantic_guards": catches.get("semantic_guard_count") == 12,
        "all_replays_pass": all(item["returncode"] == 0 for item in replay.values()),
        "helper_live_replayed": skip_default or "verify_default_read_only_entrypoint.py" in replay,
        "read_only_replays": before == after,
        "landing_matches": production.get("landing_candidate") == LANDING,
    }
    if not skip_default:
        default_path = ROOT / "DEFAULT_ENTRYPOINT_VERIFICATION.json"
        default = json.loads(default_path.read_text(encoding="utf-8")) if default_path.is_file() else {}
        checks["default_entrypoint_read_only"] = (
            default.get("status") == "PASS"
            and default.get("returncode") == 0
            and default.get("hashes_unchanged") is True
        )

    external_path = ROOT / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md"
    followup_path = ROOT / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md"
    review_state = "PENDING"
    if followup_path.is_file():
        raw = followup_path.read_text(encoding="utf-8")
        review_state = "ACCEPTED" if "G184_REPAIR_ACCEPTED" in raw else "NOT_ACCEPTED"
        checks["external_review_accepted"] = review_state == "ACCEPTED"
    elif external_path.is_file():
        raw = external_path.read_text(encoding="utf-8")
        if "G184_ACCEPTED_WITH_STATED_BOUNDS" in raw:
            review_state = "ACCEPTED"
            checks["external_review_accepted"] = True
        elif "G184_REPAIR_REQUIRED" in raw:
            review_state = "REPAIR_REQUIRED"
        elif "G184_REFUTED" in raw:
            review_state = "REFUTED"
            checks["external_review_not_refuted"] = False

    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "audit": "G184",
        "status": status,
        "external_review": review_state,
        "checks": checks,
        "missing_files": missing,
        "source_hash_failures": source_failures,
        "replays": replay,
    }
    if os.environ.get("UDT_WRITE_VERIFICATION_RESULT") == "1":
        (ROOT / "VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    run()
