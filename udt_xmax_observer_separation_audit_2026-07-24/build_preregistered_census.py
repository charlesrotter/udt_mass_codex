#!/usr/bin/env python3
"""Freeze the tracked textual X_max candidate universe before adjudication."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ALLOWED_SUFFIXES = {".md", ".tsv", ".json", ".py", ".txt", ".tex"}
TOKEN = re.compile(r"X_max|Xmax|x_max|xmax|X_MAX|X_\{\\max\}")
EXPECTED_COUNT = 854


def git(*arguments: str) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.decode("utf-8", "replace"))
    return completed.stdout


def main() -> None:
    candidates = []
    for raw in git("ls-files", "-z").split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8", "surrogateescape")
        path = ROOT / relative
        if path.suffix.lower() not in ALLOWED_SUFFIXES or not path.is_file():
            continue
        payload = path.read_bytes()
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        matching_lines = sum(1 for line in text.splitlines() if TOKEN.search(line))
        if not matching_lines:
            continue
        blob = git("rev-parse", f"HEAD:{relative}").decode().strip()
        candidates.append(
            {
                "candidate_id": f"X{len(candidates) + 1:04d}",
                "path": relative,
                "git_blob": blob,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
                "matching_lines": matching_lines,
            }
        )
    if len(candidates) != EXPECTED_COUNT:
        raise AssertionError(
            f"candidate count changed: expected {EXPECTED_COUNT}, found {len(candidates)}"
        )
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        fields = [
            "candidate_id",
            "path",
            "git_blob",
            "sha256",
            "size_bytes",
            "matching_lines",
        ]
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(candidates)
    identity = "\n".join(row["path"] for row in candidates).encode()
    print(f"candidate_count={len(candidates)}")
    print(f"path_identity_sha256={hashlib.sha256(identity).hexdigest()}")


if __name__ == "__main__":
    main()
