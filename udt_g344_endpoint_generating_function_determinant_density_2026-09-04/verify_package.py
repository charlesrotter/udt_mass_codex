#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the bounded G344 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


LANDING = (
    "GLOBAL_NONCOINCIDENT_QUADRATIC_SCREEN_ENDPOINT_GENERATOR_CLOSES"
    "__MIXED_HESSIAN_IS_A_TYPED_AFFINE_WEIGHTED_ENDPOINT_BIDENSITY"
    "__EXACT_STATIONARY_COMPOSITION_REVERSAL_REFERENCE_AND_SCREEN_COVARIANCE"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_LIGHT_FLUX_DISTANCE_PROBABILITY_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
PREREGISTRATION_COMMIT = "5c16ca60"
QUALIFICATION_COMMIT = "9701e595"
SCRIPT_HASHES = {
    "derive_endpoint_generator.py": "4cc4c58259e3bd6612556af8440eee0517cc40cfebd734a60fa7e97825fcb7d1",
    "verify_endpoint_generator_independent.py": "fb050e8f1fa8d877f4238116e61c67daf5e4d1d5907e1e1ed075161484e7af35",
    "run_catch_proofs.py": "727dff07ccc0861b80b962e77135eb280682a151554ffedd9c7cd50f005afcac",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def source_matches(repo: Path, source: str, expected: str) -> bool:
    direct = repo / source
    if direct.is_file() and digest(direct) == expected:
        return True
    sealed = repo / "sources" / source
    return sealed.is_file() and digest(sealed) == expected


def main() -> None:
    root = Path(__file__).resolve().parent
    repo = root.parent
    checks: dict[str, bool] = {}

    production = json.loads((root / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    checks["production_13580_of_13580"] = (
        production["status"] == "PASS"
        and production["assertions"] == 13580
        and production["failed"] == []
        and production["landing"] == LANDING
        and production["selected_alternatives"]
        == ["A", "C1", "R1", "A1", "S1", "P1", "Q1"]
        and production["maxima"]["hessian_identity_relative_error"] < 5.0e-9
        and production["maxima"]["generator_composition_relative_error"] < 5.0e-9
    )
    checks["independent_4882_of_4882"] = (
        independent["status"] == "PASS"
        and independent["assertions"] == 4882
        and independent["failed"] == []
        and "finite endpoint derivatives" in independent["method"]
        and independent["maxima"]["finite_mixed_hessian_relative_error"] < 3.0e-7
        and independent["maxima"]["action_integral_relative_error"] < 3.0e-7
    )
    checks["hostile_14_of_14"] = (
        hostile["status"] == "PASS"
        and hostile["caught"] == hostile["total"] == 14
        and hostile["failed"] == []
        and all(hostile["mutations"].values())
    )
    checks["preregistration_and_qualification_tokens"] = (
        production["preregistration_commit"] == PREREGISTRATION_COMMIT
        and PREREGISTRATION_COMMIT in (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
        and QUALIFICATION_COMMIT in (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    )
    checks["frozen_script_hashes"] = all(
        digest(root / name) == expected for name, expected in SCRIPT_HASHES.items()
    )

    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    note = (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    premise = (root / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")

    checks["analytic_B_invertibility"] = all(token in exact for token in (
        "B_j=0\\iff T_1=T_0", "\\det B=B_\\parallel B_Z>0",
        "one type-I generating chart covers the complete noncoincident domain",
    ))
    checks["generator_and_hessians"] = all(token in exact for token in (
        "S^0_{10}(x_1,x_0)", "p_1=+\\partial_{x_1}S^0_{10}",
        "K_{10}=-\\partial_{x_1}\\partial_{x_0}S^0_{10}=B^{-T}",
    ))
    checks["additive_endpoint_coboundary_qualified"] = all(token in exact + note + premise for token in (
        "k(T_1,T_0)=f(T_1)-f(T_0)", "CHOSE_GENERATOR_NORMALIZATION",
        "does not alter any G344 Hessian or density result",
    ))
    checks["stationary_composition_and_density"] = all(token in exact for token in (
        "H_1=B_{21}^{-1}A_{21}+D_{10}B_{10}^{-1}",
        "\\operatorname{stat}_{x_1}",
        "\\Delta_{20}={\\Delta_{21}\\Delta_{10}\\over|\\det H_1|}",
        "all six endpoint orderings",
    ))
    checks["reversal_and_affine_weights"] = all(token in exact for token in (
        "S^0_{01}(x_0,x_1)=-S^0_{10}(x_1,x_0)",
        "S^{0\\prime}=aS^0", "\\Delta'=a^2\\Delta",
        "conformally symplectic rather than canonical",
    ))
    checks["screen_bidensity_and_reference_covariance"] = all(token in exact for token in (
        "K'=R_1KR_0^T", "det(R_1)det(R_0)",
        "its determinant is a bidensity", "No reference\nevent becomes a hidden scale",
    ))
    checks["principal_limits_and_G342_recovery"] = all(token in exact for token in (
        "is exactly G342's source-normalized", "S^0_{10}={|x_1-x_0|^2\\over2\\ell}",
        "B_\\parallel={3\\over7\\kappa}", "neither principal family loses",
    ))
    checks["coincidence_and_compact_labels_typed"] = (
        "The pole is the standard boundary singularity" in exact
        and "Nothing in G344 sums, weights, identifies, or selects" in exact
        and "compact_lifts\tSUPPLIED_PATH_LABELS" in ledger
    )
    checks["bounded_nonphysical_language"] = (
        "not yet brightness" in lay
        and "light_flux_probability_distance\tOPEN_NOT_DERIVED" in ledger
        and "It is not a selected\nspacetime action" in audit
        and "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED" in exact
    )

    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_review_acceptance"] = (
        digest(external_path)
        == "c01f0f13bb08d0675d6d637c5960a1fd25963b287ada01cb45905283340c95ff"
        and external.rstrip().endswith(
            "ACCEPT_G344_BOUNDED_SCREEN_ENDPOINT_GENERATOR_AND_BIDENSITY"
        )
        and "No high-severity findings" in external
        and "No medium-severity findings" in external
        and "does not replace the analytic proof" in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_provenance"] = all(token in transmission for token in (
        "29 manifest payloads",
        "a3958fa39a20e1e3bab5bf977d963527df8a89d82cd16bd4ab92d0f3c525c6ee",
        "c12c583fb415d707f372f43073c8ba06f4e4731e241c833778e35e1774d9f1a3",
        "293d95dc9257b3ffe9bfcf7de39ba9168a67384a30726e3e226abe9842e76170",
        "c01f0f13bb08d0675d6d637c5960a1fd25963b287ada01cb45905283340c95ff",
        "ACCEPT_G344_BOUNDED_SCREEN_ENDPOINT_GENERATOR_AND_BIDENSITY",
    ))

    source_rows = (root / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
    checks["frozen_dependency_hashes"] = all(
        source_matches(repo, fields[0], fields[1])
        for fields in (line.split("\t") for line in source_rows if line.strip())
        if fields[1] != "NA_METHOD"
    )

    before = snapshot(root)
    environment = dict(os.environ)
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    replay_specs = (
        ("derive_endpoint_generator.py", '"assertions": 13580'),
        ("verify_endpoint_generator_independent.py", '"assertions": 4882'),
        ("run_catch_proofs.py", '"caught": 14'),
    )
    for script, token in replay_specs:
        replay = subprocess.run(
            [sys.executable, "-B", "-S", str(root / script)],
            cwd=root,
            env=environment,
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
