#!/usr/bin/env python3
"""Fail-closed verifier for the basic versus universal-query residual audit."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(eq, residuals, atlas, controls, variations, global_rows, founding, status, premises, authority, sources) -> None:
    assert [row["equivalence_id"] for row in eq] == [f"E{i:02d}" for i in range(1, 8)]
    assert len({row["equivalence_id"] for row in eq}) == 7
    assert [row["residual_id"] for row in residuals] == [f"R{i:02d}" for i in range(1, 9)]
    assert len({row["residual_id"] for row in residuals}) == 8
    assert [row["residual_id"] for row in atlas] == [f"R{i:02d}" for i in range(1, 9)]
    assert len({row["residual_id"] for row in atlas}) == 8
    by_r = {row["residual_id"]: row for row in atlas}
    assert by_r["R01"]["operator_basic_descent"] == "MIXED_SCALAR_BASIC__PROJECTOR_NONBASIC"
    assert by_r["R02"]["operator_basic_descent"] == "GENERICALLY_NO"
    assert by_r["R02"]["solution_set_descent"] == "YES_BY_UNIVERSAL_PREDICATE"
    assert by_r["R02"]["finite_local_tensor_reduction"] == "YES_ON_FINITE_ALGEBRAIC_REGULAR_DOMAIN"
    assert by_r["R02"]["linearized_variation_equivalence"] == "COEFFICIENT_MAP_YES__SQUARED_SCALARIZATION_NO"
    assert by_r["R03"]["finite_local_tensor_reduction"] == "NOT_GUARANTEED"
    assert by_r["R04"]["finite_local_tensor_reduction"] == "NO_IN_GENERAL"
    assert by_r["R04"]["global_metric_relation_reduction"] == "YES_GENUINELY_GLOBAL"
    assert by_r["R05"]["linearized_variation_equivalence"] == "CHAIN_RULE_REQUIRED"
    assert by_r["R06"]["linearized_variation_equivalence"] == "TANGENT_CONE_OR_INTERFACE_RULE_OPEN"
    assert by_r["R07"]["operator_basic_descent"] == "BASE_PART_BASIC__PAIR_POLARIZATION_NONBASIC"
    assert by_r["R07"]["boundary_stratified_equivalence"] == "OPEN_NOT_SELECTED"
    assert all(by_r["R08"][key] == "OPEN" for key in (
        "operator_basic_descent", "solution_set_descent", "finite_local_tensor_reduction",
        "finite_jet_natural_reduction", "linearized_variation_equivalence",
        "global_metric_relation_reduction", "boundary_stratified_equivalence",
    ))

    assert [row["control_id"] for row in controls] == [f"K{i:02d}" for i in range(1, 16)]
    by_k = {row["control_id"]: row for row in controls}
    assert by_k["K03"]["ruling"] == "BASIC_TRACEFREE_TENSOR_REDUCTION"
    assert by_k["K05"]["ruling"] == "ONE_BASIC_SCALAR_TOO_WEAK"
    assert by_k["K06"]["ruling"] == "UNIVERSAL_FAMILY_NOT_S_EQUAL_ZERO"
    assert by_k["K08"]["ruling"] == "ZERO_SET_ONLY_NOT_VARIATION_EQUIVALENT"
    assert by_k["K10"]["ruling"] == "SCALARIZATION_LOSES_FIRST_VARIATION"
    assert by_k["K14"]["ruling"] == "NOT_REDUCIBLE_TO_FINITE_LOCAL_METRIC_JETS_IN_GENERAL"
    assert by_k["K15"]["ruling"] == "DOWNSTREAM_COMPATIBILITY_ONLY"

    assert [row["variation_id"] for row in variations] == [f"V{i:02d}" for i in range(1, 9)]
    by_v = {row["variation_id"]: row for row in variations}
    assert by_v["V01"]["guard"] == "no independent delta_q"
    assert by_v["V03"]["status"] == "REJECT_AS_AUTOMATIC_REPLACEMENT"
    assert by_v["V04"]["variation_rule"] == "include DS_g chain term"
    assert by_v["V05"]["status"] == "OPEN"
    assert by_v["V08"]["status"] == "DERIVED_REGULAR__STRATIFIED_AT_DOMAIN_CHANGE"

    assert [row["control_id"] for row in global_rows] == [f"G{i:02d}" for i in range(1, 5)]
    by_g = {row["control_id"]: row for row in global_rows}
    assert by_g["G01"]["all_loop_trivial"] == "YES"
    assert by_g["G02"]["all_loop_trivial"] == "NO"
    assert by_g["G01"]["local_finite_jet_data"] == by_g["G02"]["local_finite_jet_data"]
    assert by_g["G03"]["all_loop_trivial"] == "NOT_SUFFICIENT_IN_GENERAL"
    assert by_g["G04"]["all_loop_trivial"] == "GENUINE_GLOBAL_METRIC_RELATION"

    assert [row["ruling_id"] for row in founding] == [f"F{i:02d}" for i in range(1, 7)]
    by_f = {row["ruling_id"]: row for row in founding}
    assert by_f["F01"]["remaining_open"] == "does not supply L(g,q)=0"
    assert by_f["F03"]["remaining_open"] == "does not choose residual functional or local/global class"
    assert by_f["F05"]["remaining_open"] == "does not choose residual or quantifier"
    assert by_f["F06"]["remaining_open"] == "no nontrivial native residual selected"

    assert [row["status_id"] for row in status] == [f"S{i:02d}" for i in range(1, 13)]
    by_s = {row["status_id"]: row for row in status}
    assert by_s["S02"]["status"] == "DERIVED_LOGICAL"
    assert by_s["S03"]["status"] == "DERIVED_FINITE_BASIC_TENSOR_REDUCTION"
    assert by_s["S04"]["status"] == "DERIVED_CONTROL"
    assert by_s["S08"]["status"] == "ADMISSIBLE_GENUINE_NOT_SELECTED"
    assert by_s["S09"]["status"] == "NOT_REQUIRED_FOR_UNIVERSAL_QUERY_ARCHITECTURE"
    assert by_s["S10"]["status"] == "CONDITIONAL_DOWNSTREAM_COMPATIBILITY_ANCHOR"

    assert [row["premise_id"] for row in premises] == [f"P{i:02d}" for i in range(1, 15)]
    by_p = {row["premise_id"]: row for row in premises}
    assert by_p["P03"]["status"] == "DERIVED_CONTAINER"
    assert by_p["P03"]["exclusion"] == "no physical section and no delta_q"
    assert by_p["P06"]["status"] == "OPEN_INACTIVE"
    assert by_p["P07"]["status"] == "ADMISSIBLE_NOT_SELECTED"
    assert by_p["P08"]["status"] == "OPEN"
    assert by_p["P10"]["status"] == "CONDITIONAL_OBSERVATIONAL_COMPATIBILITY_ANCHOR"

    assert [row["authority_id"] for row in authority] == [f"A{i:02d}" for i in range(1, 11)]
    by_a = {row["authority_id"]: row for row in authority}
    assert by_a["A01"]["status"] == "PROHIBITED_WITHOUT_FIELD_OWNERSHIP"
    assert by_a["A02"]["status"] == "NOT_SUPPLIED"
    assert by_a["A03"]["status"] == "NOT_SUPPLIED"
    assert by_a["A04"]["status"] == "NOT_SELECTED"
    assert by_a["A05"]["status"] == "NOT_SUPPLIED"
    assert by_a["A06"]["status"] == "NOT_SELECTED"
    assert by_a["A07"]["status"] == "NO"
    assert by_a["A08"]["status"] == "INACTIVE"
    assert by_a["A09"]["status"] == "NOT_DERIVED"
    assert by_a["A10"]["status"] == "NONE"

    assert len(sources) == len({row["path"] for row in sources}) == 26
    for row in sources:
        path = ROOT / row["path"]
        assert path.is_file()
        assert path.stat().st_size == int(row["size"])
        assert digest(path) == row["sha256"]


eq = table("EQUIVALENCE_NOTION_UNIVERSE.tsv")
residuals = table("RESIDUAL_CLASS_UNIVERSE.tsv")
atlas = table("REDUCTION_EQUIVALENCE_ATLAS.tsv")
controls = table("EXACT_CONTROL_LEDGER.tsv")
variations = table("VARIATION_EQUIVALENCE_LEDGER.tsv")
global_rows = table("GLOBAL_LOCAL_CONTROL.tsv")
founding = table("FOUNDATIONAL_RULING.tsv")
status = table("STATUS_LEDGER.tsv")
premises = table("PREMISE_LEDGER.tsv")
authority = table("AUTHORITY_BOUNDARY.tsv")
sources = table("SOURCE_MANIFEST.tsv")
validate(eq, residuals, atlas, controls, variations, global_rows, founding, status, premises, authority, sources)

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
assert production["status"] == independent["status"] == "PASS"
assert production["exact_checks"] == 54 and independent["exact_checks"] == 15
common = (
    "pair_values", "query_coefficient_rank", "query_coefficient_nullity", "query_kernel_generator",
    "strict_tracefree_control_trace", "strict_tracefree_control_pair_value",
    "universal_query_tangent_rank", "linear_basic_tangent_rank", "squared_basic_tangent_rank",
    "coefficient_tangent_rank", "squared_coefficient_gradient_rank_at_solution",
    "metric_dependent_query_total_derivative",
    "torus_loop_holonomy", "klein_loop_holonomy", "local_flat_jet_orders_compared",
    "sne_conditional_shape",
)
for key in common:
    assert production[key] == independent[key], key
assert production["trace_free_map_rank"] == production["stacked_query_tracefree_rank"] == 9
assert production["nonzero_metric_line_trace"] == "-4"

tree = ast.parse((HERE / "verify_universal_query_independent.py").read_text(encoding="utf-8"))
imports = {
    alias.name.split(".")[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.Import)
    for alias in node.names
} | {
    (node.module or "").split(".")[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.ImportFrom)
}
assert imports <= {"__future__", "json", "fractions", "pathlib"}
independent_text = (HERE / "verify_universal_query_independent.py").read_text(encoding="utf-8")
assert "derive_universal_query_residual" not in independent_text and "sympy" not in independent_text.lower()


def must_fail(catch_id, mutate):
    values = [deepcopy(item) for item in (
        eq, residuals, atlas, controls, variations, global_rows, founding, status, premises, authority, sources
    )]
    mutate(*values)
    try:
        validate(*values)
    except (AssertionError, KeyError, ValueError):
        return (catch_id, "REJECT", "PASS")
    raise AssertionError(f"catch did not fail: {catch_id}")


catches = []
catches.append(must_fail("C01_MISSING_EQUIVALENCE", lambda e, *_: e.pop()))
catches.append(must_fail("C02_DUPLICATE_EQUIVALENCE", lambda e, *_: e.append(deepcopy(e[0]))))
catches.append(must_fail("C03_MISSING_RESIDUAL_CLASS", lambda e, r, *_: r.pop()))
catches.append(must_fail("C04_DUPLICATE_RESIDUAL_CLASS", lambda e, r, *_: r.append(deepcopy(r[0]))))
catches.append(must_fail("C05_NONBASIC_FALSE_NO_SOLUTION_DESCENT", lambda e, r, a, *_: a[1].update(solution_set_descent="NO")))
catches.append(must_fail("C06_SOLUTION_DESCENT_FALSE_OPERATOR_BASIC", lambda e, r, a, *_: a[1].update(operator_basic_descent="YES")))
catches.append(must_fail("C07_FINITE_REDUCTION_FROM_INVARIANCE", lambda e, r, a, *_: a[2].update(finite_local_tensor_reduction="YES_ALWAYS")))
catches.append(must_fail("C08_ZERO_SET_IGNORES_TANGENT", lambda e, r, a, c, v, *_: v[2].update(status="ACCEPTED_EQUIVALENT")))
catches.append(must_fail("C09_QUERY_VARIED_AS_FIELD", lambda e, r, a, c, v, g, f, s, p, *_: p[2].update(exclusion="independent delta_q")))
catches.append(must_fail("C10_REALIZED_SECTION_INTRODUCED", lambda e, r, a, c, v, g, f, s, p, au, *_: au[1].update(status="DERIVED")))
catches.append(must_fail("C11_FIBER_MEASURE_INTRODUCED", lambda e, r, a, c, v, g, f, s, p, au, *_: au[2].update(status="DERIVED")))
catches.append(must_fail("C12_LOCAL_JETS_DECIDE_HOLONOMY", lambda e, r, a, c, v, g, *_: g[2].update(all_loop_trivial="SUFFICIENT")))
catches.append(must_fail("C13_QUOTIENT_PROMOTED_TO_UDT", lambda e, r, a, c, v, g, f, s, p, au, *_: au[3].update(status="SELECTED_UDT")))
catches.append(must_fail("C14_SINGULAR_UNIQUE_TANGENT", lambda e, r, a, c, v, *_: v[4].update(status="DERIVED_UNIQUE")))
catches.append(must_fail("C15_BOUNDARY_COLLAPSED", lambda e, r, a, *_: a[6].update(operator_basic_descent="ALL_BASIC")))
catches.append(must_fail("C16_SNE_SELECTS_RESIDUAL", lambda e, r, a, c, v, g, f, s, p, au, *_: au[6].update(status="YES")))
catches.append(must_fail("C17_CSN_ACTIVATED", lambda e, r, a, c, v, g, f, s, p, au, *_: au[7].update(status="ACTIVE")))
catches.append(must_fail("C18_PHYSICS_PROMOTED", lambda e, r, a, c, v, g, f, s, p, au, *_: au[8].update(status="DERIVED")))
catches.append(must_fail("C19_CONTROL_PROMOTED_PHYSICAL", lambda e, r, a, c, v, g, f, s, p, au, *_: au[9].update(status="UDT_LAW")))
catches.append(must_fail("C20_ESCAPE_REMOVED", lambda e, r, *_: r.pop(7)))
catches.append(must_fail("C21_STRICTNESS_FALSE_IRREDUCIBILITY", lambda e, r, a, c, v, g, f, s, *_: s[3].update(status="DERIVED_NOT_REDUCIBLE_TO_ANY_BASIC_TENSOR")))
catches.append(must_fail("C22_SCALARIZATION_FALSE_VARIATION", lambda e, r, a, c, *_: c[9].update(ruling="VARIATION_EQUIVALENT")))
assert len(catches) == 22
with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("catch_id", "expected", "observed"))
    writer.writerows(catches)

overall = {row["status_id"]: row for row in status}["S12"]["status"]
review_verdict = "NOT_RUN"
if (HERE / "FRESH_ADVERSARIAL_REVIEW_RESULT.json").exists():
    review = json.loads((HERE / "FRESH_ADVERSARIAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    review_verdict = review["verdict"]
    assert review_verdict in {"PASS", "PASS_WITH_CAVEATS", "ACCEPT_WITH_REQUIRED_REPAIRS"}
    assert review["files_modified_by_reviewer"] == 0
    assert digest(HERE / "FRESH_ADVERSARIAL_REVIEW.md") == review["review_output_sha256"]
    if overall.startswith("VERIFIED"):
        assert review.get("required_repairs", 0) == 0
else:
    assert overall == "PROVISIONAL_PENDING_FRESH_ADVERSARIAL_REVIEW"

result = {
    "status": "PASS" if overall.startswith("VERIFIED") else "PASS_PRE_REVIEW",
    "equivalence_notions": len(eq),
    "residual_classes": len(residuals),
    "control_rows": len(controls),
    "variation_rows": len(variations),
    "global_local_rows": len(global_rows),
    "foundational_rows": len(founding),
    "production_exact_checks": production["exact_checks"],
    "independent_exact_checks": independent["exact_checks"],
    "catch_proofs": len(catches),
    "frozen_sources": len(sources),
    "fresh_adversarial_review": review_verdict,
    "result": "UNIVERSAL_QUERY_OPERATOR_CAN_REMAIN_NONBASIC__SOLUTION_SET_DESCENDS__LOCAL_ALGEBRAIC_CONTROL_REDUCES_TO_BASIC_TENSOR__GLOBAL_PATH_CONTROL_NOT_FINITE_LOCAL__ARCHITECTURE_NOT_SELECTED",
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
