#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the bounded G341 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


PREREGISTRATION_COMMIT = "6f1441f6"
LANDING = (
    "EACH_NONZERO_UNIVERSAL_COVER_LIFT_HAS_ONE_REGULAR_FUTURE_NULL_SOLUTION"
    "__NO_INTERIOR_CONJUGATE_CAUSTIC_ON_THE_SUPPLIED_TAUB_KASNER_NULL_CONE"
    "__MIXED_RAYS_HAVE_NONZERO_G269_NULL_ROTATION_WITH_TRIVIAL_SCREEN_QUOTIENT_ROTATION"
    "__COMPACT_MULTIPLICITY_IS_PATH_LABELLED_NOT_PER_LIFT_NONUNIQUENESS"
    "__NO_LIGHT_MODEL_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
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
    independent = json.loads(
        (root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    checks["production_8992_of_8992"] = (
        production["all_passed"]
        and production["checks_passed"] == production["checks_total"] == 8992
        and production["coverage"]
        == {
            "compact_lattice_cases": 16,
            "endpoint_inverse_cases": 72,
            "mixed_local_cases": 420,
            "principal_boundary_cases": 120,
            "zero_shift_mixed_cases": 96,
        }
    )
    checks["independent_4400_of_4400"] = (
        independent["all_passed"]
        and independent["checks_passed"] == independent["checks_total"] == 4400
        and independent["coverage"]
        == {
            "direct_connection_transport_cases": 144,
            "direct_metric_cases": 320,
            "independent_endpoint_inverse_cases": 44,
        }
        and "no production import or result read" in independent["method"]
    )
    checks["hostile_16_of_16"] = (
        hostile["all_passed"]
        and hostile["catches_passed"] == hostile["catches_total"] == 16
        and hostile["validator_shared_by_baseline_and_mutants"]
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
    audit = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    completeness = (root / "COMPLETENESS_MAP.md").read_text(encoding="utf-8")

    checks["analytic_global_inverse"] = all(
        token in exact
        for token in (
            "## 3. Global endpoint inverse",
            "continuously and strictly increasingly onto every",
            "Every mixed `(q_X,q_perp)` has exactly one `(T_r,lambda)`",
            "This is an analytic global result",
        )
    )
    checks["endpoint_rank_and_principal_charts"] = (
        "\\mathcal D=" in exact
        and "Consequently the mixed two-variable endpoint determinant is" in exact
        and "Thus the future null cone is an immersion throughout the mixed\nstratum" in exact
        and "polar-coordinate degeneracy, not\ngeometric rank loss" in exact
        and "Both\nprincipal limits are therefore regular in nonsingular direction charts" in exact
    )
    checks["no_caustic_scope_is_bounded"] = (
        "no positive-time interior conjugate caustic on this supplied universal-cover cone"
        in exact
        and "it is not a theorem for generic G332 developments or perturbed metrics" in exact
        and "generic_spacetime_stability\tOPEN" in ledger
        and "metric perturbations" in completeness
    )
    checks["compact_multiplicity_path_labelled"] = (
        "countable path-labelled family" in exact
        and "not a multivalued inverse within one lift" in exact
        and "branch crossing/cut tie is not a\nconjugate caustic" in exact
        and hostile["checks"]["deleted_winding"]
        and hostile["checks"]["branch_crossing_conflation"]
    )
    checks["screen_carry_and_quotient_distinguished"] = (
        "The natural\nscreen-quotient rotation is zero" in exact
        and "This does not make\nthe full transported source pair plane equal" in exact
        and "G269_endpoint_clock_mismatch\tDERIVED_CONDITIONAL_BOUNDED\tnonzero exactly on mixed rays"
        in ledger
        and hostile["checks"]["invented_screen_rotation"]
        and hostile["checks"]["pair_plane_conflation"]
    )
    checks["zero_shift_full_relation_active"] = (
        "At the zero-shift direction (19), `delta=0` while `W` is nonzero" in exact
        and "a quiet redshift channel does not mean the\nwhole observer relation is quiet" in lay
        and hostile["checks"]["zero_shift_relation_erasure"]
    )
    checks["reversal_and_signed_depth_typed"] = (
        "Under mathematical reversal" in exact
        and "a later physical return remains a separate future leg" in exact
        and hostile["checks"]["frequency_orientation_reversal"]
        and hostile["checks"]["signed_depth_distance_conflation"]
    )
    checks["metric_kernel_equation_unchanged"] = (
        "metric_kernel_angular_equation\tUNCHANGED" in ledger
        and "metric, completed-pair kernel, angular sector, and provisional equation are unchanged"
        in exact
    )
    checks["no_light_route_scale_selection"] = (
        "electromagnetic_light_model\tNOT_USED" in ledger
        and "physical_route_distance_population\tOPEN" in ledger
        and "scale_Xmax\tOPEN" in ledger
        and hostile["checks"]["light_model_import"]
        and hostile["checks"]["physical_route_selection"]
        and hostile["checks"]["scale_xmax_promotion"]
        and "does not say which route Nature populates" in lay
    )
    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_acceptance_authenticated"] = (
        digest(external_path)
        == "8b9276c4937ade7c823d6caf74e0ac841d7c70993f3af3986f151a5825a9393c"
        and external.rstrip().endswith(
            "ACCEPT_G341_BOUNDED_NONPRINCIPAL_NULL_RELATION_AND_SCREEN_CARRY"
        )
        and "No findings at high, medium, or low severity" in external
        and "implementation-distinct" in external
        and "not premise-independent" in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_authenticated"] = (
        "30 manifest payloads" in transmission
        and "fab22d4eea96f1080aa8daf9a8dbb37b4f0cc0f91a291a775ab7b0c09fbe0bd4"
        in transmission
        and "1860832f56889b2ec0246e0dfb535525dc3fd6b6728b6ac63cfc9ba76c67fb53"
        in transmission
        and "268a2f4c871fc1f4e56520f21ad99e03621f5516e153810a03de6be44aafef27"
        in transmission
        and "8b9276c4937ade7c823d6caf74e0ac841d7c70993f3af3986f151a5825a9393c"
        in transmission
        and "ACCEPT_G341_BOUNDED_NONPRINCIPAL_NULL_RELATION_AND_SCREEN_CARRY"
        in transmission
    )
    checks["evidence_reports_agree"] = (
        "production checks: `8992/8992`" in audit
        and "implementation-distinct direct metric/Christoffel checks: `4400/4400`" in audit
        and "hostile mutations caught: `16/16`" in audit
        and "G341 selects preregistered alternative A" in audit
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
        ("derive_nonprincipal_relation.py", '"checks_total": 8992'),
        ("verify_nonprincipal_independent.py", '"checks_total": 4400'),
        ("run_catch_proofs.py", '"catches_total": 16'),
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
