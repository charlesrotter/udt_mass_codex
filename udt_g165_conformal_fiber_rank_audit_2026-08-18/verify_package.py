#!/usr/bin/env python3
"""Fail-closed package verifier for G165."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    manifest = read_tsv(PKG / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 19
    for row in manifest:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]

    census = read_tsv(PKG / "CONDITION_CENSUS.tsv")
    assert len(census) == 59
    assert sum(row["survives_metric_restrictor_filter"] == "True" for row in census) == 0

    production = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PKG / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    catches = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["primary_landing"] == "NO_OWNED_NONIDENTITY_CONDITION"
    assert production["source_count"] == 19
    assert all(production["algebra"]["checks"].values())
    assert independent["status"] == "PASS" and independent["exact_rational_trials"] == 1200
    assert catches["status"] == "PASS" and catches["catch_count"] == 9
    assert (PKG / "AUDIT_REPORT.md").is_file()
    assert (PKG / "EVIDENCE_GATES.md").is_file()
    print("PASS: G165 package; 19 sources, 59 candidates, exact algebra, 1200 rational trials, 9 catches")


if __name__ == "__main__":
    main()
