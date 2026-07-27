#!/usr/bin/env python3
"""Independent stdlib replay; intentionally imports no production module."""

from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    out = {row[key]: row for row in rows}
    assert len(out) == len(rows)
    return out


def reject(overclaim: str, state: dict[str, bool]) -> None:
    rules = {
        "ENDPOINT_ONLY_DERIVED": state["endpoint_statement"] and state["path_independence"],
        "PATH_LABELLED_DERIVED": state["path_statement"] and state["path_constitutive"],
        "SEMANTICS_OPEN": state["abstract_ordered"] and not (
            state["endpoint_statement"] and state["path_independence"]
        ) and not (state["path_statement"] and state["path_constitutive"]),
    }
    if not rules[overclaim]:
        raise AssertionError(overclaim)


def main() -> int:
    claims = unique(read("SOURCE_CLAIM_OUTCOMES.tsv"), "claim_id")
    reqs = unique(read("REQUIREMENT_OUTCOMES.tsv"), "requirement_id")
    routes = unique(read("SEMANTIC_ROUTE_OUTCOMES.tsv"), "route_id")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))

    assert set(claims) == {f"C{i:02d}" for i in range(1, 37)}
    assert set(reqs) == {f"Q{i:02d}" for i in range(1, 19)}
    assert set(routes) == {f"R{i:02d}" for i in range(1, 9)}

    # Independent decisive-source reconstruction.
    abstract_claims = {"C02", "C04", "C05", "C07", "C08", "C12", "C15", "C33", "C36"}
    assert all(claims[c]["abstract_ordered_effect"] in {"DERIVES", "SUPPORTS"} for c in abstract_claims)
    explicit_open = {"C13", "C18", "C21", "C25", "C27", "C30", "C35", "C36"}
    assert all(claims[c]["endpoint_physical_force"] == "NO" for c in explicit_open)
    path_availability_only = {"C16", "C20", "C26", "C28"}
    assert all(claims[c]["path_physical_force"] == "NO" for c in path_availability_only)
    assert all(row["endpoint_physical_force"] == "NO" for row in claims.values())
    assert all(row["path_physical_force"] == "NO" for row in claims.values())

    state = {
        "abstract_ordered": all(reqs[q]["audit_status"].startswith("DERIVED") for q in ("Q01", "Q02", "Q03", "Q04")),
        "endpoint_statement": False,
        "path_independence": reqs["Q09"]["audit_status"] == "DERIVED",
        "path_statement": False,
        "path_constitutive": reqs["Q08"]["audit_status"] == "DERIVED",
    }
    reject("SEMANTICS_OPEN", state)
    for forbidden in ("ENDPOINT_ONLY_DERIVED", "PATH_LABELLED_DERIVED"):
        try:
            reject(forbidden, state)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"false positive {forbidden}")

    assert routes["R02"]["outcome"] == "ADMISSIBLE_CONDITIONAL"
    assert routes["R03"]["outcome"] == "DERIVED_GIVEN_INPUT_NOT_FOUNDED_PHYSICAL"
    assert routes["R06"]["outcome"] == "CONDITIONAL_ON_ENDPOINT_REQUIREMENT"
    assert routes["R08"]["outcome"] == "DERIVED_WITH_PREMISE_STAMPS"
    assert result["primary_ruling"] == "SEMANTICS_OPEN"
    assert result["endpoint_physical_forcing_claims"] == 0
    assert result["path_physical_forcing_claims"] == 0
    assert result["catch_proofs_passed"] == 16
    assert result["downstream_physics_activated"] is False

    independent = {
        "status": "PASS",
        "implementation": "stdlib_independent_no_production_import",
        "claims_replayed": len(claims),
        "requirements_replayed": len(reqs),
        "routes_replayed": len(routes),
        "forbidden_primary_rulings_rejected": 2,
        "primary_ruling_reproduced": "SEMANTICS_OPEN",
    }
    print(json.dumps(independent, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
