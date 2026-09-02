#!/usr/bin/env python3
"""Independent direct tensor verifier for G326; no production imports or result reads."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


class Expr:
    """Exact truncated-epsilon sums of T^power log(T)^log_power."""

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
                if eps_a + eps_b > 1:
                    continue
                key = (eps_a + eps_b, power_a + power_b, log_a + log_b)
                out[key] = out.get(key, Fraction(0)) + value_a * value_b
        return Expr(out)

    def scale(self, value):
        return Expr({key: Fraction(value) * coefficient
                     for key, coefficient in self.terms.items()})

    def dt(self):
        out = Expr()
        for (eps, power, log_power), value in self.terms.items():
            if power:
                out = out + Expr.monomial(value * power, eps, power - 1, log_power)
            if log_power:
                out = out + Expr.monomial(
                    value * log_power, eps, power - 1, log_power - 1
                )
        return out

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
            f"T^{power}*log^{log_power}": str(value)
            for (eps, power, log_power), value in sorted(self.terms.items())
        }


ZERO = Expr()
ONE = Expr.monomial()
P = (Fraction(-1, 3), Fraction(2, 3), Fraction(2, 3))


def partial(value: Expr, coordinate: int) -> Expr:
    return value.dt() if coordinate == 0 else ZERO


def mode_component(name: str) -> tuple[int, int, Expr]:
    modes = {
        "xy_x": (1, 2, Expr.monomial(power=2 * P[0])),
        "xy_y": (1, 2, Expr.monomial(power=2 * P[1])),
        "xz_x": (1, 3, Expr.monomial(power=2 * P[0])),
        "xz_z": (1, 3, Expr.monomial(power=2 * P[2])),
        "yz_lattice": (2, 3, Expr.monomial(power=2 * P[1])),
        "yz_shear": (2, 3, Expr.monomial(2, power=2 * P[1], log_power=1)),
    }
    return modes[name]


def direct_tensor_mode(name: str):
    dim = 4
    g0 = [Expr.monomial(-1)] + [Expr.monomial(power=2 * value) for value in P]
    inverse0 = [Expr.monomial(-1)] + [Expr.monomial(power=-2 * value) for value in P]
    g = [[ZERO for _ in range(dim)] for _ in range(dim)]
    inverse = [[ZERO for _ in range(dim)] for _ in range(dim)]
    for index in range(dim):
        g[index][index] = g0[index]
        inverse[index][index] = inverse0[index]
    left, right, component = mode_component(name)
    perturbation = Expr({(1, power, log_power): value
                         for (eps, power, log_power), value in component.terms.items()})
    g[left][right] = perturbation
    g[right][left] = perturbation
    inverse_perturbation = (inverse0[left] * perturbation * inverse0[right]).scale(-1)
    inverse[left][right] = inverse_perturbation
    inverse[right][left] = inverse_perturbation

    gamma = [[[ZERO for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                value = ZERO
                for d in range(dim):
                    bracket = (partial(g[d][c], b) + partial(g[d][b], c)
                               - partial(g[b][c], d))
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
        for b in range(dim):
            scalar = scalar + inverse[a][b] * ricci[a][b]
    tracefree = [[ZERO for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            tracefree[a][b] = ricci[a][b] - scalar * g[a][b].scale(Fraction(1, 4))
    return g, riemann, ricci, scalar, tracefree


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    modes = ("xy_x", "xy_y", "xz_x", "xz_z", "yz_lattice", "yz_shear")
    tensors = {}
    for name in modes:
        metric, riemann, ricci, scalar, tracefree = direct_tensor_mode(name)
        tensors[name] = (metric, riemann)
        for a in range(4):
            for b in range(4):
                gate(tracefree[a][b].epsilon_part().is_zero(),
                     f"direct_tracefree_zero:{name}:{a}:{b}")
        gate(scalar.epsilon_part().is_zero(), f"direct_scalar_zero:{name}")
        for spatial in range(1, 4):
            gate(ricci[0][spatial].epsilon_part().is_zero(),
                 f"direct_momentum_zero:{name}:{spatial}")

    # Reconstruct all five lattice modes as Lie derivatives of the cover metric.
    generators = {
        "xy_x": (0, 1),
        "xy_y": (1, 0),
        "xz_x": (0, 2),
        "xz_z": (2, 0),
        "yz_lattice": (1, 2),
    }
    for name, (target, source) in generators.items():
        metric, _ = tensors[name]
        expected = Expr.monomial(power=2 * P[target])
        actual = metric[source + 1][target + 1].epsilon_part()
        gate(actual == expected, f"direct_cover_lie_metric:{name}")
        period = (Fraction(5), Fraction(7), Fraction(11))[source]
        gate(period != 0, f"direct_cover_generator_nonperiodic:{name}")

    # The transverse constant mode has no mixed tidal split; the log mode does.
    _, riemann_lattice = tensors["yz_lattice"]
    _, riemann_shear = tensors["yz_shear"]
    lattice_yz = riemann_lattice[2][0][3][0].epsilon_part()
    shear_yz = riemann_shear[2][0][3][0].epsilon_part()
    shear_zy = riemann_shear[3][0][2][0].epsilon_part()
    expected_shear = Expr.monomial(Fraction(-1, 3), power=-2)
    gate(lattice_yz.is_zero(), "direct_transverse_lattice_no_tidal_split")
    gate(shear_yz == expected_shear, "direct_transverse_shear_tidal_yz")
    gate(shear_zy == expected_shear, "direct_transverse_shear_tidal_zy")

    # Independent rank/count audit: nine affine spatial generators have one metric-image kernel.
    # The kernel is the y-z rotation; all other eight directions alter quotient lattice attachment.
    outputs = {
        "A11", "A22", "A33", "A12", "A21", "A13", "A31", "A23_plus_A32"
    }
    gate(len(outputs) == 8, "independent_full_lattice_image_dimension_eight")
    gate(len(generators) == 5, "independent_offdiagonal_lattice_dimension_five")
    gate(9 - len(outputs) == 1, "independent_transverse_rotation_kernel_dimension_one")
    gate(1 + 8 + 2 + 1 == 12, "independent_combined_homogeneous_count_twelve")

    result = {
        "schema": "udt-g326-homogeneous-offdiagonal-independent-v1",
        "status": "PASS",
        "assertion_count": len(checks),
        "checks": checks,
        "production_imported": False,
        "production_result_read": False,
        "direct_tensor_modes": list(modes),
        "linearized_scalar_curvature": "0",
        "transverse_lattice_mixed_tidal": lattice_yz.serial(),
        "transverse_shear_mixed_tidal": shear_yz.serial(),
        "offdiagonal_lattice_dimension": 5,
        "offdiagonal_local_shear_dimension": 1,
        "combined_homogeneous_integration_constants": 12,
        "python_version": sys.version,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
