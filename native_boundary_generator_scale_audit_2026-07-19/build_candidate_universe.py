#!/usr/bin/env python3
"""Freeze base-tree sources relevant to boundary charge and scale selection."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "ad9e9bd5c27e4bfe40defcc225f81f2806a1c9f9"
TOKENS = (
    "lapse flux",
    "boundary charge",
    "normalized charge",
    "Hamiltonian boundary",
    "presymplectic",
    "Noether",
    "Komar",
    "Xmax=alpha",
    "X_{\\max}=\\alpha",
    "homothety",
    "Common-Scale Neutrality",
    "bootstrap",
)
SUFFIXES = {".md", ".py", ".json", ".txt", ".tsv"}

LOAD_BEARING = {
    "LIVE.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
    "asymptotic_boundary_lineage_audit_2026-07-19/BOUNDARY_OBJECT_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/GLOBAL_CLOSURE_EQUATION_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/MASS_PROVENANCE_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/QUANTITY_LIMIT_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/STATUS_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/DERIVATION_RESULT.json",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "native_action_stage1_2026-07-18/arm_A/cold_output/D0_D5.md",
    "native_action_stage1_2026-07-18/arm_B/cold_output/D0_D5.md",
    "native_action_stage2_2026-07-18/arm_A/D6_RETURN/D6.md",
    "native_action_stage2_2026-07-18/arm_B/D6_RETURN/D6.md",
    "native_action_arm_c_2026-07-18/ARM_C_RETURN/ARM_C_REPORT.md",
    "archive/native_action_chat_2026-07-14_15/UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_solution_space_closure.py",
    "archive/native_action_chat_2026-07-14_15/UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/verify_udt_finite_cell_boundary.py",
    "archive/native_action_chat_2026-07-14_15/UDT_FOUNDING_TO_DYNAMICS_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/UDT_GLOBAL_BOOTSTRAP_DERIVATION_RESULTS.md",
    "bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md",
    "bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv",
}


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=text)


def history(path: str) -> tuple[str, str, str, str]:
    raw = str(git("log", "--follow", "--format=%H%x09%cs", BASE, "--", path)).splitlines()
    parsed = [line.split("\t", 1) for line in raw if "\t" in line]
    if not parsed:
        raise AssertionError(f"missing history: {path}")
    last_commit, last_date = parsed[0]
    first_commit, first_date = parsed[-1]
    return first_commit, first_date, last_commit, last_date


def disposition(path: str, first_date: str) -> tuple[str, str]:
    if path in LOAD_BEARING:
        return "LOAD_BEARING", "explicit controlling or algebraic source"
    if path.startswith("reorganization_") or path.startswith("rescued_workspaces/"):
        return "DUPLICATE_OR_AUDIT_RECORD", "fixed historical organization or rescued snapshot"
    if first_date < "2026-07-01" or path.startswith(("archive/pre_2026-07-01/", "archive/pre_native_coupled/")):
        return "NEGATIVE_CONTROL", "pre-July-1 provenance firewall"
    if path.startswith("archive/native_action_chat_2026-07-14_15/"):
        return "CONTEXT_ONLY", "post-July archived conditional source; not selected load-bearing subset"
    if path.startswith(("native_action_stage", "native_action_arm_c_", "native_action_final_adjudication_")):
        return "CONTEXT_ONLY", "frozen action-family evidence outside explicit load-bearing subset"
    return "EXCLUDED_WITH_REASON", "token occurrence outside bounded charge/scale lineage"


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

    candidates = sorted(set(hits) | LOAD_BEARING)
    missing = sorted(path for path in candidates if path not in paths)
    if missing:
        raise AssertionError(f"registered source absent from base: {missing}")

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
            first_commit, first_date, last_commit, last_date = history(path)
            initial, reason = disposition(path, first_date)
            writer.writerow([
                path,
                str(git("rev-parse", f"{BASE}:{path}")).strip(),
                hashlib.sha256(data).hexdigest(),
                len(data), first_commit, first_date, last_commit, last_date,
                "PRE_JULY1" if first_date < "2026-07-01" else "JULY1_OR_LATER",
                ";".join(hits.get(path, [])), initial, reason,
            ])

    count: dict[str, int] = {}
    with output.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            count[row["initial_disposition"]] = count.get(row["initial_disposition"], 0) + 1
    print(f"PASS candidates={len(candidates)} token_hits={len(hits)} counts={dict(sorted(count.items()))}")


if __name__ == "__main__":
    main()
