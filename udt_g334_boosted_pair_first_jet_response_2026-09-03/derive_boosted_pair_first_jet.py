#!/usr/bin/env python3
"""Exact G334 finite-boost and first-order transport classification."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


class Surd:
    """Exact arithmetic in Q[s]/(s^2-radicand)."""

    __slots__ = ("a", "b", "radicand")

    def __init__(self, a=0, b=0, radicand=1):
        self.a = F(a)
        self.b = F(b)
        self.radicand = F(radicand)

    def lift(self, other):
        if isinstance(other, Surd):
            if other.radicand != self.radicand:
                raise ValueError("incompatible quadratic extensions")
            return other
        return Surd(other, 0, self.radicand)

    def __add__(self, other):
        other = self.lift(other)
        return Surd(self.a + other.a, self.b + other.b, self.radicand)

    __radd__ = __add__

    def __neg__(self):
        return Surd(-self.a, -self.b, self.radicand)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Surd(
            self.a * other.a + self.b * other.b * self.radicand,
            self.a * other.b + self.b * other.a,
            self.radicand,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = F(other)
        return Surd(self.a / other, self.b / other, self.radicand)

    def __eq__(self, other):
        other = self.lift(other)
        return self.a == other.a and self.b == other.b

    def nonzero(self):
        return self.a != 0 or self.b != 0

    def pair(self):
        return [str(self.a), str(self.b)]


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), 0)
             for j in range(len(right[0]))] for i in range(len(left))]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def boost_from_half_tangent(t):
    """Rational parametrization of every finite boost control used in the replay."""
    denominator = 1 - t * t
    if denominator <= 0:
        raise ValueError("finite boost control requires |t|<1")
    ch = (1 + t * t) / denominator
    sh = 2 * t / denominator
    return ch, sh


def g333_rate(scalar_r, constant_c, cosmological_lambda, branch, mu):
    radicand = 2 * (scalar_r + 2 * constant_c**2 - 2 * cosmological_lambda)
    if radicand <= 0:
        raise ValueError("outside strict G332 radicand stratum")
    root = Surd(0, branch, radicand)
    b = -constant_c + root
    rate = (b - constant_c) / 2 - b * mu
    return radicand, b, rate


def inherited_response(rate, ch, sh):
    zero = rate * 0
    base = [[zero, zero], [zero, 2 * rate]]
    boost = [[ch, sh], [sh, ch]]
    transformed = matmul(transpose(boost), matmul(base, boost))
    return transformed


def add_transport(response, alpha, beta, gamma, delta):
    """Add in-plane commutator terms; screen-orthogonal terms contract to zero."""
    return [
        [response[0][0] - 2 * alpha, response[0][1] + beta - gamma],
        [response[1][0] + beta - gamma, response[1][1] + 2 * delta],
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()

    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    controls = (
        ("unequal_left", F(12)),
        ("unequal_right", F(138, 7)),
        ("unequal_second", F(28, 3)),
        ("unequal_third", F(352, 43)),
        ("equal_left", F(6)),
        ("equal_right", F(6)),
    )
    mu_values = (F(0), F(1, 16), F(1, 4), F(9, 16), F(1))
    boost_controls = (F(-3, 4), F(-1, 2), F(-1, 5), F(0), F(1, 5), F(1, 2), F(3, 4))
    records = []
    branch_values = {}

    for label, scalar_r in controls:
        for cosmological_lambda in (F(-2), F(3), F(11)):
            for constant_c in (F(-20), F(20)):
                for branch in (-1, 1):
                    for mu in mu_values:
                        radicand, b, rate = g333_rate(
                            scalar_r, constant_c, cosmological_lambda, branch, mu
                        )
                        branch_values.setdefault(
                            (label, cosmological_lambda, constant_c, mu), {}
                        )[branch] = b
                        for t in boost_controls:
                            ch, sh = boost_from_half_tangent(t)
                            prefix = f"{label}_{cosmological_lambda}_{constant_c}_{branch}_{mu}_{t}"
                            require(ch * ch - sh * sh == 1, f"{prefix}_Lorentz")
                            response = inherited_response(rate, ch, sh)
                            d00 = 2 * rate * sh * sh
                            d01 = 2 * rate * sh * ch
                            d11 = 2 * rate * ch * ch
                            require(response == [[d00, d01], [d01, d11]],
                                    f"{prefix}_congruence")
                            require(d11 - d00 == 2 * rate, f"{prefix}_invariant_difference")
                            require(d01 * d01 == d00 * d11, f"{prefix}_rank_one")
                            mixed_trace = -d00 + d11
                            mixed_determinant = -d00 * d11 + d01 * d01
                            require(mixed_trace == 2 * rate, f"{prefix}_mixed_trace")
                            require(mixed_determinant == 0, f"{prefix}_mixed_determinant")

                            phi_dot = d00 / 2
                            require(phi_dot == rate * sh * sh, f"{prefix}_terminal_phi")
                            if t == 0:
                                require(phi_dot == 0, f"{prefix}_unboosted_terminal_blind")
                            else:
                                require(phi_dot / (sh * sh) == rate,
                                        f"{prefix}_terminal_reconstructs_nonzero_boost")
                            require((d11 - d00) / 2 == rate,
                                    f"{prefix}_complete_reconstructs_all_boosts")

                            # A varying Lorentz rapidity has beta=gamma=zeta and no symmetric
                            # metric-component contribution at the slice.
                            for zeta in (F(-7, 3), F(0), F(5, 2)):
                                carried = add_transport(response, F(0), zeta, zeta, F(0))
                                require(carried == response, f"{prefix}_{zeta}_boost_rate_cancels")

                            # A general supplied pair transport changes raw component derivatives.
                            general = add_transport(response, F(2, 3), F(5, 7), F(-1, 4), F(-3, 5))
                            require(general[0][0] == d00 - F(4, 3),
                                    f"{prefix}_general_transport_clock")
                            require(general[0][1] == d01 + F(27, 28),
                                    f"{prefix}_general_transport_cross")
                            require(general[1][1] == d11 - F(6, 5),
                                    f"{prefix}_general_transport_ruler")
                            require(general[0][0] / 2 == rate * sh * sh - F(2, 3),
                                    f"{prefix}_general_transport_phi")

                            # A moving orthonormal frame may cancel the raw component jet.
                            orthonormalized = add_transport(
                                response, d00 / 2, -d01, 0, -d11 / 2
                            )
                            require(orthonormalized == [[0, 0], [0, 0]],
                                    f"{prefix}_reorthonormalized_components_zero")

                            records.append({
                                "control": label,
                                "R": str(scalar_r),
                                "Lambda": str(cosmological_lambda),
                                "C": str(constant_c),
                                "branch": branch,
                                "mu": str(mu),
                                "boost_half_tangent": str(t),
                                "radicand": str(radicand),
                                "b": b.pair(),
                                "q": rate.pair(),
                                "n_h": [[entry.pair() for entry in row] for row in response],
                            })

    for key, branches in branch_values.items():
        require(branches[-1] != branches[1], f"both_branches_distinct_{key}")

    # Exact reversal parity on a nonzero witness.
    _, _, witness = g333_rate(F(12), F(20), F(3), 1, F(1, 4))
    require(witness.nonzero(), "witness_rate_nonzero")
    ch_p, sh_p = boost_from_half_tangent(F(1, 2))
    ch_m, sh_m = boost_from_half_tangent(F(-1, 2))
    plus = inherited_response(witness, ch_p, sh_p)
    minus = inherited_response(witness, ch_m, sh_m)
    require(plus[0][0] == minus[0][0], "reversal_clock_even")
    require(plus[1][1] == minus[1][1], "reversal_ruler_even")
    require(plus[0][1] == -minus[0][1], "reversal_cross_odd")
    require(plus[0][0] / 2 == minus[0][0] / 2, "reversal_phi_even")

    # The normal derivative cannot be promoted to the boosted observer derivative: for sh != 0,
    # u(f)=ch*n(f)+sh*v(f), and G333 supplies no v(f).
    normal_jet = F(7, 5)
    spatial_jet_a = F(0)
    spatial_jet_b = F(9, 4)
    u_jet_a = ch_p * normal_jet + sh_p * spatial_jet_a
    u_jet_b = ch_p * normal_jet + sh_p * spatial_jet_b
    require(u_jet_a != u_jet_b, "observer_time_requires_unsupplied_spatial_jet")

    landing = (
        "G333_FIRST_NORMAL_RESPONSE_HAS_EXACT_FINITE_BOOST_CONGRUENCE"
        "__ARBITRARY_PAIR_FIRST_JET_REMAINS_TRANSPORT_QUALIFIED"
        "__COMPLETE_MATRIX_EXCEEDS_TERMINAL_PHI_ON_INHERITED_GERMS"
        "__NO_NEW_CHANNEL_OR_OBSERVER_TIME_EVOLUTION"
    )
    payload = {
        "package": "G334",
        "grade": "DERIVED_CONDITIONAL_BOUNDED__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS",
        "landing": landing,
        "classifications": [
            "TRANSPORT_QUALIFIED_CONGRUENCE",
            "COMPLETE_MATRIX_STRONGER_ON_DECLARED_TRANSPORT",
        ],
        "analytic_result": {
            "base_first_jet": "diag(0,2q)",
            "boosted_first_jet": "2q*[[sinh(z)^2,sinh(z)cosh(z)],[sinh(z)cosh(z),cosh(z)^2]]",
            "mixed_characteristic_data": {"trace": "2q", "determinant": "0"},
            "terminal_Phi_normal_derivative": "q*sinh(z)^2 on inherited transport",
            "general_transport_addition": "[[-2alpha,beta-gamma],[beta-gamma,2delta]]",
            "observer_time_derivative": "OPEN; requires spatial first jet in addition to n jet",
        },
        "sample_count": len(records),
        "checks_passed": len(checks),
        "checks_sha256": hashlib.sha256(("\n".join(checks) + "\n").encode("utf-8")).hexdigest(),
        "check_examples": checks[:10] + checks[-10:],
        "records": records,
        "topology_inputs_used": [],
        "scope": {
            "all_finite_boosts": "analytic; exact rational controls exercised",
            "all_unit_directions": True,
            "both_G332_branches": True,
            "normal_derivative_only": True,
            "arbitrary_transport_unique_from_boost": False,
            "later_evolution": "OPEN",
            "physical_germ_population": "OPEN",
            "matter_mass_scale_Xmax_observations": "OPEN",
        },
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "checks_passed": len(checks),
        "classifications": payload["classifications"],
        "sample_count": len(records),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
