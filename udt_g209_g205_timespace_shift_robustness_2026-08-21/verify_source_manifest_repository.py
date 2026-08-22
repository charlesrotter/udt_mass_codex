#!/usr/bin/env python3
"""Verify G209 source hashes in the live repository; package replay does not depend on this."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUT = PACKAGE / "SOURCE_PROVENANCE_VERIFICATION.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checked = []
    for row in rows:
        path = ROOT / row["path"]
        actual = digest(path)
        if actual != row["sha256"]:
            raise AssertionError(f"source hash mismatch: {row['path']}")
        checked.append(row["path"])
    result = {
        "status": "PASS",
        "checked_in_live_repository_context": len(checked),
        "paths": checked,
        "package_replay_dependency": False,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
