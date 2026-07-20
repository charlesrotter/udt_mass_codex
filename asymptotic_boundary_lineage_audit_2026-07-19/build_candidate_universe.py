#!/usr/bin/env python3
"""Freeze the base-tree boundary-token census with Git provenance metadata."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "85a0363b2bef9a1cfb0149dc1aaf20bcd44e1bd8"
TOKENS = (
    "A=1-r/X",
    "WR-L",
    "X_max",
    "finite proper",
    "infinite optical",
    "mass dilation",
    "phi=0",
    "fold",
)
SUFFIXES = {".md", ".py", ".json", ".txt", ".tsv"}

LOAD_BEARING = {
    "CANON.md",
    "SIMPLE_METRIC_MACRO.md",
    "simple_metric_FE_rederive.py",
    "simple_metric_L_P_selection_derive.py",
    "simple_metric_L_P_selection_derive_out.json",
    "simple_metric_L_P_selection_derive_results.md",
    "simple_metric_L_principle_closure_attack_results.md",
    "simple_metric_L_wall_regularity_closure_out.json",
    "simple_metric_L_wall_regularity_closure_results.md",
    "simple_metric_WR_L_external_triple_blind_audit_results.md",
    "research/macro/verify_wrl_canon.py",
    "simple_metric_L_native_optical_derive.py",
    "simple_metric_L_native_optical_derive_out.json",
    "simple_metric_L_native_optical_derive_results.md",
    "simple_metric_HL_unification.py",
    "simple_metric_HL_unification_out.json",
    "simple_metric_HL_unification_results.md",
    "simple_metric_timelive_AP_exact_derive_results.md",
    "simple_metric_timelive_AP_intermediate_out.json",
    "simple_metric_timelive_AP_intermediate_results.md",
    "simple_metric_timelive_AP_out.json",
    "simple_metric_timelive_AP_results.md",
    "simple_metric_angular_timelive_L.py",
    "simple_metric_angular_timelive_L_out.json",
    "simple_metric_angular_timelive_L_results.md",
    "simple_metric_mass_xmax_cascade.md",
    "simple_metric_xmax_POSTULATE.md",
    "simple_metric_Pell_mass_lock_derive.md",
    "simple_metric_J1_build_results.md",
    "simple_metric_J1_honesty_skeleton_results.md",
    "simple_metric_sphere_ceiling.py",
    "simple_metric_sphere_ceiling_build.py",
    "simple_metric_sphere_ceiling_build_out.json",
    "simple_metric_sphere_ceiling_build_results.md",
    "simple_metric_sphere_ceiling_select_results.md",
    "simple_metric_S3_native_dust_ceiling.py",
    "simple_metric_S3_native_dust_ceiling_out.json",
    "simple_metric_S3_native_dust_ceiling_results.md",
    "derive_universe_fold_d1.py",
    "universe_cell_fold_jc_sigma_results.md",
    "universe_cell_T2_identities_results.md",
    "universe_cell_T3_closure_results.md",
    "universe_cell_vacuum_impossibility_results.md",
    "node05_seal_parity_regrade_results.md",
    "F4_seal_boundary_MAP.md",
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "native_dilation_weight_derivation_results.md",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "archive/B1_mass_dilation_cost_results.md",
    "archive/native_action_chat_2026-07-14_15/UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/verify_udt_finite_cell_boundary.py",
    "archive/native_action_chat_2026-07-14_15/verify_udt_finite_cell_boundary_out.txt",
    "archive/native_action_chat_2026-07-14_15/UDT_WRL_SCAFFOLD_NATIVE_ACTION_SEPARATION_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_scaffold_separation.py",
    "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_scaffold_separation_out.txt",
    "archive/native_action_chat_2026-07-14_15/UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_solution_space_closure.py",
    "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_solution_space_closure_out.txt",
    "archive/native_action_chat_2026-07-14_15/UDT_WRL_OFFSHELL_PROVENANCE_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/UDT_WRL_CONFORMAL_CARRIER_SCALE_CLOSURE_DERIVATION_RESULTS.md",
    "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
    "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
    "udt_premise_reset_audit_2026-07-19/RERUN_PRIORITY.md",
}

CONTEXT_ONLY = {
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "MEMORY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_ELEGANT_FRAME.md",
    "UDT_METHOD_MUSIC.md",
    "UDT_DOTTED_LINE.md",
    "UDT_ELEGANCE_UNCOVER.md",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md",
    "NEGATIVES_REGISTRY.md",
}


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=text)


def history(path: str) -> tuple[str, str, str, str]:
    raw = str(git("log", "--follow", "--format=%H%x09%cs", BASE, "--", path)).splitlines()
    rows = [line.split("\t", 1) for line in raw if "\t" in line]
    if not rows:
        raise AssertionError(f"missing history: {path}")
    last_commit, last_date = rows[0]
    first_commit, first_date = rows[-1]
    return first_commit, first_date, last_commit, last_date


def initial_disposition(path: str, first_date: str) -> tuple[str, str]:
    if path in LOAD_BEARING:
        return "LOAD_BEARING", "explicit boundary-lineage source or executable evidence"
    if path in CONTEXT_ONLY:
        return "CONTEXT_ONLY", "current navigation or framing context; not affirmative calculation"
    if path.startswith(("reorganization_", "rescued_workspaces/", "native_action_sync_audit_")):
        return "DUPLICATE_SNAPSHOT", "audit, transcript, or rescued snapshot; source path reviewed instead"
    if path.startswith(("archive/pre_2026-07-01/", "archive/pre_native_coupled/")) or first_date < "2026-07-01":
        return "NEGATIVE_CONTROL", "pre-July-1 provenance firewall: failures/counterexamples only"
    if path.startswith("archive/"):
        return "CONTEXT_ONLY", "archived post-July conditional or historical context; requires explicit regrade"
    return "EXCLUDED_WITH_REASON", "token occurs outside the bounded boundary lineage; no authority inferred"


def main() -> None:
    paths = str(git("ls-tree", "-r", "--name-only", BASE)).splitlines()
    hits: dict[str, list[str]] = {}
    for path in paths:
        if Path(path).suffix not in SUFFIXES:
            continue
        data = bytes(git("show", f"{BASE}:{path}", text=False))
        source = data.decode("utf-8", errors="ignore")
        matched = [token for token in TOKENS if token in source]
        if matched:
            hits[path] = matched

    candidates = sorted(set(hits) | LOAD_BEARING | CONTEXT_ONLY)
    missing = sorted(path for path in candidates if path not in paths)
    if missing:
        raise AssertionError(f"registered paths absent from base: {missing}")

    output = HERE / "CANDIDATE_UNIVERSE.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow([
            "path", "blob", "sha256", "size_bytes", "first_commit", "first_date",
            "last_commit", "last_date", "provenance_era", "matched_tokens",
            "initial_disposition", "reason",
        ])
        for path in candidates:
            data = bytes(git("show", f"{BASE}:{path}", text=False))
            blob = str(git("rev-parse", f"{BASE}:{path}")).strip()
            first_commit, first_date, last_commit, last_date = history(path)
            era = "PRE_JULY1" if first_date < "2026-07-01" else "JULY1_OR_LATER"
            disposition, reason = initial_disposition(path, first_date)
            writer.writerow([
                path, blob, hashlib.sha256(data).hexdigest(), len(data), first_commit, first_date,
                last_commit, last_date, era, ";".join(hits.get(path, [])), disposition, reason,
            ])

    counts: dict[str, int] = {}
    with output.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
    print(f"PASS candidates={len(candidates)} token_hits={len(hits)} counts={dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
