#!/usr/bin/env python3
"""Administrative preregistration verifier; evaluates no scientific outcome."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv",
    ]
    for name in required:
        assert (HERE / name).is_file(), name

    prereg = (HERE / "PREREGISTRATION.md").read_text()
    assert "NOT YET EVALUATED" in prereg
    assert "G88 stationary AM lapse continuation is outside" in prereg
    assert "partial reciprocal response" in prereg
    assert "not as a physical frozen-sector trajectory" in prereg

    with (HERE / "PREMISE_LEDGER.tsv").open(newline="") as handle:
        premises = list(csv.DictReader(handle, delimiter="\t"))
    assert len(premises) == 15
    assert {row["status"] for row in premises} >= {
        "OBSERVED", "CONDITIONAL", "DERIVED", "CHOSE", "CHOSE_DIAGNOSTIC", "OPEN", "INACTIVE"
    }

    with (HERE / "FALSIFICATION_CONTRACT.tsv").open(newline="") as handle:
        gates = list(csv.DictReader(handle, delimiter="\t"))
    assert len(gates) == 11

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 6
    for row in sources:
        path = ROOT / row["path"]
        assert path.is_file(), path
        assert sha256(path) == row["sha256"], path

    forbidden = [
        HERE / "DERIVATION_RESULT.json",
        HERE / "AUDIT_REPORT.md",
        HERE / "INDEPENDENT_VERIFICATION.json",
    ]
    assert not any(path.exists() for path in forbidden)
    print("preregistration: PASS")
    print(f"premises: {len(premises)}")
    print(f"falsification_gates: {len(gates)}")
    print(f"frozen_sources: {len(sources)}")
    print("outcome_artifacts_absent: PASS")


if __name__ == "__main__":
    main()
