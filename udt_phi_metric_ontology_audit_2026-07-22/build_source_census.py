#!/usr/bin/env python3
"""Build the frozen-base phi source census and load-bearing lineage.

This script does not infer physics from filenames.  It only inventories literal
token occurrences, immutable source identities, commit dates, and preregistered
semantic anchors for the separately audited load-bearing source set.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


BASE = "e06fb57b3e13a398289ec687a89cfd46b3728635"
ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

TEXT_SUFFIXES = {
    ".md", ".tsv", ".txt", ".py", ".json", ".yaml", ".yml", ".tex", ".csv"
}
TOKEN = re.compile(r"(?<![A-Za-z])phi(?![A-Za-z])|φ", re.IGNORECASE)


SOURCES = [
    {
        "id": "S01",
        "path": "UDT_NATIVE_ACTION_COLD_PACKET.md",
        "authority": "CURRENT_POST_FIREWALL_FOUNDATION_PACKET",
        "use": "reciprocal ratio; CSN split; conditional metric block; static seal",
        "anchor": "phi=\\tfrac12\\ln(v/u)",
    },
    {
        "id": "S02",
        "path": "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "authority": "OWNER_LOCKED_FOUNDATIONAL_POSTULATE",
        "use": "common scale is calibration while reciprocal phi remains meaningful",
        "anchor": "Common-Scale Neutrality declares the first factor calibrational",
    },
    {
        "id": "S03",
        "path": "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "authority": "POST_FIREWALL_DERIVATION_WITH_PREMISE_STAMPS",
        "use": "composition/exponential derivation and chosen sign/unit",
        "anchor": "Sign and unit of $\\phi$",
    },
    {
        "id": "S04",
        "path": "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
        "authority": "OWNER_LOCKED_AUDIT_MEANING",
        "use": "signed local field; distance/comparison separation",
        "anchor": "Signed dilation field belonging to a location",
    },
    {
        "id": "S05",
        "path": "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
        "authority": "CURRENT_SEMANTIC_CORRECTION",
        "use": "semantic overloading diagnosis and open comparison map",
        "anchor": "The exact relation among local `phi`, observer comparison, physical distance",
    },
    {
        "id": "S06",
        "path": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
        "authority": "FROZEN_FINAL_ACTION_ADJUDICATION",
        "use": "off-shell fields and reciprocal constraint domain remain open",
        "anchor": "Off-shell fields and reciprocal constraint domain",
    },
    {
        "id": "S07",
        "path": "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
        "authority": "POST_FIREWALL_SELECTOR_AUDIT",
        "use": "metric-only; metric-plus-phi; coframe; multiplier; readout routes live",
        "anchor": "Metric-only, metric-plus-phi, coframe, multiplier, hard-constraint",
    },
    {
        "id": "S08",
        "path": "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md",
        "authority": "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "use": "independent scalar is an added class premise; no phi equation from CSN/bootstrap",
        "anchor": "whether `phi` is an independently varied field",
    },
    {
        "id": "S09",
        "path": "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md",
        "authority": "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "use": "static phi seal does not select complete coframe action",
        "anchor": "current foundation does\nnot derive one complete physical coframe action",
    },
    {
        "id": "S10",
        "path": "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md",
        "authority": "VERIFIED_WITH_CAVEATS_BOUNDED_AUDIT",
        "use": "physical readout family is unselected; phi can be metric-visible or invisible",
        "anchor": "where `phi`\ndisappears from the isolated metric block",
    },
    {
        "id": "S11",
        "path": "udt_independent_amplitude_metric_atlas_2026-07-21/PREREGISTRATION.md",
        "authority": "BOUNDED_ATLAS_PREMISE",
        "use": "independent phi was a deliberate configuration-space control",
        "anchor": "eleventh independently controlled amplitude varies `phi`",
    },
    {
        "id": "S12",
        "path": "udt_structural_ensemble_metric_atlas_2026-07-21/PREREGISTRATION.md",
        "authority": "BOUNDED_ATLAS_PREMISE",
        "use": "independent phi explicitly stamped OPEN CONFIGURATION BRANCH C02",
        "anchor": "OPEN CONFIGURATION BRANCH C02",
    },
    {
        "id": "S13",
        "path": "udt_instrument_motif_atlas_2026-07-21/AUDIT_REPORT.md",
        "authority": "OBSERVED_BOUNDED_ATLAS",
        "use": "metric/phi concomitant motifs within chosen two-jet ensemble",
        "anchor": "6,144 immutable metric/phi pointwise two-jets",
    },
    {
        "id": "S14",
        "path": "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
        "authority": "VERIFIED_WITH_CAVEATS_GLOBAL_ATLAS",
        "use": "bootstrap is on-shell admissibility and supplies no off-shell ranking functional",
        "anchor": "Current bootstrap is on-shell admissibility",
    },
    {
        "id": "S15",
        "path": "udt_local_selector_holonomy_closure_2026-07-22/AUDIT_REPORT.md",
        "authority": "VERIFIED_WITH_CAVEATS_LOCAL_ATLAS",
        "use": "metric and phi deliberately independent; native realization relation absent",
        "anchor": "deliberately varies ten metric amplitudes and `phi` independently",
    },
    {
        "id": "S16",
        "path": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "authority": "NAVIGATION_SYNTHESIS_ONLY",
        "use": "current dependency synthesis and exact open joins",
        "anchor": "The representative,\nLorentzian readout, full transverse/angular block",
    },
    {
        "id": "S17",
        "path": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE_CORRECTION_LAYER.md",
        "authority": "EXTERNAL_REVIEW_QUALIFICATION_LAYER",
        "use": "realization relation is prior to an action fork",
        "anchor": "Registered Reciprocity, CSN, finite-cell/seal data, and bootstrap constrain",
    },
    {
        "id": "S18",
        "path": "udt_metric_to_frontier_reference_2026-07-22/OPEN_JOIN_LEDGER.tsv",
        "authority": "NAVIGATION_DEPENDENCY_LEDGER",
        "use": "reciprocal block to complete time-live metric join remains open",
        "anchor": "reciprocal clock-parallel block",
    },
    {
        "id": "S19",
        "path": "CANON.md",
        "authority": "MIXED_DATE_CONTROL_HISTORICAL_ONLY_FOR_THIS_AUDIT",
        "use": "pre-July seal/operator history disclosed but not affirmative physics",
        "anchor": "C-2026-06-10-2: The finite-cell canon",
    },
]


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def route(path: str, load_bearing: set[str]) -> tuple[str, str]:
    lower = path.lower()
    if path in load_bearing:
        return "LOAD_BEARING", "INDIVIDUALLY_ADJUDICATED"
    if path == "CANON.md":
        return "MIXED_DATE_CONTROL", "ROUTED_ONLY"
    if lower.startswith("archive/") or lower.startswith("legacy/"):
        return "HISTORICAL_OR_LEGACY", "ROUTED_NOT_ADJUDICATED"
    if any(k in lower for k in ("transcript", "_raw", "request.md", "stdout", "stderr")):
        return "TRANSCRIPT_OR_RAW_EVIDENCE", "ROUTED_NOT_ADJUDICATED"
    if path in {"LIVE.md", "HANDOFF.md", "INDEX.md", "MEMORY.md", "AGENTS.md", "CLAUDE.md"}:
        return "CURRENT_CONTROL_OR_NAVIGATION", "ROUTED_NOT_AFFIRMATIVE_SOURCE"
    if Path(path).suffix == ".py":
        return "CODE_OR_VERIFIER", "ROUTED_NOT_SEMANTICALLY_ADJUDICATED"
    if re.search(r"2026-07-(?:0[1-9]|1\d|2[0-2])", path):
        return "POST_FIREWALL_EVIDENCE_CANDIDATE", "ROUTED_NOT_ADJUDICATED"
    return "OTHER_LITERAL_CANDIDATE", "ROUTED_NOT_ADJUDICATED"


def tree_entries() -> list[tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", BASE], cwd=ROOT
    )
    rows: list[tuple[str, str]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path_b = record.split(b"\t", 1)
        _mode, obj_type, blob = meta.decode().split()
        if obj_type != "blob":
            continue
        rows.append((path_b.decode(), blob))
    return rows


def first_last(path: str) -> tuple[str, str, str, str]:
    history = run(
        "git", "log", "--follow", "--format=%H%x09%aI", "--", path
    ).splitlines()
    if not history:
        raise RuntimeError(f"no history for {path}")
    last_commit, last_date = history[0].split("\t", 1)
    first_commit, first_date = history[-1].split("\t", 1)
    return first_commit, first_date, last_commit, last_date


def anchor_lines(text: str, anchor: str) -> str:
    normalized = text.replace("\r\n", "\n")
    target = anchor.replace("\r\n", "\n")
    start = normalized.find(target)
    if start < 0:
        raise RuntimeError(f"anchor not found: {anchor!r}")
    if normalized.find(target, start + 1) >= 0:
        raise RuntimeError(f"anchor not unique: {anchor!r}")
    line0 = normalized.count("\n", 0, start) + 1
    line1 = line0 + target.count("\n")
    return str(line0) if line0 == line1 else f"{line0}-{line1}"


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if run("git", "rev-parse", BASE) != BASE:
        raise RuntimeError("base commit mismatch")

    load_bearing = {row["path"] for row in SOURCES}
    entries = tree_entries()
    census: list[dict[str, object]] = []
    routing_counts: Counter[str] = Counter()
    total_occurrences = 0

    for path, blob in entries:
        suffix = Path(path).suffix.lower()
        if suffix not in TEXT_SUFFIXES and Path(path).name not in {
            "LIVE.md", "HANDOFF.md", "INDEX.md", "MEMORY.md", "AGENTS.md", "CLAUDE.md", "CANON.md"
        }:
            continue
        disk_path = ROOT / path
        if not disk_path.is_file():
            raise RuntimeError(f"base path absent from clean checkout: {path}")
        data = disk_path.read_bytes()
        if run("git", "hash-object", path) != blob:
            raise RuntimeError(f"working source differs from base blob: {path}")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        hits = len(TOKEN.findall(text))
        if not hits:
            continue
        routing, review = route(path, load_bearing)
        census.append(
            {
                "path": path,
                "git_blob": blob,
                "sha256": sha256(data),
                "bytes": len(data),
                "phi_token_occurrences": hits,
                "routing": routing,
                "review_status": review,
            }
        )
        routing_counts[routing] += 1
        total_occurrences += hits

    census.sort(key=lambda row: str(row["path"]))
    write_tsv(
        OUT / "FORENSIC_PHI_SOURCE_CENSUS.tsv",
        census,
        [
            "path", "git_blob", "sha256", "bytes", "phi_token_occurrences",
            "routing", "review_status",
        ],
    )

    lineage: list[dict[str, object]] = []
    entry_map = dict(entries)
    for source in SOURCES:
        path = source["path"]
        data = (ROOT / path).read_bytes()
        text = data.decode("utf-8")
        first_commit, first_date, last_commit, last_date = first_last(path)
        firewall = (
            "MIXED_DATE__PRE_JULY_CONTENT_NEGATIVE_OR_LINEAGE_ONLY"
            if path == "CANON.md"
            else "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE"
        )
        lineage.append(
            {
                "source_id": source["id"],
                "path": path,
                "git_blob": entry_map[path],
                "sha256": sha256(data),
                "bytes": len(data),
                "first_commit": first_commit,
                "first_commit_date": first_date,
                "last_commit": last_commit,
                "last_commit_date": last_date,
                "firewall": firewall,
                "authority": source["authority"],
                "use": source["use"],
                "anchor_lines": anchor_lines(text, source["anchor"]),
                "anchor_sha256": sha256(source["anchor"].encode()),
            }
        )

    write_tsv(
        OUT / "LOAD_BEARING_SOURCE_LINEAGE.tsv",
        lineage,
        [
            "source_id", "path", "git_blob", "sha256", "bytes", "first_commit",
            "first_commit_date", "last_commit", "last_commit_date", "firewall",
            "authority", "use", "anchor_lines", "anchor_sha256",
        ],
    )

    summary = {
        "base": BASE,
        "candidate_files": len(census),
        "literal_token_occurrences": total_occurrences,
        "load_bearing_sources": len(lineage),
        "routing_counts": dict(sorted(routing_counts.items())),
        "generated_records_excluded_from_selection": True,
        "token_regex": TOKEN.pattern,
    }
    (OUT / "FORENSIC_CENSUS_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
