#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser(description="Verify the frozen audit-package manifest")
parser.add_argument("--write", action="store_true", help="refresh PACKAGE_VERIFICATION.json")
args = parser.parse_args()

rows = []
for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected, name = line.split(None, 1)
    path = HERE / name.strip()
    assert path.is_file() and digest(path) == expected
    rows.append(name.strip())
assert len(rows) == len(set(rows))
result = {
    "status": "PASS",
    "package_members": len(rows),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
}
if args.write:
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
