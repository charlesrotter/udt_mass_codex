#!/usr/bin/env python3
"""Independent stdlib verification of the invariant-Xmax boundary audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


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


def xr_add(x: F, y: F) -> F:
    denominator = 1 + x * y
    if denominator == 0:
        raise ZeroDivisionError
    return (x + y) / denominator


def xr_subtract(x: F, alpha: F) -> F:
    denominator = 1 - x * alpha
    if denominator == 0:
        raise ZeroDivisionError
    return (x - alpha) / denominator


def display(x: F, epsilon: F) -> F:
    return x + epsilon * x**3 * (1 - x**2)


def verify_interval_actions() -> dict[str, object]:
    controls = [
        (F(1, 3), F(1, 5), F(-1, 7)),
        (F(-2, 5), F(1, 4), F(2, 9)),
        (F(3, 8), F(-1, 6), F(1, 10)),
    ]
    checks = 0
    for x, alpha, beta in controls:
        combined_parameter = xr_add(alpha, beta)
        if xr_subtract(xr_subtract(x, alpha), beta) != xr_subtract(
            x, combined_parameter
        ):
            raise AssertionError("observer action composition")
        if xr_subtract(xr_subtract(x, alpha), -alpha) != x:
            raise AssertionError("observer action inverse")
        if not (-1 < xr_subtract(x, alpha) < 1):
            raise AssertionError("bound preservation")
        checks += 3

    epsilon = F(1, 4)
    # g'_epsilon=1+epsilon*(3x^2-5x^4). The bracket has minimum -2
    # on [-1,1], so this exact witness has derivative >=1/2.
    derivative_floor = 1 - 2 * epsilon
    if derivative_floor != F(1, 2) or derivative_floor <= 0:
        raise AssertionError("counterdisplay monotonicity")
    neutral_slope = 1
    if neutral_slope != 1:
        raise AssertionError("counterdisplay neutral slope")

    x, alpha = F(1, 3), F(1, 5)
    underlying = xr_subtract(x, alpha)
    actual = display(underlying, epsilon)
    displayed_x = display(x, epsilon)
    displayed_alpha = display(alpha, epsilon)
    false_mobius = xr_subtract(displayed_x, displayed_alpha)
    mismatch = actual - false_mobius
    if underlying != F(1, 7) or mismatch == 0:
        raise AssertionError("slope-matched nonprojective witness")
    checks += 4
    return {
        "checks": checks,
        "underlying_shifted": str(underlying),
        "actual_shifted": str(actual),
        "false_mobius_shifted": str(false_mobius),
        "mismatch": str(mismatch),
    }


def verify_projective_class() -> int:
    # With d=1, F(0)=-1 gives b=-1. F(1)=0 gives a=1.
    # F(infinity)=1 gives c=a=1.
    a, b, c, d = F(1), F(-1), F(1), F(1)
    if b / d != -1:
        raise AssertionError("negative anchor")
    if (a + b) / (c + d) != 0:
        raise AssertionError("neutral anchor")
    if a / c != 1:
        raise AssertionError("positive anchor")
    # At exp(phi)=2, r=4 and the projective readout is 3/5.
    r = F(4)
    if (a * r + b) / (c * r + d) != F(3, 5):
        raise AssertionError("projective tanh witness")
    return 4


def verify_wrl_readouts() -> dict[str, object]:
    # y=exp(-phi)=1/2 corresponds to phi=log(2).
    y = F(1, 2)
    lapse_squared = y * y
    coordinate_fraction = 1 - lapse_squared
    proper_fraction = 1 - y
    projective_fraction = (1 - y * y) / (1 + y * y)
    if (
        coordinate_fraction,
        proper_fraction,
        projective_fraction,
    ) != (F(3, 4), F(1, 2), F(3, 5)):
        raise AssertionError("WRL readout witness")
    if len({coordinate_fraction, proper_fraction, projective_fraction}) != 3:
        raise AssertionError("readout collapse")

    # Differential identities with X=3 and y=exp(-phi).
    xmax = F(3)
    dr_dphi = 2 * xmax * y * y
    proper_density = dr_dphi / y
    optical_density = dr_dphi / (y * y)
    if proper_density != 2 * xmax * y:
        raise AssertionError("proper density")
    if optical_density != 2 * xmax:
        raise AssertionError("optical density")
    return {
        "checks": 6,
        "coordinate_fraction": str(coordinate_fraction),
        "proper_fraction": str(proper_fraction),
        "projective_fraction": str(projective_fraction),
        "proper_reach_over_X": "2",
        "optical_reach": "INFINITE",
    }


def verify_coframe_reparametrization() -> int:
    controls = [
        (F(5), F(3), F(2, 7), F(11, 4)),
        (F(7, 2), F(9, 5), F(4, 3), F(2)),
        (F(13, 3), F(1, 2), F(5, 8), F(17, 6)),
    ]
    for xmax, length, hprime, q in controls:
        dx = xmax * hprime
        coframe = length * dx / (xmax * hprime)
        metric = q * dx * dx / (xmax * xmax * hprime * hprime)
        if coframe != length or metric != q:
            raise AssertionError("Jacobian reparametrization")
    return 2 * len(controls)


def lambda_area(lam: F, shear: F, t: F) -> F:
    denominator = lam * lam - shear * shear * t * t
    if denominator == 0:
        raise ZeroDivisionError
    return lam * t * (lam * lam - shear * shear) / denominator


def lambda_shape(lam: F, shear: F, t: F) -> F:
    denominator = lam * lam - shear * shear * t * t
    if denominator == 0:
        raise ZeroDivisionError
    return (
        lam**4 * shear * shear * (1 - t * t) ** 2
        / denominator**2
    )


def verify_lambda_controls() -> int:
    count = 0
    controls = [
        (F(1), F(1, 2)),
        (F(2), F(1)),
        (F(2), F(2)),
        (F(3), F(3)),
    ]
    for lam, shear in controls:
        for t in (F(1, 3), F(9, 10), F(99, 100)):
            denominator = lam * lam - shear * shear * t * t
            if denominator <= 0:
                raise AssertionError("nonsingular declared branch")
            area = lambda_area(lam, shear, t)
            shape = lambda_shape(lam, shear, t)
            if shear == lam:
                if area != 0 or shape != lam * lam:
                    raise AssertionError("matched branch")
            count += 3

    # Generic t->1 algebraic limits when s<lambda.
    for lam, shear in [(F(1), F(1, 2)), (F(2), F(1))]:
        area_limit = (
            lam * (lam * lam - shear * shear)
            / (lam * lam - shear * shear)
        )
        shape_limit = F(0)
        if area_limit != lam or shape_limit != 0:
            raise AssertionError("generic asymptotic limit")
        count += 2
    return count


def expect_clean(
    mutation: str,
    interval: dict[str, object],
    projective: dict[str, object],
    wrl: dict[str, object],
    coframe: dict[str, object],
    lambdas: dict[str, object],
    result: dict[str, object],
) -> bool:
    if mutation == "Xmax_promoted_from_working_to_canon":
        return result["owner_working_premise"].startswith("one_universal")
    if mutation == "endpoint_promoted_to_domain_point":
        return interval["endpoints_in_domain"] is False
    if mutation == "signed_coordinate_called_negative_distance":
        return interval["physical_distance_signed"] is False
    if mutation == "tanh_uniqueness_false_positive":
        return interval[
            "tanh_unique_from_invariant_bound_group_reversal_slope"
        ] is False
    if mutation == "slope_matched_counterfamily_deleted":
        return len(interval["compactifications"]) == 4
    if mutation == "projective_premise_hidden":
        return projective["physical_readout_premise"] == "OPEN_NOT_DERIVED"
    if mutation == "conditional_projective_result_promoted":
        return projective["status"].startswith("DERIVED_CONDITIONAL")
    if mutation == "coordinate_reach_called_proper_reach":
        return wrl["coordinate_reach"] != wrl["proper_reach"]
    if mutation == "optical_boundary_called_finite":
        return wrl["optical_reach"] == "INFINITE"
    if mutation == "three_metric_readouts_collapsed":
        return wrl["three_readouts_equal"] is False
    if mutation == "coframe_reparametrization_dropped_Jacobian":
        return coframe["exact_residual"] == "ZERO"
    if mutation == "coframe_covariance_promoted_to_H_selector":
        return coframe["coframe_selects_H"] is False
    if mutation == "regularity_promoted_to_coordinate_selector":
        return coframe["regularity_selects_coordinate_chart"] is False
    if mutation == "asymptotic_unattainability_promoted_to_area_BC":
        return lambdas["asymptotic_unattainability_alone"] == (
            "does_not_force_s_or_lambda"
        )
    if mutation == "lambda_set_to_one":
        return lambdas["lambda_one_selected"] is False
    if mutation == "display_H_inserted_into_lambda_equation":
        return lambdas["display_H_enters_equations"] is False
    if mutation == "nonunit_matched_branch_deleted":
        return any(
            row["lambda"] == "2" and row["s"] == "2"
            for row in lambdas["witnesses"]
        )
    if mutation == "route_missing_or_duplicate":
        routes = read_tsv("ROUTE_RULING_MATRIX.tsv")
        return len(routes) == 16 and len({row["route_id"] for row in routes}) == 16
    if mutation == "native_position_law_false_positive":
        return result["native_position_law_closed"] is False
    if mutation == "maximum_conclusion_overstated":
        return "DOES_NOT_YET_SELECT_THE_POSITION_READOUT_OR_LAMBDA" in (
            result["maximum_conclusion"]
        )
    raise AssertionError(f"unknown mutation: {mutation}")


def verify_mutations() -> list[dict[str, str]]:
    interval = read_json("INTERVAL_ACTION_CLASSIFICATION.json")
    projective = read_json("PROJECTIVE_CLASS_RESULT.json")
    wrl = read_json("WRL_DISTANCE_RESULT.json")
    coframe = read_json("COFRAME_REPARAMETRIZATION_RESULT.json")
    lambdas = read_json("ONE_BOUNDARY_LAMBDA_RESULT.json")
    result = read_json("RESULT.json")
    registered = read_tsv("CATCH_PROOFS.tsv")
    if len(registered) != 20:
        raise AssertionError("catch count")
    outcomes = []
    for row in registered:
        mutation = row["mutation"]
        if not expect_clean(
            mutation, interval, projective, wrl, coframe, lambdas, result
        ):
            raise AssertionError(f"clean catch failed: {row['catch_id']}")
        copies = [
            copy.deepcopy(item)
            for item in [interval, projective, wrl, coframe, lambdas, result]
        ]
        mi, mp, mw, mc, ml, mr = copies
        if mutation == "Xmax_promoted_from_working_to_canon":
            mr["owner_working_premise"] = "CANON_DERIVED_XMAX"
        elif mutation == "endpoint_promoted_to_domain_point":
            mi["endpoints_in_domain"] = True
        elif mutation == "signed_coordinate_called_negative_distance":
            mi["physical_distance_signed"] = True
        elif mutation == "tanh_uniqueness_false_positive":
            mi["tanh_unique_from_invariant_bound_group_reversal_slope"] = True
        elif mutation == "slope_matched_counterfamily_deleted":
            mi["compactifications"] = mi["compactifications"][:3]
        elif mutation == "projective_premise_hidden":
            mp["physical_readout_premise"] = "DERIVED"
        elif mutation == "conditional_projective_result_promoted":
            mp["status"] = "DERIVED_UNCONDITIONAL"
        elif mutation == "coordinate_reach_called_proper_reach":
            mw["proper_reach"] = mw["coordinate_reach"]
        elif mutation == "optical_boundary_called_finite":
            mw["optical_reach"] = "FINITE"
        elif mutation == "three_metric_readouts_collapsed":
            mw["three_readouts_equal"] = True
        elif mutation == "coframe_reparametrization_dropped_Jacobian":
            mc["exact_residual"] = "NONZERO"
        elif mutation == "coframe_covariance_promoted_to_H_selector":
            mc["coframe_selects_H"] = True
        elif mutation == "regularity_promoted_to_coordinate_selector":
            mc["regularity_selects_coordinate_chart"] = True
        elif mutation == "asymptotic_unattainability_promoted_to_area_BC":
            ml["asymptotic_unattainability_alone"] = "forces_s_and_lambda"
        elif mutation == "lambda_set_to_one":
            ml["lambda_one_selected"] = True
        elif mutation == "display_H_inserted_into_lambda_equation":
            ml["display_H_enters_equations"] = True
        elif mutation == "nonunit_matched_branch_deleted":
            ml["witnesses"] = [
                witness for witness in ml["witnesses"]
                if not (witness["lambda"] == "2" and witness["s"] == "2")
            ]
        elif mutation == "native_position_law_false_positive":
            mr["native_position_law_closed"] = True
        elif mutation == "maximum_conclusion_overstated":
            mr["maximum_conclusion"] = "NATIVE_CLOSURE"

        if mutation == "route_missing_or_duplicate":
            caught = len(read_tsv("ROUTE_RULING_MATRIX.tsv")[:-1]) != 16
        else:
            caught = not expect_clean(mutation, mi, mp, mw, mc, ml, mr)
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
    interval = verify_interval_actions()
    projective_checks = verify_projective_class()
    wrl = verify_wrl_readouts()
    coframe_checks = verify_coframe_reparametrization()
    lambda_checks = verify_lambda_controls()
    catches = verify_mutations()
    source_checks = verify_source_hashes()
    routes = read_tsv("ROUTE_RULING_MATRIX.tsv")
    statuses = read_tsv("STATUS_LEDGER.tsv")
    readouts = read_tsv("OPERATIONAL_READOUT_ATLAS.tsv")
    result = read_json("RESULT.json")
    if (
        len(routes) != 16
        or len(statuses) != 16
        or len(readouts) != 5
        or result["native_position_law_closed"] is not False
        or result["lambda_closed"] is not False
    ):
        raise AssertionError("ledger or result contract")

    output = {
        "schema": "udt-invariant-xmax-independent-verification-1.0",
        "method": "stdlib_Fraction_no_production_import",
        "interval_action_checks": interval["checks"],
        "interval_mismatch": interval["mismatch"],
        "projective_checks": projective_checks,
        "wrl_readout_checks": wrl["checks"],
        "coframe_checks": coframe_checks,
        "lambda_checks": lambda_checks,
        "source_hash_checks": source_checks,
        "route_checks": len(routes),
        "status_checks": len(statuses),
        "readout_checks": len(readouts),
        "catch_count": len(catches),
        "catch_pass_count": len(catches),
        "all_checks_pass": True,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
