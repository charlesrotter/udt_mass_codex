#!/usr/bin/env python3
"""Dependency-free, no-write integrity verifier for the G218 whiteboard."""

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


source_rows = rows(PACKAGE / "SOURCE_MANIFEST.tsv")
source_matches = []
for row in source_rows:
    actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
    source_matches.append(actual == row["sha256"])

report = (PACKAGE / "WHITEBOARD_REPORT.md").read_text(encoding="utf-8")
next_audit = (PACKAGE / "NEXT_AUDIT_PREREGISTRATION.md").read_text(encoding="utf-8")
debate = rows(PACKAGE / "DEBATE_LEDGER.tsv")
status = rows(PACKAGE / "STATUS_LEDGER.tsv")

required_report_tokens = (
    "QUERY_INDEXED_REGULAR_CORRESPONDENCE_UNIFIES_EVENT_INCIDENCE_DEPTH_AND_POSITIVE_CLOCK_JET",
    "d\\tau_B}{d\\tau_A}=e^{-\\delta_Q}",
    "PRIMARY_STATIC_SCALAR_KERNEL_CLOSES_MODULO_CLOCK_ORIGIN",
    "NULL_INCIDENCE_IS_AN_EXACT_METRIC_NATIVE_CAUSAL_QUERY_NOT_A_UNIVERSAL_POSITIONAL_OWNER",
    "after emission, reception, branch, and clock-readout ownership",
    "radar-echo map, not generally the identity",
    "No dissent remained",
)
required_next_tokens = (
    "PROPOSED_NOT_RUN",
    "f_a(tau)=r tau+a tau^2",
    "moving-Minkowski",
    "SCALAR_CHAIN_FACTORS_THROUGH_ONE_CLOCK_ARROW__PROTOCOL_REMAINS_QUERY_TYPED",
    "treating future causal return as mathematical inversion",
)

checks = {
    "source_count": len(source_rows) == 9,
    "source_hashes": bool(source_matches) and all(source_matches),
    "debate_rows": len(debate) == 10,
    "status_rows": len(status) == 7,
    "report_tokens": all(token in report for token in required_report_tokens),
    "next_audit_tokens": all(token in next_audit for token in required_next_tokens),
}

print(json.dumps({
    "audit": "G218",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "source_count": len(source_rows),
    "debate_rows": len(debate),
    "status_rows": len(status),
    "landing": "QUERY_INDEXED_CLOCK_CORRESPONDENCE_PONDER_CONSENSUS",
}, sort_keys=True))
