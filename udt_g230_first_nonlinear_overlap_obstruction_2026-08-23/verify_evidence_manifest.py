#!/usr/bin/env python3
"""Verify the deterministic G230 evidence manifest and package coverage."""

from __future__ import annotations

import csv
import hashlib

from build_evidence_manifest import FILES, ROOT


def main() -> None:
    with (ROOT / "EVIDENCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["path"] for row in rows] == list(FILES)
    assert len(rows) == len(FILES)
    for row in rows:
        payload = (ROOT / row["path"]).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
        assert len(payload) == int(row["bytes"])
    ignored = {"EVIDENCE_MANIFEST.tsv"}
    present = {
        path.name
        for path in ROOT.iterdir()
        if path.is_file() and path.name not in ignored
    }
    assert present == set(FILES), f"manifest coverage mismatch: {sorted(present ^ set(FILES))}"
    print(f"PASS: G230 manifest {len(rows)} rows, hashes and coverage exact")


if __name__ == "__main__":
    main()
