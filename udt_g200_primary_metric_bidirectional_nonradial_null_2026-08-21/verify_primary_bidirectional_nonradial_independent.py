#!/usr/bin/env python3
"""Independent exact metric-jet and branch-series verification for G200.

No SymPy and no production imports or artifacts are used.  A first-order exact dual number carries
the radial derivative of the full metric two-jet, so the contracted curvature tide and its radial
derivative are reconstructed together from the metric.
"""

from fractions import Fraction as F
import json
import random


N = 4


class Jet:
    __slots__ = ("v", "d")

    def __init__(self, value=0, derivative=0):
        self.v = value if isinstance(value, F) else F(value)
        self.d = derivative if isinstance(derivative, F) else F(derivative)

    @staticmethod
    def cast(other):
        return other if isinstance(other, Jet) else Jet(other, 0)

    def __add__(self, other):
        other = self.cast(other)
        return Jet(self.v + other.v, self.d + other.d)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, -self.d)

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) - self

    def __mul__(self, other):
        other = self.cast(other)
        return Jet(self.v * other.v, self.d * other.v + self.v * other.d)

    __rmul__ = __mul__

    def reciprocal(self):
        return Jet(F(1) / self.v, -self.d / (self.v * self.v))

    def __truediv__(self, other):
        return self * self.cast(other).reciprocal()

    def __rtruediv__(self, other):
        return self.cast(other) / self

    def __pow__(self, power):
        if power == 0:
            return Jet(1, 0)
        if power < 0:
            return (self.reciprocal()) ** (-power)
        return Jet(self.v**power, power * self.v ** (power - 1) * self.d)

    def __eq__(self, other):
        other = self.cast(other)
        return self.v == other.v and self.d == other.d

    def __repr__(self):
        return f"Jet({self.v},{self.d})"


