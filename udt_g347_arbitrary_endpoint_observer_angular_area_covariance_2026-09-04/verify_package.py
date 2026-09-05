#!/usr/bin/env python3
"""Dependency-free aggregate verifier for externally accepted bounded G347."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


LANDING = (
    "EXACT_FINITE_TIMELIKE_ENDPOINT_OBSERVER_COVARIANCE_CLOSES"
    "__QUOTIENT_SCREEN_ISOMETRY_AND_INVERSE_FREQUENCY_SKY_CONFORMALITY"
    "__SOURCE_DOPPLER_SQUARED_DIRECTIONAL_AREAS"
    "__SQUARED_FREQUENCY_REVERSAL_INVERSE_G345_MEAN_AND_STATIONARY_SEWING_RETAIN_COVARIANT_FORM"
    "__NO_PREFERRED_OBSERVER_LIGHT_DISTANCE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
PREREGISTRATION_COMMIT = "c80d2666"
SCRIPT_HASHES = {
    "derive_endpoint_observer_covariance.py":
        "a25d55ff60edb46f790605c7386f1296f8f50abefd3f4b1d20ad9a42a81156e6",
    "verify_endpoint_observer_covariance_independent.py":
        "5514ba62b890bd6b1b6ac41cf9b97e4a5fcd322d9c699e71fb031db7e6f2f152",
    "run_catch_proofs.py":
        "63e72797a10758cd16e4410e879634d1ebbc536cc725d858105d12c6ea657e3b",
}
SOURCE_HASHES = {
    "udt_g340_finite_separated_normal_observer_relations_2026-09-03/EXACT_DERIVATION.md":
        "1c8998906a354b26d18dd2fd307564b158d74bdd52c865daa6b0f0300378740f",
    "udt_g343_bilocal_screen_phase_space_propagator_2026-09-04/EXACT_DERIVATION.md":
        "b295455e2835e3a04de7e91dbafb61ba0b0cef0f1eaea338c90cfe8a1cab5051",
    "udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md":
        "e59887e92b055cc18a8215ae6acbbf88528d1371b2afcc03371935c574079722",
    "udt_g346_directional_angular_area_reciprocity_2026-09-04/EXACT_DERIVATION.md":
        "e406301ea81b617dd971d1f1818ce2cfc402e6fa0f91a2925162992f1047c534",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def source_matches(repo, root, source, expected):
    candidates = (repo / source, root / "sources" / source, root.parent / "sources" / source)
    return any(path.is_file() and digest(path) == expected for path in candidates)


def main():
    root = Path(__file__).resolve().parent
    repo = root.parent
    checks = {}
    production = json.loads((root / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    checks["production_73924_of_73924"] = (
        production["status"] == "PASS"
        and production["assertions"] == 73924
        and production["failed"] == []
        and production["landing"] == LANDING
        and production["preregistration_commit"] == PREREGISTRATION_COMMIT
        and production["near_null_boosts"] >= 1000
        and production["noninvariant_examples"] >= 500
        and production["selected_alternatives"]
        == ["A", "Q1", "S1", "A1", "R1", "G1", "N1", "B1", "P1"]
    )
    checks["independent_23547_of_23547"] = (
        independent["status"] == "PASS"
        and independent["assertions"] == 23547
        and independent["failed"] == []
        and independent["finite_difference_cases"] >= 50
        and independent["near_null_cases"] >= 300
        and "imports no production" in independent["method"]
    )
    checks["hostile_22_of_22"] = (
        hostile["status"] == "PASS"
        and hostile["caught"] == hostile["total"] == 22
        and hostile["failed"] == []
        and all(hostile["mutations"].values())
    )
    checks["frozen_script_hashes"] = all(
        digest(root / name) == expected for name, expected in SCRIPT_HASHES.items()
    )
    checks["frozen_source_hashes"] = all(
        source_matches(repo, root, source, expected)
        for source, expected in SOURCE_HASHES.items()
    )

    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    note = (root / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    premise = (root / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")

    checks["preregistered_without_retuning"] = (
        PREREGISTRATION_COMMIT in note
        and "No candidate\nformula, alternative, tolerance, domain, or maximum conclusion was changed"
        in note
        and "outcomes unseen" in (root / "PREREGISTRATION.md").read_text(encoding="utf-8")
    )
    checks["quotient_screen_isometry"] = all(token in exact for token in (
        "Q_k=k^\\perp/\\operatorname{span}(k)",
        "I_{v\\leftarrow u}X",
        "metric isometry",
        "I_{w\\leftarrow v}I_{v\\leftarrow u}=I_{w\\leftarrow u}",
    ))
    checks["sky_frequency_conformality"] = all(token in exact for token in (
        "\\theta_v=\\delta s_v",
        "{\\omega_u\\over\\omega_v}I_{v\\leftarrow u}\\theta_u",
        "d\\Omega_v",
        "\\gamma(1-\\beta\\mathbin\\cdot s_u)",
    ))
    checks["source_doppler_squared_areas"] = all(token in exact for token in (
        "\\mathscr A'_{1\\leftarrow0}=D_0^2",
        "\\mathscr A'_{0\\leftarrow1}=D_1^2",
        "source endpoint, not the target endpoint",
        "not numerically observer invariant",
    ))
    checks["reversal_and_G345_covariance"] = all(token in exact for token in (
        "{\\omega_{v_0}\\over\\omega_{v_1}}",
        "\\widehat\\Delta'_{10}",
        "{\\widehat\\Delta_{10}\\over D_0D_1}",
        "={1\\over\\widehat\\Delta'_{10}}",
    ))
    checks["stationary_sewing_covariance"] = all(token in exact for token in (
        "\\widehat h'_1={\\widehat h_1\\over D_1^2}",
        "\\mathscr A'_{2\\leftarrow0}",
        "Bare multiplication remains false",
    ))
    checks["finite_boost_boundary"] = all(token in exact for token in (
        "Every finite `|\\beta|<1` gives `D>0`",
        "`D\\to0`",
        "A null vector is not a unit timelike observer",
    ))
    checks["scope_and_premise_guard"] = (
        "It does **not** yet say which observers or routes are physically populated" in lay
        and "owner-provisional" in audit
        and "OWNER_ADOPTED_PROVISIONAL_POSTULATES_NOT_CANON" in premise
        and "Charles alone canonizes" in premise
        and "External acceptance does not widen this bounded scope" in audit
    )
    checks["native_not_imported_optics"] = (
        "no external aberration or optical theorem" in exact
        and "Textbook aberration, Etherington reciprocity" in audit
        and "were not used" in audit
    )
    checks["compact_labels_not_aggregated"] = (
        "Nothing here sums, weights, identifies, or selects lifts" in exact
        and "all lift labels retained separately" in premise
    )

    external_path = root / "EXTERNAL_REVIEW_RESPONSE.md"
    external = external_path.read_text(encoding="utf-8")
    checks["external_review_acceptance"] = (
        digest(external_path)
        == "af2e0a6612cac8a4b0a090927ae4b84a9338fef3ee60d694e86c05521b11ac4d"
        and external.rstrip().endswith(
            "ACCEPT_G347_BOUNDED_ENDPOINT_OBSERVER_COVARIANCE"
        )
        and "mathematically correct on the sealed premises" in external
        and "None changes a formula or requires repair" in external
    )
    transmission = (root / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    checks["external_transmission_provenance"] = all(token in transmission for token in (
        "30-file intake",
        "gpt-5.4",
        "gpt-5.6-sol",
        "20ea825280901a140f01cd425676d8519f765fd874d6fb37a8f81b1255abad8e",
        "727492d6f4d21d315cff136d2289f452a864397df78f13d02eff8b660587891f",
        "9799dd3ab5a153a1be91dd9375d646ede0edf9358549e4587c3f3c274ab75e21",
        "af2e0a6612cac8a4b0a090927ae4b84a9338fef3ee60d694e86c05521b11ac4d",
        "ACCEPT_G347_BOUNDED_ENDPOINT_OBSERVER_COVARIANCE",
    ))

    before = snapshot(root)
    environment = dict(os.environ)
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    replays = (
        ("derive_endpoint_observer_covariance.py", '"assertions": 73924'),
        ("verify_endpoint_observer_covariance_independent.py", '"assertions": 23547'),
        ("run_catch_proofs.py", '"caught": 22'),
    )
    for script, token in replays:
        completed = subprocess.run(
            [sys.executable, "-B", "-S", str(root / script)],
            cwd=root,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        checks["no_write_replay_" + script] = completed.returncode == 0 and token in completed.stdout
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
