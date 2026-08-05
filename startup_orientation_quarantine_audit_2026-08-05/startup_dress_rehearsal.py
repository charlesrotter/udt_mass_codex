#!/usr/bin/env python3
"""Zero-history rehearsal of the bounded startup route."""

from __future__ import annotations

import json
import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def marked(path: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    begin = "<!-- STARTUP_CURRENT_BEGIN -->"
    end = "<!-- STARTUP_CURRENT_END -->"
    assert text.count(begin) == text.count(end) == 1
    return text.split(begin, 1)[1].split(end, 1)[0]


def main() -> None:
    live = marked("LIVE.md")
    handoff = marked("HANDOFF.md")
    program = (ROOT / "CURRENT_RESEARCH_PROGRAM.md").read_text(encoding="utf-8")
    premises = (ROOT / "CURRENT_SCIENTIFIC_PREMISES.md").read_text(encoding="utf-8")
    with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(encoding="utf-8", newline="") as handle:
        premise_rows = list(csv.DictReader(handle, delimiter="\t"))
    index = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    memory = (ROOT / "MEMORY.md").read_text(encoding="utf-8")

    assertions = {
        "live_wins": "overrides every older status description" in live,
        "program_is_spine": "CURRENT_RESEARCH_PROGRAM.md" in live and "CURRENT_RESEARCH_PROGRAM.md" in handoff,
        "founded_object_relational": "relational character" in live and "supplied depth" in live,
        "general_pair_depth_open": "actual two-observer relational depth law" in live and "still `OPEN`" in live,
        "law_order_not_derived": "law-order `NOT_DERIVED`" in live,
        "response_first_only_priority": "WORKING_PRIORITY_FOR_BOUNDED_TEST" in live,
        "action_first_conditional": "ADMISSIBLE_CONDITIONAL" in live,
        "xmax_gate_present": "positional-dilation asymptote" in live and "X_max" in program,
        "complete_return_open": "complete bootstrap return" in program and "OPEN" in program,
        "next_is_bounded_not_launched": "not launched by the present audit" in program and "not automatic" in handoff.lower(),
        "premise_registry_current": len(premise_rows) == 27 and "Current scientific premise index" in premises,
        "index_is_pointer_only": "Historical navigation" in index and "PARENT SCIENTIFIC" not in index,
        "memory_has_one_top": memory.count("## TOP — CURRENT POINTER") == 1 and "## PRIOR TOP" not in memory,
    }
    assert all(assertions.values()), {key: value for key, value in assertions.items() if not value}
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    result = {
        "status": "PASS",
        "branch": branch,
        "head": head,
        "documents_read": [
            "LIVE.md#STARTUP_CURRENT", "HANDOFF.md#STARTUP_CURRENT",
            "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
            "INDEX.md", "MEMORY.md",
        ],
        "assertions": assertions,
        "maximum_conclusion": "BOUNDED_ORIENTATION_REPRODUCES_CURRENT_OPEN_SCIENTIFIC_STATE",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
