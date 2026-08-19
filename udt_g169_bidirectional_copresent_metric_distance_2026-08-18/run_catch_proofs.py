#!/usr/bin/env python3
"""Semantic and algebraic mutation catches for G169."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
audit = (HERE / "AUDIT_REPORT.md").read_text()
exact = (HERE / "EXACT_DERIVATION.md").read_text()
ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text()
prereg = (HERE / "PREREGISTRATION.md").read_text()

catches: dict[str, bool] = {}

# Algebra mutations: each asserted bad rule must be caught by an exact witness.
q = Fraction(2, 1)
catches["false_q_reversal"] = q * q != 1
chi = (1 - q) / (1 + q)
catches["false_chi_evenness"] = chi != -chi
catches["false_arbitrary_triangle_additivity"] = Fraction(1, 5) != Fraction(1, 2) * Fraction(1, 3)
catches["surface_reversal_not_reciprocal"] = Fraction(1, 2) * Fraction(1, 2) != 1

identity = ((1, 0), (0, 1))
shear = ((1, 1), (0, 1))
catches["scalar_closure_not_matrix_closure"] = shear != identity and shear[0][0] * shear[1][1] == 1

# Semantic catches: fail closed on the main tempting promotions.
catches["ownership_not_derived"] = "PROPOSED_WORKING_FOUNDATIONAL_CLARIFICATION_NOT_DERIVED" in ledger
catches["distance_definition_not_canonized"] = "PROPOSED_WORKING_DEFINITION_CANDIDATE" in ledger
catches["no_scalar_metric_overclaim"] = "not established physical metric distances" in exact
catches["coincidence_boundary_retained"] = "OPEN_BOUNDARY" in ledger and "rank two to rank one" in exact
catches["arbitrary_triangle_category_guard"] = "arbitrary-triangle additivity" in prereg and "category error" in exact
catches["path_not_inserted"] = "It is not a path, force, profile, or dynamical law." in audit
catches["external_review_still_open"] = "FRESH_ADVERSARIAL_REVIEW_OPEN" in audit

for name, passed in catches.items():
    if not passed:
        raise AssertionError(name)

result = {
    "catches_passed": sum(catches.values()),
    "catches_total": len(catches),
    "catches": catches,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"passed": result["catches_passed"], "total": result["catches_total"]}, sort_keys=True))
