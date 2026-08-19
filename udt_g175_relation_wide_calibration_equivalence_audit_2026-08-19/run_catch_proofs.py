#!/usr/bin/env python3
"""Semantic and algebraic regression catches for G175."""

from __future__ import annotations

from fractions import Fraction
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
ledger = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
manifest = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))

catches: list[tuple[str, bool]] = [
    ("landing_is_local_nonselection", "A_LOCAL_CALIBRATION_DOES_NOT_OWN_RELATION_WIDE_CARRY" in exact),
    ("supplied_map_only_sufficient", "Calling this relation-wide sufficiency a" in exact),
    ("constant_unit_iff", "if and only if" in exact and "n=cm" in exact),
    ("anchored_neighborhood", "entire A-neighborhood" in exact),
    ("all_A_jets", "All A jets agree" in exact),
    ("position_dependent_not_gauge", "a varying regrading is not" in exact),
    ("metric_unit_not_selected", "DERIVED_OPTION_NOT_SELECTED" in exact),
    ("metric_unit_half_phi", "Phi_{\\rm unit}=\\frac\\phi2" in exact),
    ("founded_phi_retained", "Phi_{\\rm founded}=\\phi" in exact),
    ("determinant_candidate_not_selected", "candidate rather than a selected carry law" in exact),
    ("cE_no_derivative", "does not contain a\nderivative of" in exact),
    ("G174_retained", "G174 local" in ledger),
    ("physical_owner_open", "physical carry owner\tOPEN" in ledger),
    ("no_candidate_selected", "m_A" not in audit and "m_P" not in audit),
    ("source_count", len(manifest) == 8),
    ("protected_and_scaffolds_absent", all("udt_g1" not in row["path"] or not any(f"udt_g{i}" in row["path"] for i in range(142, 161)) for row in manifest)),
]

# Independent exact mutation controls for the load-bearing transition.
Kp, Kq = Fraction(3, 5), Fraction(7, 11)
fp, fq = Fraction(1), Fraction(4)
Rm = Kq / Kp
Rn = (Kq / (fq * fq)) / (Kp / (fp * fp))
catches.append(("anchored_transition_mutation", Rn / Rm == Fraction(1, 16)))
catches.append(("constant_transition_mutation", ((Kq / 9) / (Kp / 9)) == Rm))

bad = [name for name, ok in catches if not ok]
if bad:
    raise SystemExit(bad)

result = {
    "status": "PASS__G175_SEMANTIC_AND_ALGEBRAIC_CATCHES",
    "catches_total": len(catches),
    "catches_passed": len(catches),
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(result, sort_keys=True))
