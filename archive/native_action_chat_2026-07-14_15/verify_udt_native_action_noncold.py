#!/usr/bin/env python3
"""Symbolic checks for UDT_NATIVE_ACTION_NONCOLD_DERIVATION_RESULTS.md.

This script verifies encoded algebra only. It does not certify the premise set,
action completeness, native provenance, boundary legality, or uniqueness.
"""

import sympy as sp


def assert_zero(name, expr):
    value = sp.simplify(sp.trigsimp(expr))
    if value != 0:
        raise AssertionError(f"{name}: expected zero, got {value}")
    print(f"PASS {name}")


def geometry(metric, coords):
    dim = len(coords)
    inv = sp.simplify(metric.inv())
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                gamma[a][b][c] = sp.simplify(
                    sum(
                        inv[a, d]
                        * (
                            sp.diff(metric[d, b], coords[c])
                            + sp.diff(metric[d, c], coords[b])
                            - sp.diff(metric[b, c], coords[d])
                        )
                        for d in range(dim)
                    )
                    / 2
                )

    ricci = sp.zeros(dim)
    for a in range(dim):
        for b in range(dim):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(gamma[c][a][b], coords[c])
                    - sp.diff(gamma[c][a][c], coords[b])
                    + sum(
                        gamma[c][c][d] * gamma[d][a][b]
                        - gamma[c][b][d] * gamma[d][a][c]
                        for d in range(dim)
                    )
                    for c in range(dim)
                )
            )
    scalar = sp.simplify(
        sum(inv[a, b] * ricci[a, b] for a in range(dim) for b in range(dim))
    )
    einstein_down = sp.simplify(ricci - metric * scalar / 2)
    einstein_mixed = sp.simplify(inv * einstein_down)
    return inv, ricci, scalar, einstein_mixed


def euler_second_order(lagrangian, field, coordinate):
    return sp.simplify(
        sp.diff(lagrangian, field)
        - sp.diff(sp.diff(lagrangian, sp.diff(field, coordinate)), coordinate)
        + sp.diff(
            sp.diff(lagrangian, sp.diff(field, coordinate, 2)), coordinate, 2
        )
    )


