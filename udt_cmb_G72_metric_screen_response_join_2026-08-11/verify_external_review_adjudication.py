#!/usr/bin/env python3
"""Verify the additions-only G72 external-review adjudication layer."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_HASH = "24a19ea21ba1e99cbb9b958aaffab089d3da838313fe33e046b5898c4339a5c8"
TRANSCRIPT_HASH = "d69d5e8df2fed69c88b02a2621c1b6be26d3fc365a49e11fd634b4e4c09acbbf"
REVIEW_MANIFEST_HASH = "feedefd56092817ae9d9984318d975ce5a6cb95308125ebb8edb86bcb543b902"
PROTECTED_PREFIX = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate_review_text(raw: str) -> bool:
    required = (
        "`VERIFIED_AS_CONDITIONAL_RESPONSE`",
        "same supplied calibrated query",
        "physical TT/TE/EE/BB open",
        "`psi` is decisively not the relative polar rotation",
        "zero/constant-source argument is valid only as a local order-zero response statement",
        "SNe P1 remains only a future low-redshift compatibility anchor",
    )
    return raw.startswith(required[0]) and all(token in raw for token in required[1:])


def main() -> None:
    review = table(HERE / "REVIEW_MANIFEST.tsv")
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    checks = {
        "review_manifest_hash": digest(HERE / "REVIEW_MANIFEST.tsv") == REVIEW_MANIFEST_HASH,
        "reviewed_paths": len(review) == 38 and len({row["path"] for row in review}) == 38
        and all(digest(ROOT / row["path"]) == row["sha256"] for row in review),
        "protected_excluded": not any(row["path"].startswith(PROTECTED_PREFIX) for row in review),
        "raw_hash": digest(HERE / "EXTERNAL_REVIEW_RAW.md") == RAW_HASH,
        "transcript_hash": digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == TRANSCRIPT_HASH,
        "external_landing_and_scope": validate_review_text(raw),
        "internal_landing_unchanged": result["landing"]
        == "METRIC_OWNS_SOURCE_FREE_SCREEN_RESPONSE__PHYSICAL_OBSERVABLE_OPEN",
        "g68_values": "3.549305994648684e-24" in raw
        and "0.0023238059699749714" in raw and "0.12946143790625805" in raw,
        "semantic_replay": "semantic mutations were caught `14/14`" in raw,
    }
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT,
        check=True, capture_output=True, text=True
    ).stdout.splitlines()
    protected = [line for line in status if line.startswith("?? " + PROTECTED_PREFIX)]
    checks["protected_metadata"] = len(protected) == 7
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g72-external-adjudication-v1",
        "status": "PASS",
        "external_landing": "VERIFIED_AS_CONDITIONAL_RESPONSE",
        "effective_scientific_landing": result["landing"],
        "reviewed_manifest_rows": len(review),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "protected_untracked_contents_read": False,
    }
    (HERE / "EXTERNAL_REVIEW_LIVE_GATES.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
