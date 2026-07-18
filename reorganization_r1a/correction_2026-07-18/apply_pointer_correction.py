#!/usr/bin/env python3
"""Apply the five preregistered R1A pointer corrections exactly once."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("POINTER_CORRECTION_RESULT.tsv")
PREFIX = "archive/pre_2026-07-01/"
CHANGES = (
    ("HANDOFF_ARCHIVE.md", "PROVENANCE_AUDIT_2026-06-30.md"),
    ("FOUNDATIONAL_ASSUMPTIONS_LEDGER.md", "STEP2_timelive_matter_results.md"),
    ("HANDOFF_ARCHIVE.md", "coupled_timelive_VERIFIER.md"),
    ("archive/tier_d_round3_contract.md", "lepton_ladder_test_results.md"),
    ("NEGATIVES_REGISTRY.md", "weld_discriminator_results.md"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    grouped: dict[str, list[str]] = {}
    for source, target in CHANGES:
        grouped.setdefault(source, []).append(target)

    rows: list[dict[str, str]] = []
    replacements: dict[str, bytes] = {}
    for source, targets in grouped.items():
        path = ROOT / source
        before = path.read_bytes()
        text = before.decode("utf-8")
        updated = text
        for target in targets:
            new_target = PREFIX + target
            if updated.count(target) != 1:
                raise SystemExit(
                    f"expected exactly one unqualified occurrence: {source}: {target}"
                )
            if new_target in updated:
                raise SystemExit(f"pointer already qualified: {source}: {new_target}")
            updated = updated.replace(target, new_target, 1)
        after = updated.encode("utf-8")
        replacements[source] = after
        rows.append(
            {
                "source": source,
                "authorized_targets": ";".join(targets),
                "replacement_count": str(len(targets)),
                "before_sha256": sha256(before),
                "after_sha256": sha256(after),
            }
        )

    for source, data in replacements.items():
        (ROOT / source).write_bytes(data)

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "source",
                "authorized_targets",
                "replacement_count",
                "before_sha256",
                "after_sha256",
            ),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"PASS: applied {len(CHANGES)} preregistered pointer corrections")


if __name__ == "__main__":
    main()
