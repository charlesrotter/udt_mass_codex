#!/usr/bin/env python3
"""Fail-closed verifier for the complete non-ultrastatic branch audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIMARY = (
    "COMPLETE_NONULTRASTATIC_CONFIGURATIONS_EXIST__"
    "INTRINSIC_STATIONARY_DEPTH_EXISTS_IN_BOUNDED_STATIC_CONTROL__"
    "FULL_INTRINSIC_PAIR_REMAINS_CONDITIONAL"
)


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
    assert_unique("CONFIGURATION_STRATUM_UNIVERSE.tsv", "stratum_id", {f"C{i:02d}" for i in range(1, 13)})
    assert_unique("CONFIGURATION_STRATUM_OUTCOMES.tsv", "stratum_id", {f"C{i:02d}" for i in range(1, 13)})
    assert_unique("WITNESS_UNIVERSE.tsv", "witness_id", {f"W{i:02d}" for i in range(1, 7)})
    assert_unique("WITNESS_OUTCOMES.tsv", "witness_id", {f"W{i:02d}" for i in range(1, 7)})
    assert_unique("PROPERTY_GATE_UNIVERSE.tsv", "gate_id", {f"G{i:02d}" for i in range(1, 17)})
    assert_unique("PROPERTY_GATE_OUTCOMES.tsv", "gate_id", {f"G{i:02d}" for i in range(1, 17)})
    assert_unique("FALSIFICATION_CONTRACT.tsv", "catch_id", {f"F{i:02d}" for i in range(1, 19)})
    assert_unique("CATCH_PROOFS.tsv", "catch_id", {f"F{i:02d}" for i in range(1, 19)})
    assert all(row["status"] == "PASS" for row in rows("CATCH_PROOFS.tsv"))
    assert len(rows("SOURCE_MANIFEST.tsv")) == 19

    code, source_stdout, source_stderr = run("build_source_manifest.py")
    assert code == 0 and source_stderr == ""
    assert source_stdout.strip() == "PASS source_manifest 19/19"

    code, derived_stdout, derived_stderr = run("derive_nonultrastatic_branch.py")
    assert code == 0 and derived_stderr == ""
    derived = json.loads(derived_stdout)
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert derived == saved
    assert derived["primary_ruling"] == PRIMARY
    assert (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8") == derived_stdout
    assert (HERE / "DERIVATION_STDERR.txt").read_text(encoding="utf-8").strip() == derived_stderr

    code, independent_stdout, independent_stderr = run("verify_nonultrastatic_independent.py")
    assert code == 0 and independent_stderr == ""
    independent = json.loads(independent_stdout)
    saved_independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert independent == saved_independent
    assert independent["primary_ruling_reproduced"] == PRIMARY
    assert (HERE / "INDEPENDENT_STDOUT.txt").read_text(encoding="utf-8") == independent_stdout
    assert (HERE / "INDEPENDENT_STDERR.txt").read_text(encoding="utf-8").strip() == independent_stderr
    independent_code = (HERE / "verify_nonultrastatic_independent.py").read_text(encoding="utf-8")
    assert "derive_nonultrastatic_branch" not in independent_code

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    for token in (
        "COMPLETE_NONULTRASTATIC_CONFIGURATIONS_EXIST",
        "THE_FULL_INTRINSIC_CLOCK_RULER_PAIR_REMAINS_CONDITIONAL",
        "The two positive witnesses may not be joined by assertion",
        "No action or equations have selected",
        "No fresh external-model semantic review was authorized",
    ):
        assert token in report
    for token in (
        "General law-neutral stationary class", "Stationary clock depth",
        "The angular twist produces the ruler line",
        "A complete metric-native time-line control", "Exact remaining join",
    ):
        assert token in exact
    assert "S09\tall_gate_complete_intrinsic_pair_witness\tOPEN" in status
    assert "S11\tlambda\tOPEN" in status
    assert "S14\taction_variation_source_boundary_density_bootstrap_mass_Xmax_dynamics\tOPEN_OR_CONDITIONAL" in status

    result = {
        "status": "PASS",
        "sources": 19,
        "strata": 12,
        "witnesses": 6,
        "property_gates": 16,
        "catch_proofs": 18,
        "production_replay": "PASS",
        "independent_replay": "PASS",
        "primary_ruling": PRIMARY,
        "audit_report_sha256": hashlib.sha256((HERE / "AUDIT_REPORT.md").read_bytes()).hexdigest(),
        "status_ledger_sha256": hashlib.sha256((HERE / "STATUS_LEDGER.tsv").read_bytes()).hexdigest(),
    }
    saved_verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    assert saved_verification == result
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
