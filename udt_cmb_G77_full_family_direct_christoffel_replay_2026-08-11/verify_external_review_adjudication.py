#!/usr/bin/env python3
"""Reproduce the load-bearing G77 external-review adjudication gates."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST_SHA256 = "073351d373c27801553aeb347808216c5654c3b3a17665ded2eb79311718346a"
RAW_SHA256 = "36e4431d89581c514efca4fed1d56df1bf01416a07cee7d7691cb9132bf37441"
TRANSCRIPT_SHA256 = "69a1e0218fe6bd462e8da4fb330f2133f26a41c49df07061173f5e2cfabf4297"
LANDING = "VERIFIED_FULL_FAMILY_DIRECT_REPLAY__FOUR_G76_EXCEPTIONS_RESOLVED_IN_G77"


def digest(path: Path) -> str:
    block = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            block.update(chunk)
    return block.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    manifest = rows(HERE / "REVIEW_MANIFEST.tsv")
    manifest_paths = [row["path"] for row in manifest]
    all_payload_hashes = all(
        (ROOT / row["path"]).is_file() and digest(ROOT / row["path"]) == row["sha256"]
        for row in manifest
    )
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    checks = {
        "review_manifest_hash": digest(HERE / "REVIEW_MANIFEST.tsv") == MANIFEST_SHA256,
        "exact_40_unique_payload_rows": len(manifest) == len(set(manifest_paths)) == 40,
        "all_reviewed_payload_hashes": all_payload_hashes,
        "external_raw_hash": digest(HERE / "EXTERNAL_REVIEW_RAW.md") == RAW_SHA256,
        "external_transcript_hash": digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == TRANSCRIPT_SHA256,
        "required_landing_exact": LANDING in raw and result["landing"] == LANDING,
        "no_external_findings": "No findings." in raw,
        "no_required_corrections": "Correction list: `none`." in raw and result["correction_list"] == [],
        "bounded_scope_preserved": all(
            token in raw
            for token in (
                "does not justify continuum injectivity",
                "physical profile/source/endpoint/scale selection",
                "polarization",
                "bootstrap/action/matter",
                "CMB observable",
            )
        ),
    }
    output = {
        "schema": "udt-cmb-g77-external-review-adjudication-verification-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "manifest_sha256": MANIFEST_SHA256,
        "external_raw_sha256": RAW_SHA256,
        "external_transcript_sha256": TRANSCRIPT_SHA256,
        "landing": LANDING,
    }
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
