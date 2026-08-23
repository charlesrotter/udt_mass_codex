#!/usr/bin/env python3
"""Verify the minimal G237 Git chronology bundle without a live Git repository."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
BUNDLE = PACKAGE / "CHRONOLOGY_OBJECT_BUNDLE.json"
OUT = PACKAGE / "CHRONOLOGY_BUNDLE_VERIFICATION.json"


def object_id(kind: str, data: bytes) -> str:
    payload = kind.encode() + b" " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def parse_tree(data: bytes) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    cursor = 0
    while cursor < len(data):
        space = data.index(b" ", cursor)
        nul = data.index(b"\0", space)
        if nul + 21 > len(data):
            raise ValueError("truncated tree entry")
        mode = data[cursor:space].decode()
        name = data[space + 1:nul].decode()
        oid = data[nul + 1:nul + 21].hex()
        entries[name] = (mode, oid)
        cursor = nul + 21
    return entries


def main() -> None:
    bundle = json.loads(BUNDLE.read_text())
    commit_body = base64.b64decode(bundle["commit_body_base64"], validate=True)
    root_raw = base64.b64decode(bundle["root_tree_raw_base64"], validate=True)
    package_raw = base64.b64decode(bundle["package_tree_raw_base64"], validate=True)
    prereg_raw = base64.b64decode(bundle["preregistration_raw_base64"], validate=True)
    root_entries = parse_tree(root_raw)
    package_entries = parse_tree(package_raw)
    commit_lines = commit_body.decode().splitlines()
    declared_root = commit_lines[0].split()[1]
    declared_parent = commit_lines[1].split()[1]
    current_prereg = (PACKAGE / "PREREGISTRATION.md").read_bytes()
    checks = {
        "bundle_export_status": bundle.get("export_status") == "PASS",
        "commit_object": object_id("commit", commit_body) == bundle["commit"],
        "commit_root_link": declared_root == bundle["root_tree"],
        "commit_parent_link": declared_parent == bundle["parent"],
        "root_tree_object": object_id("tree", root_raw) == bundle["root_tree"],
        "root_to_package_link": root_entries.get(bundle["package_name"], (None, None))[1]
        == bundle["package_tree"],
        "package_tree_object": object_id("tree", package_raw) == bundle["package_tree"],
        "package_to_prereg_link": package_entries.get(
            bundle["preregistration_name"], (None, None)
        )[1]
        == bundle["preregistration_blob"],
        "preregistration_blob_object": object_id("blob", prereg_raw)
        == bundle["preregistration_blob"],
        "preregistration_sha256": hashlib.sha256(prereg_raw).hexdigest()
        == bundle["preregistration_sha256"],
        "committed_equals_current": prereg_raw == current_prereg,
    }
    result = {
        "audit": "G237_SELF_CONTAINED_CHRONOLOGY_BUNDLE_VERIFICATION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "requires_live_git": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
