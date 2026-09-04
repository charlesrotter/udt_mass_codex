#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the bounded G345 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


LANDING = (
    "OBSERVER_CALIBRATED_ENDPOINT_SCREEN_DETERMINANT_SCALAR_CLOSES"
    "__UNIQUE_IN_THE_SYMMETRIC_FIRST_POWER_FREQUENCY_MONOMIAL_CLASS"
    "__EXACT_AFFINE_REFERENCE_GL2_REVERSAL_AND_STATIONARY_SEWING"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_LIGHT_FLUX_LUMINOSITY_PROBABILITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
PREREGISTRATION_COMMIT = "d22f1bdb"
QUALIFICATION_COMMIT = "f20a5072"
SCRIPT_HASHES = {
    "derive_screen_scalar.py": "a4da2b7d1a534dd97b6f040aac98270b75cd3bdb007a6d6ac85ed8994b983dec",
    "verify_screen_scalar_independent.py": "4bf6825a081ac1ba72ae03fc64ab4be7cd3f9cc184aa5ba2badfb93ace401fbb",
    "run_catch_proofs.py": "37e803384bfa322260b19bdcfc0711df472acc038aa4de03ae6609fcf76f9f4b",
}
SOURCE_HASHES = {
    "udt_g340_finite_separated_normal_observer_relations_2026-09-03/EXACT_DERIVATION.md":
        "1c8998906a354b26d18dd2fd307564b158d74bdd52c865daa6b0f0300378740f",
    "udt_g342_full_null_jacobi_beam_area_2026-09-04/EXACT_DERIVATION.md":
        "3906be2e481e04d705715743ce1f73b9ba323742cf9a6cdac57daa3e7e4df9d6",
    "udt_g343_bilocal_screen_phase_space_propagator_2026-09-04/EXACT_DERIVATION.md":
        "b295455e2835e3a04de7e91dbafb61ba0b0cef0f1eaea338c90cfe8a1cab5051",
    "udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md":
        "8af5dd5dfdb259bcafd184155664792c9f6f027428202e3e69039735a604687a",
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


def main():
    root = Path(__file__).resolve().parent
    repo = root.parent
    checks = {}

    production = json.loads((root / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    checks["production_9824_of_9824"] = (
        production["status"] == "PASS"
        and production["assertions"] == 9824
        and production["failed"] == []
        and production["landing"] == LANDING
        and production["preregistration_commit"] == PREREGISTRATION_COMMIT
        and production["selected_alternatives"]
        == ["A", "U1", "N1", "C1", "R1", "S1", "Q1"]
        and max(production["maxima"].values()) < 7.0e-9
    )
    checks["independent_4360_of_4360"] = (
        independent["status"] == "PASS"
        and independent["assertions"] == 4360
        and independent["failed"] == []
        and "reference-free" not in independent["method"].lower()
        and "lambda-gamma fundamental basis" in independent["method"]
        and max(independent["maxima"].values()) < 2.0e-7
    )
    checks["hostile_17_of_17"] = (
        hostile["status"] == "PASS"
        and hostile["caught"] == hostile["total"] == 17
        and hostile["failed"] == []
        and all(hostile["mutations"].values())
    )
    checks["frozen_script_hashes"] = all(
        digest(root / name) == expected for name, expected in SCRIPT_HASHES.items()
    )
    checks["frozen_source_hashes"] = all(
        source_matches(repo, source, expected) for source, expected in SOURCE_HASHES.items()
    )

    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    prereg = (root / "PREREGISTRATION.md").read_text(encoding="utf-8")
    note = (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    premise = (root / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")

    checks["preregistration_token_and_execution_repair"] = (
        PREREGISTRATION_COMMIT in audit
        and PREREGISTRATION_COMMIT in note
        and QUALIFICATION_COMMIT in audit
        and "9822/9824" in note
        and "two-scale consistency" in note
        and "No candidate formula" in note
    )
    checks["affine_weight_derivation"] = all(token in exact for token in (
        "\\widehat K_{10}={K_{10}\\over\\sqrt{\\omega_1\\omega_0}}",
        "\\widehat\\Delta_{10}",
        "2+a+b=0", "a=b=-1",
    ))
    checks["general_screen_scalar_derivation"] = all(token in exact for token in (
        "x_i'=R_i x_i", "K_{10}'=R_1^{-T}K_{10}R_0^{-1}",
        "q_i'=R_i^{-T}q_iR_i^{-1}", "metric induced",
    ))
    checks["reversal_and_endpoint_reset"] = all(token in exact for token in (
        "\\widehat K_{01}=-\\widehat K_{10}^T",
        "B_{01}^{[1]}=-\\alpha_{01}",
        "\\Delta_{01}^{[1]}={\\Delta_{10}^{[0]}\\over\\alpha_{01}^2}",
    ))
    checks["stationary_composition_typed"] = all(token in exact for token in (
        "H_1=B_{21}^{-1}B_{20}B_{10}^{-1}",
        "\\widehat h_1", "\\widehat\\Delta_{20}",
        "Bare multiplication is false", "all six endpoint orderings",
    ))
    checks["reference_free_and_principal_formulas"] = all(token in exact for token in (
        "J_\\parallel", "(T_0^2+\\lambda^2)(T_1^2+\\lambda^2)",
        "\\widehat\\Delta_X", "\\widehat\\Delta_\\perp",
        "|T_1-T_0|^{-2}",
    ))
    checks["scope_and_nonuniqueness_guard"] = (
        "does **not** select a unique physical observable" in exact
        and "not yet\n+brightness" not in lay
        and "It is not yet\nbrightness" in lay
        and "physical_observable_uniqueness\tOPEN_NOT_DERIVED" in ledger
        and "OWNER_ADOPTED_PROVISIONAL_POSTULATES_NOT_CANON" in premise
        and "Charles alone canonizes" in premise
    )
    checks["no_forbidden_physical_promotion"] = all(token in exact + lay + audit for token in (
        "not yet", "not a physical light-transfer", "No luminosity", "does not choose a path",
    ))

    before = snapshot(root)
    environment = dict(os.environ)
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    replay_specs = (
        ("derive_screen_scalar.py", '"assertions": 9824'),
        ("verify_screen_scalar_independent.py", '"assertions": 4360'),
        ("run_catch_proofs.py", '"caught": 17'),
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
