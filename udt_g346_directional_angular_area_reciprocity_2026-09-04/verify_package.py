#!/usr/bin/env python3
"""Dependency-free aggregate verifier for the externally accepted bounded G346 package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


LANDING = (
    "TWO_DIRECTIONAL_METRIC_ANGULAR_AREA_JACOBIANS_CLOSE"
    "__SQUARED_FREQUENCY_REVERSAL_AND_INVERSE_G345_GEOMETRIC_MEAN"
    "__EXACT_AFFINE_REFERENCE_GL2_ENDPOINT_RESET_AND_STATIONARY_SEWING"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_BRIGHTNESS_FLUX_LUMINOSITY_PROBABILITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
PREREGISTRATION_COMMIT = "9a037558"
SCRIPT_HASHES = {
    "derive_directional_angular_area.py":
        "f119ed163f1113c3fe6ba4c6a19a6e3f2a682e678473bc4196190d25d6c2c143",
    "verify_directional_angular_area_independent.py":
        "73c9aee78fa5cad7b008db824b0c0c754dfbe48675a5a1b1284f4c316bd91520",
    "run_catch_proofs.py":
        "4f726b57e08bc71f22397048915361cbcfb73a69ce1b1356afdc93b279552ead",
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
    "udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md":
        "e59887e92b055cc18a8215ae6acbbf88528d1371b2afcc03371935c574079722",
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

    checks["production_11204_of_11204"] = (
        production["status"] == "PASS"
        and production["assertions"] == 11204
        and production["failed"] == []
        and production["landing"] == LANDING
        and production["preregistration_commit"] == PREREGISTRATION_COMMIT
        and production["selected_alternatives"]
        == ["A", "R1", "G1", "C1", "S1", "N1", "Q1"]
        and max(production["maxima"].values()) < 8.0e-9
    )
    checks["independent_4251_of_4251"] = (
        independent["status"] == "PASS"
        and independent["assertions"] == 4251
        and independent["failed"] == []
        and "RK4 Jacobi integration" in independent["method"]
        and "imports no production" in independent["method"]
        and max(independent["maxima"].values()) < 2.5e-7
    )
    checks["hostile_20_of_20"] = (
        hostile["status"] == "PASS"
        and hostile["caught"] == hostile["total"] == 20
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
    note = (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    ledger = (root / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    premise = (root / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")

    checks["preregistration_and_no_retuning"] = (
        PREREGISTRATION_COMMIT in audit
        and PREREGISTRATION_COMMIT in note
        and "No formula, tolerance, alternative" in note
        and "18/19" in note
        and "cannot contain the hash" in note
    )
    checks["metric_sky_and_area_derivation"] = all(token in exact for token in (
        "p_i=\\omega_i q_i\\theta_i",
        "d\\Omega_i=\\sqrt{\\det q_i}",
        "dA_i=\\sqrt{\\det q_i}",
        "No intensity, luminosity, detector",
    ))
    checks["directional_formulas"] = all(token in exact for token in (
        "\\mathscr A_{1\\leftarrow0}",
        "\\omega_0^2|\\det B_{10}|",
        "\\mathscr A_{0\\leftarrow1}",
        "\\omega_1^2|\\det B_{01}|",
    ))
    checks["general_screen_covariance"] = all(token in exact for token in (
        "x_i'=R_ix_i", "p_i'=R_i^{-T}p_i",
        "q_i'=R_i^{-T}q_iR_i^{-1}", "B_{10}'=R_1B_{10}R_0^T",
    ))
    checks["frequency_reversal_and_endpoint_reset"] = all(token in exact for token in (
        "B_{01}=-B_{10}^T",
        "\\left({\\omega_0\\over\\omega_1}\\right)^2",
        "B_{01}^{[1]}=-\\alpha_{01}",
        "=\\alpha_{01}^2\\mathscr A_{1\\leftarrow0}^{[0]}",
    ))
    checks["inverse_G345_geometric_mean"] = all(token in exact for token in (
        "\\widehat\\Delta_{10}",
        "\\sqrt{\\mathscr A_{1\\leftarrow0}\\mathscr A_{0\\leftarrow1}}",
        "={1\\over\\widehat\\Delta_{10}}",
        "symmetric geometric mean",
    ))
    checks["stationary_sewing_typed"] = all(token in exact for token in (
        "H_1=B_{21}^{-1}B_{20}B_{10}^{-1}",
        "\\widehat h_1", "\\mathscr A_{2\\leftarrow0}",
        "Bare multiplication is false", "outer endpoints coincide",
    ))
    checks["mixed_principal_and_coincidence"] = all(token in exact for token in (
        "J_\\parallel", "\\mathscr G_{10}",
        "\\mathscr A_{1\\leftarrow0,X}",
        "\\mathscr A_{1\\leftarrow0,\\perp}",
        "|\\epsilon|^2(1+O(\\epsilon))",
    ))
    checks["scope_and_premise_guard"] = (
        "External acceptance does not widen any of these boundaries" in exact
        and "does **not** do" in lay
        and "OWNER_ADOPTED_PROVISIONAL_POSTULATES_NOT_CANON" in premise
        and "Charles alone canonizes" in premise
        and "OPEN_NOT_DERIVED" in ledger
        and "No optical reciprocity theorem" in audit
    )
    checks["compact_labels_not_aggregated"] = (
        "Nothing in G346 sums, weights, identifies, or physically selects lifts" in exact
        and "compact_lifts\tSUPPLIED_PATH_LABELS" in ledger
    )

    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_review_acceptance"] = (
        digest(external_path)
        == "798633026df1ca03249900c57a4c4cf3848a8590fe4ef2f58617f63c4bef6199"
        and external.rstrip().endswith(
            "ACCEPT_G346_BOUNDED_DIRECTIONAL_ANGULAR_AREA_RECIPROCITY"
        )
        and "No blocking mathematical defect was found" in external
        and "integrity scaffolding rather than substantive derivations" in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_provenance"] = all(token in transmission for token in (
        "29 manifest payloads",
        "a2c611e69e21535486f23a5578093517236e5edd32d24960008b217dd77f9751",
        "3ebe8c9072785d505e5369483d4f4ec54bcde0cc9e44c8c95039021cd8c89c5b",
        "35dc7923680c95039aaa55913d7d8db8b75a840a3866d57c00fba64c801a5f8e",
        "798633026df1ca03249900c57a4c4cf3848a8590fe4ef2f58617f63c4bef6199",
        "ACCEPT_G346_BOUNDED_DIRECTIONAL_ANGULAR_AREA_RECIPROCITY",
    ))

    before = snapshot(root)
    environment = dict(os.environ)
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    replay_specs = (
        ("derive_directional_angular_area.py", '"assertions": 11204'),
        ("verify_directional_angular_area_independent.py", '"assertions": 4251'),
        ("run_catch_proofs.py", '"caught": 20'),
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
        "review_status": "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
