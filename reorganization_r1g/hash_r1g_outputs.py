#!/usr/bin/env python3
"""Write the deterministic SHA-256 inventory for the R1G overlay."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    root = repo / "reorganization_r1g"
    output = args.output.resolve()
    records = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == output or "__pycache__" in path.parts:
            continue
        payload = path.read_bytes()
        records.append((path.relative_to(repo).as_posix(), hashlib.sha256(payload).hexdigest(), len(payload)))
    lines = ["path\tsha256\tsize_bytes"]
    lines.extend(f"{path}\t{digest}\t{size}" for path, digest, size in records)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"hashed_files={len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
