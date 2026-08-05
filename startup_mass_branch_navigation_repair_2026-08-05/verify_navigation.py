#!/usr/bin/env python3
"""Fail-closed verifier for the plural mass-branch navigation repair."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import stat
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = Path(__file__).with_name("VERIFICATION_RESULT.json")
BASE = "cce7d17e3d7a3bbf942a84a8a82b801c578727cd"
MAP = "udt_scientific_arc_recovery_checkpoint_2026-08-04/MASS_BRANCH_AUTHORITY_MAP.tsv"
RECON = "udt_post_july_mass_branch_reconciliation_2026-08-01/FAMILY_RECONCILIATION.tsv"
EFFECTS = "udt_post_july_mass_branch_reconciliation_2026-08-01/MECHANISM_EFFECT_MATRIX.tsv"

SOURCE_HASHES = {
    MAP: "1483331ab0e00bc6f800589edaaf56fff7c670a75292e49a05adc9935a063bdf",
    RECON: "5b195277235247d15ec04769a74397d31925525ebba4556ad888dc0ec6a89ef3",
    EFFECTS: "1925d92980256680f6b90d66f777962ad5b668903836216f171b8ce635e10d0b",
}

ARCHIVE_HASHES = {
    "archive/startup_orientation_history_2026-08-05/LIVE.pre_cleanup.md":
        "e5799c95824a5877cfedbd625b67ed6e68559f9becbf7541561333f0903e72b2",
    "archive/startup_orientation_history_2026-08-05/HANDOFF.pre_cleanup.md":
        "d103140cb43c547c04750f83636a3e9f7eba3a747653c7e581c5ed6f600c1410",
    "archive/startup_orientation_history_2026-08-05/INDEX.pre_cleanup.md":
        "9af54308d17322d59e8de610dd109a5aa8df38e52c9c657cc2c2383a7728ab7a",
    "archive/startup_orientation_history_2026-08-05/README.pre_cleanup.md":
        "239c0e3c64b283feaadaacabc9a3e29e4db003bff082eee38d6f4d3a1317f5f4",
    "archive/startup_orientation_history_2026-08-05/MEMORY.pre_cleanup.md":
        "8c25ba692a5c6117930c15e0e23b8354cb4575cda42edae94792dd09ae6f69d8",
    "archive/startup_orientation_history_2026-08-05/AGENTS.pre_cleanup.md":
        "ca754afde36a0ff6cb6ffc47a65ed9c1d19889334ccbd7a1f82b5d636a46bb95",
    "archive/startup_orientation_history_2026-08-05/CLAUDE.pre_cleanup.md":
        "59b2b74da1e087a608bccdafdac24a8f902799c396e129e3720e8bb5670b1a2e",
}

CURRENT_DOCS = [
    "LIVE.md",
    "HANDOFF.md",
    "CURRENT_RESEARCH_PROGRAM.md",
    "AGENTS.md",
    "INDEX.md",
    "README.md",
    "MEMORY.md",
    "research/particle_mass/README.md",
]

ALLOWED_TRACKED = set(CURRENT_DOCS) | {
    "startup_mass_branch_navigation_repair_2026-08-05/PREREGISTRATION.md",
    "startup_mass_branch_navigation_repair_2026-08-05/SCOPE_CORRECTION_01.md",
    "startup_mass_branch_navigation_repair_2026-08-05/verify_navigation.py",
    "startup_mass_branch_navigation_repair_2026-08-05/VERIFICATION_RESULT.json",
    "startup_mass_branch_navigation_repair_2026-08-05/AUDIT_REPORT.md",
}

PROTECTED_PREFIX = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
PROTECTED_PATH_SHA = "e33471d5aae31d7fcac7dcd531bcf1bf7ad380976f7a6c6043582bf58691222a"
PROTECTED_METADATA_SHA = "94305a15f705c3bd6dd2aea648ce994dabb0334e249c47d076ddb9ed1b047227"


class GateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_sources() -> dict[str, object]:
    actual = {path: sha((ROOT / path).read_bytes()) for path in SOURCE_HASHES}
    require(actual == SOURCE_HASHES, "FROZEN_SOURCE_HASH_DRIFT")

    branch_rows = read_tsv(MAP)
    family_rows = read_tsv(RECON)
    require(len(branch_rows) == 7, "AUTHORITY_MAP_ROW_COUNT")
    require(len(family_rows) == 7, "RECONCILIATION_ROW_COUNT")
    require([row["family_id"] for row in branch_rows] == [f"F0{i}" for i in range(1, 8)], "AUTHORITY_IDS")
    require([row["family_id"] for row in family_rows] == [f"F0{i}" for i in range(1, 8)], "RECON_IDS")
    by_id = {row["family_id"]: row for row in branch_rows}
    require(by_id["F01"]["current_status"] == "CONDITIONAL_GEOMETRIC_MASS_BEARING_BRANCH", "F01_STATUS")
    require(
        by_id["F02"]["current_status"]
        == "CONDITIONAL_GEOMETRIC_MASS_BEARING_LANDING_WITH_SECTOR_DICHOTOMY",
        "F02_STATUS",
    )
    require(by_id["F04"]["current_status"] == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL", "F04_STATUS")
    require(by_id["F03"]["current_status"] == "CONTROL_STRATUM_NOT_FAMILY", "F03_STATUS")
    require(by_id["F05"]["current_status"] == "STRUCTURAL_COMPLETION_CLASS_NOT_FAMILY", "F05_STATUS")
    require(by_id["F06"]["current_status"] == "EXACT_EMPTY_SCOPE_NOT_FAMILY", "F06_STATUS")
    require(by_id["F07"]["current_status"] == "FORMAL_MODULE_CLASS_NOT_FAMILY", "F07_STATUS")
    return {"sha256": actual, "authority_rows": len(branch_rows), "reconciliation_rows": len(family_rows)}


def validate_navigation(texts: dict[str, str]) -> dict[str, object]:
    for path, text in texts.items():
        require(MAP in text, f"MISSING_AUTHORITY_ROUTE:{path}")

    program = texts["CURRENT_RESEARCH_PROGRAM.md"]
    for token in [
        "`F01` is a conditional geometry-only mass-bearing family",
        "`F02` is a different conditional geometry-only landing",
        "`F04` is a separate genuine full-3D Hopf-capable model",
        "It is not a\n  metric-only mass branch",
        "`F03`, `F05`, `F06`, and `F07` are not additional realized mass families",
        "plural survivor map",
        "No candidate reading is yet unconditional physical UDT mass",
        "distinct\nsurvivors may ultimately belong to different sectors",
        RECON,
        EFFECTS,
    ]:
        require(token in program, f"PROGRAM_GUARD:{token}")

    live = texts["LIVE.md"]
    handoff = texts["HANDOFF.md"]
    require("No family is selected as the unique physical branch" in live, "LIVE_UNIQUE_GUARD")
    require("No unique branch or physical UDT mass has been\nselected" in handoff, "HANDOFF_UNIQUE_GUARD")
    require("F03/F05/F06/F07" in live and "not additional\nrealized mass families" in live, "LIVE_NONFAMILY_GUARD")

    for path in ("LIVE.md", "HANDOFF.md"):
        text = texts[path]
        require(text.count("<!-- STARTUP_CURRENT_BEGIN -->") == 1, f"BEGIN_MARKER:{path}")
        require(text.count("<!-- STARTUP_CURRENT_END -->") == 1, f"END_MARKER:{path}")
        require("STARTUP_PRIOR" not in text, f"STALE_STARTUP_LAYER:{path}")

    return {"documents_routed": len(texts), "family_ids_exposed": 7, "conditional_witnesses": 3}


def validate_links(texts: dict[str, str]) -> dict[str, int]:
    checked = 0
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for path, text in texts.items():
        source = ROOT / path
        for raw in pattern.findall(text):
            target = raw.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            require((source.parent / target).resolve().exists(), f"BROKEN_LINK:{path}:{raw}")
            checked += 1
    for target in SOURCE_HASHES:
        require((ROOT / target).is_file(), f"MISSING_SOURCE:{target}")
    return {"markdown_links_checked": checked, "explicit_sources_checked": len(SOURCE_HASHES)}


def validate_historical() -> dict[str, object]:
    actual = {path: sha((ROOT / path).read_bytes()) for path in ARCHIVE_HASHES}
    require(actual == ARCHIVE_HASHES, "ARCHIVE_SNAPSHOT_DRIFT")

    old_agents = (ROOT / "archive/startup_orientation_history_2026-08-05/AGENTS.pre_cleanup.md").read_bytes()
    agents = (ROOT / "AGENTS.md").read_bytes()
    marker = b"## Codex/Claude compatibility"
    require(agents[agents.index(marker):] == old_agents[old_agents.index(marker):], "AGENTS_METHOD_TAIL_DRIFT")

    changed = set(
        subprocess.check_output(["git", "diff", "--name-only", BASE], cwd=ROOT, text=True).splitlines()
    )
    require(changed <= ALLOWED_TRACKED, f"OUT_OF_SCOPE_TRACKED:{sorted(changed - ALLOWED_TRACKED)}")
    return {"archive_snapshots": len(actual), "changed_paths": sorted(changed)}


def validate_protected_untracked() -> dict[str, object]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-uall"], cwd=ROOT, text=True).splitlines()
    paths = sorted(line[3:] for line in raw if line.startswith("?? " + PROTECTED_PREFIX))
    require(len(paths) == 83, f"PROTECTED_COUNT:{len(paths)}")
    require(sha(("\n".join(paths) + "\n").encode()) == PROTECTED_PATH_SHA, "PROTECTED_PATH_SET")
    rows = []
    for item in paths:
        info = (ROOT / item).stat()
        rows.append(f"{item}\t{info.st_size}\t{info.st_mtime_ns}\t{stat.S_IMODE(info.st_mode):04o}")
    metadata_sha = sha(("\n".join(rows) + "\n").encode())
    require(metadata_sha == PROTECTED_METADATA_SHA, "PROTECTED_METADATA_DRIFT")
    return {"paths": len(paths), "path_sha256": PROTECTED_PATH_SHA, "metadata_sha256": metadata_sha}


def caught(label: str, fn) -> str:
    try:
        fn()
    except GateError:
        return "CAUGHT"
    raise GateError(f"CATCH_FAILED:{label}")


def catch_proofs(texts: dict[str, str]) -> dict[str, str]:
    def require_route(text: str) -> None:
        require(MAP in text, "ROUTE_REMOVED")

    def reject_f04_promotion(text: str) -> None:
        require("It is not a\n  metric-only mass branch" in text, "F04_PROMOTED")

    def reject_nonfamily_promotion(text: str) -> None:
        require("are not additional realized mass families" in text, "SUPPORT_PROMOTED")

    def require_plural(text: str) -> None:
        require("plural survivor map" in text, "PLURALITY_LOST")

    def require_source(data: bytes) -> None:
        require(sha(data) == SOURCE_HASHES[MAP], "SOURCE_MUTATED")

    program = texts["CURRENT_RESEARCH_PROGRAM.md"]
    return {
        "missing_authority_route_rejected": caught("route", lambda: require_route(program.replace(MAP, ""))),
        "f04_metric_only_promotion_rejected": caught(
            "f04", lambda: reject_f04_promotion(program.replace("It is not a\n  metric-only mass branch", "It is a metric-only mass branch", 1))
        ),
        "support_class_promotion_rejected": caught(
            "support", lambda: reject_nonfamily_promotion(program.replace("are not additional realized mass families", "are additional realized mass families", 1))
        ),
        "single_winner_collapse_rejected": caught("plural", lambda: require_plural(program.replace("plural survivor map", "single selected branch", 1))),
        "authority_map_mutation_rejected": caught("source", lambda: require_source((ROOT / MAP).read_bytes() + b"x")),
    }


def main() -> None:
    texts = {path: (ROOT / path).read_text(encoding="utf-8") for path in CURRENT_DOCS}
    result = {
        "status": "PASS",
        "frozen_sources": validate_sources(),
        "current_navigation": validate_navigation(texts),
        "links": validate_links(texts),
        "historical_preservation": validate_historical(),
        "protected_untracked": validate_protected_untracked(),
        "catch_proofs": catch_proofs(texts),
        "maximum_conclusion": "EXISTING_PLURAL_MASS_BRANCH_AUTHORITY_IS_EXPLICITLY_ROUTED_WITHOUT_STATUS_PROMOTION",
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
