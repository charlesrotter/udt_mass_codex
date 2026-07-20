#!/usr/bin/env python3
"""Build the one-row-per-load-bearing-source authority adjudication."""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent

# path: role, authority, allowed affirmative use, prohibition, ruling for this audit
ROWS = {
    "CANON.md": ("owner canon ledger", "MIXED_DATE_CONTROL", "current owner locks only, cross-checked against LIVE and later clarifications", "pre-July scientific prose cannot supply affirmative post-firewall UDT physics", "SCOPE_AND_HISTORY_ONLY"),
    "LIVE.md": ("current controlling state", "CURRENT_CONTROL", "frontier, premise stamps, authority boundary", "cannot substitute for load-bearing algebra", "CONTROLLING_SCOPE"),
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": ("CSN postulate", "OWNER_LOCKED_FOUNDATION", "pre-scale local conformal equivalence and explicit non-consequences", "does not select action, representative, derivative order, boundary, or carrier", "FOUNDING_SELECTOR_ONLY"),
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": ("bootstrap principle", "OWNER_STATED_WORKING", "on-shell global self-consistency and narrow density-window requirement", "cannot be inserted as a local coupling or treated as a supplied off-shell equation", "ON_SHELL_REQUIREMENT_ONLY"),
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": ("selector audit", "CURRENT_POST_FIREWALL_EVIDENCE", "pre-/post-scale branch distinction and exact open selector list", "does not promote EH or C2 to complete native action", "BRANCH_SCOPE"),
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": ("exact C0 foundation", "HARD_FROZEN_OWNER_PACKET", "enumerated foundation and firewall", "no unenumerated historical physics may enter", "FOUNDATION_INPUT"),
    "UDT_NATIVE_ACTION_COLD_PACKET.md": ("exact C1 clarification", "HARD_FROZEN_OWNER_PACKET", "premise/status ledger including seal, carrier, bootstrap, Xmax", "does not supply action, coefficient, source, or boundary completion", "FOUNDATION_INPUT"),
    "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md": ("carrier clarification", "OWNER_CURRENT_CLARIFICATION", "S2 is reopened historical working posit", "round S2 cannot be assumed as native output", "CARRIER_EXCLUSION_GATE"),
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md": ("Xmax clarification", "OWNER_CURRENT_CLARIFICATION", "universal unattainable Xmax working posit and conditional global-output lead", "value, normalization, primitive status, and local insertion remain open", "GLOBAL_LENGTH_STATUS"),
    "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md": ("toric closure audit", "CURRENT_POST_FIREWALL_EVIDENCE", "conditional toric/cap inventory and nonuniqueness", "cannot promote toric slots, caps, roundness, or action", "CONDITIONAL_ANGULAR_GEOMETRY"),
    "angular_toric_closure_selector_2026-07-19/DERIVATION_RESULT.json": ("toric exact output", "CURRENT_POST_FIREWALL_EVIDENCE", "machine-readable conditional toric algebra", "premise status remains that of report", "CONDITIONAL_ALGEBRA"),
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv": ("toric status ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "exact derived/conditional/open distinctions", "cannot turn compatibility into uniqueness", "STATUS_SCOPE"),
    "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md": ("phi-angular selector audit", "CURRENT_POST_FIREWALL_EVIDENCE", "bounded failure of present selectors to force branch/direction", "does not authorize an added phi-angular equation", "NEGATIVE_SELECTOR_EVIDENCE"),
    "bootstrap_csn_phi_angular_selector_2026-07-19/CANDIDATE_OPERATOR.tsv": ("candidate operator ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "candidate inventory and premise failures", "candidate rows are not UDT equations", "CANDIDATE_ONLY"),
    "bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv": ("phi-angular status ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "current underdetermination labels", "no native operator promotion", "STATUS_SCOPE"),
    "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md": ("representative selector audit", "CURRENT_POST_FIREWALL_EVIDENCE", "endpoint-flat CSN counterfamily and bootstrap/Xmax limits", "does not rule out a future complete scale-bearing closure", "CURRENT_SELECTOR_NEGATIVE"),
    "boundary_bootstrap_representative_selector_audit_2026-07-19/STATUS_LEDGER.tsv": ("representative status ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "scoped selector statuses", "no absolute representative or scale promotion", "STATUS_SCOPE"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md": ("immediate parent audit", "CURRENT_POST_FIREWALL_EVIDENCE", "conditional coefficient ruler and next exact seam", "cannot assume L2+L4 or its coefficients", "PARENT_RESULT"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/DIMENSIONAL_OBJECT_LEDGER.tsv": ("dimensional inventory", "CURRENT_POST_FIREWALL_EVIDENCE", "dimension/provenance of existing matter objects", "conditional objects cannot become native inputs", "DIMENSIONAL_GATE"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/NEXT_SCIENTIFIC_DECISION.md": ("authorized seam", "CURRENT_POST_FIREWALL_NAVIGATION", "defines this bounded selector question", "not evidence for its answer", "QUESTION_ONLY"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv": ("parent status ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "coefficient and mass status distinctions", "no coefficient-origin promotion", "STATUS_SCOPE"),
    "matter_carrier_provenance_audit_results.md": ("carrier provenance audit", "PRE_FIREWALL_OR_MIXED_CONTEXT", "may expose historical carrier assumptions and failures", "cannot affirmatively derive current UDT carrier/action", "COUNTEREXAMPLE_OR_PROVENANCE_ONLY"),
    "native_action_final_adjudication_2026-07-18/COUNTERMODEL_COMPLETENESS_FINAL.tsv": ("countermodel completeness correction", "HARD_FROZEN_POST_FIREWALL", "limits of prior countermodels and open completeness", "must remain byte-identical; no action promotion", "FROZEN_SCOPE_EVIDENCE"),
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md": ("native-action final adjudication", "HARD_FROZEN_POST_FIREWALL", "C2/EH/action/source/boundary distinctions", "cannot be edited or strengthened", "FROZEN_ACTION_STATUS"),
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": ("native-action status ledger", "HARD_FROZEN_POST_FIREWALL", "exact UNIQUE-CONDITIONAL/CONDITIONAL/OPEN labels", "cannot be edited or strengthened", "FROZEN_ACTION_STATUS"),
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": ("native topology audit", "CURRENT_POST_FIREWALL_EVIDENCE", "implementation is Hopf-capable; carrier/section/action remain conditional", "topology cannot supply dimensional coefficient or carrier emergence", "TOPOLOGY_SCOPE"),
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv": ("topology status ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "topological versus carrier statuses", "no carrier/action promotion", "STATUS_SCOPE"),
    "noNull_energy.py": ("conditional continuum implementation", "ACTIVE_CODE_PROVENANCE", "locates historical L2/L4 coefficients for comparison after derivation", "its S2 target and functional are excluded as premises", "CONDITIONAL_COMPARISON_ONLY"),
    "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md": ("null/Hopf metric audit", "CURRENT_POST_FIREWALL_EVIDENCE", "conditional reciprocal Hopf witness, connection, and missing soldering", "does not derive toric completion, roundness, carrier, section, or action", "CONDITIONAL_HOPF_ROUTE"),
    "null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json": ("null/Hopf exact output", "CURRENT_POST_FIREWALL_EVIDENCE", "machine-readable conditional quotient algebra", "premise status remains that of report", "CONDITIONAL_ALGEBRA"),
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv": ("null/Hopf status ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "compatibility/open distinctions", "no direct celestial-carrier identity", "STATUS_SCOPE"),
    "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md": ("scale closure census", "CURRENT_POST_FIREWALL_EVIDENCE", "compactness rank and Xmax-reciprocity scale neutrality", "does not supply absolute Xmax or local coefficient", "GLOBAL_RATIO_SCOPE"),
    "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv": ("scale status ledger", "CURRENT_POST_FIREWALL_EVIDENCE", "no noncircular scale breaker and exact open objects", "no scale-selection promotion", "STATUS_SCOPE"),
}


def main() -> None:
    with (HERE / "SOURCE_CENSUS.tsv").open(encoding="utf-8", newline="") as handle:
        census = list(csv.DictReader(handle, delimiter="\t"))
    expected = {row["path"] for row in census if row["initial_disposition"] == "LOAD_BEARING_CANDIDATE"}
    if expected != set(ROWS):
        raise AssertionError(
            f"source adjudication mismatch missing={sorted(expected-set(ROWS))} extra={sorted(set(ROWS)-expected)}"
        )
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
