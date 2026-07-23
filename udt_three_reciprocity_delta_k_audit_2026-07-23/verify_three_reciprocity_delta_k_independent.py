#!/usr/bin/env python3
"""Independent stdlib verification of the three-reciprocity audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def eye() -> list[list[F]]:
    return [[F(1), F(0)], [F(0), F(1)]]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] - b[i][j] for j in range(2)] for i in range(2)]


def scale(value: F, a: list[list[F]]) -> list[list[F]]:
    return [[value * item for item in row] for row in a]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(2)), F(0))
            for j in range(2)
        ]
        for i in range(2)
    ]


def inv(a: list[list[F]]) -> list[list[F]]:
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if determinant == 0:
        raise AssertionError("singular control")
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def compose(left: F, right: F) -> F:
    denominator = 1 + left * right
    if denominator == 0:
        raise ZeroDivisionError("Xmax boundary composition undefined")
    return (left + right) / denominator


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for piece in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(piece)
    return value.hexdigest()


def read_json(name: str) -> dict[str, object]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_covariance() -> int:
    controls = [
        (
            [[F(2), F(1)], [F(1), F(1)]],
            [[F(3), F(-2)], [F(5), F(1)]],
        ),
        (
            [[F(1), F(3)], [F(-2), F(1)]],
            [[F(-1), F(4)], [F(2), F(3)]],
        ),
        (
            [[F(4), F(-1)], [F(3), F(2)]],
            [[F(7), F(2)], [F(-3), F(5)]],
        ),
    ]
    reference = scale(F(-1), eye())
    for transform, delta in controls:
        inverse = inv(transform)
        lhs = mul(mul(transform, add(reference, delta)), inverse)
        rhs = add(
            mul(mul(transform, reference), inverse),
            mul(mul(transform, delta), inverse),
        )
        if lhs != rhs:
            raise AssertionError("covariance decomposition")

    central = scale(F(7, 3), eye())
    for transform, _ in controls:
        if mul(mul(transform, central), inv(transform)) != central:
            raise AssertionError("central survivor")
    if central == [[F(0), F(0)], [F(0), F(0)]]:
        raise AssertionError("vacuous central survivor")

    mirror = [[F(0), F(1)], [F(1), F(0)]]
    generator = [[F(-1), F(0)], [F(0), F(1)]]
    if mul(mul(mirror, generator), mirror) != scale(F(-1), generator):
        raise AssertionError("reciprocal reversal")
    if mul(mul(mirror, reference), mirror) != reference:
        raise AssertionError("reference source reversal")
    return len(controls) + 3


def verify_xmax_group() -> int:
    controls = [
        (F(1, 5), F(2, 7), F(-1, 3)),
        (F(-2, 5), F(1, 4), F(3, 8)),
        (F(3, 10), F(-1, 6), F(2, 9)),
    ]
    for x, y, z in controls:
        if compose(compose(x, y), z) != compose(x, compose(y, z)):
            raise AssertionError("associativity")
        if compose(F(0), x) != x:
            raise AssertionError("identity")
        if compose(x, -x) != 0:
            raise AssertionError("inverse")
        character_xy = (1 - compose(x, y)) / (1 + compose(x, y))
        character_product = ((1 - x) / (1 + x)) * ((1 - y) / (1 + y))
        if character_xy != character_product:
            raise AssertionError("multiplicative character")

    try:
        compose(F(1), F(-1))
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("opposite endpoints falsely composable")
    return len(controls) * 4 + 1


def b_value(lam: F, u: F, t: F) -> F:
    denominator = lam + u * t
    if denominator == 0:
        raise AssertionError("singular flow control")
    return lam * (u + lam * t) / denominator


def db_dp(lam: F, u: F, t: F) -> F:
    denominator = lam + u * t
    db_dt = lam * (lam * lam - u * u) / (denominator * denominator)
    dt_dp = lam * (1 - t * t)
    return db_dt * dt_dp


def verify_lambda_flow() -> int:
    count = 0
    controls = [
        (F(1), F(1, 2), F(1, 3)),
        (F(2), F(3, 2), F(2, 5)),
        (F(3), F(4), F(-1, 4)),
        (F(5, 2), F(1), F(3, 7)),
    ]
    for lam, shear, t in controls:
        plus = b_value(lam, shear, t)
        minus = b_value(lam, -shear, t)
        if db_dp(lam, shear, t) + plus * plus - lam * lam != 0:
            raise AssertionError("positive eigen Riccati")
        if db_dp(lam, -shear, t) + minus * minus - lam * lam != 0:
            raise AssertionError("negative eigen Riccati")
        area = (plus + minus) / 2
        shape = ((plus - minus) / 2) ** 2
        expected_area = (
            lam * t * (lam * lam - shear * shear)
            / (lam * lam - shear * shear * t * t)
        )
        expected_shape = (
            lam**4 * shear * shear * (1 - t * t) ** 2
            / (lam * lam - shear * shear * t * t) ** 2
        )
        if area != expected_area or shape != expected_shape:
            raise AssertionError("area/shape formula")
        count += 4

    for lam in (F(1), F(2), F(3), F(5, 2)):
        for t in (F(1, 5), F(2, 3)):
            plus = b_value(lam, lam, t)
            minus = b_value(lam, -lam, t)
            area = (plus + minus) / 2
            shape = ((plus - minus) / 2) ** 2
            if area != 0 or shape != lam * lam:
                raise AssertionError("matched two-seal flow")
            count += 2
    return count


def expect_rejection(
    mutation: str,
    covariance: dict[str, object],
    xmax: dict[str, object],
    flow: dict[str, object],
    result: dict[str, object],
) -> bool:
    if mutation == "covariance_promoted_to_necessity":
        return covariance["zero_is_forced_by_covariance"] is False
    if mutation == "central_survivor_deleted":
        return covariance["central_survivor_nonzero_for_mu_nonzero"] is True
    if mutation == "c_anchor_dropped":
        return covariance["c_retained_symbolically"] is True
    if mutation == "reversal_demotes_reference_source":
        return covariance["mirror_action"] == "L->-L;K_rec->K_rec"
    if mutation == "endpoint_flat_bulk_countermodel_deleted":
        return covariance["endpoint_flat_survivor"] == "mu*(1-xi^2)^2*I"
    if mutation == "Xmax_law_promoted_to_unique":
        return xmax["status"] == "CHOSE_CONDITIONAL_NOT_UNIQUE"
    if mutation == "position_field_join_silently_inserted":
        return xmax["position_field_join"] == "OPEN_NOT_CERTIFIED"
    if mutation == "opposite_endpoints_promoted_to_group_pair":
        return xmax["opposite_endpoints_composable"] is False
    if mutation == "endpoints_promoted_to_regular_seals":
        return xmax["endpoints_are_regular_mirror_seals"] is False
    if mutation == "lambda_set_to_one":
        return flow["two_seals_force_lambda_one"] is False
    if mutation == "lambda_two_witness_missing":
        return any(
            row["lambda"] == "2" and row["S_shape"] == "4"
            for row in flow["witnesses"]
        )
    if mutation == "lambda_three_witness_missing":
        return any(
            row["lambda"] == "3" and row["S_shape"] == "9"
            for row in flow["witnesses"]
        )
    if mutation == "conditional_premises_hidden":
        return len(flow["added_control_premises"]) == 6
    if mutation == "route_missing_or_duplicate":
        routes = read_tsv("ROUTE_RULING_MATRIX.tsv")
        return len(routes) == 14 and len({row["route_id"] for row in routes}) == 14
    if mutation == "native_derivation_false_positive":
        return result["native_closure"] is False
    if mutation == "two_seal_premise_promoted_native":
        return "parallel_screen" in flow["added_control_premises"]
    if mutation == "source_sign_hidden":
        return "negative_constant_source_sign" in flow["added_control_premises"]
    if mutation == "maximum_conclusion_overstated":
        return "LAMBDA_EQUALS_ONE_REMAINS_OPEN" in result["maximum_conclusion"]
    raise AssertionError(f"unknown mutation: {mutation}")


def verify_mutations() -> list[dict[str, str]]:
    covariance = read_json("RECIPROCITY_COVARIANCE.json")
    xmax = read_json("XMAX_GROUP_ENDPOINTS.json")
    flow = read_json("CONSTANT_LAMBDA_RICCATI.json")
    result = read_json("RESULT.json")
    registered = read_tsv("CATCH_PROOFS.tsv")
    if len(registered) != 18:
        raise AssertionError("catch count")
    outcomes = []
    for row in registered:
        clean = expect_rejection(
            row["mutation"], covariance, xmax, flow, result
        )
        if not clean:
            raise AssertionError(f"clean catch failed: {row['catch_id']}")

        mutated_covariance = copy.deepcopy(covariance)
        mutated_xmax = copy.deepcopy(xmax)
        mutated_flow = copy.deepcopy(flow)
        mutated_result = copy.deepcopy(result)
        mutation = row["mutation"]
        if mutation == "covariance_promoted_to_necessity":
            mutated_covariance["zero_is_forced_by_covariance"] = True
        elif mutation == "central_survivor_deleted":
            mutated_covariance["central_survivor_nonzero_for_mu_nonzero"] = False
        elif mutation == "c_anchor_dropped":
            mutated_covariance["c_retained_symbolically"] = False
        elif mutation == "reversal_demotes_reference_source":
            mutated_covariance["mirror_action"] = "L->-L;K_rec->-K_rec"
        elif mutation == "endpoint_flat_bulk_countermodel_deleted":
            mutated_covariance["endpoint_flat_survivor"] = "NONE"
        elif mutation == "Xmax_law_promoted_to_unique":
            mutated_xmax["status"] = "DERIVED_UNIQUE"
        elif mutation == "position_field_join_silently_inserted":
            mutated_xmax["position_field_join"] = "DERIVED"
        elif mutation == "opposite_endpoints_promoted_to_group_pair":
            mutated_xmax["opposite_endpoints_composable"] = True
        elif mutation == "endpoints_promoted_to_regular_seals":
            mutated_xmax["endpoints_are_regular_mirror_seals"] = True
        elif mutation == "lambda_set_to_one":
            mutated_flow["two_seals_force_lambda_one"] = True
        elif mutation == "lambda_two_witness_missing":
            mutated_flow["witnesses"] = [
                witness for witness in mutated_flow["witnesses"]
                if witness["lambda"] != "2"
            ]
        elif mutation == "lambda_three_witness_missing":
            mutated_flow["witnesses"] = [
                witness for witness in mutated_flow["witnesses"]
                if witness["lambda"] != "3"
            ]
        elif mutation == "conditional_premises_hidden":
            mutated_flow["added_control_premises"] = []
        elif mutation == "native_derivation_false_positive":
            mutated_result["native_closure"] = True
        elif mutation == "two_seal_premise_promoted_native":
            mutated_flow["added_control_premises"].remove("parallel_screen")
        elif mutation == "source_sign_hidden":
            mutated_flow["added_control_premises"].remove(
                "negative_constant_source_sign"
            )
        elif mutation == "maximum_conclusion_overstated":
            mutated_result["maximum_conclusion"] = "NATIVE_CLOSURE"

        if mutation == "route_missing_or_duplicate":
            routes = read_tsv("ROUTE_RULING_MATRIX.tsv")
            caught = len(routes[:-1]) != 14
        else:
            caught = not expect_rejection(
                mutation,
                mutated_covariance,
                mutated_xmax,
                mutated_flow,
                mutated_result,
            )
        if not caught:
            raise AssertionError(f"mutation escaped: {row['catch_id']}")
        outcomes.append(
            {
                "catch_id": row["catch_id"],
                "mutation": mutation,
                "result": "PASS_REJECTED",
            }
        )
    return outcomes


def verify_source_hashes() -> int:
    rows = read_tsv("SOURCE_LINEAGE.tsv")
    if len(rows) != 20:
        raise AssertionError("source count")
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"]:
            raise AssertionError(f"source drift: {row['path']}")
    return len(rows)


def main() -> None:
    covariance_checks = verify_covariance()
    xmax_checks = verify_xmax_group()
    flow_checks = verify_lambda_flow()
    mutation_outcomes = verify_mutations()
    source_checks = verify_source_hashes()

    result = read_json("RESULT.json")
    routes = read_tsv("ROUTE_RULING_MATRIX.tsv")
    statuses = read_tsv("STATUS_LEDGER.tsv")
    counters = read_tsv("COUNTERFAMILY_ATLAS.tsv")
    if result["native_closure"] is not False:
        raise AssertionError("native closure overclaim")
    if len(routes) != 14 or len(statuses) != 14 or len(counters) != 4:
        raise AssertionError("ledger coverage")
    if any(row["ruling"] == "DERIVES_MISSING_PREMISE" for row in routes):
        raise AssertionError("route overclaim")

    output = {
        "schema": "udt-three-reciprocity-independent-verification-1.0",
        "method": "stdlib_Fraction_no_production_import",
        "covariance_checks": covariance_checks,
        "xmax_group_checks": xmax_checks,
        "lambda_flow_checks": flow_checks,
        "source_hash_checks": source_checks,
        "route_checks": len(routes),
        "status_checks": len(statuses),
        "counterfamily_checks": len(counters),
        "catch_count": len(mutation_outcomes),
        "catch_pass_count": len(mutation_outcomes),
        "all_checks_pass": True,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
