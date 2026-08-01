#!/usr/bin/env python3
"""Build the deterministic forward-only dependency freeze and repair result."""

from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REVIEW = ROOT / "udt_p4_cold_adversarial_review_2026-08-01"
OVERLAY = REVIEW / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv"
FREEZE = HERE / "TRANSITIVE_DEPENDENCY_FREEZE.tsv"
MANIFEST = HERE / "TRANSITIVE_DEPENDENCY_MANIFEST.sha256"
RESULTS = HERE / "REPAIR_RESULTS.json"
STATUS = "FORWARD_CORRECTION_FREEZE_2026-08-01"
PROVENANCE = "DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def main() -> None:
    with OVERLAY.open(newline="") as handle:
        source = list(csv.DictReader(handle, delimiter="\t"))
    fields = [
        "freeze_date",
        "freeze_status",
        "provenance_status",
        "path",
        "sha256",
        "review_base_sha256",
        "review_base_byte_identical",
        "classification",
        "cited_by_count",
        "cited_by",
        "classification_reason",
    ]
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, delimiter="\t", fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in sorted(source, key=lambda item: item["path"]):
        writer.writerow(
            {
                "freeze_date": "2026-08-01",
                "freeze_status": STATUS,
                "provenance_status": PROVENANCE,
                "path": row["path"],
                "sha256": row["sha256"],
                "review_base_sha256": row["base_sha256"],
                "review_base_byte_identical": row["base_byte_identical"],
                "classification": row["classification"],
                "cited_by_count": row["cited_by_count"],
                "cited_by": row["cited_by"],
                "classification_reason": row["classification_reason"],
            }
        )
    FREEZE.write_text(out.getvalue())
    MANIFEST.write_text(
        "".join(f"{row['sha256']}  ../{row['path']}\n" for row in sorted(source, key=lambda item: item["path"]))
    )
    counts = Counter(row["classification"] for row in source)
    summary = ROOT / "P4_ARC_SUMMARY_2026-07-31.md"
    result = {
        "status": "REPAIR_BUILT_PENDING_INDEPENDENT_VERIFICATION",
        "base": "c9c8b3848a7ff85b7941e803bf87c0ff48b9f98c",
        "headline_target": str(summary.relative_to(ROOT)),
        "headline_sha256": sha(summary),
        "cold_review_tree": "d1254e1e018d55ead4b57696629163c3d0006db5",
        "dependency_rows": len(source),
        "load_bearing": counts["LOAD_BEARING"],
        "supporting": counts["SUPPORTING"],
        "freeze_sha256": sha(FREEZE),
        "dependency_manifest_sha256": sha(MANIFEST),
        "provenance": PROVENANCE,
        "maximum_conclusion": "cold-review headline and forward dependency-freeze defects repaired; no T4, stability, adoption, physics, or canon conclusion",
    }
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
