#!/usr/bin/env python3
"""Exact symbolic G200 derivation from the primary static-spherical metric."""

import json
import sympy as sp


def main() -> None:
    x0, r, th, ph = sp.symbols("x0 r theta varphi", real=True)
    energy, angmom = sp.symbols("E L", positive=True)
    lam = sp.symbols("lambda", real=True)
    f = sp.Function("f")(r)
    coords = (x0, r, th, ph)
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

    speed = sp.sqrt(energy**2 - f * angmom**2 / r**2)
    qdot = sp.simplify(angmom**2 * (2 * f - r * sp.diff(f, r)) / (2 * r**3))
    substitutions = {th: sp.pi / 2}

    tide_perp = sp.simplify(
        angmom**2 * (r * sp.diff(f, r) - 2 * f + 2) / (2 * r**4)
    )
    tide_parallel = sp.simplify(
        angmom**2 * (r * sp.diff(f, r, 2) - sp.diff(f, r)) / (2 * r**3)
    )
    tide_expected = sp.diag(tide_parallel, tide_perp)
    tide_r = sp.diag(sp.diff(tide_parallel, r), sp.diff(tide_perp, r))

    assertions = []
    branches = {}

    def contraction(sa, sb, k):
        total = 0
        nz_sa = [i for i in range(n) if sa[i] != 0]
        nz_sb = [i for i in range(n) if sb[i] != 0]
        nz_k = [i for i in range(n) if k[i] != 0]
        for mu in nz_sa:
            for nu in range(n):
                if g[mu, nu] == 0:
                    continue
                for alpha in nz_k:
                    for beta in nz_sb:
                        for rho in nz_k:
                            total += (
                                g[mu, nu] * sa[mu]
                                * riemann[nu][alpha][beta][rho]
                                * k[alpha] * sb[beta] * k[rho]
                            )
        return sp.simplify(total.subs(substitutions))

    for sign in (1, -1):
        label = "plus" if sign == 1 else "minus"
        signed_q = sign * speed
        signed_l = sign * angmom
        k = sp.Matrix([energy / f, signed_q, 0, signed_l / r**2])
        s_perp = sp.Matrix([0, 0, 1 / r, 0])
        s_parallel = sp.Matrix([
            0,
            -f * signed_l / (energy * r),
            0,
            signed_q / (energy * r),
        ])
        screens = (s_parallel, s_perp)

        null_norm = sp.simplify((k.T * g * k)[0].subs(substitutions))
        assertions.append(null_norm == 0)

        # Direct affine geodesic residual using the Killing first integrals.
        accelerations = sp.Matrix([
            sp.diff(energy / f, r) * signed_q,
            qdot,
            0,
            sp.diff(signed_l / r**2, r) * signed_q,
        ])
        geodesic = []
        for a in range(n):
            connection = sum(gamma[a][b][c] * k[b] * k[c]
                             for b in range(n) for c in range(n))
            geodesic.append(sp.simplify((accelerations[a] + connection).subs(substitutions)))
        assertions.extend(value == 0 for value in geodesic)

        # Orthonormal quotient screen at the event.
        gram = sp.Matrix([[sp.simplify((sa.T * g * sb)[0].subs(substitutions))
                           for sb in screens] for sa in screens])
        orthogonal = [sp.simplify((screen.T * g * k)[0].subs(substitutions))
                      for screen in screens]
        assertions.extend(gram[i, j] == sp.eye(2)[i, j]
                          for i in range(2) for j in range(2))
        assertions.extend(value == 0 for value in orthogonal)

        # Screen carry: s_perp is parallel; s_parallel is parallel in the quotient.
        screen_connection = []
        for screen_index, screen in enumerate(screens):
            nabla = []
            for a in range(n):
                directional = sum(k[b] * sp.diff(screen[a], coords[b]) for b in range(n))
                connection = sum(gamma[a][b][c] * k[b] * screen[c]
                                 for b in range(n) for c in range(n))
                nabla.append(sp.simplify((directional + connection).subs(substitutions)))
            if screen_index == 0:
                coefficient = -signed_l * sp.diff(f, r) / (2 * energy * r)
                quotient_residual = [sp.simplify(nabla[a] - coefficient * k[a])
                                     for a in range(n)]
            else:
                quotient_residual = nabla
            assertions.extend(value == 0 for value in quotient_residual)
            screen_connection.append([str(value) for value in nabla])

        tide = sp.Matrix([[contraction(sa, sb, k) for sb in screens] for sa in screens])
        tide_residual = sp.simplify(tide - tide_expected)
        assertions.extend(tide_residual[i, j] == 0 for i in range(2) for j in range(2))

        # Local vertex series through the first radial-sampling split.
        jacobi_series = sp.zeros(2)
        for mode in range(2):
            t0 = tide_expected[mode, mode]
            tr = tide_r[mode, mode]
            jacobi_series[mode, mode] = sp.expand(
                lam - t0 * lam**3 / 6 - sign * speed * tr * lam**4 / 12
            )
            # Coefficients lambda and lambda^2 of D''+T(lambda)D vanish exactly.
            local_tide = t0 + sign * speed * tr * lam
            residual = sp.expand(sp.diff(jacobi_series[mode, mode], lam, 2)
                                 + local_tide * jacobi_series[mode, mode])
            assertions.append(sp.expand(residual).coeff(lam, 1) == 0)
            assertions.append(sp.expand(residual).coeff(lam, 2) == 0)

        frequency = sp.simplify(energy / sp.sqrt(f))
        branches[label] = {
            "signed_radial_velocity": str(signed_q),
            "signed_angular_momentum": str(signed_l),
            "geodesic_residual": [str(value) for value in geodesic],
            "frequency": str(frequency),
            "screen_gram": [[str(gram[i, j]) for j in range(2)] for i in range(2)],
            "screen_connection": screen_connection,
            "tidal_matrix": [[str(tide[i, j]) for j in range(2)] for i in range(2)],
            "jacobi_series_through_lambda4": [str(jacobi_series[i, i]) for i in range(2)],
        }

    # The same event has one sign-blind local tide and frequency law.
    assertions.append(branches["plus"]["tidal_matrix"] == branches["minus"]["tidal_matrix"])
    assertions.append(branches["plus"]["frequency"] == branches["minus"]["frequency"])

    # The first accumulated difference is radial-gradient sampling at lambda^4.
    series_difference = sp.diag(
        -speed * sp.diff(tide_parallel, r) * lam**4 / 6,
        -speed * sp.diff(tide_perp, r) * lam**4 / 6,
    )
    assertions.append(series_difference.subs(angmom, 0) == sp.zeros(2))
    assertions.append(series_difference.subs(speed, 0) == sp.zeros(2))

    flat_subs = {
        f: 1,
        sp.diff(f, r): 0,
        sp.diff(f, r, 2): 0,
        sp.diff(f, r, 3): 0,
    }
    assertions.extend(sp.simplify(tide_expected[i, i].subs(flat_subs)) == 0 for i in range(2))
    assertions.extend(sp.simplify(tide_r[i, i].subs(flat_subs)) == 0 for i in range(2))

    # Explicit nonzero-gradient witness.
    witness = {
        r: sp.Rational(2),
        f: sp.Rational(3, 2),
        sp.diff(f, r): sp.Rational(1, 3),
        sp.diff(f, r, 2): sp.Rational(-2, 5),
        sp.diff(f, r, 3): sp.Rational(1, 7),
        energy: sp.Rational(2),
        angmom: sp.Rational(1),
    }
    witness_difference = sp.simplify(series_difference.subs(witness) / lam**4)
    assertions.extend(witness_difference[i, i] != 0 for i in range(2))

    payload = {
        "landing": "ONE_PRIMARY_NONRADIAL_LAW__FINITE_DIRECTIONAL_DIFFERENCE_IS_RADIAL_REGIME_SAMPLING",
        "all_pass": all(bool(item) for item in assertions),
        "assertions": len(assertions),
        "passed": sum(bool(item) for item in assertions),
        "common_tide": {
            "parallel": str(tide_parallel),
            "perpendicular": str(tide_perp),
        },
        "radial_tide_derivative": {
            "parallel": str(sp.simplify(sp.diff(tide_parallel, r))),
            "perpendicular": str(sp.simplify(sp.diff(tide_perp, r))),
        },
        "first_finite_difference_Dplus_minus_Dminus": [
            str(series_difference[i, i]) for i in range(2)
        ],
        "nonzero_gradient_witness_difference_over_lambda4": [
            str(witness_difference[i, i]) for i in range(2)
        ],
        "branches": branches,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
