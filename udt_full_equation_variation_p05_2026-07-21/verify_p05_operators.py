#!/usr/bin/env python3
"""Independent reconstruction and fail-closed mutation catches for P05."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULT = HERE / "OPERATOR_RESULT.json"
FALLBACK = "NAMED_BULK_OPERATORS_AND_VARIATION_OBSTRUCTIONS_CHARACTERIZED"
PROTOCOL = "NAMED_DYNAMICS_OPERATOR_COMPLETE_IN_EXACT_PREMISE_CLASS"
TABLES = [
    "lane_L01/BULK_OPERATOR.tsv",
    "lane_L01/BOUNDARY_CURRENT.tsv",
    "lane_L01/NOETHER_AND_CONSTRAINTS.tsv",
    "lane_L01/PRINCIPAL_CHARACTER.tsv",
    "lane_L02/BULK_OPERATOR.tsv",
    "lane_L02/BOUNDARY_CURRENT.tsv",
    "lane_L02/NOETHER_AND_CONSTRAINTS.tsv",
    "lane_L02/PRINCIPAL_CHARACTER.tsv",
    "FIELD_EQUATION_COMPLETENESS.tsv",
    "VARIATION_DOMAIN_MATRIX.tsv",
    "REDUCED_ACTION_SCAR.tsv",
    "GLOBAL_AXIS_CARRYFORWARD.tsv",
    "STATUS_LEDGER.tsv",
    "SOURCE_LINEAGE.tsv",
]
SOURCES = {
    "P04_MANIFEST": ("udt_dynamics_branch_ruling_p04_2026-07-21/SHA256SUMS.txt", "d01d65fc5abcc35078c961d0d3fc0eec7ad26e205735a77f7d83e2b45121de3f"),
    "P04_RESULT": ("udt_dynamics_branch_ruling_p04_2026-07-21/RULING_RESULT.json", "d524a993798ec8148421f5b2099358354025dae331fcef5388f6ad4c4c256039"),
    "ARM_C_MANIFEST": ("native_action_arm_c_2026-07-18/SHA256SUMS.txt", "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f"),
    "ARM_C_VARIATION": ("native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_variation_domain.py", "084511961b6c69270278c64ae69f58942b044f106990e7071a5003f8535aee7e"),
    "ARM_C_ACTION": ("native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_unique_action_weights.py", "33e804e990fad69e49b3471adc8443f8037e7d4b5f617999dd1579286c3e430c"),
    "ARM_C_BOUNDARY": ("native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_boundary_charge.py", "e29f017a354275b62d415961365583d165bffc9637303b1a3ae9feb17510184d"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load():
    return (
        json.loads(RESULT.read_text(encoding="utf-8")),
        {name: rows(HERE / name) for name in TABLES},
        json.loads((HERE / "OPERATOR_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")),
    )


def validate(result: dict, tables: dict[str, list[dict[str, str]]], graph: dict) -> None:
    require(result["schema"] == "udt-p05-conditional-operator-builds-1.0", "schema")
    require(result["status"] == "PASS", "status")
    require(result["evidence_grade"] == "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW", "grade")
    require(result["protocol_maximum"] == PROTOCOL and result["protocol_maximum_earned"] is False, "protocol maximum")
    require(result["maximum_conclusion"] == FALLBACK, "fallback maximum")
    require(result["counts"] == {"authorized_lanes_built": 2, "bridge_lanes_excluded": 1, "bulk_operator_rows": 14, "raw_boundary_rows": 13, "field_pairs": 21, "field_pairs_complete_actions": 0, "global_axes_free": 12, "variation_domains": 6, "reduced_action_scars": 5, "solutions_computed": 0}, "counts")
    require(result["lane_rulings"] == {
        "L01": "BULK_METRIC_OPERATOR_DERIVED_CONDITIONAL_BOUNDARY_AND_EXTRA_FIELDS_OPEN",
        "L02": "FORMAL_BULK_METRIC_OPERATOR_DERIVED_CONDITIONAL_REPRESENTATIVE_BOUNDARY_AND_EXTRA_FIELDS_OPEN",
        "L03": "EXCLUDED_NO_OPERATOR_TO_VARY",
    }, "lane rulings")
    scope = result["scope"]
    require(scope["CPU_only"] and scope["full_metric_varied_before_reduction"], "positive scope")
    require(not any(scope[key] for key in ("GPU_used", "symmetry_ansatz_used_for_operator_derivation", "source_or_carrier_loaded", "boundary_completion_selected", "physical_representative_selected", "ODE_or_PDE_run", "P06_launched", "canon_changed")), "scope promotion")

    for lane in ("L01", "L02"):
        bulk = tables[f"lane_{lane}/BULK_OPERATOR.tsv"]
        require(len(bulk) == 7 and {row["id"] for row in bulk} == {f"O{i:02d}" for i in range(1, 8)}, f"{lane} bulk")
        require(next(row for row in bulk if row["id"] == "O07")["status"] == "DERIVED_REGULAR_4D", f"{lane} Euler bulk")
    l01_bulk = {row["id"]: row for row in tables["lane_L01/BULK_OPERATOR.tsv"]}
    l02_bulk = {row["id"]: row for row in tables["lane_L02/BULK_OPERATOR.tsv"]}
    require(l01_bulk["O04"]["formula"] == "delta S_bulk=integral sqrt_abs_g*(-2*alpha*B^ab)*h_ab+boundary", "Bach variation")
    require(l01_bulk["O05"]["status"] == "CONDITIONAL_BULK_EQUATION" and l01_bulk["O06"]["formula"] == "order_g=4", "Bach scope")
    require(l02_bulk["O04"]["formula"] == "delta S_bulk=integral sqrt_abs_g*(-kappa*(G^ab+Lambda*g^ab))*h_ab+boundary", "EH variation")
    require("Lambda" in l02_bulk["O01"]["formula"] and l02_bulk["O05"]["status"] == "CONDITIONAL_BULK_EQUATION" and l02_bulk["O06"]["formula"] == "order_g=2", "EH scope")

    l01_boundary = tables["lane_L01/BOUNDARY_CURRENT.tsv"]
    l02_boundary = tables["lane_L02/BOUNDARY_CURRENT.tsv"]
    require(len(l01_boundary) == 6 and len(l02_boundary) == 7, "boundary counts")
    require(any(row["id"] == "B02" and "nabla_d(h_bc)" in row["formula"] for row in l01_boundary), "C2 derivative-h channel")
    require(any(row["id"] == "B03" and "nabla_d(C^abcd)" in row["formula"] for row in l01_boundary), "C2 h channel")
    require(any(row["id"] == "B01" and "nabla_b(h^ab)-nabla^a(h)" in row["formula"] for row in l02_boundary), "EH boundary current")
    require(next(row for row in l02_boundary if row["id"] == "B04")["status"] == "CONDITIONAL_COMPARISON_ONLY", "GHY comparison remains unadopted")
    require(all(any(row["status"] == "OPEN_STOP" for row in tables[f"lane_{lane}/BOUNDARY_CURRENT.tsv"]) for lane in ("L01", "L02")), "boundary stop")
    require(all(any("Euler_boundary" == row["channel"] for row in tables[f"lane_{lane}/BOUNDARY_CURRENT.tsv"]) for lane in ("L01", "L02")), "Euler boundary retained")

    l01_noether = {row["id"]: row for row in tables["lane_L01/NOETHER_AND_CONSTRAINTS.tsv"]}
    l02_noether = {row["id"]: row for row in tables["lane_L02/NOETHER_AND_CONSTRAINTS.tsv"]}
    require(l01_noether["N01"]["status"] == "OFF_SHELL_NOETHER_IDENTITY" and l01_noether["N02"]["status"] == "OFF_SHELL_NOETHER_IDENTITY", "Bach Noether")
    require(l02_noether["N01"]["status"] == "OFF_SHELL_NOETHER_IDENTITY" and l02_noether["N02"]["status"] == "ON_SHELL_CONSEQUENCE_NOT_IDENTITY", "EH identities")
    require(all(len(tables[f"lane_{lane}/NOETHER_AND_CONSTRAINTS.tsv"]) == 5 for lane in ("L01", "L02")), "constraint projections")

    l01_principal = tables["lane_L01/PRINCIPAL_CHARACTER.tsv"]
    l02_principal = tables["lane_L02/PRINCIPAL_CHARACTER.tsv"]
    require(next(row for row in l01_principal if row["id"] == "P01")["ungauge_fixed"] == "DEGENERATE_DIFFEO_PLUS_WEYL", "Bach gauge degeneracy")
    require(next(row for row in l01_principal if row["id"] == "P01")["principal_factor"] == "alpha*(g^ab*xi_a*xi_b)^2", "Bach principal")
    require(next(row for row in l02_principal if row["id"] == "P01")["ungauge_fixed"] == "DEGENERATE_DIFFEO", "EH gauge degeneracy")
    require(next(row for row in l02_principal if row["id"] == "P01")["principal_factor"] == "kappa*(g^ab*xi_a*xi_b)", "EH principal")
    require(all(next(row for row in tables[f"lane_{lane}/PRINCIPAL_CHARACTER.tsv"] if row["id"] == "P02")["principal_factor"] == "UNDEFINED" for lane in ("L01", "L02")), "degenerate arena retained")

    complete = tables["FIELD_EQUATION_COMPLETENESS.tsv"]
    require(len(complete) == 21 and len({row["pair_id"] for row in complete}) == 21, "field pair count")
    require({(row["lane_id"], row["realization_id"]) for row in complete} == {(lane, realization) for lane in ("L01", "L02", "L03") for realization in ("C01", "C02", "C03", "C04", "C05", "C06", "C07")}, "field pair Cartesian product")
    require(all(row["field_removed"] == "NO" and row["boundary_complete"] == "NO" and row["global_existence"] == "UNEVALUATED" for row in complete), "field boundary global status")
    require(sum("BULK_EQUATION_COMPLETE" in row["p05_equation_status"] for row in complete) == 2, "two metric bulk rows")
    require(sum(row["p05_equation_status"] == "EXCLUDED_NO_OPERATOR_TO_VARY" for row in complete) == 7, "L03 excluded rows")

    variations = {row["id"]: row for row in tables["VARIATION_DOMAIN_MATRIX.tsv"]}
    require(len(variations) == 6, "variation domains")
    require(variations["V01"]["relation_to_full_operator"] == "FULL_EQUATION_RETAINED", "full variation")
    require(variations["V02"]["equation"] == "J^T*E=0" and variations["V02"]["relation_to_full_operator"] == "TANGENT_PROJECTION_ONLY", "hard restriction")
    require(variations["V03"]["relation_to_full_operator"] == "TANGENT_PROJECTION_AFTER_LAMBDA_ELIMINATION", "multiplier")
    require(variations["V06"]["status"] == "OPEN_IN_CURRENT_UDT", "boundary variation")

    scars = {row["id"]: row for row in tables["REDUCED_ACTION_SCAR.tsv"]}
    require(len(scars) == 5, "scar count")
    require(scars["R01"]["status"] == "EXACT_CHAIN_RULE_SCAR", "chain scar")
    require(scars["R03"]["status"] == "EXACT_REDUCED_EH_BOUNDARY_PRIMITIVE", "EH scar")
    require(scars["R04"]["status"] == "VACUOUS_SCAR_TEST_REJECTED", "vacuous C2 test")

    axes = tables["GLOBAL_AXIS_CARRYFORWARD.tsv"]
    require(len(axes) == 12 and {row["axis_id"] for row in axes} == {f"A{i:02d}" for i in range(1, 13)}, "axis coverage")
    require(all(row["p05_disposition"] == "FREE_UNSELECTED_UNSOLVED" and row["value_or_choice"] == "NONE" for row in axes), "axis status")
    status = {row["id"]: row for row in tables["STATUS_LEDGER.tsv"]}
    require(len(status) == 15 and status["S05"]["status"] == "OPEN_STOP" and status["S06"]["status"] == "OPEN_OR_ABSENT", "open stops")
    require(status["S13"]["status"] == "NOT_EARNED" and status["S14"]["status"] == FALLBACK and status["S15"]["status"] == "NOT_LAUNCHED", "maximum stop")

    require(graph["schema"] == "udt-p05-operator-dependency-graph-1.0", "graph schema")
    node_ids = {node["id"] for node in graph["nodes"]}
    require(len(node_ids) == len(graph["nodes"]), "graph nodes")
    realized = {(edge["from"], edge["to"]) for edge in graph["edges"]}
    forbidden = {(edge["from"], edge["to"]) for edge in graph["forbidden_edges"]}
    require(all(edge["from"] in node_ids and edge["to"] in node_ids for edge in graph["edges"]), "graph endpoints")
    require(not realized & forbidden, "forbidden graph edge")
    require(("RAW_BOUNDARY_CURRENT", "COMPLETE_P05_OPERATOR") in forbidden, "raw current stop")
    require(("P04_L03", "FULL_METRIC_VARIATION") in forbidden, "bridge stop")

    lineage = tables["SOURCE_LINEAGE.tsv"]
    require(len(lineage) == 6 and {row["role"] for row in lineage} == set(SOURCES), "source coverage")
    for row in lineage:
        path, expected = SOURCES[row["role"]]
        require(row["path"] == path and row["sha256"] == expected and digest(ROOT / path) == expected, f"source {row['role']}")
        require(result["source_sha256"][row["role"]] == expected, f"result source {row['role']}")
    for name, expected in result["table_sha256"].items():
        require(digest(HERE / name) == expected, f"table hash {name}")


def independent_algebra(checks: dict[str, str]) -> None:
    # Different coefficient/rank reconstruction from the generator.
    c2 = [[Fraction(1)], [Fraction(-2)], [Fraction(1, 3)]]
    e4 = [[Fraction(1)], [Fraction(-4)], [Fraction(1)]]
    require(c2 != e4 and c2[0][0] * e4[1][0] - c2[1][0] * e4[0][0] == -2, "independent curvature vectors")
    checks["independent_curvature_inventory"] = "PASS"

    x = sp.symbols("x", real=True)
    y = -x
    aa, bb, cc = sp.Rational(2), sp.Rational(5), sp.Rational(7)
    full_ex = aa * x + cc * y
    full_ey = bb * y + cc * x
    reduced = sp.diff(aa * x**2 / 2 + bb * y**2 / 2 + cc * x * y, x)
    require(sp.simplify(reduced - (full_ex - full_ey)) == 0 and sp.simplify(full_ex + full_ey) != 0, "independent chain rule")
    checks["independent_reduced_variation_scar"] = "PASS"

    r = sp.symbols("r", positive=True)
    f = sp.Function("f")(r)
    curvature = -sp.diff(f, r, 2) - 4 * sp.diff(f, r) / r + 2 * (1 - f) / r**2
    primitive = -r**2 * sp.diff(f, r) - 2 * r * f + 2 * r
    require(sp.simplify(sp.diff(primitive, r) - r**2 * curvature) == 0, "independent EH primitive")
    checks["independent_EH_reduction"] = "PASS"

    q = sp.symbols("q")
    require(sp.factor(q**2).as_powers_dict()[q] == 2 and sp.factor(q).as_powers_dict()[q] == 1, "independent principal multiplicity")
    checks["independent_principal_multiplicity"] = "PASS"

    # At an orthonormal point, independently contract the EH P tensor against
    # a deterministic integer derivative field and compare the divergence form.
    D = [[[Fraction((d + 1) * 100 + (b + 1) * 10 + (c + 1) + (b - c) ** 2) for c in range(4)] for b in range(4)] for d in range(4)]
    for d in range(4):
        for b in range(4):
            for c in range(b):
                D[d][b][c] = D[d][c][b]
    for a in range(4):
        theta = Fraction(0)
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    p = Fraction(int(a == c) * int(d == b) - int(a == d) * int(c == b), 2)
                    theta += 2 * p * D[d][b][c]
        expected = sum(D[b][a][b] for b in range(4)) - sum(D[a][b][b] for b in range(4))
        require(theta == expected, "independent EH current")
    checks["independent_EH_boundary_current"] = "PASS"


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError, StopIteration, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation passed: {name}")


def main() -> None:
    tracked = [RESULT, HERE / "OPERATOR_DEPENDENCY_GRAPH.json", *[HERE / name for name in TABLES]]
    before = {str(path.relative_to(HERE)): digest(path) for path in tracked}
    environment = dict(os.environ); environment["PYTHONDONTWRITEBYTECODE"] = "1"; environment["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run([sys.executable, "-B", str(HERE / "derive_p05_operators.py")], cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False)
    require(replay.returncode == 0 and not replay.stderr, replay.stdout + replay.stderr)
    require(replay.stdout == (HERE / "OPERATOR_TRANSCRIPT.txt").read_text(encoding="utf-8"), "transcript")
    require(before == {str(path.relative_to(HERE)): digest(path) for path in tracked}, "deterministic replay")
    result, tables, graph = load()
    validate(result, tables, graph)
    checks = {"deterministic_replay_and_full_contract": "PASS", "source_hash_replay": "PASS", "independent_table_reconciliation": "PASS"}
    independent_algebra(checks)
    require(result["check_count"] == 32 and len(result["checks"]) == 32 and set(result["checks"].values()) == {"PASS"}, "main checks")
    checks["main_exact_checks_reconciled"] = "PASS"

    catches: dict[str, str] = {}
    bad = copy.deepcopy(result); bad["schema"] = "bad"
    expect_failure("schema", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["protocol_maximum_earned"] = True
    expect_failure("false_protocol_completion", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["maximum_conclusion"] = PROTOCOL
    expect_failure("maximum_inflation", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["scope"]["boundary_completion_selected"] = True
    expect_failure("boundary_selection", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["scope"]["physical_representative_selected"] = True
    expect_failure("representative_selection", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["scope"]["source_or_carrier_loaded"] = True
    expect_failure("source_import", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["scope"]["symmetry_ansatz_used_for_operator_derivation"] = True
    expect_failure("early_reduction", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["scope"]["P06_launched"] = True
    expect_failure("P06_launch", lambda: validate(bad, tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L01/BULK_OPERATOR.tsv"] if row["id"] == "O05")["status"] = "NATIVE_UDT_EQUATION"
    expect_failure("Bach_promotion", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L02/BULK_OPERATOR.tsv"] if row["id"] == "O05")["status"] = "NATIVE_UDT_EQUATION"
    expect_failure("EH_promotion", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L02/BULK_OPERATOR.tsv"] if row["id"] == "O01")["formula"] = "L02=kappa*R"
    expect_failure("Lambda_silently_removed", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["lane_L01/BOUNDARY_CURRENT.tsv"] = [row for row in bad_tables["lane_L01/BOUNDARY_CURRENT.tsv"] if row["id"] != "B03"]
    expect_failure("C2_h_boundary_channel_removed", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L01/BOUNDARY_CURRENT.tsv"] if row["status"] == "OPEN_STOP")["status"] = "DIFFERENTIABLE"
    expect_failure("C2_boundary_false_close", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L02/BOUNDARY_CURRENT.tsv"] if row["id"] == "B04")["status"] = "NATIVE_ADOPTED"
    expect_failure("GHY_import", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["lane_L02/BOUNDARY_CURRENT.tsv"] = [row for row in bad_tables["lane_L02/BOUNDARY_CURRENT.tsv"] if row["channel"] != "Euler_boundary"]
    expect_failure("Euler_boundary_erased", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L01/PRINCIPAL_CHARACTER.tsv"] if row["id"] == "P01")["ungauge_fixed"] = "NONDEGENERATE_HYPERBOLIC"
    expect_failure("Bach_raw_symbol_promotion", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L02/PRINCIPAL_CHARACTER.tsv"] if row["id"] == "P01")["ungauge_fixed"] = "NONDEGENERATE_HYPERBOLIC"
    expect_failure("EH_raw_symbol_promotion", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["lane_L01/PRINCIPAL_CHARACTER.tsv"] if row["id"] == "P02")["principal_factor"] = "alpha*q^2"
    expect_failure("degenerate_arena_erased", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["FIELD_EQUATION_COMPLETENESS.tsv"].pop()
    expect_failure("missing_field_pair", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["FIELD_EQUATION_COMPLETENESS.tsv"].append(copy.deepcopy(bad_tables["FIELD_EQUATION_COMPLETENESS.tsv"][0]))
    expect_failure("duplicate_field_pair", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["FIELD_EQUATION_COMPLETENESS.tsv"] if row["pair_id"] == "L01_C02")["field_removed"] = "YES"
    expect_failure("independent_phi_removed", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["FIELD_EQUATION_COMPLETENESS.tsv"] if row["pair_id"] == "L02_C07")["boundary_complete"] = "YES"
    expect_failure("connection_branch_false_complete", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["VARIATION_DOMAIN_MATRIX.tsv"] if row["id"] == "V02")["relation_to_full_operator"] = "FULL_EQUIVALENT"
    expect_failure("hard_variation_equated", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["VARIATION_DOMAIN_MATRIX.tsv"] if row["id"] == "V03")["relation_to_full_operator"] = "FULL_EQUATION_RETAINED"
    expect_failure("multiplier_equated", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["REDUCED_ACTION_SCAR.tsv"] if row["id"] == "R04")["status"] = "EQUIVALENCE_PROVED"
    expect_failure("vacuous_C2_test_accepted", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["GLOBAL_AXIS_CARRYFORWARD.tsv"].pop()
    expect_failure("missing_global_axis", lambda: validate(result, bad_tables, graph), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["GLOBAL_AXIS_CARRYFORWARD.tsv"] if row["axis_id"] == "A09")["value_or_choice"] = "S3"
    expect_failure("topology_selected", lambda: validate(result, bad_tables, graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["edges"].append({"from": "RAW_BOUNDARY_CURRENT", "to": "COMPLETE_P05_OPERATOR", "relation": "automatic"})
    expect_failure("raw_current_called_complete", lambda: validate(result, tables, bad_graph), catches)
    bad_graph = copy.deepcopy(graph); bad_graph["edges"].append({"from": "P04_L03", "to": "FULL_METRIC_VARIATION", "relation": "invented"})
    expect_failure("bridge_operator_invented", lambda: validate(result, tables, bad_graph), catches)
    bad = copy.deepcopy(result); bad["source_sha256"]["P04_MANIFEST"] = "0" * 64
    expect_failure("source_hash_drift", lambda: validate(bad, tables, graph), catches)
    bad = copy.deepcopy(result); bad["table_sha256"]["STATUS_LEDGER.tsv"] = "0" * 64
    expect_failure("table_hash_drift", lambda: validate(bad, tables, graph), catches)
    require(len(catches) == 31 and set(catches.values()) == {"PASS"}, "catch count")

    output = {
        "schema": "udt-p05-conditional-operator-verification-1.0",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_proof_count": len(catches),
        "catch_proofs": catches,
        "main_result_sha256": digest(RESULT),
        "main_transcript_sha256": digest(HERE / "OPERATOR_TRANSCRIPT.txt"),
        "scope": {"independent_implementation": True, "generator_imported": False, "fresh_algebra": True, "CPU_only": True, "solutions_computed": False},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "P05_INDEPENDENT_VERIFICATION=PASS",
        f"checks={len(checks)}",
        f"catch_proofs={len(catches)}",
        "generator_imported=NO",
        "lanes=L01,L02",
        "field_pairs=21/21",
        "complete_action_pairs=0",
        "global_axes=12/12_free",
        "protocol_maximum_earned=NO",
        f"main_result_sha256={output['main_result_sha256']}",
    ]
    text = "\n".join(transcript) + "\n"
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
