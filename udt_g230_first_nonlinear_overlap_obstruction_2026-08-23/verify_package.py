#!/usr/bin/env python3
"""Aggregate G230 package verifier with optional full production replay."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import hostile_mutation_tests as hostile


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def verify_hash_table(name: str, base: Path, order: str) -> bool:
    lines = (ROOT / name).read_text(encoding="utf-8").splitlines()[1:]
    for line in lines:
        first, second = line.split("\t")
        path, digest = (first, second) if order == "path_hash" else (second, first)
        current = hashlib.sha256((base / path).read_bytes()).hexdigest()
        if current != digest:
            if name != "SOURCE_MANIFEST.tsv":
                return False
            frozen = subprocess.run(
                ["git", "show", f"3808e397:{path}"],
                cwd=REPO,
                check=True,
                capture_output=True,
            ).stdout
            if hashlib.sha256(frozen).hexdigest() != digest:
                return False
    return True


def independent_replay() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "verify_second_jet_independent.py"), "--no-write"],
        check=True,
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="rerun the long exact production solve")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    exact = load("exact_results.json")
    independent_saved = load("independent_results.json")
    hostile_saved = load("hostile_results.json")
    independent_live = independent_replay()
    hostile_live = hostile.derive()

    checks: dict[str, bool] = {
        "preregistration_hashes_match": verify_hash_table(
            "PREREGISTRATION_HASHES.tsv", ROOT, "path_hash"
        ),
        "source_manifest_hashes_match": verify_hash_table(
            "SOURCE_MANIFEST.tsv", REPO, "hash_path"
        ),
        "production_saved_all_checks": all(exact["checks"].values()),
        "production_saved_rank_closure": exact["ranks"] == exact["expected_ranks"],
        "production_saved_landing": exact["landing"]
        == "FIRST_NONLINEAR_OVERLAP_OBSTRUCTION__FULL_LOCAL_4JET_REALIZATION",
        "complete_210_case_polarization": exact["quadratic_polarization"]["cases"] == 210,
        "nonzero_R_squared_witness": exact["nonzero_commutator_witness"]["rhs_nonzero_count"] > 0,
        "independent_no_write_matches_saved": independent_live == independent_saved,
        "independent_full21_checks": all(independent_saved["checks"].values()),
        "hostile_no_write_matches_saved": hostile_live == hostile_saved,
        "hostile_9_of_9": all(hostile_saved["catches"].values()),
        "regional_history_ceiling_present": (
            "No finite-region field"
            in (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
            and "Neither route generates values or selects a physical history"
            in " ".join((ROOT / "NEXT_GATE.md").read_text(encoding="utf-8").split())
        ),
    }

    if args.full:
        import derive_second_jet_overlap as production

        checks["full_production_no_write_matches_saved"] = production.derive() == exact

    result = {
        "landing": "G230_PACKAGE_VERIFIED",
        "full_production_replayed": args.full,
        "saved_artifacts_checked": True,
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_pass": all(checks.values()),
        "preregistration_commit": "3808e397",
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "verification_results.json").write_text(text + "\n", encoding="utf-8")
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
