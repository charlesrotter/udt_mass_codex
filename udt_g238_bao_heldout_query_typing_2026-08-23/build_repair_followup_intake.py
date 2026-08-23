#!/usr/bin/env python3
"""Build the sealed G238 repair-only follow-up intake without BOSS outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
ORIGINAL_PREREG_COMMIT = "cf7deed2"
REPAIR_PREREG_COMMIT = "f064dcd8"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def copy(source: Path, target: Path, copied: set[Path]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    copied.add(target)


def committed_file(commit: str, name: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{PACKAGE.name}/{name}"], cwd=ROOT
    )


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g238_repair_followup_", dir="/tmp"))
    target_package = intake / PACKAGE.name
    target_package.mkdir()
    copied: set[Path] = set()

    for source in sorted(PACKAGE.iterdir()):
        if source.is_file():
            copy(source, target_package / source.name, copied)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in source_rows:
        source = ROOT / row["path"]
        if not source.is_file() or digest(source) != row["sha256"]:
            raise RuntimeError(f"source mismatch: {row['path']}")
        copy(source, intake / row["path"], copied)

    chronology = (
        (ORIGINAL_PREREG_COMMIT, "PREREGISTRATION.md", "PREREGISTRATION_AT_CF7DEED2.md"),
        (REPAIR_PREREG_COMMIT, "REPAIR_PREREGISTRATION.md", "REPAIR_PREREGISTRATION_AT_F064DCD8.md"),
    )
    for commit, source_name, target_name in chronology:
        committed = committed_file(commit, source_name)
        current = (PACKAGE / source_name).read_bytes()
        if committed != current:
            raise RuntimeError(f"{source_name} differs from committed chronology anchor")
        target = intake / "chronology" / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(committed)
        copied.add(target)

    entries = [
        {"path": path.relative_to(intake).as_posix(), "sha256": digest(path)}
        for path in sorted(copied)
    ]
    tree_material = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in entries
    ).encode()
    scope = {
        "task": "read-only repair-only follow-up review of G238 R1 and R2",
        "instructions": f"{PACKAGE.name}/REPAIR_FOLLOWUP_REQUEST.md",
        "restrictions": [
            "inspect only this sealed intake",
            "verify only preregistered repairs R1 and R2 and the retained bounded landing",
            "do not inspect or infer BOSS outcome artifacts absent from the intake",
            "run checks only in a writable ephemeral copy",
            "do not edit evidence files",
            "do not continue the research",
        ],
        "payload_file_count": len(entries),
        "tree_digest_sha256": hashlib.sha256(tree_material).hexdigest(),
        "files": entries,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    for path in sorted(intake.rglob("*"), reverse=True):
        path.chmod(0o555 if path.is_dir() else 0o444)
    intake.chmod(0o555)
    print(
        json.dumps(
            {
                "intake": str(intake),
                "payload_file_count": len(entries),
                "total_file_count_including_scope": len(entries) + 1,
                "tree_digest_sha256": scope["tree_digest_sha256"],
                "review_scope_sha256": digest(scope_path),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
