#!/usr/bin/env python3
"""Freeze the current post-firewall source chain for the two-frame limit audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "73b33e2c9f11e897976d571810a8e98dc3a2e644"

SOURCES = [
    (
        "S01", "udt_clock_anchor_scale_threading_audit_2026-07-22/AUDIT_REPORT.md",
        "IMMEDIATE_PARENT_VERIFIED_WITH_CAVEATS",
        "c_E, F, X, local null cancellation, endpoint classes, and scale-map status",
        "Keeping the observed finite `c_E` explicit in the complete positive-`X` spherical areal form,",
    ),
    (
        "S02", "udt_phi_metric_ontology_audit_2026-07-22/AUDIT_REPORT.md",
        "CURRENT_PHI_ONTOLOGY_AUDIT",
        "signed dimensionless phi and open complete-geometric ownership",
        "The post-firewall foundation determines that `phi` is a **dimensionless logarithmic reciprocal",
    ),
    (
        "S03", "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md",
        "CURRENT_RECIPROCAL_MEANING_AUDIT",
        "reciprocal metric block, c_E, and tensorial observer reciprocity",
        "Reciprocal-c: c_E and 1/c_E are coequal directions of one clock-length conversion.",
    ),
    (
        "S04", "UDT_NATIVE_ACTION_COLD_PACKET.md",
        "CURRENT_FOUNDATION_PACKET",
        "founding reciprocal block and its exact premise stamps",
        "the reciprocal clock/parallel-direction block is",
    ),
    (
        "S05", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "FOUNDING_DERIVATION_RECORD",
        "clock/ruler redistribution and finite c_E anchor",
        "Thus positional dilation redistributes clock and radial-ruler calibration without changing the",
    ),
    (
        "S06", "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
        "OWNER_LOCKED_MEANING_LEDGER",
        "finite c_E, signed phi, nonnegative distance, X_max, density, and scale layers",
        "Finite Einsteinian c measured at terrestrial and solar scales; ordinary clock-length baseline",
    ),
    (
        "S07", "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md",
        "VERIFIED_CONFORMAL_CAUSAL_AUDIT",
        "co-presence does not by itself imply mutual access",
        "One whole solution can have all events in its domain without making all events mutually accessible.",
    ),
    (
        "S08", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "OWNER_LOCKED_FOUNDATION",
        "pre-scale common calibration role",
        "Common-Scale Neutrality declares the first factor calibrational; UDT Reciprocity governs the",
    ),
    (
        "S09", "udt_time_live_characteristic_flux_audit_2026-07-21/AUDIT_REPORT.md",
        "TIME_LIVE_CHARACTERISTIC_AUDIT",
        "conditional metric cone and angular/shift/time-live incompleteness",
        "Time dependence adds real structure, but it does **not** close the boundary-selector seam.",
    ),
    (
        "S10", "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
        "EXTERNALLY_VERIFIED_WITH_CAVEATS_GLOBAL_ATLAS",
        "retained global completions and nonselecting bootstrap",
        "Current bootstrap is on-shell admissibility. It has no off-shell functional that ranks the atlas",
    ),
    (
        "S11", "udt_clock_ruler_soldering_selector_audit_2026-07-20/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_SOLDERING_AUDIT",
        "seal-local frame result and open complete angular/normal/time-on lift",
        "Within the conditional mixed Lorentzian readout and a supplied reciprocal base, the spatial seal",
    ),
    (
        "S12", "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md",
        "VERIFIED_WITH_CAVEATS_SCALE_CENSUS",
        "absence of a physical absolute regime map",
        "With only `M_tot`, `X_max`, measured `c_E`, measured `G_obs`, and dimensionless metric/state data,",
    ),
    (
        "S13", "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "CURRENT_EVIDENCE_LINKED_SYNTHESIS",
        "current dependency and open-join synthesis",
        "Measured ordinary-regime `c_E` and `G_obs` are observational anchors.",
    ),
    (
        "S14", "udt_metric_to_frontier_reference_2026-07-22/REFERENCE_CORRECTION_LAYER.md",
        "CURRENT_COLD_REVIEW_QUALIFICATION",
        "admissibility versus operational realization",
        "Registered Reciprocity, CSN, finite-cell/seal data, and bootstrap constrain",
    ),
    (
        "S15", "udt_reciprocity_regime_angular_center_audit_2026-07-22/AUDIT_REPORT.md",
        "PRIOR_SPHERICAL_CONTROL",
        "regular areal-center theorem to be retained but separated from regime scale",
        "The new metric-led result comes from the complete angular sector.",
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
