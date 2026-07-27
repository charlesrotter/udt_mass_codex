#!/usr/bin/env python3
"""Fail-closed package verifier for the founding-semantics audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(script: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return result.returncode, result.stdout, result.stderr


def assert_unique(name: str, key: str, expected: set[str]) -> None:
    values = [row[key] for row in rows(name)]
    assert len(values) == len(set(values))
    assert set(values) == expected


def main() -> int:
    assert_unique("SOURCE_CLAIM_UNIVERSE.tsv", "claim_id", {f"C{i:02d}" for i in range(1, 37)})
    assert_unique("SOURCE_CLAIM_OUTCOMES.tsv", "claim_id", {f"C{i:02d}" for i in range(1, 37)})
    assert_unique("SEMANTIC_ROUTE_UNIVERSE.tsv", "route_id", {f"R{i:02d}" for i in range(1, 9)})
    assert_unique("SEMANTIC_ROUTE_OUTCOMES.tsv", "route_id", {f"R{i:02d}" for i in range(1, 9)})
    assert_unique("REQUIREMENT_UNIVERSE.tsv", "requirement_id", {f"Q{i:02d}" for i in range(1, 19)})
    assert_unique("REQUIREMENT_OUTCOMES.tsv", "requirement_id", {f"Q{i:02d}" for i in range(1, 19)})
    assert_unique("FALSIFICATION_CONTRACT.tsv", "catch_id", {f"F{i:02d}" for i in range(1, 17)})
    assert_unique("CATCH_PROOFS.tsv", "catch_id", {f"F{i:02d}" for i in range(1, 17)})
    assert all(row["status"] == "PASS" for row in rows("CATCH_PROOFS.tsv"))
    assert len(rows("SOURCE_MANIFEST.tsv")) == 21
    assert len(rows("SOURCE_LINEAGE.tsv")) == 9

    code, source_stdout, source_stderr = run("build_source_manifest.py")
    assert code == 0 and source_stderr == "" and source_stdout.strip() == "PASS source_manifest 21/21"

    code, derived_stdout, derived_stderr = run("derive_founding_semantics.py")
    assert code == 0 and derived_stderr == ""
    derived = json.loads(derived_stdout)
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert derived == saved
    assert (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8") == derived_stdout
    assert (HERE / "DERIVATION_STDERR.txt").read_text(encoding="utf-8").strip() == derived_stderr

    code, independent_stdout, independent_stderr = run("verify_semantics_independent.py")
    assert code == 0 and independent_stderr == ""
    independent = json.loads(independent_stdout)
    saved_independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert independent == saved_independent
    assert (HERE / "INDEPENDENT_STDOUT.txt").read_text(encoding="utf-8") == independent_stdout
    assert (HERE / "INDEPENDENT_STDERR.txt").read_text(encoding="utf-8").strip() == independent_stderr
    independent_code = (HERE / "verify_semantics_independent.py").read_text(encoding="utf-8")
    assert "derive_founding_semantics" not in independent_code

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_ADJUDICATION.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    for token in (
        "SEMANTICS_OPEN", "zero source claims forcing physical endpoint-only semantics",
        "zero forcing physical path-labelled", "No `lambda` is selected",
        "No fresh external-model semantic review was authorized",
    ):
        assert token in report
    for token in (
        "abstract depth space", "not a path-ontology theorem",
        "Observer-frame reciprocity does not close the fork",
    ):
        assert token in exact
    assert "S12\tprimary_founding_semantics\tSEMANTICS_OPEN" in status
    assert "S13\tlambda\tOPEN" in status

    result = {
        "status": "PASS",
        "sources": 21,
        "claims": 36,
        "routes": 8,
        "requirements": 18,
        "catch_proofs": 16,
        "production_replay": "PASS",
        "independent_replay": "PASS",
        "primary_ruling": "SEMANTICS_OPEN",
        "audit_report_sha256": hashlib.sha256((HERE / "AUDIT_REPORT.md").read_bytes()).hexdigest(),
        "status_ledger_sha256": hashlib.sha256((HERE / "STATUS_LEDGER.tsv").read_bytes()).hexdigest(),
    }
    saved_verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    assert saved_verification == result
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
