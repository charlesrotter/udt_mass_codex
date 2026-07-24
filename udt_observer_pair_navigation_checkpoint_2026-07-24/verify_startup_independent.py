#!/usr/bin/env python3
"""Independent stdlib check of the observer-pair startup route."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
FILES = (
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "AGENTS.md",
    "MEMORY.md",
    "research/README.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
)
RELATIONAL = "udt_relational_pair_depth_realization_audit_2026-07-24"
OPERATOR = "udt_observer_pair_clock_operator_audit_2026-07-24"


def current_slice(text: str) -> str:
    begin = "<!-- STARTUP_CURRENT_BEGIN -->"
    end = "<!-- STARTUP_CURRENT_END -->"
    assert text.count(begin) == 1
    assert text.count(end) == 1
    return text.split(begin, 1)[1].split(end, 1)[0]


def evaluate(texts: dict[str, str]) -> dict[str, bool]:
    live = current_slice(texts["LIVE.md"])
    handoff = current_slice(texts["HANDOFF.md"])
    authority_headings = [
        line
        for line in texts["UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"].splitlines()
        if line.startswith("## ") and "authority" in line
    ]
    return {
        "all_controls_route_relational": all(RELATIONAL in texts[path] for path in FILES),
        "all_controls_route_operator": all(OPERATOR in texts[path] for path in FILES),
        "live_relational_only": "DILATION IS ONLY AN INTER-FRAME COMPARISON" in live,
        "live_three_observer_scoped":
            "THE THREE-OBSERVER CONTROL DOES NOT REFUTE PAIR DILATION" in live,
        "live_bilocal_type": "OBSERVER_INDEXED_BILOCAL_METRIC_FAMILY_GIVEN_F" in live,
        "live_next_transition": "TRANSITION LAW BETWEEN OBSERVER-INDEXED DEPTH-AND-ANGLE CHARTS" in live,
        "handoff_local_neutral":
            "local physics\n  in each observer's own frame is unchanged" in handoff,
        "handoff_three_observer_scoped": "does not invalidate pairwise dilation" in handoff,
        "handoff_next_transition":
            "transition law between observer-indexed depth-and-angle charts" in handoff,
        "memory_current": "## TOP — CURRENT POINTER (2026-07-24)" in texts["MEMORY.md"],
        "research_current": "## Current scientific spine — July 24" in texts["research/README.md"],
        "frontier_current":
            "## July 24 observer-pair clock and relational-depth overlay — current authority"
            in texts["UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"],
        "frontier_unique_current":
            sum("current authority" in line for line in authority_headings) == 1,
    }


def expect_rejection(texts: dict[str, str], file: str, old: str, new: str) -> bool:
    changed = dict(texts)
    changed[file] = changed[file].replace(old, new)
    return not all(evaluate(changed).values())


def main() -> None:
    texts = {path: (ROOT / path).read_text(encoding="utf-8") for path in FILES}
    checks = evaluate(texts)
    targets = [
        ROOT / RELATIONAL / "AUDIT_REPORT.md",
        ROOT / RELATIONAL / "STATUS_LEDGER.tsv",
        ROOT / RELATIONAL / "NEXT_STEP.md",
        ROOT / OPERATOR / "AUDIT_REPORT.md",
        ROOT / OPERATOR / "STATUS_LEDGER.tsv",
        ROOT / OPERATOR / "NEXT_STEP.md",
    ]
    checks["required_targets_exist"] = all(path.exists() for path in targets)
    catches = {
        "relational_route_loss": expect_rejection(
            texts, "AGENTS.md", RELATIONAL, "missing-relational"
        ),
        "operator_route_loss": expect_rejection(
            texts, "MEMORY.md", OPERATOR, "missing-operator"
        ),
        "local_neutrality_loss": expect_rejection(
            texts,
            "HANDOFF.md",
            "local physics\n  in each observer's own frame is unchanged",
            "local physics is slowed",
        ),
        "three_observer_overstatement": expect_rejection(
            texts,
            "LIVE.md",
            "THE THREE-OBSERVER CONTROL DOES NOT REFUTE PAIR DILATION",
            "THE THREE-OBSERVER CONTROL REFUTES PAIR DILATION",
        ),
        "ambiguous_prior_current_authority": expect_rejection(
            texts,
            "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
            "— prior authority",
            "— prior current authority",
        ),
    }
    assert all(checks.values())
    assert all(catches.values())
    output = {
        "schema": "udt-observer-pair-startup-independent-1.0",
        "result": "PASS",
        "checks": checks,
        "check_count": len(checks),
        "catches": catches,
        "catch_count": len(catches),
        "control_files": len(FILES),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
