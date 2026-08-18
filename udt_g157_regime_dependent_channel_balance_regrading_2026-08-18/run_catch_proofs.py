#!/usr/bin/env python3
"""Mutation catches for G157's freedom-versus-owner regrading."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load():
    with (HERE / "REGRADING_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(rows):
    assert len(rows) == 20
    assert {row["source_id"] for row in rows} == {f"S{i:02d}" for i in range(1, 21)}
    assert all(row["active_depth_only_lockstep"] == "NO" for row in rows)
    by_id = {row["source_id"]: row for row in rows}
    assert by_id["S13"]["regraded_role"] == "EXPECTED_CHANNEL_FREEDOM"
    assert by_id["S18"]["regraded_role"] == "GENUINE_EVOLUTION_LAW_OPEN"
    assert by_id["S04"]["regraded_role"] == "GENUINE_TYPED_OWNER_OPEN"
    assert "cross-query carry" in by_id["S04"]["retained_open"]
    assert "does not propagate kappa" in by_id["S18"]["rationale"]
    assert all("derived physical" not in row["rationale"] for row in rows)


def catch(name, mutation):
    rows = deepcopy(load())
    mutation(rows)
    try:
        validate(rows)
    except (AssertionError, KeyError):
        return {"name": name, "caught": True}
    return {"name": name, "caught": False}


def main():
    validate(load())
    catches = [
        catch("omit_source", lambda rows: rows.pop()),
        catch("activate_depth_only_lockstep", lambda rows: rows[2].update(active_depth_only_lockstep="YES")),
        catch("call_G150_missing_selector", lambda rows: rows[12].update(regraded_role="GENUINE_TYPED_OWNER_OPEN")),
        catch("erase_common_scale_evolution_gap", lambda rows: rows[17].update(regraded_role="EXPECTED_CHANNEL_FREEDOM")),
        catch("erase_cross_query_carry_gap", lambda rows: rows[3].update(regraded_role="EXPECTED_CHANNEL_FREEDOM", retained_open="none")),
        catch("promote_varying_balance_to_prediction", lambda rows: rows[12].update(rationale="derived physical loud quiet loud score")),
    ]
    assert all(item["caught"] for item in catches)
    result = {"status": "PASS", "catch_count": len(catches), "caught": catches}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
