#!/usr/bin/env python3
"""Freeze the exact post-firewall source chain used by this audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "f5f30018dda111f4bf131a5675f8480ca605a268"

SOURCES = [
    (
        "S01", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "FOUNDING_DERIVATION_RECORD",
        "two-way c identity, dual Reciprocity, and declared static spherical metric",
        "the postulate derives the reciprocal UDT metric family:",
    ),
    (
        "S02", "UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION_PACKET",
        "authoritative premise separation and reciprocal block limits",
        "the reciprocal clock/parallel-direction block is",
    ),
    (
        "S03", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "OWNER_LOCKED_FOUNDATION",
        "common scale is calibration; reciprocal determinant-one factor survives",
        "Common-Scale Neutrality declares the first factor calibrational; UDT Reciprocity governs the",
    ),
    (
        "S04", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
        "FINAL_ABC_ADJUDICATION",
        "reciprocal kinematic statuses and explicit metric-readout conditions",
        "S08\tReciprocal Lorentzian metric block\tCONDITIONAL",
    ),
    (
        "S05", "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
        "OWNER_MEANING_LEDGER",
        "finite observed c, signed local phi, observer comparison, and metric-is-theory",
        "O13\tmetric_status\tThe metric is the theory; derived geometry precedes imported dynamics",
    ),
    (
        "S06", "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
        "PREMISE_RESET_AUDIT",
        "reciprocal-c survives while observer comparison remains to be derived",
        "The Reciprocal-c anchor survives:",
    ),
    (
        "S07", "udt_phi_metric_ontology_audit_2026-07-22/AUDIT_REPORT.md",
        "CURRENT_VERIFIED_WITH_CAVEATS_AUDIT",
        "phi is logarithmic reciprocal imbalance; geometric ownership had remained open",
        "The post-firewall foundation determines that `phi` is a **dimensionless logarithmic reciprocal",
    ),
    (
        "S08", "udt_reciprocal_subbundle_ownership_audit_2026-07-22/AUDIT_REPORT.md",
        "IMMEDIATELY_PRIOR_VERIFIED_WITH_CAVEATS_AUDIT",
        "universal fixed rank-two selector obstruction to be semantically regraded",
        "The current registered UDT premises do **not** derive a universal distinguished reciprocal",
    ),
    (
        "S09", "udt_chart_coframe_invariance_atlas_2026-07-21/AUDIT_REPORT.md",
        "OBSERVED_BOUNDED_ATLAS",
        "tensor invariance versus partition-dependent supplied splits",
        "whether UDT supplies an invariant projector/distribution that makes one split intrinsic",
    ),
    (
        "S10", "udt_independent_amplitude_metric_atlas_2026-07-21/PREREGISTRATION.md",
        "CONFIGURATION_ATLAS_PREREGISTRATION",
        "ten metric amplitudes and phi intentionally varied independently",
        "constructive atlas. This package must independently vary ten metric amplitudes and the separate",
    ),
    (
        "S11", "udt_structural_ensemble_metric_atlas_2026-07-21/PREREGISTRATION.md",
        "CONFIGURATION_ATLAS_PREREGISTRATION",
        "ensemble census deliberately broader than a derived UDT metric family",
        "It maps the complete metric/coframe and the independent signed `phi`",
    ),
    (
        "S12", "udt_metric_to_frontier_reference_2026-07-22/REFERENCE_CORRECTION_LAYER.md",
        "COLD_REVIEW_QUALIFICATION_LAYER",
        "realization and action remain separate questions",
        "The mathematically prior question is whether realization",
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
        source_text = data.decode("utf-8")
        matches = [number for number, line in enumerate(source_text.splitlines(), 1) if anchor in line]
        if len(matches) != 1:
            raise RuntimeError(f"anchor count {len(matches)}: {path}: {anchor}")
        number = matches[0]
        line = source_text.splitlines()[number - 1]
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
            "anchor_sha256": hashlib.sha256(line.encode()).hexdigest(),
        })
    fields = list(output[0])
    with (HERE / "SOURCE_LINEAGE.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(f"sources={len(output)}")


if __name__ == "__main__":
    main()
