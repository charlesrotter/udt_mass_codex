#!/usr/bin/env python3
"""Independent fail-closed verifier for the R1C fixed-root preregistration."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable


def run(repo: Path, command: list[str], *, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if completed.returncode:
        stderr = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{stderr}")
    return completed.stdout


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tree(repo: Path, base: str) -> dict[str, tuple[str, str]]:
    raw = bytes(run(repo, ["git", "ls-tree", "-z", base], binary=True))
    result = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_type, oid = metadata.decode("ascii").split()
        if object_type == "blob":
            result[raw_path.decode("utf-8", "surrogateescape")] = (mode, oid)
    return result


def blob(repo: Path, base: str, path: str) -> bytes:
    return bytes(run(repo, ["git", "show", f"{base}:{path}"], binary=True))


def validate(repo: Path, base: str, rows: list[dict[str, str]]) -> None:
    exact = tree(repo, base)
    paths = [row["path"] for row in rows]
    assert len(paths) == len(set(paths)) == len(exact) == 1114
    assert set(paths) == set(exact)
    for row in rows:
        mode, oid = exact[row["path"]]
        payload = blob(repo, base, row["path"])
        assert row["git_mode"] == mode and row["git_blob_oid"] == oid
        assert row["sha256"] == hashlib.sha256(payload).hexdigest()
        assert int(row["size_bytes"]) == len(payload)
        assert row["first_commit_date"] and row["last_commit_date"]
        assert row["first_commit"] and row["last_commit"]


def rejected(check: Callable[[], Any]) -> str:
    try:
        check()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch-proof corruption was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--freeze-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    base = str(run(repo, ["git", "rev-parse", args.base])).strip()
    assert base == "07c67bfbe661705c6b936243fa1ed697f23c1644"
    rows = load(args.inventory)
    validate(repo, base, rows)
    freeze = json.loads(args.freeze_result.read_text(encoding="utf-8"))
    assert freeze["base"] == base
    assert freeze["root_blob_rows"] == freeze["unique_paths"] == len(rows)
    assert freeze["inventory_sha256"] == hashlib.sha256(args.inventory.read_bytes()).hexdigest()
    assert freeze["generated_records_influence_universe"] is False

    report = {
        "result": "PASS",
        "mode": "R1C_PREREGISTRATION_INDEPENDENT_FAIL_CLOSED_VERIFY",
        "base": base,
        "root_blob_rows": len(rows),
        "unique_primary_universe_paths": len({row["path"] for row in rows}),
        "inventory_sha256": freeze["inventory_sha256"],
        "catchproof": {
            "missing_row_rejected": rejected(lambda: validate(repo, base, rows[:-1])),
            "duplicate_row_rejected": rejected(lambda: validate(repo, base, rows + [rows[0]])),
            "bad_oid_rejected": rejected(
                lambda: validate(repo, base, [dict(rows[0], git_blob_oid="0" * 40), *rows[1:]])
            ),
            "bad_sha256_rejected": rejected(
                lambda: validate(repo, base, [dict(rows[0], sha256="0" * 64), *rows[1:]])
            ),
        },
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
