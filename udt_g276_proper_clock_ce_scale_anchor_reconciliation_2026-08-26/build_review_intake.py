#!/usr/bin/env python3
"""Build a self-contained sealed G276 read-only review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
PREREG_COMMIT = "e5fddc76"
SEALED_ROOT = (REPO / "REVIEW_SCOPE.json").is_file()


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def frozen_source(relative: str, expected: str) -> bytes:
    sealed = PACKAGE / "sources" / relative
    if sealed.is_file() and digest(sealed.read_bytes()) == expected:
        return sealed.read_bytes()
    if SEALED_ROOT:
        raise AssertionError(f"sealed frozen source unavailable or changed: {relative}")
    live = REPO / relative
    if live.is_file() and digest(live.read_bytes()) == expected:
        return live.read_bytes()
    completed = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative}"],
        cwd=REPO,
        capture_output=True,
        check=True,
    )
    assert digest(completed.stdout) == expected, relative
    return completed.stdout


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g276_review_", dir="/tmp"))
    destination = intake / PACKAGE.name
    destination.mkdir()

    for source in sorted(PACKAGE.iterdir()):
        if source.is_file():
            shutil.copy2(source, destination / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 7
    for row in rows:
        target = destination / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(frozen_source(row["path"], row["sha256"]))

    package_files = [path for path in destination.rglob("*") if path.is_file()]
    total_files = len(package_files) + 2
    manifest_entries = total_files - 1
    scope = {
        "status": "SEALED_READ_ONLY_ADVERSARIAL_REVIEW_INTAKE",
        "package": PACKAGE.name,
        "preregistration_commit": PREREG_COMMIT,
        "file_count_including_scope_and_manifest": total_files,
        "manifest_entry_count_excluding_manifest": manifest_entries,
        "manifest_semantics": (
            "REVIEW_MANIFEST.tsv lists every physical file except itself; its SHA-256 is recorded "
            "externally because a cryptographic self-hash would be recursive"
        ),
        "review_question": (
            "Verify only whether one independent same-segment proper-clock record fixes the one "
            "constant homothety through c_E, rather than merely relabelling units."
        ),
        "allowed": [
            "inspect only this intake",
            "run registered no-write replays or bounded checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "access repository or protected packages outside this intake",
            "inspect observational outcomes",
            "select a clock value, history, distance protocol, relation population, or Xmax",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    assert len(payloads) == manifest_entries
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in payloads:
            payload = path.read_bytes()
            writer.writerow((str(path.relative_to(intake)), digest(payload), len(payload)))
    assert len([path for path in intake.rglob("*") if path.is_file()]) == total_files

    print(
        json.dumps(
            {
                "intake": str(intake),
                "file_count": total_files,
                "scope_sha256": digest(scope_path.read_bytes()),
                "manifest_sha256": digest(manifest_path.read_bytes()),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
