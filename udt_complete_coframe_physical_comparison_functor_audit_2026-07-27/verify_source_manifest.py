#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def blob(path: Path) -> str:
    result = subprocess.run(["git", "hash-object", str(path)], cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE)
    return result.stdout.strip()


def main() -> int:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        scope = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    assert len(scope) == len(manifest) == 20
    assert [(row["source_id"], row["path"]) for row in scope] == [(row["source_id"], row["path"]) for row in manifest]
    for row in manifest:
        path = ROOT / row["path"]
        assert path.is_file()
        assert blob(path) == row["git_blob"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    print(json.dumps({"result": "PASS", "sources": 20}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
