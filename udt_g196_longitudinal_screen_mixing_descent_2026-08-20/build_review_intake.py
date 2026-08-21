#!/usr/bin/env python3
"""Build a sealed G196 adversarial-review intake without transmitting it."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g196_review_"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()
    review_runtime = intake / ".review_runtime"
    review_runtime.mkdir()
    payload_rows = []

    for source in sorted(PACKAGE.iterdir()):
        if not source.is_file() or source.name == "build_review_intake.py":
            continue
        relative = Path(PACKAGE.name) / source.name
        target = package_target / source.name
        shutil.copy2(source, target)
        payload_rows.append(
            {"path": str(relative), "sha256": digest(target), "role": "G196 package"}
        )

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    for row in sources:
        relative = Path(row["path"])
        source = ROOT / relative
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied_digest = digest(target)
        if copied_digest != row["sha256"]:
            raise SystemExit(f"source drift while sealing {relative}")
        payload_rows.append(
            {"path": str(relative), "sha256": copied_digest, "role": row["role"]}
        )

    if len({row["path"] for row in payload_rows}) != len(payload_rows):
        raise SystemExit("duplicate sealed path")

    scope = {
        "schema": "udt-sealed-review-scope-v1",
        "task": "G196 fresh read-only adversarial review",
        "payload_file_count": len(payload_rows),
        "total_file_count_including_scope": len(payload_rows) + 1,
        "restrictions": [
            "inspect only this intake",
            "do not edit evidence files",
            "do not continue the research",
            "run only the registered no-write replay or bounded read-only checks",
        ],
        "registered_replay": (
            "TMPDIR=.review_runtime TMP=.review_runtime TEMP=.review_runtime "
            "G196_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 "
            f"{PACKAGE.name}/verify_package.py --no-write"
        ),
        "files": sorted(payload_rows, key=lambda row: row["path"]),
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
                "payload_file_count": len(payload_rows),
                "total_file_count": len(tree_lines),
                "review_scope_sha256": digest(scope_path),
                "tree_sha256": tree_digest,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
