#!/usr/bin/env python3
"""Build a sealed G223 review intake in a supplied empty directory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    dst = args.destination.resolve()
    if dst.exists() and any(dst.iterdir()):
        raise SystemExit("destination must be absent or empty")
    dst.mkdir(parents=True, exist_ok=True)

    package_dst = dst / ROOT.name
    shutil.copytree(ROOT, package_dst, ignore=shutil.ignore_patterns("__pycache__"))

    manifest_rows = (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    source_paths: list[str] = []
    for line in manifest_rows:
        rel = line.split("\t", 1)[0]
        source_paths.append(rel)
        # Preserve repository-relative paths so the registered package verifier
        # runs unchanged inside the sealed intake.
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, target)

    files = sorted(p for p in dst.rglob("*") if p.is_file())
    scope = {
        "status": "SEALED_READ_ONLY_REVIEW_INTAKE",
        "package": ROOT.name,
        "package_files": sum(1 for p in package_dst.rglob("*") if p.is_file()),
        "source_files": len(source_paths),
        "total_payload_files_before_scope": len(files),
        "allowed": ["read", "registered no-write replay", "bounded independent checks"],
        "forbidden": ["edit evidence", "continue research", "inspect outside intake"],
    }
    scope_path = dst / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    print(f"intake={dst}")
    print(f"payload_files={len(files) + 1}")
    print(f"scope_sha256={sha256(scope_path)}")


if __name__ == "__main__":
    main()
