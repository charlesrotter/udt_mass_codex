#!/usr/bin/env python3
"""Verify the immutable G79 external-review return and adjudication layer."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    assert result["status"] == "VERIFIED_WITH_CAVEATS"
    assert result["scientific_corrections"] == 0
    assert len(result["binding_caveats"]) == 3
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == result["sealed_manifest_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == result["raw_review_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_STDOUT.txt") == result["stdout_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == result["transcript_sha256"]
    with (HERE / "REVIEW_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 36
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    for token in (
        "VERIFIED_WITH_CAVEATS",
        "sqrt(21)/4",
        "0.7559850215834019",
        "sealed package is not self-rerunnable unchanged",
        "not fully end-to-end independent",
        "reverse source-initial",
    ):
        assert token in raw + adjudication
    output = {
        "schema": "udt-cmb-g79-external-adjudication-verification-v1",
        "status": "PASS",
        "sealed_payload_rows": len(rows),
        "sealed_intake_files": len(rows) + 1,
        "scientific_corrections": 0,
        "binding_caveats": 3,
    }
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

