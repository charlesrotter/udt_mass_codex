#!/usr/bin/env python3
"""Build a sealed read-only G222 review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE_REL = HERE.relative_to(ROOT)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g222_review_"))
    files: list[tuple[Path, Path, str]] = []
    for source in sorted(HERE.iterdir()):
        if source.is_file():
            files.append((source, PACKAGE_REL / source.name, "G222_PACKAGE"))

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = ROOT / row["path"]
        if sha(source) != row["sha256"]:
            raise RuntimeError(f"source hash changed: {row['path']}")
        files.append((source, Path(row["path"]), "FROZEN_SOURCE"))

    seen: set[Path] = set()
    manifest_rows: list[tuple[str, str, int, str]] = []
    for source, relative, role in files:
        if relative in seen:
            continue
        seen.add(relative)
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest_rows.append((str(relative), sha(target), target.stat().st_size, role))

    manifest = intake / "REVIEW_MANIFEST.tsv"
    manifest.write_text(
        "path\tsha256\tbytes\trole\n"
        + "".join(f"{path}\t{digest}\t{size}\t{role}\n" for path, digest, size, role in manifest_rows),
        encoding="utf-8",
    )
    scope = {
        "task": "fresh read-only adversarial review of the bounded G222 landing",
        "payload_files": len(manifest_rows),
        "review_manifest_sha256": sha(manifest),
        "permissions": "inspect only intake; bounded read-only checks; no edits; no continuation",
        "network": "not required",
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for path in intake.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o444)
    for path in sorted((p for p in intake.rglob("*") if p.is_dir()), reverse=True):
        os.chmod(path, 0o555)
    os.chmod(intake, 0o555)

    print(json.dumps({
        "intake": str(intake),
        "payload_files": len(manifest_rows),
        "total_files": len(manifest_rows) + 2,
        "review_manifest_sha256": sha(manifest),
        "review_scope_sha256": sha(scope_path),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
