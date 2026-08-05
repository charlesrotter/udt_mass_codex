#!/usr/bin/env python3
"""Apply the preregistered relational-phi dispositions to every active identity."""

from __future__ import annotations

import csv
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, str]], fields: list[str]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", lineterminator="\n", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def focused_hits(row: dict[str, str]) -> int:
    return sum(
        int(value)
        for key, value in row.items()
        if key.startswith("hits_") and key != "hits_broad_phi_depth"
    )


def rule_matches(rule: dict[str, str], row: dict[str, str], focused: int) -> bool:
    kind = rule["match_kind"]
    value = rule["match_value"]
    path = row["path"]
    if kind == "EXACT_SET":
        return path in value.split(";")
    if kind == "PREFIX_SET":
        return any(path.startswith(prefix) for prefix in value.split(";"))
    if kind == "REGEX":
        return re.search(value, path) is not None
    if kind == "ROW_FLAG":
        key, expected = value.split("=", 1)
        actual = str(focused) if key == "focused_hits" else row[key]
        return actual == expected
    if kind == "ROW_DATE":
        if value.startswith("first_date<"):
            return row["first_date"][:10] < value.split("<", 1)[1]
        raise ValueError(f"unsupported date rule: {value}")
    if kind == "FALLBACK":
        return True
    raise ValueError(f"unknown match kind: {kind}")


def main() -> None:
    active = read_tsv("ACTIVE_REGRADE_UNIVERSE.tsv")
    rules = read_tsv("SEMANTIC_FAMILY_RULES.tsv")
    rules.sort(key=lambda row: (-int(row["priority"]), row["family_id"]))
    allowed = {
        row["disposition"] for row in read_tsv("CLASSIFICATION_SCHEMA.tsv")
    }
    ledger: list[dict[str, str]] = []
    for source in active:
        focused = focused_hits(source)
        matched = [rule for rule in rules if rule_matches(rule, source, focused)]
        if not matched:
            raise AssertionError(f"unmatched active identity: {source['path']}")
        top_priority = int(matched[0]["priority"])
        tied = [rule for rule in matched if int(rule["priority"]) == top_priority]
        if len(tied) != 1:
            raise AssertionError(
                f"ambiguous primary rule for {source['path']}: "
                + ",".join(rule["family_id"] for rule in tied)
            )
        rule = tied[0]
        if rule["disposition"] not in allowed:
            raise AssertionError(f"unknown disposition: {rule['disposition']}")
        flags = [
            key.removeprefix("hits_")
            for key, value in source.items()
            if key.startswith("hits_") and key != "hits_broad_phi_depth" and int(value)
        ]
        ledger.append({
            "path": source["path"],
            "source_sha256": source["sha256"],
            "first_date": source["first_date"],
            "current_control": source["current_control"],
            "current_frontier": source["current_frontier"],
            "frozen_manifest": source["frozen_manifest"],
            "historical_or_pre_july": source["historical_or_pre_july"],
            "focused_hit_count": str(focused),
            "dependency_flags": ";".join(flags) if flags else "NONE",
            "family_id": rule["family_id"],
            "disposition": rule["disposition"],
            "dependency_type": rule["dependency_type"],
            "family_ruling": rule["family_ruling"],
            "reuse_gate": rule["reuse_gate"],
            "manual_review_status": (
                "LINE_LEVEL_OR_FAMILY_SOURCE_REVIEWED"
                if focused or source["current_control"] == "YES"
                else "MECHANICAL_BROAD_ONLY"
            ),
        })
    fields = list(ledger[0])
    write_tsv("ACTIVE_REGRADING_LEDGER.tsv", ledger, fields)
    counts = Counter((row["family_id"], row["disposition"]) for row in ledger)
    count_rows = [
        {"family_id": family, "disposition": disposition, "path_count": str(count)}
        for (family, disposition), count in sorted(counts.items())
    ]
    write_tsv("FAMILY_COUNTS.tsv", count_rows, ["family_id", "disposition", "path_count"])
    dispositions = Counter(row["disposition"] for row in ledger)
    family_identity = sha256_bytes(
        "".join(f"{row['path']}\t{row['family_id']}\t{row['disposition']}\n" for row in ledger).encode()
    )
    summary = {
        "schema": "udt.relational_phi_regrade.ledger.v1",
        "active_count": len(ledger),
        "unique_path_count": len({row["path"] for row in ledger}),
        "focused_path_count": sum(int(row["focused_hit_count"]) > 0 for row in ledger),
        "manual_or_family_reviewed_count": sum(
            row["manual_review_status"] == "LINE_LEVEL_OR_FAMILY_SOURCE_REVIEWED" for row in ledger
        ),
        "disposition_counts": dict(sorted(dispositions.items())),
        "rederivation_required_count": dispositions.get("REDERIVATION_REQUIRED", 0),
        "family_identity_sha256": family_identity,
    }
    (HERE / "REGRADING_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
