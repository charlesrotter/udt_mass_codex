#!/usr/bin/env python3
"""Build a sealed G238 intake without BOSS outcome artifacts."""

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
PREREG_COMMIT = "cf7deed2"


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


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g238_review_", dir="/tmp"))
    target_package = intake / PACKAGE.name
    target_package.mkdir()
    copied: set[Path] = set()

    for source in sorted(PACKAGE.iterdir()):
        if not source.is_file() or source.name.startswith("EXTERNAL_REVIEW"):
            continue
        copy(source, target_package / source.name, copied)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in source_rows:
        source = ROOT / row["path"]
        if not source.is_file() or digest(source) != row["sha256"]:
            raise RuntimeError(f"source mismatch: {row['path']}")
        copy(source, intake / row["path"], copied)

    committed_prereg = subprocess.check_output(
        ["git", "show", f"{PREREG_COMMIT}:{PACKAGE.name}/PREREGISTRATION.md"], cwd=ROOT
    )
    current_prereg = (PACKAGE / "PREREGISTRATION.md").read_bytes()
    if committed_prereg != current_prereg:
        raise RuntimeError("preregistration differs from committed chronology anchor")
    chronology_target = intake / "chronology" / "PREREGISTRATION_AT_CF7DEED2.md"
    chronology_target.parent.mkdir()
    chronology_target.write_bytes(committed_prereg)
    copied.add(chronology_target)

    entries = [
        {"path": path.relative_to(intake).as_posix(), "sha256": digest(path)}
        for path in sorted(copied)
    ]
    tree_material = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in entries
    ).encode()
    scope = {
        "task": "fresh read-only adversarial review of G238 BAO held-out query typing",
        "instructions": f"{PACKAGE.name}/ADVERSARIAL_REVIEW_REQUEST.md",
        "restrictions": [
            "inspect only this sealed intake",
            "do not inspect or infer BOSS outcome artifacts absent from the intake",
            "run bounded checks only in an ephemeral copy",
            "do not edit evidence files",
            "do not continue the research",
            "do not choose a feature, profile, source model, branch weight, or cosmology",
        ],
        "payload_file_count": len(entries),
        "tree_digest_sha256": hashlib.sha256(tree_material).hexdigest(),
        "files": entries,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
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
