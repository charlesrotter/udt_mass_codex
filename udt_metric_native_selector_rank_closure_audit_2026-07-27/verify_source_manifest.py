#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 18
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file()
        assert str(path.stat().st_size) == row["size"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        blob = subprocess.check_output(
            ["git", "rev-parse", "HEAD:" + row["path"]], cwd=ROOT, text=True
        ).strip()
        assert blob == row["git_blob"]
    print(json.dumps({"schema": "udt.selector_rank.sources.v1", "result": "PASS", "rows": 18}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
