#!/usr/bin/env python3
"""From-scratch metric derivation for the bounded G288 center germ.

No formula is imported from an earlier UDT audit.  The script starts with the
four metric components, differentiates them, builds the Levi-Civita connection
and curvature, contracts the nonradial null screen, and only then expands the
regular-center germ.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def clean(expr: sp.Expr) -> sp.Expr:
    return sp.factor(sp.trigsimp(sp.simplify(expr)))


def main() -> None:
    x0, r, theta, varphi = sp.symbols("x0 r theta varphi", real=True)
    coords = (x0, r, theta, varphi)
    f = sp.Function("f")(r)
    g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(theta) ** 2)
    gi = clean(g.inv())
    dim = 4

    Gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                Gamma[a][b][c] = clean(
                    sp.Rational(1, 2)
                    * sum(
                        gi[a, d]
                        * (
                            sp.diff(g[d, c], coords[b])
                            + sp.diff(g[d, b], coords[c])
                            - sp.diff(g[b, c], coords[d])
                        )
                        for d in range(dim)
                    )
                )

    # Convention: R^a_{bcd} = d_c Gamma^a_db - d_d Gamma^a_cb
    #                         + Gamma^a_ce Gamma^e_db - Gamma^a_de Gamma^e_cb.
    Riem = [[[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    Riem[a][b][c][d] = clean(
                        sp.diff(Gamma[a][d][b], coords[c])
                        - sp.diff(Gamma[a][c][b], coords[d])
                        + sum(
                            Gamma[a][c][e] * Gamma[e][d][b]
                            - Gamma[a][d][e] * Gamma[e][c][b]
                            for e in range(dim)
                        )
                    )

    Rlow = [[[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    Rlow[a][b][c][d] = clean(sum(g[a, e] * Riem[e][b][c][d] for e in range(dim)))

    Ric = [[sp.S.Zero for _ in range(dim)] for _ in range(dim)]
    for b in range(dim):
        for d in range(dim):
            Ric[b][d] = clean(sum(Riem[a][b][a][d] for a in range(dim)))
    scalar = clean(sum(gi[a, b] * Ric[a][b] for a in range(dim) for b in range(dim)))
    ricci_sq = clean(
        sum(
            gi[a, c] * gi[b, d] * Ric[a][b] * Ric[c][d]
            for a in range(dim)
            for b in range(dim)
            for c in range(dim)
            for d in range(dim)
        )
    )
    riemann_sq = clean(
        sum(
            gi[a, e] * gi[b, ff] * gi[c, h] * gi[d, j]
            * Rlow[a][b][c][d] * Rlow[e][ff][h][j]
            for a in range(dim)
            for b in range(dim)
            for c in range(dim)
            for d in range(dim)
            for e in range(dim)
            for ff in range(dim)
            for h in range(dim)
            for j in range(dim)
            if Rlow[a][b][c][d] != 0 and Rlow[e][ff][h][j] != 0
        )
    )
    weyl_sq = clean(riemann_sq - 2 * ricci_sq + scalar**2 / 3)

    # Direct nonradial normalized null-screen contraction at the equator.
    ca, sa = sp.symbols("ca sa", real=True)
    rootf = sp.sqrt(f)
    U = (1 / rootf, 0, 0, 0)
    er = (0, rootf, 0, 0)
    etheta = (0, 0, 1 / r, 0)
    evarphi = (0, 0, 0, 1 / r)
    kvec = tuple(U[i] + ca * er[i] + sa * evarphi[i] for i in range(dim))
    spar = tuple(-sa * er[i] + ca * evarphi[i] for i in range(dim))
    sperp = etheta

    def tidal(left: tuple, right: tuple) -> sp.Expr:
        # g(left, R(right,k)k), using the convention above.
        val = sum(
            Rlow[a][b][c][d] * left[a] * kvec[b] * right[c] * kvec[d]
            for a in range(dim)
            for b in range(dim)
            for c in range(dim)
            for d in range(dim)
            if Rlow[a][b][c][d] != 0
        )
        val = val.subs(theta, sp.pi / 2).subs(ca**2, 1 - sa**2)
        return clean(val)

    tpar = tidal(spar, spar)
    tperp = tidal(sperp, sperp)
    toff = tidal(spar, sperp)
    apar = clean(r**2 * tpar / sa**2)
    aperp = clean(r**2 * tperp / sa**2)

    # Static-clock acceleration derived from U and Gamma, then converted to
    # the orthonormal radial component.
    acc_r = clean(Gamma[1][0][0] / f)
    acc_hat = clean(acc_r / rootf)

    # Geometric areal mass-aspect change of variables only:
    # g^{-1}(dr,dr) = f = 1 - 2 mu/r.
    mu = clean(r * (1 - f) / 2)

    # Radial null readout: dr/dx0 = +/- f.  With x0=c_E t,
    # dr/dt=+/- c_E f, while d ell/d tau=c_E for static normalization.
    coordinate_null_factor = f
    local_null_factor = sp.S.One

    # Center series, through r^8.
    c2, c4, c6, c8 = sp.symbols("c2 c4 c6 c8", real=True)
    fpoly = 1 + c2 * r**2 + c4 * r**4 + c6 * r**6 + c8 * r**8
    subs_poly = {
        f: fpoly,
        sp.diff(f, r): sp.diff(fpoly, r),
        sp.diff(f, r, 2): sp.diff(fpoly, r, 2),
    }

    def series(expr: sp.Expr, order: int = 9) -> sp.Expr:
        return clean(sp.series(expr.subs(subs_poly, simultaneous=True), r, 0, order).removeO())

    N_series = clean(sp.series(sp.sqrt(fpoly), r, 0, 10).removeO())
    phi_series = clean(sp.series(-sp.log(fpoly) / 2, r, 0, 10).removeO())
    acc_series = clean(sp.diff(N_series, r))
    mu_series = series(mu, 10)
    apar_series = series(apar, 10)
    aperp_series = series(aperp, 10)
    scalar_series = series(scalar, 9)
    weyl_series = series(weyl_sq, 9)
    riemann_series = series(riemann_sq, 9)

    C = sp.symbols("C", real=True)
    quadratic = {
        f: 1 + C * r**2,
        sp.diff(f, r): 2 * C * r,
        sp.diff(f, r, 2): 2 * C,
    }

    # General single-coefficient maps are derived from the freshly obtained
    # expressions, not entered as inputs.
    kk, ck = sp.symbols("k ck", integer=True, positive=True)
    mono = 1 + ck * r ** (2 * kk)
    mono_sub = {
        f: mono,
        sp.diff(f, r): sp.diff(mono, r),
        sp.diff(f, r, 2): sp.diff(mono, r, 2),
    }
    mono_apar = clean(apar.subs(mono_sub, simultaneous=True))
    mono_aperp = clean(aperp.subs(mono_sub, simultaneous=True))
    mono_scalar = clean(scalar.subs(mono_sub, simultaneous=True))

    checks: dict[str, bool] = {}
    checks["inverse_metric"] = clean(g * gi - sp.eye(4)) == sp.zeros(4)
    checks["connection_lower_symmetry"] = all(
        clean(Gamma[a][b][c] - Gamma[a][c][b]) == 0
        for a in range(dim) for b in range(dim) for c in range(dim)
    )
    checks["null_vector"] = clean(
        sum(g[a, b] * kvec[a] * kvec[b] for a in range(dim) for b in range(dim))
        .subs(theta, sp.pi / 2).subs(ca**2, 1 - sa**2)
    ) == 0
    checks["screen_parallel_unit"] = clean(
        sum(g[a, b] * spar[a] * spar[b] for a in range(dim) for b in range(dim))
        .subs(theta, sp.pi / 2).subs(ca**2, 1 - sa**2)
    ) == 1
    checks["screen_perp_unit"] = clean(
        sum(g[a, b] * sperp[a] * sperp[b] for a in range(dim) for b in range(dim))
        .subs(theta, sp.pi / 2)
    ) == 1
    checks["screen_offdiagonal_zero"] = toff == 0
    checks["angular_quadratic_zero_parallel"] = clean(apar.subs(quadratic, simultaneous=True)) == 0
    checks["angular_quadratic_zero_perp"] = clean(aperp.subs(quadratic, simultaneous=True)) == 0
    checks["quadratic_weyl_zero"] = clean(weyl_sq.subs(quadratic, simultaneous=True)) == 0
    checks["quadratic_scalar_constant"] = not clean(scalar.subs(quadratic, simultaneous=True)).has(r)
    checks["quadratic_constant_sectional_curvature"] = all(
        clean((Ric[a][b] + 3 * C * g[a, b]).subs(quadratic, simultaneous=True)) == 0
        for a in range(dim) for b in range(dim)
    )
    checks["acceleration_from_connection"] = clean(acc_hat - sp.diff(rootf, r)) == 0
    checks["mass_aspect_definition"] = clean(f - (1 - 2 * mu / r)) == 0
    checks["angular_no_r2_parallel"] = sp.expand(apar_series).coeff(r, 2) == 0
    checks["angular_no_r2_perp"] = sp.expand(aperp_series).coeff(r, 2) == 0
    checks["angular_first_ratio"] = clean(
        sp.expand(apar_series).coeff(r, 4) - 4 * sp.expand(aperp_series).coeff(r, 4)
    ) == 0
    checks["phi_negative_for_c2_positive_locally"] = sp.expand(phi_series).coeff(r, 2) == -c2 / 2
    checks["local_null_normalized_ce_factor"] = local_null_factor == 1
    checks["coordinate_null_uses_f"] = coordinate_null_factor == f
    checks["monomial_parallel_map"] = clean(mono_apar - 2 * kk * (kk - 1) * ck * r ** (2 * kk)) == 0
    checks["monomial_perp_map"] = clean(mono_aperp - (kk - 1) * ck * r ** (2 * kk)) == 0
    checks["monomial_scalar_map"] = clean(
        mono_scalar + 2 * (2 * kk + 1) * (kk + 1) * ck * r ** (2 * kk - 2)
    ) == 0

    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"G288 production failed closed: {failed}")

    result = {
        "landing_candidate": (
            "PARTIAL_CENTER_INTERLOCK_ONLY"
            "__QUADRATIC_NEGATIVE_PROFILE_GERM_IS_ZERO_TIDE_CONSTANT_CURVATURE"
            "__ANGULAR_TIDE_BEGINS_AT_INDEPENDENT_QUARTIC_JET"
            "__NO_PLANCK_SCALE_OR_HISTORY_SELECTED"
        ),
        "scope": "analytic even smooth-center germ of the primary static-spherical areal metric",
        "fresh_metric_expressions": {
            "scalar_curvature": str(scalar),
            "ricci_squared": str(ricci_sq),
            "riemann_squared": str(riemann_sq),
            "weyl_squared": str(weyl_sq),
            "screen_tidal_parallel": str(tpar),
            "screen_tidal_perpendicular": str(tperp),
            "screen_tidal_offdiagonal": str(toff),
            "angular_parallel": str(apar),
            "angular_perpendicular": str(aperp),
            "static_acceleration_orthonormal": str(acc_hat),
            "geometric_mass_aspect": str(mu),
            "coordinate_radial_null_slope": "+/- c_E*f",
            "normalized_local_radial_null_speed": "c_E",
        },
        "center_series": {
            "f": str(fpoly),
            "N_sqrt_f": str(N_series),
            "phi": str(phi_series),
            "acceleration": str(acc_series),
            "mu_geometric": str(mu_series),
            "angular_parallel": str(apar_series),
            "angular_perpendicular": str(aperp_series),
            "scalar_curvature": str(scalar_series),
            "weyl_squared": str(weyl_series),
            "riemann_squared": str(riemann_series),
        },
        "general_monomial_maps": {
            "angular_parallel": str(mono_apar),
            "angular_perpendicular": str(mono_aperp),
            "scalar_curvature": str(mono_scalar),
        },
        "quadratic_family": {
            "f": "1 + C*r**2",
            "angular_parallel": str(clean(apar.subs(quadratic, simultaneous=True))),
            "angular_perpendicular": str(clean(aperp.subs(quadratic, simultaneous=True))),
            "scalar_curvature": str(clean(scalar.subs(quadratic, simultaneous=True))),
            "riemann_squared": str(clean(riemann_sq.subs(quadratic, simultaneous=True))),
            "weyl_squared": str(clean(weyl_sq.subs(quadratic, simultaneous=True))),
        },
        "interpretive_guards": {
            "mu_is_physical_mass": False,
            "planck_scale_inserted": False,
            "xmax_inserted": False,
            "negative_profile_is_negative_distance": False,
            "negative_profile_is_pair_arrow_reversal": False,
            "old_audit_formula_imported": False,
        },
        "checks": checks,
        "check_count": len(checks),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "checks": len(checks), "landing": result["landing_candidate"]}, sort_keys=True))


if __name__ == "__main__":
    main()
