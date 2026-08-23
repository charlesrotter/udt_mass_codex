#!/usr/bin/env python3
"""Verify exact membership and hashes of the final G233 evidence package."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "FINAL_EVIDENCE_MANIFEST.tsv"


def included(path: Path) -> bool:
    return (
        path.is_file()
        and path != MANIFEST
        and "__pycache__" not in path.parts
        and ".review_runtime" not in path.parts
    )


def main() -> None:
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "sha256\tpath":
        raise SystemExit("invalid final manifest header")
    registered = {}
    for line in lines[1:]:
        digest, relative = line.split("\t")
        if relative in registered:
            raise SystemExit(f"duplicate final manifest path: {relative}")
        registered[relative] = digest
    actual = {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in ROOT.rglob("*")
        if included(path)
    }
    if registered != actual:
        missing = sorted(set(actual) - set(registered))
        extra = sorted(set(registered) - set(actual))
        changed = sorted(k for k in set(actual) & set(registered) if actual[k] != registered[k])
        raise SystemExit(f"final manifest mismatch: missing={missing}, extra={extra}, changed={changed}")
    print(f"PASS: {len(actual)} final G233 evidence hashes and exact membership")


if __name__ == "__main__":
    main()
