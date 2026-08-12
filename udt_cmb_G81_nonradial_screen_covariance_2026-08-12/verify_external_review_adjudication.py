#!/usr/bin/env python3
"""Verify the G81 external-review and live provenance closure."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    assert result["status"] == "VERIFIED_WITH_CAVEATS"
    assert result["scientific_corrections"] == 0
    assert len(result["binding_caveats"]) == 2
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == result["sealed_manifest_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == result["raw_review_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == result["review_transcript_sha256"]
    with (HERE / "REVIEW_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 37
    assert sum(row["role"] == "G81_package" for row in rows) == 28
    assert sum(row["role"] != "G81_package" for row in rows) == 9
    for row in rows:
        assert digest(ROOT / row["path"]) == row["sha256"]
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    for token in (
        "VERIFIED_WITH_CAVEATS",
        "DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS",
        "D_reverse_AB = Z B transpose(D_forward) transpose(A)",
        "1.1801666864663825e-3",
        "Corrections:",
        "DOP853 integrator family",
        "not a UDT-specific selector",
    ):
        assert token in raw + adjudication
    output = {
        "schema": "udt-cmb-g81-external-adjudication-verification-v1",
        "status": "PASS",
        "scientific_corrections": 0,
        "binding_caveats": 2,
        "sealed_intake_files": 38,
        "sealed_payload_rows": 37,
        "live_payload_hashes_verified": 37,
        "source_bytes_verified_live": 9,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