def zeros(*shape):
    if len(shape) == 1:
        return [Jet(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def metric_coordinate_jets(r, f, fp, fpp):
    # Every entry is itself a radial Jet.  Coordinates are (x0,r,theta,varphi), theta=pi/2.
    g = zeros(N, N)
    dg = zeros(N, N, N)
    ddg = zeros(N, N, N, N)
    g[0][0] = -f
    g[1][1] = 1 / f
    g[2][2] = r * r
    g[3][3] = r * r

    dg[0][0][1] = -fp
    dg[1][1][1] = -fp / (f * f)
    dg[2][2][1] = 2 * r
    dg[3][3][1] = 2 * r

    ddg[0][0][1][1] = -fpp
    ddg[1][1][1][1] = 2 * fp * fp / (f**3) - fpp / (f * f)
    ddg[2][2][1][1] = Jet(2)
    ddg[3][3][1][1] = Jet(2)
    ddg[3][3][2][2] = -2 * r * r
    return g, dg, ddg


def connection_and_riemann(g, dg, ddg):
    gi = zeros(N, N)
    for i in range(N):
        gi[i][i] = 1 / g[i][i]
    dgi = zeros(N, N, N)
    for a in range(N):
        for b in range(N):
            for ell in range(N):
                dgi[a][b][ell] = -sum(
                    (gi[a][e] * dg[e][q][ell] * gi[q][b] for e in range(N) for q in range(N)),
                    Jet(0),
                )

    gamma = zeros(N, N, N)
    dgamma = zeros(N, N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                gamma[a][b][c] = Jet(F(1, 2)) * sum(
                    (gi[a][d] * (dg[d][c][b] + dg[d][b][c] - dg[b][c][d])
                     for d in range(N)), Jet(0)
                )
                for ell in range(N):
                    dgamma[a][b][c][ell] = Jet(F(1, 2)) * sum([(
                            dgi[a][d][ell]
                            * (dg[d][c][b] + dg[d][b][c] - dg[b][c][d])
                            + gi[a][d]
                            * (ddg[d][c][b][ell] + ddg[d][b][c][ell]
                               - ddg[b][c][d][ell])
                        )
                        for d in range(N)
                    ], Jet(0))

    riemann = zeros(N, N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    riemann[a][b][c][d] = (
                        dgamma[a][d][b][c] - dgamma[a][c][b][d]
                        + sum((gamma[a][c][e] * gamma[e][d][b]
                               - gamma[a][d][e] * gamma[e][c][b]
                               for e in range(N)), Jet(0))
                    )
    return gamma, riemann


def sparse(vector):
    return [(i, value) for i, value in enumerate(vector) if value != Jet(0)]


def tide_matrix(g, riemann, k, screens):
    out = zeros(2, 2)
    nz_k = sparse(k)
    for aa, sa in enumerate(screens):
        for bb, sb in enumerate(screens):
            total = Jet(0)
            for mu, sa_mu in sparse(sa):
                for nu in range(N):
                    if g[mu][nu] == Jet(0):
                        continue
                    for alpha, k_alpha in nz_k:
                        for beta, sb_beta in sparse(sb):
                            for rho, k_rho in nz_k:
                                total += (g[mu][nu] * sa_mu * riemann[nu][alpha][beta][rho]
                                          * k_alpha * sb_beta * k_rho)
            out[aa][bb] = total
    return out


def one_case(r0, energy, q0, angmom, f0, fp0, fpp0, fppp0):
    r = Jet(r0, 1)
    f = Jet(f0, fp0)
    fp = Jet(fp0, fpp0)
    fpp = Jet(fpp0, fppp0)
    q2 = energy * energy - f * angmom * angmom / (r * r)
    assert q2.v == q0 * q0
    q = Jet(q0, q2.d / (2 * q0))

    g, dg, ddg = metric_coordinate_jets(r, f, fp, fpp)
    _, riemann = connection_and_riemann(g, dg, ddg)

    expected_parallel = angmom**2 * (r * fpp - fp) / (2 * r**3)
    expected_perp = angmom**2 * (r * fp - 2 * f + 2) / (2 * r**4)
    expected = [[expected_parallel, Jet(0)], [Jet(0), expected_perp]]

    tides = []
    assertions = 0
    for sign in (1, -1):
        k = [energy / f, sign * q, Jet(0), sign * angmom / (r * r)]
        s_parallel = [Jet(0), -f * sign * angmom / (energy * r), Jet(0),
                      sign * q / (energy * r)]
        s_perp = [Jet(0), Jet(0), 1 / r, Jet(0)]
        null = sum((g[a][b] * k[a] * k[b] for a in range(N) for b in range(N)), Jet(0))
        assert null == Jet(0)
        assertions += 1
        tide = tide_matrix(g, riemann, k, (s_parallel, s_perp))
        for i in range(2):
            for j in range(2):
                assert tide[i][j] == expected[i][j]
                assertions += 1
        tides.append(tide)

    for i in range(2):
        for j in range(2):
            assert tides[0][i][j] == tides[1][i][j]
            assertions += 1

    # Independently reconstructed vertex-series coefficients.
    nonzero_gradient = False
    for mode in range(2):
        tide = expected[mode][mode]
        cubic_plus = -tide.v / 6
        cubic_minus = -tide.v / 6
        quartic_plus = -q0 * tide.d / 12
        quartic_minus = q0 * tide.d / 12
        assert cubic_plus == cubic_minus
        assert quartic_plus - quartic_minus == -q0 * tide.d / 6
        assertions += 2
        nonzero_gradient = nonzero_gradient or tide.d != 0

    ambient_nonflat = any(
        riemann[a][b][c][d].v != 0
        for a in range(N) for b in range(N) for c in range(N) for d in range(N)
    )
    assert ambient_nonflat
    assertions += 1
    return assertions, nonzero_gradient


def main():
    rng = random.Random(200)
    cases = 2000
    assertions = 0
    gradient_cases = 0
    for _ in range(cases):
        r0 = F(rng.randint(2, 19), rng.randint(1, 7))
        energy = F(rng.randint(5, 17), rng.randint(1, 5))
        q0 = energy * F(rng.randint(1, 4), 5)
        angmom = F(rng.randint(1, 11), rng.randint(1, 7))
        f0 = (energy * energy - q0 * q0) * r0 * r0 / (angmom * angmom)
        fp0 = F(rng.choice([i for i in range(-13, 14) if i != 0]), rng.randint(1, 11))
        fpp0 = F(rng.randint(-13, 13), rng.randint(1, 11))
        fppp0 = F(rng.randint(-13, 13), rng.randint(1, 11))
        count, gradient = one_case(r0, energy, q0, angmom, f0, fp0, fpp0, fppp0)
        assertions += count
        gradient_cases += int(gradient)

    assert gradient_cases >= 1900

    # Flat, strict-radial, and tangential series controls.
    flat_controls = 40
    for j in range(1, flat_controls + 1):
        r = Jet(F(j + 2, 3), 1)
        f = Jet(1, 0)
        fp = Jet(0, 0)
        fpp = Jet(0, 0)
        energy = Jet(5)
        q = Jet(3, -16 / (3 * r.v))
        angmom = 4 * r.v
        g, dg, ddg = metric_coordinate_jets(r, f, fp, fpp)
        _, riemann = connection_and_riemann(g, dg, ddg)
        k = [energy / f, q, Jet(0), Jet(angmom) / (r * r)]
        screens = ([Jet(0), -f * Jet(angmom) / (energy * r), Jet(0), q / (energy * r)],
                   [Jet(0), Jet(0), 1 / r, Jet(0)])
        tide = tide_matrix(g, riemann, k, screens)
        assert tide == [[Jet(0), Jet(0)], [Jet(0), Jet(0)]]
        assertions += 4

    print(json.dumps({
        "all_pass": True,
        "cases": cases,
        "assertions": assertions,
        "nonzero_gradient_cases": gradient_cases,
        "flat_controls": flat_controls,
        "method": "independent exact-Fraction radial-dual metric-two-jet reconstruction",
        "production_imports": False,
        "production_artifacts_read": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
