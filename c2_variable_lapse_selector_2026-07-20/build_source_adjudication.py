#!/usr/bin/env python3
"""Build one explicit adjudication row per load-bearing source."""

from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent

FOUNDATION = {
    "CANON.md": ("canon/control ledger", "MIXED_DATE_CONTROL", "current owner locks only after later controls", "pre-July science cannot affirm post-firewall physics", "SCOPE_HISTORY_ONLY"),
    "LIVE.md": ("controlling state", "CURRENT_CONTROL", "frontier and authority boundary", "not load-bearing algebra", "CONTROLLING_SCOPE"),
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": ("C0 foundation", "HARD_FROZEN_OWNER_PACKET", "exact supplied foundation", "no historical import", "FOUNDATION_INPUT"),
    "UDT_NATIVE_ACTION_COLD_PACKET.md": ("C1 clarification", "HARD_FROZEN_OWNER_PACKET", "seal/carrier/bootstrap/Xmax statuses", "no action or boundary completion", "FOUNDATION_INPUT"),
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": ("CSN postulate", "OWNER_LOCKED_FOUNDATION", "pre-scale conformal equivalence", "does not select a representative or action", "FOUNDING_SELECTOR"),
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": ("bootstrap principle", "OWNER_STATED_WORKING", "on-shell consistency", "cannot become a missing local EOM", "ON_SHELL_ONLY"),
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md": ("Xmax clarification", "OWNER_CURRENT_CLARIFICATION", "working global posit", "no local insertion or value", "GLOBAL_STATUS"),
    "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md": ("carrier clarification", "OWNER_CURRENT_CLARIFICATION", "S2 reopened as posit", "no carrier/action assumption", "CARRIER_EXCLUSION"),
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": ("action selector audit", "POST_FIREWALL_EVIDENCE", "pre/post-scale action distinctions", "no C2 completion promotion", "ACTION_BRANCH_SCOPE"),
}

