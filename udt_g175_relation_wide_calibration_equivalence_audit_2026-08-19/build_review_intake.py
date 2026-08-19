#!/usr/bin/env python3
"""Build a sealed read-only G175 review intake under /tmp."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "6df732bd"
out = Path(tempfile.mkdtemp(prefix="udt_g175_calibration_carry_review_", dir="/tmp"))
package_out = out / HERE.name
package_out.mkdir()

for src in sorted(HERE.iterdir()):
    if src.is_file():
        shutil.copy2(src, package_out / src.name)

for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    if not line.strip():
        continue
    expected, rel, _role = line.split("\t")
    frozen = subprocess.run(
        ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{rel}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    if hashlib.sha256(frozen).hexdigest() != expected:
        raise RuntimeError(rel)
    dst = out / "sources" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(frozen)

tree = []
for path in sorted(p for p in out.rglob("*") if p.is_file()):
    tree.append(
        {
            "path": str(path.relative_to(out)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
    )
scope = {
    "package": HERE.name,
    "files_before_scope": len(tree),
    "tree": tree,
    "restrictions": [
        "read-only",
        "no edits",
        "no research continuation",
        "no repository access",
        "no protected-package access",
        "no internet",
    ],
}
scope_path = out / "REVIEW_SCOPE.json"
scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
for path in out.rglob("*"):
    path.chmod(0o444 if path.is_file() else 0o555)
out.chmod(0o555)
print(
    json.dumps(
        {
            "intake": str(out),
            "files": len(tree) + 1,
            "scope_sha256": hashlib.sha256(scope_path.read_bytes()).hexdigest(),
        },
        sort_keys=True,
    )
)
