#!/usr/bin/env python3
"""Freeze the preregistered CSN source universe at the exact base commit."""

from __future__ import annotations

import csv
import hashlib
import pathlib
import re
import subprocess

BASE = "c171b052ad321df7d71832cfa35403f07108d61e"
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(__file__).resolve().parent

PATTERN = (
    r"CSN|Common[- ]Scale|common scale|scale[- ]neutral|scale[- ]free|"
    r"pre[- ]scale|conformal representative|physical representative"
)

MANDATORY = {
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md",
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_NATIVE_ACTION_WORKSTATION_SYNC_AUDIT_2026-07-17.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md",
    "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md",
    "reciprocal_c_clock_channel_correction_2026-07-19/AUDIT_REPORT.md",
    "reciprocal_clock_optical_scale_selector_2026-07-19/DERIVATION_REPORT.md",
    "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
    "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
    "udt_premise_reset_audit_2026-07-19/POST_PREREG_C_G_SCALE_CLARIFICATION.md",
    "udt_premise_reset_audit_2026-07-19/SEMANTIC_CONFLICT_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "udt_clock_anchor_scale_threading_audit_2026-07-22/AUDIT_REPORT.md",
    "udt_clock_anchor_scale_threading_audit_2026-07-22/CLOCK_ANCHOR_LEDGER.tsv",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_realization_zoomout_2026-07-23/AUDIT_REPORT.md",
    "udt_csn_dphi_transport_selector_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_bootstrap_substrate_micro_closure_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
    "udt_two_observer_separation_selector_audit_2026-07-24/AUDIT_REPORT.md",
    "udt_involutive_exchange_branch_availability_audit_2026-07-24/AUDIT_REPORT.md",
}

LOAD_BEARING = set(MANDATORY)


def run(*args: str) -> bytes:
    return subprocess.check_output(args, cwd=ROOT)


def git_blob(path: str) -> str:
    return run("git", "rev-parse", f"{BASE}:{path}").decode().strip()


def git_bytes(path: str) -> bytes:
    return run("git", "show", f"{BASE}:{path}")


def classify(path: str) -> str:
    if path in LOAD_BEARING:
        return "LOAD_BEARING"
    if path.startswith(("archive/", "reorganization_r")):
        return "HISTORICAL_OR_FIXED_RECORD"
    if path in {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "AGENTS.md"}:
        return "NAVIGATION_OR_CONTROL"
    if re.search(r"/(AUDIT_REPORT|DERIVATION_REPORT|STATUS_LEDGER)\.(md|tsv)$", path):
        return "DOWNSTREAM_RESULT"
    if path.endswith((".py", ".json", ".npz")):
        return "CODE_OR_MACHINE_EVIDENCE"
    return "SUPPORTING_TEXT"


def main() -> None:
    grep = subprocess.run(
        [
            "git",
            "grep",
            "-I",
            "-l",
            "-E",
            PATTERN,
            BASE,
            "--",
            "*.md",
            "*.tsv",
            "*.txt",
            "*.json",
            "*.py",
        ],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode()
    paths = {line.split(":", 1)[1] for line in grep.splitlines() if line.strip()}
    paths.update(MANDATORY)

    tracked = set(run("git", "ls-tree", "-r", "--name-only", BASE).decode().splitlines())
    missing = sorted(paths - tracked)
    if missing:
        raise SystemExit(f"mandatory paths missing at base: {missing}")

    rows = []
    manifest = []
    regex = re.compile(PATTERN, re.IGNORECASE)
    for path in sorted(paths):
        data = git_bytes(path)
        text = data.decode("utf-8", errors="replace")
        blob = git_blob(path)
        sha = hashlib.sha256(data).hexdigest()
        count = len(regex.findall(text))
        role = classify(path)
        rows.append(
            {
                "path": path,
                "blob": blob,
                "sha256": sha,
                "bytes": len(data),
                "query_hits": count,
                "role": role,
                "mandatory": "YES" if path in MANDATORY else "NO",
            }
        )
        manifest.append(
            {
                "path": path,
                "blob": blob,
                "sha256": sha,
                "bytes": len(data),
            }
        )

    with (OUT / "SOURCE_CENSUS.tsv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=rows[0].keys(), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=manifest[0].keys(), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(manifest)

    print(f"base={BASE}")
    print(f"source_count={len(rows)}")
    print(f"mandatory_count={sum(r['mandatory'] == 'YES' for r in rows)}")
    print(f"load_bearing_count={sum(r['role'] == 'LOAD_BEARING' for r in rows)}")
    print(f"total_query_hits={sum(int(r['query_hits']) for r in rows)}")


if __name__ == "__main__":
    main()
