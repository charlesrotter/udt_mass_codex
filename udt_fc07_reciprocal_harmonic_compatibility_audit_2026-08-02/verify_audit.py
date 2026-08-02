#!/usr/bin/env python3
"""Fail-closed semantic, provenance, and implementation verifier."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
EXPECTED_CANDIDATES = [f"R{i:02d}" for i in range(16)]


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    candidates = rows("RELATION_CANDIDATES.tsv")
    outcomes = rows("RELATION_OUTCOMES.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    algebra = rows("ALGEBRA_LEDGER.tsv")
    sources = rows("SOURCE_MANIFEST.tsv")
    anchors = rows("SOURCE_ANCHOR_LEDGER.tsv")
    catches = rows("CATCH_PROOFS.tsv")
    derivation = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))

    assert [row["id"] for row in candidates] == EXPECTED_CANDIDATES
    assert [row["candidate_id"] for row in outcomes] == EXPECTED_CANDIDATES
    assert len(algebra) == 18
    assert len(premises) == 17
    assert len(catches) == 20 and all(row["result"] == "PASS" for row in catches)
    assert derivation["outcome"] == "NO_ADDITIONAL_GEOMETRY_CUTTING_RELATION_DERIVED"
    assert derivation["checks_passed"] == derivation["checks_total"] == 43
    assert derivation["density_scan_authorized"] is False
    assert independent["outcome"] == derivation["outcome"]
    assert independent["checks_passed"] == independent["checks_total"] == 39
    assert independent["semantic_catches_passed"] == independent["semantic_catches_total"] == 20
    assert independent["implementation"] == "python_stdlib_fraction_no_primary_import"
    assert independent["source_hashes_valid"] is True

    # The 17 preregistered source identities must remain exact.
    assert len(sources) == len({row["path"] for row in sources}) == 17
    for row in sources:
        path = ROOT / row["path"]
        blob = subprocess.check_output(
            ["git", "hash-object", "--", row["path"]], cwd=ROOT, text=True
        ).strip()
        assert path.is_file()
        assert digest(path) == row["sha256"]
        assert blob == row["git_blob"]
        assert path.stat().st_size == int(row["bytes"])
    recorded_manifest_digest = (PACKAGE / "SOURCE_MANIFEST.sha256").read_text(
        encoding="utf-8"
    ).split()[0]
    assert digest(PACKAGE / "SOURCE_MANIFEST.tsv") == recorded_manifest_digest

    # Every load-bearing textual anchor must remain in the frozen source.
    source_paths = {row["path"] for row in sources}
    assert len(anchors) == 14
    for row in anchors:
        assert row["path"] in source_paths
        text = (ROOT / row["path"]).read_text(encoding="utf-8")
        assert row["exact_anchor"] in text, (row["id"], row["path"])

    # Independent verifier must not import SymPy or the production derivation.
    primary_tree = ast.parse((PACKAGE / "derive_compatibility.py").read_text(encoding="utf-8"))
    independent_tree = ast.parse(
        (PACKAGE / "verify_compatibility_independent.py").read_text(encoding="utf-8")
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
    assert not any("derive_compatibility" in name for name in independent_from)

    status = {row["candidate_id"]: row["outcome"] for row in outcomes}
    assert status["R02"].startswith("NOT_DERIVED")
    assert status["R03"] == "CONDITIONAL_IFF_D_CONSTANT"
    assert status["R06"].endswith("LEVEL_NOT_SELECTED")
    assert status["R07"] == "NONZERO_CONSTANT_SOLDER_REFUTED_ON_CLOSED_BASE"
    assert status["R09"] == "NATURALITY_GATE_ONLY"
    assert status["R12"] == "OPEN_COMPLETE_SEAL_LIFT__EVEN_REFLECTION_CONTROL_DOES_NOT_FIX_LEVEL"
    assert "J07_J11_OPEN" in status["R13"]
    assert status["R15"].startswith("SURVIVES")

    premise = {row["id"]: row for row in premises}
    assert premise["P06"]["status_at_base"] == "WORKING_CONDITIONAL_NOT_DERIVED"
    assert premise["P09"]["status_at_base"] == "SUPPLIED_CONDITION"
    assert premise["P15"]["status_at_base"] == "CHALLENGED_INACTIVE"
    assert premise["P16"]["pin_class"] == "EXCLUDED_OPEN"

    verification = {
        "status": "PASS",
        "candidate_relations": len(candidates),
        "algebra_rows": len(algebra),
        "primary_checks": derivation["checks_total"],
        "independent_checks": independent["checks_total"],
        "semantic_catches": len(catches),
        "source_identities": len(sources),
        "source_anchors": len(anchors),
        "outcome": derivation["outcome"],
        "density_scan_authorized": False,
    }
    (PACKAGE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
