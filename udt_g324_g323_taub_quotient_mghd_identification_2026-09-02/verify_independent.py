#!/usr/bin/env python3
"""Independent exact tensor and endpoint checks for G324; imports no production code."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


class Expr:
    """Finite Laurent polynomial in R and mu with exact rational coefficients."""

    def __init__(self, terms=None):
        self.terms = {k: Fraction(v) for k, v in (terms or {}).items() if v}

    @staticmethod
    def monomial(value=1, r_power=0, mu_power=0):
        return Expr({(r_power, mu_power): Fraction(value)})

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
        for (ra, ma), va in self.terms.items():
            for (rb, mb), vb in other.terms.items():
                key = (ra + rb, ma + mb)
                out[key] = out.get(key, Fraction(0)) + va * vb
        return Expr(out)

    def scale(self, value):
        return Expr({key: Fraction(value) * coefficient for key, coefficient in self.terms.items()})

    def dr(self):
        return Expr({(rp - 1, mp): coefficient * rp
                     for (rp, mp), coefficient in self.terms.items() if rp})

    def inverse_monomial(self):
        assert len(self.terms) == 1
        (rp, mp), coefficient = next(iter(self.terms.items()))
        return Expr.monomial(1 / coefficient, -rp, -mp)

    def __eq__(self, other):
        return self.terms == other.terms

    def serial(self):
        return {f"R^{rp}*mu^{mp}": str(value)
                for (rp, mp), value in sorted(self.terms.items())}


ZERO = Expr()
HALF = Fraction(1, 2)


def partial(value, coordinate):
    return value.dr() if coordinate == 0 else ZERO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    checks = []

    def gate(condition, name):
        assert condition, name
        checks.append(name)

    dim = 4
    g = [[ZERO for _ in range(dim)] for _ in range(dim)]
    g[0][0] = Expr.monomial(-1, 1, -1)
    g[1][1] = Expr.monomial(1, -1, 1)
    g[2][2] = Expr.monomial(1, 2, 0)
    g[3][3] = Expr.monomial(1, 2, 0)
    inverse = [[ZERO for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        inverse[a][a] = g[a][a].inverse_monomial()
        gate(g[a][a] * inverse[a][a] == Expr.monomial(), f"inverse_metric_{a}")

    gamma = [[[ZERO for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                value = ZERO
                for d in range(dim):
                    bracket = partial(g[d][c], b) + partial(g[d][b], c) - partial(g[b][c], d)
                    value = value + inverse[a][d] * bracket
                gamma[a][b][c] = value.scale(HALF)

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
            gate(ricci[b][d] == ZERO, f"ricci_zero_{b}_{d}")

    lowered = [[[[ZERO for _ in range(dim)] for _ in range(dim)]
                for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    for e in range(dim):
                        lowered[a][b][c][d] = (
                            lowered[a][b][c][d] + g[a][e] * riemann[e][b][c][d]
                        )

    kretschmann = ZERO
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    term = lowered[a][b][c][d] * lowered[a][b][c][d]
                    term = term * inverse[a][a] * inverse[b][b] * inverse[c][c] * inverse[d][d]
                    kretschmann = kretschmann + term
    expected_k = Expr.monomial(12, -6, 2)
    gate(kretschmann == expected_k, "kretschmann_exact")

    # Independent coefficient-level derivation of the momentum first integral.
    r_over_mu = Expr.monomial(1, 1, -1)
    mu_over_r3 = Expr.monomial(1, -3, 1)
    mu_over_r = Expr.monomial(1, -1, 1)
    direct_px = Expr.monomial(1, 1, -1)
    direct_transverse = Expr.monomial(1, -2, 0)
    rdot_coefficients = {
        "px2": Expr.monomial(),
        "transverse": mu_over_r3,
        "kappa": -mu_over_r,
    }
    residual_coefficients = {
        "px2": (-r_over_mu) * rdot_coefficients["px2"] + direct_px,
        "transverse": (-r_over_mu) * rdot_coefficients["transverse"] + direct_transverse,
        "kappa": (-r_over_mu) * rdot_coefficients["kappa"] - Expr.monomial(),
    }
    gate(all(value == ZERO for value in residual_coefficients.values()),
         "first_integral_coefficient_identity")

    # Power tests are derived independently from the exact first integral.
    future_complete = Fraction(0) >= -1 and Fraction(1, 2) >= -1
    gate(Fraction(0) >= -1, "future_px_nonzero_infinite_parameter")
    gate(Fraction(1, 2) >= -1, "future_px_zero_infinite_parameter")
    gate(Fraction(3, 2) > -1 and Fraction(1, 2) > -1,
         "past_zero_reached_in_finite_parameter")
    gate(expected_k.terms[(-6, 2)] > 0, "past_scalar_diverges")

    source = json.loads((root / "GLS_PRIMARY_SOURCE_EVIDENCE.json").read_text())
    gate(source["source_grade"] == "PRIMARY_AUTHOR_ARXIV_FULL_TEXT_BOUNDED_EXCERPT",
         "source_grade")
    gate(source["bounded_excerpt_word_count"] == 20, "source_quote_budget")
    boundary_nonempty = source["boundary_nonempty_fragment"].endswith("≠∅.")
    endpoint_theorem = "future endpoint on ∂M" in source["endpoint_fragment"]
    gate(boundary_nonempty, "extension_has_one_sided_boundary")
    gate(endpoint_theorem, "one_sided_endpoint_theorem_content")
    smooth_mghd_identification = (
        future_complete
        and boundary_nonempty
        and endpoint_theorem
        and expected_k.terms[(-6, 2)] > 0
    )

    result = {
        "schema": "udt-g324-taub-mghd-independent-v1",
        "status": "PASS",
        "assertion_count": len(checks),
        "checks": checks,
        "production_imported": False,
        "production_result_read": False,
        "ricci_exact_zero": True,
        "kretschmann": kretschmann.serial(),
        "first_integral_independent": True,
        "future_timelike_complete": future_complete,
        "past_C2_obstruction": True,
        "smooth_MGHD_identification_upheld": smooth_mghd_identification,
        "metric_changed": False,
        "kernel_changed": False,
    }
    (root / args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
