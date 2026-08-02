#!/usr/bin/env python3
"""Fail-closed integrity check for the frozen reciprocal-closure preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique(table: list[dict[str, str]], key: str, expected: int) -> bool:
    values = [row[key] for row in table]
    return len(values) == expected and len(set(values)) == expected and all(values)


def git_blob(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    premises = rows("PREMISE_LEDGER.tsv")
    candidates = rows("CANDIDATE_UNIVERSE.tsv")
    falsifiers = rows("FALSIFICATION_CONTRACT.tsv")
    sources = rows("SOURCE_INVENTORY.tsv")

    checks: dict[str, bool] = {
        "premises_20_unique": unique(premises, "id", 20),
        "candidates_10_unique": unique(candidates, "id", 10),
        "falsifiers_15_unique": unique(falsifiers, "id", 15),
        "sources_24_unique_ids": unique(sources, "id", 24),
        "sources_24_unique_paths": unique(sources, "path", 24),
        "null_outcome_retained": any(row["id"] == "C10" for row in candidates),
        "free_candidate_premises_visible": all(
            any(row["id"] == pid and row["status_before_audit"].startswith("FREE_") for row in premises)
            for pid in ("P14", "P15", "P16", "P17")
        ),
        "historical_sources_not_affirmative": all(
            row["affirmative_authority"].startswith("NO_") for row in sources if row["id"] in {"S05", "S06"}
        ),
    }

    path_checks = []
    for row in sources:
        path = ROOT / row["path"]
        exists = path.is_file()
        data = path.read_bytes() if exists else b""
        sha_ok = exists and hashlib.sha256(data).hexdigest() == row["sha256"]
        blob_ok = exists and git_blob(data) == row["git_blob"]
        path_checks.append(exists and sha_ok and blob_ok)
    checks["all_source_files_exist"] = all((ROOT / row["path"]).is_file() for row in sources)
    checks["all_source_sha256_and_blobs_match"] = all(path_checks)

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "counts": {
            "premises": len(premises),
            "candidates": len(candidates),
            "falsifiers": len(falsifiers),
            "sources": len(sources),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
