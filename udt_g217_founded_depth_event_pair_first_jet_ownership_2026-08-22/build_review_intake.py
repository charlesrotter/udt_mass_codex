#!/usr/bin/env python3
"""Build a fresh sealed G217 adversarial-review intake."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DEST = Path(tempfile.mkdtemp(prefix="udt_g217_review_", dir="/tmp"))
PACKAGE_DEST = DEST / PACKAGE.name
PACKAGE_DEST.mkdir()

package_files = sorted(path for path in PACKAGE.iterdir() if path.is_file())
for source in package_files:
    shutil.copy2(source, PACKAGE_DEST / source.name)

source_rows = []
for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    expected, relative = line.split("\t", 1)
    source = ROOT / relative
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != expected:
        raise AssertionError(f"source hash mismatch: {relative}")
    target = DEST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    source_rows.append(relative)

scope = {
    "audit": "G217",
    "purpose": "fresh bounded adversarial review of founded-depth positive first-jet ownership",
    "review_mode": "fresh_adversarial",
    "package": PACKAGE.name,
    "package_file_count": len(package_files),
    "frozen_source_count": len(source_rows),
    "allowed_actions": ["inspect intake", "run bounded read-only checks", "run registered no-write replay"],
    "forbidden_actions": ["edit evidence", "continue research", "access repository outside intake"],
    "scientific_ceiling": "conditional positive first jet on supplied paired events and depth; no event population or full germ",
}
(DEST / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

rows = []
for path in sorted(item for item in DEST.rglob("*") if item.is_file() and item.name != "REVIEW_MANIFEST.tsv"):
    rows.append((hashlib.sha256(path.read_bytes()).hexdigest(), path.relative_to(DEST).as_posix()))
(DEST / "REVIEW_MANIFEST.tsv").write_text(
    "sha256\tpath\n" + "".join(f"{digest}\t{relative}\n" for digest, relative in rows)
)

for path in DEST.rglob("*"):
    if path.is_file():
        path.chmod(0o444)
for path in sorted((item for item in DEST.rglob("*") if item.is_dir()), reverse=True):
    path.chmod(0o555)
DEST.chmod(0o555)

print(json.dumps({
    "status": "PASS",
    "intake": str(DEST),
    "file_count": len(rows) + 1,
    "package_files": len(package_files),
    "frozen_sources": len(source_rows),
    "scope_sha256": hashlib.sha256((DEST / "REVIEW_SCOPE.json").read_bytes()).hexdigest(),
    "manifest_sha256": hashlib.sha256((DEST / "REVIEW_MANIFEST.tsv").read_bytes()).hexdigest(),
}, sort_keys=True))
