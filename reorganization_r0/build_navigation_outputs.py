#!/usr/bin/env python3
"""Derive Phase-R0 root-retention and dependency-summary navigation files."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from pathlib import Path


PERMANENT_ROOT = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CANON.md",
    "CLAUDE.md",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md",
    "HANDOFF.md",
    "INDEX.md",
    "LIVE.md",
    "MEMORY.md",
    "NEGATIVES_REGISTRY.md",
    "PROBLEM_STATEMENT.md",
    "PROVENANCE.md",
    "README.md",
    "pytest.ini",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "root_requirement", "reason", "release_gate", "source_basis"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--dependencies", type=Path, required=True)
    parser.add_argument("--retention-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    args = parser.parse_args()

    inventory = read_tsv(args.inventory)
    dependencies = read_tsv(args.dependencies)
    by_path = {row["path"]: row for row in inventory}
    startup_targets: set[str] = set()
    import_targets: set[str] = set()
    for edge in dependencies:
        targets = edge["resolved_target"].split("|")
        for target in targets:
            if "/" in target or target not in by_path:
                continue
            if edge["category"] == "STARTUP" and edge["status"].startswith("RESOLVED"):
                startup_targets.add(target)
            if edge["category"] in {"PYTHON_IMPORT", "TEST"} and edge["status"].startswith(
                "RESOLVED"
            ):
                import_targets.add(target)

    rows: list[dict[str, str]] = []
    all_candidates = set(PERMANENT_ROOT) | startup_targets | import_targets
    all_candidates |= {
        row["path"] for row in inventory if row["classification"] == "CONTROL"
    }
    for path in sorted(all_candidates):
        if path == "README.md":
            rows.append(
                {
                    "path": path,
                    "root_requirement": "PERMANENT_ROOT",
                    "reason": "concise public navigation entry added by R0",
                    "release_gate": "none; remains root",
                    "source_basis": "R0 user requirement",
                }
            )
            continue
        row = by_path[path]
        if path in PERMANENT_ROOT:
            requirement = "PERMANENT_ROOT"
            reason = "startup, canon, provenance, test configuration, or repository control contract"
            release_gate = "none; remains root"
        elif row["classification"] == "CONTROL":
            requirement = "ROOT_CONTROL_UNTIL_GOVERNANCE_MIGRATION"
            reason = "current control-plane file referenced by governance or tooling"
            release_gate = "explicit governance-path migration plus startup/test verification"
        elif path in startup_targets:
            requirement = "ROOT_PINNED_UNTIL_POINTER_MIGRATION"
            reason = "statically resolved startup/frontier reference"
            release_gate = "rewrite every startup/reference edge and re-run dependency verifier"
        else:
            requirement = "ROOT_PINNED_UNTIL_IMPORT_MIGRATION"
            reason = "resolved Python/test import currently depends on root module resolution"
            release_gate = "package/import migration with existing tests at baseline or better"
        bases: list[str] = []
        if path in startup_targets:
            bases.append("STARTUP_REFERENCE")
        if path in import_targets:
            bases.append("PYTHON_OR_TEST_IMPORT")
        if row["classification"] == "CONTROL":
            bases.append("CONTROL")
        rows.append(
            {
                "path": path,
                "root_requirement": requirement,
                "reason": reason,
                "release_gate": release_gate,
                "source_basis": ";".join(bases),
            }
        )
    write_tsv(args.retention_output, rows)

    categories = Counter(row["category"] for row in dependencies)
    statuses = Counter(row["status"] for row in dependencies)
    matrix = Counter((row["category"], row["status"]) for row in dependencies)
    lines = [
        "# Phase R0 dependency summary",
        "",
        "This summarizes the complete static edge table in `DEPENDENCY_MAP.tsv` at base `bfa0b9a`.",
        "Dynamic and unresolved paths are deliberately retained; this is not a runtime trace.",
        "",
        "## Coverage by category",
        "",
        "| Category | Edges |",
        "|---|---:|",
    ]
    for category, count in sorted(categories.items()):
        lines.append(f"| `{category}` | {count} |")
    lines.extend(
        [
            "",
            "## Resolution matrix",
            "",
            "| Category | Status | Edges |",
            "|---|---|---:|",
        ]
    )
    for (category, status), count in sorted(matrix.items()):
        lines.append(f"| `{category}` | `{status}` | {count} |")
    unresolved_statuses = {
        "AMBIGUOUS_BASENAME",
        "DYNAMIC",
        "DYNAMIC_OR_GLOB",
        "MISSING_OR_GENERATED",
        "UNRESOLVED",
    }
    lines.extend(
        [
            "",
            "## Unresolved/dynamic audit queue",
            "",
            f"Static edges total: {len(dependencies)}. Dynamic or unresolved edges: "
            f"{sum(count for status, count in statuses.items() if status in unresolved_statuses)}.",
            "The following are representative rows only; the TSV retains every row.",
            "",
            "| Source | Line | Category | Raw target | Status |",
            "|---|---:|---|---|---|",
        ]
    )
    examples: Counter[str] = Counter()
    for row in dependencies:
        if row["status"] not in unresolved_statuses:
            continue
        if examples[row["category"]] >= 8:
            continue
        examples[row["category"]] += 1
        raw = row["raw_target"].replace("|", "\\|")[:100]
        lines.append(
            f"| `{row['source']}` | {row['line'] or ''} | `{row['category']}` | `{raw}` | "
            f"`{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- `EXTERNAL_OR_STDLIB` is a static import classification, not proof that a package is installed.",
            "- `MISSING_OR_GENERATED` often denotes an output path; it must be adjudicated before a move.",
            "- `RESOLVED_BY_BASENAME` needs path normalization before relocation because the source did not name the full path.",
            "- A dynamic expression is surfaced verbatim and never guessed.",
            "- Markdown-link coverage does not convert plain prose references; exact root-name prose references are separate `TEXT_REFERENCE` edges.",
        ]
    )
    args.summary_output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"root retention rows: {len(rows)}")
    print(f"dependency summary edges: {len(dependencies)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
