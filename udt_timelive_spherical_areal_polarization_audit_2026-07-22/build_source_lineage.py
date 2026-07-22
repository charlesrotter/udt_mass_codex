#!/usr/bin/env python3
"""Freeze the post-firewall source chain for the time-live areal audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "066d1ee05c3ad144d28b096b4a4728cca06941fa"

SOURCES = [
    (
        "S01", "udt_reciprocity_regime_angular_center_audit_2026-07-22/AUDIT_REPORT.md",
        "IMMEDIATELY_PRIOR_VERIFIED_WITH_CAVEATS_AUDIT",
        "static angular-center condition and frame-regime classification",
        "The new metric-led result comes from the complete angular sector.",
    ),
    (
        "S02", "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md",
        "CURRENT_RECIPROCAL_MEANING_AUDIT",
        "founded local pair and tensorial macro observer reciprocity",
        "The owner correction is significant and the post-firewall source chain confirms it.",
    ),
    (
        "S03", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "FOUNDING_DERIVATION_RECORD",
        "static reciprocal metric and declared readout premises",
        "the postulate derives the reciprocal UDT metric family:",
    ),
    (
        "S04", "UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION_PACKET",
        "reciprocal block and explicit transverse/time-live open scope",
        "the reciprocal clock/parallel-direction block is",
    ),
    (
        "S05", "udt_time_live_characteristic_flux_audit_2026-07-21/AUDIT_REPORT.md",
        "VERIFIED_BOUNDED_TIME_LIVE_AUDIT",
        "time-live causal classes and action/boundary nonselection",
        "Time dependence adds real structure, but it does **not** close the boundary-selector seam.",
    ),
    (
        "S06", "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_METRIC_WIDE_AUDIT",
        "warped angular and mixed curvature derives per representative",
        "Cartan geometry faithfully describes a chosen metric's local curvature and transport; it does not choose which complete metric the universe realizes.",
    ),
    (
        "S07", "invariant_reciprocal_causal_flow_2026-07-18/DERIVATION_REPORT.md",
        "VERIFIED_CONDITIONAL_STATIC_OPTICAL_AUDIT",
        "static normalized null readout and WR-L extension",
        "its invariant content is **optical travel geometry**, not a scalar position-dependent local speed of light.",
    ),
    (
        "S08", "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md",
        "VERIFIED_CONFORMAL_CAUSAL_AUDIT",
        "positive common scaling preserves cones but not physical intervals",
        "positive common-scale change does not alter who can causally reach whom.",
    ),
    (
        "S09", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "OWNER_LOCKED_FOUNDATION",
        "pre-scale local common calibration and representative distinction",
        "Common-Scale Neutrality declares the first factor calibrational; UDT Reciprocity governs the",
    ),
    (
        "S10", "udt_phi_metric_ontology_audit_2026-07-22/AUDIT_REPORT.md",
        "CURRENT_VERIFIED_WITH_CAVEATS_ONTOLOGY_AUDIT",
        "phi logarithmic imbalance and complete-geometry ownership gap",
        "The post-firewall foundation determines that `phi` is a **dimensionless logarithmic reciprocal",
    ),
    (
        "S11", "udt_chart_coframe_invariance_atlas_2026-07-21/AUDIT_REPORT.md",
        "OBSERVED_BOUNDED_ATLAS",
        "tensor invariance versus supplied coframe partitions",
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
    output = []
    for source_id, path, authority, use, anchor in SOURCES:
        data = run("git", "show", f"{BASE}:{path}", binary=True)
        lines = data.decode("utf-8").splitlines()
        matches = [number for number, line in enumerate(lines, 1) if anchor in line]
        if len(matches) != 1:
            raise RuntimeError(f"anchor count {len(matches)}: {path}: {anchor}")
        number = matches[0]
        first_commit, first_date, last_commit, last_date = history(path)
        output.append({
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
        writer = csv.DictWriter(handle, list(output[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(f"sources={len(output)}")


if __name__ == "__main__":
    main()
