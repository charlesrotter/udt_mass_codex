#!/usr/bin/env python3
"""Export bounded Git evidence that G237 preregistration preceded computation."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import subprocess


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
COMMIT = "ad49b9c8"
RELATIVE = f"{PACKAGE.name}/PREREGISTRATION.md"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def git_blob_sha1(data: bytes) -> str:
    payload = b"blob " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def git_commit_sha1(data: bytes) -> str:
    payload = b"commit " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def git_object_sha1(kind: str, data: bytes) -> str:
    payload = kind.encode() + b" " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def parse_tree(data: bytes) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    cursor = 0
    while cursor < len(data):
        space = data.index(b" ", cursor)
        nul = data.index(b"\0", space)
        mode = data[cursor:space].decode()
        name = data[space + 1:nul].decode()
        object_id = data[nul + 1:nul + 21].hex()
        entries[name] = (mode, object_id)
        cursor = nul + 21
    return entries


def main() -> None:
    commit_full = git("rev-parse", COMMIT).decode().strip()
    commit_body = git("cat-file", "-p", commit_full)
    root_tree = commit_body.splitlines()[0].decode().split()[1]
    root_tree_raw = git("cat-file", "tree", root_tree)
    root_entries = parse_tree(root_tree_raw)
    package_tree = root_entries[PACKAGE.name][1]
    package_tree_raw = git("cat-file", "tree", package_tree)
    committed_prereg = git("show", f"{commit_full}:{RELATIVE}")
    current_prereg = (PACKAGE / "PREREGISTRATION.md").read_bytes()
    tree_line = git("ls-tree", commit_full, RELATIVE).decode().strip()
    blob = tree_line.split()[2]
    result = {
        "audit": "G237_PREREGISTRATION_CHRONOLOGY_PROOF",
        "status": "PASS",
        "commit": commit_full,
        "commit_recomputed_sha1": git_commit_sha1(commit_body),
        "parent": git("rev-parse", f"{commit_full}^").decode().strip(),
        "tree_line": tree_line,
        "registered_blob": blob,
        "committed_blob_recomputed_sha1": git_blob_sha1(committed_prereg),
        "committed_prereg_sha256": hashlib.sha256(committed_prereg).hexdigest(),
        "current_prereg_sha256": hashlib.sha256(current_prereg).hexdigest(),
        "committed_equals_current": committed_prereg == current_prereg,
        "commit_body": commit_body.decode(),
        "ceiling": (
            "Git proves committed object identity, ancestry, and preregistration contents; "
            "it cannot prove the retroactive absence of untracked private computation."
        ),
    }
    checks = [
        result["commit"] == result["commit_recomputed_sha1"],
        result["registered_blob"] == result["committed_blob_recomputed_sha1"],
        result["committed_equals_current"] is True,
    ]
    result["status"] = "PASS" if all(checks) else "FAIL"
    (PACKAGE / "CHRONOLOGY_PROOF.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    bundle = {
        "audit": "G237_MINIMAL_GIT_OBJECT_BUNDLE",
        "commit": commit_full,
        "parent": result["parent"],
        "root_tree": root_tree,
        "package_name": PACKAGE.name,
        "package_tree": package_tree,
        "preregistration_name": "PREREGISTRATION.md",
        "preregistration_blob": blob,
        "commit_body_base64": base64.b64encode(commit_body).decode(),
        "root_tree_raw_base64": base64.b64encode(root_tree_raw).decode(),
        "package_tree_raw_base64": base64.b64encode(package_tree_raw).decode(),
        "preregistration_raw_base64": base64.b64encode(committed_prereg).decode(),
        "preregistration_sha256": hashlib.sha256(committed_prereg).hexdigest(),
    }
    bundle_checks = [
        git_object_sha1("commit", commit_body) == bundle["commit"],
        git_object_sha1("tree", root_tree_raw) == bundle["root_tree"],
        git_object_sha1("tree", package_tree_raw) == bundle["package_tree"],
        git_object_sha1("blob", committed_prereg) == bundle["preregistration_blob"],
    ]
    bundle["export_status"] = "PASS" if all(bundle_checks) else "FAIL"
    (PACKAGE / "CHRONOLOGY_OBJECT_BUNDLE.json").write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: result[key] for key in result if key != "commit_body"}, indent=2))
    if result["status"] != "PASS" or bundle["export_status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
