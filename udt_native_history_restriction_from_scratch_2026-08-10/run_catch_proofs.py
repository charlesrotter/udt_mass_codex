#!/usr/bin/env python3
"""Fail-closed algebraic, ownership, and scope catches for the G61 audit."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-only", action="store_true")
    args = parser.parse_args()

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    with (HERE / "OWNER_CLASSIFICATION.tsv").open(newline="", encoding="utf-8") as stream:
        owners = list(csv.DictReader(stream, delimiter="\t"))
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))

    classes = {row["candidate_id"]: row["classification"] for row in owners}
    catches = {
        "F01_all_ten_components_and_nonzero_jacobian": (
            "det(dg/dq)=16 L T^3 u^5 w^6" in exact and result["exact_check_count"] == 14
        ),
        "F02_regular_domain_explicit": (
            "positive screen" in exact and "A00<0" in exact and "det A<0" in exact
        ),
        "F03_finite_jet_prolongation_explicit": (
            "det J^k F" in exact and "exponents are `5` at first jet and `15` at second jet" in exact
        ),
        "F04_identities_not_dynamics": (
            classes["O02"] == "IDENTITY_FOR_ALL_REGULAR_HISTORIES"
            and "calling Maurer--Cartan or Bianchi compatibility an evolution law" in exact
        ),
        "F05_natural_tensor_not_silently_zeroed": (
            "Constructing `Ric(g)` or `C(g)` is not the same act" in exact
        ),
        "F06_composition_not_bulk_equation": (
            classes["O03"] == "CONDITIONAL_COMPARISON_RULE"
            and "It does not select the ambient metric\nmovie" in exact
        ),
        "F07_cE_not_derivative_selector": "`c_E` calibrates" in exact and "no\nderivative" in exact,
        "F08_Xmax_not_local_PDE_or_wall": (
            "not a material wall or variational boundary" in exact
        ),
        "F09_boundary_not_interior_operator": (
            "boundary data without\nan interior operator leave infinitely many interiors" in exact
            and "g_epsilon=g+epsilon chi h" in exact
        ),
        "F10_R17_not_universal": (
            "but do\nnot select R17" in exact
            and classes["O05"] == "GLOBAL_OR_BOUNDARY_RESTRICTION_ONLY"
        ),
        "F11_bootstrap_inactive": "Bootstrap remains a working hypothesis and is inactive" in prereg,
        "F12_negative_is_source_bounded": (
            "source-bounded structural result" in report and "not a no-go theorem" in report
        ),
        "F13_no_downstream_physics": (
            "No action, source, carrier, matter, mass" in exact
        ),
        "F14_protected_and_stopped_absent": (
            len(sources) == 10
            and not any(
                "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" in row["path"]
                or "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" in row["path"]
                for row in sources
            )
        ),
        "F15_landing_is_component_and_source_bounded": (
            "ON_THE_DECLARED_POSITIVE_SCREEN_TIME_ORIENTED_COMPONENT" in exact
            and "IN_THE_TEN_FROZEN_SOURCES" in report
        ),
        "F16_boundary_germ_not_global_causality": (
            "full boundary germ" in exact
            and "does **not** automatically preserve chronology, global hyperbolicity, causal\nfaithfulness" in exact
        ),
    }
    failed = sorted(key for key, value in catches.items() if not value)
    output = {
        "schema_version": 1,
        "catch_count": len(catches),
        "caught_count": len(catches) - len(failed),
        "failed": failed,
        "catches": catches,
    }
    if not args.read_only:
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(output, indent=2, sort_keys=True))
    assert not failed, failed


if __name__ == "__main__":
    main()
