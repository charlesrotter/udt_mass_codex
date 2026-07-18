#!/usr/bin/env python3
"""Build the additions-only R1C root ownership and lane navigation overlay."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any


OWNERS = {
    "CONTROL_ROOT",
    "FOUNDATIONS",
    "NATIVE_ACTION",
    "PARTICLE_MASS",
    "MACRO",
    "LEGACY_FROZEN",
    "CROSS_LANE_SHARED",
    "UNKNOWN_BLOCKED",
}
RESEARCH_LANES = {"FOUNDATIONS", "NATIVE_ACTION", "PARTICLE_MASS", "MACRO"}
READINESS = {
    "RETAIN_ROOT",
    "IMMUTABLE_PATH",
    "MOVE_READY",
    "POINTER_MIGRATION_REQUIRED",
    "IMPORT_MIGRATION_REQUIRED",
    "MANIFEST_MIGRATION_REQUIRED",
    "BLOCKED",
}
FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
CONTROL_EXACT = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CANON.md",
    "CLAUDE.md",
    "CODEX_STARTUP_REHEARSAL_2026-07-17.md",
    "COGNITIVE_CORRAL_TRIGGERS_SETUP.md",
    "CROSS_MODEL_VERIFY.md",
    "HANDOFF.md",
    "HANDOFF_ARCHIVE.md",
    "HYGIENE_HEADER_TEMPLATE.md",
    "INDEX.md",
    "LIVE.md",
    "MEMORY.md",
    "NEGATIVES_REGISTRY.md",
    "PROBLEM_STATEMENT.md",
    "PROVENANCE.md",
    "README.md",
    "REORGANIZATION_R0_PREREG_2026-07-18.md",
    "STATE.md",
    "STRUCTURE_HYGIENE.md",
}
LEGACY_EXACT = {
    "regrade_S2_defect_2026-07-04.md",
}
FOUNDATION_EXACT = {
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md",
    "F4_seal_boundary_MAP.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_VERIFY_DISPATCH.md",
    "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md",
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
}
NATIVE_ACTION_EXACT_PREFIXES = (
    "UDT_NATIVE_ACTION_",
    "UDT_GR_TO_UDT_SELECTOR_",
    "UDT_WORKSTATION_TRANSFER_",
    "UDT_F_POSTRETURN_AUDIT_AND_CODEX_TRANSITION_",
)
PARTICLE_PREFIXES = (
    "noNull",
    "verify_noNull",
    "verify_virial",
    "stability_",
    "hopfion_",
    "H3_",
    "H4_",
    "UDT_H3_",
    "fs_hopfion",
    "matter_carrier_provenance_",
)
PARTICLE_EXACT = {
    "controlled_relax_hessian.py",
    "long_relax_256.py",
}
MACRO_PREFIXES = (
    "simple_metric",
    "macro_",
    "threadB_",
    "verify_lorentz_light_clue",
    "lorentz_light_clue",
)
MACRO_EXACT = {
    "J_of_s_light_deflection_confrontation_MAP.md",
    "SIMPLE_METRIC_MACRO.md",
    "UDT_DOTTED_LINE.md",
    "UDT_ELEGANCE_UNCOVER.md",
    "UDT_ELEGANT_FRAME.md",
    "UDT_METHOD_MUSIC.md",
    "UDT_NATURE_LEAN_FRAME.md",
    "verify_center_escape.py",
    "verify_center_nogo.py",
    "verify_eos_dS_window.py",
    "verify_wrl_canon.py",
    "verify_alpha_source_coeff.py",
}
AUTHORITY_SOURCES = (
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "MEMORY.md",
    "CANON.md",
    "NEGATIVES_REGISTRY.md",
    "PROVENANCE.md",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "native_action_final_adjudication_2026-07-18/PROVENANCE_FIREWALL.tsv",
)
CURRENT_SOURCE_RANGES = {
    "LIVE.md": [(1, 103)],
    "HANDOFF.md": [(1, 65), (68, 135)],
    "INDEX.md": [(1, 110)],
    "MEMORY.md": [(1, 25)],
}


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {field: str(row.get(field, "-")).replace("\t", "\\t").replace("\n", "\\n") for field in fields}
            )


def load_boundary(repo: Path) -> Any:
    path = repo / "reorganization_r1a/correction_2026-07-18/reference_boundary.py"
    spec = importlib.util.spec_from_file_location("r1c_corrected_boundary", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def in_ranges(line: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= line <= end for start, end in ranges)


def compact_sources(edges: list[dict[str, str]], categories: set[str]) -> str:
    grouped: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge["category"] in categories:
            grouped[edge["category"]].add(edge["source"])
    if not grouped:
        return "NONE"
    return "|".join(
        f"{category}[{len(sources)}]={';'.join(sorted(sources))}"
        for category, sources in sorted(grouped.items())
    )


def family_token(path: str) -> str:
    stem = PurePosixPath(path).stem
    stem = re.sub(r"(_results|_MAP|_map|_preregistration|_PREREG.*|_out|_output)$", "", stem)
    parts = stem.split("_")
    return "_".join(parts[: min(3, len(parts))])


def provisional_owner(
    row: dict[str, str],
    r0_class: str,
    r1b_class: str | None,
    authority_sources: set[str],
    text: str | None,
) -> tuple[str, str]:
    path = row["path"]
    lower = path.lower()
    corroboration = []
    if authority_sources:
        corroboration.append("CURRENT_OR_LEDGER_REFERENCE")
    if r0_class in {"ACTIVE", "CONTROL"}:
        corroboration.append("R0_ACTIVE_OR_CONTROL")
    if row["last_commit_date"] >= "2026-07-01":
        corroboration.append("POST_JULY_ACTIVITY")
    if text:
        corroboration.append("CONTENT_AVAILABLE")

    if path in CONTROL_EXACT or r0_class == "CONTROL":
        return "CONTROL_ROOT", "PERMANENT_CONTROL_REGISTRY+R0_CONTROL"
    if path in LEGACY_EXACT:
        return "LEGACY_FROZEN", "FINAL_PROVENANCE_FIREWALL_CHALLENGE_ONLY+HISTORICAL_RECORD"
    if path in FOUNDATION_EXACT:
        return "FOUNDATIONS", "CURRENT_FOUNDATION_LEDGER+OWNER_RECORD"
    if path.startswith(NATIVE_ACTION_EXACT_PREFIXES):
        return "NATIVE_ACTION", "CURRENT_NATIVE_ACTION_CONTROLLER+POST_JULY_PROVENANCE"
    if path in MACRO_EXACT:
        return "MACRO", "LIVE_MACRO_READ_ORDER+INDEX_LANE_TABLE"
    if path in PARTICLE_EXACT:
        return "PARTICLE_MASS", "STABILITY_ARC_SUPPORT_SCRIPT+PAIRED_CURRENT_RECORD"
    if path.startswith(PARTICLE_PREFIXES):
        return "PARTICLE_MASS", "LIVE_PARTICLE_ARC+FAMILY_DEPENDENCY_COHERENCE"
    if path.startswith(MACRO_PREFIXES):
        return "MACRO", "LIVE_MACRO_LANE+FAMILY_DEPENDENCY_COHERENCE"
    if lower.startswith(("native_action_", "native_readout_", "native_geometric_action")):
        return "NATIVE_ACTION", "FINAL_NATIVE_ACTION_FIREWALL+CONTENT_FAMILY"
    if lower.startswith(("matter_sector_map", "quantization_map", "udt_canonical_geometry")):
        return "FOUNDATIONS", "FOUNDATION_LEDGER_REFERENCE+CONTENT_FAMILY"
    if r1b_class == "PERMANENT_ROOT":
        return "CONTROL_ROOT", "R1B_INDIVIDUAL_PERMANENT_ROOT_RULING"
    if r1b_class in {"HARD_FROZEN", "HISTORICAL_SNAPSHOT", "BLOCKED"}:
        return "LEGACY_FROZEN", "R1B_INDIVIDUAL_HISTORICAL_OR_FROZEN_RULING"
    if r1b_class == "ACTIVE_CROSS_ERA":
        return "CROSS_LANE_SHARED", "R1B_ACTIVE_CROSS_ERA+MULTI_LANE_PROVENANCE"
    if r0_class == "FROZEN_EVIDENCE":
        return "LEGACY_FROZEN", "R0_FROZEN_EVIDENCE+FIXED_BASE_PROVENANCE"
    if row["artifact_type"] == "OPAQUE_DATA":
        return "UNKNOWN_BLOCKED", "OPAQUE_ROOT_DATA+NO_AUTHORIZED_CONTENT_INFERENCE"
    if r0_class == "UNKNOWN/BLOCKED":
        return "UNKNOWN_BLOCKED", "R0_UNKNOWN_BLOCKED+NO_CURRENT_OVERRIDE"
    if lower.startswith(("cascade_", "p1_", "p2_", "p3_", "p4_", "p5_", "weld_", "angular_")):
        return "LEGACY_FROZEN", "PRE_NATIVE_FAMILY+R0_HISTORICAL_EVIDENCE"
    if row["first_commit_date"] < "2026-07-01" and r0_class in {"MOVE_CANDIDATE", "ARCHIVE_CANDIDATE"}:
        return "LEGACY_FROZEN", "PRE_JULY_PROVENANCE+R0_MOVE_OR_ARCHIVE_CLASS"
    if len(corroboration) >= 2 and any(term in lower for term in ("mass", "carrier", "hopf", "virial")):
        return "PARTICLE_MASS", "+".join(corroboration[:2]) + "+CONTENT_SEMANTICS"
    if len(corroboration) >= 2 and any(term in lower for term in ("action", "selector", "reciprocal")):
        return "NATIVE_ACTION", "+".join(corroboration[:2]) + "+CONTENT_SEMANTICS"
    return "UNKNOWN_BLOCKED", "INSUFFICIENT_NONPREFIX_EVIDENCE"


def source_status(
    path: str,
    artifact_type: str,
    mentions: dict[str, list[tuple[int, int]]],
) -> str:
    priority = [source for source in AUTHORITY_SOURCES if source in mentions]
    if priority:
        return ";".join(
            f"{source}:{','.join(str(line) for line, _ in mentions[source][:8])}"
            for source in priority
        )
    if artifact_type == "MARKDOWN":
        return f"SELF_STATUS_BANNER:{path}"
    return "NO_EXPLICIT_PHYSICS_STATUS_SOURCE"


def readiness_for(
    row: dict[str, str],
    owner: str,
    frozen_status: str,
    inbound: list[dict[str, str]],
    unresolved: list[dict[str, str]],
) -> tuple[str, str, str]:
    if owner in {"CONTROL_ROOT", "CROSS_LANE_SHARED"}:
        return "RETAIN_ROOT", "ROOT_CONTROL_OR_SHARED_INTERFACE", "-"
    if owner == "UNKNOWN_BLOCKED" or row["artifact_type"] == "OPAQUE_DATA":
        return "BLOCKED", "OWNERSHIP_OR_OPAQUE_DATA_UNRESOLVED", "-"
    if "R0_FROZEN_EVIDENCE" in frozen_status or "REFERENCED_BY_SIX_FROZEN_PACKAGES" in frozen_status:
        return "IMMUTABLE_PATH", frozen_status, "-"
    categories = {edge["category"] for edge in inbound}
    if "MANIFEST" in categories or "ROOT_MANIFEST" in frozen_status:
        return "MANIFEST_MIGRATION_REQUIRED", "MANIFEST_DEPENDENCY_REQUIRES_SEPARATE_AUTHORITY", "-"
    if categories & {"PYTHON_IMPORT", "TEST"}:
        return "IMPORT_MIGRATION_REQUIRED", "PYTHON_IMPORT_OR_TEST_PATH_CLOSURE_REQUIRED", "-"
    if unresolved:
        return "BLOCKED", "UNRESOLVED_DYNAMIC_OR_AMBIGUOUS_PATH_TOUCH", "-"
    if categories & {"FILE_PATH", "STARTUP", "MARKDOWN_LINK", "TEXT_REFERENCE"}:
        return "POINTER_MIGRATION_REQUIRED", "EXACT_MUTABLE_POINTER_CLOSURE_REQUIRED", "-"
    lane_dir = {
        "FOUNDATIONS": "research/foundations/",
        "NATIVE_ACTION": "research/native_action/",
        "PARTICLE_MASS": "research/particle_mass/",
        "MACRO": "research/macro/",
        "LEGACY_FROZEN": "archive/pre_2026-07-01/",
    }.get(owner, "-")
    return "MOVE_READY", "NO_RECORDED_INBOUND_DEPENDENCY", lane_dir + row["path"] if lane_dir != "-" else "-"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--r0-inventory", type=Path, required=True)
    parser.add_argument("--r1b-adjudication", type=Path, required=True)
    parser.add_argument("--dependency-map", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output_root.resolve()
    registry = output / "_registry"
    registry.mkdir(parents=True, exist_ok=True)
    boundary = load_boundary(repo)
    frozen_rows = load_tsv(args.inventory)
    assert len(frozen_rows) == 1114
    root_paths = {row["path"] for row in frozen_rows}
    r0 = {row["path"]: row for row in load_tsv(args.r0_inventory)}
    r1b = {row["path"]: row for row in load_tsv(args.r1b_adjudication)}
    dependencies = load_tsv(args.dependency_map)

    inbound: dict[str, list[dict[str, str]]] = defaultdict(list)
    outbound: dict[str, list[dict[str, str]]] = defaultdict(list)
    unresolved: dict[str, list[dict[str, str]]] = defaultdict(list)
    for edge in dependencies:
        if edge["source"] in root_paths:
            outbound[edge["source"]].append(edge)
        targets = set(filter(None, edge["resolved_target"].split("|")))
        for target in root_paths & targets:
            inbound[target].append(edge)
        if edge["status"] in {"DYNAMIC", "DYNAMIC_OR_GLOB", "AMBIGUOUS_BASENAME", "MISSING_OR_GENERATED"}:
            raw = edge["raw_target"]
            for path in root_paths:
                if path in raw:
                    unresolved[path].append(edge)

    authority_texts = {}
    for source in AUTHORITY_SOURCES:
        path = repo / source
        if path.is_file():
            authority_texts[source] = path.read_text(encoding="utf-8", errors="replace")
    authority_mentions: dict[str, dict[str, list[tuple[int, int]]]] = defaultdict(dict)
    for path in sorted(root_paths):
        for source, text in authority_texts.items():
            offsets = boundary.occurrences(text, path)
            if offsets:
                authority_mentions[path][source] = [
                    (text.count("\n", 0, offset) + 1, offset) for offset in offsets
                ]

    frontier_rows = []
    for edge in dependencies:
        source = edge["source"]
        if source not in CURRENT_SOURCE_RANGES or not edge["line"].isdigit():
            continue
        line = int(edge["line"])
        if not in_ranges(line, CURRENT_SOURCE_RANGES[source]):
            continue
        if not edge["status"].startswith("RESOLVED"):
            continue
        for target in filter(None, edge["resolved_target"].split("|")):
            target_path = repo / target.rstrip("/")
            if target_path.exists():
                frontier_rows.append(
                    {
                        "target_path": target,
                        "target_kind": "ROOT_FILE" if target in root_paths else ("DIRECTORY" if target.endswith("/") else "TRACKED_NESTED"),
                        "source": source,
                        "line": line,
                        "category": edge["category"],
                    }
                )
    for target in ("UDT_METHOD_MUSIC.md", "UDT_DOTTED_LINE.md", "UDT_ELEGANCE_UNCOVER.md", "SIMPLE_METRIC_MACRO.md"):
        frontier_rows.append(
            {"target_path": target, "target_kind": "ROOT_FILE", "source": "LIVE.md", "line": 8, "category": "EXPLICIT_MACRO_READ_ORDER"}
        )
    unique_frontier = {
        (row["target_path"], row["source"], row["line"], row["category"]): row for row in frontier_rows
    }
    frontier_rows = sorted(unique_frontier.values(), key=lambda row: (row["target_path"], row["source"], row["line"]))
    frontier_targets = {row["target_path"].rstrip("/") for row in frontier_rows}

    texts = {}
    for row in frozen_rows:
        path = repo / row["path"]
        if row["artifact_type"] in {"MARKDOWN", "PYTHON", "JSON", "TSV", "CSV", "TEXT", "LOG", "CONFIG"}:
            texts[row["path"]] = path.read_text(encoding="utf-8", errors="replace")

    owner_map: dict[str, str] = {}
    basis_map: dict[str, str] = {}
    for row in frozen_rows:
        path = row["path"]
        owner, basis = provisional_owner(
            row,
            r0.get(path, {}).get("classification", "UNKNOWN/BLOCKED"),
            r1b.get(path, {}).get("classification"),
            set(authority_mentions[path]),
            texts.get(path),
        )
        owner_map[path], basis_map[path] = owner, basis

    # LIVE marks the pre-simple-metric cell/microphysics pivots as history. Apply
    # that controlling status before dependency-consumer inference so a later
    # citation cannot launder an older artifact into an active owner.
    for row in frozen_rows:
        path = row["path"]
        if (
            owner_map[path] == "UNKNOWN_BLOCKED"
            and row["artifact_type"] != "OPAQUE_DATA"
            and r0.get(path, {}).get("classification") != "UNKNOWN/BLOCKED"
            and row["last_commit_date"] <= "2026-07-08"
            and path not in frontier_targets
        ):
            owner_map[path] = "LEGACY_FROZEN"
            basis_map[path] = "LIVE_PRIOR_CELL_OR_PRE_SIMPLE_METRIC_HISTORY+COMMIT_ERA"

    # Resolve remaining unknown text/code only from corroborating inbound consumers
    # and outbound dependencies whose owners are already established.
    for _ in range(2):
        for row in frozen_rows:
            path = row["path"]
            if owner_map[path] != "UNKNOWN_BLOCKED" or row["artifact_type"] == "OPAQUE_DATA":
                continue
            consumers = {
                owner_map.get(edge["source"])
                for edge in inbound[path]
                if owner_map.get(edge["source"]) in RESEARCH_LANES
            }
            for edge in outbound[path]:
                for target in filter(None, edge["resolved_target"].split("|")):
                    if owner_map.get(target) in RESEARCH_LANES:
                        consumers.add(owner_map[target])
            if len(consumers) == 1:
                owner_map[path] = next(iter(consumers))
                basis_map[path] = "DEPENDENCY_CONSUMER_COHERENCE+CONTENT_OR_COMMIT_PROVENANCE"
            elif len(consumers) >= 2:
                owner_map[path] = "CROSS_LANE_SHARED"
                basis_map[path] = "MULTIPLE_ACTIVE_LANE_CONSUMERS+DEPENDENCY_EVIDENCE"


    ownership_rows = []
    readiness_rows = []
    for row in frozen_rows:
        path = row["path"]
        owner = owner_map[path]
        secondary = {
            owner_map.get(edge["source"])
            for edge in inbound[path]
            if owner_map.get(edge["source"]) in RESEARCH_LANES and owner_map.get(edge["source"]) != owner
        }
        if owner == "FOUNDATIONS" and path.startswith(("UDT_RECIPROCAL_", "UDT_COMMON_", "UDT_GLOBAL_", "UDT_S2_", "UDT_XMAX_")):
            secondary.add("NATIVE_ACTION")
        if owner == "NATIVE_ACTION" and path.startswith("UDT_NATIVE_ACTION_COLD"):
            secondary.add("FOUNDATIONS")
        frozen_flags = []
        r0_class = r0.get(path, {}).get("classification", "UNKNOWN/BLOCKED")
        if r0_class == "FROZEN_EVIDENCE":
            frozen_flags.append("R0_FROZEN_EVIDENCE")
        frozen_sources = sorted({edge["source"] for edge in inbound[path] if edge["source"].startswith(FROZEN_PREFIXES)})
        if frozen_sources:
            frozen_flags.append("REFERENCED_BY_SIX_FROZEN_PACKAGES")
        if any(edge["category"] == "MANIFEST" for edge in inbound[path]):
            frozen_flags.append("MANIFEST_EDGE_TARGET")
        if "manifest" in path.lower() or path in {"artifact_manifest.json", "basin_audit_manifest.json"}:
            frozen_flags.append("ROOT_MANIFEST")
        frozen_status = ";".join(frozen_flags) or "NOT_FROZEN_OR_MANIFEST"
        readiness, blockers, destination = readiness_for(
            row, owner, frozen_status, inbound[path], unresolved[path]
        )
        physics_source = source_status(path, row["artifact_type"], authority_mentions[path])
        if physics_source == "NO_EXPLICIT_PHYSICS_STATUS_SOURCE":
            paired_docs = {
                edge["source"]
                for edge in inbound[path]
                if edge["source"].endswith(".md")
            }
            for edge in outbound[path]:
                paired_docs.update(
                    target
                    for target in filter(None, edge["resolved_target"].split("|"))
                    if target.endswith(".md")
                )
            if paired_docs:
                physics_source = "DEPENDENCY_STATUS_SOURCE:" + ";".join(sorted(paired_docs)[:8])
            elif owner == "LEGACY_FROZEN":
                physics_source = "reorganization_r1b/postmove_forensic_census/ROOT_FILE_INVENTORY.tsv"
            elif owner in RESEARCH_LANES:
                physics_source = "INDEX.md+DEPENDENCY_FAMILY_EVIDENCE"
        assert owner in OWNERS and readiness in READINESS
        ownership_rows.append(
            {
                "current_path": path,
                "artifact_type": row["artifact_type"],
                "first_commit_date": row["first_commit_date"],
                "last_commit_date": row["last_commit_date"],
                "physics_status_source": physics_source,
                "frozen_manifest_status": frozen_status,
                "runtime_import_test_dependencies": compact_sources(inbound[path], {"PYTHON_IMPORT", "FILE_PATH", "TEST", "MANIFEST"}),
                "primary_owner": owner,
                "secondary_consumers": ";".join(sorted(secondary)) or "NONE",
                "ownership_evidence": basis_map[path],
                "current_frontier_target": "YES" if path in frontier_targets else "NO",
            }
        )
        readiness_rows.append(
            {
                "current_path": path,
                "primary_owner": owner,
                "migration_readiness": readiness,
                "blocking_or_change_requirement": blockers,
                "inbound_dependency_categories": ";".join(sorted({edge["category"] for edge in inbound[path]})) or "NONE",
                "inbound_dependency_sources": ";".join(sorted({edge["source"] for edge in inbound[path]})) or "NONE",
                "unresolved_dynamic_touches": len(unresolved[path]),
                "recommended_destination_if_migrated": destination,
            }
        )

    ownership_fields = (
        "current_path",
        "artifact_type",
        "first_commit_date",
        "last_commit_date",
        "physics_status_source",
        "frozen_manifest_status",
        "runtime_import_test_dependencies",
        "primary_owner",
        "secondary_consumers",
        "ownership_evidence",
        "current_frontier_target",
    )
    readiness_fields = (
        "current_path",
        "primary_owner",
        "migration_readiness",
        "blocking_or_change_requirement",
        "inbound_dependency_categories",
        "inbound_dependency_sources",
        "unresolved_dynamic_touches",
        "recommended_destination_if_migrated",
    )
    write_tsv(registry / "ROOT_OWNERSHIP.tsv", ownership_rows, ownership_fields)
    write_tsv(registry / "MIGRATION_READINESS.tsv", readiness_rows, readiness_fields)
    write_tsv(
        registry / "CURRENT_FRONTIER_TARGETS.tsv",
        frontier_rows,
        ("target_path", "target_kind", "source", "line", "category"),
    )

    lane_specs = (
        ("foundations", "FOUNDATIONS"),
        ("native_action", "NATIVE_ACTION"),
        ("particle_mass", "PARTICLE_MASS"),
        ("macro", "MACRO"),
    )
    for dirname, lane in lane_specs:
        lane_rows = []
        for own, ready in zip(ownership_rows, readiness_rows, strict=True):
            secondaries = set() if own["secondary_consumers"] == "NONE" else set(own["secondary_consumers"].split(";"))
            if own["primary_owner"] == lane or lane in secondaries:
                lane_rows.append(
                    {
                        "current_path": own["current_path"],
                        "relationship": "PRIMARY" if own["primary_owner"] == lane else "SECONDARY_CONSUMER",
                        "primary_owner": own["primary_owner"],
                        "artifact_type": own["artifact_type"],
                        "physics_status_source": own["physics_status_source"],
                        "frozen_manifest_status": own["frozen_manifest_status"],
                        "migration_readiness": ready["migration_readiness"],
                    }
                )
        write_tsv(
            output / dirname / "ROOT_INVENTORY.tsv",
            lane_rows,
            (
                "current_path",
                "relationship",
                "primary_owner",
                "artifact_type",
                "physics_status_source",
                "frozen_manifest_status",
                "migration_readiness",
            ),
        )

    summary = {
        "result": "GENERATED",
        "mode": "R1C_ADDITIONS_ONLY_LANE_OWNERSHIP_OVERLAY",
        "frozen_root_rows": len(frozen_rows),
        "ownership_rows": len(ownership_rows),
        "readiness_rows": len(readiness_rows),
        "primary_owner_counts": dict(sorted(Counter(row["primary_owner"] for row in ownership_rows).items())),
        "migration_readiness_counts": dict(sorted(Counter(row["migration_readiness"] for row in readiness_rows).items())),
        "frontier_reference_rows": len(frontier_rows),
        "frontier_unique_targets": len(frontier_targets),
        "generated_records_influence_frozen_universe": False,
    }
    (registry / "OVERLAY_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
