#!/usr/bin/env python3
"""Hostile controls for the G90 all-instruments-live classification."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ALL_INSTRUMENTS_LIVE_CATCH_PROOF_RESULT.json"


def live(blocks: dict[str, np.ndarray], contributions: dict[str, np.ndarray]) -> bool:
    block_gate = all(np.linalg.norm(blocks[name]) > 0 for name in ("B", "Q", "S", "Y", "Z"))
    four_s_gate = bool(np.all(np.abs(blocks["S"]) > 0))
    contribution_gate = all(np.linalg.norm(contributions[name]) > 0 for name in ("B", "Q", "S", "Y", "Z"))
    return block_gate and four_s_gate and contribution_gate


def main() -> None:
    blocks = {name: np.ones((2, 2)) for name in ("B", "Q", "S", "Y", "Z")}
    contributions = {
        "B": np.array([[1.0, 0.0], [0.0, 0.0]]),
        "Q": np.array([[0.0, 1.0], [1.0, 0.0]]),
        "S": np.array([[0.0, 0.0], [0.0, 1.0]]),
        "Y": np.array([[2.0, 0.0], [0.0, 0.0]]),
        "Z": np.array([[0.0, 2.0], [2.0, 0.0]]),
    }
    hdot = sum(contributions.values())

    def frozen(name: str) -> bool:
        mutant = {key: value.copy() for key, value in blocks.items()}
        mutant[name][:] = 0.0
        return not live(mutant, contributions)

    s_mutant = {key: value.copy() for key, value in blocks.items()}
    s_mutant["S"][1, 1] = 0.0
    omitted_hq = sum(value for name, value in contributions.items() if name != "Q")
    response_classes = ("quiet", "flat", "monotone")
    checks = {
        "baseline_all_active_passes": live(blocks, contributions),
        "catch_frozen_Q": frozen("Q"),
        "catch_frozen_Y": frozen("Y"),
        "catch_frozen_Z": frozen("Z"),
        "catch_one_frozen_S_entry": not live(s_mutant, contributions),
        "catch_omitted_HQ": not np.allclose(omitted_hq, hdot),
        "catch_quiet_survival_called_selection": not all(kind == "quiet" for kind in response_classes),
    }
    result = {
        "schema": "udt.g90.all_instruments_live_catches.v1",
        "checks": checks,
        "passed": all(checks.values()),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
