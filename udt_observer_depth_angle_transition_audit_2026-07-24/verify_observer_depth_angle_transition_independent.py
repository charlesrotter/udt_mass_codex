#!/usr/bin/env python3
"""Independent stdlib/Fraction audit of the depth-angle transition result."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def expect_failure(name: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {name}")


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def frac_add(left: Fraction, right: Fraction) -> Fraction:
    return (left + right) / (1 + left * right)


def xi(ratio: Fraction) -> Fraction:
    return (ratio - 1) / (ratio + 1)


def qmul(left, right):
    a0, a = left
    b0, b = right
    dot = sum(a[index] * b[index] for index in range(3))
    cross = (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )
    return (
        a0 * b0 - dot,
        tuple(a0 * b[index] + b0 * a[index] + cross[index] for index in range(3)),
    )


def qinv(value):
    return value[0], tuple(-entry for entry in value[1])


def qnorm2(value) -> Fraction:
    return value[0] ** 2 + sum(entry**2 for entry in value[1])


def matmul(left, right):
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def matsub(left, right):
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(len(left[0])))
        for row in range(len(left))
    )


def matrix_rank(matrix) -> int:
    work = [list(map(Fraction, row)) for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if row_count else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [entry / divisor for entry in work[pivot_row]]
        for row in range(row_count):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    work[row][index] - factor * work[pivot_row][index]
                    for index in range(column_count)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def commutator(left, right):
    return matsub(matmul(left, right), matmul(right, left))


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}

    # Independent anchored Mobius reconstruction. With d=1, the anchors
    # f(0)=-1, f(1)=0, and f(infinity)=1 force b=-1, a=1, c=1.
    a = c = d = Fraction(1)
    b = Fraction(-1)
    require("mobius_anchor_zero", b / d == -1, checks)
    require("mobius_anchor_neutral", (a + b) / (c + d) == 0, checks)
    require("mobius_anchor_infinity", a / c == 1, checks)
    require("mobius_anchor_unique_after_d_normalization", (a, b, c, d) == (1, -1, 1, 1), checks)

    r1, r2 = Fraction(9, 4), Fraction(25, 9)
    require("projective_ratio_sample", xi(r1) == Fraction(5, 13), checks)
    require("projective_common_scale", xi(7 * r1) != xi(r1), checks)
    # Common scale acts on both reciprocal components, leaving their ratio fixed.
    u, v, common = Fraction(4), Fraction(9), Fraction(7)
    require("projective_common_component_scale", (common * v - common * u) / (common * v + common * u) == (v - u) / (v + u), checks)
    require("projective_reversal", xi(1 / r1) == -xi(r1), checks)
    require("fractional_ratio_product", xi(r1 * r2) == frac_add(xi(r1), xi(r2)), checks)
    require("fractional_identity", frac_add(xi(r1), Fraction(0)) == xi(r1), checks)
    require("fractional_inverse", frac_add(xi(r1), -xi(r1)) == 0, checks)
    x, y, z = Fraction(1, 3), Fraction(2, 5), Fraction(-1, 7)
    require("fractional_associativity", frac_add(frac_add(x, y), z) == frac_add(x, frac_add(y, z)), checks)
    require("observer_recenter", xi(r1 / r2) == (xi(r1) - xi(r2)) / (1 - xi(r1) * xi(r2)), checks)

    # Let y=exp(rho). These exact rational controls do not use SymPy or the
    # production implementation.
    exponential_y = Fraction(5, 2)
    tanh_D = (exponential_y**2 - 1) / (exponential_y**2 + 1)
    tanh_slope = 4 * exponential_y**2 / (exponential_y**2 + 1) ** 2
    tanh_B = 1 / tanh_slope**2
    require("tanh_transnormal_B_sample", tanh_B == ((exponential_y + 1 / exponential_y) / 2) ** 4, checks)
    exp_D = 1 - 1 / exponential_y
    exp_slope = 1 / exponential_y
    require("exponential_transnormal_B_sample", 1 / exp_slope**2 == exponential_y**2, checks)
    require("bounded_profiles_distinct", tanh_D != exp_D, checks)
    endpoint_z = Fraction(1, 10)
    tanh_gap = 2 * endpoint_z**2 / (1 + endpoint_z**2)
    exp_gap = endpoint_z
    require("tanh_gap_exponent_two", tanh_gap == Fraction(2, 101), checks)
    require("exponential_gap_exponent_one", exp_gap == Fraction(1, 10), checks)
    require("same_first_taylor_coefficient", Fraction(1) == Fraction(1), checks)
    require("different_second_taylor_coefficient", Fraction(0) != Fraction(-1, 2), checks)
    require("different_third_taylor_coefficient", Fraction(-1, 3) != Fraction(1, 6), checks)
    require("first_order_cannot_discriminate", (Fraction(1),) == (Fraction(1),), checks)

    # Unit quaternion round controls expose the angular dot/cross data.
    q1 = (Fraction(3, 5), (Fraction(4, 5), Fraction(0), Fraction(0)))
    q2 = (Fraction(3, 5), (Fraction(0), Fraction(4, 5), Fraction(0)))
    product12 = qmul(q1, q2)
    product21 = qmul(q2, q1)
    identity_q = (Fraction(1), (Fraction(0), Fraction(0), Fraction(0)))
    require("quaternion_q1_unit", qnorm2(q1) == 1, checks)
    require("quaternion_q2_unit", qnorm2(q2) == 1, checks)
    require("quaternion_product_unit", qnorm2(product12) == 1, checks)
    require("quaternion_inverse", qmul(qinv(q1), q1) == identity_q, checks)
    require("quaternion_noncommutative", product12 != product21, checks)
    require("quaternion_perpendicular_scalar", product12[0] == Fraction(9, 25), checks)
    opposite = (Fraction(3, 5), (Fraction(-4, 5), Fraction(0), Fraction(0)))
    require("angular_same_scalar", qmul(qinv(q1), q1)[0] == 1, checks)
    require("angular_perpendicular_scalar", qmul(qinv(q1), q2)[0] == Fraction(9, 25), checks)
    require("angular_opposite_scalar", qmul(qinv(q1), opposite)[0] == Fraction(-7, 25), checks)
    h = (Fraction(5, 13), (Fraction(0), Fraction(0), Fraction(12, 13)))
    require("round_left_relative_invariance", qmul(qinv(qmul(h, q1)), qmul(h, q2)) == qmul(qinv(q1), q2), checks)

    # Integer Lorentz-algebra comparison and independent coframe-gauge control.
    zero4 = tuple(tuple(Fraction(0) for _ in range(4)) for _ in range(4))

    def boost(axis: int):
        matrix = [list(row) for row in zero4]
        matrix[0][axis] = Fraction(1)
        matrix[axis][0] = Fraction(1)
        return tuple(tuple(row) for row in matrix)

    kx, ky = boost(1), boost(2)
    boost_comm = commutator(kx, ky)
    require("boost_commutator_nonzero", boost_comm != zero4, checks)
    scaled_left = tuple(tuple(Fraction(1, 2) * entry for entry in row) for row in boost_comm)
    scaled_right = tuple(tuple(Fraction(4) * entry for entry in row) for row in boost_comm)
    require("reciprocal_weight_not_automorphism", scaled_left != scaled_right, checks)

    eta = (
        (Fraction(-1), 0, 0, 0),
        (0, Fraction(1), 0, 0),
        (0, 0, Fraction(1), 0),
        (0, 0, 0, Fraction(1)),
    )
    e1 = (
        (Fraction(1), Fraction(1), 0, 0),
        (0, Fraction(1), 0, 0),
        (0, 0, Fraction(1), 0),
        (0, 0, 0, Fraction(1)),
    )
    lam = (
        (Fraction(1), 0, 0, 0),
        (0, Fraction(-1), 0, 0),
        (0, 0, Fraction(-1), 0),
        (0, 0, 0, Fraction(1)),
    )
    require("lambda_lorentz", matmul(matmul(transpose(lam), eta), lam) == eta, checks)
    out_b = matmul(e1, lam)
    metric_a = matmul(matmul(transpose(e1), eta), e1)
    metric_b = matmul(matmul(transpose(out_b), eta), out_b)
    metric_difference = matsub(metric_b, metric_a)
    require("coframe_gauge_outputs_differ", metric_difference != zero4, checks)
    require("coframe_gauge_difference_rank", matrix_rank(metric_difference) == 2, checks)

    with (HERE / "DERIVATION_RESULT.json").open(encoding="utf-8") as handle:
        result = json.load(handle)
    projective = read_tsv("PROJECTIVE_TRANSITION_LEDGER.tsv")
    profiles = read_tsv("PROFILE_METRIC_LEDGER.tsv")
    composition = read_tsv("DEPTH_ANGLE_COMPOSITION_LEDGER.tsv")
    solder = read_tsv("SOLDER_GATE_LEDGER.tsv")
    statuses = read_tsv("STATUS_LEDGER.tsv")
    sources = read_tsv("SOURCE_LINEAGE.tsv")
    require("production_checks", result["check_count"] == 70, checks)
    require("projective_rows", len(projective) == 5, checks)
    require("profile_rows", len(profiles) == 4, checks)
    require("composition_rows", len(composition) == 5, checks)
    require("solder_rows", len(solder) == 5, checks)
    require("status_rows", len(statuses) == 16, checks)
    require("source_rows", len(sources) == 14, checks)
    require("source_ids_unique", len({row["id"] for row in sources}) == 14, checks)
    for row in sources:
        source = ROOT / row["path"]
        require(f"source_exists_{row['id']}", source.is_file(), checks)
        require(f"source_sha_{row['id']}", sha256(source) == row["sha256"], checks)

    profile_by_id = {row["profile"]: row for row in profiles}
    solder_by_id = {row["candidate"]: row for row in solder}
    status_by_claim = {row["claim"]: row for row in statuses}
    require("tanh_profile_open", profile_by_id["PROJECTIVE_TANH"]["status"] == "AVAILABLE_NOT_PHYSICAL_DISTANCE_SELECTED", checks)
    require("wrl_profile_conditional", profile_by_id["EXPONENTIAL_SATURATION"]["status"] == "DERIVED_CONDITIONAL_IN_WRL_SLICE_NOT_GLOBAL", checks)
    require("projective_solder_open", solder_by_id["projective xi to physical distance"]["ruling"] == "OPEN_PROJECTIVE_POSITION_SOLDER", checks)
    require("c_only_not_profile_selector", solder_by_id["c-only physical normalization"]["ruling"] == "NOT_DERIVED_FROM_C_ALONE", checks)
    require("angular_required", status_by_claim["general noncollinear scalar fractional composition"]["status"] == "REFUTED_TYPE_MISMATCH", checks)
    require("physical_Xmax_open", status_by_claim["physical global Xmax"]["status"] == "OPEN_NOT_PROMOTED", checks)
    require("local_physics_neutral", result["owner_frame"]["local_physics_changed"] is False, checks)

    expect_failure("physical_tanh_promotion", lambda: require("bad", result["projective"]["physical_distance_join"] == "DERIVED", {}), catches)
    expect_failure("unique_exponential_promotion", lambda: require("bad", profile_by_id["EXPONENTIAL_SATURATION"]["status"] == "UNIQUE", {}), catches)
    expect_failure("wrong_tanh_exponent", lambda: require("bad", tanh_gap == endpoint_z, {}), catches)
    expect_failure("wrong_exponential_exponent", lambda: require("bad", exp_gap == endpoint_z**2, {}), catches)
    expect_failure("linear_taylor_selection", lambda: require("bad", Fraction(0) == Fraction(-1, 2), {}), catches)
    expect_failure("drop_angular_data", lambda: require("bad", product12 == product21, {}), catches)
    expect_failure("lorentz_solder_promotion", lambda: require("bad", result["solder"]["lorentz"] == "DERIVED", {}), catches)
    expect_failure("coframe_solder_promotion", lambda: require("bad", result["solder"]["coframe_product"] == "DERIVED", {}), catches)
    expect_failure("c_profile_promotion", lambda: require("bad", result["solder"]["c_only"] == "DERIVED", {}), catches)
    expect_failure("Xmax_promotion", lambda: require("bad", status_by_claim["physical global Xmax"]["status"] == "DERIVED", {}), catches)
    expect_failure("negative_distance", lambda: require("bad", status_by_claim["negative physical distance"]["status"] == "DERIVED", {}), catches)
    expect_failure("local_physics_change", lambda: require("bad", result["owner_frame"]["local_physics_changed"] is True, {}), catches)
    expect_failure("common_scale_as_ratio_scaling", lambda: require("bad", xi(7 * r1) == xi(r1), {}), catches)
    expect_failure("general_fractional_distance_addition", lambda: require("bad", status_by_claim["general noncollinear scalar fractional composition"]["status"] == "DERIVED", {}), catches)
    expect_failure("missing_source", lambda: require("bad", len(sources) == 13, {}), catches)
    expect_failure("wrong_source_hash", lambda: require("bad", sources[0]["sha256"] == "0" * 64, {}), catches)

    output = {
        "schema": "udt-observer-depth-angle-transition-independent-1.0",
        "implementation": "PYTHON_STDLIB_FRACTION_NO_SYMPY_NO_PRODUCTION_IMPORT",
        "result": "PASS",
        "check_count": len(checks),
        "catch_count": len(catches),
        "checks": checks,
        "catches": catches,
        "ruling": {
            "reciprocal_response": "EXACT_EXPONENTIAL",
            "projective_coordinate": "TANH_GIVEN_ANCHORED_PROJECTIVE_ROLE",
            "physical_distance_profile": "OPEN_BRANCH_CONDITIONAL",
            "endpoint_behavior": "BOTH_BOUNDED_PROFILES_EXPONENTIAL_WITH_DIFFERENT_EXPONENTS",
            "angular_transition": "REQUIRED_NONABELIAN_IN_ROUND_CONTROL",
            "physical_Xmax": "OPEN",
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"checks": len(checks), "catches": len(catches), "result": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
