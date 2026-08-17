#!/usr/bin/env python3
"""Fail-closed verifier for the bounded G148 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: dict[str, bool] = {}
required = (
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "WITNESS_REGISTRATION.md",
    "derive_relation_first_pair_first_jet.py",
    "verify_relation_first_pair_first_jet_independent.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_RESULT.json",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "OUTCOME_PREMISE_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md",
    "FRESH_ADVERSARIAL_REVIEW.md",
    "REVIEW_REPAIR.md",
    "FRESH_ADVERSARIAL_FOLLOWUP.md",
)
for name in required:
    checks[f"required_{name}"] = (HERE / name).is_file()

with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
    sources = list(csv.DictReader(handle, delimiter="\t"))
checks["source_count_5"] = len(sources) == 5
for i, row in enumerate(sources):
    path = ROOT / row["path"]
    checks[f"source_{i}_exists"] = path.is_file()
    checks[f"source_{i}_hash"] = path.is_file() and sha256(path) == row["sha256"]
    checks[f"source_{i}_not_protected"] = not any(
        token in row["path"]
        for token in (
            "kernel_plane_global_curvature_holonomy_atlas",
            "native_onshell_timelive_reset_owner_audit",
            "pair_regime_flow_reciprocal_orchestra_amplification",
            "sne_xmax_G88",
        )
    )

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
checks["production_pass"] = production["status"] == "PASS" and production["checks_passed"] == 29 == production["checks_total"]
checks["independent_pass"] = independent["status"] == "PASS" and independent["checks_passed"] == 23 == independent["checks_total"]

for key in (
    "covariant_vector_decomposition",
    "screen_piece_in_pair_screen",
    "rest_projection",
    "rest_norm_split",
    "ambient_norm_split",
    "terminal_phi_derivative_identity",
    "catch_missing_screen_term",
    "catch_missing_rest_space_tilt",
    "catch_wrong_radial_weight",
    "all_block_hdot_additivity",
):
    checks[f"production_gate_{key}"] = production["checks"].get(key) is True

for name in ("B", "Q", "S", "Y", "Z"):
    checks[f"production_{name}_live"] = production["checks"].get(f"{name}_first_jet_live") is True
    checks[f"independent_{name}_live"] = independent["checks"].get(f"{name}_first_jet_live") is True
    checks[f"agreement_{name}_hdot"] = production["details"]["block_results"][name]["hdot"] == independent["block_results"][name]["hdot"]
    checks[f"agreement_{name}_phidot"] = production["details"]["block_results"][name]["phidot"] == independent["block_results"][name]["phidot"]
    checks[f"both_{name}_projector_live"] = (
        production["details"]["block_results"][name]["projector_dot_nonzero"] is True
        and independent["block_results"][name]["projector_dot_nonzero"] is True
    )

checks["agreement_base_h"] = production["details"]["base_h"] == independent["base_h"]
checks["agreement_base_det"] = production["details"]["base_det_h"] == independent["base_det_h"]
checks["agreement_combined_hdot"] = production["details"]["combined_hdot"] == independent["combined_hdot"]
checks["agreement_combined_phidot"] = production["details"]["combined_phidot"] == independent["combined_phidot"]

independent_source = (HERE / "verify_relation_first_pair_first_jet_independent.py").read_text(encoding="utf-8")
checks["independent_no_sympy"] = "sympy" not in independent_source
checks["independent_no_production_import"] = "import derive_relation_first_pair_first_jet" not in independent_source
checks["independent_fraction_route"] = "from fractions import Fraction" in independent_source

prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")

for token in (
    "observing calculation",
    "every `B,Q,S,Y,Z` block retained",
    "not call those coefficients alone a physical",
    "Maximum conclusion",
):
    checks[f"prereg_{token[:18]}"] = token in prereg

for token in (
    "WORKING_RELATION_FIRST_REPRESENTATION_ONLY",
    "EXACT_COVARIANT_FIRST_JET_IDENTITY_FOR_A_SUPPLIED_SMOOTH_REGULAR_CALIBRATED_PAIR",
    "LAMBDA_WITNESS_ESTABLISHES_COMPLETE_PAIR_ALGEBRAIC_FIRST_VARIATION_LIVENESS_ONLY",
    "PHYSICAL_CARRIER_HISTORY_DYNAMICS_AND_OBSERVATIONAL_REGIME_PATTERN_OPEN",
    "bypasses rather than",
    "exact coefficient limits only",
    "No history selection",
):
    checks[f"audit_{token[:22]}"] = token in audit

for token in (
    "\\nabla_u\\boldsymbol\\xi",
    "\\operatorname{sech}^2\\phi",
    "\\tanh\\phi",
    "radial coefficient is maximal rather than minimal",
    "does not derive a direction at coincidence",
):
    checks[f"exact_{token[:22]}"] = token in exact

checks["lay_keeps_history_open"] = "complete time-live metric history" in lay and "not which numerical history" in lay
checks["ledger_working_not_derived_carrier"] = "CHOSE_WORKING_INTERPRETATION" in ledger and "called uniquely derived" in ledger
checks["ledger_no_dynamics_promotion"] = "called an equation of motion" in ledger
checks["audit_no_resolved_carrier_claim"] = "ownership loop can be stopped" not in audit
checks["exact_no_native_physical_weight_claim"] = "Three native coefficient families" not in exact
checks["lambda_clock_flow_separated"] = "not identify `lambda` with query clock flow" in exact

review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
repair = (HERE / "REVIEW_REPAIR.md").read_text(encoding="utf-8")
followup = (HERE / "FRESH_ADVERSARIAL_FOLLOWUP.md").read_text(encoding="utf-8")
checks["review_reruns_recorded"] = all(token in review for token in ("29/29", "23/23", "90/90", "5/5"))
checks["review_required_repairs_recorded"] = all(
    token in review for token in ("Separate the arbitrary", "Keep `xi=rho n`", "exact coefficient limits")
)
checks["repair_all_three_classes"] = all(
    token in repair for token in ("`lambda` liveness", "bypasses rather than resolves", "coefficient limits only")
)
checks["followup_pass"] = "Verdict: `FOLLOWUP_PASS`" in followup
checks["followup_counts"] = all(token in followup for token in ("29/29", "23/23", "99/99"))
checks["followup_maximum_landing"] = all(
    token in followup
    for token in (
        "WORKING_RELATION_FIRST_REPRESENTATION_ONLY",
        "LAMBDA_WITNESS_ESTABLISHES_COMPLETE_PAIR_ALGEBRAIC_FIRST_VARIATION_LIVENESS_ONLY",
        "PHYSICAL_CARRIER_HISTORY_DYNAMICS_AND_OBSERVATIONAL_REGIME_PATTERN_OPEN",
    )
)

payload = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks_passed": sum(checks.values()),
    "checks_total": len(checks),
    "failed": [name for name, ok in checks.items() if not ok],
}
if "--write" in sys.argv:
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
print(f"{payload['status']}: {payload['checks_passed']}/{payload['checks_total']} G148 package checks")
if payload["failed"]:
    print("FAILED:", ", ".join(payload["failed"]))
    raise SystemExit(1)
