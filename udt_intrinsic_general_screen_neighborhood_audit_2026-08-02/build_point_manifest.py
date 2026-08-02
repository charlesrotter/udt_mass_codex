#!/usr/bin/env python3
"""Hash the 34 exact curvature-invariant point certificates."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
POINT_DIR = HERE / "invariant_points"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = sorted(POINT_DIR.glob("C??_p?.json"))
assert len(paths) == len({path.name for path in paths}) == 34
expected = {f"C{i:02d}_{point}.json" for i in range(1, 18) for point in ("p1", "p2")}
assert {path.name for path in paths} == expected
(HERE / "POINT_MANIFEST.sha256").write_text(
    "\n".join(f"{digest(path)}  {path.relative_to(HERE)}" for path in paths) + "\n",
    encoding="utf-8",
)
print(f"PASS point certificates={len(paths)} manifest_sha256={digest(HERE / 'POINT_MANIFEST.sha256')}")
