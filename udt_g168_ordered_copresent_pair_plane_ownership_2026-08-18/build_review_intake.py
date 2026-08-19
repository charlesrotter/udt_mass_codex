#!/usr/bin/env python3
"""Build a sealed G168 review intake under /tmp."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
out = Path(tempfile.mkdtemp(prefix="udt_g168_pair_plane_review_", dir="/tmp"))
package_out = out / HERE.name
package_out.mkdir()

exclude = {"build_review_intake.py"}
copied = []
for src in sorted(HERE.iterdir()):
    if src.is_file() and src.name not in exclude:
        dst = package_out / src.name
        shutil.copy2(src, dst)
        copied.append(dst)

for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    expected, rel, _role = line.split("\t")
    src = ROOT / rel
    actual = hashlib.sha256(src.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"source drift: {rel}")
    dst = out / "sources" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    copied.append(dst)

tree_rows = []
for path in sorted(p for p in out.rglob("*") if p.is_file()):
    tree_rows.append(
        {
            "path": str(path.relative_to(out)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
    )
scope = {
    "package": HERE.name,
    "files_before_scope": len(tree_rows),
    "tree": tree_rows,
    "restrictions": [
        "read-only",
        "no edits",
        "no continuation of research",
        "no repository access outside intake",
        "no protected-package access",
        "no internet",
    ],
}
scope_path = out / "REVIEW_SCOPE.json"
scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
digest = hashlib.sha256(scope_path.read_bytes()).hexdigest()
print(json.dumps({"intake": str(out), "files": len(tree_rows) + 1, "scope_sha256": digest}, sort_keys=True))
