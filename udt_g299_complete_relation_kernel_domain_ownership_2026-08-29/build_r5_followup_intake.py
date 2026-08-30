#!/usr/bin/env python3
"""Build a sealed G299 R5-only replay-portability follow-up intake under /tmp."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
LANDING = (
    "ACTIVE_PREMISES_REQUIRE_COMPLETE_CARRY_BUT_DO_NOT_TYPE_THE_KERNEL_DOMAIN"
    "__ARCHITECTURE_REMAINS_OPEN"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g299_r5_followup_", dir="/tmp"))
    shutil.copytree(
        PACKAGE,
        intake / PACKAGE.name,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    source_paths = []
    for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        expected, relative = line.split("\t")
        source = REPO / relative
        assert sha(source) == expected
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        source_paths.append(relative)

    scope = {
        "package": PACKAGE.name,
        "review": "read-only G299 R5 replay-portability completion-only follow-up",
        "allowed": [
            "inspect only this sealed intake",
            "verify only R5_COMPLETION_PREREGISTRATION.md",
            "run the registered python3 -S checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files or continue the research",
            "reopen scientific repairs R1 through R4",
            "change the scientific question landing equations sources premise grade or conclusion",
            "access the repository protected packages internet or observational outcomes",
        ],
        "frozen_sources": source_paths,
        "scientific_landing_unchanged": LANDING,
        "repair_scope": "R5 dependency-free exact production replay only",
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n")

    payloads = sorted(
        path
        for path in intake.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    )
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    rows = ["sha256\tpath"]
    rows.extend(f"{sha(path)}\t{path.relative_to(intake)}" for path in payloads)
    manifest_path.write_text("\n".join(rows) + "\n")
    manifest_sha = sha(manifest_path)
    seal_path = intake / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{manifest_sha}  REVIEW_MANIFEST.tsv\n")

    print(
        json.dumps(
            {
                "intake": str(intake),
                "manifest_payloads": len(payloads),
                "total_files": len(payloads) + 2,
                "scope_sha256": sha(scope_path),
                "manifest_sha256": manifest_sha,
                "detached_seal_sha256": sha(seal_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
