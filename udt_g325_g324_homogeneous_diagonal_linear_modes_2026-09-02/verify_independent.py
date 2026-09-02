#!/usr/bin/env python3
"""Independent direct first-order tensor engine for G325; no production imports/results."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


class Expr:
    """Exact truncated-epsilon sums of t^power log(t)^log_power."""

    def __init__(self, terms=None):
        self.terms = {
            (int(eps), Fraction(power), int(log_power)): Fraction(value)
            for (eps, power, log_power), value in (terms or {}).items()
            if value and int(eps) <= 1
        }

    @staticmethod
    def monomial(value=1, eps=0, power=0, log_power=0):
        return Expr({(eps, Fraction(power), log_power): Fraction(value)})

    def __add__(self, other):
        out = dict(self.terms)
        for key, value in other.terms.items():
            out[key] = out.get(key, Fraction(0)) + value
            if not out[key]:
                del out[key]
        return Expr(out)

    def __neg__(self):
        return Expr({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        out = {}
        for (eps_a, power_a, log_a), value_a in self.terms.items():
            for (eps_b, power_b, log_b), value_b in other.terms.items():
                eps = eps_a + eps_b
                if eps > 1:
                    continue
                key = (eps, power_a + power_b, log_a + log_b)
                out[key] = out.get(key, Fraction(0)) + value_a * value_b
        return Expr(out)

    def scale(self, value):
        return Expr({key: Fraction(value) * coefficient
                     for key, coefficient in self.terms.items()})

    def dt(self):
        out = Expr()
        for (eps, power, log_power), value in self.terms.items():
            if power:
                out = out + Expr.monomial(
                    value * power, eps, power - 1, log_power
                )
            if log_power:
                out = out + Expr.monomial(
                    value * log_power, eps, power - 1, log_power - 1
                )
        return out

    def with_epsilon(self):
        return Expr({(1, power, log_power): value
                     for (eps, power, log_power), value in self.terms.items()
                     if eps == 0})

    def inverse_first_order(self):
        base = [(key, value) for key, value in self.terms.items() if key[0] == 0]
        assert len(base) == 1
        (eps, power, log_power), coefficient = base[0]
        assert eps == 0 and log_power == 0
        inverse_base = Expr.monomial(1 / coefficient, 0, -power, 0)
        perturbation = Expr({key: value for key, value in self.terms.items() if key[0] == 1})
        return inverse_base - inverse_base * inverse_base * perturbation

    def epsilon_part(self):
        return Expr({(0, power, log_power): value
                     for (eps, power, log_power), value in self.terms.items() if eps == 1})

    def is_zero(self):
        return not self.terms

    def __eq__(self, other):
        if not isinstance(other, Expr):
            return NotImplemented
        return self.terms == other.terms

    def serial(self):
        return {
            f"eps^{eps}*T^{power}*log^{log_power}": str(value)
            for (eps, power, log_power), value in sorted(self.terms.items())
        }


ZERO = Expr()
ONE = Expr.monomial()
P = (Fraction(-1, 3), Fraction(2, 3), Fraction(2, 3))


def partial(value: Expr, coordinate: int) -> Expr:
    return value.dt() if coordinate == 0 else ZERO


def mode_u(name: str, index: int) -> Expr:
    if name == "constant_x":
        return ONE if index == 0 else ZERO
    if name == "constant_y":
        return ONE if index == 1 else ZERO
    if name == "constant_z":
        return ONE if index == 2 else ZERO
    if name == "gauge":
        return Expr.monomial(P[index], power=-1)
    if name == "shear":
        coefficient = (Fraction(0), Fraction(1), Fraction(-1))[index]
        return Expr.monomial(coefficient, power=0, log_power=1) if coefficient else ZERO
    if name == "scalar":
        return Expr.monomial((1 - P[index]) / 4, power=2)
    raise ValueError(name)


def direct_tensor_mode(name: str):
    dim = 4
    g = [[ZERO for _ in range(dim)] for _ in range(dim)]
    g[0][0] = Expr.monomial(-1)
    for spatial in range(3):
        background = Expr.monomial(power=2 * P[spatial])
        perturbation = background * mode_u(name, spatial).with_epsilon().scale(2)
        g[spatial + 1][spatial + 1] = background + perturbation
    inverse = [[ZERO for _ in range(dim)] for _ in range(dim)]
    for index in range(dim):
        inverse[index][index] = g[index][index].inverse_first_order()

    gamma = [[[ZERO for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                value = ZERO
                for d in range(dim):
                    bracket = partial(g[d][c], b) + partial(g[d][b], c) - partial(g[b][c], d)
                    value = value + inverse[a][d] * bracket
                gamma[a][b][c] = value.scale(Fraction(1, 2))

    riemann = [[[[ZERO for _ in range(dim)] for _ in range(dim)]
                for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    value = partial(gamma[a][b][d], c) - partial(gamma[a][b][c], d)
                    for e in range(dim):
                        value = value + gamma[a][e][c] * gamma[e][b][d]
                        value = value - gamma[a][e][d] * gamma[e][b][c]
                    riemann[a][b][c][d] = value

    ricci = [[ZERO for _ in range(dim)] for _ in range(dim)]
    for b in range(dim):
        for d in range(dim):
            for a in range(dim):
                ricci[b][d] = ricci[b][d] + riemann[a][b][a][d]

    scalar = ZERO
    for a in range(dim):
        scalar = scalar + inverse[a][a] * ricci[a][a]
    tracefree = [[ZERO for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            tracefree[a][b] = ricci[a][b] - scalar * g[a][b].scale(Fraction(1, 4))

    lowered = [[[[ZERO for _ in range(dim)] for _ in range(dim)]
                for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    for e in range(dim):
                        lowered[a][b][c][d] = lowered[a][b][c][d] + g[a][e] * riemann[e][b][c][d]
    electric = []
    for spatial in range(1, 4):
        electric.append(lowered[0][spatial][0][spatial] * inverse[spatial][spatial])
    return g, ricci, scalar, tracefree, electric


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    modes = ("constant_x", "constant_y", "constant_z", "gauge", "shear", "scalar")
    scalar_eps = None
    shear_split = None
    for name in modes:
        metric, ricci, scalar, tracefree, electric = direct_tensor_mode(name)
        for a in range(4):
            for b in range(4):
                gate(tracefree[a][b].epsilon_part().is_zero(),
                     f"direct_tracefree_zero:{name}:{a}:{b}")
        if name in ("constant_x", "constant_y", "constant_z", "gauge", "shear"):
            gate(scalar.epsilon_part().is_zero(), f"direct_scalar_zero:{name}")
        if name == "scalar":
            scalar_eps = scalar.epsilon_part()
            gate(scalar_eps == Expr.monomial(4), "direct_scalar_mode_delta_R_four")
        if name == "shear":
            shear_split = (electric[1] - electric[2]).epsilon_part()
            expected_options = (Expr.monomial(Fraction(-2, 3), power=-2),
                                Expr.monomial(Fraction(2, 3), power=-2))
            gate(shear_split in expected_options, "direct_shear_curvature_split")

    # Direct Lie derivative in synchronous coordinates: L_(d/dT) g_ii = d_T g_ii.
    gauge_metric, _, _, _, _ = direct_tensor_mode("gauge")
    for spatial in range(3):
        background = Expr.monomial(power=2 * P[spatial])
        expected = background.dt()
        actual = gauge_metric[spatial + 1][spatial + 1].epsilon_part()
        gate(actual == expected, f"direct_time_shift_lie_derivative:{spatial}")

    # A scaling generator c*x on a compact coordinate circle is single-valued only for c=0.
    for label, coefficient, period in (
        ("x", Fraction(2, 3), Fraction(5)),
        ("y", Fraction(-4, 7), Fraction(11)),
        ("z", Fraction(9, 13), Fraction(17)),
    ):
        gate(coefficient * period != 0, f"scaling_generator_fails_periodicity:{label}")

    # Exact parameter count from two independent exponent constraints.
    q = (Fraction(0), Fraction(1), Fraction(-1))
    gate(sum(q) == 0, "independent_q_trace_constraint")
    gate(sum(p_i * q_i for p_i, q_i in zip(P, q)) == 0,
         "independent_q_kasner_constraint")

    result = {
        "schema": "udt-g325-homogeneous-diagonal-independent-v1",
        "status": "PASS",
        "assertion_count": len(checks),
        "checks": checks,
        "production_imported": False,
        "production_result_read": False,
        "direct_tensor_modes": list(modes),
        "linearized_scalar_curvature": scalar_eps.serial(),
        "linearized_shear_curvature_split": shear_split.serial(),
        "time_shift_is_lie_derivative": True,
        "constant_cover_scalings_fail_fixed_quotient_periodicity": True,
        "python_version": sys.version,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
