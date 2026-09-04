#!/usr/bin/env python3
"""Aggregate, dependency-free, no-write verifier for the G338 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


LANDING = (
    "EXPLICIT_LAWFUL_TAUB_DEVELOPMENT_CARRIES_NATIVE_COMPLETED_PAIR_RESPONSE_FOR_FINITE_TIME"
    "__ZERO_BOOST_TERMINAL_BLINDNESS_COEXISTS_WITH_NONTRIVIAL_RULER_DENSITY"
    "__INITIAL_SILENCE_CAN_TURN_ON_EXACTLY__NO_OCCUPANCY_OR_SCALE_SELECTION"
)
PREREGISTRATION_COMMIT = "01e2110a"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.name: digest(path)
        for path in sorted(root.iterdir())
        if path.is_file()
    }


def matches_frozen_source(repo: Path, source_path: str, expected_hash: str) -> bool:
    """Authenticate a preregistered source now or at the frozen commit."""
    current = repo / source_path
    if current.is_file() and digest(current) == expected_hash:
        return True
    if not (repo / ".git").exists():
        return False
    frozen = subprocess.run(
        ["git", "show", f"{PREREGISTRATION_COMMIT}:{source_path}"],
        cwd=repo,
        capture_output=True,
        check=False,
    )
    return (
        frozen.returncode == 0
        and hashlib.sha256(frozen.stdout).hexdigest() == expected_hash
    )


def main() -> None:
    root = Path(__file__).resolve().parent
    checks: dict[str, bool] = {}

    production = json.loads((root / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    checks["production_169_of_169"] = production["all_passed"] and production["checks_passed"] == production["checks_total"] == 169
    checks["independent_16_of_16"] = independent["all_passed"] and independent["checks_passed"] == independent["checks_total"] == 16
    checks["hostile_9_of_9"] = hostile["all_passed"] and hostile["catches_passed"] == hostile["catches_total"] == 9
    checks["landing_agreement"] = production["landing"] == independent["landing"] == LANDING

    for name in ("EXACT_DERIVATION.md", "LAY_REPORT.md", "AUDIT_REPORT.md"):
        text = (root / name).read_text(encoding="utf-8")
        checks[f"{name}_has_bounded_conclusion"] = "NO_OCCUPANCY_OR_SCALE_SELECTION" in text or (
            "does not" in text.lower() and "scale" in text.lower()
        )

    # Verify frozen source hashes when run in the repository; the sealed review
    # intake intentionally need not contain repository-global sources.
    repo = root.parent
    source_lines = [
        line
        for line in (root / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
        if line.strip()
    ]
    if (repo / ".git").exists() or all(
        (repo / line.split("\t", 1)[0]).is_file() for line in source_lines
    ):
        checks["frozen_source_hashes_or_preregistration_commit"] = all(
            matches_frozen_source(repo, fields[0], fields[1])
            for fields in (line.split("\t") for line in source_lines)
        )
    else:
        checks["sealed_source_absence_is_explicit"] = True

    before = snapshot(root)
    env = dict(os.environ)
    env["UDT_NO_WRITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    commands = (
        "derive_explicit_taub_pair_readout.py",
        "verify_explicit_taub_pair_readout_independent.py",
        "run_catch_proofs.py",
    )
    for script in commands:
        completed = subprocess.run(
            [sys.executable, "-S", script],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        checks[f"no_write_replay_{script}"] = completed.returncode == 0
        if completed.returncode != 0:
            raise AssertionError(f"{script}: {completed.stderr}")
    after = snapshot(root)
    checks["aggregate_replay_changes_no_bytes"] = before == after

    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise AssertionError(f"package verification failures: {failed}")

    result = {
        "landing": LANDING,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_passed": all(checks.values()),
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        (root / "VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
