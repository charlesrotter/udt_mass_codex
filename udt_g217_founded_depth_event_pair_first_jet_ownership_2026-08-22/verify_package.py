#!/usr/bin/env python3
"""Fail-closed no-write aggregate replay for G217."""

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
    completed = subprocess.run(
        [sys.executable, "-B", str(ROOT / script)],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


before = hashes()
production = run("derive_first_jet_ownership.py")
independent = run("verify_first_jet_independent.py")
catches = run("run_catch_proofs.py")
sources = run("verify_source_manifest_repository.py")
after = hashes()

if before != after:
    raise AssertionError("G217 core files changed during replay")
if production.get("status") != "PASS" or production.get("exact_checks") != 37:
    raise AssertionError("production failed")
if independent.get("status") != "PASS" or independent.get("cases") != 10_000:
    raise AssertionError("independent replay failed")
if independent.get("assertions") != 190_000:
    raise AssertionError("independent assertion count changed")
if catches.get("status") != "PASS" or catches.get("catches") != 16:
    raise AssertionError("hostile catches failed")
if not sources.get("all_source_hashes_match") or sources.get("source_count") != 13:
    raise AssertionError("source provenance failed")

print(json.dumps({
    "audit": "G217",
    "status": "PASS",
    "no_write_replay": True,
    "core_files_hashed": len(CORE),
    "exact_checks": production["exact_checks"],
    "independent_cases": independent["cases"],
    "independent_assertions": independent["assertions"],
    "hostile_catches": catches["catches"],
    "source_count": sources["source_count"],
    "exp_depth_ab": production["exp_depth_ab"],
    "first_jet_multiplier_ab": production["first_jet_multiplier_ab"],
    "actual_composite_multiplier": production["actual_composite_multiplier"],
    "independent_direct_multiplier": production["independent_direct_multiplier"],
    "landing": production["landing"],
}, sort_keys=True))