EXACT = {
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md": ("final action ruling", "HARD_FROZEN_POST_FIREWALL", "C2/EH/action distinctions", "immutable; no strengthening", "FROZEN_ACTION_STATUS"),
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": ("final status ledger", "HARD_FROZEN_POST_FIREWALL", "UNIQUE-CONDITIONAL and OPEN labels", "immutable", "FROZEN_ACTION_STATUS"),
    "native_action_final_adjudication_2026-07-18/COUNTERMODEL_COMPLETENESS_FINAL.tsv": ("completeness correction", "HARD_FROZEN_POST_FIREWALL", "countermodel limits", "no complete-universe claim", "FROZEN_SCOPE"),
    "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md": ("whole-metric Cartan audit", "CURRENT_EVIDENCE", "full coframe census", "Cartan identities are not EOM", "METRIC_COMPLETENESS_WARNING"),
    "metric_cartan_holonomy_audit_2026-07-19/STATUS_LEDGER.tsv": ("Cartan status ledger", "CURRENT_EVIDENCE", "derived/open distinctions", "no action promotion", "STATUS_SCOPE"),
    "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md": ("conditional Hopf audit", "CURRENT_EVIDENCE", "orbit/connection witness", "no carrier/action derivation", "CONDITIONAL_HOPF_ROUTE"),
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv": ("Hopf status ledger", "CURRENT_EVIDENCE", "compatibility/open distinctions", "no carrier promotion", "STATUS_SCOPE"),
    "null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json": ("Hopf exact algebra", "CURRENT_EVIDENCE", "conditional identities", "inherits premises", "CONDITIONAL_ALGEBRA"),
    "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md": ("toric closure audit", "CURRENT_EVIDENCE", "conditional S3 family", "premises not founded", "CONDITIONAL_GLOBAL_GEOMETRY"),
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv": ("toric status ledger", "CURRENT_EVIDENCE", "conditional/open distinctions", "no topology promotion", "STATUS_SCOPE"),
    "angular_toric_closure_selector_2026-07-19/DERIVATION_RESULT.json": ("toric exact algebra", "CURRENT_EVIDENCE", "cap/lattice calculations", "inherits premises", "CONDITIONAL_ALGEBRA"),
    "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md": ("phi-angular audit", "CURRENT_EVIDENCE", "selectors fail to force local equation", "no invented equation", "NEGATIVE_SELECTOR_EVIDENCE"),
    "bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv": ("phi-angular ledger", "CURRENT_EVIDENCE", "underdetermination labels", "no equation promotion", "STATUS_SCOPE"),
    "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md": ("boundary audit", "CURRENT_EVIDENCE", "boundary/bootstrap limits", "future completion remains open", "BOUNDARY_SELECTOR_NEGATIVE"),
    "boundary_bootstrap_representative_selector_audit_2026-07-19/STATUS_LEDGER.tsv": ("boundary ledger", "CURRENT_EVIDENCE", "selector statuses", "no boundary action promotion", "STATUS_SCOPE"),
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": ("topology audit", "CURRENT_EVIDENCE", "Hopf capability caveat", "topology does not set action", "TOPOLOGY_SCOPE"),
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv": ("topology ledger", "CURRENT_EVIDENCE", "topology/carrier labels", "no carrier promotion", "STATUS_SCOPE"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md": ("dimensional audit", "CURRENT_EVIDENCE", "coefficient ruler", "no scale promotion", "DIMENSIONAL_GATE"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv": ("dimensional ledger", "CURRENT_EVIDENCE", "scale statuses", "no scale promotion", "STATUS_SCOPE"),
    "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md": ("scale census", "CURRENT_EVIDENCE", "homothety rank", "no absolute equation", "SCALE_SCOPE"),
    "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv": ("scale ledger", "CURRENT_EVIDENCE", "open scale objects", "no Xmax value", "STATUS_SCOPE"),
    "angular_derivative_weight_selector_2026-07-20/AUDIT_REPORT.md": ("derivative-weight audit", "CURRENT_EVIDENCE", "order separation", "no L2/L4 import", "DERIVATIVE_SCOPE"),
    "angular_derivative_weight_selector_2026-07-20/STATUS_LEDGER.tsv": ("derivative ledger", "CURRENT_EVIDENCE", "route labels", "no material weighting", "STATUS_SCOPE"),
    "angular_derivative_weight_selector_2026-07-20/DERIVATION_RESULT.json": ("derivative exact algebra", "CURRENT_EVIDENCE", "CSN order algebra", "bounded premises", "CONDITIONAL_ALGEBRA"),
    "c2_angular_reduction_selector_2026-07-20/AUDIT_REPORT.md": ("immediate parent audit", "CURRENT_EVIDENCE", "compact round-shape theorem", "product and boundary caveats remain", "PARENT_RESULT"),
    "c2_angular_reduction_selector_2026-07-20/STATUS_LEDGER.tsv": ("parent status ledger", "CURRENT_EVIDENCE", "exact conditional labels", "no scale/matter promotion", "STATUS_SCOPE"),
    "c2_angular_reduction_selector_2026-07-20/EQUATION_LEDGER.tsv": ("parent equations", "CURRENT_EVIDENCE", "product Bach and shape identities", "constant-lapse limitation", "PARENT_ALGEBRA"),
    "c2_angular_reduction_selector_2026-07-20/DERIVATION_RESULT.json": ("parent exact output", "CURRENT_EVIDENCE", "curvature roots and coefficients", "inherits product premises", "PARENT_ALGEBRA"),
    "c2_angular_reduction_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md": ("authorized seam", "CURRENT_NAVIGATION", "defines variable-lapse question", "not outcome evidence", "QUESTION_ONLY"),
    "c2_angular_reduction_selector_2026-07-20/COMPLETENESS_SCOPE.tsv": ("parent scope", "CURRENT_EVIDENCE", "omitted lapse/shift/boundary layers", "omissions stay open", "SCOPE_GATE"),
}

ROWS = {**FOUNDATION, **EXACT}


def main() -> None:
    with (HERE / "SOURCE_CENSUS.tsv").open(encoding="utf-8", newline="") as handle:
        census = list(csv.DictReader(handle, delimiter="\t"))
    expected = {row["path"] for row in census if row["initial_disposition"] == "LOAD_BEARING_CANDIDATE"}
    if expected != set(ROWS):
        raise AssertionError(f"mismatch missing={sorted(expected-set(ROWS))} extra={sorted(set(ROWS)-expected)}")
    fields = ["id", "path", "role", "authority", "affirmative_use", "prohibition", "audit_ruling"]
    with (HERE / "SOURCE_ADJUDICATION.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for index, path in enumerate(sorted(ROWS), 1):
            role, authority, use, prohibition, ruling = ROWS[path]
            writer.writerow({"id": f"R{index:02d}", "path": path, "role": role, "authority": authority,
                             "affirmative_use": use, "prohibition": prohibition, "audit_ruling": ruling})
    print(f"PASS rows={len(ROWS)}")


if __name__ == "__main__":
    main()
