#!/usr/bin/env python3
"""Fail-closed semantic, provenance, and implementation verifier."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
EXPECTED = [f"R{i:02d}" for i in range(16)]


def table(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    candidates = table("CANDIDATE_RESPONSE_REGISTRY.tsv")
    outcomes = table("RELATION_OUTCOMES.tsv")
    responses = table("RESPONSE_CLASSIFICATION.tsv")
    upper = table("UPPER_RIGHT_CONTROL_ATLAS.tsv")
    algebra = table("ALGEBRA_LEDGER.tsv")
    premises = table("PREMISE_LEDGER.tsv")
    outcome_premises = table("OUTCOME_PREMISE_AUDIT.tsv")
    sources = table("SOURCE_MANIFEST.tsv")
    catches = table("CATCH_PROOFS.tsv")
    derivation = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))

    assert [row["id"] for row in candidates] == EXPECTED
    assert [row["candidate_id"] for row in outcomes] == EXPECTED
    assert [row["candidate_id"] for row in responses] == [f"R{i:02d}" for i in range(2, 8)]
    assert len(algebra) == 13
    assert len(upper) == 2
    assert len(premises) == 17
    assert len(outcome_premises) == 18
    assert len(catches) == 15 and all(row["status"] == "PASS" for row in catches)

    assert derivation["outcome"] == "MINIMAL_CROSS_SECTOR_RESPONSE_EXISTS__LAW_SELECTION_OPEN"
    assert derivation["checks_passed"] == derivation["checks_total"] == 43
    assert derivation["law_selected"] is False
    assert derivation["density_scan_authorized"] is False
    assert derivation["explicit_witness_scope"] == "M_MINUS_IDENTITY_ONLY"
    assert independent["outcome"] == derivation["outcome"]
    assert independent["checks_passed"] == independent["checks_total"] == 29
    assert independent["semantic_catches_passed"] == independent["semantic_catches_total"] == 15
    assert independent["implementation"] == "python_stdlib_no_primary_import"
    assert independent["source_hashes_valid"] is True

    nonexact = [row for row in responses if row["classification"] != "EXACT"]
    assert len(nonexact) == 1
    assert nonexact[0]["candidate_id"] == "R07"
    assert nonexact[0]["d_response_coefficient"] == "1"
    status = {row["candidate_id"]: row["outcome"] for row in outcomes}
    assert status["R00"] == "DERIVED_UNIVERSAL_COMPACT_BOUNDARYLESS"
    assert status["R07"] == "UNIQUE_MINIMAL_ALTERNATING_CROSS_MOTIF_MOD_EXACT"
    assert status["R09"] == "CONSTRUCTIVE_NONZERO_HARMONIC_WITNESS"
    assert status["R12"] == "POINTWISE_RULER_HARMONIC_OWNERSHIP_BREAKS"
    assert status["R13"] == "SPLIT_RELATIVE_NOT_FULLY_FRAME_INDEPENDENT"
    assert status["R14"].endswith("NOT_SELECTED_LAW")
    assert status["R15"] == "CLOSED_NO_DENSITY_SCAN"
    assert upper[0]["eta1_closed"] == "YES" and upper[0]["primitive_harmonic_representative"] == "eta1"
    assert upper[1]["eta1_closed"] == "NO" and upper[1]["primitive_harmonic_representative"] == "ds"

    premise = {row["id"]: row for row in premises}
    assert premise["P08"]["status_at_base"] == "DERIVED_GIVEN_TYPED_SPLIT"
    assert premise["P10"]["status_at_base"] == "AUXILIARY_CONSTANT"
    assert premise["P14"]["status_at_base"] == "CHALLENGED_INACTIVE"
    assert premise["P15"]["pin_class"] == "EXCLUDED_OPEN"
    assert premise["P17"]["pin_class"] == "EXCLUDED_OPEN"
    assert outcome_premises[-1]["premise_id"] == "P18"
    assert outcome_premises[-1]["status"] == "RETAINED_DERIVED_SCOPED"

    assert len(sources) == len({row["path"] for row in sources}) == 15
    for row in sources:
        path = ROOT / row["path"]
        blob = subprocess.check_output(
            ["git", "hash-object", "--", row["path"]], cwd=ROOT, text=True
        ).strip()
        assert path.is_file()
        assert digest(path) == row["sha256"]
        assert blob == row["git_blob"]
        assert path.stat().st_size == int(row["bytes"])
    recorded_source_digest = (PACKAGE / "SOURCE_MANIFEST.sha256").read_text(
        encoding="utf-8"
    ).split()[0]
    assert digest(PACKAGE / "SOURCE_MANIFEST.tsv") == recorded_source_digest

    primary_tree = ast.parse((PACKAGE / "derive_broader_response.py").read_text(encoding="utf-8"))
    independent_tree = ast.parse(
        (PACKAGE / "verify_broader_response_independent.py").read_text(encoding="utf-8")
    )
    primary_imports = {
        alias.name
        for node in ast.walk(primary_tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    independent_imports = {
        alias.name
        for node in ast.walk(independent_tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    independent_from = {
        node.module or ""
        for node in ast.walk(independent_tree)
        if isinstance(node, ast.ImportFrom)
    }
    assert "sympy" in primary_imports
    assert "sympy" not in independent_imports
    assert not any("derive_broader_response" in name for name in independent_from)

    verification = {
        "status": "PASS",
        "candidate_outcomes": len(outcomes),
        "minimal_response_rows": len(responses),
        "upper_right_controls": len(upper),
        "algebra_rows": len(algebra),
        "primary_checks": derivation["checks_total"],
        "independent_checks": independent["checks_total"],
        "semantic_catches": len(catches),
        "source_identities": len(sources),
        "outcome": derivation["outcome"],
        "law_selected": False,
        "density_scan_authorized": False,
    }
    (PACKAGE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
