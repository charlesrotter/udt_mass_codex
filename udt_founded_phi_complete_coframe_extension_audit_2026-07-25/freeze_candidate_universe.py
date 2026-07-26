#!/usr/bin/env python3
"""Freeze the preregistered founded-phi audit inputs and candidate universe."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "bc7713f"

TEXT_SUFFIXES = {".md", ".tsv", ".json", ".txt", ".py", ".tex", ".csv"}
PHI = re.compile(r"(?i)(?<![A-Za-z])(?:dphi|phi)(?![A-Za-z])|\\phi|[φΦ]")
ACTIVE_CONCEPT = re.compile(
    r"(?i)(?<![A-Za-z])(?:dphi|phi)(?![A-Za-z])|\\phi|[φΦ]|"
    r"reciprocal[-_ ]depth|scalar[-_ ]solder|complete[-_ ]coframe|"
    r"clock[-_ /]ruler|observer[-_ ]pair|pair[-_ ]depth|dilation"
)
DATED_ACTIVE = re.compile(r"2026-07-(?:19|20|21|22|23|24|25)$")
RESULT_ROLES = {
    "AUDIT_REPORT.md",
    "DERIVATION_REPORT.md",
    "EXACT_DERIVATION.md",
    "STATUS_LEDGER.tsv",
    "NEXT_STEP.md",
    "LAY_REPORT.md",
    "RESULT.json",
    "RESULTS.json",
    "FINAL_ADJUDICATION_REPORT.md",
    "FINAL_STATUS_LEDGER.tsv",
}
CONTROL_PATHS = {
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CANON.md",
    "MEMORY.md",
    "NEGATIVES_REGISTRY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
}
FROZEN_ACTIVE_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
INPUTS = [
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "reciprocal_c_clock_channel_correction_2026-07-19/AUDIT_REPORT.md",
    "udt_observer_pair_clock_operator_audit_2026-07-24/AUDIT_REPORT.md",
    "CANON.md",
    "udt_native_coframe_composition_law_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_native_coframe_composition_law_audit_2026-07-23/derive_composition_audit.py",
    "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md",
    "udt_intrinsic_clock_transverse_solder_audit_2026-07-24/AUDIT_REPORT.md",
    "udt_founded_constraint_atlas_p03_2026-07-21/AUDIT_REPORT.md",
    "udt_common_scale_neutrality_provenance_audit_2026-07-24/AUDIT_REPORT.md",
    "udt_global_local_relational_closure_audit_2026-07-25/AUDIT_REPORT.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
]


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout.strip()


def git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace"))
    return result.stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def active_role(path: str) -> tuple[str, str] | None:
    if path in CONTROL_PATHS:
        return "CONTROL_OR_FOUNDATION", "MANDATORY_CONTROL_OR_FOUNDATION"
    if path.startswith(FROZEN_ACTIVE_PREFIXES) and Path(path).name in RESULT_ROLES:
        return "FROZEN_ACTIVE_EVIDENCE", "ACTIVE_FINAL_ADJUDICATION_RESULT"
    parts = Path(path).parts
    if parts and DATED_ACTIVE.search(parts[0]):
        name = Path(path).name
        if name in RESULT_ROLES or name.endswith("_results.md"):
            return "CURRENT_POSTJULY_RESULT", "DATED_RESULT_ROLE"
    return None


def main() -> None:
    if git("show", "-s", "--format=%s", BASE) != "Preregister founded phi coframe extension audit":
        raise AssertionError("candidate base is not the preregistration commit")
    tracked = git("ls-tree", "-r", "--name-only", BASE).splitlines()
    concept_families: set[str] = set()
    for path in tracked:
        if path.startswith(PACKAGE + "/") or Path(path).suffix.lower() not in TEXT_SUFFIXES:
            continue
        role = active_role(path)
        if not role or path in CONTROL_PATHS:
            continue
        text = git_bytes("show", f"{BASE}:{path}").decode("utf-8", "replace")
        if ACTIVE_CONCEPT.search(text):
            concept_families.add(Path(path).parts[0])
    forensic: list[dict[str, object]] = []
    active: list[dict[str, object]] = []
    for path in tracked:
        if path.startswith(PACKAGE + "/") or Path(path).suffix.lower() not in TEXT_SUFFIXES:
            continue
        data = git_bytes("show", f"{BASE}:{path}")
        text = data.decode("utf-8", "replace")
        lines = text.splitlines()
        hits = [index for index, line in enumerate(lines, 1) if PHI.search(line)]
        concept_hits = [
            index for index, line in enumerate(lines, 1) if ACTIVE_CONCEPT.search(line)
        ]
        blob = git("rev-parse", f"{BASE}:{path}")
        excluded = (
            path.startswith(("archive/", "reorganization_", "grok/quarantine_free_DA/"))
            or "/archive/" in path
        )
        role = active_role(path)
        family_companion = bool(
            role and path not in CONTROL_PATHS and Path(path).parts[0] in concept_families
        )
        include_active = bool(
            role and not excluded and (concept_hits or family_companion or path in CONTROL_PATHS)
        )
        if hits:
            forensic.append(
                {
                    "path": path,
                    "git_blob": blob,
                    "sha256": sha(data),
                    "size_bytes": len(data),
                    "phi_line_count": len(hits),
                    "first_phi_line": hits[0],
                    "operational_exclusion": "HISTORICAL_OR_QUARANTINE" if excluded else "NONE",
                    "active_result_candidate": "YES" if include_active else "NO",
                }
            )
        if include_active:
            active.append(
                {
                    "candidate_id": "",
                    "path": path,
                    "git_blob": blob,
                    "sha256": sha(data),
                    "size_bytes": len(data),
                    "phi_line_count": len(hits),
                    "concept_line_count": len(concept_hits),
                    "source_status": role[0],
                    "selection_basis": (
                        role[1] if concept_hits or path in CONTROL_PATHS
                        else role[1] + "+CONCEPT_FAMILY_COMPANION"
                    ),
                    "primary_ruling": "PENDING",
                    "affected": "PENDING",
                }
            )
    forensic.sort(key=lambda row: str(row["path"]))
    active.sort(key=lambda row: str(row["path"]))
    for index, row in enumerate(active, 1):
        row["candidate_id"] = f"AR{index:04d}"

    sources = []
    for path in INPUTS:
        data = git_bytes("show", f"{BASE}:{path}")
        sources.append(
            {
                "path": path,
                "git_blob": git("rev-parse", f"{BASE}:{path}"),
                "sha256": sha(data),
                "size_bytes": len(data),
                "role": "LOAD_BEARING_EXTENSION_OR_PHI_STATUS_SOURCE",
            }
        )

    write_tsv(
        "FORENSIC_PHI_CENSUS.tsv",
        [
            "path",
            "git_blob",
            "sha256",
            "size_bytes",
            "phi_line_count",
            "first_phi_line",
            "operational_exclusion",
            "active_result_candidate",
        ],
        forensic,
    )
    write_tsv(
        "ACTIVE_RESULT_CANDIDATES.tsv",
        [
            "candidate_id",
            "path",
            "git_blob",
            "sha256",
            "size_bytes",
            "phi_line_count",
            "concept_line_count",
            "source_status",
            "selection_basis",
            "primary_ruling",
            "affected",
        ],
        active,
    )
    write_tsv(
        "INPUT_SOURCE_MANIFEST.tsv",
        ["path", "git_blob", "sha256", "size_bytes", "role"],
        sources,
    )
    print(f"forensic_phi_files={len(forensic)}")
    print(f"active_result_candidates={len(active)}")
    print(f"input_sources={len(sources)}")


if __name__ == "__main__":
    main()
