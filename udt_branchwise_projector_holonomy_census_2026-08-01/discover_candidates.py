#!/usr/bin/env python3
"""Run the preregistered content discovery against frozen base blobs."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
BASE = "156b8a57d2e4ce65a588e5f7c2d82d0bd1f88334"
PATTERNS = {
    "D03": re.compile(r"projector|spectral projector|eigenline|eigenbundle|invariant line|rank[- ]one", re.I),
    "D04": re.compile(r"holonomy|centralizer|parallel subbundle|reduced bundle|preserved line", re.I),
    "D05": re.compile(r"complete metric|complete branch|metric branch|metric family|coframe family|complete cell", re.I),
    "D06": re.compile(r"Killing line|Killing plane|d\s*phi|null direction|celestial|toric|involution|fixed set", re.I),
}


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], output: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)


def read_blobs(entries: list[dict[str, str]]):
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    assert proc.stdin is not None and proc.stdout is not None
    for row in entries:
        proc.stdin.write((row["git_blob"] + "\n").encode("ascii"))
        proc.stdin.flush()
        header = proc.stdout.readline().decode("ascii").strip().split()
        assert len(header) == 3 and header[1] == "blob"
        data = proc.stdout.read(int(header[2]))
        assert proc.stdout.read(1) == b"\n"
        yield row, data
    proc.stdin.close()
    assert proc.wait(timeout=30) == 0


def first_match(text: str, pattern: re.Pattern[str]) -> tuple[int, str]:
    for line_number, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            clean = " ".join(line.replace("\t", " ").split())
            return line_number, clean[:240]
    return 0, ""


def main() -> int:
    base = rows("BASE_TREE_MANIFEST.tsv")
    reports = rows("AUDIT_REPORT_UNIVERSE.tsv")
    report_by_group = {row["top_group"]: row for row in reports}
    eligible = [row for row in base if row["text_discovery_eligible"] == "YES"]
    hits = []
    group_files: dict[str, set[str]] = defaultdict(set)
    group_rules: dict[str, set[str]] = defaultdict(set)
    group_matches: dict[str, int] = defaultdict(int)
    unreadable = []
    for row, data in read_blobs(eligible):
        if b"\0" in data:
            unreadable.append(row["path"])
            continue
        text = data.decode("utf-8", "replace")
        matched_rules = []
        total = 0
        first_line = 0
        first_excerpt = ""
        for rule, pattern in PATTERNS.items():
            count = len(pattern.findall(text))
            if count:
                matched_rules.append(rule)
                total += count
                line_number, excerpt = first_match(text, pattern)
                if first_line == 0 or line_number < first_line:
                    first_line, first_excerpt = line_number, excerpt
        if not matched_rules:
            continue
        group = row["top_group"]
        group_files[group].add(row["path"])
        group_rules[group].update(matched_rules)
        group_matches[group] += total
        hits.append(
            {
                "path": row["path"],
                "top_group": group,
                "git_blob": row["git_blob"],
                "sha256": row["sha256"],
                "rule_ids": ";".join(matched_rules),
                "match_count": total,
                "first_match_line": first_line,
                "first_match_excerpt": first_excerpt,
            }
        )
    write_tsv(
        "DISCOVERY_HITS.tsv",
        ["path", "top_group", "git_blob", "sha256", "rule_ids", "match_count", "first_match_line", "first_match_excerpt"],
        hits,
    )

    group_meta = {row["top_group"]: row for row in rows("PACKAGE_GROUP_UNIVERSE.tsv")}
    groups = []
    for group in sorted(group_files):
        report = report_by_group.get(group, {})
        groups.append(
            {
                "top_group": group,
                "tracked_paths": group_meta[group]["tracked_paths"],
                "hit_files": len(group_files[group]),
                "match_count": group_matches[group],
                "rule_ids": ";".join(sorted(group_rules[group])),
                "audit_report": report.get("path", "-"),
                "audit_report_sha256": report.get("sha256", "-"),
                "first_commit": report.get("first_commit", "UNKNOWN"),
                "first_commit_date": report.get("first_commit_date", "UNKNOWN"),
                "last_commit": report.get("last_commit", "UNKNOWN"),
                "last_commit_date": report.get("last_commit_date", "UNKNOWN"),
                "required_disposition": "PENDING_CONTENT_ADJUDICATION",
            }
        )
    write_tsv(
        "DISCOVERY_GROUPS.tsv",
        ["top_group", "tracked_paths", "hit_files", "match_count", "rule_ids", "audit_report", "audit_report_sha256", "first_commit", "first_commit_date", "last_commit", "last_commit_date", "required_disposition"],
        groups,
    )

    report_screen = []
    hit_group_names = set(group_files)
    for report in reports:
        report_screen.append(
            {
                **report,
                "content_discovery_hit": "YES" if report["top_group"] in hit_group_names else "NO",
                "required_disposition": "PENDING_CONTENT_ADJUDICATION",
            }
        )
    write_tsv(
        "AUDIT_REPORT_SCREEN.tsv",
        ["path", "top_group", "git_blob", "sha256", "first_commit", "first_commit_date", "last_commit", "last_commit_date", "content_discovery_hit", "required_disposition"],
        report_screen,
    )

    result = {
        "base": BASE,
        "text_paths_scanned": len(eligible),
        "binary_or_null_text_paths_skipped": len(unreadable),
        "hit_files": len(hits),
        "hit_groups": len(groups),
        "audit_reports_screened": len(report_screen),
        "audit_report_groups_with_hits": sum(row["content_discovery_hit"] == "YES" for row in report_screen),
        "rule_file_counts": {
            rule: sum(rule in row["rule_ids"].split(";") for row in hits) for rule in sorted(PATTERNS)
        },
        "discovery_hits_sha256": hashlib.sha256((PKG / "DISCOVERY_HITS.tsv").read_bytes()).hexdigest(),
        "discovery_groups_sha256": hashlib.sha256((PKG / "DISCOVERY_GROUPS.tsv").read_bytes()).hexdigest(),
        "audit_report_screen_sha256": hashlib.sha256((PKG / "AUDIT_REPORT_SCREEN.tsv").read_bytes()).hexdigest(),
        "status": "PASS",
    }
    (PKG / "DISCOVERY_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
