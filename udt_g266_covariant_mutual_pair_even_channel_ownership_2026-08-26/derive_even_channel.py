#!/usr/bin/env python3
"""Exact symbolic G266 derivation; prints JSON and writes nothing."""

import json
import sympy as sp


def zero(expr, name, checks):
    assert sp.simplify(expr) == 0, name
    checks.append(name)


def main():
    r, a, b, k, x, y0 = sp.symbols("r a b k x y0", positive=True)
    gamma = (r + 1 / r) / 2
    xi = (1 / r - r) / 2
    mutual = 1 / gamma
    D = sp.diag(r, 1 / r)
    checks = []

    zero(D.det() - 1, "determinant_one", checks)
    zero(sp.trace(D) / 2 - gamma, "trace_channel", checks)
    zero((D[1, 1] - D[0, 0]) / 2 - xi, "odd_channel", checks)
    zero(gamma**2 - xi**2 - 1, "hyperbolic_norm", checks)
    zero(gamma.subs(r, 1 / r) - gamma, "gamma_reversal_even", checks)
    zero(xi.subs(r, 1 / r) + xi, "xi_reversal_odd", checks)
    zero(mutual - 2 * r / (1 + r**2), "inverse_trace_projection", checks)
    zero(mutual.subs(r, 1 / r) - mutual, "mutual_projection_reversal_even", checks)
    zero(gamma - xi - r, "recover_clock_leg", checks)
    zero(gamma + xi - 1 / r, "recover_ruler_leg", checks)

    ga, gb = (a + 1 / a) / 2, (b + 1 / b) / 2
    xa, xb = (1 / a - a) / 2, (1 / b - b) / 2
    gab = (a * b + 1 / (a * b)) / 2
    xab = (1 / (a * b) - a * b) / 2
    zero(gab - (ga * gb + xa * xb), "gamma_composition_requires_odd", checks)
    zero(xab - (xa * gb + ga * xb), "xi_composition", checks)
    zero((sp.diag(a, 1 / a) * sp.diag(b, 1 / b) - sp.diag(a * b, 1 / (a * b))).norm(),
         "matrix_composition", checks)
    zero((D**2 - 2 * gamma * D + sp.eye(2)).norm(), "cayley_hamilton_trace_generator", checks)

    # A continuous positive multiplicative scalar m(delta) obeys m(-delta)=1/m(delta).
    # Reversal evenness adds m(-delta)=m(delta), hence m(delta)^2=1 and positivity gives m=1.
    m = sp.symbols("m", positive=True)
    assert sp.solve(sp.Eq(m, 1 / m), m) == [1]
    checks.append("even_multiplicative_equation_reduces_to_m_equals_one")

    f_areal = y0**2 * sp.exp(-2 * k * x)
    f_slice = (y0 - k * x) ** 2
    f_optical = y0**2 - 2 * k * x
    delta_areal = -sp.log(f_areal / y0**2) / 2
    delta_slice = -sp.log(f_slice / y0**2) / 2
    delta_optical = -sp.log(f_optical / y0**2) / 2

    zero(sp.diff(delta_areal, x) - k, "areal_depth_per_distance", checks)
    zero(sp.diff(delta_slice, x) - k / (y0 - k * x), "slice_depth_per_distance", checks)
    zero(sp.diff(delta_optical, x) - k / f_optical, "optical_depth_per_distance", checks)
    zero(f_areal.subs(x, 0) - y0**2, "areal_anchor", checks)
    zero(f_slice.subs(x, 0) - y0**2, "slice_anchor", checks)
    zero(f_optical.subs(x, 0) - y0**2, "optical_anchor", checks)

    unit = {y0: 1, x: 0}
    zero(sp.diff(f_areal, x).subs(unit) + 2 * k, "common_first_jet_areal", checks)
    zero(sp.diff(f_slice, x).subs(unit) + 2 * k, "common_first_jet_slice", checks)
    zero(sp.diff(f_optical, x).subs(unit) + 2 * k, "common_first_jet_optical", checks)
    assert sp.simplify(sp.diff(f_areal, x, 2).subs(unit) - 4 * k**2) == 0
    assert sp.simplify(sp.diff(f_slice, x, 2).subs(unit) - 2 * k**2) == 0
    assert sp.simplify(sp.diff(f_optical, x, 2).subs(unit)) == 0
    checks.append("distinct_second_jet_fingerprints_4_2_0")

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
        "invariant_algebra": "for determinant-one two-by-two reciprocal matrices, trace is the primitive conjugacy invariant; other smooth reversal-even scalars remain functions of Gamma",
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
