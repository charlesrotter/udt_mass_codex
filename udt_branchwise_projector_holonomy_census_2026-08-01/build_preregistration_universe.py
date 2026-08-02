#!/usr/bin/env python3
"""Freeze the complete base tree and package/report metadata without reading scientific content."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
BASE = "156b8a57d2e4ce65a588e5f7c2d82d0bd1f88334"
TEXT_SUFFIXES = {".md", ".tsv", ".csv", ".json", ".py", ".txt", ".yaml", ".yml", ".toml"}


def run(args: list[str]) -> str:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True).stdout


def tree_rows() -> list[dict[str, str]]:
    raw = subprocess.run(
        ["git", "ls-tree", "-r", "-z", BASE], cwd=ROOT, capture_output=True, check=True
    ).stdout
    parsed = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        head, path_raw = item.split(b"\t", 1)
        mode, kind, blob = head.decode("ascii").split()
        path = path_raw.decode("utf-8", "surrogateescape")
        parsed.append({"mode": mode, "kind": kind, "blob": blob, "path": path})
    return parsed


def blob_sha256(rows: list[dict[str, str]]) -> dict[str, str]:
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    assert proc.stdin is not None and proc.stdout is not None
    result = {}
    for row in rows:
        proc.stdin.write((row["blob"] + "\n").encode("ascii"))
        proc.stdin.flush()
        header = proc.stdout.readline().decode("ascii").strip().split()
        assert len(header) == 3 and header[1] == "blob"
        size = int(header[2])
        data = proc.stdout.read(size)
        assert proc.stdout.read(1) == b"\n"
        result[row["blob"]] = hashlib.sha256(data).hexdigest()
    proc.stdin.close()
    assert proc.wait(timeout=30) == 0
    return result


def commit_metadata(path: str) -> tuple[str, str, str, str]:
    added = run(["git", "log", "--follow", "--diff-filter=A", "--format=%H%x09%aI", "--", path]).splitlines()
    latest = run(["git", "log", "-1", "--format=%H%x09%aI", BASE, "--", path]).strip()
    first = added[-1].split("\t", 1) if added else ("UNKNOWN", "UNKNOWN")
    last = latest.split("\t", 1) if latest else ("UNKNOWN", "UNKNOWN")
    return first[0], first[1], last[0], last[1]


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows = tree_rows()
    sha = blob_sha256(rows)
    base_rows = []
    group_counts: Counter[str] = Counter()
    for row in rows:
        path = row["path"]
        top = path.split("/", 1)[0] if "/" in path else "ROOT"
        group_counts[top] += 1
        suffix = Path(path).suffix.lower()
        base_rows.append(
            {
                "path": path,
                "mode": row["mode"],
                "git_blob": row["blob"],
                "sha256": sha[row["blob"]],
                "top_group": top,
                "suffix": suffix or "-",
                "text_discovery_eligible": "YES" if suffix in TEXT_SUFFIXES else "NO",
            }
        )
    write_tsv(
        "BASE_TREE_MANIFEST.tsv",
        ["path", "mode", "git_blob", "sha256", "top_group", "suffix", "text_discovery_eligible"],
        base_rows,
    )

    reports = [row for row in rows if row["path"].endswith("/AUDIT_REPORT.md")]
    report_rows = []
    for row in reports:
        first_hash, first_date, last_hash, last_date = commit_metadata(row["path"])
        report_rows.append(
            {
                "path": row["path"],
                "top_group": row["path"].split("/", 1)[0],
                "git_blob": row["blob"],
                "sha256": sha[row["blob"]],
                "first_commit": first_hash,
                "first_commit_date": first_date,
                "last_commit": last_hash,
                "last_commit_date": last_date,
            }
        )
    write_tsv(
        "AUDIT_REPORT_UNIVERSE.tsv",
        ["path", "top_group", "git_blob", "sha256", "first_commit", "first_commit_date", "last_commit", "last_commit_date"],
        report_rows,
    )

    group_rows = [
        {
            "top_group": group,
            "tracked_paths": count,
            "has_audit_report": "YES" if any(row["top_group"] == group for row in report_rows) else "NO",
        }
        for group, count in sorted(group_counts.items())
    ]
    write_tsv("PACKAGE_GROUP_UNIVERSE.tsv", ["top_group", "tracked_paths", "has_audit_report"], group_rows)

    manifest_bytes = (PKG / "BASE_TREE_MANIFEST.tsv").read_bytes()
    report_bytes = (PKG / "AUDIT_REPORT_UNIVERSE.tsv").read_bytes()
    group_bytes = (PKG / "PACKAGE_GROUP_UNIVERSE.tsv").read_bytes()
    result = {
        "base": BASE,
        "base_tree_paths": len(base_rows),
        "text_discovery_eligible": sum(row["text_discovery_eligible"] == "YES" for row in base_rows),
        "audit_reports": len(report_rows),
        "top_groups": len(group_rows),
        "base_tree_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "audit_report_universe_sha256": hashlib.sha256(report_bytes).hexdigest(),
        "package_group_universe_sha256": hashlib.sha256(group_bytes).hexdigest(),
        "status": "PASS",
    }
    (PKG / "PREREGISTRATION_UNIVERSE_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
