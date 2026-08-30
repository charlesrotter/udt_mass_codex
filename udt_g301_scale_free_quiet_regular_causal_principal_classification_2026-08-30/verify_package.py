#!/usr/bin/env python3
"""Aggregate no-import verifier for the G301 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "TWO_INEQUIVALENT_FULL_METRIC_QUIET_PRINCIPAL_CLASSES_SURVIVE"
    "__GENERIC_RICCI_FLAT_AND_TRACEFREE_RICCI_WITH_ONE_CONSTANT_SCALAR_DATUM"
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(name):
    with (HERE / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def main():
    checks = 0
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 12
    checks += 1
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file()
        assert sha256(path) == row["sha256"]
        checks += 2

    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    invariant_basis = load_json("INVARIANT_BASIS_VERIFICATION.json")
    catches = load_json("CATCH_PROOF_RESULT.json")
    assert production["landing"] == LANDING
    assert independent["landing"] == LANDING
    assert independent["verdict"] == "INDEPENDENT_COEFFICIENT_STRATA_AGREEMENT_CONDITIONAL_ON_TWO_TERM_BASIS"
    assert not independent["full_invariant_basis_certified"]
    assert invariant_basis["verdict"] == "INDEPENDENT_FULL_SPACE_BASIS_CERTIFIED"
    assert invariant_basis["algebraic_curvature_dimension"] == 20
    assert invariant_basis["intertwiner_unknowns"] == 200
    assert invariant_basis["equivariance_rows"] == 1200
    assert invariant_basis["rational_rank"] == 198
    assert invariant_basis["rational_nullity"] == 2
    assert invariant_basis["exact_null_vectors"] == ["RICCI", "SCALAR_TIMES_METRIC"]
    assert invariant_basis["exact_null_vectors_independent"]
    assert not invariant_basis["production_imported"]
    assert production["assertions"] == 27829
    assert independent["assertions"] == 49609
    assert production["generic_rank"] == 10
    assert production["tracefree_rank"] == 9
    assert production["scalar_only_rank"] == 1
    assert production["zero_rank"] == 0
    assert catches["verdict"] == "PASS" and catches["caught"] == catches["total"] == 12
    assert not production["metric_change"] and not production["kernel_change"]
    assert not production["field_equation_adopted"]
    assert not independent["production_imported"]
    checks += 25

    # Source-driven ownership gate: these exact frozen sources state that the class assumptions and
    # formula remain unowned. This is a provenance check; the external review remains epistemic.
    g259 = (ROOT / "udt_g259_metric_only_parent_operator_fork_classification_2026-08-25/EXACT_DERIVATION.md").read_text(encoding="utf-8")
    g296 = (ROOT / "udt_g296_complete_metric_native_residual_order_map_2026-08-29/EXACT_DERIVATION.md").read_text(encoding="utf-8")
    g259_flat = " ".join(g259.split())
    g296_flat = " ".join(g296.split())
    assert "additional operator-class premises" in g259_flat
    assert "None of them proves all four restrictions" in g259_flat
    assert "Neither working clarification derives locality, second order, symmetric rank two, or identity divergence freedom" in g296_flat
    assert "Current premises select no residual form" in (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_text(encoding="utf-8") or "CURRENT_PREMISES_DO_NOT_PRIVILEGE_ONE_RESIDUAL_FORM" in (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_text(encoding="utf-8")
    checks += 4

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    repair_review = (HERE / "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    exact_flat = " ".join(exact.split())
    lay_flat = " ".join(lay.split())
    audit_flat = " ".join(audit.split())
    # Narrative checks below are packaging regressions only, never scientific certification.
    required_exact = (
        "F=DF_0",
        "a+4b",
        "trace-free Ricci",
        "R=\\text{constant}",
        "principal-class statement only",
        "identity divergence freedom is exactly one of G259's explicit unowned",
        "No metric component, reciprocal-kernel operator",
        "1,200-by-200 system has modular rank 198",
    )
    for token in required_exact:
        assert token in exact_flat
        checks += 1
    for token in (
        "two serious possibilities",
        "did **not** yet tell us which fork UDT owns",
        "Nothing in G301 changed the UDT metric or reciprocal kernel",
    ):
        assert token in lay_flat
        checks += 1
    assert "returned `ACCEPT_REPAIRS`" in audit_flat
    assert "`ACCEPT_REPAIRS`" in repair_review
    assert "Exact remaining defect: none within the preregistered repair scope" in repair_review
    assert ledger.count("FREE_AND_EXPLORED_CANDIDATE_PREMISE") >= 6
    checks += 4

    result = {
        "verdict": "PASS",
        "checks": checks,
        "source_rows": len(rows),
        "landing": LANDING,
        "external_review_pending": False,
        "scientific_certifiers": [
            "EXPLICIT_INVARIANT_THEORY_PROOF",
            "INDEPENDENT_20_TO_10_LORENTZ_INTERTWINER_CENSUS",
            "INDEPENDENT_COEFFICIENT_STRATA_REPLAY",
            "FRESH_EXTERNAL_GPT54_PREMISE_AUDIT",
        ],
        "narrative_token_checks_are_scientific_evidence": False,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
