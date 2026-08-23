#!/usr/bin/env python3
"""Build the deterministic final G233 evidence manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "FINAL_EVIDENCE_MANIFEST.tsv"


def included(path: Path) -> bool:
    return (
        path.is_file()
        and path != OUT
        and "__pycache__" not in path.parts
        and ".review_runtime" not in path.parts
    )


def main() -> None:
    files = sorted(path for path in ROOT.rglob("*") if included(path))
    lines = ["sha256\tpath"]
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}\t{path.relative_to(ROOT).as_posix()}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(files)} entries to {OUT.name}")


if __name__ == "__main__":
    main()
