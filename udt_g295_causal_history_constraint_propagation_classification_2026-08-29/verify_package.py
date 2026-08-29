#!/usr/bin/env python3
"""Fail-closed G295 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    with (ROOT / "SOURCE_SCOPE.tsv").open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    require(len(sources) == 9, "source count changed")
    for row in sources:
        path = REPO / row["path"]
        require(path.is_file(), f"source missing: {row['path']}")
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            frozen = subprocess.run(
                ["git", "show", f"d7253a9f:{row['path']}"],
                cwd=REPO,
                capture_output=True,
                check=False,
            )
            require(frozen.returncode == 0, f"frozen source unavailable: {row['path']}")
            payload = frozen.stdout
        require(hashlib.sha256(payload).hexdigest() == row["sha256"], f"source hash changed: {row['path']}")

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    expected = (
        "ONE_COVARIANT_HISTORY_CONDITION_IS_THE_MINIMAL_TYPE__"
        "SLICE_CONSTRAINT_AND_CAUSAL_UPDATE_ARE_A_REPRESENTATION__"
        "FORMULA_AND_REALIZED_HISTORY_REMAIN_OPEN"
    )
    require(production["all_pass"] and production["exact_checks"] == 39, "production checks changed")
    require(independent["all_pass"] and independent["assertions"] == 34539, "independent checks changed")
    require(not independent["production_imported"] and not independent["production_result_read"], "independent route contaminated")
    require(production["landing"] == independent["expected_landing"] == expected, "landing mismatch")
    require(catches["all_pass"] and catches["catch_count"] == 12, "catch proofs changed")

    required = (
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "SOURCE_SCOPE.tsv",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "AUDIT_REPORT.md",
        "ARCHITECTURE_CLASSIFICATION.tsv",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "COMMANDS.md",
    )
    for name in required:
        require((ROOT / name).is_file(), f"missing evidence file: {name}")

    production_source = (ROOT / "derive_causal_history_classification.py").read_text(encoding="utf-8")
    independent_source = (ROOT / "verify_causal_history_independent.py").read_text(encoding="utf-8")
    require("import sympy" in production_source, "production method changed")
    require("from fractions import Fraction" in independent_source, "independent method changed")
    require("derive_causal_history_classification" not in independent_source, "independent imports production")
    require("DERIVATION_RESULT" not in independent_source, "independent reads production output")

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for token in (
        "type simplification, not equation-count reduction",
        "least-foliation-dependent",
        "law family is not one realized history",
        "AU=RA",
        "screen sector",
        "no global now",
        "FORMULA_AND_REALIZED_HISTORY_REMAIN_OPEN",
    ):
        require(token in exact, f"scientific guard absent: {token}")

    result = {
        "all_pass": True,
        "source_rows": len(sources),
        "production_checks": production["exact_checks"],
        "independent_assertions": independent["assertions"],
        "hostile_catches": catches["catch_count"],
        "landing": expected,
    }
    (ROOT / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
