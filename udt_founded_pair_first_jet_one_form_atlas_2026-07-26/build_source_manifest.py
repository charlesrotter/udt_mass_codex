#!/usr/bin/env python3
"""Build the preregistered source manifest."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    output = ["path\trole\tgit_blob\tsha256\tsize"]
    for row in rows:
        path = row["path"]
        payload = (ROOT / path).read_bytes()
        blob = subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()
        output.append("\t".join([path, row["role"], blob, hashlib.sha256(payload).hexdigest(), str(len(payload))]))
    (HERE / "SOURCE_MANIFEST.tsv").write_text("\n".join(output) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
