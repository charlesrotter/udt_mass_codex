#!/usr/bin/env python3
"""Build a sealed G128 external-review intake from committed files only."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE = HERE.name


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    committed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "--", PACKAGE],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = [row["path"] for row in csv.DictReader(stream, delimiter="\t")]
    paths = sorted(set(committed + sources))
    intake = Path(tempfile.mkdtemp(prefix="udt_g128_review_"))
    entries = []
    for relative in paths:
        source = ROOT / relative
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        entries.append(
            {"path": relative, "sha256": digest(destination), "bytes": destination.stat().st_size}
        )
    scope = {
        "purpose": "read-only adversarial review of bounded G128 finite-path screen persistence",
        "repository_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
        ).stdout.strip(),
        "restrictions": [
            "inspect only files listed in this scope",
            "do not edit files",
            "do not continue the research",
            "do not access repository files outside the intake",
            "do not access protected packages",
            "do not use the internet",
        ],
        "files": entries,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "intake": str(intake),
                "file_count_including_scope": len(entries) + 1,
                "scope_sha256": digest(scope_path),
                "repository_commit": scope["repository_commit"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
