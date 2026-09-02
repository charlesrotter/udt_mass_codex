#!/usr/bin/env python3
"""Dependency-free verifier for the sealed G328 preregistration ancestry proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


EXPECTED_COMMIT = "96298482a035a6ffa9103d3949c6aa4fee987c75"
EXPECTED_PATHS = {
    "udt_g328_g324_transverse_first_fourier_census_2026-09-02/COMPLETENESS_MAP.md":
        "b6164faa78f089c4c15249ee2edf32885eef1702",
    "udt_g328_g324_transverse_first_fourier_census_2026-09-02/MAP.md":
        "a2df840b4b1973a469980c96d6ac5d1973c2fa22",
    "udt_g328_g324_transverse_first_fourier_census_2026-09-02/PREMISE_LEDGER.tsv":
        "2955d4077e5f7655b20428aac409b6700530c771",
    "udt_g328_g324_transverse_first_fourier_census_2026-09-02/PREREGISTRATION.md":
        "bf24a59c5560533571d4b71d04e8ee761001bb68",
    "udt_g328_g324_transverse_first_fourier_census_2026-09-02/SOURCE_SCOPE.tsv":
        "7b5a7df779eade0b8248812b1b3fefef53b6daed",
}


def git_object_id(kind: str, payload: bytes) -> str:
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parent
    commit_payload = (root / "PREREGISTRATION_COMMIT_OBJECT.txt").read_bytes()
    commit = git_object_id("commit", commit_payload)
    assert commit == EXPECTED_COMMIT, "preregistration commit object mismatch"

    changes = {}
    for line in (root / "PREREGISTRATION_CHANGESET.tsv").read_text(
        encoding="utf-8"
    ).splitlines()[1:]:
        status, path = line.split("\t")
        changes[path] = status
    assert changes == {path: "A" for path in EXPECTED_PATHS}, "changeset mismatch"

    tree = {}
    for line in (root / "PREREGISTRATION_TREE.tsv").read_text(
        encoding="utf-8"
    ).splitlines()[1:]:
        mode, kind, object_id, path = line.split("\t")
        assert mode == "100644" and kind == "blob", "tree type mismatch"
        tree[path] = object_id
    assert tree == EXPECTED_PATHS, "tree entries mismatch"

    result = {
        "schema": "udt-g328-preregistration-proof-v1",
        "status": "PASS",
        "commit": commit,
        "path_count": len(tree),
        "scope": "repository-carried content and ancestry marker; not trusted timestamp",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
