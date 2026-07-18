#!/usr/bin/env python3
"""Build separate R1B post-move forensic and operational dependency summaries."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


REORGANIZATION_PREFIXES = ("reorganization_r0/", "reorganization_r1a/", "reorganization_r1b/")


def load_tsv(path: Path) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        assert reader.fieldnames
        return rows, tuple(reader.fieldnames)


def write_tsv(path: Path, rows: list[dict[str, str]], fields: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def counts(rows: list[dict[str, str]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(row[key] for row in rows).items()))


def operational(source: str) -> bool:
    return not source.startswith(REORGANIZATION_PREFIXES)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--forensic-map", type=Path, required=True)
    parser.add_argument("--forensic-summary", type=Path, required=True)
    parser.add_argument("--base-census-summary", type=Path, required=True)
    parser.add_argument("--migration-result", type=Path, required=True)
    parser.add_argument("--pointer-census", type=Path, required=True)
    parser.add_argument("--operational-output-dir", type=Path, required=True)
    parser.add_argument("--comparison-output", type=Path, required=True)
    args = parser.parse_args()

    forensic_rows, fields = load_tsv(args.forensic_map)
    forensic_summary = json.loads(args.forensic_summary.read_text(encoding="utf-8"))
    base_summary = json.loads(args.base_census_summary.read_text(encoding="utf-8"))
    migration_rows, _ = load_tsv(args.migration_result)
    pointer_rows, _ = load_tsv(args.pointer_census)
    assert len(migration_rows) == 2
    assert forensic_summary["dependency_edge_count"] == len(forensic_rows)
    assert counts(forensic_rows, "category") == forensic_summary["dependency_category_counts"]
    assert all(row["content_identical"] == "YES" for row in migration_rows)
    assert not [row for row in pointer_rows if row["role"] == "STALE_NON_FROZEN_OPERATIONAL_POINTER"]

    operational_rows = [row for row in forensic_rows if operational(row["source"])]
    excluded_rows = [row for row in forensic_rows if not operational(row["source"])]
    output = args.operational_output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    operational_map = output / "DEPENDENCY_MAP.tsv"
    write_tsv(operational_map, operational_rows, fields)

    operational_summary: dict[str, Any] = {
        "result": "PASS",
        "mode": "R1B_POSTMOVE_OPERATIONAL_DEPENDENCY_CENSUS",
        "base_commit": forensic_summary["base_commit"],
        "dependency_edge_count": len(operational_rows),
        "dependency_category_counts": counts(operational_rows, "category"),
        "dependency_status_counts": counts(operational_rows, "status"),
        "source_count": len({row["source"] for row in operational_rows}),
        "excluded_historical_edge_count": len(excluded_rows),
        "excluded_historical_source_count": len({row["source"] for row in excluded_rows}),
        "exclusion_prefixes": list(REORGANIZATION_PREFIXES),
        "operational_map_sha256": sha256(operational_map),
        "generated_audit_records_influence_selection": False,
        "selection_was_frozen_before_adjudication_and_mutation": True,
    }
    (output / "SCAN_SUMMARY.json").write_text(
        json.dumps(operational_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    forensic_categories = counts(forensic_rows, "category")
    comparison = {
        "result": "PASS",
        "mode": "R1B_DUAL_DEPENDENCY_CENSUS_COMPARISON",
        "base_selection_commit": base_summary["base"],
        "postmove_commit": forensic_summary["base_commit"],
        "base_full_forensic_edges": base_summary["full_forensic_dependency_edges"],
        "base_operational_edges": base_summary["operational_dependency_edges"],
        "postmove_full_forensic_edges": len(forensic_rows),
        "postmove_operational_edges": len(operational_rows),
        "postmove_historical_reorganization_edges_excluded": len(excluded_rows),
        "postmove_full_forensic_category_counts": forensic_categories,
        "postmove_operational_category_counts": operational_summary["dependency_category_counts"],
        "forensic_map_sha256": sha256(args.forensic_map),
        "operational_map_sha256": sha256(operational_map),
        "full_and_operational_counts_kept_separate": True,
        "generated_audit_records_influence_selection": False,
        "moved_files": len(migration_rows),
        "stale_non_frozen_operational_pointers": 0,
    }
    args.comparison_output.parent.mkdir(parents=True, exist_ok=True)
    args.comparison_output.write_text(
        json.dumps(comparison, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(comparison, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
