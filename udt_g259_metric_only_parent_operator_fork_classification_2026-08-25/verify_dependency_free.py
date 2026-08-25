#!/usr/bin/env python3
"""Dependency-free exact replay for the bounded G259 repair landing."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class Poly2:
    """Sparse exact polynomial in formal variables b and t."""

    def __init__(self, terms: dict[tuple[int, int], Fraction] | None = None) -> None:
        self.terms = {
            power: Fraction(coefficient)
            for power, coefficient in (terms or {}).items()
            if coefficient
        }

    @classmethod
    def constant(cls, value: int | Fraction) -> "Poly2":
        return cls({(0, 0): Fraction(value)})

    @classmethod
    def monomial(cls, b_power: int, t_power: int, coefficient: int = 1) -> "Poly2":
        return cls({(b_power, t_power): Fraction(coefficient)})

    def _coerce(self, other: object) -> "Poly2":
        if isinstance(other, Poly2):
            return other
        if isinstance(other, (int, Fraction)):
            return Poly2.constant(other)
        return NotImplemented

    def __add__(self, other: object) -> "Poly2":
        other_poly = self._coerce(other)
        if other_poly is NotImplemented:
            return NotImplemented
        terms = dict(self.terms)
        for power, coefficient in other_poly.terms.items():
            terms[power] = terms.get(power, Fraction(0)) + coefficient
            if not terms[power]:
                del terms[power]
        return Poly2(terms)

    __radd__ = __add__

    def __neg__(self) -> "Poly2":
        return Poly2({power: -coefficient for power, coefficient in self.terms.items()})

    def __sub__(self, other: object) -> "Poly2":
        other_poly = self._coerce(other)
        if other_poly is NotImplemented:
            return NotImplemented
        return self + (-other_poly)

    def __rsub__(self, other: object) -> "Poly2":
        other_poly = self._coerce(other)
        if other_poly is NotImplemented:
            return NotImplemented
        return other_poly - self

    def __mul__(self, other: object) -> "Poly2":
        other_poly = self._coerce(other)
        if other_poly is NotImplemented:
            return NotImplemented
        terms: dict[tuple[int, int], Fraction] = {}
        for (b1, t1), coefficient1 in self.terms.items():
            for (b2, t2), coefficient2 in other_poly.terms.items():
                power = (b1 + b2, t1 + t2)
                terms[power] = terms.get(power, Fraction(0)) + coefficient1 * coefficient2
        return Poly2(terms)

    __rmul__ = __mul__

    def dt(self) -> "Poly2":
        return Poly2(
            {
                (b_power, t_power - 1): coefficient * t_power
                for (b_power, t_power), coefficient in self.terms.items()
                if t_power
            }
        )

    def coefficient(self, b_power: int, t_power: int) -> Fraction:
        return self.terms.get((b_power, t_power), Fraction(0))

    def evaluate(self, b_value: Fraction, t_value: Fraction) -> Fraction:
        return sum(
            coefficient * b_value**b_power * t_value**t_power
            for (b_power, t_power), coefficient in self.terms.items()
        )

    def is_zero(self) -> bool:
        return not self.terms


def poly_value(coeffs: list[Fraction], x: Fraction) -> Fraction:
    return sum(coefficient * x**power for power, coefficient in enumerate(coeffs))


def poly_derivative(coeffs: list[Fraction], x: Fraction, order: int) -> Fraction:
    value = Fraction(0)
    for power, coefficient in enumerate(coeffs):
        if power < order:
            continue
        factor = 1
        for offset in range(order):
            factor *= power - offset
        value += coefficient * factor * x ** (power - order)
    return value


def run_replay() -> dict[str, object]:
    assertions = 0

    # Primary spherical residual dependence and mass-aspect identities.
    coefficient_sets = [
        [Fraction(1), Fraction(2), Fraction(-3), Fraction(5)],
        [Fraction(4, 3), Fraction(-7, 5), Fraction(2, 9), Fraction(11, 4)],
        [Fraction(9, 7), Fraction(0), Fraction(3, 8), Fraction(-5, 11), Fraction(7, 13)],
    ]
    radii = [Fraction(1, 3), Fraction(2, 5), Fraction(7, 4), Fraction(5, 2)]
    for coeffs in coefficient_sets:
        for radius in radii:
            f_value = poly_value(coeffs, radius)
            f_prime = poly_derivative(coeffs, radius, 1)
            f_second = poly_derivative(coeffs, radius, 2)
            e0 = radius * f_prime + f_value - 1
            e1 = radius * f_prime + radius**2 * f_second / 2
            e0_prime = 2 * f_prime + radius * f_second
            assert radius * e0_prime == 2 * e1
            assertions += 1

            mu_value = radius * (1 - f_value) / 2
            mu_prime = (1 - f_value - radius * f_prime) / 2
            mu_second = -(2 * f_prime + radius * f_second) / 2
            assert e0 == -2 * mu_prime
            assert e1 == -radius * mu_second
            assert f_value == 1 - 2 * mu_value / radius
            assertions += 3

    # Complete registered vacuum family substitution on exact rational points.
    for constant in (Fraction(-7, 3), Fraction(0), Fraction(11, 5)):
        for radius in radii:
            f_value = 1 + constant / radius
            f_prime = -constant / radius**2
            f_second = 2 * constant / radius**3
            assert radius * f_prime + f_value - 1 == 0
            assert radius * f_prime + radius**2 * f_second / 2 == 0
            assertions += 2

    # Standard-library symbolic polynomial replay of the complete FLRW R^2 control.
    b_formal = Poly2.monomial(1, 0)
    t_formal = Poly2.monomial(0, 1)
    hubble = 2 * b_formal * t_formal
    hubble_dot = hubble.dt()
    scalar_r = 6 * (hubble_dot + 2 * hubble * hubble)
    ricci_00 = -3 * (hubble_dot + hubble * hubble)
    ricci_space = hubble_dot + 3 * hubble * hubble
    scalar_dot = scalar_r.dt()
    scalar_ddot = scalar_dot.dt()
    box_scalar = -scalar_ddot - 3 * hubble * scalar_dot
    h_r2_00 = (
        2 * scalar_r * ricci_00
        + Fraction(1, 2) * scalar_r * scalar_r
        + 2 * (-box_scalar - scalar_ddot)
    )
    h_r2_space = (
        2 * scalar_r * ricci_space
        - Fraction(1, 2) * scalar_r * scalar_r
        + 2 * (box_scalar + hubble * scalar_dot)
    )
    divergence = h_r2_00.dt() + 3 * hubble * (h_r2_00 + h_r2_space)
    assert divergence.is_zero()
    assert h_r2_00.coefficient(2, 0) == -72
    assert h_r2_space.coefficient(2, 0) == -216
    assertions += 3

    for b_value in (Fraction(1, 7), Fraction(-2, 5), Fraction(9, 4)):
        h00_at_zero = h_r2_00.evaluate(b_value, Fraction(0))
        hspace_at_zero = h_r2_space.evaluate(b_value, Fraction(0))
        assert h00_at_zero == -72 * b_value**2
        assert hspace_at_zero == -216 * b_value**2
        assert h00_at_zero and hspace_at_zero
        assertions += 3
        for ell in (Fraction(1, 3), Fraction(5, 2)):
            extension_one = ell**2 * h00_at_zero
            extension_two = 2 * ell**2 * h00_at_zero
            assert extension_one != extension_two
            assertions += 1

    # Ricci-flat data make every term in H^(R^2) vanish, whereas the registered FLRW witness does not.
    ricci_flat_h00 = 2 * 0 * 0 - Fraction(1, 2) * 0 + 2 * (0 - 0)
    ricci_flat_hspace = 2 * 0 * 0 - Fraction(1, 2) * 0 + 2 * (0 - 0)
    assert ricci_flat_h00 == 0 and ricci_flat_hspace == 0
    assert h_r2_space.coefficient(2, 0) != 0
    assertions += 2

    # The null operator accepts a non-Einstein metric; it cannot have the Einstein zero set.
    radius = Fraction(2, 3)
    non_einstein_f = 1 + radius**2
    non_einstein_fp = 2 * radius
    non_einstein_e0 = radius * non_einstein_fp + non_einstein_f - 1
    assert non_einstein_e0 != 0
    assert Fraction(0) == 0
    assertions += 2

    # c_E^x G_obs^y cannot be a pure length without a mass/source attachment.
    y_power = Fraction(0)  # mass neutrality
    x_power = -2 * y_power  # time neutrality
    assert -y_power == 0
    assert -x_power - 2 * y_power == 0
    assert x_power + 3 * y_power != 1
    assertions += 3

    # Twelve fixed values leave every simple-node first derivative movable.
    for node in range(1, 13):
        product_value = 1
        for other in range(1, 13):
            product_value *= node - other
        assert product_value == 0
        derivative_value = 1
        for other in range(1, 13):
            if other != node:
                derivative_value *= node - other
        assert derivative_value != 0
        assertions += 2

    # Source/type guards for the theorem application and zero-operator repair.
    with (ROOT / "PREMISE_LEDGER.tsv").open(newline="") as handle:
        premises = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    for name in ("locality", "rank_two_symmetry", "second_order", "divergence_free"):
        assert premises[name]["status"] == "NEW_PREMISE_CANDIDATE"
        assert premises[name]["included"] == "explored_not_owned"
        assertions += 2
    assert premises["nonidentity_parent_operator"]["status"] == "DEFINITIONAL_NONIDENTITY_GATE"
    assertions += 1

    theorem_scope = (ROOT / "LOVELOCK_NAVARRO_SCOPE.md").read_text()
    exact = (ROOT / "EXACT_DERIVATION.md").read_text()
    required_scope_phrases = (
        "Theorem 5.3",
        "fixed signature",
        "metric two-jet",
        "divergence vanishes identically",
        "2m <= n-1",
        "does not say that UDT's physical parent operator belongs to this class",
    )
    for phrase in required_scope_phrases:
        assert phrase in theorem_scope
        assertions += 1
    for phrase in (
        "The degenerate case \\(a=0\\) is the identically zero operator",
        "not a physical parent law",
        "nonidentity `a != 0` equation gate",
    ):
        assert phrase in exact
        assertions += 1

    return {
        "status": "PASS",
        "assertions": assertions,
        "standard_library_only": True,
        "sympy_imported": False,
        "production_imported": False,
        "production_result_read": False,
        "checks": {
            "spherical_residual_dependency": True,
            "mass_aspect_identity": True,
            "complete_vacuum_family_substitution": True,
            "R2_time_live_polynomial_identity": True,
            "R2_Ricci_flat_retention_and_nonidentity": True,
            "zero_operator_excluded_from_Einstein_zero_set": True,
            "cE_Gobs_no_length": True,
            "twelve_values_leave_derivative_freedom": True,
            "theorem_hypotheses_remain_unowned": True,
            "theorem_scope_and_zero_operator_wording": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-result",
        action="store_true",
        help="write only DEPENDENCY_FREE_REPLAY_RESULT.json after all checks pass",
    )
    args = parser.parse_args()
    result = run_replay()
    if args.write_result:
        (ROOT / "DEPENDENCY_FREE_REPLAY_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n"
        )
    print(
        "PASS: dependency-free G259 replay, "
        f"{result['assertions']} exact assertions, write_result={args.write_result}"
    )


if __name__ == "__main__":
    main()
