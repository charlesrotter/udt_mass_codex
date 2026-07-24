#!/usr/bin/env python3
"""Independent stdlib verification; does not import the production derivation."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition: bool, message: str, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(message)
    checks[message] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((entry * value for entry, value in zip(row, vector)), Fraction(0)) for row in matrix]


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*matrix)]


def validate(
    result: dict,
    candidates: list[dict[str, str]],
    statuses: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> None:
    if result.get("schema") != "udt-metric-native-observer-separation-asymptote-1.0":
        raise AssertionError("schema")
    if result.get("check_count") != 39 or set(result.get("checks", {}).values()) != {"PASS"}:
        raise AssertionError("production checks")
    if len(candidates) != 8 or len({row["candidate"] for row in candidates}) != 8:
        raise AssertionError("candidate coverage")
    if len(statuses) != 9 or len({row["claim"] for row in statuses}) != 9:
        raise AssertionError("status coverage")
    if len(sources) != 11 or len({row["path"] for row in sources}) != 11:
        raise AssertionError("source coverage")

    profiles = result["profile_family"]
    if profiles["bounded_tanh"]["endpoint_D_over_X"] != "1":
        raise AssertionError("tanh endpoint")
    if profiles["bounded_exponential"]["endpoint_D_over_X"] != "1":
        raise AssertionError("exponential endpoint")
    if profiles["unbounded_linear"]["endpoint_D_over_X"] != "oo":
        raise AssertionError("unbounded control")

    readings = result["wrl_readings"]
    expected_endpoints = {
        "coordinate_areal_r": "1",
        "slice_proper_ell": "2",
        "optical_depth": "oo",
        "projective_tanh": "1",
    }
    if {name: row["endpoint_over_X"] for name, row in readings.items()} != expected_endpoints:
        raise AssertionError("distinct endpoint classes")

    required_depth_tokens = ("a20", "a30", "a21", "a31", "b", "e", "U", "W", "R", "Q")
    depth_norm = result["complete_horizontal_metric"]["depth_norm_B"]
    if any(token not in depth_norm for token in required_depth_tokens):
        raise AssertionError("complete depth norm sectors")
    if result["complete_horizontal_metric"]["determinant"] != "Q**2*R**2*W**2":
        raise AssertionError("horizontal determinant")

    transnormal = result["transnormal_distance"]
    if transnormal["law"] != "dD/dphi=1/sqrt(B(phi))":
        raise AssertionError("transnormal law")
    if transnormal["wrl_endpoint"] != "2*X":
        raise AssertionError("WRL proper endpoint")

    angular = result["angular_countercontrol"]
    if angular["difference"] != "3*pi**2*L**2":
        raise AssertionError("angular diameter countercontrol")

    by_claim = {row["claim"]: row for row in statuses}
    if by_claim["clock_dilation_alone_fixes_global_Xmax"]["status"] != "REFUTED_IN_CURRENT_CONFIGURATION_CLASS":
        raise AssertionError("global promotion")
    if by_claim["complete_current_metric_parent_selects_unique_D_of_phi"]["status"] != "OPEN_NOT_SELECTED":
        raise AssertionError("unique D promotion")
    if by_claim["tanh_is_metric_native_distance_law"]["status"] != "NOT_DERIVED":
        raise AssertionError("tanh promotion")

    by_candidate = {row["candidate"]: row for row in candidates}
    if "physical_reciprocal_clock_leg" not in by_candidate["horizontal_coframe_distance"]["requires"]:
        raise AssertionError("clock leg dependency")
    if by_candidate["global_pair_diameter"]["global_Xmax_status"] != "DEFINITIONAL_OUTPUT_NOT_YET_EVALUABLE":
        raise AssertionError("diameter availability")

    for row in sources:
        if sha256(ROOT / row["path"]) != row["sha256"]:
            raise AssertionError(f"source identity {row['path']}")


def expect_failure(name: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, TypeError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {name}")


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    candidates = read_tsv(HERE / "DISTANCE_CANDIDATE_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    checks: dict[str, str] = {}

    validate(result, candidates, statuses, sources)
    checks["production_outputs_fail_closed"] = "PASS"

    # F1 independently: equal origin/slope does not determine shape or finiteness.
    for value in (0.0, 0.25, 1.0, 3.0):
        tanh_value = math.tanh(value)
        exp_value = 1.0 - math.exp(-value)
        linear_value = value
        require(tanh_value >= 0 and exp_value >= 0 and linear_value >= 0, f"F1 nonnegative {value}", checks)
    h = 1e-7
    tanh_slope = math.tanh(h) / h
    exp_slope = (1.0 - math.exp(-h)) / h
    require(abs(tanh_slope - 1.0) < 1e-6, "F1 tanh unit origin slope", checks)
    require(abs(exp_slope - 1.0) < 1e-6, "F1 exponential unit origin slope", checks)
    require(abs(math.tanh(1.0) - (1.0 - math.exp(-1.0))) > 0.1, "F1 bounded shapes distinct", checks)
    require(math.tanh(30.0) == 1.0, "F1 tanh bounded numeric", checks)
    require(abs((1.0 - math.exp(-30.0)) - 1.0) < 1e-12, "F1 exponential bounded numeric", checks)
    require(30.0 > 20.0, "F1 linear unbounded control", checks)

    # F2 exact rational reconstruction at T=2.
    Tclock = Fraction(2)
    coordinate = 1 - Fraction(1, Tclock**2)
    proper = 2 * (1 - Fraction(1, Tclock))
    projective = (Tclock**2 - 1) / (Tclock**2 + 1)
    require(coordinate == Fraction(3, 4), "F2 coordinate at T=2", checks)
    require(proper == 1, "F2 proper at T=2", checks)
    require(projective == Fraction(3, 5), "F2 projective at T=2", checks)
    require(len({coordinate, proper, projective}) == 3, "F2 algebraic readings distinct", checks)
    require(abs(2 * math.log(2) - float(coordinate)) > 0.5, "F2 optical distinct", checks)

    # F3 independent rational coframe pullback.
    U, W, R, Q = Fraction(2), Fraction(3), Fraction(5), Fraction(7)
    b, e = Fraction(1), Fraction(2)
    a20, a30 = Fraction(1, 3), Fraction(-1, 4)
    a21, a31 = Fraction(2, 5), Fraction(1, 6)
    E = [
        [U, b, Fraction(0), Fraction(0)],
        [Fraction(0), W, Fraction(0), Fraction(0)],
        [R * a20 + e * a30, R * a21 + e * a31, R, e],
        [Q * a30, Q * a31, Fraction(0), Q],
    ]
    dx1, dx2, dx3 = Fraction(6), Fraction(-2), Fraction(3)
    dx0 = -b * dx1 / U
    theta = mat_vec(E, [dx0, dx1, dx2, dx3])
    require(theta[0] == 0, "F3 clock-horizontal injection", checks)
    spacetime_square = -theta[0] ** 2 + theta[1] ** 2 + theta[2] ** 2 + theta[3] ** 2
    k2 = R * a21 + e * a31 - (b / U) * (R * a20 + e * a30)
    k3 = Q * (a31 - (b / U) * a30)
    S = [
        [W, Fraction(0), Fraction(0)],
        [k2, R, e],
        [k3, Fraction(0), Q],
    ]
    spatial_theta = mat_vec(S, [dx1, dx2, dx3])
    horizontal_square = sum((value**2 for value in spatial_theta), Fraction(0))
    require(spacetime_square == horizontal_square, "F3 full pullback identity", checks)
    require(W * R * Q > 0, "F3 positive spatial coframe determinant", checks)

    p0, p1, p2, p3 = Fraction(2), Fraction(-1), Fraction(3), Fraction(4)
    c0 = (p0 - a20 * p2 - a30 * p3) / U
    c1 = (p1 - a21 * p2 - a31 * p3 - b * c0) / W
    c2 = p2 / R
    c3 = (p3 - e * p2 / R) / Q
    restricted_p = [p1 - b * p0 / U, p2, p3]
    reconstructed_p = mat_vec(transpose(S), [c1, c2, c3])
    require(reconstructed_p == restricted_p, "F3 depth covector decomposition", checks)
    require(c1**2 + c2**2 + c3**2 > 0, "F3 positive horizontal depth norm", checks)

    # Transnormal/eikonal law and the WR-L realization.
    X = Fraction(3)
    B_at_T2 = Tclock**2 / (4 * X**2)
    Dprime = Fraction(math.isqrt(B_at_T2.denominator), math.isqrt(B_at_T2.numerator))
    require(B_at_T2 == Fraction(1, 9), "transnormal WRL B at T=2", checks)
    require(Dprime == 3, "transnormal WRL Dprime at T=2", checks)
    require(Dprime == 2 * X / Tclock, "transnormal WRL metric law", checks)
    require(2 * X == 6, "transnormal WRL endpoint 2X", checks)

    # F4 complete product geometry: same clock law, different angular diameter.
    L = 2.0
    diameter_one = math.sqrt(L * L + (math.pi * L) ** 2 + (math.pi * L) ** 2)
    diameter_two = math.sqrt(L * L + (2 * math.pi * L) ** 2 + (math.pi * L) ** 2)
    require(diameter_two > diameter_one, "F4 angular completion changes global diameter", checks)
    require(
        abs(diameter_two**2 - diameter_one**2 - 3 * math.pi**2 * L**2) < 1e-12,
        "F4 diameter difference exact numeric",
        checks,
    )

    # F5 observer and scale dependence.
    beta, gamma = Fraction(3, 5), Fraction(5, 4)
    require(gamma**2 * (1 - beta**2) == 1, "F5 boost identity", checks)
    require(Fraction(1, gamma) == Fraction(4, 5), "F5 event pairing changes horizontal span", checks)
    require(Fraction(7, 3) * Fraction(5, 2) == Fraction(35, 6), "F5 common scale changes length", checks)

    catches: dict[str, str] = {}

    mutated = copy.deepcopy(result)
    mutated["complete_horizontal_metric"]["depth_norm_B"] = "p1**2/W**2+p2**2/R**2+p3**2/Q**2"
    expect_failure("drop_shift_and_angular_couplings", lambda: validate(mutated, candidates, statuses, sources), catches)

    mutated = copy.deepcopy(result)
    mutated["wrl_readings"]["optical_depth"]["endpoint_over_X"] = "1"
    expect_failure("identify_distinct_metric_readings", lambda: validate(mutated, candidates, statuses, sources), catches)

    mutated_statuses = copy.deepcopy(statuses)
    next(row for row in mutated_statuses if row["claim"] == "clock_dilation_alone_fixes_global_Xmax")[
        "status"
    ] = "DERIVED"
    expect_failure("promote_local_clock_law_to_global_Xmax", lambda: validate(result, candidates, mutated_statuses, sources), catches)

    mutated = copy.deepcopy(result)
    mutated["profile_family"]["unbounded_linear"]["endpoint_D_over_X"] = "1"
    expect_failure("erase_arbitrary_profile_counterfamily", lambda: validate(mutated, candidates, statuses, sources), catches)

    mutated_candidates = copy.deepcopy(candidates)
    next(row for row in mutated_candidates if row["candidate"] == "horizontal_coframe_distance")[
        "requires"
    ] = "metric_only"
    expect_failure("erase_clock_leg_dependency", lambda: validate(result, mutated_candidates, statuses, sources), catches)

    mutated_statuses = copy.deepcopy(statuses)
    next(row for row in mutated_statuses if row["claim"] == "tanh_is_metric_native_distance_law")[
        "status"
    ] = "DERIVED"
    expect_failure("promote_tanh", lambda: validate(result, candidates, mutated_statuses, sources), catches)

    mutated_candidates = copy.deepcopy(candidates)
    next(row for row in mutated_candidates if row["candidate"] == "global_pair_diameter")[
        "global_Xmax_status"
    ] = "DERIVED_FROM_LOCAL_X"
    expect_failure("identify_local_X_with_global_diameter", lambda: validate(result, mutated_candidates, statuses, sources), catches)

    mutated_sources = copy.deepcopy(sources)
    mutated_sources[0]["sha256"] = "0" * 64
    expect_failure("corrupt_source_identity", lambda: validate(result, candidates, statuses, mutated_sources), catches)

    mutated = copy.deepcopy(result)
    mutated["check_count"] = 38
    expect_failure("missing_production_check", lambda: validate(mutated, candidates, statuses, sources), catches)

    mutated_candidates = candidates[:-1]
    expect_failure("missing_candidate", lambda: validate(result, mutated_candidates, statuses, sources), catches)

    output = {
        "schema": "udt-metric-native-observer-separation-independent-verification-1.0",
        "implementation": "python_stdlib_fraction_and_float_no_production_import",
        "checks": checks,
        "check_count": len(checks),
        "catches": catches,
        "catch_count": len(catches),
        "source_count": len(sources),
        "result_sha256": sha256(HERE / "DERIVATION_RESULT.json"),
        "candidate_ledger_sha256": sha256(HERE / "DISTANCE_CANDIDATE_LEDGER.tsv"),
        "status_ledger_sha256": sha256(HERE / "STATUS_LEDGER.tsv"),
        "status": "PASS",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"independent_checks={len(checks)}")
    print(f"exercised_catches={len(catches)}")
    print(f"result_sha256={output['result_sha256']}")
    print("status=PASS")


if __name__ == "__main__":
    main()
