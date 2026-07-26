#!/usr/bin/env python3
"""Freeze candidate paths from prior active census plus later tracked text changes."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR = ROOT / "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/ACTIVE_RESULT_CANDIDATES.tsv"
PRIOR_RESULT = "3ff555b4a48a70067313afef0cf10eba2e17fd49"
BASE = "b4d16fb47e87086eb24fe9115d4ee50bc47d7722"
TEXT_SUFFIXES = {".md", ".tsv", ".json", ".py", ".txt", ".yaml", ".yml"}
CONTROLS = {
    "AGENTS.md", "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "research/README.md", "research/_registry/README.md",
}


def git(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, check=True)
    return [line for line in result.stdout.splitlines() if line]


def main() -> None:
    with PRIOR.open(newline="", encoding="utf-8") as handle:
        prior_rows = list(csv.DictReader(handle, delimiter="\t"))
    sources: dict[str, set[str]] = {}
    for row in prior_rows:
        sources.setdefault(row["path"], set()).add("PRIOR_399_ACTIVE_CENSUS")
    for path in git("diff", "--name-only", f"{PRIOR_RESULT}..{BASE}"):
        if Path(path).suffix.lower() in TEXT_SUFFIXES:
            sources.setdefault(path, set()).add("POST_FOUNDED_PHI_CHANGE")
    for path in CONTROLS:
        sources.setdefault(path, set()).add("CURRENT_CONTROL")
    for path in git("ls-tree", "-r", "--name-only", BASE, "udt_global_functional_dof_constraint_rank_audit_2026-07-26"):
        if Path(path).suffix.lower() in TEXT_SUFFIXES:
            sources.setdefault(path, set()).add("FAULTY_AUDIT_PACKAGE")

    tracked = set(git("ls-tree", "-r", "--name-only", BASE))
    output = []
    for index, path in enumerate(sorted(sources), start=1):
        if path not in tracked:
            raise SystemExit(f"candidate not tracked at base: {path}")
        output.append({
            "candidate_id": f"C{index:04d}",
            "path": path,
            "selection_sources": ";".join(sorted(sources[path])),
            "base_blob": subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip(),
        })
    with (HERE / "ACTIVE_SEMANTIC_CANDIDATES.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["candidate_id", "path", "selection_sources", "base_blob"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    main()
