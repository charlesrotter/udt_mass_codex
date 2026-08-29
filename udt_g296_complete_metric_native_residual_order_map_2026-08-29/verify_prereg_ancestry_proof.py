#!/usr/bin/env python3
"""Verify the G296 preregistration ancestry proof without Git or third-party packages."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROOF = HERE / "PREREG_ANCESTRY_PROOF.json"
EXPECTED_COMMIT = "f7a050f054d83583c449b9854ce9b17b7d2f2186"
EXPECTED_FILES = (
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
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
    assert cursor == len(payload)
    return rows


def main() -> None:
    proof = json.loads(PROOF.read_text(encoding="utf-8"))
    commit_raw = base64.b64decode(proof["commit_object_base64"], validate=True)
    root_tree_raw = base64.b64decode(proof["root_tree_object_base64"], validate=True)
    package_tree_raw = base64.b64decode(proof["package_tree_object_base64"], validate=True)

    assert proof["commit"] == EXPECTED_COMMIT
    assert object_id("commit", commit_raw) == EXPECTED_COMMIT
    tree_line = next(line for line in commit_raw.splitlines() if line.startswith(b"tree "))
    root_tree_id = tree_line.split()[1].decode("ascii")
    assert root_tree_id == proof["commit_tree"]
    assert object_id("tree", root_tree_raw) == root_tree_id

    root_rows = parse_tree(root_tree_raw)
    package_rows = [row for row in root_rows if row[1] == proof["package"]]
    assert len(package_rows) == 1 and package_rows[0][0] == "40000"
    assert package_rows[0][2] == proof["package_tree"]
    assert object_id("tree", package_tree_raw) == proof["package_tree"]

    package_rows = parse_tree(package_tree_raw)
    assert tuple(row[1] for row in package_rows) == EXPECTED_FILES
    assert tuple(proof["preregistered_files"]) == EXPECTED_FILES
    assert proof["implementation_or_outcome_files_in_prereg_tree"] == []
    for mode, name, digest in package_rows:
        assert mode == "100644"
        assert object_id("blob", (HERE / name).read_bytes()) == digest

    result = {
        "all_pass": True,
        "commit": EXPECTED_COMMIT,
        "commit_hash_verified": True,
        "root_tree_link_verified": True,
        "package_tree_link_verified": True,
        "preregistered_blobs_verified": len(package_rows),
        "only_four_preregistration_files": True,
        "implementation_or_outcome_files_present": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
