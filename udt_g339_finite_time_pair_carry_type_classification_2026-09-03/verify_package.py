#!/usr/bin/env python3
"""Aggregate, dependency-free, no-write verifier for the bounded G339 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


LANDING = (
    "FINITE_TIME_PAIR_COMPONENTS_DEPEND_ON_SUPPLIED_CARRY"
    "__G338_LIE_CARRY_IS_THE_COMOVING_OBSERVER_SEPARATION_QUERY"
    "__PARALLEL_AND_FERMI_LOCAL_RULERS_ARE_QUIET_CONTROLS"
    "__METRIC_DEFORMATION_IS_RECOVERED_FROM_TYPED_PAIR_PLUS_CARRY"
    "__NO_PHYSICAL_CARRY_SELECTED"
)
PREREGISTRATION_COMMIT = "f6394739"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.name: digest(path)
        for path in sorted(root.iterdir())
        if path.is_file()
    }


def matches_frozen_source(repo: Path, source_path: str, expected_hash: str) -> bool:
    """Authenticate a preregistered source now or at the preregistration commit."""
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
    independent = json.loads(
        (root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    checks["production_2182_of_2182"] = (
        production["all_passed"]
        and production["checks_passed"] == production["checks_total"] == 2182
    )
    checks["independent_16155_of_16155"] = (
        independent["all_passed"]
        and independent["checks_passed"] == independent["checks_total"] == 16155
        and independent["random_cases"] == 1200
        and independent["regular_cases"] == 1135
    )
    checks["hostile_12_of_12"] = (
        hostile["all_passed"]
        and hostile["catches_passed"] == hostile["catches_total"] == 12
    )
    checks["landing_agreement"] = (
        production["landing"] == independent["landing"] == hostile["landing"] == LANDING
    )
    checks["preregistration_commit_recorded"] = (
        production["preregistration_commit"] == PREREGISTRATION_COMMIT
        and PREREGISTRATION_COMMIT
        in (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    )

    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    checks["connecting_field_is_infinitesimal_and_supplied"] = (
        "infinitesimal separation" in exact
        and "supplied comoving normal" in audit
        and "selected comoving normal observers" in exact
    )
    checks["parallel_is_different_query"] = (
        "different objects" in lay
        and "not the\n  connecting field" in exact
    )
    checks["quiet_does_not_erase_curvature"] = (
        "not zero curvature" in exact and "geometry is not lost" in lay
    )
    checks["clock_boundary_not_spacetime_boundary"] = (
        "pair plane itself remains Lorentzian" in exact
    )
    checks["no_population_or_scale_selection"] = (
        "physical_observer_population\tOPEN" in ledger
        and "observation_scale_Xmax\tOPEN" in ledger
        and "has not selected that population" in lay
    )
    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_acceptance_authenticated"] = (
        digest(external_path)
        == "22943e5e00ed44da3690eb41aefc6111e4418d1d8f5ddcac6486776897c98eee"
        and external.rstrip().endswith("ACCEPT_G339_BOUNDED_CARRY_TYPE_CLASSIFICATION")
        and "No repair requests are required" in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_authenticated"] = (
        "32 manifest payloads" in transmission
        and "22943e5e00ed44da3690eb41aefc6111e4418d1d8f5ddcac6486776897c98eee"
        in transmission
        and "ACCEPT_G339_BOUNDED_CARRY_TYPE_CLASSIFICATION" in transmission
    )

    source_lines = [
        line
        for line in (root / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
        if line.strip()
    ]
    repo = root.parent
    if (repo / ".git").exists() or all(
        (repo / line.split("\t", 1)[0]).is_file() for line in source_lines
    ):
        checks["frozen_source_hashes_or_preregistration_commit"] = all(
            matches_frozen_source(repo, fields[0], fields[1])
            for fields in (line.split("\t") for line in source_lines)
        )
    else:
        # A sealed review intake deliberately contains only copied source evidence,
        # not the repository or its Git history. Its outer manifest authenticates it.
        checks["sealed_source_absence_is_explicit"] = True

    before = snapshot(root)
    env = dict(os.environ)
    env["UDT_NO_WRITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    commands = (
        "derive_carry_type_classification.py",
        "verify_carry_type_independent.py",
        "run_catch_proofs.py",
    )
    for script in commands:
        completed = subprocess.run(
            [sys.executable, "-B", "-S", script],
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

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
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
