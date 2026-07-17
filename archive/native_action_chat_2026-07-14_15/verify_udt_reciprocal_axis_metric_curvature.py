#!/usr/bin/env python3
"""Exact full-tensor curvature audit for a rank-one reciprocal-axis texture.

Metric:
  g_00=-1/q,
  g_ij=delta_ij+(q-1)n_i n_j,
  n(z)=(cos(kz),sin(kz),0),
with constant q=exp(2phi)>0.

All calculations are exact Fractions at z=0 using analytic first and second
metric derivatives. No finite differences or linearization are used.
"""

from fractions import Fraction as F


N = 4


def zeros(*shape):
    if len(shape) == 1:
        return [F(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def curvature(q, k, theta_second=0, q_first=0, q_second=0, parallel=False):
    q, k, theta_second = F(q), F(k), F(theta_second)
    q_first, q_second = F(q_first), F(q_second)

    # Coordinates: 0=t, 1=x, 2=y, 3=z. Values at z=0.
    g = zeros(N, N)
    g[0][0] = -1 / q
    g[2][2] = 1

    gi = zeros(N, N)
    gi[0][0] = -q
    gi[2][2] = 1

    if parallel:
        g[1][1] = 1
        g[3][3] = q
        gi[1][1] = 1
        gi[3][3] = 1 / q
    else:
        g[1][1] = q
        g[3][3] = 1
        gi[1][1] = 1 / q
        gi[3][3] = 1

    # dg[mu][a][b] = partial_mu g_ab.
    dg = zeros(N, N, N)
    dg[3][0][0] = q_first / q**2

    # d2g[mu][nu][a][b] = partial_mu partial_nu g_ab.
    d2g = zeros(N, N, N, N)
    d2g[3][3][0][0] = q_second / q**2 - 2 * q_first**2 / q**3

    if parallel:
        dg[3][3][3] = q_first
        dg[3][1][3] = (q - 1) * k
        dg[3][3][1] = (q - 1) * k
        d2g[3][3][3][3] = q_second - 2 * (q - 1) * k * k
        d2g[3][3][1][1] = 2 * (q - 1) * k * k
        d2g[3][3][1][3] = 2 * q_first * k + (q - 1) * theta_second
        d2g[3][3][3][1] = 2 * q_first * k + (q - 1) * theta_second
    else:
        dg[3][1][1] = q_first
        dg[3][1][2] = (q - 1) * k
        dg[3][2][1] = (q - 1) * k
        d2g[3][3][1][1] = q_second - 2 * (q - 1) * k * k
        d2g[3][3][2][2] = 2 * (q - 1) * k * k
        d2g[3][3][1][2] = 2 * q_first * k + (q - 1) * theta_second
        d2g[3][3][2][1] = 2 * q_first * k + (q - 1) * theta_second

    # Derivative of inverse metric.
    dgi = zeros(N, N, N)
    for mu in range(N):
        for a in range(N):
            for d in range(N):
                dgi[mu][a][d] = -sum(
                    gi[a][p] * dg[mu][p][s] * gi[s][d]
                    for p in range(N)
                    for s in range(N)
                )

    # Christoffel Gamma^a_bc.
    Gamma = zeros(N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                Gamma[a][b][c] = F(1, 2) * sum(
                    gi[a][d]
                    * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                    for d in range(N)
                )

    # Analytic derivative partial_mu Gamma^a_bc.
    dGamma = zeros(N, N, N, N)
    for mu in range(N):
        for a in range(N):
            for b in range(N):
                for c in range(N):
                    value = F(0)
                    for d in range(N):
                        bracket = dg[b][d][c] + dg[c][d][b] - dg[d][b][c]
                        dbracket = (
                            d2g[mu][b][d][c]
                            + d2g[mu][c][d][b]
                            - d2g[mu][d][b][c]
                        )
                        value += dgi[mu][a][d] * bracket + gi[a][d] * dbracket
                    dGamma[mu][a][b][c] = F(1, 2) * value

    # R^a_bcd = partial_c Gamma^a_db - partial_d Gamma^a_cb
    #          + Gamma^a_ce Gamma^e_db - Gamma^a_de Gamma^e_cb.
    Rup = zeros(N, N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    Rup[a][b][c][d] = (
                        dGamma[c][a][d][b]
                        - dGamma[d][a][c][b]
                        + sum(
                            Gamma[a][c][e] * Gamma[e][d][b]
                            - Gamma[a][d][e] * Gamma[e][c][b]
                            for e in range(N)
                        )
                    )

    Rlow = zeros(N, N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    Rlow[a][b][c][d] = sum(g[a][e] * Rup[e][b][c][d] for e in range(N))

    Ricci = zeros(N, N)
    for b in range(N):
        for d in range(N):
            Ricci[b][d] = sum(Rup[a][b][a][d] for a in range(N))

    Rscalar = sum(gi[a][b] * Ricci[a][b] for a in range(N) for b in range(N))

    Weyl = zeros(N, N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    ricci_wedge = (
                        g[a][c] * Ricci[b][d]
                        - g[a][d] * Ricci[b][c]
                        - g[b][c] * Ricci[a][d]
                        + g[b][d] * Ricci[a][c]
                    )
                    scalar_wedge = g[a][c] * g[b][d] - g[a][d] * g[b][c]
                    Weyl[a][b][c][d] = (
                        Rlow[a][b][c][d]
                        - F(1, 2) * ricci_wedge
                        + Rscalar * scalar_wedge / 6
                    )

    invdiag = [gi[i][i] for i in range(N)]
    Riemann2 = sum(
        Rlow[a][b][c][d] ** 2
        * invdiag[a]
        * invdiag[b]
        * invdiag[c]
        * invdiag[d]
        for a in range(N)
        for b in range(N)
        for c in range(N)
        for d in range(N)
    )
    Ricci2 = sum(
        Ricci[a][b] ** 2 * invdiag[a] * invdiag[b]
        for a in range(N)
        for b in range(N)
    )
    Weyl2 = sum(
        Weyl[a][b][c][d] ** 2
        * invdiag[a]
        * invdiag[b]
        * invdiag[c]
        * invdiag[d]
        for a in range(N)
        for b in range(N)
        for c in range(N)
        for d in range(N)
    )

    # Tensor audits.
    audits = {
        "gamma_lower_symmetry": all(
            Gamma[a][b][c] == Gamma[a][c][b]
            for a in range(N)
            for b in range(N)
            for c in range(N)
        ),
        "riemann_last_pair": all(
            Rlow[a][b][c][d] == -Rlow[a][b][d][c]
            for a in range(N)
            for b in range(N)
            for c in range(N)
            for d in range(N)
        ),
        "riemann_first_pair": all(
            Rlow[a][b][c][d] == -Rlow[b][a][c][d]
            for a in range(N)
            for b in range(N)
            for c in range(N)
            for d in range(N)
        ),
        "riemann_pair_exchange": all(
            Rlow[a][b][c][d] == Rlow[c][d][a][b]
            for a in range(N)
            for b in range(N)
            for c in range(N)
            for d in range(N)
        ),
        "riemann_first_bianchi": all(
            Rlow[a][b][c][d] + Rlow[a][c][d][b] + Rlow[a][d][b][c] == 0
            for a in range(N)
            for b in range(N)
            for c in range(N)
            for d in range(N)
        ),
        "ricci_symmetry": all(Ricci[a][b] == Ricci[b][a] for a in range(N) for b in range(N)),
        "weyl_trace": all(
            sum(gi[a][c] * Weyl[a][b][c][d] for a in range(N) for c in range(N)) == 0
            for b in range(N)
            for d in range(N)
        ),
        "weyl_invariant_identity": Weyl2 == Riemann2 - 2 * Ricci2 + Rscalar**2 / 3,
    }

    return {
        "q": q,
        "k": k,
        "theta_second": theta_second,
        "q_first": q_first,
        "q_second": q_second,
        "parallel": parallel,
        "R": Rscalar,
        "Ricci2": Ricci2,
        "Riemann2": Riemann2,
        "Weyl2": Weyl2,
        "audits": audits,
    }


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


base = curvature(F(9, 4), F(5, 3))
for name, ok in base["audits"].items():
    check(name.replace("_", " "), ok)

flat_q = curvature(F(1), F(5, 3))
flat_k = curvature(F(9, 4), F(0))
check("q=1 gives zero scalar curvature", flat_q["R"] == 0)
check("q=1 gives zero Ricci norm", flat_q["Ricci2"] == 0)
check("q=1 gives zero Riemann norm", flat_q["Riemann2"] == 0)
check("q=1 gives zero Weyl norm", flat_q["Weyl2"] == 0)
check("k=0 gives zero full curvature", all(flat_k[key] == 0 for key in ("R", "Ricci2", "Riemann2", "Weyl2")))
check("metric determinant is constant minus one", (-F(1, base["q"])) * base["q"] == -1)

# At z=0, n=(1,0,0) and only d_z n=(0,k,0) is nonzero. More generally every
# derivative is proportional to dz, so this exact point calculation represents
# the algebraic rank-one identity n dot (d_mu n cross d_nu n)=0.
nvec = (F(1), F(0), F(0))
dn = [(F(0), F(0), F(0)) for _ in range(N)]
dn[3] = (F(0), base["k"], F(0))


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


area = [
    sum(nvec[a] * cross(dn[mu], dn[nu])[a] for a in range(3))
    for mu in range(N)
    for nu in range(N)
]
check("manufactured axis texture has area-form F=0", all(value == 0 for value in area))
check("rank-one texture nevertheless has nonzero Weyl norm", base["Weyl2"] != 0)
check("rank-one texture has positive Weyl norm", base["Weyl2"] > 0)


def expected_invariants(q, k):
    q, k = F(q), F(k)
    d = q - 1
    return {
        "R": -d**2 * k**2 / (2 * q),
        "Ricci2": d**2 * (3 * q**2 + 2 * q + 3) * k**4 / (4 * q**2),
        "Riemann2": d**2 * (11 * q**2 + 10 * q + 11) * k**4 / (4 * q**2),
        "Weyl2": 4 * d**2 * (q**2 + q + 1) * k**4 / (3 * q**2),
    }


expected_base = expected_invariants(F(9, 4), F(5, 3))
for key in ("R", "Ricci2", "Riemann2", "Weyl2"):
    check(f"exact closed form for {key}", base[key] == expected_base[key])

# Exact k^4 scaling of quadratic curvature invariants and k^2 scaling of R.
k1, k2 = F(2, 3), F(7, 5)
c1 = curvature(F(9, 4), k1)
c2 = curvature(F(9, 4), k2)
check("scalar curvature scales as k^2", c2["R"] / c1["R"] == (k2 / k1) ** 2)
for key in ("Ricci2", "Riemann2", "Weyl2"):
    check(f"{key} scales as k^4", c2[key] / c1[key] == (k2 / k1) ** 4)

# Print exact probe values for independent reconstruction/interpolation.
print("\nEXACT PROBES (k=1):")
all_probe_formulas = True
for q in (F(1), F(3, 2), F(2), F(9, 4), F(3), F(4)):
    out = curvature(q, F(1))
    expected = expected_invariants(q, F(1))
    all_probe_formulas = all_probe_formulas and all(
        out[key] == expected[key] for key in ("R", "Ricci2", "Riemann2", "Weyl2")
    )
    print(
        f"q={q}: R={out['R']}, Ricci2={out['Ricci2']}, "
        f"Riemann2={out['Riemann2']}, Weyl2={out['Weyl2']}"
    )
check("closed forms hold at every rational q probe", all_probe_formulas)

passed = sum(ok for _, ok in checks)
total = len(checks)
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
