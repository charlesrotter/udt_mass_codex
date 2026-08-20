#!/usr/bin/env python3
"""Build a sealed G194 repair-only follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g194_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()
    review_runtime = intake / ".review_runtime"
    review_runtime.mkdir()

    included = []
    for source in sorted(PACKAGE.iterdir()):
        if not source.is_file() or source.name == "build_review_intake.py":
            continue
        target = package_target / source.name
        shutil.copy2(source, target)
        included.append(target)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        source = ROOT / row["path"]
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        included.append(target)

    scope = {
        "package": PACKAGE.name,
        "purpose": "read-only G194 R5 repair-only follow-up review",
        "restrictions": [
            "inspect only this intake",
            "do not edit evidence files",
            "do not continue the research",
            "run only the registered no-write replay",
            "verify only preregistered R5, retained R2/R3, and the unchanged bounded landing",
            "the replay must leave .review_runtime empty",
        ],
        "registered_replay": (
            "G194_REVIEW_RUNTIME_REQUIRED=1 TMPDIR=.review_runtime TMP=.review_runtime "
            "TEMP=.review_runtime PYTHONDONTWRITEBYTECODE=1 python3 "
            f"{PACKAGE.name}/verify_package.py --no-write"
        ),
        "payload_files": len(included),
        "files": [
            {"path": str(path.relative_to(intake)), "sha256": digest(path)}
            for path in sorted(included)
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    tree_lines = []
    for path in sorted(intake.rglob("*")):
        if path.is_file():
            tree_lines.append(f"{path.relative_to(intake)}\t{digest(path)}")
    tree_digest = hashlib.sha256(("\n".join(tree_lines) + "\n").encode()).hexdigest()

    for path in sorted(intake.rglob("*"), reverse=True):
        if path.is_file():
            path.chmod(0o444)
        elif path.is_dir():
            path.chmod(0o555)
    review_runtime.chmod(0o700)
    intake.chmod(0o555)

    print(
        json.dumps(
            {
                "intake": str(intake),
                "payload_files": len(included),
                "total_files": len(tree_lines),
                "scope_sha256": digest(scope_path),
                "tree_sha256": tree_digest,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
