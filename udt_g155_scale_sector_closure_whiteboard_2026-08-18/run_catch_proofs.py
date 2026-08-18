#!/usr/bin/env python3
"""Mutation catches for the G155 role/rank conclusion."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
HISTORY = {"PHYSICAL_HISTORY_CONSTRAINT", "PHYSICAL_HISTORY_EVOLUTION"}


def load() -> list[dict[str, str]]:
    with (HERE / "EQUATION_ROLE_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(rows: list[dict[str, str]], expected_landing: str = "RANK_ZERO") -> None:
    assert len(rows) == 41
    assert {r["source_id"] for r in rows} == {f"S{i:02d}" for i in range(1, 42)}
    by_source = {r["source_id"]: r for r in rows}
    assert by_source["S06"]["role"] == "INACTIVE_OR_OPEN"
    assert by_source["S06"]["active_status"] == "INACTIVE_CHALLENGED"
    assert by_source["S18"]["role"] == "CALIBRATION_OR_WORKING_FRAME"
    assert by_source["S37"]["role"] == "QUERY_EVOLUTION"
    for row in rows:
        rank = int(row["physical_history_principal_rank"])
        if row["role"] not in HISTORY:
            assert rank == 0
    history = [r for r in rows if r["role"] in HISTORY]
    landing = "RANK_ZERO" if not history else "NONZERO"
    assert landing == expected_landing


def must_catch(name: str, mutation) -> dict[str, object]:
    sample = deepcopy(load())
    mutation(sample)
    try:
        validate(sample)
    except (AssertionError, KeyError, ValueError):
        return {"name": name, "caught": True}
    return {"name": name, "caught": False}


def main() -> None:
    validate(load())
    catches = [
        must_catch("omit_frozen_source", lambda r: r.pop()),
        must_catch("promote_evaluator_to_metric_evolution", lambda r: r[39].update(role="PHYSICAL_HISTORY_EVOLUTION", physical_history_principal_rank="1")),
        must_catch("activate_strong_CSN", lambda r: r[5].update(role="PHYSICAL_HISTORY_CONSTRAINT", active_status="ACTIVE", physical_history_principal_rank="1")),
        must_catch("promote_fixed_K_to_volume_law", lambda r: r[17].update(role="PHYSICAL_HISTORY_CONSTRAINT", physical_history_principal_rank="1")),
        must_catch("promote_Jacobi_to_metric_evolution", lambda r: r[36].update(role="PHYSICAL_HISTORY_EVOLUTION", physical_history_principal_rank="2")),
    ]
    wrong_landing_caught = False
    try:
        validate(load(), expected_landing="EVOLUTION_PRESENT")
    except AssertionError:
        wrong_landing_caught = True
    catches.append({"name": "change_reported_landing", "caught": wrong_landing_caught})
    assert all(c["caught"] for c in catches)
    result = {"status": "PASS", "catch_count": len(catches), "caught": catches}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
