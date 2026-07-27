#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 17 and len({row["path"] for row in rows}) == 17
    output = ["path\tgit_blob\tsha256\trole"]
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        blob = subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT, text=True
        ).strip()
        output.append(f"{row['path']}\t{blob}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\t{row['role']}")
    (HERE / "SOURCE_MANIFEST.tsv").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("PASS source manifest 17")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
