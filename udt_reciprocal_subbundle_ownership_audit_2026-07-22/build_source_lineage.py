#!/usr/bin/env python3
"""Freeze the exact source chain used by the subbundle ownership audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "14b06fdc1434301de1516cd2dbc226ad3fa1a3e1"

SOURCES = [
    (
        "S01", "UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION_PACKET",
        "abstract reciprocal pair; conditional physical slot; static seal",
        "Identifying the reciprocal spatial slot with the `phi`-gradient direction is **CONDITIONAL**",
    ),
    (
        "S02", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "OWNER_LOCKED_FOUNDATION",
        "common scale is calibration rather than directional selector",
        "Common-Scale Neutrality declares the first factor calibrational; UDT Reciprocity governs the",
    ),
    (
        "S03", "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "OWNER_WORKING_PRINCIPLE",
        "global admissibility; no local selector operator",
        "- **No nonlocal insertion:** the global average density may not be written directly into a local",
    ),
    (
        "S04", "udt_phi_metric_ontology_audit_2026-07-22/AUDIT_REPORT.md", "CURRENT_VERIFIED_WITH_CAVEATS_AUDIT",
        "phi meaning partially closed; complete geometric ownership open",
        "Therefore the foundation currently says **what `phi` measures**, but not **which complete geometric",
    ),
    (
        "S05", "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md", "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "multiple complete seal/coframe lifts survive",
        "UDT's reciprocal character has an exact depth-reversing involution, but the current foundation does",
    ),
    (
        "S06", "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md", "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "transition algebra constrains but does not select soldering or cover",
        "Neither structure selects its invariant modulus, physical soldering, cover, caps, angular lift, or",
    ),
    (
        "S07", "udt_reciprocal_plane_projector_audit_2026-07-21/AUDIT_REPORT.md", "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "projector-compatible connection conditional on supplied integrable umbilical split",
        "The law fails for nonintegrable twist and for trace-free cross-shear. Current UDT evidence does not",
    ),
    (
        "S08", "udt_metric_native_two_pair_selector_audit_2026-07-21/AUDIT_REPORT.md", "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "conditional reflection-seal complement; universal two-pair selector absent",
        "The conformal metric, orientation, scalar depth, and ordinary curvature data do **not** select a",
    ),
    (
        "S09", "udt_chart_coframe_invariance_atlas_2026-07-21/AUDIT_REPORT.md", "OBSERVED_BOUNDED_ATLAS",
        "full tensors invariant; supplied 2+2 split remains partition dependent",
        "whether UDT supplies an invariant projector/distribution that makes one split intrinsic",
    ),
    (
        "S10", "udt_joint_invariant_subspace_atlas_2026-07-21/AUDIT_REPORT.md", "OBSERVED_BOUNDED_ATLAS",
        "smaller-family splits do not survive complete curvature orchestra",
        "But none of those unique smaller-family splits survives the complete curvature orchestra.",
    ),
    (
        "S11", "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md", "VERIFIED_WITH_CAVEATS_GLOBAL_ATLAS",
        "global completion families remain unselected",
        "Registered Reciprocity, Common-Scale Neutrality, finite-cell/seal data, bootstrap, and the current",
    ),
    (
        "S12", "udt_local_selector_holonomy_closure_2026-07-22/AUDIT_REPORT.md", "VERIFIED_WITH_CAVEATS_LOCAL_ATLAS",
        "full-curvature/flat dichotomy and missing phi-metric realization relation",
        "The registered analytic atlas deliberately varies ten metric amplitudes and `phi` independently.",
    ),
    (
        "S13", "udt_finite_cell_completion_atlas_2026-07-21/AUDIT_REPORT.md", "BOUNDED_TYPE_SPACE_ATLAS",
        "finite-cell completion space has unbounded retained remainders",
        "This is a type-space atlas, not a finite list of worlds.",
    ),
    (
        "S14", "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md", "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "static seal supplies one scalar wire, not complete boundary data",
        "The canonized static spatial fold gives",
    ),
    (
        "S15", "udt_metric_to_frontier_reference_2026-07-22/REFERENCE_CORRECTION_LAYER.md", "COLD_REVIEW_QUALIFICATION_LAYER",
        "realization relation is prior to action fork",
        "Registered Reciprocity, CSN, finite-cell/seal data, and bootstrap constrain",
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
        text = data.decode("utf-8")
        matches = [index for index, line in enumerate(text.splitlines(), start=1) if anchor in line]
        if len(matches) != 1:
            raise RuntimeError(f"anchor count {len(matches)}: {path}: {anchor}")
        line_number = matches[0]
        anchor_line = text.splitlines()[line_number - 1]
        first_commit, first_date, last_commit, last_date = history(path)
        rows.append(
            {
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
                "anchor_line": str(line_number),
                "anchor_sha256": hashlib.sha256(anchor_line.encode()).hexdigest(),
            }
        )
    fields = list(rows[0])
    with (HERE / "SOURCE_LINEAGE.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"sources={len(rows)}")


if __name__ == "__main__":
    main()
