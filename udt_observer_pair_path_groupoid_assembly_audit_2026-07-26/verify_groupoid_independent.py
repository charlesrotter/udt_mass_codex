#!/usr/bin/env python3
"""Independent Fraction-only observer-pair groupoid verification."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def diag(*values):
    return [[F(values[i]) if i == j else F(0) for j in range(len(values))] for i in range(len(values))]


ETA = diag(-1, 1, 1, 1)


def lorentz_inverse(value):
    return matmul(matmul(ETA, transpose(value)), ETA)


def conjugate(transform, value):
    return matmul(matmul(transform, value), lorentz_inverse(transform))


def boost(i):
    value = eye(4)
    value[0][0] = F(5, 4)
    value[0][i] = F(3, 4)
    value[i][0] = F(3, 4)
    value[i][i] = F(5, 4)
    return value


def rotation(i, j):
    value = eye(4)
    value[i][i] = F(3, 5)
    value[i][j] = F(-4, 5)
    value[j][i] = F(4, 5)
    value[j][j] = F(3, 5)
    return value


def generator(lam):
    return diag(-1, 1, lam, lam)


def character(lam, q):
    q = F(q)
    return diag(1 / q, q, q**lam, q**lam)


def is_lorentz(value):
    return matmul(matmul(transpose(value), ETA), value) == ETA


def check(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main():
    checks = {}
    lambdas = (-2, -1, 0, 1, 2)
    Rscreen = rotation(2, 3)
    Vdir = rotation(1, 2)
    Vobs = boost(2)
    Uab = boost(2)
    Ubc = rotation(1, 3)
    Uac = matmul(Ubc, Uab)

    check("independent_screen_rotation_Lorentz", is_lorentz(Rscreen), checks)
    check("independent_direction_rotation_Lorentz", is_lorentz(Vdir), checks)
    check("independent_observer_boost_Lorentz", is_lorentz(Vobs), checks)
    check("independent_path_maps_Lorentz", is_lorentz(Uab) and is_lorentz(Ubc) and is_lorentz(Uac), checks)

    typed_composition_passes = 0
    screen_gauge_passes = 0
    vertical_composition_passes = 0
    direction_untyped_matches = []
    for lam in lambdas:
        X = generator(lam)
        check(f"screen_commutes_lambda_{lam}", matmul(Rscreen, X) == matmul(X, Rscreen), checks)
        screen_gauge_passes += 1

        Xb = conjugate(Uab, X)
        Xc_seq = conjugate(Ubc, Xb)
        Xc_direct = conjugate(Uac, X)
        check(f"path_conjugation_lambda_{lam}", Xc_seq == Xc_direct, checks)

        Da = character(lam, F(2))
        Db = character(lam, F(3))
        Dab = character(lam, F(6))
        Db_at_B = conjugate(Uab, Db)
        Tab = matmul(Uab, Da)
        Tbc = matmul(Ubc, Db_at_B)
        Tac = matmul(Uac, Dab)
        check(f"typed_composition_lambda_{lam}", matmul(Tbc, Tab) == Tac, checks)
        typed_composition_passes += 1

        Vb = conjugate(Uab, Vdir)
        Db_out = conjugate(Vb, Db_at_B)
        typed_vertical = matmul(matmul(matmul(matmul(Ubc, Db_out), Vb), Uab), Da)
        expected_vertical = matmul(matmul(matmul(Ubc, Vb), Uab), Dab)
        check(f"vertical_composition_lambda_{lam}", typed_vertical == expected_vertical, checks)
        vertical_composition_passes += 1

        untyped = matmul(matmul(matmul(Ubc, Db_out), Uab), Da)
        untyped_expected = matmul(Uac, Dab)
        direction_untyped_matches.append((lam, untyped == untyped_expected))

    check("independent_all_five_screen_gauges", screen_gauge_passes == 5, checks)
    check("independent_all_five_typed_compositions", typed_composition_passes == 5, checks)
    check("independent_all_five_vertical_compositions", vertical_composition_passes == 5, checks)
    check("independent_direction_reset_only_lambda_one", direction_untyped_matches == [(-2, False), (-1, False), (0, False), (1, True), (2, False)], checks)

    X1 = generator(1)
    check("independent_lambda_one_observer_dependence", conjugate(Vobs, X1) != X1, checks)
    bare_event_independent = [lam for lam in lambdas if conjugate(Vdir, generator(lam)) == generator(lam) and conjugate(Vobs, generator(lam)) == generator(lam)]
    check("independent_no_tested_lambda_bare_event", bare_event_independent == [], checks)

    # Endpoint-only potential differences: exhaustive 5^3 finite control.
    potential_triangles = 0
    for pa, pb, pc in product(range(-2, 3), repeat=3):
        dab, dbc, dac = pb - pa, pc - pb, pc - pa
        check(f"potential_triangle_{potential_triangles}", dab + dbc == dac and -dab == pa - pb, checks)
        potential_triangles += 1
    check("independent_125_potential_triangles", potential_triangles == 125, checks)

    # Any finite endpoint cocycle can be reconstructed from a basepoint row.
    endpoint_values = {"O": 0, "A": 2, "B": -1, "C": 3}
    deltas = {(left, right): endpoint_values[right] - endpoint_values[left] for left in endpoint_values for right in endpoint_values}
    reconstructed = {name: deltas[("O", name)] for name in endpoint_values}
    check("independent_basepoint_reconstruction", all(deltas[(left, right)] == reconstructed[right] - reconstructed[left] for left in endpoint_values for right in endpoint_values), checks)

    symmetric_odd_values = [value for value in range(0, 6) if value == -value]
    check("independent_symmetric_odd_only_zero", symmetric_odd_values == [0], checks)

    # Faithful positive real character and metric-isometry controls.
    q_values = (F(1, 3), F(1, 2), F(1), F(2), F(3))
    identity_q = [q for q in q_values if character(0, q) == eye(4)]
    lorentz_q = [q for q in q_values if matmul(matmul(transpose(character(0, q)), ETA), character(0, q)) == ETA]
    check("independent_only_unit_character_period", identity_q == [F(1)], checks)
    check("independent_only_zero_depth_character_is_Lorentz", lorentz_q == [F(1)], checks)

    # Centralizing versus noncentralizing loop transport.
    X0 = generator(0)
    Hscreen = Rscreen
    Hbase = boost(1)
    check("independent_screen_holonomy_equal", conjugate(Hscreen, X0) == X0, checks)
    check("independent_base_holonomy_different", conjugate(Hbase, X0) != X0, checks)
    check("independent_holonomy_reversal", conjugate(lorentz_inverse(Hbase), conjugate(Hbase, X0)) == X0, checks)

    summary = {name: value for name, value in checks.items() if not name.startswith(("screen_commutes_lambda_", "path_conjugation_lambda_", "typed_composition_lambda_", "vertical_composition_lambda_", "potential_triangle_"))}
    census_check_count = len(checks) - len(summary)
    result = {
        "schema": "udt-observer-pair-path-groupoid-independent-1.0",
        "result": "PASS",
        "summary_check_count": len(summary),
        "census_check_count": census_check_count,
        "checks": summary,
        "counts": {
            "lambda_values_tested": len(lambdas),
            "screen_gauge_passes": screen_gauge_passes,
            "typed_composition_passes": typed_composition_passes,
            "vertical_composition_passes": vertical_composition_passes,
            "direction_reset_matches": sum(1 for _, matched in direction_untyped_matches if matched),
            "bare_event_independent_lambda_values": len(bare_event_independent),
            "potential_triangles_tested": potential_triangles,
            "positive_character_factors_tested": len(q_values),
            "identity_character_factors": len(identity_q),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

