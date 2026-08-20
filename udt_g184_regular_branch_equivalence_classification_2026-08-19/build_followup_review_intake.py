#!/usr/bin/env python3
"""Build a sealed repair-only follow-up intake for G184."""

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run():
    intake = Path(tempfile.mkdtemp(prefix="udt_g184_repair_followup_"))
    target_root = intake / ROOT.name
    target_root.mkdir()
    excluded = {
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSCRIPT.txt.gz",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "FOLLOWUP_TRANSMISSION_RECORD.md",
    }
    for source in sorted(ROOT.iterdir()):
        if source.is_file() and source.name not in excluded:
            shutil.copy2(source, target_root / source.name)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = REPO / row["path"]
        target = intake / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    files = []
    for path in sorted(item for item in intake.rglob("*") if item.is_file()):
        files.append({
            "path": str(path.relative_to(intake)),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        })
    scope = {
        "audit": "G184 repair-only follow-up",
        "mode": "read-only packaging-repair verification",
        "allowed_root": str(intake),
        "file_count_without_scope": len(files),
        "files": files,
        "restrictions": [
            "inspect only this intake",
            "verify only the preregistered no-write live-helper replay repair",
            "do not edit files",
            "do not continue the research",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "payload_files": len(files),
        "total_files": len(files) + 1,
        "review_scope_sha256": sha256(scope_path),
    }, sort_keys=True))


if __name__ == "__main__":
    run()
