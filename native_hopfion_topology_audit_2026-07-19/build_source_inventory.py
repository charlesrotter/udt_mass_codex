#!/usr/bin/env python3
"""Build the deterministic source inventory for the preregistered topology audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import pathlib
import subprocess


SOURCES = [
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "current_frontier", "CURRENT_AUTHORITY"),
    ("UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md", "exact_C0", "FROZEN_FOUNDATION"),
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "exact_C1", "FROZEN_FOUNDATION"),
    ("UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "selector_status", "CURRENT_EVIDENCE"),
    ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "action_carrier_status", "FROZEN_EVIDENCE"),
    ("UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md", "owner_carrier_status", "CURRENT_AUTHORITY"),
    ("matter_carrier_provenance_audit_results.md", "carrier_provenance", "CURRENT_EVIDENCE"),
    ("archive/native_action_chat_2026-07-14_15/UDT_MUTUAL_DILATION_RESISTANCE_DERIVATION_RESULTS.md", "prior_metric_carrier_routes", "POST_JULY_ARCHIVED_EVIDENCE"),
    ("reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md", "metric_direction_selector", "CURRENT_EVIDENCE"),
    ("native_hopfion_route_MAP.md", "historical_hopf_route_map", "HISTORICAL_STATUS_SUPERSEDED_PROSPECTIVELY"),
    ("node_H1_hopfion_compactification_results.md", "local_ball_topology", "CONDITIONAL_EVIDENCE"),
    ("H3_hopfion_solve_preregistration.md", "historical_solve_contract", "FROZEN_PREREGISTRATION"),
    ("node_H3_hopfion_solve_results.md", "historical_3d_hopfion_result", "CONDITIONAL_EVIDENCE"),
    ("hopfion_arc_scripts_2026-07-05/fs_hopfion.py", "original_3d_hopf_solver", "CURRENT_CODE_PROVENANCE"),
    ("noNull_energy.py", "corrected_3d_continuum_discretization", "CURRENT_CODE"),
    ("noNull_resolve.py", "corrected_3d_field_and_charge_solver", "CURRENT_CODE"),
    ("stability_branch_follow_256_DECISION.md", "particle_arc_decision_record", "CURRENT_EVIDENCE"),
    ("noNull_behavioral_F_results.md", "finite_slice_behavior", "CURRENT_EVIDENCE"),
    ("noNull_schur_inertia_ALL.json", "static_inertia_result", "CURRENT_EVIDENCE"),
    ("tests/test_solver_integrity.py", "s2_vs_s3_import_guard", "CURRENT_TEST_WITH_HISTORICAL_NATIVE_WORDING"),
]


def run_git(root: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def commit_edge(root: pathlib.Path, path: str, reverse: bool) -> tuple[str, str]:
    args = ["log", "--follow", "--format=%H%x09%aI"]
    if reverse:
        args.append("--reverse")
    args.extend(["--", path])
    lines = run_git(root, *args).splitlines()
    if not lines:
        raise RuntimeError(f"no history for {path}")
    commit, date = lines[0].split("\t", 1)
    return commit, date


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    root = package.parent
    output = pathlib.Path(args.output)
    if not output.is_absolute():
        output = root / output

    rows = []
    for rel, role, provenance in SOURCES:
        path = root / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        tracked = run_git(root, "ls-files", "--error-unmatch", "--", rel)
        if tracked != rel:
            raise RuntimeError(f"unexpected tracked path resolution: {rel} -> {tracked}")
        first_commit, first_date = commit_edge(root, rel, reverse=True)
        last_commit, last_date = commit_edge(root, rel, reverse=False)
        rows.append({
            "current_path": rel,
            "git_blob": run_git(root, "hash-object", "--", rel),
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
            "first_commit": first_commit,
            "first_date": first_date,
            "last_commit": last_commit,
            "last_date": last_date,
            "audit_role": role,
            "provenance_status": provenance,
        })

    output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"SOURCE_INVENTORY rows={len(rows)} output={output.relative_to(root)}")


if __name__ == "__main__":
    main()
