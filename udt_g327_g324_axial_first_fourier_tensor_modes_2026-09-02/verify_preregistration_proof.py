#!/usr/bin/env python3
"""Dependency-free verifier for the sealed G327 preregistration commit proof."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


COMMIT = "9bec301bc265bf67afa5f8398f7557ccdabb855b"
PREFIX = "udt_g327_g324_axial_first_fourier_tensor_modes_2026-09-02/"
FILES = {
    PREFIX + "COMPLETENESS_MAP.md": "90164d56a09cc658104ee99666f328b9e0a61be0",
    PREFIX + "MAP.md": "e9ec11a0557b1d572a1d572d9c245f5eb0ccb70b",
    PREFIX + "PREMISE_LEDGER.tsv": "1babd1a4c5b7691f8c7670d490dd043f5c109504",
    PREFIX + "PREREGISTRATION.md": "1b687ca3344457ed208215a3b85a54d3b5f2f253",
    PREFIX + "SOURCE_SCOPE.tsv": "0a93ab8adb6c0b1a00cfa5d2b036e58e314d35ef",
}


def git_object(kind: str, payload: bytes) -> str:
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    commit_payload = (root / "PREREGISTRATION_COMMIT_OBJECT.txt").read_bytes()
    gate(git_object("commit", commit_payload) == COMMIT, "raw_commit_object_hash")
    commit_text = commit_payload.decode("utf-8")
    gate("tree 1a7fedca384e509831597d19ff16d032526e4731\n" in commit_text,
         "commit_tree_recorded")
    gate("parent 2077ec6bef8dab2102a7b64dc8c5146c5670716c\n" in commit_text,
         "commit_parent_recorded")

    with (root / "PREREGISTRATION_CHANGESET.tsv").open(newline="", encoding="utf-8") as handle:
        changes = list(csv.DictReader(handle, delimiter="\t"))
    gate({row["path"] for row in changes} == set(FILES), "exact_preregistered_file_set")
    gate(all(row["status"] == "A" for row in changes), "all_five_added_at_preregistration")

    with (root / "PREREGISTRATION_TREE.tsv").open(newline="", encoding="utf-8") as handle:
        tree = list(csv.DictReader(handle, delimiter="\t"))
    gate({row["path"]: row["object"] for row in tree} == FILES,
         "tree_blob_registry_exact")
    gate(all(row["mode"] == "100644" and row["type"] == "blob" for row in tree),
         "tree_modes_and_types_exact")

    for path, expected in FILES.items():
        local = root / path.removeprefix(PREFIX)
        gate(git_object("blob", local.read_bytes()) == expected,
             "blob:" + local.name)

    result = {
        "schema": "udt-g327-preregistration-proof-v1",
        "status": "PASS",
        "commit": COMMIT,
        "assertion_count": len(checks),
        "checks": checks,
        "scope_note": "content-and-ancestry-marker proof, not an external trusted timestamp",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

