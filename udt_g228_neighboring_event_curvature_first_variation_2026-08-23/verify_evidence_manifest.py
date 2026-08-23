#!/usr/bin/env python3
"""Verify the frozen G228 evidence manifest without writing."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    rows = (ROOT / "EVIDENCE_MANIFEST.tsv").read_text().splitlines()
    assert rows[0] == "path\tbytes\tsha256"
    for row in rows[1:]:
        name, size, digest = row.split("\t")
        data = (ROOT / name).read_bytes()
        assert len(data) == int(size), name
        assert hashlib.sha256(data).hexdigest() == digest, name
    print(f"PASS: {len(rows) - 1} G228 evidence entries")


if __name__ == "__main__":
    main()
