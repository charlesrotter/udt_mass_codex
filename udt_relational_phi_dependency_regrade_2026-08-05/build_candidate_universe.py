#!/usr/bin/env python3
"""Build the deterministic broad exposure and active relational-phi regrade universes."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "682adb6c9d4cc7c9834cb5ea6a7712a32206650b"
TEXT_SUFFIXES = {".md", ".tsv", ".csv", ".py", ".json", ".txt", ".yaml", ".yml"}
CONTROLS = {
    "AGENTS.md", "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md",
    "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "NEGATIVES_REGISTRY.md",
    "research/README.md", "research/_registry/README.md",
}
PATTERNS = {
    "broad_phi_depth": re.compile(r"(?i)(?<![A-Za-z0-9_])phi(?![A-Za-z0-9_])|dphi|depth|φ"),
    "pointwise_or_physical_phi": re.compile(r"(?i)(?:absolute|pointwise|global|physical|realized|local)\s+`?phi`?|`?phi`?\s+(?:field|profile|assignment|owner|ownership|section)"),
    "independent_phi_variation": re.compile(r"(?i)(?:independent(?:ly)?\s+(?:vary|varied|variable|scalar|phi)|var(?:y|ied|iation|ying)[^\n]{0,50}phi|phi[^\n]{0,50}independent)"),
    "endpoint_difference": re.compile(r"(?i)(?:delta|depth)[^\n]{0,80}phi\s*\([^)]*\)\s*[-−]\s*phi\s*\([^)]*\)|phi\s*\([^)]*\)\s*[-−]\s*phi\s*\([^)]*\)"),
    "selection_or_ownership": re.compile(r"(?i)(?:select|selection|nonselect|owner|ownership|assign)[^\n]{0,80}(?:phi|depth)|(?:phi|depth)[^\n]{0,80}(?:select|owner|assign)"),
    "presentation_or_factorization": re.compile(r"(?i)(?:presentation|factorization|reference coframe|gauge)[^\n]{0,80}(?:phi|depth)|(?:phi|depth)[^\n]{0,80}(?:presentation|factorization|gauge)"),
    "stationary_killing": re.compile(r"(?i)(?:delta_K|q_K|Killing[^\n]{0,80}(?:phi|depth|lapse)|N\s*\([^)]*\)\s*/\s*N\s*\([^)]*\))"),
    "supplied_conditional": re.compile(r"(?i)(?:supplied|fixed|prescribed|chosen|conditional)[^\n]{0,60}(?:phi|depth)|(?:phi|depth)[^\n]{0,60}(?:supplied|fixed|prescribed|chosen|conditional)"),
    "placeholder_or_arbitrary": re.compile(r"(?i)(?:phi|depth)[^\n]{0,60}(?:undefined placeholder|arbitrary function|free scalar)|(?:undefined placeholder|arbitrary function|free scalar)[^\n]{0,60}(?:phi|depth)"),
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, errors="surrogateescape")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tracked_at_base() -> list[str]:
    return run("git", "ls-tree", "-r", "--name-only", BASE).splitlines()


def file_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def commit_info(path: str, reverse: bool) -> tuple[str, str]:
    args = ["git", "log"]
    if reverse:
        args.append("--reverse")
    args.extend(["--format=%H%x09%aI", "--diff-filter=A", "--", path])
    lines = run(*args).splitlines()
    if not lines:
        lines = run("git", "log", "-1", "--format=%H%x09%aI", "--", path).splitlines()
    if not lines:
        return "-", "-"
    commit, stamp = lines[0].split("\t", 1)
    return commit, stamp


def last_info(path: str) -> tuple[str, str]:
    lines = run("git", "log", "-1", "--format=%H%x09%aI", "--", path).splitlines()
    if not lines:
        return "-", "-"
    return tuple(lines[0].split("\t", 1))  # type: ignore[return-value]


def manifest_members() -> set[str]:
    result: set[str] = set()
    manifests = [
        "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
        "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
        "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
        "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
        "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
        "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
    ]
    for manifest in manifests:
        result.add(manifest)
        parent = Path(manifest).parent
        for line in (ROOT / manifest).read_text(encoding="utf-8").splitlines():
            if line.strip():
                result.add(str(parent / line.split(None, 1)[1].strip()))
    return result


def current_targets() -> set[str]:
    rows = read_table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    return {row["target_path"].rstrip("/") for row in rows}


def founding_sources() -> set[str]:
    package = ROOT / "udt_founding_phi_ownership_morphism_audit_2026-08-05"
    rows = read_table(package / "SOURCE_MANIFEST.tsv") + read_table(package / "SOURCE_ADDENDUM_MANIFEST.tsv")
    return {row["path"] for row in rows}


def under_target(path: str, targets: set[str]) -> bool:
    return any(path == target or path.startswith(target + "/") for target in targets)


def main() -> None:
    frozen = manifest_members()
    targets = current_targets()
    sources = founding_sources()
    exposures: list[dict[str, str]] = []
    for path in tracked_at_base():
        if path.startswith(HERE.name + "/") or Path(path).suffix.lower() not in TEXT_SUFFIXES:
            continue
        data = file_bytes(path)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        counts = {name: len(pattern.findall(text)) for name, pattern in PATTERNS.items()}
        if counts["broad_phi_depth"] == 0:
            continue
        first_commit, first_date = commit_info(path, True)
        last_commit, last_date = last_info(path)
        first_day = first_date[:10] if first_date != "-" else "-"
        historical = path.startswith(("archive/", "reorganization_")) or (first_day != "-" and first_day < "2026-07-01")
        is_control = path in CONTROLS
        is_target = under_target(path, targets)
        is_source = path in sources
        is_frozen = path in frozen
        active = (not historical and first_day >= "2026-07-01") or is_control or is_target or is_source
        exposures.append({
            "path": path,
            "bytes": str(len(data)),
            "sha256": digest(data),
            "first_commit": first_commit,
            "first_date": first_date,
            "last_commit": last_commit,
            "last_date": last_date,
            "current_control": "YES" if is_control else "NO",
            "current_frontier": "YES" if is_target else "NO",
            "founding_source": "YES" if is_source else "NO",
            "frozen_manifest": "YES" if is_frozen else "NO",
            "historical_or_pre_july": "YES" if historical else "NO",
            "active_regrade": "YES" if active else "NO",
            **{f"hits_{name}": str(counts[name]) for name in PATTERNS},
        })
    exposures.sort(key=lambda row: row["path"])
    columns = list(exposures[0]) if exposures else []
    with (HERE / "FULL_EXPOSURE_CENSUS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(exposures)
    active_rows = [row for row in exposures if row["active_regrade"] == "YES"]
    with (HERE / "ACTIVE_REGRADE_UNIVERSE.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(active_rows)
    identity_hash = digest("\n".join(row["path"] for row in active_rows).encode() + b"\n")
    summary = {
        "schema": "udt.relational_phi_regrade.universe.v1",
        "base": BASE,
        "full_exposure_count": len(exposures),
        "active_regrade_count": len(active_rows),
        "active_identity_sha256": identity_hash,
        "frozen_exposure_count": sum(row["frozen_manifest"] == "YES" for row in exposures),
        "historical_exposure_count": sum(row["historical_or_pre_july"] == "YES" for row in exposures),
        "current_control_count": sum(row["current_control"] == "YES" for row in exposures),
        "current_frontier_count": sum(row["current_frontier"] == "YES" for row in exposures),
    }
    (HERE / "UNIVERSE_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
