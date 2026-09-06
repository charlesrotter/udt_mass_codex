#!/usr/bin/env python3
"""Verify fixed-snapshot coverage, sources, anchors, and dependency metadata."""

from __future__ import annotations

import csv
from collections import Counter

import update_metric_kernel_account as account


def main() -> int:
    expected = account.build_rows()
    if not account.SIDECAR.is_file():
        raise SystemExit("coverage sidecar missing")
    with account.SIDECAR.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != account.FIELDS:
            raise SystemExit("coverage sidecar schema mismatch")
        actual = list(reader)
    if actual != expected:
        raise SystemExit("coverage sidecar is stale; run update_metric_kernel_account.py --write")
    ids = {row["premise_id"] for row in actual}
    for row in actual:
        upstream = set(filter(None, row["upstream_ids"].split(";")))
        if not upstream <= ids:
            raise SystemExit(f"unknown upstream for {row['premise_id']}: {sorted(upstream-ids)}")
        if not row["manuscript_anchor"]:
            raise SystemExit(f"missing manuscript anchor: {row['premise_id']}")
        if row["documentation_status"].startswith("NOT_YET"):
            raise SystemExit(f"documentation placeholder remains: {row['premise_id']}")
    counts = Counter(row["role"] for row in actual)
    expected_counts = {
        "MAIN_ARGUMENT": 65,
        "SUPPORTING_LEMMA": 123,
        "BOUNDARY_RESULT": 76,
        "CONTROL_ONLY": 57,
        "OUTSIDE_SCOPE": 12,
        "SUPERSEDED_HISTORICAL": 2,
    }
    if counts != expected_counts:
        raise SystemExit(f"coverage counts changed: {dict(counts)}")
    manuscript = account.ROOT.joinpath("UDT_METRIC_KERNEL_DEVELOPMENT.md").read_text(encoding="utf-8")
    manuscript_path = account.ROOT / "UDT_METRIC_KERNEL_DEVELOPMENT.md"
    if account.sha256(manuscript_path) != account.REVIEWED_MANUSCRIPT_SHA256:
        raise SystemExit("reviewed manuscript bytes changed; fidelity review required")
    for heading in ("## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7.", "## 8.", "## Appendix A"):
        if heading not in manuscript:
            raise SystemExit(f"manuscript heading missing: {heading}")
    print(f"PASS metric-kernel account: {len(actual)} rows; roles={dict(sorted(counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
