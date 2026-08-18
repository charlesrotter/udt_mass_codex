#!/usr/bin/env python3
"""Fail-closed final package verifier for G163."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main() -> None:
    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_RESULT.json")
    catches = load_json("CATCH_PROOF_RESULT.json")
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["xmax_absent_from_preregistered_x_free_residuals"] is True
    assert production["xmax_jacobian_zero_by_construction"] is True
    assert production["source_census_independent_xmax_owner_found"] is False
    assert independent["xmax_absence_is_structural_not_independent_identifiability_evidence"] is True
    assert catches["genuine_mutation_catch_count"] == 3
    assert catches["semantic_guard_count"] == 5

    with (HERE / "DEPENDENCY_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        ledger = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["id"] for row in ledger] == [f"G{i}" for i in range(135, 155)]
    assert all(row["final_class"] and row["native_scale_free_content"] for row in ledger)

    review = (HERE / "ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    gates = (HERE / "EVIDENCE_GATES.md").read_text(encoding="utf-8")
    for token in (
        "PASS_WITH_REPAIRS",
        "structural check by construction",
        "no independent dimensionful `Xmax` owner",
    ):
        assert token in review
    for token in (
        "ZERO_JACOBIAN_COLUMN_IS_A_STRUCTURAL_CHECK_BY_CONSTRUCTION",
        "FROZEN_26_SOURCE_CENSUS_FINDS_NO_INDEPENDENT_XMAX_OWNER",
    ):
        assert token in report
    for token in (
        "Noncircular supremum-ownership criterion",
        "not independent identifiability evidence",
        "dimensionally homogeneous monomial/power constructions",
    ):
        assert token in exact
    assert "Final grade: `VERIFIED_WITH_CAVEATS`" in report
    assert "Premise/startup and repository gates:** PASS" in gates
    print("PASS: G163 repaired package, 20-row regrade, and adversarial evidence boundary")


if __name__ == "__main__":
    main()
