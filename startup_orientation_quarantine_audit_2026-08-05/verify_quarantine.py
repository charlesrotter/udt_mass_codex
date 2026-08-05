#!/usr/bin/env python3
"""Independent fail-closed verifier for the startup/orientation quarantine."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "startup_orientation_history_2026-08-05"
RESULT = Path(__file__).with_name("VERIFICATION_RESULT.json")

EXPECTED = {
    "LIVE": ("LIVE.md", "LIVE.pre_cleanup.md", "e5799c95824a5877cfedbd625b67ed6e68559f9becbf7541561333f0903e72b2", 112658),
    "HANDOFF": ("HANDOFF.md", "HANDOFF.pre_cleanup.md", "d103140cb43c547c04750f83636a3e9f7eba3a747653c7e581c5ed6f600c1410", 106117),
    "INDEX": ("INDEX.md", "INDEX.pre_cleanup.md", "9af54308d17322d59e8de610dd109a5aa8df38e52c9c657cc2c2383a7728ab7a", 58179),
    "README": ("README.md", "README.pre_cleanup.md", "239c0e3c64b283feaadaacabc9a3e29e4db003bff082eee38d6f4d3a1317f5f4", 16262),
    "MEMORY": ("MEMORY.md", "MEMORY.pre_cleanup.md", "8c25ba692a5c6117930c15e0e23b8354cb4575cda42edae94792dd09ae6f69d8", 20764),
    "AGENTS": ("AGENTS.md", "AGENTS.pre_cleanup.md", "ca754afde36a0ff6cb6ffc47a65ed9c1d19889334ccbd7a1f82b5d636a46bb95", 27287),
    "CLAUDE": ("CLAUDE.md", "CLAUDE.pre_cleanup.md", "59b2b74da1e087a608bccdafdac24a8f902799c396e129e3720e8bb5670b1a2e", 24917),
    "RESEARCH_README": ("research/README.md", "research_README.pre_cleanup.md", "d0f6284a607e7d6f4c1cebcef3c65a75e6f8db5bdf4070a127443e97ac9e1b2c", 23190),
    "REGISTRY_README": ("research/_registry/README.md", "research_registry_README.pre_cleanup.md", "aeead8a0d928cbec33ad29f47f85440f63d43e790e05c3753100a3ae7efb50a4", 4734),
}

UNCHANGED = {
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": "9128ddf72b32ef761295dcc6c370e7eb563ade8b34201c82f17989701887baef",
    "CURRENT_RESEARCH_PROGRAM.md": "e2e47cb6283efa0404431902d7a7018177c1e285869385536fb0f6856d0b5691",
    "CURRENT_SCIENTIFIC_PREMISES.md": "4962841f868b6b86de525a91ad2534041c32cee8c27379d9567e7c903a14608f",
    "CURRENT_SCIENTIFIC_PREMISES.tsv": "0fa377cb50b775875dd8f2de95acb840f3d38183c71b54caef242a89cfc1fa13",
}

DIRTY_SHA = "131a923e58322166ab247d8f1d8216ca23c8c3119e9c22d126f1efeeb2d61c69"
DIRTY_PREFIX = "?? udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"


class GateError(AssertionError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def current_block(data: bytes) -> bytes:
    marker = b"<!-- STARTUP_CURRENT_END -->"
    stop = data.index(marker) + len(marker)
    return data[:stop]


def validate_archive() -> dict[str, dict[str, object]]:
    out = {}
    for key, (_, snapshot, expected_sha, expected_bytes) in EXPECTED.items():
        data = (ARCHIVE / snapshot).read_bytes()
        require(sha(data) == expected_sha, f"ARCHIVE_HASH:{snapshot}")
        require(len(data) == expected_bytes, f"ARCHIVE_SIZE:{snapshot}")
        out[key] = {"path": str((ARCHIVE / snapshot).relative_to(ROOT)), "sha256": sha(data), "bytes": len(data)}
    return out


def validate_retained() -> dict[str, object]:
    live = (ROOT / "LIVE.md").read_bytes()
    handoff = (ROOT / "HANDOFF.md").read_bytes()
    memory = (ROOT / "MEMORY.md").read_bytes()
    old_live = (ARCHIVE / "LIVE.pre_cleanup.md").read_bytes()
    old_handoff = (ARCHIVE / "HANDOFF.pre_cleanup.md").read_bytes()
    old_memory = (ARCHIVE / "MEMORY.pre_cleanup.md").read_bytes()
    require(current_block(live) == current_block(old_live), "LIVE_CURRENT_BLOCK_DRIFT")
    require(current_block(handoff) == current_block(old_handoff), "HANDOFF_CURRENT_BLOCK_DRIFT")
    memory_stop = old_memory.index(b"## PRIOR TOP")
    require(memory.startswith(old_memory[:memory_stop].rstrip()), "MEMORY_CURRENT_TOP_DRIFT")
    agents = (ROOT / "AGENTS.md").read_bytes()
    old_agents = (ARCHIVE / "AGENTS.pre_cleanup.md").read_bytes()
    method = b"## Codex/Claude compatibility"
    require(agents[agents.index(method):] == old_agents[old_agents.index(method):], "AGENTS_BINDING_TAIL_DRIFT")
    claude = (ROOT / "CLAUDE.md").read_bytes()
    old_claude = (ARCHIVE / "CLAUDE.pre_cleanup.md").read_bytes()
    orientation = b"## Orientation"
    require(claude[:claude.index(orientation)].rstrip() == old_claude[:old_claude.index(orientation)].rstrip(), "CLAUDE_METHOD_DRIFT")
    registry = (ROOT / "research/_registry/README.md").read_bytes()
    old_registry = (ARCHIVE / "research_registry_README.pre_cleanup.md").read_bytes()
    durable = b"`ROOT_OWNERSHIP.tsv` and `MIGRATION_READINESS.tsv`"
    require(registry[registry.index(durable):] == old_registry[old_registry.index(durable):], "REGISTRY_DURABLE_SEMANTICS_DRIFT")
    return {
        "live_current_block_sha256": sha(current_block(live)),
        "handoff_current_block_sha256": sha(current_block(handoff)),
        "memory_current_prefix_sha256": sha(old_memory[:memory_stop].rstrip()),
        "agents_binding_tail_sha256": sha(agents[agents.index(method):]),
        "claude_method_prefix_sha256": sha(claude[:claude.index(orientation)].rstrip()),
        "registry_durable_tail_sha256": sha(registry[registry.index(durable):]),
    }


def validate_hygiene() -> dict[str, object]:
    texts = {name: (ROOT / name).read_text(encoding="utf-8") for name in EXPECTED.values() for name in [name[0]]}
    require(texts["LIVE.md"].count("STARTUP_CURRENT_BEGIN") == 1, "LIVE_BEGIN_COUNT")
    require(texts["LIVE.md"].count("STARTUP_CURRENT_END") == 1, "LIVE_END_COUNT")
    require("STARTUP_PRIOR" not in texts["LIVE.md"], "LIVE_STALE_MARKER")
    require(texts["HANDOFF.md"].count("STARTUP_CURRENT_BEGIN") == 1, "HANDOFF_BEGIN_COUNT")
    require(texts["HANDOFF.md"].count("STARTUP_CURRENT_END") == 1, "HANDOFF_END_COUNT")
    require("STARTUP_PRIOR" not in texts["HANDOFF.md"], "HANDOFF_STALE_MARKER")
    require("## PRIOR TOP" not in texts["MEMORY.md"], "MEMORY_PRIOR_TOP")
    require("**➤ PARENT" not in texts["INDEX.md"] and "**➤ PRIOR" not in texts["INDEX.md"], "INDEX_FRONTIER_TOUR")
    require("## Prior scientific checkpoint" not in texts["README.md"], "README_PRIOR_CHECKPOINT")
    require("PRE-P4" not in texts["AGENTS.md"] and "udt_general_screen_complete_cell_atlas" not in texts["AGENTS.md"], "AGENTS_DATED_ROUTE")
    claude_orientation = texts["CLAUDE.md"].split("## Orientation", 1)[1]
    require("SUBSUMED / HISTORICAL trackers" not in claude_orientation, "CLAUDE_STALE_TRACKERS")
    require("70 passed" not in claude_orientation and "69 passed" not in claude_orientation, "CLAUDE_PINNED_TEST_COUNT")
    require("## Parent scientific spine" not in texts["research/README.md"], "RESEARCH_PARENT_TOUR")
    require("## Prior scientific spine" not in texts["research/README.md"], "RESEARCH_PRIOR_TOUR")
    for name in ("AGENTS.md", "INDEX.md", "README.md", "CLAUDE.md"):
        require("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md" in texts[name], f"MISSING_FRONTIER_DISCLOSURE:{name}")
        context = texts[name].split("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", 1)[1][:220]
        require("historical" in context.lower(), f"FRONTIER_NOT_HISTORICAL:{name}")
    return {name: {"lines": len(text.splitlines()), "bytes": len(text.encode())} for name, text in texts.items()}


def validate_unchanged() -> dict[str, str]:
    out = {}
    for path, expected in UNCHANGED.items():
        actual = sha((ROOT / path).read_bytes())
        require(actual == expected, f"UNCHANGED_HASH:{path}")
        out[path] = actual
    return out


def validate_links() -> dict[str, int]:
    checked = 0
    markdown = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for path in [ROOT / name[0] for name in EXPECTED.values()] + [ARCHIVE / "README.md"]:
        for raw in markdown.findall(path.read_text(encoding="utf-8")):
            target = raw.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            require(resolved.exists(), f"BROKEN_LINK:{path.relative_to(ROOT)}:{raw}")
            checked += 1
    explicit = [
        "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "udt_native_law_order_architecture_audit_2026-08-05/AUDIT_REPORT.md",
        "research/_registry/CURRENT_ARTIFACT_PATHS.tsv", "CANON.md",
        "NEGATIVES_REGISTRY.md", "PROVENANCE.md",
    ]
    for target in explicit:
        require((ROOT / target).exists(), f"MISSING_TARGET:{target}")
    return {"markdown_links_checked": checked, "explicit_targets_checked": len(explicit)}


def validate_dirty() -> dict[str, object]:
    raw = subprocess.run(
        ["git", "status", "--porcelain=v1", "-uall"], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    ).stdout.splitlines()
    protected = sorted(line for line in raw if line.startswith(DIRTY_PREFIX))
    payload = ("\n".join(protected) + "\n").encode()
    require(len(protected) == 83, f"DIRTY_COUNT:{len(protected)}")
    require(sha(payload) == DIRTY_SHA, f"DIRTY_SHA:{sha(payload)}")
    return {"protected_paths": len(protected), "metadata_sha256": sha(payload)}


def caught(label: str, fn) -> str:
    try:
        fn()
    except (GateError, ValueError, FileNotFoundError):
        return "CAUGHT"
    raise GateError(f"CATCH_FAILED:{label}")


def catch_proofs() -> dict[str, str]:
    old_live = (ARCHIVE / "LIVE.pre_cleanup.md").read_bytes()
    current = (ROOT / "LIVE.md").read_bytes()
    frontier = (ROOT / "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md").read_bytes()

    def check_hash(data: bytes, expected: str) -> None:
        require(sha(data) == expected, "MUTATED_HASH")

    def check_current(data: bytes) -> None:
        require(current_block(data) == current_block(old_live), "CURRENT_DRIFT")

    def check_markers(data: bytes) -> None:
        text = data.decode()
        require(text.count("STARTUP_CURRENT_BEGIN") == 1 and text.count("STARTUP_CURRENT_END") == 1, "MARKERS")
        require("STARTUP_PRIOR" not in text, "STALE")

    return {
        "archive_mutation_rejected": caught("archive", lambda: check_hash(old_live + b"x", EXPECTED["LIVE"][2])),
        "current_block_mutation_rejected": caught("current", lambda: check_current(current.replace(b"FOUNDING OBJECT", b"ALTERED OBJECT", 1))),
        "duplicate_marker_rejected": caught("duplicate", lambda: check_markers(current + b"\n<!-- STARTUP_CURRENT_BEGIN -->\n")),
        "stale_prior_marker_rejected": caught("stale", lambda: check_markers(current + b"\n<!-- STARTUP_PRIOR_BEGIN -->\n")),
        "frontier_mutation_rejected": caught("frontier", lambda: check_hash(frontier + b"x", UNCHANGED["UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"])),
        "current_program_mutation_rejected": caught("program", lambda: check_hash((ROOT / "CURRENT_RESEARCH_PROGRAM.md").read_bytes() + b"x", UNCHANGED["CURRENT_RESEARCH_PROGRAM.md"])),
    }


def main() -> None:
    result = {
        "status": "PASS",
        "archive_snapshots": validate_archive(),
        "retained_fragments": validate_retained(),
        "live_hygiene": validate_hygiene(),
        "unchanged_authorities": validate_unchanged(),
        "links": validate_links(),
        "protected_dirty_metadata": validate_dirty(),
        "catch_proofs": catch_proofs(),
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
