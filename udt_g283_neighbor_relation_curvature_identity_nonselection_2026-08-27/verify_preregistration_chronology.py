#!/usr/bin/env python3
"""Dependency-free, repository-independent G283 preregistration chronology proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
PREREG_COMMIT = "18100a3a4a6721be4544cebe2e5e12cc84178167"
OUTCOME_COMMIT = "98403a7485c9e72ffe30fa5571abb603a3b74668"
PREREG_BLOB = "96d91d1143a84fa3bf6785bd17e239ed4ff44b73"


def git_object_id(kind: str, payload: bytes) -> str:
    header = f"{kind} {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload, usedforsecurity=False).hexdigest()


def header_value(payload: bytes, key: str) -> str:
    prefix = key.encode("ascii") + b" "
    for line in payload.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].decode("ascii")
    raise AssertionError(f"missing {key} header")


def commit_epoch(payload: bytes) -> int:
    committer = header_value(payload, "committer")
    return int(committer.rsplit(" ", 2)[-2])


def verify_chronology() -> dict[str, object]:
    prereg_commit_payload = (PACKAGE / "PREREGISTRATION_COMMIT_OBJECT.txt").read_bytes()
    outcome_commit_payload = (PACKAGE / "OUTCOME_COMMIT_OBJECT.txt").read_bytes()
    preregistration_payload = (PACKAGE / "PREREGISTRATION.md").read_bytes()
    checks = {
        "preregistration_commit_object_exact": (
            git_object_id("commit", prereg_commit_payload) == PREREG_COMMIT
        ),
        "outcome_commit_object_exact": (
            git_object_id("commit", outcome_commit_payload) == OUTCOME_COMMIT
        ),
        "outcome_direct_parent_is_preregistration": (
            header_value(outcome_commit_payload, "parent") == PREREG_COMMIT
        ),
        "preregistration_blob_exact": (
            git_object_id("blob", preregistration_payload) == PREREG_BLOB
        ),
        "preregistration_precedes_outcome": (
            commit_epoch(prereg_commit_payload) < commit_epoch(outcome_commit_payload)
        ),
        "subjects_distinguish_preregistration_and_outcome": (
            b"Preregister G283 neighboring-curvature identity test" in prereg_commit_payload
            and b"Derive G283 curvature identity nonselection" in outcome_commit_payload
        ),
    }
    result = {
        "audit": "G283_PREREGISTRATION_CHRONOLOGY",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "preregistration_commit": PREREG_COMMIT,
        "outcome_commit": OUTCOME_COMMIT,
        "preregistration_blob": PREREG_BLOB,
        "checks": checks,
    }
    if result["status"] != "PASS":
        raise AssertionError({name: value for name, value in checks.items() if not value})
    return result


def main() -> None:
    print(json.dumps(verify_chronology(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
