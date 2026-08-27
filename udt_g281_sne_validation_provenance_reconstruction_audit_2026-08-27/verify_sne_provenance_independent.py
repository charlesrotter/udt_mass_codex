#!/usr/bin/env python3
"""Independent, deliberately smaller cross-check of the G281 landing."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def table(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    routes = table("ROUTE_PROVENANCE_MATRIX.tsv")
    census = table("HISTORICAL_CLAIM_CENSUS.tsv")
    status = {row["id"]: row for row in table("STATUS_LEDGER.tsv")}

    # An independent operational test of the old one-factor versus two-factor distinction.
    redshift = 2.75
    areal_distance = 17.0
    old_one_factor = redshift * areal_distance
    transparent_two_factor = redshift * redshift * areal_distance

    # The empirical lineage must contain both the original overclaim and later reconstruction route.
    classes = {row["current_class"] for row in census}
    failed_prediction_gates = []
    for row in routes:
        gates = (
            row["profile_or_history_fixed_before_SNe"],
            row["physical_query_branch_fixed"],
            row["native_area_from_same_history"],
            row["transfer_native_or_explicitly_conditional"],
            row["no_data_shaped_profile_or_basis"],
            row["holdout_not_used_for_selection"],
        )
        if row["maximum_class"] == "NATIVE_PREDICTION" and not all(value == "YES" for value in gates):
            failed_prediction_gates.append(row["route"])

    g189 = (
        ROOT / "udt_g189_p1_free_metric_flux_interface_2026-08-20/AUDIT_REPORT.md"
    ).read_text()
    g278_result = json.loads(
        (
            ROOT
            / "udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/DERIVATION_RESULT.json"
        ).read_text()
    )
    g279 = (
        ROOT / "udt_g279_native_kernel_observational_interface_provenance_audit_2026-08-27/AUDIT_REPORT.md"
    ).read_text()

    checks = {
        "one_factor_and_two_factor_are_not_equivalent": not math.isclose(
            old_one_factor, transparent_two_factor
        ),
        "their_ratio_is_exactly_Z": math.isclose(
            transparent_two_factor / old_one_factor, redshift, rel_tol=0.0, abs_tol=1e-15
        ),
        "historical_overclaim_class_present": "SCAFFOLDED_OR_OVERCLAIMED" in classes,
        "empirical_reconstruction_class_present": "EMPIRICAL_RECONSTRUCTION" in classes,
        "no_invalid_native_prediction_gate": not failed_prediction_gates,
        "status_separates_redshift_from_area": (
            "does_not_determine_areal_or_optical_distance" in status["S01"]["forbidden_upgrade"]
        ),
        "p1_free_control_does_not_close_prediction": (
            "P1 is exactly one supplied" in g189
            and "It does not reject completed-pair" in g189
            and "IMPORTED_CONDITIONAL" in g189
        ),
        "g278_landing_is_resolution_sensitive": (
            g278_result["landing"] == "SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE"
        ),
        "g278_did_not_retune_kernel": g278_result["frozen"]["kernel_retuned"] is False,
        "g279_declares_observational_imports": (
            "transparent radiative transfer" in g279
            and "chosen finite hat basis" in g279
            and "published Cepheid ladder" in g279
        ),
    }
    if not all(checks.values()):
        raise AssertionError(
            json.dumps(
                {
                    "checks": checks,
                    "failed": [name for name, passed in checks.items() if not passed],
                    "failed_prediction_gates": failed_prediction_gates,
                },
                indent=2,
                sort_keys=True,
            )
        )
    print(
        json.dumps(
            {
                "audit": "G281_INDEPENDENT_PROVENANCE_CROSSCHECK",
                "status": "PASS",
                "checks": checks,
                "operational_control": {
                    "Z": redshift,
                    "R": areal_distance,
                    "old_one_factor": old_one_factor,
                    "transparent_two_factor": transparent_two_factor,
                    "ratio": transparent_two_factor / old_one_factor,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
