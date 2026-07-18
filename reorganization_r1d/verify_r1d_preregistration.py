#!/usr/bin/env python3
"""Independent fail-closed check of the committed R1D preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

BASE = "b3c50109df90658378d157c65fc723b1265c48c8"
PREFIXES = ("reorganization_r0/", "reorganization_r1a/", "reorganization_r1b/", "reorganization_r1c/")


def git(repo: Path, *args: str, binary: bool = False):
    result = subprocess.run(["git", *args], cwd=repo, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=not binary, check=False)
    assert result.returncode == 0, result.stderr
    return result.stdout


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    out = Path(__file__).resolve().parent
    frozen = json.loads((out / "PREREGISTERED_INPUTS.json").read_text(encoding="utf-8"))
    assert frozen["base"] == BASE
    paths = [p for p in git(repo, "ls-tree", "-r", "--name-only", BASE).splitlines()
             if p.startswith(PREFIXES) or p.startswith("research/_registry/")]
    with (out / "FIXED_HISTORY_SHA256.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [r["path"] for r in rows] == sorted(paths)
    for row in rows:
        payload = git(repo, "show", f"{BASE}:{row['path']}", binary=True)
        assert git(repo, "rev-parse", f"{BASE}:{row['path']}").strip() == row["git_blob_oid"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
        assert len(payload) == int(row["size_bytes"])
    assert hashlib.sha256((out / "FIXED_HISTORY_SHA256.tsv").read_bytes()).hexdigest() == frozen["fixed_history_tsv_sha256"]
    source = git(repo, "show", f"{BASE}:{frozen['source']}", binary=True)
    assert hashlib.sha256(source).hexdigest() == frozen["source_sha256"]
    assert git(repo, "rev-parse", f"{BASE}:{frozen['source']}").strip() == frozen["source_blob"]
    assert source.decode().splitlines()[9] == frozen["source_line_10"]
    assert "../../simple_metric_solution_space_ZOOM.md" not in source.decode()
    assert frozen["fixed_root_inventory_rows"] == 1114
    assert frozen["dirty_path_count"] == 54
    print(json.dumps({"result": "PASS", "fixed_history_rows": len(rows),
                      "fixed_root_artifacts": 1114, "source_blob": frozen["source_blob"],
                      "source_sha256": frozen["source_sha256"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
