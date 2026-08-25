#!/usr/bin/env python3
"""Mechanical certification for the G255 evidence package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def load_tsv(name: str):
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    if args.no_write and args.output:
        raise SystemExit("--no-write and --output are mutually exclusive")

    assertions = 0
    slots = load_tsv("SLOT_CENSUS.tsv")
    extracts = load_tsv("PRIMARY_CLAIM_EXTRACTS.tsv")
    census = load_tsv("EQUATION_OWNERSHIP_CENSUS.tsv")
    candidates = load_tsv("CANDIDATE_EQUATION_LEDGER.tsv")
    contract = load_tsv("CLASSIFICATION_CONTRACT.tsv")
    manifest = load_tsv("SOURCE_MANIFEST.tsv")
    expected_slots = [f"G{i}" for i in range(165, 255)]

    assert [row["slot"] for row in slots] == expected_slots
    assert [row["slot"] for row in extracts] == expected_slots
    assert [row["slot"] for row in census] == expected_slots
    assert len(slots) == len(extracts) == len(census) == 90
    assertions += 4
    assert {row["class_id"] for row in contract} == {f"C{i:02d}" for i in range(1, 15)}
    assert len(candidates) == 21
    assert len(manifest) == 321
    assertions += 3

    exact_derivations = 0
    registry_present = 0
    controller_matches = 0
    for row in slots:
        report = ROOT / row["primary_report"]
        assert report.is_file()
        assertions += 1
        if row["exact_derivation"]:
            assert (ROOT / row["exact_derivation"]).is_file()
            exact_derivations += 1
            assertions += 1
        if row["registry_row"] == "PRESENT":
            registry_present += 1
        if row["historical_report_is_current_controller"] == "true":
            controller_matches += 1
    assert exact_derivations == 83
    assert registry_present == 87
    assert controller_matches == 86
    assertions += 3

    for row in manifest:
        path = ROOT / row["path"]
        assert path.is_file()
        assert digest(path) == row["sha256"]
        assertions += 2

    counts = Counter(row["primary_class"] for row in census)
    expected_counts = {
        "C01": 1,
        "C02": 1,
        "C03": 7,
        "C04": 5,
        "C05": 16,
        "C06": 10,
        "C07": 4,
        "C08": 14,
        "C09": 10,
        "C10": 10,
        "C11": 12,
    }
    assert dict(sorted(counts.items())) == expected_counts
    assert not any(row["primary_class"] in {"C12", "C13", "C14"} for row in census)
    assert not any(row["classification"] in {"C12", "C13", "C14"} for row in candidates)
    assertions += 3

    production = json.loads((PKG / "EQUATION_OWNERSHIP_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    assert production["landing"] == independent["landing"] == "NO_LOST_CLOSURE_IN_G165_G254"
    assert production["slot_count"] == independent["slot_count"] == 90
    assert production["owned_local_metric_condition_count"] == independent["owned_local_metric_condition_count"] == 0
    assert production["owned_global_relation_law_count"] == independent["owned_global_relation_law_count"] == 0
    assert production["candidate_unresolved_count"] == independent["unresolved_candidate_count"] == 0
    assert independent["counterhistory_curvature_cases"] == 85
    assert independent["hostile_mutations_caught"] == 4
    assertions += 7

    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    reconciliation = (PKG / "SCOPE_RECONCILIATION.md").read_text(encoding="utf-8")
    assert "NO_LOST_CLOSURE_IN_G165_G254" in report
    assert "C12 | owned nonidentity local metric condition | 0" in report
    assert "C13 | owned nonidentity global relation law | 0" in report
    assert "not a declaration that\n  every Lorentz metric" in report
    assert "It is not a derived list\nof physical UDT histories" in reconciliation
    assertions += 5

    result = {
        "status": "PASS",
        "assertion_count": assertions,
        "slot_count": len(slots),
        "source_count": len(manifest),
        "exact_derivation_count": exact_derivations,
        "registry_row_count_in_range": registry_present,
        "current_controller_match_count": controller_matches,
        "candidate_count": len(candidates),
        "class_counts": expected_counts,
        "landing": "NO_LOST_CLOSURE_IN_G165_G254",
        "external_review": "PENDING",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
