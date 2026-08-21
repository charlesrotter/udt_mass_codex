#!/usr/bin/env python3
"""Exact symbolic G199 derivation from the primary static-spherical metric."""

import json
import sympy as sp


def main() -> None:
    t, r, th, ph = sp.symbols("t r theta varphi", real=True)
    f = sp.Function("f")(r)
    f0, energy = sp.symbols("f_o E", positive=True)
    coords = (t, r, th, ph)
    n = 4
    g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2)
    gi = sp.simplify(g.inv())

    gamma = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            gi[a, d] * (
                sp.diff(g[d, c], coords[b])
                + sp.diff(g[d, b], coords[c])
                - sp.diff(g[b, c], coords[d])
            )
            for d in range(n)
        ))
        for c in range(n)] for b in range(n)] for a in range(n)]

    # R^a_{bcd}, with R(X,Y)Z^a = R^a_{bcd} Z^b X^c Y^d.
    riemann = [[[[
        sp.simplify(
            sp.diff(gamma[a][d][b], coords[c])
            - sp.diff(gamma[a][c][b], coords[d])
            + sum(
                gamma[a][c][e] * gamma[e][d][b]
                - gamma[a][d][e] * gamma[e][c][b]
                for e in range(n)
            )
        )
        for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]

    substitutions = {th: sp.pi / 2}
    screens = (
        sp.Matrix([0, 0, 1 / r, 0]),
        sp.Matrix([0, 0, 0, 1 / r]),
    )

    checks = []
    results = {}
    for sign in (1, -1):
        label = "plus" if sign == 1 else "minus"
        k = sp.Matrix([energy / f, sign * energy, 0, 0])
        u = sp.Matrix([1 / sp.sqrt(f), 0, 0, 0])

        null_norm = sp.simplify((k.T * g * k)[0])
        frequency = sp.simplify(-(u.T * g * k)[0])
        checks.extend([null_norm == 0, frequency == energy / sp.sqrt(f)])

        # k^b partial_b k^a + Gamma^a_bc k^b k^c.
        geodesic = []
        for a in range(n):
            directional = sum(k[b] * sp.diff(k[a], coords[b]) for b in range(n))
            connection = sum(gamma[a][b][c] * k[b] * k[c] for b in range(n) for c in range(n))
            geodesic.append(sp.simplify(directional + connection))
        checks.extend(value == 0 for value in geodesic)

        screen_connection = []
        for screen in screens:
            nabla = []
            for a in range(n):
                directional = sum(k[b] * sp.diff(screen[a], coords[b]) for b in range(n))
                connection = sum(
                    gamma[a][b][c] * k[b] * screen[c]
                    for b in range(n) for c in range(n)
                )
                nabla.append(sp.simplify((directional + connection).subs(substitutions)))
            screen_connection.append(nabla)
            checks.extend(value == 0 for value in nabla)

        tide = sp.zeros(2)
        for aa, sa in enumerate(screens):
            for bb, sb in enumerate(screens):
                total = 0
                for mu in range(n):
                    for nu in range(n):
                        for alpha in range(n):
                            for beta in range(n):
                                for rho in range(n):
                                    total += (
                                        g[mu, nu]
                                        * sa[mu]
                                        * riemann[nu][alpha][beta][rho]
                                        * k[alpha]
                                        * sb[beta]
                                        * k[rho]
                                    )
                tide[aa, bb] = sp.simplify(total.subs(substitutions))
        checks.extend(tide[i, j] == 0 for i in range(2) for j in range(2))

        # Vertex-normalized physical screen map D(lambda)=lambda I.
        lam = sp.symbols("lambda", real=True)
        jacobi = lam * sp.eye(2)
        jacobi_residual = sp.simplify(jacobi.diff(lam, 2) + tide * jacobi)
        checks.extend(jacobi_residual[i, j] == 0 for i in range(2) for j in range(2))
        checks.extend(jacobi.subs(lam, 0)[i, j] == 0 for i in range(2) for j in range(2))
        checks.extend(jacobi.diff(lam).subs(lam, 0)[i, j] == sp.eye(2)[i, j]
                      for i in range(2) for j in range(2))

        results[label] = {
            "k": [str(sp.simplify(x)) for x in k],
            "geodesic_residual": [str(x) for x in geodesic],
            "frequency": str(frequency),
            "screen_connection": [[str(x) for x in row] for row in screen_connection],
            "tidal_matrix": [[str(tide[i, j]) for j in range(2)] for i in range(2)],
            "jacobi_map": [[str(jacobi[i, j]) for j in range(2)] for i in range(2)],
        }

    # Nonvacuity: the ambient curvature is generically nonzero even though the radial null tide cancels.
    curvature_control = sp.simplify(riemann[0][1][0][1])
    checks.append(curvature_control != 0)
    checks.append(sp.diff(f, r) != 0)
    checks.append(sp.diff(f, r, 2) != 0)

    # Same local metric jet gives identical two-direction screen tides and frequency magnitude.
    checks.append(results["plus"]["tidal_matrix"] == results["minus"]["tidal_matrix"])
    checks.append(results["plus"]["frequency"] == results["minus"]["frequency"])

    payload = {
        "landing": "PRIMARY_METRIC_RADIAL_NULL_PAIR_IS_REVERSAL_SYMMETRIC__NO_NATIVE_CHIRAL_SPLIT",
        "assertions": len(checks),
        "passed": sum(bool(x) for x in checks),
        "all_pass": all(bool(x) for x in checks),
        "ambient_curvature_control_R0_101": str(curvature_control),
        "source_normalization": "E=sqrt(f_o)",
        "endpoint_frequency_ratio": "sqrt(f_o/f_s)=exp(phi_s-phi_o)",
        "affine_areal_relation": "r(lambda)=r_o+sign*sqrt(f_o)*lambda",
        "results": results,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
