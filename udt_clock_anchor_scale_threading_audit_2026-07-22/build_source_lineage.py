#!/usr/bin/env python3
"""Freeze the post-firewall source chain for the clock-anchor/threading audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "e4075a05e6f64714e732f375641bd73447d3559c"

SOURCES = [
    (
        "S01", "udt_timelive_spherical_areal_polarization_audit_2026-07-22/AUDIT_REPORT.md",
        "IMMEDIATELY_PRIOR_VERIFIED_WITH_CAVEATS_AUDIT",
        "complete positive-X areal form and surviving F",
        "the angular sector defines the coordinate scalar and oriented areal dual",
    ),
    (
        "S02", "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md",
        "CURRENT_RECIPROCAL_MEANING_AUDIT",
        "c_E reciprocal pair and tensorial macro observer reciprocity",
        "Reciprocal-c: c_E and 1/c_E are coequal directions of one clock-length conversion.",
    ),
    (
        "S03", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "FOUNDING_DERIVATION_RECORD",
        "explicit c_E metric and WR-L wall interpretation",
        "the postulate derives the reciprocal UDT metric family:",
    ),
    (
        "S04", "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
        "OWNER_LOCKED_MEANING_LEDGER",
        "finite c_E X_max density G and scale-layer meanings",
        "Finite Einsteinian c measured at terrestrial and solar scales; ordinary clock-length baseline",
    ),
    (
        "S05", "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md",
        "VERIFIED_CONFORMAL_CAUSAL_AUDIT",
        "whole-solution semantics and metric causal accessibility",
        "One whole solution can have all events in its domain without making all events mutually accessible.",
    ),
    (
        "S06", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "OWNER_LOCKED_FOUNDATION",
        "pre-scale calibration role",
        "Common-Scale Neutrality declares the first factor calibrational; UDT Reciprocity governs the",
    ),
    (
        "S07", "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_SCALE_CENSUS",
        "dimensional rank and absence of absolute ruler",
        "With only `M_tot`, `X_max`, measured `c_E`, measured `G_obs`, and dimensionless metric/state data,",
    ),
    (
        "S08", "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_REPRESENTATIVE_AUDIT",
        "endpoint-flat counterfamily and bootstrap nonselection",
        "No existing noncircular finite-cell, bootstrap, or `X_max`-reciprocity rule selects the physical representative",
    ),
    (
        "S09", "clock_curvature_selector_audit_2026-07-19/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_CLOCK_CURVATURE_AUDIT",
        "conditional lapse equation and its non-forcing",
        "The WR–L clock–curvature identity is real and mathematically strong, but it is not presently a native UDT field equation.",
    ),
    (
        "S10", "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
        "EXTERNALLY_VERIFIED_WITH_CAVEATS_GLOBAL_ATLAS",
        "bootstrap remains on-shell admissibility",
        "Current bootstrap is on-shell admissibility. It has no off-shell functional that ranks the atlas",
    ),
    (
        "S11", "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_MATTER_DIMENSIONAL_AUDIT",
        "hidden matter ruler and c_E/G calibration",
        "previous global rank result: `c_E` and `G_obs` calibrate mass per length, while one absolute ruler",
    ),
    (
        "S12", "udt_reciprocity_regime_angular_center_audit_2026-07-22/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_STATIC_CENTER_AUDIT",
        "regular spherical center and angular divergence",
        "The new metric-led result comes from the complete angular sector.",
    ),
    (
        "S13", "UDT_NATIVE_ACTION_COLD_PACKET.md",
        "CURRENT_FOUNDATION_PACKET",
        "founding reciprocal block and open time-live scope",
        "the reciprocal clock/parallel-direction block is",
    ),
    (
        "S14", "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
        "CURRENT_SELECTOR_CLASSIFICATION",
        "bootstrap status and what it does not imply",
        "Bootstrap closure | `WORKING`; selector mechanism `OPEN`",
    ),
    (
        "S15", "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "CURRENT_EVIDENCE_LINKED_SYNTHESIS",
        "observational anchor and realization seam",
        "Measured ordinary-regime `c_E` and `G_obs` are observational anchors.",
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
