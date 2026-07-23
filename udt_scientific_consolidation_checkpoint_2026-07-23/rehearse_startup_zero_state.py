#!/usr/bin/env python3
"""Zero-state deterministic rehearsal of the bounded startup path.

This process receives no conversational context and does not import either
checkpoint builder or verifier.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def bounded(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    begin = "<!-- STARTUP_CURRENT_BEGIN -->"
    end = "<!-- STARTUP_CURRENT_END -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise AssertionError(f"startup markers: {path.name}")
    return text.split(begin, 1)[1].split(end, 1)[0]


def git(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout.strip()


def main() -> None:
    agents = ROOT.joinpath("AGENTS.md").read_text(encoding="utf-8")
    live = bounded(ROOT / "LIVE.md")
    handoff = bounded(ROOT / "HANDOFF.md")
    checkpoint = HERE.joinpath("SCIENTIFIC_CHECKPOINT.md").read_text(encoding="utf-8")
    statuses = read_tsv(HERE / "CURRENT_STATUS_LEDGER.tsv")
    maps = read_tsv(HERE / "METRIC_TO_FRONTIER_MAP.tsv")
    guards = read_tsv(HERE / "REGRESSION_GUARD_LEDGER.tsv")
    status = {row["object"]: row["status"] for row in statuses}

    checks = {
        "AGENTS_orders_LIVE_before_HANDOFF": agents.find("`LIVE.md`") < agents.find("`HANDOFF.md`"),
        "AGENTS_orders_checkpoint_after_HANDOFF": agents.find("`HANDOFF.md`")
        < agents.find("udt_scientific_consolidation_checkpoint_2026-07-23"),
        "LIVE_is_bounded": len(live.splitlines()) <= 60,
        "HANDOFF_is_bounded": len(handoff.splitlines()) <= 60,
        "LIVE_points_to_checkpoint": "udt_scientific_consolidation_checkpoint_2026-07-23"
        in live,
        "HANDOFF_points_to_checkpoint": "udt_scientific_consolidation_checkpoint_2026-07-23"
        in handoff,
        "status_count": len(statuses) == 24,
        "map_count": len(maps) == 13,
        "guard_count": len(guards) == 15,
        "finite_cell_not_solved": "complete on-shell `(g,phi)`"
        in checkpoint.lower()
        and "remains zero" in checkpoint.lower(),
        "current_seam_present": "conformally natural connection" in checkpoint,
        "no_follow_on_authorized": "does not authorize an action" in checkpoint,
        "reciprocal_status": status.get("reciprocal_kinematics") == "DERIVED",
        "action_status": status.get("complete_action") == "OPEN",
        "carrier_status": status.get("S2_carrier") == "POSIT",
        "scale_status": status.get("absolute_scale") == "OPEN",
    }
    output = {
        "schema": "udt-zero-state-startup-rehearsal-1.0",
        "method": "deterministic_parser_no_conversational_context_no_external_model",
        "python": sys.version.split()[0],
        "branch": git("branch", "--show-current"),
        "head": git("rev-parse", "HEAD"),
        "worktree_status": git("status", "--short"),
        "bounded_lines": {
            "LIVE.md": len(live.splitlines()),
            "HANDOFF.md": len(handoff.splitlines()),
        },
        "orientation": {
            "honest_claim": (
                "reciprocal kinematics and the scoped local causal 3plus3 "
                "geometry are derived; the finite-cell taxonomy is crossed "
                "but no complete on-shell branch is supplied"
            ),
            "premise_stamps": (
                "exact C0/C1 plus registered regularity/nontriviality/sign/unit; "
                "timelike observer meaning requires nonzero timelike dphi and "
                "recorded time orientation"
            ),
            "open_seam": (
                "conformally natural pre-scale transport versus bootstrap "
                "selection of a physical metric representative"
            ),
            "authority_boundary": (
                "no finite-cell branch, representative, action, carrier, "
                "scale, or matter law is selected"
            ),
            "status_excerpt": {
                key: status[key]
                for key in (
                    "reciprocal_kinematics",
                    "timelike_dphi_3plus3",
                    "spacelike_dphi_3plus3",
                    "null_dphi_filtration",
                    "zero_dphi_reduction",
                    "finite_cell_completion_cross",
                    "C2_Bach_bulk_action",
                    "EH_route",
                    "S2_carrier",
                    "particle_stability",
                    "complete_action",
                    "native_source",
                    "boundary_charge",
                    "absolute_scale",
                    "bridge",
                    "unconditional_mass",
                )
            },
            "regression_guards": [
                row["current_ruling"] for row in guards[:8]
            ],
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    HERE.joinpath("ZERO_STATE_REHEARSAL_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# Zero-state startup rehearsal output",
        "",
        f"- Method: `{output['method']}`",
        f"- Branch: `{output['branch']}`",
        f"- HEAD at rehearsal: `{output['head']}`",
        f"- Checks: `{sum(checks.values())}/{len(checks)}`",
        f"- LIVE bounded lines: `{output['bounded_lines']['LIVE.md']}`",
        f"- HANDOFF bounded lines: `{output['bounded_lines']['HANDOFF.md']}`",
        "",
        "## Orientation recovered",
        "",
        output["orientation"]["honest_claim"] + ".",
        "",
        "Premises: " + output["orientation"]["premise_stamps"] + ".",
        "",
        "Open seam: " + output["orientation"]["open_seam"] + ".",
        "",
        "Authority boundary: " + output["orientation"]["authority_boundary"] + ".",
        "",
        "This was a deterministic no-context parser rehearsal, not an independent",
        "model review or scientific adjudication.",
    ]
    HERE.joinpath("ZERO_CONTEXT_REHEARSAL_OUTPUT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "all_checks_pass": output["all_checks_pass"],
        "check_count": len(checks),
        "branch": output["branch"],
        "head": output["head"],
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if output["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
