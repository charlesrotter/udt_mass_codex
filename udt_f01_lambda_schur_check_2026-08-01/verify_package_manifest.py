#!/usr/bin/env python3
"""Verify the F01 package SHA-256 manifest without rewriting it."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PKG = Path(__file__).resolve().parent


def main() -> None:
    lines = (PKG / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    names = []
    for line in lines:
        expected, name = line.split(None, 1)
        path = PKG / name.strip()
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        names.append(name.strip())
    assert len(names) == len(set(names))
    actual = sorted(
        path.name
        for path in PKG.iterdir()
        if path.is_file() and path.name not in {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION_RESULT.json"}
    )
    assert sorted(names) == actual
    result = {"status": "PASS", "manifested_files": len(names), "exact_file_set": True}
    (PKG / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
