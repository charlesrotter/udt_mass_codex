#!/usr/bin/env python3
"""Verify the final ontology-audit package manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent


def main() -> None:
    manifest = PKG / "PACKAGE_MANIFEST.sha256"
    entries = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        path = PKG / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"package manifest mismatch: {name}")
        entries.append(name)
    expected = sorted(path.name for path in PKG.iterdir() if path.is_file() and path != manifest)
    if entries != expected or len(entries) != len(set(entries)):
        raise RuntimeError("package manifest coverage/order/uniqueness failure")
    print(f"PASS package manifest: files={len(entries)}")


if __name__ == "__main__":
    main()
