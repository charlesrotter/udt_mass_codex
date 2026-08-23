#!/usr/bin/env python3
"""Verify the deterministic G231 evidence manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    lines = (ROOT / "EVIDENCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    assert lines[0] == "path\tsha256\tbytes"
    seen = set()
    for line in lines[1:]:
        name, digest, size_text = line.split("\t")
        assert name not in seen
        seen.add(name)
        payload = (ROOT / name).read_bytes()
        assert len(payload) == int(size_text)
        assert hashlib.sha256(payload).hexdigest() == digest
    assert len(seen) == 28
    print("PASS: verified 28 exact G231 evidence files")


if __name__ == "__main__":
    main()
