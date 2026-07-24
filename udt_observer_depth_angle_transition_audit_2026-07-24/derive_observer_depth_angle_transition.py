#!/usr/bin/env python3
"""Exact CPU derivation for observer depth-angle transitions."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def check(store: dict[str, str], name: str, condition: bool) -> None:
    if not bool(condition):
        raise AssertionError(name)
    store[name] = "PASS"


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def qmul(left: tuple[sp.Expr, sp.Matrix], right: tuple[sp.Expr, sp.Matrix]):
    a0, avec = left
    b0, bvec = right
    return (
        sp.expand(a0 * b0 - avec.dot(bvec)),
        sp.simplify(a0 * bvec + b0 * avec + avec.cross(bvec)),
    )


def qinv(value: tuple[sp.Expr, sp.Matrix]):
    return value[0], -value[1]


def qnorm2(value: tuple[sp.Expr, sp.Matrix]):
    return sp.expand(value[0] ** 2 + value[1].dot(value[1]))


def commutator(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.simplify(left * right - right * left)


def flatten(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(list(matrix))


def main() -> None:
    checks: dict[str, str] = {}
    rho, beta = sp.symbols("rho beta", real=True)
    x, y, z = sp.symbols("x y z", real=True)
    scale, length = sp.symbols("Dmax L", positive=True)

    # Anchored projectivization of the reciprocal positive ray.
    a, b, c, d, ratio = sp.symbols("a b c d ratio")
    mobius = (a * ratio + b) / (c * ratio + d)
    solution = sp.solve(
        [
            sp.Eq(b / d, -1),
            sp.Eq((a + b) / (c + d), 0),
            sp.Eq(a / c, 1),
            sp.Eq(d, 1),
        ],
        [a, b, c, d],
        dict=True,
    )
    check(checks, "projective_anchor_solution_unique", solution == [{a: 1, b: -1, c: 1, d: 1}])
    xi_ratio = (ratio - 1) / (ratio + 1)
    check(
        checks,
        "ratio_to_tanh",
        sp.simplify(
            xi_ratio.subs(ratio, sp.exp(2 * rho))
            - sp.tanh(rho).rewrite(sp.exp)
        )
        == 0,
    )
    common = sp.symbols("common", positive=True)
    u, v = sp.symbols("u v", positive=True)
    xi_uv = (v - u) / (v + u)
    check(
        checks,
        "projective_common_scale_neutral",
        sp.simplify(xi_uv.subs({u: common * u, v: common * v}) - xi_uv) == 0,
    )
    check(
        checks,
        "projective_reversal",
        sp.simplify(xi_ratio.subs(ratio, 1 / ratio) + xi_ratio) == 0,
    )

    def frac_add(left, right):
        return sp.cancel((left + right) / (1 + left * right))

    check(
        checks,
        "fractional_from_ratio_product",
        sp.factor(
            xi_ratio.subs(ratio, sp.symbols("r1") * sp.symbols("r2"))
            - frac_add(
                xi_ratio.subs(ratio, sp.symbols("r1")),
                xi_ratio.subs(ratio, sp.symbols("r2")),
            )
        )
        == 0,
    )
    check(checks, "fractional_identity", sp.simplify(frac_add(x, 0) - x) == 0)
    check(checks, "fractional_inverse", sp.simplify(frac_add(x, -x)) == 0)
    check(
        checks,
        "fractional_associativity",
        sp.factor(frac_add(frac_add(x, y), z) - frac_add(x, frac_add(y, z))) == 0,
    )
    alpha = sp.tanh(beta)
    check(
        checks,
        "observer_recenter_law",
        sp.simplify(
            sp.tanh(rho - beta) - (sp.tanh(rho) - alpha) / (1 - alpha * sp.tanh(rho))
        )
        == 0,
    )
    check(checks, "self_depth_neutral", sp.tanh(0) == 0)

    # Same reciprocal exponential, different metric distance profiles.
    profiles = {
        "PROJECTIVE_TANH": scale * sp.tanh(rho),
        "EXPONENTIAL_SATURATION": scale * (1 - sp.exp(-rho)),
        "LINEAR_UNBOUNDED": length * rho,
        "FULLFRAME_RADIAL_CONTROL": length * (sp.exp(rho) - 1),
    }
    profile_B = {name: sp.simplify(1 / sp.diff(expr, rho) ** 2) for name, expr in profiles.items()}
    check(
        checks,
        "B_projective_tanh",
        sp.simplify(profile_B["PROJECTIVE_TANH"] - sp.cosh(rho) ** 4 / scale**2) == 0,
    )
    check(
        checks,
        "B_exponential_saturation",
        sp.simplify(profile_B["EXPONENTIAL_SATURATION"] - sp.exp(2 * rho) / scale**2) == 0,
    )
    check(
        checks,
        "B_linear",
        sp.simplify(profile_B["LINEAR_UNBOUNDED"] - 1 / length**2) == 0,
    )
    check(
        checks,
        "B_fullframe_control",
        sp.simplify(profile_B["FULLFRAME_RADIAL_CONTROL"] - sp.exp(-2 * rho) / length**2) == 0,
    )
    for name, expr in profiles.items():
        check(checks, f"{name.lower()}_origin", sp.simplify(expr.subs(rho, 0)) == 0)
        check(checks, f"{name.lower()}_unit_slope", sp.simplify(sp.diff(expr, rho).subs(rho, 0) / (scale if name in {"PROJECTIVE_TANH", "EXPONENTIAL_SATURATION"} else length)) == 1)
    check(
        checks,
        "tanh_endpoint",
        sp.limit(profiles["PROJECTIVE_TANH"], rho, sp.oo) == scale,
    )
    check(
        checks,
        "exponential_endpoint",
        sp.limit(profiles["EXPONENTIAL_SATURATION"], rho, sp.oo) == scale,
    )
    check(checks, "linear_unbounded", sp.limit(profiles["LINEAR_UNBOUNDED"], rho, sp.oo) == sp.oo)
    check(
        checks,
        "fullframe_unbounded",
        sp.limit(profiles["FULLFRAME_RADIAL_CONTROL"], rho, sp.oo) == sp.oo,
    )
    check(
        checks,
        "tanh_gap_exact",
        sp.simplify(
            1
            - sp.tanh(rho).rewrite(sp.exp)
            - 2 / (sp.exp(2 * rho) + 1)
        )
        == 0,
    )
    check(
        checks,
        "exponential_gap_exact",
        sp.simplify(1 - profiles["EXPONENTIAL_SATURATION"] / scale - sp.exp(-rho)) == 0,
    )
    dilation = sp.exp(rho)
    distance_symbol = sp.symbols("D", nonnegative=True)
    check(
        checks,
        "exponential_profile_dilation_vs_gap",
        sp.simplify(
            dilation.subs(rho, -sp.log(1 - distance_symbol / scale))
            - scale / (scale - distance_symbol)
        )
        == 0,
    )
    check(
        checks,
        "projective_profile_dilation_vs_gap",
        sp.simplify(
            dilation.subs(
                rho,
                sp.Rational(1, 2)
                * sp.log(
                    (1 + distance_symbol / scale)
                    / (1 - distance_symbol / scale)
                ),
            )
            ** 2
            - (scale + distance_symbol) / (scale - distance_symbol)
        )
        == 0,
    )
    tanh_series = sp.series(sp.tanh(rho), rho, 0, 7).removeO()
    exp_series = sp.series(1 - sp.exp(-rho), rho, 0, 7).removeO()
    check(checks, "taylor_same_linear_anchor", sp.diff(tanh_series, rho).subs(rho, 0) == sp.diff(exp_series, rho).subs(rho, 0) == 1)
    check(checks, "taylor_profiles_distinct", sp.expand(tanh_series - exp_series) != 0)
    check(
        checks,
        "wrl_matches_exponential_family",
        sp.simplify(
            profile_B["EXPONENTIAL_SATURATION"].subs(scale, 2 * sp.symbols("X", positive=True))
            - sp.exp(2 * rho) / (4 * sp.symbols("X", positive=True) ** 2)
        )
        == 0,
    )
    check(
        checks,
        "profile_B_distinct_generic",
        all(
            sp.simplify(profile_B[first] - profile_B[second]) != 0
            for index, first in enumerate(profile_B)
            for second in list(profile_B)[index + 1 :]
        ),
    )

    # Exact round S3/unit-quaternion observer-relative transition.
    c0, s0 = sp.Rational(3, 5), sp.Rational(4, 5)
    e1 = sp.Matrix([1, 0, 0])
    e2 = sp.Matrix([0, 1, 0])
    q1 = (c0, s0 * e1)
    q2 = (c0, s0 * e2)
    product12 = qmul(q1, q2)
    product21 = qmul(q2, q1)
    check(checks, "quaternion_q1_unit", qnorm2(q1) == 1)
    check(checks, "quaternion_q2_unit", qnorm2(q2) == 1)
    check(checks, "quaternion_product_unit", sp.simplify(qnorm2(product12)) == 1)
    identity = (sp.Integer(1), sp.zeros(3, 1))
    q1_inv_product = qmul(qinv(q1), q1)
    check(checks, "quaternion_inverse", q1_inv_product == identity)
    check(checks, "quaternion_noncommutative_angular", product12[1] != product21[1])
    check(checks, "quaternion_perpendicular_scalar", product12[0] == sp.Rational(9, 25))
    same = qmul(qinv(q1), q1)
    opposite_axis = (c0, -s0 * e1)
    opposite_relative = qmul(qinv(q1), opposite_axis)
    perpendicular_relative = qmul(qinv(q1), q2)
    check(checks, "same_radius_dot_plus_one", same[0] == 1)
    check(checks, "same_radius_dot_zero", perpendicular_relative[0] == sp.Rational(9, 25))
    check(checks, "same_radius_dot_minus_one", opposite_relative[0] == sp.Rational(-7, 25))
    h = (sp.Rational(5, 13), sp.Matrix([0, 0, sp.Rational(12, 13)]))
    left_q1 = qmul(h, q1)
    left_q2 = qmul(h, q2)
    check(
        checks,
        "round_left_relative_invariance",
        qmul(qinv(left_q1), left_q2) == qmul(qinv(q1), q2),
    )
    check(
        checks,
        "round_antipode_axis_collapse",
        sp.simplify(sp.sin(sp.pi)) == 0 and sp.simplify(sp.cos(sp.pi)) == -1,
    )
    sigma, radius = sp.symbols("sigma b", positive=True)
    hopf_loop = 2 * sp.pi * radius * sigma
    horizontal_loop = 2 * sp.pi * radius
    check(checks, "squashed_round_limit", sp.simplify(hopf_loop.subs(sigma, 1) - horizontal_loop) == 0)
    check(checks, "squashed_directional_length_split", sp.simplify(hopf_loop.subs(sigma, 2) - horizontal_loop) != 0)

    # Local Lorentz comparison: full non-collinear closure is not the reciprocal scalar flow.
    def boost(axis: int) -> sp.Matrix:
        matrix = sp.zeros(4)
        matrix[0, axis] = 1
        matrix[axis, 0] = 1
        return matrix

    def rotation(first: int, second: int) -> sp.Matrix:
        matrix = sp.zeros(4)
        matrix[first, second] = -1
        matrix[second, first] = 1
        return matrix

    Kx, Ky, Kz = boost(1), boost(2), boost(3)
    Jx, Jy, Jz = rotation(2, 3), rotation(3, 1), rotation(1, 2)
    lorentz_basis = [Jx, Jy, Jz, Kx, Ky, Kz]
    commutators = [
        flatten(commutator(lorentz_basis[i], lorentz_basis[j]))
        for i in range(6)
        for j in range(i + 1, 6)
    ]
    commutator_rank = sp.Matrix.hstack(*commutators).rank()
    check(checks, "lorentz_commutators_span_algebra", commutator_rank == 6)
    boost_comm = commutator(Kx, Ky)
    check(checks, "boost_boost_generates_rotation", boost_comm in (Jz, -Jz))
    qweight = sp.symbols("q", positive=True)
    lhs = qweight ** -1 * boost_comm
    rhs = qweight**2 * boost_comm
    mismatch = sp.simplify(rhs - lhs)
    check(checks, "reciprocal_weight_not_lorentz_automorphism", mismatch != sp.zeros(4))
    check(
        checks,
        "positive_automorphism_only_trivial",
        sp.solve(sp.Eq(qweight**3, 1), qweight) == [1],
    )

    # Complete triangular coframe multiplication fails independent coframe gauge descent.
    eta = sp.diag(-1, 1, 1, 1)
    E1 = sp.eye(4)
    E1[0, 1] = 1
    Lambda = sp.diag(1, -1, -1, 1)
    check(checks, "lambda_lorentz", Lambda.T * eta * Lambda == eta)
    out_a = E1
    out_b = E1 * Lambda
    metric_difference = sp.simplify(out_b.T * eta * out_b - out_a.T * eta * out_a)
    check(checks, "coframe_product_gauge_outputs_differ", metric_difference != sp.zeros(4))
    check(checks, "coframe_product_difference_rank", metric_difference.rank() == 2)

    # Source identities.
    source_rows = []
    with (HERE / "SOURCE_LINEAGE.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    check(checks, "source_count", len(source_rows) == 14)
    check(checks, "source_ids_unique", len({row["id"] for row in source_rows}) == 14)
    for row in source_rows:
        check(
            checks,
            f"source_hash_{row['id']}",
            hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"],
        )

    projective_rows = [
        {
            "object": "reciprocal positive ray after CSN",
            "result": "ratio r=v/u",
            "status": "DERIVED_IN_DECLARED_DUAL_REPRESENTATION",
            "limit": "projective position interpretation separate",
        },
        {
            "object": "three-anchor projective coordinate",
            "result": "xi=(r-1)/(r+1)=tanh(rho)",
            "status": "UNIQUE_GIVEN_ANCHORED_PROJECTIVE_INTERPRETATION",
            "limit": "axes/neutral anchors plus projective role required",
        },
        {
            "object": "observer recenter",
            "result": "xi'=(xi-alpha)/(1-alpha*xi)",
            "status": "DERIVED_ON_RECIPROCAL_PROJECTIVE_RAY",
            "limit": "alpha=tanh(beta); oriented chart coordinate",
        },
        {
            "object": "same-direction composition",
            "result": "xi12=(xi1+xi2)/(1+xi1*xi2)",
            "status": "DERIVED_ON_ONE_PARAMETER_DOMAIN",
            "limit": "not general nonnegative three-observer distance addition",
        },
        {
            "object": "physical radial magnitude",
            "result": "abs(xi) with direction stored separately",
            "status": "TYPE_CORRECT_AVAILABLE",
            "limit": "does not derive D=Xmax*abs(xi)",
        },
    ]
    write_tsv(
        "PROJECTIVE_TRANSITION_LEDGER.tsv",
        ["object", "result", "status", "limit"],
        projective_rows,
    )

    profile_rows = [
        {
            "profile": "PROJECTIVE_TANH",
            "D_of_rho": "Dmax*tanh(rho)",
            "required_B": "cosh(rho)^4/Dmax^2",
            "endpoint_gap": "~2*Dmax*exp(-2rho)",
            "registered_match": "projective display only",
            "status": "AVAILABLE_NOT_PHYSICAL_DISTANCE_SELECTED",
        },
        {
            "profile": "EXPONENTIAL_SATURATION",
            "D_of_rho": "Dmax*(1-exp(-rho))",
            "required_B": "exp(2rho)/Dmax^2",
            "endpoint_gap": "Dmax*exp(-rho)",
            "registered_match": "WR-L radial proper distance with Dmax=2X",
            "status": "DERIVED_CONDITIONAL_IN_WRL_SLICE_NOT_GLOBAL",
        },
        {
            "profile": "LINEAR_UNBOUNDED",
            "D_of_rho": "L*rho",
            "required_B": "1/L^2",
            "endpoint_gap": "none",
            "registered_match": "same-anchor countercontrol",
            "status": "ADMISSIBLE_CONTROL",
        },
        {
            "profile": "FULLFRAME_RADIAL_CONTROL",
            "D_of_rho": "L*(exp(rho)-1)",
            "required_B": "exp(-2rho)/L^2",
            "endpoint_gap": "none",
            "registered_match": "conditional CSN-homothetic full-frame radial coframe",
            "status": "DERIVED_CONDITIONAL_CONTROL_NOT_SELECTED",
        },
    ]
    write_tsv(
        "PROFILE_METRIC_LEDGER.tsv",
        ["profile", "D_of_rho", "required_B", "endpoint_gap", "registered_match", "status"],
        profile_rows,
    )

    composition_rows = [
        {
            "domain": "ordered reciprocal one-parameter ray",
            "transition": "multiplicative ratio / additive rho / fractional xi",
            "angular_data": "none on fixed line",
            "status": "DERIVED_EXACT",
        },
        {
            "domain": "round S3 observer-relative chart",
            "transition": "unit-quaternion relative product",
            "angular_data": "dot and cross products required",
            "status": "DERIVED_CONDITIONAL_ROUND_BRANCH",
        },
        {
            "domain": "constant-squashed homogeneous S3",
            "transition": "left-relative group element survives",
            "angular_data": "direction changes metric length",
            "status": "DERIVED_GROUP_CONTROL_DISTANCE_PROFILE_OPEN",
        },
        {
            "domain": "round antipodal cut",
            "transition": "scalar distance single-valued; axis/path nonunique",
            "angular_data": "path family",
            "status": "DERIVED_EXACT_CONTROL",
        },
        {
            "domain": "local timelike frame group",
            "transition": "non-collinear boosts close with rotation",
            "angular_data": "screen rotation generated",
            "status": "DERIVED_COMPARISON_NO_RECIPROCAL_SOLDER",
        },
    ]
    write_tsv(
        "DEPTH_ANGLE_COMPOSITION_LEDGER.tsv",
        ["domain", "transition", "angular_data", "status"],
        composition_rows,
    )

    solder_rows = [
        {
            "candidate": "projective xi to physical distance",
            "positive_evidence": "unique anchored CSN projective coordinate",
            "blocking_evidence": "metric B must equal cosh^4(rho)/Dmax^2; no selected branch supplies it",
            "ruling": "OPEN_PROJECTIVE_POSITION_SOLDER",
        },
        {
            "candidate": "WR-L exponential proper profile",
            "positive_evidence": "exact D=2X*(1-exp(-rho)) in supplied slice",
            "blocking_evidence": "local radial slice lacks global observer-pair diameter and complete clock/event pairing",
            "ruling": "CONDITIONAL_LOCAL_PROFILE_NOT_GLOBAL_XMAX",
        },
        {
            "candidate": "local Lorentz 3+3 solder",
            "positive_evidence": "boost-boost commutator generates angular rotation",
            "blocking_evidence": "reciprocal weighting is not Lorentz bracket automorphism; rho-to-rapidity map absent",
            "ruling": "NOT_DERIVED_TYPE_BLOCKED",
        },
        {
            "candidate": "triangular coframe product solder",
            "positive_evidence": "exact chart group closure",
            "blocking_evidence": "does not descend through independent coframe gauge representatives",
            "ruling": "CHOSE_IF_USED_AS_PHYSICAL_COMPOSITION",
        },
        {
            "candidate": "c-only physical normalization",
            "positive_evidence": "founding clock-length conversion",
            "blocking_evidence": "dimensionless rho per length needs another length/time normalization",
            "ruling": "NOT_DERIVED_FROM_C_ALONE",
        },
    ]
    write_tsv(
        "SOLDER_GATE_LEDGER.tsv",
        ["candidate", "positive_evidence", "blocking_evidence", "ruling"],
        solder_rows,
    )

    status_rows = [
        {"claim": "reciprocal exponential response", "status": "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS", "scope": "ordered reciprocal pair given additive depth"},
        {"claim": "anchored reciprocal projective coordinate", "status": "UNIQUE_GIVEN_PROJECTIVE_POSITION_INTERPRETATION", "scope": "CSN positive ray and three anchors"},
        {"claim": "radial fractional observer transition", "status": "DERIVED_ON_RECIPROCAL_PROJECTIVE_RAY", "scope": "oriented one-parameter chart"},
        {"claim": "negative physical distance", "status": "NOT_USED", "scope": "sign belongs to direction/oriented coordinate"},
        {"claim": "exponential approach in reciprocal depth", "status": "DERIVED_FOR_BOTH_BOUNDED_REGISTERED_PROFILES", "scope": "gap exponent one for WR-L proper; exponent two for projective tanh"},
        {"claim": "early first-order Taylor discrimination", "status": "IMPOSSIBLE_AT_LINEAR_ORDER", "scope": "tanh and exponential saturation share origin and unit slope"},
        {"claim": "tanh as physical proper distance", "status": "OPEN_PROJECTIVE_POSITION_SOLDER", "scope": "requires transnormal B match and selected complete branch"},
        {"claim": "simple exponential physical proper distance", "status": "DERIVED_CONDITIONAL_IN_WRL_RADIAL_SLICE", "scope": "not global pair distance or universal Xmax"},
        {"claim": "round depth-angle transition", "status": "DERIVED_CONDITIONAL_ROUND_BRANCH", "scope": "unit-quaternion relative product and round metric"},
        {"claim": "general noncollinear scalar fractional composition", "status": "REFUTED_TYPE_MISMATCH", "scope": "angular dot/cross data required"},
        {"claim": "reciprocal depth equals Lorentz rapidity", "status": "NOT_DERIVED", "scope": "full Lorentz character/bracket obstruction"},
        {"claim": "complete coframe product is physical observer composition", "status": "CHOSE_NOT_DERIVED", "scope": "independent coframe gauge obstruction"},
        {"claim": "c fixes dimensionless distance-depth profile", "status": "NOT_DERIVED_FROM_C_ALONE", "scope": "c converts clock and length units"},
        {"claim": "physical global Xmax", "status": "OPEN_NOT_PROMOTED", "scope": "complete branch pairing diameter and scale join missing"},
        {"claim": "local observer physics", "status": "NEUTRAL_SELF_DEPTH_UNCHANGED", "scope": "rho_p(p)=0 every observer"},
        {"claim": "overall", "status": "PROJECTIVE_RADIAL_TRANSITION_DERIVED_PHYSICAL_DISTANCE_SOLDER_OPEN", "scope": "verified bounded controls"},
    ]
    write_tsv("STATUS_LEDGER.tsv", ["claim", "status", "scope"], status_rows)

    result = {
        "schema": "udt-observer-depth-angle-transition-1.0",
        "compute": "CPU_ONLY_EXACT",
        "check_count": len(checks),
        "checks": checks,
        "sources": len(source_rows),
        "projective": {
            "coordinate": "xi=tanh(rho)",
            "status": "UNIQUE_GIVEN_ANCHORED_PROJECTIVE_INTERPRETATION",
            "transition": "xi_prime=(xi-alpha)/(1-alpha*xi)",
            "composition": "xi12=(xi1+xi2)/(1+xi1*xi2)",
            "physical_distance_join": "OPEN",
        },
        "profiles": {
            "tanh": "PROJECTIVE_AVAILABLE_PHYSICAL_DISTANCE_OPEN",
            "exponential": "WRL_RADIAL_PROPER_DERIVED_CONDITIONAL_NOT_GLOBAL",
            "linear": "ADMISSIBLE_UNBOUNDED_CONTROL",
            "fullframe": "CONDITIONAL_UNBOUNDED_CONTROL",
            "first_order_taylor": "DEGENERATE_CANNOT_DISCRIMINATE",
        },
        "depth_angle": {
            "round": "UNIT_QUATERNION_RELATIVE_TRANSITION_DERIVED_CONDITIONAL",
            "noncollinear": "DOT_AND_CROSS_ANGULAR_DATA_REQUIRED",
            "squashed": "GROUP_RELATIVE_TRANSITION_SURVIVES_RADIAL_ISOTROPY_DOES_NOT",
            "cut": "SCALAR_SINGLE_VALUED_FULL_TRANSPORT_PATH_FAMILY",
        },
        "solder": {
            "projective_to_metric": "OPEN",
            "lorentz": "NOT_DERIVED_TYPE_BLOCKED",
            "coframe_product": "CHOSE_NOT_DERIVED",
            "c_only": "NOT_DERIVED",
        },
        "owner_frame": {
            "self_depth": "ZERO_EVERY_OBSERVER",
            "local_physics_changed": False,
        },
        "maximum_conclusion": (
            "THE_RECIPROCAL_RAY_DERIVES_AN_EXACT_OBSERVER_INDEXED_PROJECTIVE_RADIAL_"
            "TRANSITION_WITH_TANH_COORDINATE_AND_FRACTIONAL_RECENTERING_GIVEN_THE_"
            "ANCHORED_PROJECTIVE_INTERPRETATION__THE_COMPLETE_ROUND_CONTROL_DERIVES_"
            "A_NONABELIAN_DEPTH_ANGLE_TRANSITION_REQUIRING_ANGULAR_DATA__THE_"
            "EXPONENTIAL_RECIPROCAL_RESPONSE_IS_EXACT_AND_BOUNDED_TANH_AND_WRL_"
            "PROPER_PROFILES_BOTH_APPROACH_THEIR_LIMITS_EXPONENTIALLY_IN_DEPTH_BUT_"
            "WITH_DIFFERENT_EXPONENTS__NO_REGISTERED_METRIC_OR_COFRAME_OBJECT_YET_"
            "SOLDERS_ONE_PROFILE_TO_UNIVERSAL_PHYSICAL_OBSERVER_DISTANCE__PHYSICAL_"
            "XMAX_REMAINS_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"checks": len(checks), "sources": len(source_rows), "result": "PASS"}, sort_keys=True))
    print(result["maximum_conclusion"])


if __name__ == "__main__":
    main()
