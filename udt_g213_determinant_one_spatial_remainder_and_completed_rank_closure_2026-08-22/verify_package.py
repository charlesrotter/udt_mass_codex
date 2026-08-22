#!/usr/bin/env python3
"""Fail-closed no-write core package replay for G213."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
CORE = sorted(path for path in ROOT.iterdir() if path.is_file() and path.name not in {
    "VERIFICATION_RESULT.json", "REVIEW_SCOPE.json", "REVIEW_MANIFEST.tsv"
})


def hashes():
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in CORE}


def run_json(script):
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
production = run_json("derive_spatial_remainder_and_rank.py")
independent = run_json("verify_completed_rank_independent.py")
catches = run_json("run_catch_proofs.py")
sources = run_json("verify_source_manifest_repository.py")
after = hashes()

if before != after:
    raise AssertionError("core package changed during no-write replay")
if not production.get("all_checks_pass"):
    raise AssertionError("production failed")
if independent.get("status") != "PASS" or independent.get("cases") != 10_000:
    raise AssertionError("independent replay failed")
if independent.get("mode_census_rank") != 5:
    raise AssertionError("independent mode census failed")
if independent.get("g207_g208_union_rank") != 4:
    raise AssertionError("independent prior-tile coverage failed")
if independent.get("grading_completion_rank") != 5:
    raise AssertionError("independent grading completion failed")
if not catches.get("all_catches_pass"):
    raise AssertionError("catch replay failed")
if not sources.get("all_source_hashes_match"):
    raise AssertionError("source provenance failed")

print(json.dumps({
    "audit": "G213",
    "status": "PASS",
    "no_write_replay": True,
    "core_files_hashed": len(CORE),
    "exact_algebra_checks": production["exact_algebra_checks"],
    "independent_cases": independent["cases"],
    "independent_assertions": independent["assertions"],
    "independent_mode_census_rank": independent["mode_census_rank"],
    "independent_g207_g208_union_rank": independent["g207_g208_union_rank"],
    "independent_grading_completion_rank": independent["grading_completion_rank"],
    "hostile_catches": catches["catches"],
    "source_count": sources["source_count"],
    "g129_design_rank": production["g129_design_rank"],
    "landing": production["landing"],
}, sort_keys=True))