def main():
    t, r, th, ph = sp.symbols("t r theta varphi", real=True)
    coords = (t, r, th, ph)

    # A. Reciprocal simple metric: exact curvature, total derivative, and tensor equations.
    A = sp.Function("A")(r)
    metric_a = sp.diag(-A, 1 / A, r**2, r**2 * sp.sin(th) ** 2)
    _, _, scalar_a, einstein_a = geometry(metric_a, coords)
    scalar_expected = -sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
    assert_zero("A1 reciprocal Ricci scalar", scalar_a - scalar_expected)
    assert_zero("A2 reciprocal determinant", metric_a.det() + r**4 * sp.sin(th) ** 2)

    reduced_eh = sp.expand(r**2 * scalar_a)
    boundary_primitive = -r**2 * sp.diff(A, r) - 2 * r * A + 2 * r
    assert_zero("A3 reduced EH is a radial boundary term", reduced_eh - sp.diff(boundary_primitive, r))
    assert_zero("A4 reduced EH tangent Euler equation is empty", euler_second_order(reduced_eh, A, r))

    gt_expected = (r * sp.diff(A, r) + A - 1) / r**2
    gang_expected = sp.diff(A, r, 2) / 2 + sp.diff(A, r) / r
    assert_zero("A5 unrestricted-then-restricted Gt", einstein_a[0, 0] - gt_expected)
    assert_zero("A6 unrestricted-then-restricted Gr", einstein_a[1, 1] - gt_expected)
    assert_zero("A7 unrestricted-then-restricted Gang", einstein_a[2, 2] - gang_expected)

    # B. Free SSS EH variation and the multiplier/tangent-variation distinction.
    nu = sp.Function("nu")(r)
    lam = sp.Function("lam")(r)
    metric_free = sp.diag(-sp.exp(2 * nu), sp.exp(2 * lam), r**2, r**2 * sp.sin(th) ** 2)
    _, _, scalar_free, _ = geometry(metric_free, coords)
    reduced_free = sp.simplify(sp.exp(nu + lam) * r**2 * scalar_free)
    e_nu = euler_second_order(reduced_free, nu, r)
    e_lam = euler_second_order(reduced_free, lam, r)
    on_constraint = {lam: -nu}
    e_nu_c = sp.simplify(e_nu.subs(on_constraint).doit())
    e_lam_c = sp.simplify(e_lam.subs(on_constraint).doit())
    assert_zero("B1 tangent/multiplier equation on reciprocity", e_nu_c - e_lam_c)

    A_free = sp.Function("A_free")(r)
    e_full_a = sp.simplify(e_nu_c.subs(nu, sp.log(A_free) / 2).doit())
    assert_zero("B2 full EH equation retains A+rA'=1", e_full_a - 2 * (1 - A_free - r * sp.diff(A_free, r)))

    # A multiplier gives E_nu + mu = E_lam + mu = 0. Eliminating mu gives only
    # E_nu-E_lam=0, already identically zero on the reciprocal surface.
    multiplier = sp.symbols("multiplier")
    multiplier_eliminated = sp.simplify((e_nu_c + multiplier) - (e_lam_c + multiplier))
    assert_zero("B3 multiplier does not restore the discarded normal equation", multiplier_eliminated)

    # C. The R1-legal reduced kinetic family is not coefficient-unique.
    phi = sp.Function("phi")(r)
    zeta, mu = sp.symbols("zeta mu", real=True)
    rho = sp.Function("rho")(r)
    kinetic_family = (
        rho**2 * zeta * sp.diff(phi, r) ** 2 / 2
        + 2 * mu * rho * sp.diff(rho, r) * sp.diff(phi, r)
    )
    e_phi_family = euler_second_order(kinetic_family, phi, r)
    assert_zero(
        "C1 kinetic family Euler equation",
        e_phi_family
        + sp.diff(
            zeta * rho**2 * sp.diff(phi, r)
            + 2 * mu * rho * sp.diff(rho, r),
            r,
        ),
    )
    # Different mu values change the equation for a general transverse profile.
    assert_zero(
        "C2 nonzero mixing changes dynamics",
        sp.diff(e_phi_family, mu)
        + sp.diff(2 * rho * sp.diff(rho, r), r),
    )

    # D. Same reference static energy, different lapse source.
    N = sp.symbols("N", positive=True)
    a2, a4 = sp.symbols("a2 a4", real=True)
    rho2, rho4 = sp.symbols("rho2 rho4", real=True)
    lapse_lagrangian = -N * (N**a2 * rho2 + N**a4 * rho4)
    assert_zero("D1 lapse family has the same N=1 static density", lapse_lagrangian.subs(N, 1) + rho2 + rho4)
    lapse_source = -sp.diff(lapse_lagrangian, N)
    source_at_one = sp.simplify(lapse_source.subs(N, 1))
    assert_zero("D2 lapse source depends on completion", source_at_one - ((1 + a2) * rho2 + (1 + a4) * rho4))

    # E. Conditional minimal physical-metric stress trace and mass identity.
    xi, kappa4, X, Y = sp.symbols("xi kappa4 X Y", real=True)
    rho_min = xi * X / 2 + kappa4 * Y / 4
    stress_trace = -xi * X / 2 + kappa4 * Y / 4
    rho4_min = kappa4 * Y / 4
    assert_zero("E1 L2 cancels from rho+S", rho_min + stress_trace - 2 * rho4_min)

    kappa_g, lapse = sp.symbols("kappa_g lapse", real=True)
    lapse_rhs = kappa_g * lapse * (rho_min + stress_trace) / 2
    assert_zero("E2 conditional EH lapse source", lapse_rhs - kappa_g * lapse * rho4_min)

    scale, E2, E4 = sp.symbols("scale E2 E4", positive=True)
    scaled_energy = scale * E2 + E4 / scale
    assert_zero("E3 Derrick stationarity gives E2=E4", sp.diff(scaled_energy, scale).subs(scale, 1) - (E2 - E4))
    second_at_virial = sp.diff(scaled_energy, scale, 2).subs({scale: 1, E2: E4})
    assert_zero("E4 virial curvature is 2E4", second_at_virial - 2 * E4)
    assert_zero(
        "E5 conditional weak-field mass identity",
        (2 * E4 - (E2 + E4)).subs(E2, E4),
    )

    print("ALL SYMBOLIC CHECKS PASS")


if __name__ == "__main__":
    main()
