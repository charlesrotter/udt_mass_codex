#!/usr/bin/env python3
"""Repository-context provenance gate for G206 sources."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parent
OUT = PACKAGE / "SOURCE_PROVENANCE_VERIFICATION.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    checked: list[str] = []
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = REPOSITORY / row["path"]
            assert path.is_file(), row["path"]
            assert sha256(path) == row["sha256"], row["path"]
            checked.append(row["path"])
    result = {
        "all_pass": True,
        "checked_in_live_repository_context": len(checked),
        "package_replay_dependency": False,
        "paths": checked,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
