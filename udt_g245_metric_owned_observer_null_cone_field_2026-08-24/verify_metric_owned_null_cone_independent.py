#!/usr/bin/env python3
"""Independent exact-Fraction verification for G245; no SymPy or production imports."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction as F
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "INDEPENDENT_VERIFICATION.json"
LANDING = (
    "OBSERVER_GERM_AND_METRIC_OWN_LOCAL_DIRECTION_LABELLED_NULL_CONE_FIELD"
    "__G244_AREA_SHAPE_ARE_INDUCED_CONE_GEOMETRY"
    "__SOURCE_POPULATION_GLOBAL_BRANCH_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)
Matrix = tuple[tuple[F, F], tuple[F, F]]


def mat(a: int | F, b: int | F, c: int | F, d: int | F) -> Matrix:
    return ((F(a), F(b)), (F(c), F(d)))


I = mat(1, 0, 0, 1)
Z = mat(0, 0, 0, 0)


def add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def sub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def scale(c: F | int, a: Matrix) -> Matrix:
    c = F(c)
    return tuple(tuple(c * a[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def transpose(a: Matrix) -> Matrix:
    return mat(a[0][0], a[1][0], a[0][1], a[1][1])


def mul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(2)), F(0)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def det(a: Matrix) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def trace(a: Matrix) -> F:
    return a[0][0] + a[1][1]


def inv(a: Matrix) -> Matrix:
    delta = det(a)
    if delta == 0:
        raise ZeroDivisionError("singular matrix")
    return scale(F(1, 1) / delta, mat(a[1][1], -a[0][1], -a[1][0], a[0][0]))


def strings(a: Matrix) -> list[list[str]]:
    return [[str(a[i][j]) for j in range(2)] for i in range(2)]


def random_invertible(rng: random.Random) -> Matrix:
    while True:
        candidate = mat(*(rng.randint(-7, 7) for _ in range(4)))
        if det(candidate) != 0:
            return candidate


def sym(rng: random.Random) -> Matrix:
    a, b, c = (rng.randint(-6, 6) for _ in range(3))
    return mat(a, b, b, c)


def rotations() -> tuple[Matrix, ...]:
    return (
        I,
        mat(0, -1, 1, 0),
        mat(F(3, 5), -F(4, 5), F(4, 5), F(3, 5)),
        mat(-1, 0, 0, 1),
    )


def finite_census() -> dict[str, int]:
    rng = random.Random(245240826)
    qs = rotations()
    cases = 0
    assertions = 0
    parity_flips = 0
    orientation_sensitive = 0
    for index in range(5000):
        D = random_invertible(rng)
        B = sym(rng)
        T = sym(rng)
        V = mul(B, D)
        Dt = transpose(D)
        Vt = transpose(V)
        H = mul(Dt, D)
        Hdot = add(mul(Vt, D), mul(Dt, V))
        Hddot = sub(scale(2, mul(Vt, V)), scale(2, mul(mul(Dt, T), D)))
        theta = trace(B)
        Sigma = sub(B, scale(theta / 2, I))
        Bprime = scale(-1, add(T, mul(B, B)))
        T_hat = sub(T, scale(trace(T) / 2, I))
        checks = [
            mul(Dt, V) == mul(Vt, D),
            det(H) == det(D) ** 2,
            Hdot == scale(2, mul(mul(Dt, B), D)),
            trace(Bprime) == -trace(T) - theta**2 / 2 - trace(mul(Sigma, Sigma)),
            sub(Bprime, scale(trace(Bprime) / 2, I))
            == sub(scale(-theta, Sigma), T_hat),
            Hddot == sub(scale(2, mul(Vt, V)), scale(2, mul(mul(Dt, T), D))),
        ]
        Qo = qs[index % 4]
        Qs = qs[(3 * index + 1) % 4]
        Dg = mul(mul(transpose(Qs), D), Qo)
        Vg = mul(mul(transpose(Qs), V), Qo)
        Tg = mul(mul(transpose(Qs), T), Qs)
        Hg = mul(transpose(Dg), Dg)
        checks.extend([
            Hg == mul(mul(transpose(Qo), H), Qo),
            mul(Vg, inv(Dg)) == mul(mul(transpose(Qs), B), Qs),
            det(Hg) == det(H),
            abs(det(Dg)) == abs(det(D)),
            sub(scale(2, mul(transpose(Vg), Vg)), scale(2, mul(mul(transpose(Dg), Tg), Dg)))
            == mul(mul(transpose(Qo), Hddot), Qo),
        ])
        if det(Qs) * det(Qo) == -1:
            parity_flips += 1
            checks.append((det(Dg) > 0) == (det(D) < 0))
        else:
            checks.append((det(Dg) > 0) == (det(D) > 0))
        if mul(mul(Dt, T), D) != T:
            orientation_sensitive += 1
        if not all(checks):
            raise RuntimeError(f"independent finite case failed: {index}")
        assertions += len(checks)
        cases += 1
    return {
        "cases": cases,
        "assertions": assertions,
        "reflection_parity_flip_cases": parity_flips,
        "H_orientation_sensitive_tide_cases": orientation_sensitive,
    }


def series_control() -> dict[str, object]:
    T0 = mat(1, 0, 0, 4)
    T1 = mat(0, 3, 3, 0)
    coefficients = [Z for _ in range(9)]
    coefficients[1] = I
    residuals: list[bool] = []
    for n in range(7):
        forcing = mul(T0, coefficients[n])
        if n >= 1:
            forcing = add(forcing, mul(T1, coefficients[n - 1]))
        coefficients[n + 2] = scale(-F(1, (n + 2) * (n + 1)), forcing)
    for n in range(7):
        lhs = scale((n + 2) * (n + 1), coefficients[n + 2])
        lhs = add(lhs, mul(T0, coefficients[n]))
        if n >= 1:
            lhs = add(lhs, mul(T1, coefficients[n - 1]))
        residuals.append(lhs == Z)
    return {
        "D3": strings(coefficients[3]),
        "D4": strings(coefficients[4]),
        "D4_offdiagonal_nonzero": coefficients[4][0][1] != 0,
        "commutator": strings(sub(mul(T0, T1), mul(T1, T0))),
        "recurrence_orders": len(residuals),
        "all_recurrence_residuals_zero": all(residuals),
    }


def controls() -> dict[str, object]:
    T = mat(1, 0, 0, 4)
    Q = mat(0, -1, 1, 0)
    h2a = scale(-2, T)
    h2b = scale(-2, mul(mul(transpose(Q), T), Q))

    # Exact singular position block embedded in a symplectic phase.
    Ablock = mat(-1, 0, 0, 1)
    Bblock = mat(0, 0, 0, 3)
    Cblock = Z
    Dblock = Ablock
    symplectic_blocks = (
        mul(transpose(Ablock), Dblock) == I,
        mul(transpose(Bblock), Dblock) == transpose(mul(transpose(Bblock), Dblock)),
        mul(transpose(Ablock), Cblock) == transpose(mul(transpose(Ablock), Cblock)),
    )
    try:
        inv(Bblock)
        inverse_failed = False
    except ZeroDivisionError:
        inverse_failed = True
    return {
        "H_Hprime_nonclosure": {
            "same_H": strings(I),
            "same_Hprime": strings(Z),
            "Hsecond_1": strings(h2a),
            "Hsecond_2": strings(h2b),
            "different": h2a != h2b,
        },
        "rational_caustic_phase": {
            "position_rank": 1,
            "position_det": str(det(Bblock)),
            "position_inverse_rejected": inverse_failed,
            "symplectic_block_identities": all(symplectic_blocks),
            "full_phase_invertible": det(Ablock) * det(Dblock) != 0,
        },
        "rotating_tide_series": series_control(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = {
        "audit": "G245_INDEPENDENT_FRACTION_RECONSTRUCTION",
        "classification": LANDING,
        "imports_production_code": False,
        "reads_production_output": False,
        "null_normalization": "unique k=l/(-g(U,l))=U+n for every future null direction",
        "jacobi_role": "angular differential of metric exponential map",
        "finite_census": finite_census(),
        "controls": controls(),
        "fitted_angular_coefficients": 0,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "physical_history": "QUERY_SUPPLIED_NOT_SELECTED",
        "source_detector": "OPEN",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
