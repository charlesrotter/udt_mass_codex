#!/usr/bin/env python3
"""Fail-closed verification of the G80 external-review adjudication layer."""

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
    verification = json.loads(
        (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").read_text(encoding="utf-8")
    )
    assert result["status"] == "VERIFIED_AS_BOUNDED_GEOMETRIC_RECIPROCITY"
    assert result["scientific_corrections"] == 0
    assert len(result["binding_caveats"]) == 5
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == result["sealed_manifest_sha256"]
    assert digest(HERE / "REVERSE_PATH_EVIDENCE.npz") == result["reverse_path_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == result["raw_review_sha256"]
    with (HERE / "REVIEW_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 30
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    text = raw + adjudication
    for token in (
        "VERIFIED_AS_BOUNDED_GEOMETRIC_RECIPROCITY",
        "1.1456439237389628",
        "1.4204869936356233e-08",
        "generic self-adjoint Jacobi/Wronskian reciprocity",
        "D'_reverse = Z S_r D_forward^T S_s",
        "Past-directed reversal only",
        "No downstream promotion",
    ):
        assert token in text
    assert verification == {
        "binding_caveats": 5,
        "schema": "udt-cmb-g80-external-adjudication-verification-v1",
        "scientific_corrections": 0,
        "sealed_intake_files": 31,
        "sealed_payload_rows": 30,
        "status": "PASS",
    }
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
