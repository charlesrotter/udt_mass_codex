#!/usr/bin/env python3
"""Read-only package and source verification for G257."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "derive_gr_quiet_embedding.py",
        "verify_independent.py",
        "run_catch_proofs.py",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    assert not missing, missing

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    assert production["landing"].startswith("EXACT_GR_VACUUM_BRANCH_EMBEDS")
    assert all(production["checks"].values())
    assert independent["status"] == "PASS" and independent["assertions"] == 4777
    assert catches["status"] == "PASS" and catches["caught_count"] == 7

    external = (ROOT / "EXTERNAL_REVIEW_GPT54.md").read_text()
    assert "Disposition: `ACCEPT`" in external
    assert "Scientific defects: none found" in external
    assert "ce4040741ff40233a340be8b702010ea0ba6bb43e063605cf36d36fe3e156144" in external

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    assert len(rows) == 9
    for row in rows:
        path = REPO / row["path"]
        assert path.is_file(), path
        assert digest(path) == row["sha256"], row["path"]

    print("PASS: G257 package, external ACCEPT, 9 source hashes, landing, 4777 independent assertions, and 7 catches")


if __name__ == "__main__":
    main()
