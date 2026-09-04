#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the bounded G340 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


PREREGISTRATION_COMMIT = "d2b68663"
LANDING = (
    "METRIC_NULL_GEOMETRY_CLOSES_A_PATH_LABELLED_FINITE_NORMAL_PAIR_FAMILY"
    "__NO_PHENOMENOLOGICAL_LIGHT_MODEL_REQUIRED"
    "__SLICE_DISTANCE_NULL_EXCHANGE_RADAR_AND_PROJECTIVE_READOUT_ARE_RELATED_NOT_IDENTICAL"
    "__COMPACT_WINDINGS_REMAIN_DISTINCT_BRANCHES"
    "__NO_PHYSICAL_PROTOCOL_POPULATION_SCALE_OR_XMAX_SELECTED"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.name: digest(path)
        for path in sorted(root.iterdir())
        if path.is_file()
    }


def frozen_source_matches(repo: Path, source: str, expected: str) -> bool:
    current = repo / source
    if current.is_file() and digest(current) == expected:
        return True
    sealed = repo / "sources" / source
    if sealed.is_file() and digest(sealed) == expected:
        return True
    if not (repo / ".git").exists():
        return False
    frozen = subprocess.run(
        ["git", "show", f"{PREREGISTRATION_COMMIT}:{source}"],
        cwd=repo,
        capture_output=True,
        check=False,
    )
    return frozen.returncode == 0 and hashlib.sha256(frozen.stdout).hexdigest() == expected


def main() -> None:
    root = Path(__file__).resolve().parent
    repo = root.parent
    checks: dict[str, bool] = {}
    production = json.loads((root / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    checks["production_3868_of_3868"] = (
        production["all_passed"]
        and production["checks_passed"] == production["checks_total"] == 3868
    )
    checks["independent_5988_of_5988"] = (
        independent["all_passed"]
        and independent["checks_passed"] == independent["checks_total"] == 5988
        and independent["coverage"]["general_metric_cases"] == 1000
        and "no production import or result read" in independent["method"]
    )
    checks["hostile_15_of_15"] = (
        hostile["all_passed"]
        and hostile["catches_passed"] == hostile["catches_total"] == 15
    )
    checks["landing_agreement"] = (
        production["landing"] == independent["landing"] == hostile["landing"] == LANDING
    )
    checks["preregistration_commit"] = (
        production["preregistration_commit"] == PREREGISTRATION_COMMIT
        and PREREGISTRATION_COMMIT
        in (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    )

    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    checks["four_types_distinct"] = all(
        token in exact
        for token in (
            "Same-slice distance",
            "Metric-null propagation without a light model",
            "Two-leg radar as a supplied protocol",
            "Frequency, reciprocal depth, and projective readout",
        )
    )
    checks["general_and_principal_scope"] = (
        production["coverage"]["general_null_cases"] == 400
        and production["coverage"]["principal_one_way_cases"] == 108
        and "Solving its boundary-value inverse can be multivalued" in exact
    )
    checks["light_model_boundary"] = (
        "No Maxwell field is needed" in exact
        and "Radar reflection is clearly\nmarked as a chosen measurement procedure" in lay
        and "electromagnetic_light_model\tNOT_USED" in ledger
    )
    checks["no_physical_selection"] = (
        "physical_distance_protocol\tOPEN" in ledger
        and "physical_observer_route_population\tOPEN" in ledger
        and "scale_Xmax\tOPEN" in ledger
    )
    checks["metric_kernel_unchanged"] = (
        "metric_kernel_angular_equation\tUNCHANGED" in ledger
        and "metric, reciprocal kernel, angular sector, and provisional equation are unchanged"
        in exact
    )
    checks["signed_depth_not_distance"] = (
        "It is not\nthe sign of physical distance" in exact
        and hostile["catches"]["signed_depth_called_distance_sign"]
    )
    checks["winding_retained"] = (
        "Every lattice lift gives a separate lawful arrival branch" in
        (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
        and hostile["catches"]["winding_omission"]
    )
    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_acceptance_authenticated"] = (
        digest(external_path)
        == "fe712e1bfc62cf6ddcc14a1f34cf6712b915d69c6ae578cd3d72f3591446bdc6"
        and external.rstrip().endswith(
            "ACCEPT_G340_BOUNDED_FINITE_PAIR_RELATION_CLASSIFICATION"
        )
        and "Critical: none." in external
        and "Low: none." in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_authenticated"] = (
        "35 manifest payloads" in transmission
        and "fe712e1bfc62cf6ddcc14a1f34cf6712b915d69c6ae578cd3d72f3591446bdc6"
        in transmission
        and "ACCEPT_G340_BOUNDED_FINITE_PAIR_RELATION_CLASSIFICATION"
        in transmission
    )

    source_rows = (root / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
    checks["frozen_source_hashes"] = all(
        frozen_source_matches(repo, source, expected)
        for source, expected, _role in (
            line.split("\t") for line in source_rows if line.strip()
        )
    )

    before = snapshot(root)
    env = dict(os.environ)
    env["UDT_NO_WRITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    replay_specs = (
        ("derive_finite_pair_relations.py", '"checks_total": 3868'),
        ("verify_finite_pair_independent.py", '"checks_total": 5988'),
        ("run_catch_proofs.py", '"catches_total": 15'),
    )
    for script, token in replay_specs:
        replay = subprocess.run(
            [sys.executable, "-B", "-S", str(root / script)],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        checks[f"no_write_replay_{script}"] = replay.returncode == 0 and token in replay.stdout
    after = snapshot(root)
    checks["aggregate_replay_changes_no_bytes"] = before == after

    all_passed = all(checks.values())
    result = {
        "all_passed": all_passed,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "landing": LANDING,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        (root / "VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
