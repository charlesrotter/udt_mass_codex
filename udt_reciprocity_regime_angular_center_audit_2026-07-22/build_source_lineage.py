#!/usr/bin/env python3
"""Freeze the exact source chain for the reciprocity-regime audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "11ff6f8589a5c5d674b3dca9e65ae1c0dd8d7ac3"

SOURCES = [
    (
        "S01", "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md",
        "IMMEDIATELY_PRIOR_VERIFIED_WITH_CAVEATS_AUDIT",
        "founded reciprocal block, macro observer covariance, and general-extension boundary",
        "The owner correction is significant and the post-firewall source chain confirms it.",
    ),
    (
        "S02", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "FOUNDING_DERIVATION_RECORD",
        "static spherical metric and explicit readout assumptions",
        "the postulate derives the reciprocal UDT metric family:",
    ),
    (
        "S03", "UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION_PACKET",
        "reciprocal block and conditional radial/gradient realization",
        "the reciprocal clock/parallel-direction block is",
    ),
    (
        "S04", "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
        "OWNER_MEANING_LEDGER",
        "metric-is-theory rule and scale/observer distinctions",
        "O13\tmetric_status\tThe metric is the theory; derived geometry precedes imported dynamics",
    ),
    (
        "S05", "invariant_reciprocal_causal_flow_2026-07-18/DERIVATION_REPORT.md",
        "VERIFIED_CONDITIONAL_STATIC_OPTICAL_AUDIT",
        "finite-phi local null speed and WR-L horizon extension",
        "its invariant content is **optical travel geometry**, not a scalar position-dependent local speed of light.",
    ),
    (
        "S06", "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_METRIC_WIDE_AUDIT",
        "complete angular, shear, twist, and mixed curvature sectors",
        "Cartan geometry faithfully describes a chosen metric's local curvature and transport; it does not choose which complete metric the universe realizes.",
    ),
    (
        "S07", "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_BOUNDARY_AUDIT",
        "WR-L wall and center invariant status",
        "The WR-L wall is nevertheless **not derived to be the hard end of spacetime**.",
    ),
    (
        "S08", "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md",
        "VERIFIED_CONFORMAL_CAUSAL_AUDIT",
        "positive common scaling preserves causal cones",
        "positive common-scale change does not alter who can causally reach whom.",
    ),
    (
        "S09", "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
        "PREMISE_RESET_AUDIT",
        "finite c_E baseline and unresolved observable clock relation",
        "The Reciprocal-c anchor survives:",
    ),
    (
        "S10", "udt_chart_coframe_invariance_atlas_2026-07-21/AUDIT_REPORT.md",
        "OBSERVED_BOUNDED_ATLAS",
        "tensor invariance versus component/coframe partitions",
        "whether UDT supplies an invariant projector/distribution that makes one split intrinsic",
    ),
]


def run(*args: str, binary: bool = False):
    return subprocess.check_output(args, cwd=ROOT, text=not binary)


def history(path: str) -> tuple[str, str, str, str]:
    records = run("git", "log", "--follow", "--format=%H%x09%aI", "--", path).strip().splitlines()
    if not records:
        raise RuntimeError(f"missing history: {path}")
    last_commit, last_date = records[0].split("\t", 1)
    first_commit, first_date = records[-1].split("\t", 1)
    return first_commit, first_date, last_commit, last_date


def main() -> None:
    rows = []
    for source_id, path, authority, use, anchor in SOURCES:
        data = run("git", "show", f"{BASE}:{path}", binary=True)
        lines = data.decode("utf-8").splitlines()
        matches = [number for number, line in enumerate(lines, 1) if anchor in line]
        if len(matches) != 1:
            raise RuntimeError(f"anchor count {len(matches)}: {path}: {anchor}")
        number = matches[0]
        first_commit, first_date, last_commit, last_date = history(path)
        rows.append({
            "source_id": source_id,
            "path": path,
            "git_blob": run("git", "rev-parse", f"{BASE}:{path}").strip(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": str(len(data)),
            "first_commit": first_commit,
            "first_commit_date": first_date,
            "last_commit": last_commit,
            "last_commit_date": last_date,
            "firewall": "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE",
            "authority": authority,
            "use": use,
            "anchor_line": str(number),
            "anchor_sha256": hashlib.sha256(lines[number - 1].encode()).hexdigest(),
        })
    with (HERE / "SOURCE_LINEAGE.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"sources={len(rows)}")


if __name__ == "__main__":
    main()
