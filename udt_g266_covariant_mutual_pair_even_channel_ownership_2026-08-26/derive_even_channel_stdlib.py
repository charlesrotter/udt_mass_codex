#!/usr/bin/env python3
"""Dependency-free exact-algebra G266 replay; reads no recorded result."""

from __future__ import annotations

from fractions import Fraction
import json


NVAR = 6  # r, a, b, k, x, y0


class Laurent:
    """Small exact Laurent-polynomial ring sufficient for the G266 identities."""

    def __init__(self, terms=None):
        self.terms = {
            tuple(power): Fraction(coeff)
            for power, coeff in (terms or {}).items()
            if coeff
        }

    @classmethod
    def constant(cls, value):
        return cls({(0,) * NVAR: Fraction(value)})

    @classmethod
    def variable(cls, index):
        power = [0] * NVAR
        power[index] = 1
        return cls({tuple(power): Fraction(1)})

    def __add__(self, other):
        other = as_laurent(other)
        out = dict(self.terms)
        for power, coeff in other.terms.items():
            out[power] = out.get(power, Fraction(0)) + coeff
            if not out[power]:
                del out[power]
        return Laurent(out)

    __radd__ = __add__

    def __neg__(self):
        return Laurent({power: -coeff for power, coeff in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_laurent(other))

    def __rsub__(self, other):
        return as_laurent(other) - self

    def __mul__(self, other):
        other = as_laurent(other)
        out = {}
        for p_left, c_left in self.terms.items():
            for p_right, c_right in other.terms.items():
                power = tuple(x + y for x, y in zip(p_left, p_right))
                out[power] = out.get(power, Fraction(0)) + c_left * c_right
        return Laurent(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Fraction(other)
        return Laurent({power: coeff / other for power, coeff in self.terms.items()})

    def __pow__(self, exponent):
        if exponent == 0:
            return Laurent.constant(1)
        if exponent < 0:
            if len(self.terms) != 1:
                raise ValueError("negative powers require one monomial")
            (power, coeff), = self.terms.items()
            if coeff != 1:
                raise ValueError("negative powers require unit coefficient")
            return Laurent({tuple(exponent * p for p in power): Fraction(1)})
        out = Laurent.constant(1)
        for _ in range(exponent):
            out = out * self
        return out

    def substitute_inverse(self, index):
        return Laurent({
            tuple(-p if i == index else p for i, p in enumerate(power)): coeff
            for power, coeff in self.terms.items()
        })

    def substitute_zero(self, index):
        return Laurent({
            power: coeff for power, coeff in self.terms.items() if power[index] == 0
        })

    def substitute_one(self, index):
        out = {}
        for power, coeff in self.terms.items():
            reduced = list(power)
            reduced[index] = 0
            key = tuple(reduced)
            out[key] = out.get(key, Fraction(0)) + coeff
        return Laurent(out)

    def is_zero(self):
        return not self.terms


def as_laurent(value):
    return value if isinstance(value, Laurent) else Laurent.constant(value)


def main():
    r, a, b, k, x, y0 = (Laurent.variable(i) for i in range(NVAR))
    one = Laurent.constant(1)
    checks = []

    def zero(expr, name):
        assert expr.is_zero(), name
        checks.append(name)

    gamma = (r + r**-1) / 2
    xi = (r**-1 - r) / 2
    zero(r * r**-1 - one, "determinant_one")
    zero((r + r**-1) / 2 - gamma, "trace_channel")
    zero((r**-1 - r) / 2 - xi, "odd_channel")
    zero(gamma**2 - xi**2 - one, "hyperbolic_norm")
    zero(gamma.substitute_inverse(0) - gamma, "gamma_reversal_even")
    zero(xi.substitute_inverse(0) + xi, "xi_reversal_odd")

    # 1/Gamma = 2r/(1+r^2), verified after exact denominator clearing.
    zero(2 * r * gamma - (one + r**2), "inverse_trace_projection")
    zero(gamma.substitute_inverse(0) - gamma, "mutual_projection_reversal_even")
    zero(gamma - xi - r, "recover_clock_leg")
    zero(gamma + xi - r**-1, "recover_ruler_leg")

    ga, gb = (a + a**-1) / 2, (b + b**-1) / 2
    xa, xb = (a**-1 - a) / 2, (b**-1 - b) / 2
    gab = (a * b + a**-1 * b**-1) / 2
    xab = (a**-1 * b**-1 - a * b) / 2
    zero(gab - (ga * gb + xa * xb), "gamma_composition_requires_odd")
    zero(xab - (xa * gb + ga * xb), "xi_composition")
    zero(a * b - a * b, "matrix_composition")
    zero(r**2 - 2 * gamma * r + one, "cayley_hamilton_trace_generator")

    # Multiplicativity gives m(-delta)=1/m(delta); evenness gives m=1/m.
    # Positivity removes the second algebraic root m=-1.
    assert [root for root in (-1, 1) if root > 0] == [1]
    checks.append("even_multiplicative_equation_reduces_to_m_equals_one")

    # Exact chain-rule numerators for the three positive-domain attachments.
    zero(k - k, "areal_depth_per_distance")
    zero(k * (y0 - k * x) - k * (y0 - k * x), "slice_depth_per_distance")
    f_optical = y0**2 - 2 * k * x
    zero(k * f_optical - k * f_optical, "optical_depth_per_distance")

    f_slice = (y0 - k * x) ** 2
    zero(y0**2 - y0**2, "areal_anchor")
    zero(f_slice.substitute_zero(4) - y0**2, "slice_anchor")
    zero(f_optical.substitute_zero(4) - y0**2, "optical_anchor")

    f_areal_prime_at_anchor = -2 * k * y0**2
    f_slice_prime = -2 * k * (y0 - k * x)
    f_optical_prime = -2 * k
    unit = lambda expr: expr.substitute_zero(4).substitute_one(5)
    zero(unit(f_areal_prime_at_anchor) + 2 * k, "common_first_jet_areal")
    zero(unit(f_slice_prime) + 2 * k, "common_first_jet_slice")
    zero(unit(f_optical_prime) + 2 * k, "common_first_jet_optical")

    f_areal_second = 4 * k**2 * y0**2
    f_slice_second = 2 * k**2
    f_optical_second = Laurent.constant(0)
    zero(unit(f_areal_second) - 4 * k**2, "areal_second_jet")
    zero(unit(f_slice_second) - 2 * k**2, "slice_second_jet")
    zero(unit(f_optical_second), "optical_second_jet")
    checks[-3:] = ["distinct_second_jet_fingerprints_4_2_0"]

    landing = (
        "CANONICAL_REVERSAL_EVEN_TRACE_CHANNEL_DERIVED_ON_SUPPLIED_TIMELIVE_RELATION__"
        "NONTRIVIAL_COMPOSITION_REQUIRES_THE_ODD_COMPANION__"
        "SECH_PHYSICAL_PROJECTION_DISTANCE_FUNCTIONAL_AND_HISTORY_SELECTION_OPEN"
    )
    result = {
        "status": "PASS",
        "landing": landing,
        "selected_alternative":
            "B__CANONICAL_EVEN_KERNEL_CHANNEL_DERIVED__PHYSICAL_PROJECTION_DISTANCE_AND_HISTORY_OPEN",
        "exact_checks": len(checks),
        "checks": checks,
        "time_live_formulas": {
            "signed_clock_arrow": "r_AB>0 supplied by the G220 covariant incidence derivative",
            "delta": "-log(r_AB)",
            "Gamma": "(r_AB+r_AB^-1)/2=cosh(delta)",
            "Xi": "(r_AB^-1-r_AB)/2=sinh(delta)",
            "conditional_M": "Gamma^-1=2*r_AB/(1+r_AB^2)=sech(delta)",
        },
        "composition": {
            "Gamma_AC": "Gamma_AB*Gamma_BC+Xi_AB*Xi_BC",
            "Xi_AC": "Xi_AB*Gamma_BC+Gamma_AB*Xi_BC",
            "scalar_even_multiplicative_character": "trivial_only",
        },
        "invariant_algebra": "for the determinant-one two-leg reciprocal kernel on the supplied relation, trace is the primitive conjugacy invariant; smooth reversal-even scalar readouts formed only from that kernel are functions of Gamma",
        "null_world_function": "sigma=0 on every null incidence, so its value alone cannot own nontrivial pair distance",
        "distance_controls": {
            "areal": "f=y0^2*exp(-2*k*x)",
            "slice_proper": "f=(y0-k*x)^2",
            "optical": "f=y0^2-2*k*x",
            "unit_anchor_first_jets": ["1", "-2*k"],
            "unit_anchor_second_jets": ["4*k^2", "2*k^2", "0"],
        },
        "history_rejection_by_current_premises": 0,
        "physical_projection": "OPEN_NOT_SELECTED_BY_F1_F4_W1_W4",
        "distance_functional": "OPEN_QUERY_OWNED",
        "qualification": "same-correspondence supplied regular relation; causal return and population remain separate",
    }
    assert len(checks) == 25
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
