#!/usr/bin/env python3
"""Exact G136 algebra; prints machine-readable evidence and does not mutate the repository."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def main() -> None:
    phi, psi, k, xmax, x1, x2 = sp.symbols(
        "phi psi k X_max x_1 x_2", real=True
    )
    eps = sp.Rational(1, 4)

    def mobius(a: sp.Expr, b: sp.Expr) -> sp.Expr:
        return sp.cancel((a + b) / (1 + a * b))

    checks: dict[str, bool] = {}

    chi = sp.tanh(phi)
    checks["tanh_composition"] = sp.trigsimp(
        sp.tanh(phi + psi) - mobius(sp.tanh(phi), sp.tanh(psi))
    ) == 0
    checks["reversal"] = sp.simplify(sp.tanh(-phi) + chi) == 0
    checks["coincidence"] = chi.subs(phi, 0) == 0
    checks["positive_endpoint"] = sp.limit(chi, phi, sp.oo) == 1
    checks["negative_endpoint"] = sp.limit(chi, phi, -sp.oo) == -1

    f_k = sp.tanh(k * phi)
    checks["normalized_family_composes"] = sp.simplify(
        (
            sp.tanh(k * (phi + psi))
            - mobius(sp.tanh(k * phi), sp.tanh(k * psi))
        ).rewrite(sp.exp)
    ) == 0
    checks["family_origin_slope_is_k"] = sp.diff(f_k, phi).subs(phi, 0) == k
    checks["unit_slope_selects_k_one"] = sp.solve(
        sp.Eq(sp.diff(f_k, phi).subs(phi, 0), 1), k
    ) == [1]

    # Differentiating F(phi+psi)=F(phi) boxplus F(psi) at psi=0 gives
    # F'=k(1-F^2). Verify the selected solution exactly.
    F = sp.Function("F")
    ode = sp.Eq(sp.diff(F(phi), phi), k * (1 - F(phi) ** 2))
    checks["tanh_k_solves_classification_ode"] = sp.simplify(
        ode.lhs.subs(F(phi), f_k).doit() - ode.rhs.subs(F(phi), f_k)
    ) == 0

    # G135's slope-matched smooth counterfamily preserves endpoints but not the same law.
    z = sp.symbols("z", real=True)
    g = z + eps * z**3 * (1 - z**2)
    a, b = sp.Rational(1, 3), sp.Rational(1, 5)
    deviation = sp.factor(g.subs(z, mobius(a, b)) - mobius(g.subs(z, a), g.subs(z, b)))
    checks["smooth_remarking_unit_slope"] = sp.diff(g, z).subs(z, 0) == 1
    checks["smooth_remarking_same_law_fails"] = deviation == sp.Rational(390123, 25975936)

    x_comp = sp.cancel(xmax * mobius(x1 / xmax, x2 / xmax))
    expected_x = sp.cancel((x1 + x2) / (1 + x1 * x2 / xmax**2))
    checks["dimensional_composition"] = sp.simplify(x_comp - expected_x) == 0
    checks["xmax_fixed_point"] = sp.simplify(expected_x.subs(x2, xmax) - xmax) == 0
    checks["xmax_scale_not_in_chi"] = not chi.has(xmax)

    source_text = {
        path: (ROOT / path).read_text(encoding="utf-8")
        for path in (
            "PROVENANCE.md",
            "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
            "simple_metric_hyperbolic_derive.md",
            "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/AUDIT_REPORT.md",
            "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/EXACT_DERIVATION.md",
            "udt_g135_projective_pair_separation_constitution_audit_2026-08-17/AUDIT_REPORT.md",
        )
    }
    checks["origin_distance_unspecified"] = "distance notion was UNSPECIFIED" in source_text["PROVENANCE.md"]
    checks["founding_depth_unit_chosen"] = "Sign and unit of $\\phi$" in source_text[
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md"
    ] and "**CHOSE**" in source_text["UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md"]
    checks["historical_distance_chart_named"] = "P4" in source_text[
        "simple_metric_hyperbolic_derive.md"
    ] and "NAMED identification" in source_text["simple_metric_hyperbolic_derive.md"]
    checks["xmax_profile_open"] = "Tanh, fractional-linear, WR-L, and other forms remain candidate realizations" in source_text[
        "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/AUDIT_REPORT.md"
    ]
    checks["copresence_does_not_supply_depth"] = "a signed ordered depth" in source_text[
        "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/EXACT_DERIVATION.md"
    ] and "It also does\nnot supply" in source_text[
        "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/EXACT_DERIVATION.md"
    ]
    checks["G135_constitution_open"] = "do not yet prove that the projective chart is the operational" in source_text[
        "udt_g135_projective_pair_separation_constitution_audit_2026-08-17/AUDIT_REPORT.md"
    ]

    assert all(checks.values()), {name: ok for name, ok in checks.items() if not ok}
    result = {
        "grade": "DERIVED_CLASSIFICATION__SOURCE_ENTAILMENT_NEGATIVE__CONSTITUTIVE_CLARIFICATION_REMAINS",
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "exact_smooth_counterexample_deviation": str(deviation),
        "classification": "F(phi)=tanh(k phi), k>0",
        "normalized_classification": "F(phi)=tanh(phi)",
        "source_entailment": "NO_CURRENT_DIRECT_ENTAILMENT",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
