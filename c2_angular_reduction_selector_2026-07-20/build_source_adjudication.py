#!/usr/bin/env python3
"""Build the exact one-row-per-load-bearing-source adjudication."""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent

# path: role, authority, allowed use, prohibition, ruling
ROWS = {
    "CANON.md": ("canon/control ledger", "MIXED_DATE_CONTROL", "current owner locks only after LIVE/later-clarification cross-check", "pre-July science cannot affirm post-firewall physics", "SCOPE_HISTORY_ONLY"),
    "LIVE.md": ("controlling state", "CURRENT_CONTROL", "frontier and premise/authority boundary", "not load-bearing algebra", "CONTROLLING_SCOPE"),
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": ("C0 foundation", "HARD_FROZEN_OWNER_PACKET", "exact firewall and supplied foundation", "no unenumerated historical import", "FOUNDATION_INPUT"),
    "UDT_NATIVE_ACTION_COLD_PACKET.md": ("C1 clarification", "HARD_FROZEN_OWNER_PACKET", "seal/carrier/bootstrap/Xmax statuses", "no action, coefficient, or transverse completion supplied", "FOUNDATION_INPUT"),
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": ("CSN postulate", "OWNER_LOCKED_FOUNDATION", "pre-scale conformal equivalence", "does not select action, representative, derivative order, or boundary", "FOUNDING_SELECTOR"),
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": ("bootstrap principle", "OWNER_STATED_WORKING", "on-shell self-consistency requirement", "cannot become a local coupling or missing EOM", "ON_SHELL_ONLY"),
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md": ("Xmax clarification", "OWNER_CURRENT_CLARIFICATION", "working global posit and open origin/value", "no local insertion or numerical value", "GLOBAL_STATUS"),
    "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md": ("carrier clarification", "OWNER_CURRENT_CLARIFICATION", "S2 reopened as historical posit", "no carrier/action assumption", "CARRIER_EXCLUSION"),
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": ("action selector audit", "POST_FIREWALL_EVIDENCE", "pre/post-scale and open variation/boundary selectors", "no EH/C2 completion promotion", "ACTION_BRANCH_SCOPE"),
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md": ("final action ruling", "HARD_FROZEN_POST_FIREWALL", "exact C2/EH/action/source distinctions", "immutable; no strengthening", "FROZEN_ACTION_STATUS"),
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": ("final status ledger", "HARD_FROZEN_POST_FIREWALL", "UNIQUE-CONDITIONAL/CONDITIONAL/OPEN labels", "immutable; no strengthening", "FROZEN_ACTION_STATUS"),
    "native_action_final_adjudication_2026-07-18/COUNTERMODEL_COMPLETENESS_FINAL.tsv": ("completeness correction", "HARD_FROZEN_POST_FIREWALL", "limits of action countermodels", "no complete-universe claim", "FROZEN_SCOPE"),
    "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md": ("whole-metric Cartan audit", "CURRENT_EVIDENCE", "full 2+2 sector census and C2/EH bridge warning", "Cartan identities are not EOM; area-only shortcut refuted", "METRIC_COMPLETENESS_WARNING"),
    "metric_cartan_holonomy_audit_2026-07-19/STATUS_LEDGER.tsv": ("Cartan status ledger", "CURRENT_EVIDENCE", "exact derived/open distinctions", "no holonomy/matter promotion", "STATUS_SCOPE"),
    "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md": ("conditional Hopf metric audit", "CURRENT_EVIDENCE", "reciprocal orbit/connection witness and missing soldering", "no toric/round/carrier/action derivation", "CONDITIONAL_HOPF_ROUTE"),
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv": ("Hopf status ledger", "CURRENT_EVIDENCE", "compatibility/open distinctions", "no direct carrier identity", "STATUS_SCOPE"),
    "null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json": ("Hopf exact algebra", "CURRENT_EVIDENCE", "conditional quotient identities", "inherits report premises", "CONDITIONAL_ALGEBRA"),
    "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md": ("toric closure audit", "CURRENT_EVIDENCE", "conditional S3/circle-action theorem and nonround family", "premises not founded", "CONDITIONAL_GLOBAL_GEOMETRY"),
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv": ("toric status ledger", "CURRENT_EVIDENCE", "conditional/open distinctions", "no cap/topology promotion", "STATUS_SCOPE"),
    "angular_toric_closure_selector_2026-07-19/DERIVATION_RESULT.json": ("toric exact algebra", "CURRENT_EVIDENCE", "cap/lattice/shape calculations", "inherits report premises", "CONDITIONAL_ALGEBRA"),
    "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md": ("phi-angular selector audit", "CURRENT_EVIDENCE", "present selectors fail to force local equation", "no invented phi-angular EOM", "NEGATIVE_SELECTOR_EVIDENCE"),
    "bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv": ("phi-angular ledger", "CURRENT_EVIDENCE", "current underdetermination labels", "no equation promotion", "STATUS_SCOPE"),
    "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md": ("boundary/representative audit", "CURRENT_EVIDENCE", "endpoint-flat counterfamily and boundary/bootstrap limits", "does not rule out complete future boundary closure", "BOUNDARY_SELECTOR_NEGATIVE"),
    "boundary_bootstrap_representative_selector_audit_2026-07-19/STATUS_LEDGER.tsv": ("boundary status ledger", "CURRENT_EVIDENCE", "selector statuses", "no physical boundary action promotion", "STATUS_SCOPE"),
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": ("topology audit", "CURRENT_EVIDENCE", "Hopf capability and carrier/section caveat", "topology does not set action/scale", "TOPOLOGY_SCOPE"),
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv": ("topology ledger", "CURRENT_EVIDENCE", "exact topology/carrier labels", "no carrier promotion", "STATUS_SCOPE"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md": ("dimensional parent", "CURRENT_EVIDENCE", "coefficient ruler and missing native scale", "historical coefficients remain conditional", "DIMENSIONAL_GATE"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv": ("dimensional ledger", "CURRENT_EVIDENCE", "scale/mass statuses", "no scale promotion", "STATUS_SCOPE"),
    "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md": ("scale census", "CURRENT_EVIDENCE", "homothety/compactness rank", "no absolute scale equation", "SCALE_SCOPE"),
    "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv": ("scale ledger", "CURRENT_EVIDENCE", "open scale objects", "no Xmax value promotion", "STATUS_SCOPE"),
    "angular_derivative_weight_selector_2026-07-20/AUDIT_REPORT.md": ("immediate parent audit", "CURRENT_EVIDENCE", "pre-scale order separation and exact next seam", "no S2/L2+L4 input", "PARENT_RESULT"),
    "angular_derivative_weight_selector_2026-07-20/STATUS_LEDGER.tsv": ("parent status ledger", "CURRENT_EVIDENCE", "relative-weight and route labels", "no material weighting promotion", "STATUS_SCOPE"),
    "angular_derivative_weight_selector_2026-07-20/DERIVATION_RESULT.json": ("parent exact output", "CURRENT_EVIDENCE", "CSN/Hopf/squashing algebra", "inherits bounded branch premises", "PARENT_ALGEBRA"),
    "angular_derivative_weight_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md": ("authorized seam", "CURRENT_NAVIGATION", "defines this metric-only reduction question", "not evidence for outcome", "QUESTION_ONLY"),
    "angular_derivative_weight_selector_2026-07-20/COMPLETENESS_SCOPE.tsv": ("parent scope census", "CURRENT_EVIDENCE", "omitted fields/actions/boundaries", "omissions must remain open", "SCOPE_GATE"),
}


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
