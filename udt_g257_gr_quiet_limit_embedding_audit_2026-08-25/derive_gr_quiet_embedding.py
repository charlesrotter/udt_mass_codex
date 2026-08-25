#!/usr/bin/env python3
"""Exact G257 production derivation for the bounded GR quiet-limit embedding."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("DERIVATION_RESULT.json")


def z(expr: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.trigsimp(expr))


def main() -> None:
    t, r, th, ph = sp.symbols("t r theta varphi", real=True)
    c_e = sp.symbols("c_E", positive=True)
    f = sp.Function("f")(r)
    coords = (t, r, th, ph)
    g = sp.diag(-c_e**2 * f, 1 / f, r**2, r**2 * sp.sin(th) ** 2)
    gi = z(g.inv())
    n = 4

    gamma = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                gamma[a][b][c] = z(
                    sp.Rational(1, 2)
                    * sum(
                        gi[a, d]
                        * (
                            sp.diff(g[d, c], coords[b])
                            + sp.diff(g[d, b], coords[c])
                            - sp.diff(g[b, c], coords[d])
                        )
                        for d in range(n)
                    )
                )

    ric = sp.MutableDenseMatrix.zeros(n, n)
    for a in range(n):
        for b in range(n):
            ric[a, b] = z(
                sum(
                    sp.diff(gamma[c][a][b], coords[c])
                    - sp.diff(gamma[c][a][c], coords[b])
                    + sum(
                        gamma[c][c][d] * gamma[d][a][b]
                        - gamma[c][b][d] * gamma[d][a][c]
                        for d in range(n)
                    )
                    for c in range(n)
                )
            )

    scalar = z(sum(gi[a, b] * ric[a, b] for a in range(n) for b in range(n)))
    ein_cov = sp.MutableDenseMatrix(
        n, n, lambda a, b: z(ric[a, b] - sp.Rational(1, 2) * g[a, b] * scalar)
    )
    ein_mix = sp.MutableDenseMatrix(n, n, lambda a, b: z(sum(gi[a, c] * ein_cov[c, b] for c in range(n))))

    e0 = z(r**2 * ein_mix[0, 0])
    e1 = z(r**2 * ein_mix[2, 2])
    expected_e0 = r * sp.diff(f, r) + f - 1
    expected_e1 = r * sp.diff(f, r) + r**2 * sp.diff(f, r, 2) / 2
    assert z(e0 - expected_e0) == 0
    assert z(e1 - expected_e1) == 0
    assert z(r * sp.diff(e0, r) - 2 * e1) == 0

    c = sp.symbols("C", real=True)
    f_gr = 1 + c / r
    sub_gr = {
        f: f_gr,
        sp.diff(f, r): sp.diff(f_gr, r),
        sp.diff(f, r, 2): sp.diff(f_gr, r, 2),
    }
    ric_gr = sp.MutableDenseMatrix(n, n, lambda a, b: z(ric[a, b].subs(sub_gr)))
    ein_gr = sp.MutableDenseMatrix(n, n, lambda a, b: z(ein_mix[a, b].subs(sub_gr)))
    assert all(x == 0 for x in ric_gr)
    assert all(x == 0 for x in ein_gr)

    phi0, p, zeta = sp.symbols("phi p zeta", real=True)
    f0 = sp.exp(-2 * phi0)
    e0_phi = z(f0 * (1 - 2 * p) - 1)
    e1_phi = z(f0 * (2 * p**2 - 2 * p - zeta))

    r_s, u = sp.symbols("r_s u", real=True)
    f_u = 1 - u
    phi_u = -sp.log(f_u) / 2
    p_u = z(-u / (2 * f_u))
    zeta_u = z(u * (2 - u) / (2 * f_u**2))
    assert z(e0_phi.subs({phi0: phi_u, p: p_u})) == 0
    assert z(e1_phi.subs({phi0: phi_u, p: p_u, zeta: zeta_u})) == 0

    a_parallel = z(f0 * (2 * p**2 + p - zeta))
    a_perp = z(1 - f0 * (1 + p))
    a_parallel_gr = z(a_parallel.subs({phi0: phi_u, p: p_u, zeta: zeta_u}))
    a_perp_gr = z(a_perp.subs({phi0: phi_u, p: p_u}))
    assert z(a_parallel_gr + 3 * u / 2) == 0
    assert z(a_perp_gr - 3 * u / 2) == 0

    r_a, r_b = sp.symbols("r_A r_B", positive=True)
    f_a = 1 - r_s / r_a
    f_b = 1 - r_s / r_b
    v_a = -sp.log(f_a) / 2
    v_b = -sp.log(f_b) / 2
    delta_ab = z(v_b - v_a)
    q_ab = z(sp.exp(-2 * delta_ab))
    chi_ab = z((sp.exp(delta_ab) - sp.exp(-delta_ab)) / (sp.exp(delta_ab) + sp.exp(-delta_ab)))
    assert z(q_ab - f_b / f_a) == 0
    assert z(chi_ab - (f_a - f_b) / (f_a + f_b)) == 0

    weak_phi = sp.series(-sp.log(1 - u) / 2, u, 0, 5)
    weak_p = sp.series(p_u, u, 0, 5)
    weak_zeta = sp.series(zeta_u, u, 0, 5)
    kretschmann_gr = z(12 * r_s**2 / r**6)

    result = {
        "landing": "EXACT_GR_VACUUM_BRANCH_EMBEDS__PAIR_KERNEL_AND_ANGULAR_RESPONSE_REMAIN_NATIVE",
        "scope": "static_spherical_positive_f_vacuum_exterior_only",
        "metric_determinant": sp.sstr(z(g.det())),
        "ricci_scalar_general": sp.sstr(scalar),
        "einstein_mixed_diagonal": [sp.sstr(z(ein_mix[i, i])) for i in range(4)],
        "dimensionless_residuals": {
            "E0": sp.sstr(e0),
            "E1": sp.sstr(e1),
            "dependence": "r*d(E0)/dr = 2*E1",
            "E0_phi": sp.sstr(e0_phi),
            "E1_phi": sp.sstr(e1_phi),
        },
        "general_gr_vacuum_family": "f(r)=1+C/r on each connected exterior interval",
        "positive_mass_translation_conditional": "C=-r_s; r_s=2*G_obs*M/c_E^2 requires a supplied GR source/mass attachment",
        "pair_kernel": {
            "V": "-log(f)/2",
            "delta_AB": sp.sstr(delta_ab),
            "q_AB": sp.sstr(q_ab),
            "chi_AB": sp.sstr(chi_ab),
            "terminal_local": "Phi_hat_pair=phi for the matched static clock calibration",
        },
        "gr_branch_jets_in_u": {
            "u": "r_s/r",
            "phi": sp.sstr(phi_u),
            "p": sp.sstr(p_u),
            "zeta": sp.sstr(zeta_u),
        },
        "gr_branch_angular": {
            "A_parallel": sp.sstr(a_parallel_gr),
            "A_perp": sp.sstr(a_perp_gr),
            "sum": sp.sstr(z(a_parallel_gr + a_perp_gr)),
        },
        "weak_field": {
            "phi": str(weak_phi),
            "p": str(weak_p),
            "zeta": str(weak_zeta),
            "angular_order": "A_parallel=-3*u/2 and A_perp=+3*u/2 exactly",
        },
        "curvature": {
            "Ricci_on_branch": "0",
            "Einstein_on_branch": "0",
            "Kretschmann_on_positive_mass_not_flat": sp.sstr(kretschmann_gr),
        },
        "checks": {
            "direct_tensor_derivation": True,
            "full_ricci_zero_on_family": True,
            "residual_rank_one_on_primary_family": True,
            "pair_kernel_no_added_response": True,
            "angular_response_no_added_response": True,
        },
        "maximum_conclusion": "Exact bounded GR embedding and native readouts only; no UDT departure law, mass sign, matter recovery, or complete history selected.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
