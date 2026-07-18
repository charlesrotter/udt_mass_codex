#!/usr/bin/env python3
"""Freeze the complete tracked-root blob inventory at the R1C fixed base."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


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


def root_blobs(repo: Path, base: str) -> list[dict[str, str]]:
    raw = bytes(run(repo, ["git", "ls-tree", "-z", base], binary=True))
    rows = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_type, oid = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8", "surrogateescape")
        if object_type == "blob":
            rows.append({"path": path, "git_mode": mode, "git_blob_oid": oid})
    return sorted(rows, key=lambda row: row["path"])


def blob_payloads(repo: Path, rows: list[dict[str, str]]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    result: dict[str, bytes] = {}
    for row in rows:
        process.stdin.write(row["git_blob_oid"].encode("ascii") + b"\n")
        process.stdin.flush()
        header = process.stdout.readline().decode("ascii").strip().split()
        assert len(header) == 3 and header[1] == "blob"
        size = int(header[2])
        payload = process.stdout.read(size)
        assert process.stdout.read(1) == b"\n"
        result[row["path"]] = payload
    process.stdin.close()
    process.wait(timeout=30)
    assert process.returncode == 0
    return result


def commit_metadata(repo: Path, base: str, paths: set[str]) -> dict[str, dict[str, str]]:
    output = str(
        run(
            repo,
            [
                "git",
                "log",
                "--date=short",
                "--format=%x1e%H%x09%ad%x09%s",
                "--name-only",
                base,
                "--",
            ],
        )
    )
    metadata: dict[str, dict[str, str]] = {}
    for block in output.split("\x1e"):
        if not block.strip():
            continue
        lines = block.splitlines()
        commit, date, subject = lines[0].split("\t", 2)
        for path in (line for line in lines[1:] if line in paths):
            row = metadata.setdefault(path, {})
            if "last_commit" not in row:
                row.update(
                    {
                        "last_commit": commit,
                        "last_commit_date": date,
                        "last_commit_subject": subject,
                    }
                )
            row.update({"first_commit": commit, "first_commit_date": date})
    assert set(metadata) == paths, f"missing commit metadata: {sorted(paths - set(metadata))[:20]}"
    return metadata


def artifact_type(path: str, mode: str) -> str:
    if mode == "120000":
        return "SYMLINK"
    suffix = PurePosixPath(path).suffix.lower()
    return {
        ".md": "MARKDOWN",
        ".py": "PYTHON",
        ".json": "JSON",
        ".tsv": "TSV",
        ".csv": "CSV",
        ".txt": "TEXT",
        ".log": "LOG",
        ".sh": "SHELL",
        ".toml": "CONFIG",
        ".ini": "CONFIG",
        ".cfg": "CONFIG",
        ".yaml": "CONFIG",
        ".yml": "CONFIG",
        ".npz": "OPAQUE_DATA",
        ".npy": "OPAQUE_DATA",
        ".pt": "OPAQUE_DATA",
        ".pth": "OPAQUE_DATA",
    }.get(suffix, "OTHER")


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    base = str(run(repo, ["git", "rev-parse", args.base])).strip()
    rows = root_blobs(repo, base)
    payloads = blob_payloads(repo, rows)
    metadata = commit_metadata(repo, base, {row["path"] for row in rows})
    final = []
    for row in rows:
        payload = payloads[row["path"]]
        final.append(
            {
                **row,
                "artifact_type": artifact_type(row["path"], row["git_mode"]),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
                **metadata[row["path"]],
            }
        )
    fields = (
        "path",
        "artifact_type",
        "git_mode",
        "git_blob_oid",
        "sha256",
        "size_bytes",
        "first_commit_date",
        "first_commit",
        "last_commit_date",
        "last_commit",
        "last_commit_subject",
    )
    inventory = output / "FROZEN_ROOT_INVENTORY.tsv"
    write_tsv(inventory, final, fields)
    inventory_sha = hashlib.sha256(inventory.read_bytes()).hexdigest()
    path_oid_digest = hashlib.sha256(
        "".join(f"{row['path']}\0{row['git_blob_oid']}\n" for row in final).encode("utf-8")
    ).hexdigest()
    report = {
        "result": "PASS",
        "mode": "R1C_FIXED_BASE_COMPLETE_TRACKED_ROOT_FREEZE",
        "base": base,
        "root_blob_rows": len(final),
        "unique_paths": len({row["path"] for row in final}),
        "inventory_sha256": inventory_sha,
        "path_oid_sha256": path_oid_digest,
        "generated_records_influence_universe": False,
    }
    (output / "PREREGISTERED_ROOT_FREEZE.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
