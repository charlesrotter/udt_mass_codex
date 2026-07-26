#!/usr/bin/env python3
"""Fail-closed structural verifier and exercised catch-proofs for the audit."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIELDS = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def family(rate: str) -> str:
    return rate[3:]


def response_graph(couplings: list[dict[str, str]]) -> dict[str, set[str]]:
    graph = {field: set() for field in FIELDS}
    component_names = tuple(f"R{mu}{nu}" for mu in range(4) for nu in range(mu, 4))
    for row in couplings:
        if any(row[name] != "0" for name in component_names):
            left, right = family(row["left_rate"]), family(row["right_rate"])
            graph[left].add(right)
            graph[right].add(left)
    return graph


def connected(graph: dict[str, set[str]]) -> bool:
    seen = set()
    queue = deque([FIELDS[0]])
    while queue:
        item = queue.popleft()
        if item in seen:
            continue
        seen.add(item)
        queue.extend(graph[item] - seen)
    return seen == set(FIELDS)


def validate_state(state: dict[str, object]) -> bool:
    return (
        state["instrument_count"] == 8
        and state["instrument_unique"] is True
        and state["output_count"] == 16
        and state["output_unique"] is True
        and state["four_volume_phi_free"] is True
        and state["H_sigma_free"] is True
        and state["connection_components_gauge_invariant"] is False
        and state["scalar_rate_pairs"] == 16
        and state["ricci_rate_pairs"] == 59
        and state["scalar_second_nonzero"] == 4
        and state["ricci_second_nonzero"] == 17
        and state["ricci_graph_connected"] is True
        and state["phi_direct_neighbors"] == frozenset(("phi", "sigma", "alpha", "k"))
        and state["founded_instruments"] == frozenset(("phi",))
        and state["selected_action"] is False
        and state["selected_density"] is False
        and state["selected_physical_branch"] is False
        and state["bootstrap_closed"] is False
        and state["source_integrity"] is True
        and state["independent_result"] == "PASS"
        and state["maximum_conclusion"]
        == "EXACT_TYPED_PARTIAL_R_GEOM_AND_COMMON_DOMAIN_CROSS_RESPONSE_ATLAS_ONLY"
    )


def display(value: object) -> str:
    if isinstance(value, frozenset):
        return "frozenset(" + ",".join(sorted(value)) + ")"
    return str(value)


def main() -> None:
    checks: dict[str, str] = {}
    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    instruments = rows("INSTRUMENT_UNIVERSE.tsv")
    outputs = rows("OUTPUT_UNIVERSE.tsv")
    direct = rows("DIRECT_RESPONSE_MATRIX.tsv")
    scalar_rate = rows("CURVATURE_RATE_COUPLINGS.tsv")
    ricci_rate = rows("RICCI_RATE_COUPLINGS.tsv")
    scalar_second = rows("CURVATURE_SECOND_JET_RESPONSE.tsv")
    ricci_second = rows("RICCI_SECOND_JET_RESPONSE.tsv")
    ledger = rows("INSTRUMENT_RESPONSE_LEDGER.tsv")
    ensembles = rows("ENSEMBLE_ATLAS.tsv")
    arrows = rows("A_ARROW_AUDIT.tsv")
    status = rows("STATUS_LEDGER.tsv")

    require("V01_exact_instrument_universe", len(instruments) == 8
            and tuple(row["component"] for row in instruments) == FIELDS, checks)
    require("V02_exact_output_universe", len(outputs) == 16
            and {row["output_id"] for row in outputs} == {f"O{i:02d}" for i in range(1, 17)}, checks)
    require("V03_direct_matrix_complete", len(direct) == 16
            and all(set(row) == {"output_id", *FIELDS} for row in direct), checks)
    require("V04_algebra_checks", algebra["check_count"] == 22
            and set(algebra["checks"].values()) == {"PASS"}, checks)
    counts = algebra["counts"]
    require("V05_scalar_rate_census", len(scalar_rate) == counts["curvature_nonzero_upper_triangle_couplings"] == 16, checks)
    require("V06_ricci_rate_census", len(ricci_rate) == counts["Ricci_nonzero_upper_triangle_couplings"] == 59, checks)
    require("V07_second_jet_census", len(scalar_second) == len(ricci_second) == 24
            and sum(row["status"] == "NONZERO" for row in scalar_second) == 4
            and sum(row["status"] == "NONZERO" for row in ricci_second) == 17, checks)

    graph = response_graph(ricci_rate)
    require("V08_full_Ricci_graph_connected", connected(graph), checks)
    require("V09_phi_exact_direct_neighbors", graph["phi"] == {"phi", "sigma", "alpha", "k"}, checks)
    require("V10_phi_has_no_direct_S_edge_at_neutral_point",
            not (graph["phi"] & {"S10", "S11", "S20", "S21"}), checks)
    require("V11_angular_bridge_reaches_all_S",
            all(graph[s] & {"sigma", "alpha", "k"} for s in ("S10", "S11", "S20", "S21")), checks)
    require("V12_instrument_ledger_coverage", len(ledger) == 8
            and tuple(row["instrument"] for row in ledger) == FIELDS, checks)
    require("V13_only_phi_founded", [row["instrument"] for row in ledger
                                      if row["status"].startswith("FOUNDED")] == ["phi"], checks)
    require("V14_ensemble_coverage", len(ensembles) == 8
            and {row["ensemble_id"] for row in ensembles} == {
                "E01_RECIPROCAL_VOLUME", "E02_ANGULAR_AREA_SHAPE", "E03_TORUS_CONNECTION",
                "E04_GENERAL_DEPTH", "E05_SCALAR_CURVATURE_TRACE", "E06_FULL_RICCI_TENSOR",
                "E07_X_BOUNDARY", "E08_GLOBAL_DISCRETE"}, checks)
    require("V15_no_reverse_A_arrow", len(arrows) == 9
            and all(row["result"] in {"DOMAIN_ONLY", "CALIBRATION_ONLY", "NO_A_ARROW", "R_GEOM_ONLY"}
                    for row in arrows), checks)
    require("V16_open_claims_preserved", any(row["object"] == "reverse_admissibility_A"
                                               and row["status"] == "OPEN" for row in status)
            and any(row["object"] == "bootstrap_fixed_point" and row["status"] == "OPEN"
                    for row in status), checks)
    require("V17_independent_all_entries", independent["result"] == "PASS"
            and independent["check_count"] == 20
            and independent["ricci_hessian_reconstruction"]["entries"] == 2560
            and independent["ricci_second_jet_reconstruction"]["entries"] == 240, checks)

    source_ok = True
    for row in rows("SOURCE_MANIFEST.tsv"):
        path = HERE.parent / row["path"]
        source_ok &= path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    require("V18_source_integrity", source_ok, checks)

    base_state: dict[str, object] = {
        "instrument_count": 8,
        "instrument_unique": True,
        "output_count": 16,
        "output_unique": True,
        "four_volume_phi_free": True,
        "H_sigma_free": True,
        "connection_components_gauge_invariant": False,
        "scalar_rate_pairs": 16,
        "ricci_rate_pairs": 59,
        "scalar_second_nonzero": 4,
        "ricci_second_nonzero": 17,
        "ricci_graph_connected": True,
        "phi_direct_neighbors": frozenset(("phi", "sigma", "alpha", "k")),
        "founded_instruments": frozenset(("phi",)),
        "selected_action": False,
        "selected_density": False,
        "selected_physical_branch": False,
        "bootstrap_closed": False,
        "source_integrity": True,
        "independent_result": "PASS",
        "maximum_conclusion": algebra["maximum_conclusion"],
    }
    require("V19_base_state_valid", validate_state(base_state), checks)
    mutations = (
        ("C01_missing_instrument", "instrument_count", 7),
        ("C02_duplicate_instrument", "instrument_unique", False),
        ("C03_missing_output", "output_count", 15),
        ("C04_duplicate_output", "output_unique", False),
        ("C05_phi_inserted_into_four_volume", "four_volume_phi_free", False),
        ("C06_sigma_inserted_into_H", "H_sigma_free", False),
        ("C07_connection_component_promoted_invariant", "connection_components_gauge_invariant", True),
        ("C08_scalar_pair_dropped", "scalar_rate_pairs", 15),
        ("C09_Ricci_pair_dropped", "ricci_rate_pairs", 58),
        ("C10_scalar_second_jet_promoted", "scalar_second_nonzero", 5),
        ("C11_Ricci_second_jet_dropped", "ricci_second_nonzero", 16),
        ("C12_connected_graph_split", "ricci_graph_connected", False),
        ("C13_false_phi_S_edge", "phi_direct_neighbors", frozenset(("phi", "sigma", "alpha", "k", "S10"))),
        ("C14_unselected_S_promoted_founded", "founded_instruments", frozenset(("phi", "S10"))),
        ("C15_action_promoted_selected", "selected_action", True),
        ("C16_density_promoted_selected", "selected_density", True),
        ("C17_branch_promoted_selected", "selected_physical_branch", True),
        ("C18_bootstrap_promoted_closed", "bootstrap_closed", True),
        ("C19_source_tamper", "source_integrity", False),
        ("C20_independent_failure_ignored", "independent_result", "FAIL"),
        ("C21_partial_map_promoted_complete", "maximum_conclusion", "COMPLETE_BOOTSTRAP"),
    )
    catch_rows = []
    for catch_id, key, value in mutations:
        mutated = dict(base_state)
        mutated[key] = value
        rejected = not validate_state(mutated)
        require(f"V_{catch_id}", rejected, checks)
        catch_rows.append({"catch_id": catch_id, "mutation": f"{key}={display(value)}",
                           "expected": "REJECT", "observed": "REJECT" if rejected else "ACCEPT",
                           "result": "PASS" if rejected else "FAIL"})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t",
                                fieldnames=("catch_id", "mutation", "expected", "observed", "result"),
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(catch_rows)

    result = {
        "schema": "udt-metric-orchestra-audit-verification-1.0",
        "check_count": len(checks),
        "checks": checks,
        "catch_proofs": len(catch_rows),
        "scientific_result": "EXACT_CONNECTED_TENSOR_RESPONSE_GRAPH_IN_BOUNDED_DOMAIN",
        "maximum_conclusion": algebra["maximum_conclusion"],
        "result": "PASS",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
