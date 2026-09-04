#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the bounded G343 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


PREREGISTRATION_COMMIT = "71db75f4"
LANDING = (
    "FULL_BILOCAL_PHASE_SPACE_PROPAGATOR_CLOSES__EXACT_COMPOSITION_SYMPLECTICITY"
    "__COMMON_AFFINE_INVERSE_AND_SOURCE_NORMALIZED_FREQUENCY_RECIPROCITY"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
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
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    checks["production_8888_of_8888"] = (
        production["status"] == "PASS"
        and production["assertions"] == 8888
        and production["failed"] == []
        and production["selected_alternatives"] == ["A", "C1", "W1", "R1", "P1", "Q1"]
        and production["maxima"]["composition_relative_error"] < 5e-9
        and production["maxima"]["reference_event_covariance_relative_error"] < 5e-9
    )
    checks["independent_2960_of_2960"] = (
        independent["status"] == "PASS"
        and independent["assertions"] == 2960
        and independent["failed"] == []
        and "coordinate metric two-jet curvature" in independent["method"]
        and independent["maxima"]["curvature_relative_error"] < 2e-10
        and independent["maxima"]["ode_fundamental_relative_error"] < 2e-7
    )
    checks["hostile_13_of_13"] = (
        hostile["all_passed"]
        and hostile["catches_passed"] == hostile["catches_total"] == 13
        and hostile["validator_shared_by_baseline_and_mutants"]
        and hostile["checks"]["hidden_unit_reference_scale"]
    )
    checks["landing_agreement"] = production["landing"] == hostile["landing"] == LANDING
    checks["corrected_preregistration_commit"] = production["preregistration_commit"] == PREREGISTRATION_COMMIT

    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    execution = (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")

    checks["dimensionally_typed_direction_chart"] = all(token in exact for token in (
        "rho={T_*^2\\over T_*^2+\\lambda^2}",
        "nu=\\left.{dT\\over ds}\\right|_{T_*}",
        "Because `lambda` has the same dimension as `T`",
    ))
    checks["full_bilocal_blocks"] = all(token in exact for token in (
        "B_j(T_1,T_0)", "A_j=r_j-\\mu_j(T_0)B_j",
        "C_j=\\mu_j(T_1)r_j-\\mu_j(T_0)D_j", "M(T_1,T_0)=",
    ))
    checks["composition_and_symplecticity"] = all(token in exact for token in (
        "M(T_2,T_0)=M(T_2,T_1)M(T_1,T_0)", "M^TJM=J", "\\det M=1",
    ))
    checks["reference_event_covariance"] = all(token in exact for token in (
        "rho'={T_*'^2\\over T_*'^2+\\lambda^2}", "nu'=\\alpha(T_*')",
        "reference-event covariance", "not a selected scale",
    ))
    checks["typed_endpoint_reciprocity"] = all(token in exact for token in (
        "M(T_0,T_1)=M(T_1,T_0)^{-1}",
        "M^{[1]}(T_0,T_1)", "-\\alpha_{01}\\,[B^{[0]}(T_1,T_0)]^T",
        "Multiplying independently source-normalized vertex maps",
    ))
    checks["principal_limits_and_g342_recovery"] = all(token in exact for token in (
        "reduce exactly to G342's", "On the longitudinal family `rho=1`",
        "On the transverse family `rho=0`", "Both principal phase spaces therefore retain",
    ))
    checks["compact_paths_not_selected"] = (
        "It does not identify, sum, weight, or\nselect distinct lifts" in exact
        and "physical_route_or_population\tOPEN" in (root / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    )
    checks["discarded_runs_preserved"] = all(token in execution for token in (
        "Those runs are not\naccepted as evidence", "undeclared `T_*=1` reference",
        "failed all 400 G342 vertex-recovery component checks", "2.861212942267234",
        "No production propagator formula",
    ))
    checks["bounded_claim_language"] = (
        "externally accepted bounded result" in lay
        and "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED" in exact
        and "ACCEPTED_WITHOUT_FINDING_OR_REPAIR" in ledger
        and "does not provide luminosity" in exact
        and "selects no universe" in audit
    )

    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_review_authenticated_and_accepted"] = (
        digest(external_path)
        == "31e14bc6c971f2dae0abd0a49519279d0d4b636e50c495330d22c9d8d008056d"
        and external.rstrip().endswith(
            "ACCEPT_G343_BOUNDED_BILOCAL_SCREEN_PHASE_SPACE_PROPAGATOR"
        )
        and "No findings at any severity" in external
        and "implementation-distinct, not premise-independent" in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_provenance"] = all(token in transmission for token in (
        "29 manifest payloads",
        "0c2cb7931977d6acbd144e7ef182042bf7ebcc28a28e33efba5f95477252ce54",
        "4e8aa802894af5b0c09ba9c65fa0190a1145c6f5951c3c8dfe9cce32d6e72f0d",
        "1368529bac9648b715f50c313cdc6918a4bc3b65b443feb7305441f563eae700",
        "31e14bc6c971f2dae0abd0a49519279d0d4b636e50c495330d22c9d8d008056d",
        "ACCEPT_G343_BOUNDED_BILOCAL_SCREEN_PHASE_SPACE_PROPAGATOR",
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
        ("derive_bilocal_propagator.py", '"assertions": 8888'),
        ("verify_bilocal_independent.py", '"assertions": 2960'),
        ("run_catch_proofs.py", '"catches_total": 13'),
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
