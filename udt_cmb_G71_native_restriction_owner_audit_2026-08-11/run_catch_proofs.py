#!/usr/bin/env python3
"""Exercise fail-closed semantic mutations for the G71 ownership result."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def valid(targets, atlas, graph) -> bool:
    if len(targets) != 6:
        return False
    names = {row["target"] for row in targets}
    if names != {"SOURCE_SHAPE_OWNER", "SOURCE_NORMALIZATION_OWNER", "PHYSICAL_ENDPOINT_OWNER",
                 "PHYSICAL_PROFILE_OWNER", "GEOMETRIC_CARRY_OWNER", "OBSERVABLE_CARRY_OWNER"}:
        return False
    by_name = {row["target"]: row for row in targets}
    if by_name["GEOMETRIC_CARRY_OWNER"]["status"] != "DERIVED_CONDITIONAL_ON_QUERY":
        return False
    if any(by_name[name]["status"] == "OWNED_NATIVE" for name in names):
        return False
    if len(atlas) != 21 or len({row["source_path"] for row in atlas}) != 21:
        return False
    if not any(row["edge"] == "observation_projection" and row["status"] == "TYPE_MISMATCH" for row in graph):
        return False
    if not any(row["edge"] == "selection_map" and row["status"] == "OPEN_NO_OWNER" for row in graph):
        return False
    if not any(row["edge"] == "global_local_selection" and row["status"] == "WORKING_GLOBAL_FRAME_ONLY" for row in graph):
        return False
    return True


def main() -> None:
    targets = table("OWNER_TARGET_LEDGER.tsv")
    atlas = table("SOURCE_TARGET_ATLAS.tsv")
    graph = table("DEPENDENCY_GRAPH.tsv")
    assert valid(targets, atlas, graph)
    mutations = {}

    def caught(name, t=targets, a=atlas, g=graph):
        mutations[name] = not valid(t, a, g)

    t = deepcopy(targets); t[0]["status"] = "OWNED_NATIVE"; caught("metric_symmetry_promoted_to_source", t=t)
    t = deepcopy(targets); t[1]["status"] = "OWNED_NATIVE"; caught("known_control_promoted_to_normalization", t=t)
    t = deepcopy(targets); t[2]["status"] = "OWNED_NATIVE"; caught("control_endpoint_promoted", t=t)
    t = deepcopy(targets); t[3]["status"] = "OWNED_NATIVE"; caught("control_profile_promoted", t=t)
    t = deepcopy(targets); t[4]["status"] = "OWNED_NATIVE"; caught("conditional_carry_promoted_universally", t=t)
    t = deepcopy(targets); t[5]["status"] = "OWNED_NATIVE"; caught("geometric_carry_called_observed", t=t)
    t = deepcopy(targets); t.pop(); caught("missing_target", t=t)
    t = deepcopy(targets); t.append(deepcopy(t[0])); caught("duplicate_target", t=t)
    a = deepcopy(atlas); a.pop(); caught("missing_source", a=a)
    a = deepcopy(atlas); a.append(deepcopy(a[0])); caught("duplicate_source", a=a)
    g = [row for row in deepcopy(graph) if row["edge"] != "observation_projection"]; caught("carry_type_guard_removed", g=g)
    g = [row for row in deepcopy(graph) if row["edge"] != "selection_map"]; caught("endpoint_selection_gap_hidden", g=g)
    g = [row for row in deepcopy(graph) if row["edge"] != "global_local_selection"]; caught("bootstrap_activated", g=g)

    assert all(mutations.values()), [name for name, value in mutations.items() if not value]
    result = {"schema": "udt-cmb-g71-catch-v1", "caught": mutations,
              "passed": sum(mutations.values()), "total": len(mutations)}
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
