#!/usr/bin/env python3
"""Independent exact verifier for the complete-metric realization map."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_MAXIMUM = (
    "REGISTERED_COMPLETE_METRIC_REALIZATION_LAYERS_MAPPED__ANY_EXISTING_"
    "NATIVE_JOIN_IDENTIFIED_WITH_EXACT_SCOPE__MISSING_JOINS_REMAIN_OPEN"
)
EXPECTED_DIGESTS = {
    "layers": "b34f26a5b48ff6a17a66114731f28f0e89ac8cb31999d27d88f0d82395e36dc5",
    "joins": "c28b16de58f401e5f5839ae3adddf2e6b528a859e508d314cde12c1d8ea113cc",
    "bootstrap": "8566e4fb272fb328a7dfd8222c4e85ef1f255c1545a483a03211547951a189a7",
    "statuses": "45b2398e02f32ef410e4172368d4e3d850142da8e6b1b3142dbb7486c762c473",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def verify_sources() -> int:
    records = []
    for line in (HERE / "SOURCE_MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            raise AssertionError(f"source mismatch: {relative}")
        records.append(relative)
    if len(records) != 47 or len(set(records)) != 47:
        raise AssertionError("source identity/count")
    return len(records)


def read_rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_rows(relative: str, key: str) -> dict[str, dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        records = list(csv.DictReader(handle, delimiter="\t"))
    indexed = {row[key]: row for row in records}
    if len(indexed) != len(records):
        raise AssertionError(f"duplicate source identity: {relative}")
    return indexed


def source_semantics() -> dict[str, object]:
    """Re-derive load-bearing statuses from the frozen source records."""
    ownership = source_rows(
        "udt_reciprocal_subbundle_ownership_audit_2026-07-22/"
        "STATUS_LEDGER.tsv",
        "id",
    )
    null_section = source_rows(
        "null_section_hopfion_metric_audit_2026-07-19/"
        "STATUS_LEDGER.tsv",
        "claim_id",
    )
    toric = source_rows(
        "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
        "claim_id",
    )
    topology = source_rows(
        "native_hopfion_topology_audit_2026-07-19/"
        "TOPOLOGY_STATUS_LEDGER.tsv",
        "claim_id",
    )
    assembly = source_rows(
        "udt_global_metric_assembly_atlas_2026-07-22/STATUS_LEDGER.tsv",
        "claim_id",
    )
    action = source_rows(
        "native_action_final_adjudication_2026-07-18/"
        "FINAL_STATUS_LEDGER.tsv",
        "id",
    )
    bridge = source_rows(
        "udt_coframe_hopf_bridge_audit_2026-07-23/STATUS_LEDGER.tsv",
        "id",
    )
    representative = source_rows(
        "boundary_bootstrap_representative_selector_audit_2026-07-19/"
        "STATUS_LEDGER.tsv",
        "id",
    )
    correction_text = re.sub(
        r"\s+",
        " ",
        (
        ROOT
        / "udt_metric_to_frontier_reference_2026-07-22/"
        "REFERENCE_CORRECTION_LAYER.md"
        ).read_text(encoding="utf-8"),
    )
    required_realization_sentence = (
        "currently supply no operator, relation, functional, fixed-point map, "
        "boundary problem, codomain, or solution/uniqueness criterion"
    )

    checks = {
        "reciprocal_subbundle_not_selected": (
            ownership["S13"]["status"] == "NOT_DERIVED"
            and ownership["S14"]["status"] == "NOT_DERIVED"
        ),
        "celestial_fiber_conditional": (
            null_section["N03"]["status"] == "CONDITIONAL_DERIVED_FIBER"
        ),
        "fiber_does_not_select_section": (
            null_section["N04"]["status"]
            == "DIRECT_UNFRAMED_IDENTITY_BLOCKED"
        ),
        "component_hopf_not_frame_invariant": (
            null_section["N05"]["status"] == "NOT_FRAME_INVARIANT"
        ),
        "global_quotient_not_selected": (
            assembly["G09"]["status"] == "OPEN_NOT_SELECTED"
        ),
        "conditional_toric_completion_only": (
            toric["T06"]["status"]
            == "S3_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES"
            and toric["T16"]["status"] == "NO_TOPOLOGY_RANKING_LAW"
        ),
        "bootstrap_representative_not_supplied": (
            representative["S06"]["status"] == "OPEN_NOT_SUPPLIED"
            and representative["S13"]["status"]
            == "SELECTOR_NOT_FOUND_IN_CURRENT_FOUNDATION"
        ),
        "realization_operation_absent": (
            required_realization_sentence in correction_text
        ),
        "chart_bridge_not_native_carrier": (
            bridge["S11"]["status"] == "EXACT_CONDITIONAL"
            and bridge["S14"]["status"] == "OPEN"
        ),
        "hopfion_only_conditional_static": (
            topology["T10"]["status"]
            == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
        ),
        "native_action_source_mass_open": (
            action["S22"]["status"] == "OPEN"
            and action["S23"]["status"] == "OPEN"
            and action["S25"]["status"] == "OPEN"
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError("source semantic replay: " + ",".join(failed))
    return {
        "checks": checks,
        "passed": len(checks),
        "total": len(checks),
        "method": "DIRECT_FROZEN_SOURCE_LEDGER_AND_REPORT_REPLAY",
    }


def row_digest(records: list[dict[str, str]]) -> str:
    payload = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def subtract(left, right):
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def independent_controls() -> dict[str, object]:
    eta = [
        [F(-1), F(0), F(0), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    boost = [
        [F(13, 12), F(5, 12), F(0), F(0)],
        [F(5, 12), F(13, 12), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    metric_after = multiply(multiply(transpose(boost), eta), boost)
    if metric_after != eta:
        raise AssertionError("independent Lorentz metric control")
    selected = [
        [F(1), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
    ]
    selected_residual = subtract(
        multiply(multiply(transpose(boost), selected), boost), selected
    )
    if selected_residual == [[F(0)] * 4 for _ in range(4)]:
        raise AssertionError("coframe-label counterexample vanished")

    # Independent exact rational points on the celestial sphere.
    points = (
        (F(3, 5), F(4, 5), F(0)),
        (F(12, 13), F(0), F(5, 13)),
        (F(0), F(8, 17), F(15, 17)),
    )
    if any(sum(item * item for item in point) != 1 for point in points):
        raise AssertionError("independent null-sphere anchors")

    # Independent rational samples of the polynomial Hopf norm identity.
    samples = (
        (F(1), F(2), F(3), F(4)),
        (F(2), F(-1), F(5), F(3)),
        (F(3, 2), F(2, 3), F(-4, 5), F(7, 4)),
    )
    for x1, x2, x3, x4 in samples:
        radius2 = x1*x1 + x2*x2 + x3*x3 + x4*x4
        hopf = (
            2 * (x1*x3 + x2*x4),
            2 * (x2*x3 - x1*x4),
            x1*x1 + x2*x2 - x3*x3 - x4*x4,
        )
        if sum(item * item for item in hopf) != radius2 * radius2:
            raise AssertionError("independent Hopf norm anchor")
    return {
        "lorentz_metric_anchor": "PASS",
        "labeled_leg_changes": True,
        "celestial_rational_points": len(points),
        "hopf_polynomial_samples": len(samples),
    }


def validate(result, layers, joins, bootstrap, statuses, semantics) -> None:
    if result["schema"] != "udt-complete-metric-realization-zoomout-v1":
        raise AssertionError("schema")
    if result["source_count"] != 47 or result["new_physical_premises"] != 0:
        raise AssertionError("source/premise count")
    if result["counts"] != {
        "bootstrap_ingredients": 8,
        "joins": 12,
        "layers": 12,
        "native_end_to_end_bridges": 0,
        "open_or_obstructed_joins": 7,
        "status_rows": 14,
    }:
        raise AssertionError("counts")
    if len(layers) != 12 or len({row["id"] for row in layers}) != 12:
        raise AssertionError("layer identities")
    if len(joins) != 12 or len({row["id"] for row in joins}) != 12:
        raise AssertionError("join identities")
    if len(bootstrap) != 8 or len(
        {row["ingredient"] for row in bootstrap}
    ) != 8:
        raise AssertionError("bootstrap identities")
    if len(statuses) != 14 or len({row["id"] for row in statuses}) != 14:
        raise AssertionError("status identities")
    observed = {
        "layers": row_digest(layers),
        "joins": row_digest(joins),
        "bootstrap": row_digest(bootstrap),
        "statuses": row_digest(statuses),
    }
    if observed != EXPECTED_DIGESTS:
        raise AssertionError("semantic row contract")
    if result["maximum_conclusion"] != EXPECTED_MAXIMUM:
        raise AssertionError("maximum conclusion")
    if semantics["passed"] != semantics["total"] or semantics["total"] != 11:
        raise AssertionError("source semantic replay")
    if any(result["unification_tests"][key] for key in (
        "single_frame_independent_reciprocal_object_supplies_all_joins",
        "single_registered_realization_rule_supplies_all_joins",
    )):
        raise AssertionError("failed-closed unification promoted")

    by_layer = {row["id"]: row for row in layers}
    by_join = {row["id"]: row for row in joins}
    by_status = {row["id"]: row for row in statuses}
    by_bootstrap = {row["ingredient"]: row for row in bootstrap}
    if by_layer["L05"]["survival"] != "NOT_FRAME_INVARIANT":
        raise AssertionError("component Hopf claim promoted")
    if by_layer["L03"]["survival"] != "DERIVED_CONDITIONAL":
        raise AssertionError("null fiber status")
    if by_join["J04"]["edge_status"] != "OPEN":
        raise AssertionError("fiber-to-section promoted")
    if by_join["J08"]["edge_status"] != "OPEN":
        raise AssertionError("global completion promoted")
    if by_join["J09"]["edge_status"] != "OPEN_NO_OPERATION":
        raise AssertionError("realization promoted")
    if by_status["S11"]["status"] != "OPEN":
        raise AssertionError("carrier emergence promoted")
    if by_status["S12"]["status"] != "OPEN":
        raise AssertionError("native matter promoted")
    if by_bootstrap["operation_or_relation"][
        "registered_supply"
    ] != "ABSENT_IN_AUDITED_SOURCES":
        raise AssertionError("bootstrap operation invented")
    if by_bootstrap["uniqueness_or_ranking"][
        "registered_supply"
    ] != "ABSENT_IN_AUDITED_SOURCES":
        raise AssertionError("bootstrap selector invented")
    if result["dependency_layers"] != [
        "REPRESENTATION_DESCENT",
        "GLOBAL_COMPLETION",
        "REALIZATION",
        "DEFORMATION_DYNAMICS_AND_MATTER",
    ]:
        raise AssertionError("dependency layers")
    if result["ordering_ruling"] != {
        "controlling_first_conceptual_priority": "SOURCE_ONLY_REALIZATION_OPERATOR_AUDIT",
        "different_mathematical_types": True,
        "one_future_law_may_close_multiple_joins_jointly": True,
        "strict_total_order_derived": False,
        "this_package_completed_that_source_census": True,
    }:
        raise AssertionError("ordering ruling")


def expect_failure(identifier, callback):
    try:
        callback()
    except (AssertionError, KeyError):
        return {
            "catch_id": identifier,
            "result": "PASS",
            "scope": "SEMANTIC_MUTATION",
        }
    raise AssertionError(f"mutation passed: {identifier}")


def mutation_catches(result, layers, joins, bootstrap, statuses):
    catches = []

    def mutated(mutator):
        r = copy.deepcopy(result)
        l = copy.deepcopy(layers)
        j = copy.deepcopy(joins)
        b = copy.deepcopy(bootstrap)
        s = copy.deepcopy(statuses)
        mutator(r, l, j, b, s)
        validate(r, l, j, b, s, source_semantics())

    mutations = (
        ("M01_SOURCE_COUNT", lambda r,l,j,b,s: r.__setitem__("source_count", 46)),
        ("M02_DROP_LAYER", lambda r,l,j,b,s: l.pop()),
        ("M03_DUPLICATE_JOIN", lambda r,l,j,b,s: j.append(copy.deepcopy(j[0]))),
        ("M04_DROP_BOOTSTRAP", lambda r,l,j,b,s: b.pop()),
        ("M05_DROP_STATUS", lambda r,l,j,b,s: s.pop()),
        ("M06_NEW_PREMISE", lambda r,l,j,b,s: r.__setitem__("new_physical_premises", 1)),
        ("M07_PROMOTE_CHART", lambda r,l,j,b,s: next(x for x in l if x["id"]=="L02").__setitem__("survival", "DERIVED_PHYSICAL")),
        ("M08_SELECT_NULL_RAY", lambda r,l,j,b,s: next(x for x in j if x["id"]=="J04").__setitem__("edge_status", "DERIVED")),
        ("M09_FRAME_HOPF", lambda r,l,j,b,s: next(x for x in l if x["id"]=="L05").__setitem__("survival", "DERIVED")),
        ("M10_SELECT_COMPLETION", lambda r,l,j,b,s: next(x for x in j if x["id"]=="J08").__setitem__("edge_status", "DERIVED")),
        ("M11_BOOTSTRAP_OPERATION", lambda r,l,j,b,s: next(x for x in b if x["ingredient"]=="operation_or_relation").__setitem__("registered_supply", "DERIVED")),
        ("M12_BOOTSTRAP_UNIQUENESS", lambda r,l,j,b,s: next(x for x in b if x["ingredient"]=="uniqueness_or_ranking").__setitem__("registered_supply", "DERIVED")),
        ("M13_REALIZATION", lambda r,l,j,b,s: next(x for x in j if x["id"]=="J09").__setitem__("edge_status", "DERIVED")),
        ("M14_CARRIER_EMERGENCE", lambda r,l,j,b,s: next(x for x in s if x["id"]=="S11").__setitem__("status", "DERIVED")),
        ("M15_NATIVE_MATTER", lambda r,l,j,b,s: next(x for x in s if x["id"]=="S12").__setitem__("status", "DERIVED")),
        ("M16_COLLAPSE_LAYERS", lambda r,l,j,b,s: r.__setitem__("dependency_layers", ["ONE_JOIN"])),
        ("M17_UNIFY_OBJECT", lambda r,l,j,b,s: r["unification_tests"].__setitem__("single_frame_independent_reciprocal_object_supplies_all_joins", True)),
        ("M18_UNIFY_REALIZATION", lambda r,l,j,b,s: r["unification_tests"].__setitem__("single_registered_realization_rule_supplies_all_joins", True)),
        ("M19_END_TO_END", lambda r,l,j,b,s: r["counts"].__setitem__("native_end_to_end_bridges", 1)),
        ("M20_MAXIMUM", lambda r,l,j,b,s: r.__setitem__("maximum_conclusion", "NATIVE_MATTER_DERIVED")),
        ("M21_STRICT_ORDER", lambda r,l,j,b,s: r["ordering_ruling"].__setitem__("strict_total_order_derived", True)),
    )
    for identifier, mutator in mutations:
        catches.append(
            expect_failure(
                identifier,
                lambda mutator=mutator: mutated(mutator),
            )
        )
    return catches


def main() -> None:
    sources = verify_sources()
    controls = independent_controls()
    semantics = source_semantics()
    result = json.loads((HERE / "RESULT.json").read_text())
    layers = read_rows("LAYER_SURVIVAL_LEDGER.tsv")
    joins = read_rows("JOIN_GRAPH.tsv")
    bootstrap = read_rows("BOOTSTRAP_REALIZATION_MATRIX.tsv")
    statuses = read_rows("STATUS_LEDGER.tsv")
    validate(result, layers, joins, bootstrap, statuses, semantics)
    catches = mutation_catches(result, layers, joins, bootstrap, statuses)
    with (HERE / "CATCH_PROOFS.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["catch_id", "result", "scope"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)
    output = {
        "schema": "udt-complete-metric-realization-independent-v1",
        "status": "PASS",
        "sources_checked": sources,
        "independent_controls": controls,
        "direct_source_semantic_replay": semantics,
        "row_digests": EXPECTED_DIGESTS,
        "mutation_catches": {
            "passed": len(catches),
            "total": len(catches),
        },
        "maximum_conclusion_confirmed": EXPECTED_MAXIMUM,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
