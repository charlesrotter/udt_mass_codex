#!/usr/bin/env python3
"""Build the deterministic premise/package/claim dependency graph."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    owners = rows("OWNER_MEANING_LEDGER.tsv")
    conflicts = rows("SEMANTIC_CONFLICT_LEDGER.tsv")
    universe = rows("PACKAGE_UNIVERSE.tsv")
    packages = rows("PACKAGE_REGRADE.tsv")
    claims = rows("LOAD_BEARING_CLAIM_REGRADE.tsv")

    package_names = [row["package"] for row in universe]
    require(len(owners) == 15 and len({row["id"] for row in owners}) == 15, "owner census")
    require(len(conflicts) == 13 and len({row["id"] for row in conflicts}) == 13, "conflict census")
    require(len(package_names) == 19 and len(set(package_names)) == 19, "package universe census")
    require({row["package"] for row in packages} == set(package_names), "package regrade coverage")
    require(len(claims) == 42 and len({row["id"] for row in claims}) == 42, "claim census")
    require({row["package"] for row in claims} == set(package_names), "claim package coverage")

    allowed = {
        "SURVIVES_INDEPENDENT",
        "SURVIVES_CONDITIONAL_RELABELED",
        "ALGEBRA_VALID_PHYSICS_WITHDRAWN",
        "CONTAMINATED_RERUN_REQUIRED",
        "REFUTED_BY_OWNER_MEANING",
        "OUT_OF_SCOPE_NOT_REVIEWED",
    }
    require(all(row["primary_regrade"] in allowed for row in packages), "invalid package regrade")
    require(all(row["regrade"] in allowed for row in claims), "invalid claim regrade")

    nodes: list[dict[str, object]] = []
    edges: list[dict[str, str]] = []
    for row in owners:
        nodes.append({"id": row["id"], "type": "OWNER_MEANING", "label": row["symbol_or_object"], "status": row["audit_status"]})
    for row in conflicts:
        nodes.append({"id": row["id"], "type": "SEMANTIC_CONFLICT", "label": row["object"], "status": "REVIEW_REQUIRED"})
        for owner_id in sorted(set(re.findall(r"O\d{2}", " ".join(row.values())))):
            edges.append({"from": row["id"], "to": owner_id, "relation": "CONTROLLED_BY"})
    for row in packages:
        node_id = "P:" + row["package"]
        nodes.append({"id": node_id, "type": "PACKAGE", "label": row["package"], "status": row["primary_regrade"]})
    for row in claims:
        nodes.append({"id": row["id"], "type": "CLAIM", "label": row["claim"], "status": row["regrade"]})
        edges.append({"from": row["id"], "to": "P:" + row["package"], "relation": "BELONGS_TO"})
        for owner_id in sorted(set(re.findall(r"O\d{2}", row["corrected_semantic_dependency"]))):
            edges.append({"from": row["id"], "to": owner_id, "relation": "CONTROLLED_BY"})

    output = {
        "schema": "udt-premise-reset-dependency-graph-1.0",
        "base": "3b6dedf9bd2692b0ff5ba9e871d7952cf8752aad",
        "counts": {
            "owner_meanings": len(owners),
            "semantic_conflicts": len(conflicts),
            "packages": len(packages),
            "load_bearing_claims": len(claims),
            "nodes": len(nodes),
            "edges": len(edges),
        },
        "package_regrades": dict(sorted(Counter(row["primary_regrade"] for row in packages).items())),
        "claim_regrades": dict(sorted(Counter(row["regrade"] for row in claims).items())),
        "nodes": sorted(nodes, key=lambda row: str(row["id"])),
        "edges": sorted(edges, key=lambda row: (row["from"], row["relation"], row["to"])),
        "result": "PASS",
    }
    (HERE / "DEPENDENCY_GRAPH.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output["counts"], sort_keys=True))
    print(json.dumps(output["package_regrades"], sort_keys=True))


if __name__ == "__main__":
    main()
