#!/usr/bin/env python3
"""Build a cryptographically self-contained proof of the G296 preregistration tree."""

from __future__ import annotations

import base64
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "PREREG_ANCESTRY_PROOF.json"
COMMIT = "f7a050f054d83583c449b9854ce9b17b7d2f2186"
PACKAGE = HERE.name
EXPECTED_FILES = (
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
)


def git_object(kind: str, object_id: str) -> bytes:
    return subprocess.check_output(
        ["git", "cat-file", kind, object_id], cwd=ROOT
    )


def object_id(kind: str, payload: bytes) -> str:
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def parse_tree(payload: bytes):
    rows = []
    cursor = 0
    while cursor < len(payload):
        space = payload.index(b" ", cursor)
        nul = payload.index(b"\0", space)
        mode = payload[cursor:space].decode("ascii")
        name = payload[space + 1:nul].decode("utf-8", "surrogateescape")
        digest = payload[nul + 1:nul + 21].hex()
        rows.append((mode, name, digest))
        cursor = nul + 21
    return rows


def main() -> None:
    commit_raw = git_object("commit", COMMIT)
    assert object_id("commit", commit_raw) == COMMIT
    tree_line = next(line for line in commit_raw.splitlines() if line.startswith(b"tree "))
    root_tree_id = tree_line.split()[1].decode("ascii")
    root_tree_raw = git_object("tree", root_tree_id)
    assert object_id("tree", root_tree_raw) == root_tree_id
    root_rows = parse_tree(root_tree_raw)
    package_rows = [row for row in root_rows if row[1] == PACKAGE]
    assert len(package_rows) == 1 and package_rows[0][0] == "40000"
    package_tree_id = package_rows[0][2]
    package_tree_raw = git_object("tree", package_tree_id)
    assert object_id("tree", package_tree_raw) == package_tree_id
    package_tree_rows = parse_tree(package_tree_raw)
    assert tuple(row[1] for row in package_tree_rows) == EXPECTED_FILES

    for mode, name, digest in package_tree_rows:
        assert mode == "100644"
        payload = (HERE / name).read_bytes()
        assert object_id("blob", payload) == digest

    result = {
        "all_pass": True,
        "commit": COMMIT,
        "commit_object_base64": base64.b64encode(commit_raw).decode("ascii"),
        "commit_tree": root_tree_id,
        "root_tree_object_base64": base64.b64encode(root_tree_raw).decode("ascii"),
        "package": PACKAGE,
        "package_tree": package_tree_id,
        "package_tree_object_base64": base64.b64encode(package_tree_raw).decode("ascii"),
        "preregistered_files": list(EXPECTED_FILES),
        "implementation_or_outcome_files_in_prereg_tree": [],
        "proof_type": "raw Git commit and linked tree objects plus sealed preregistration blobs",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_pass": True,
        "commit": COMMIT,
        "package_tree": package_tree_id,
        "preregistered_files": len(EXPECTED_FILES),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
