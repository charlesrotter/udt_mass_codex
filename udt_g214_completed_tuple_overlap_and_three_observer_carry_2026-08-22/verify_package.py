#!/usr/bin/env python3
"""Fail-closed no-write aggregate replay for G214."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
EXCLUDED = {
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "REVIEW_SCOPE.json",
    "REVIEW_MANIFEST.tsv",
    "EXTERNAL_REVIEW_RAW.md",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "TRANSMISSION_RECORD.md",
}
CORE = sorted(path for path in ROOT.iterdir() if path.is_file() and path.name not in EXCLUDED)


def hashes():
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in CORE}


def run(script):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    done = subprocess.run(
        [sys.executable, "-B", str(ROOT / script)],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(done.stdout)


before = hashes()
production = run("derive_tuple_descent.py")
independent = run("verify_tuple_descent_independent.py")
catches = run("run_catch_proofs.py")
sources = run("verify_source_manifest_repository.py")
after = hashes()

if before != after:
    raise AssertionError("G214 core files changed during replay")
if production.get("status") != "PASS":
    raise AssertionError("production failed")
if independent.get("status") != "PASS" or independent.get("cases") != 10_000:
    raise AssertionError("independent replay failed")
if catches.get("status") != "PASS" or catches.get("catches", 0) < 7:
    raise AssertionError("hostile catches failed")
if not sources.get("all_source_hashes_match") or sources.get("source_count") != 14:
    raise AssertionError("source provenance failed")

print(json.dumps({
    "audit": "G214",
    "status": "PASS",
    "no_write_replay": True,
    "core_files_hashed": len(CORE),
    "exact_checks": production["exact_checks"],
    "independent_cases": independent["cases"],
    "independent_assertions": independent["assertions"],
    "hostile_catches": catches["catches"],
    "source_count": sources["source_count"],
    "landing": production["landing"],
}, sort_keys=True))
