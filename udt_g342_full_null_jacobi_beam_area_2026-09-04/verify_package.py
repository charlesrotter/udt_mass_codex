#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the bounded G342 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


PREREGISTRATION_COMMIT = "b8d56fdd"
LANDING = (
    "FULL_METRIC_JACOBI_MAP_CLOSES__BOTH_SCREEN_RATES_AND_MEAN_EXPANSION_POSITIVE"
    "__SHEAR_ZERO_ONLY_ON_LONGITUDINAL_SYMMETRY_LOCUS_OR_VERTEX"
    "__EACH_COMPACT_LIFT_RETAINS_POSITIVE_AREA_WITH_PATH_LABEL"
    "__NO_LUMINOSITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*")) if path.is_file()
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
    independent = json.loads(
        (root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    checks["production_4720_of_4720"] = (
        production["status"] == "PASS"
        and production["assertions"] == 4720
        and production["failed"] == []
        and production["selected_alternatives"] == ["A", "E1", "S1", "M1", "Q1"]
        and production["maxima"]["jacobi_residual"] < 1e-12
        and production["maxima"]["transverse_limit_relative_error"] < 5e-9
    )
    checks["independent_2080_of_2080"] = (
        independent["status"] == "PASS"
        and independent["assertions"] == 2080
        and independent["failed"] == []
        and "metric two-jet curvature" in independent["method"]
        and independent["maxima"]["curvature_error"] < 1e-12
        and independent["maxima"]["rk_map_relative_error"] < 8e-8
    )
    checks["hostile_10_of_10"] = (
        hostile["all_passed"]
        and hostile["catches_passed"] == hostile["catches_total"] == 10
        and hostile["validator_shared_by_baseline_and_mutants"]
    )
    checks["landing_agreement"] = production["landing"] == hostile["landing"] == LANDING
    checks["preregistration_commit"] = production["preregistration_commit"] == PREREGISTRATION_COMMIT

    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    execution = (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")

    checks["fixed_affine_derivation"] = all(token in exact for token in (
        "fixed affine parameter", "d\\lambda\\over d\\theta_e",
        "(-s,c)\\mathbin{\\cdot}(c,s)=0", "d eta=sin(theta_e) d varphi",
    ))
    checks["full_metric_tidal_map"] = all(token in exact for token in (
        "\\mathcal T_{AB}=g(E_A,R(E_B,\\ell)\\ell)",
        "\\begin{pmatrix}-q&0\\\\0&q\\end{pmatrix}",
        "\\ddot{\\mathcal D}+\\mathcal T\\mathcal D=0",
        "was not defined by `-D-double-dot times D-inverse`",
    ))
    checks["global_area_and_rate_classification"] = all(token in exact for token in (
        "D_\\parallel>0,\\qquad D_Z>0", "\\Theta>0",
        "w(v)={2\\over\\mathcal A(v)}", "\\dot\\Theta=-{1\\over2}\\Theta^2",
        "No screen eigenresponse or area reaches zero",
    ))
    checks["principal_limits_complete"] = (
        "On the longitudinal family `lambda=0`" in exact
        and "At the transverse projective boundary" in exact
        and "They are positive and unequal for `R>1`" in exact
        and hostile["checks"]["principal_axis_chart_loss"]
    )
    checks["compact_paths_not_selected"] = (
        "Every compact-lattice lift retains its own" in audit
        and "neither sums,\nweights, discards, nor physically selects" in exact
        and hostile["checks"]["quotient_path_deletion"]
    )
    checks["initial_miss_preserved"] = (
        "failed three of 80" in execution
        and "2.3418956002921627e-08" in execution
        and "No formula, sample,\nalternative, sign criterion, or scientific landing is changed"
        in execution
    )
    checks["no_physical_promotion"] = (
        "not yet an observed brightness\nor a distance measurement" in lay
        and "light_luminosity_distance_attachment\tNOT_USED" in ledger
        and "physical_route_population\tOPEN" in ledger
        and "scale_Xmax\tOPEN" in ledger
        and hostile["checks"]["physical_readout_promotion"]
    )

    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_acceptance_authenticated"] = (
        digest(external_path)
        == "d4905f8f5abd10fca02cb9b6a47463f6104a4f110c11c18c11307c7c6203e5b0"
        and external.rstrip().endswith(
            "ACCEPT_G342_BOUNDED_FULL_NULL_JACOBI_BEAM_AREA"
        )
        and "No defects found at high, medium, or low severity" in external
        and "not premise-independent" in external
        and "does not delete, weight, aggregate, or physically select" in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_authenticated"] = all(token in transmission for token in (
        "30 manifest payloads",
        "8a3149e3921508156070fb39272f6c4e804e8008d24c0fbaf63e120b39a03bd2",
        "d8d236512cd0f7c569265c9f4f2ba201a06656f8c09af63a12feb5eea0ddea2f",
        "a664a6acc2156d69bc2fded56752c34c444336e637cecd396cf4e27cac80c592",
        "d4905f8f5abd10fca02cb9b6a47463f6104a4f110c11c18c11307c7c6203e5b0",
        "ACCEPT_G342_BOUNDED_FULL_NULL_JACOBI_BEAM_AREA",
    ))

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
        ("derive_full_null_jacobi.py", '"assertions": 4720'),
        ("verify_full_null_jacobi_independent.py", '"assertions": 2080'),
        ("run_catch_proofs.py", '"catches_total": 10'),
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
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "landing": LANDING,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
