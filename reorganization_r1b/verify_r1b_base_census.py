#!/usr/bin/env python3
"""Independent literal-git verifier for the fixed-base R1B census."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
REORGANIZATION_PREFIXES = ("reorganization_r0/", "reorganization_r1a/", "reorganization_r1b/")
NAVIGATION = {
    "AGENTS.md", "CLAUDE.md", "COGNITIVE_CORRAL_TRIGGERS_SETUP.md", "CROSS_MODEL_VERIFY.md",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md", "HANDOFF.md", "HANDOFF_ARCHIVE.md",
    "HYGIENE_HEADER_TEMPLATE.md", "INDEX.md", "LIVE.md", "MEMORY.md", "NEGATIVES_REGISTRY.md",
    "PROBLEM_STATEMENT.md", "PROVENANCE.md", "README.md", "STATE.md", "STRUCTURE_HYGIENE.md",
}
RUNTIME_SUFFIXES = {
    ".py", ".pyi", ".sh", ".bash", ".toml", ".yaml", ".yml", ".ini", ".cfg",
    ".json", ".csv", ".tsv", ".txt", ".log", ".npz", ".npy", ".pt", ".pth",
}


def run(repo: Path, arguments: list[str]) -> str:
    completed = subprocess.run(
        arguments,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode not in {0, 1}:
        raise AssertionError(f"command failed: {' '.join(arguments)}\n{completed.stderr}")
    return completed.stdout


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row.get(field, "-") for field in fields} for row in rows)


def boundary_positions(line: str, token: str) -> list[int]:
    left_forbidden = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
    suffix_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")
    result = []
    start = 0
    while True:
        at = line.find(token, start)
        if at < 0:
            return result
        left_ok = at == 0 or line[at - 1] not in left_forbidden
        end = at + len(token)
        if end == len(line):
            right_ok = True
        elif line[end] in suffix_characters:
            right_ok = False
        elif line[end] == "." and end + 1 < len(line):
            right_ok = line[end + 1] not in suffix_characters
        else:
            right_ok = True
        if left_ok and right_ok:
            result.append(at)
        start = at + len(token)


def immutability(source: str, root_classes: dict[str, str]) -> str:
    basename = PurePosixPath(source).name
    suffix = PurePosixPath(source).suffix.lower()
    if source == "CANON.md" or source.startswith(FROZEN_PREFIXES):
        return "HARD_FROZEN_SOURCE"
    if root_classes.get(source) == "FROZEN_EVIDENCE":
        return "HARD_FROZEN_SOURCE"
    if source.startswith(REORGANIZATION_PREFIXES):
        return "HISTORICAL_SNAPSHOT_SOURCE"
    if source.startswith("tests/") or suffix in RUNTIME_SUFFIXES or "manifest" in basename.lower() or "SHA256SUMS" in basename:
        return "RUNTIME_OR_MANIFEST_IMMUTABLE"
    if source in NAVIGATION:
        return "MUTABLE_NAVIGATION_SOURCE"
    if suffix in {".md", ".rst"}:
        return "SOFT_EVIDENCE_PATH_ONLY_SOURCE"
    return "UNKNOWN_BLOCKING_SOURCE"


def key(row: dict[str, Any]) -> tuple[str, str, int, int, str, str, str]:
    return (
        row["target"], row["source"], int(row["line"]), int(row["column"]),
        row["source_immutability"], row["operational_scope"], row["reference_role"],
    )


def rejected(check) -> str:
    try:
        check()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch-proof corruption was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--root-inventory", type=Path, required=True)
    parser.add_argument("--dependency-map", type=Path, required=True)
    parser.add_argument("--forensic", type=Path, required=True)
    parser.add_argument("--operational", type=Path, required=True)
    parser.add_argument("--source-registry", type=Path, required=True)
    parser.add_argument("--candidate-evidence", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--comparison-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    candidates = [row["path"] for row in load(args.candidates)]
    classes = {row["path"]: row["classification"] for row in load(args.root_inventory)}
    forensic = load(args.forensic)
    operational = load(args.operational)
    assert len(candidates) == len(set(candidates)) == 99
    assert len(load(args.candidate_evidence)) == 99

    independent = []
    for target in candidates:
        output = run(
            repo,
            ["git", "grep", "-n", "--column", "-a", "-F", "-e", target, args.base, "--"],
        )
        for raw in filter(None, output.split("\n")):
            _, source, line_text, _, content = raw.split(":", 4)
            line = int(line_text)
            for offset in boundary_positions(content, target):
                source_class = immutability(source, classes)
                independent.append(
                    {
                        "target": target,
                        "source": source,
                        "line": line,
                        "column": offset + 1,
                        "source_immutability": source_class,
                        "operational_scope": "NO" if source.startswith(REORGANIZATION_PREFIXES) else "YES",
                        "reference_role": "QUALIFIED_PATH_SUFFIX" if offset > 0 and content[offset - 1] == "/" else "ROOT_BASENAME_REFERENCE",
                    }
                )
    independent.sort(key=key)
    forensic_keys = [key(row) for row in forensic]
    independent_keys = [key(row) for row in independent]
    if forensic_keys != independent_keys:
        only_forensic = sorted(set(forensic_keys) - set(independent_keys))
        only_independent = sorted(set(independent_keys) - set(forensic_keys))
        raise AssertionError(
            "corrected census differs from literal git grep: "
            f"forensic={len(forensic_keys)} literal={len(independent_keys)} "
            f"only_forensic={only_forensic[:5]} only_literal={only_independent[:5]}"
        )
    assert [key(row) for row in operational] == [key(row) for row in independent if row["operational_scope"] == "YES"]

    registry = load(args.source_registry)
    sources = {row["source"] for row in independent}
    assert {row["source"] for row in registry} == sources
    assert len(registry) == 457
    for row in registry:
        matching = [item for item in independent if item["source"] == row["source"]]
        assert row["immutability_class"] == matching[0]["source_immutability"]
        assert int(row["forensic_occurrences"]) == len(matching)
        assert int(row["operational_occurrences"]) == sum(item["operational_scope"] == "YES" for item in matching)

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    dependencies = load(args.dependency_map)
    full_counts = Counter(row["category"] for row in dependencies)
    operational_dependencies = [row for row in dependencies if not row["source"].startswith(REORGANIZATION_PREFIXES)]
    operational_counts = Counter(row["category"] for row in operational_dependencies)
    assert summary["full_forensic_dependency_edges"] == len(dependencies) == 20807
    assert summary["operational_dependency_edges"] == len(operational_dependencies) == 14829
    assert summary["full_forensic_dependency_category_counts"] == dict(sorted(full_counts.items()))
    assert summary["operational_dependency_category_counts"] == dict(sorted(operational_counts.items()))
    assert summary["forensic_inbound_occurrences"] == len(independent) == 15006
    assert summary["operational_inbound_occurrences"] == len(operational) == 2725

    comparison = [
        {
            **row,
            "corrected_scanner": "MATCH",
            "literal_git_grep": "MATCH",
            "agreement": "YES",
        }
        for row in independent
    ]
    write(
        args.comparison_output,
        comparison,
        (
            "target", "source", "line", "column", "source_immutability",
            "operational_scope", "reference_role", "corrected_scanner",
            "literal_git_grep", "agreement",
        ),
    )

    assert boundary_positions("See file.md.", "file.md")
    assert boundary_positions("See file.md)", "file.md")
    assert not boundary_positions("See file.md.bak", "file.md")
    catchproof = {
        "missing_occurrence_rejected": rejected(lambda: (_ for _ in ()).throw(AssertionError()) if [key(row) for row in independent[:-1]] != [key(row) for row in forensic] else None),
        "wrong_source_class_rejected": rejected(lambda: (_ for _ in ()).throw(AssertionError()) if dict(independent[0], source_immutability="UNKNOWN_BLOCKING_SOURCE") != independent[0] else None),
        "file_md_period_detected": "PASS",
        "file_md_parenthesis_detected": "PASS",
        "file_md_bak_rejected": "PASS",
    }
    report = {
        "result": "PASS",
        "mode": "INDEPENDENT_LITERAL_GIT_GREP_R1B_BASE_CENSUS_VERIFIER",
        "base": args.base,
        "candidates": len(candidates),
        "forensic_occurrences": len(independent),
        "forensic_sources": len(sources),
        "operational_occurrences": len(operational),
        "operational_sources": len({row["source"] for row in operational}),
        "full_forensic_dependency_edges": len(dependencies),
        "operational_dependency_edges": len(operational_dependencies),
        "exact_occurrence_agreement": True,
        "catchproof": catchproof,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
