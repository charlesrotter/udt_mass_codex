#!/usr/bin/env python3
"""Dependency-free G285 preregistration and frozen-source verifier."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def main() -> None:
    required = (
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "SOURCE_SCOPE.tsv",
        "COMMANDS.md",
        "STATUS_LEDGER.tsv",
        "derive_complete_separation_retyping.py",
        "verify_independent.py",
        "run_catch_proofs.py",
    )
    checks: dict[str, bool] = {f"required_{name}": (PACKAGE / name).is_file() for name in required}
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count_13"] = len(sources) == 13
    for row in sources:
        path = ROOT / row["path"]
        payload = path.read_bytes() if path.is_file() else b""
        checks[f"source_{row['path']}"] = (
            path.is_file()
            and len(payload) == int(row["bytes"])
            and hashlib.sha256(payload).hexdigest() == row["sha256"]
        )
    premise_rows = list(csv.DictReader((PACKAGE / "PREMISE_LEDGER.tsv").open(newline="", encoding="utf-8"), delimiter="\t"))
    checks["premise_rows_10"] = len(premise_rows) == 10
    prereg = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    checks["four_landing_contract"] = all(
        token in prereg
        for token in (
            "SCALAR_STATE_IS_COMPLETE_SEPARATION",
            "COMPLETE_GERM_RETYPES_SCALAR_TWINS_AS_DISTINCT_SEPARATIONS",
            "COMPLETE_GERM_RETYPING_ITSELF_SELECTS_TIDAL_VALUES",
            "CANDIDATE_COMPLETE_GERM_IS_INCONSISTENT_OR_NONFAITHFUL",
        )
    )
    checks["candidate_not_canon"] = "not canon" in prereg
    checks["no_observational_or_dynamical_import"] = all(
        token in prereg for token in ("may not canonize", "derive physical values", "introduce dynamics")
    )
    result = {
        "audit": "G285_PREREGISTRATION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source_count": len(sources),
        "premise_rows": len(premise_rows),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
