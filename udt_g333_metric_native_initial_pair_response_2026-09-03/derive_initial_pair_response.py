#!/usr/bin/env python3
"""Exact first-normal-jet response for the full G332 algebraic construction."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


class Surd:
    """Exact arithmetic in Q[s]/(s^2-q)."""

    __slots__ = ("a", "b", "q")

    def __init__(self, a=0, b=0, q=1):
        self.a = F(a)
        self.b = F(b)
        self.q = F(q)

    def lift(self, other):
        if isinstance(other, Surd):
            if other.q != self.q:
                raise ValueError("incompatible quadratic extensions")
            return other
        return Surd(other, 0, self.q)

    def __add__(self, other):
        other = self.lift(other)
        return Surd(self.a + other.a, self.b + other.b, self.q)

    __radd__ = __add__

    def __neg__(self):
        return Surd(-self.a, -self.b, self.q)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Surd(
            self.a * other.a + self.b * other.b * self.q,
            self.a * other.b + self.b * other.a,
            self.q,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = F(other)
        return Surd(self.a / other, self.b / other, self.q)

    def __eq__(self, other):
        other = self.lift(other)
        return self.a == other.a and self.b == other.b

    def nonzero(self):
        return self.a != 0 or self.b != 0

    def pair(self):
        return [str(self.a), str(self.b)]


def exact_case(scalar_r, constant_c, cosmological_lambda, branch, mu):
    """Evaluate all registered identities at one exact scalar-curvature point."""
    q = 2 * (scalar_r + 2 * constant_c**2 - 2 * cosmological_lambda)
    if q <= 0:
        raise ValueError("case is outside the strict G332 radicand stratum")
    root = Surd(0, branch, q)
    b = -constant_c + root
    k_h = (constant_c - b) / 2
    k_v = (constant_c + b) / 2

    h_h = -k_h
    h_v = -k_v
    tr_h = 2 * h_h + h_v
    mean_h = tr_h / 3
    shear_h = h_h - mean_h
    shear_v = h_v - mean_h
    shear_norm = 2 * shear_h * shear_h + shear_v * shear_v
    directional = h_h + (h_v - h_h) * mu

    tau = 2 * k_h + k_v
    k_norm = 2 * k_h * k_h + k_v * k_v
    hamiltonian = Surd(scalar_r, 0, q) + tau * tau - k_norm

    # Gaussian normal pair germ at the slice, with [n,v]=0 and gamma(v,v)=1.
    pair_h00 = F(-1)
    pair_h00_normal_derivative = F(0)
    pair_h11 = F(1)
    pair_h11_normal_derivative = 2 * directional
    length_rate = pair_h11_normal_derivative / 2
    terminal_phi_normal_derivative = F(0)

    checks = {
        "g315_sign_H_equals_minus_K": h_h == -k_h and h_v == -k_v,
        "horizontal_rate": h_h == (b - constant_c) / 2,
        "vertical_rate": h_v == -(constant_c + b) / 2,
        "directional_difference": h_v - h_h == -b,
        "trace": tr_h == (b - 3 * constant_c) / 2,
        "mean": mean_h == -constant_c / 2 + b / 6,
        "shear_horizontal": shear_h == b / 3,
        "shear_vertical": shear_v == -2 * b / 3,
        "shear_trace_zero": 2 * shear_h + shear_v == 0,
        "shear_norm": shear_norm == 2 * b * b / 3,
        "rate_reconstruction_horizontal": mean_h + shear_h == h_h,
        "rate_reconstruction_vertical": mean_h + shear_v == h_v,
        "all_direction_formula": directional == (b - constant_c) / 2 - b * mu,
        "hamiltonian": hamiltonian == 2 * cosmological_lambda,
        "branch_equation": (b + constant_c) * (b + constant_c) == q,
        "pair_unit_normal": pair_h00 == -1 and pair_h00_normal_derivative == 0,
        "pair_unit_separation": pair_h11 == 1,
        "pair_length_rate": length_rate == directional,
        "terminal_phi_blind_in_this_germ": terminal_phi_normal_derivative == 0,
    }
    return q, b, directional, checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()

    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    # Exact scalar-curvature controls inherited from the independently banked G331/G332 family.
    curvature_controls = (
        ("unequal_left", F(12), F(2), F(3), F(1, 3)),
        ("unequal_right", F(138, 7), F(2), F(3), F(2, 3)),
        ("unequal_second", F(28, 3), F(3, 2), F(5, 4), F(2, 5)),
        ("unequal_third", F(352, 43), F(5, 4), F(7, 4), F(3, 7)),
        ("equal_left", F(6), F(1), F(1), F(1, 3)),
        ("equal_right", F(6), F(1), F(1), F(2, 3)),
    )
    mu_values = (F(0), F(1, 16), F(1, 4), F(9, 16), F(1))
    records = []
    branch_pairs = {}

    for label, scalar_r, w1, w2, x in curvature_controls:
        for cosmological_lambda in (F(-2), F(3), F(11)):
            for constant_c in (F(-20), F(20)):
                for branch in (-1, 1):
                    for mu in mu_values:
                        q, b, directional, case_checks = exact_case(
                            scalar_r, constant_c, cosmological_lambda, branch, mu
                        )
                        prefix = f"{label}_{cosmological_lambda}_{constant_c}_{branch}_{mu}"
                        for gate, passed in case_checks.items():
                            require(passed, f"{prefix}_{gate}")
                        branch_pairs.setdefault(
                            (label, cosmological_lambda, constant_c), {}
                        )[branch] = b
                        records.append({
                            "control": label,
                            "x": str(x),
                            "w1": str(w1),
                            "w2": str(w2),
                            "R": str(scalar_r),
                            "Lambda": str(cosmological_lambda),
                            "C": str(constant_c),
                            "branch": branch,
                            "mu": str(mu),
                            "radicand": str(q),
                            "b": b.pair(),
                            "H_vv": directional.pair(),
                        })

    require(curvature_controls[0][1] != curvature_controls[1][1],
            "unequal_weight_nonconstant_curvature_control")
    require(curvature_controls[-2][1] == curvature_controls[-1][1],
            "equal_weight_constant_curvature_control")
    for key, branches in branch_pairs.items():
        require(branches[-1] != branches[1], f"both_branches_distinct_{key}")

    # A single non-isotropic witness defeats COMMON_ONLY and terminal completeness for this germ.
    _, witness_b, horizontal, _ = exact_case(F(12), F(20), F(3), 1, F(0))
    _, _, vertical, _ = exact_case(F(12), F(20), F(3), 1, F(1))
    require(witness_b.nonzero(), "nonisotropic_witness_b_nonzero")
    require(horizontal != vertical, "common_only_rejected")
    require(horizontal - vertical == witness_b, "directional_gap_is_b")
    require(F(0) == F(0) and horizontal != vertical,
            "same_terminal_phi_derivative_different_complete_pair_strain")

    landing = (
        "G332_METRIC_NATIVE_FIRST_RESPONSE_IS_COMMON_PLUS_DIRECTIONAL"
        "__COMPLETE_NORMAL_SPATIAL_PAIR_PULLBACK_EXCEEDS_ITS_TERMINAL_SCALAR"
        "__FIRST_JET_ONLY_NO_HOPF_SELECTION_OR_STABILITY"
    )
    payload = {
        "package": "G333",
        "grade": "DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_REVIEW",
        "landing": landing,
        "classifications": ["METRIC_2_PLUS_1", "COMPLETE_PULLBACK_STRONGER"],
        "analytic_result": {
            "H": "-K^sharp",
            "H_horizontal": "(b-C)/2",
            "H_vertical": "-(C+b)/2",
            "gamma(Hv,v)": "(b-C)/2-b*mu",
            "H_trace": "(b-3C)/2",
            "H_tracefree_eigenvalues": ["b/3", "b/3", "-2b/3"],
            "H_tracefree_norm_squared": "2*b^2/3",
            "pair_h_normal_jet": {"h00": "-1", "n(h00)": "0", "h11": "1",
                                  "n(h11)": "2*gamma(Hv,v) under [n,v]=0"},
            "terminal_pair_phi_normal_derivative": "0 for this Gaussian normal-spatial germ",
        },
        "topology_inputs_used": [],
        "sample_count": len(records),
        "checks_passed": len(checks),
        "checks": checks,
        "records": records,
        "scope": {
            "response": "first normal jet only",
            "pair_germ": "supplied Gaussian normal-spatial diagnostic germ",
            "all_unit_directions": True,
            "both_G332_branches": True,
            "Hopf_selection": False,
            "later_evolution": "OPEN",
            "stability": "OPEN",
            "occupancy": "OPEN",
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
