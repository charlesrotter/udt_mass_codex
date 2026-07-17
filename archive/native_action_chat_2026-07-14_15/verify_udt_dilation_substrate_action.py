#!/usr/bin/env python3
"""Exact algebra checks for UDT_DILATION_SUBSTRATE_ACTION_DERIVATION_RESULTS.md.

The script checks encoded differential-geometric and conservation identities.  It does not prove
the completeness of an action ansatz, the physical status of a working postulate, the Lovelock
classification theorem, or the existence of a time-live recycling solution.
"""

import sympy as sp


passed = 0


def check(label, condition):
    global passed
    if condition is not True and condition != sp.S.true:
        raise AssertionError(f"FAIL: {label}: {sp.simplify(condition)}")
    passed += 1
    print(f"PASS {passed:02d}: {label}")


def geometry(metric, coords):
    """Return Christoffels, Ricci tensor, and Ricci scalar for a coordinate metric."""
    dim = len(coords)
    inv = sp.simplify(metric.inv())
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                gamma[a][b][c] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inv[a, d]
                        * (
                            sp.diff(metric[d, c], coords[b])
                            + sp.diff(metric[d, b], coords[c])
                            - sp.diff(metric[b, c], coords[d])
                        )
                        for d in range(dim)
                    )
                )
    ricci = sp.MutableDenseMatrix(dim, dim, [0] * (dim * dim))
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
    scalar = sp.simplify(sum(inv[a, b] * ricci[a, b] for a in range(dim) for b in range(dim)))
    return inv, gamma, ricci, scalar


# 1. A nonzero accelerated-frame dilation gradient need not be curvature.
t, x, y, z = sp.symbols("t x y z", real=True)
a = sp.symbols("a", nonzero=True, real=True)
rindler = sp.diag(-(1 + a * x) ** 2, 1, 1, 1)
r_inv, r_gamma, r_ricci, r_scalar = geometry(rindler, (t, x, y, z))
coords_r = (t, x, y, z)
r_riemann = [
    [
        [
            [
                sp.simplify(
                    sp.diff(r_gamma[aa][bb][dd], coords_r[cc])
                    - sp.diff(r_gamma[aa][bb][cc], coords_r[dd])
                    + sum(
                        r_gamma[aa][cc][ee] * r_gamma[ee][bb][dd]
                        - r_gamma[aa][dd][ee] * r_gamma[ee][bb][cc]
                        for ee in range(4)
                    )
                )
                for dd in range(4)
            ]
            for cc in range(4)
        ]
        for bb in range(4)
    ]
    for aa in range(4)
]
check(
    "Rindler Riemann tensor vanishes",
    all(r_riemann[aa][bb][cc][dd] == 0 for aa in range(4) for bb in range(4) for cc in range(4) for dd in range(4)),
)
check("Rindler Ricci tensor vanishes", all(sp.simplify(v) == 0 for v in r_ricci))
check("Rindler Ricci scalar vanishes", sp.simplify(r_scalar) == 0)
phi_rindler = -sp.log(1 + a * x)
check("Rindler dilation-potential gradient is nonzero", sp.diff(phi_rindler, x) != 0)
check(
    "a first-gradient density would charge the flat accelerated chart",
    sp.simplify(sp.diff(phi_rindler, x) ** 2) != 0,
)


# 2. Reciprocal metric determinant and SR/UDT kinematic mapping.
phi, rr, X = sp.symbols("phi rr X", positive=True)
theta = sp.symbols("theta", real=True)
g_recip = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi), rr**2, rr**2 * sp.sin(theta) ** 2)
check(
    "reciprocal static determinant is phi-independent",
    sp.simplify(g_recip.det() + rr**4 * sp.sin(theta) ** 2) == 0,
)
beta2 = sp.symbols("beta2", real=True)
gamma_sr = 1 / sp.sqrt(1 - beta2)
gamma_x = 1 / sp.sqrt(1 - rr / X)
check("SR/UDT gamma map beta^2 <-> r/X", sp.simplify(gamma_sr.subs(beta2, rr / X) - gamma_x) == 0)
eps = sp.symbols("eps", positive=True)
check(
    "UDT kinematic gamma diverges at X",
    sp.limit(gamma_x.subs(rr, X * (1 - eps)), eps, 0, dir="+") == sp.oo,
)


# 3. Curvature of the unrestricted spherical reciprocal metric.
A = sp.Function("A")(rr)
spherical = sp.diag(-A, 1 / A, rr**2, rr**2 * sp.sin(theta) ** 2)
s_inv, s_gamma, s_ricci, R4 = geometry(spherical, (t, rr, theta, z))
R4_expected = -sp.diff(A, rr, 2) - 4 * sp.diff(A, rr) / rr - 2 * (A - 1) / rr**2
check("spherical reciprocal Ricci scalar", sp.simplify(R4 - R4_expected) == 0)
A_WRL = 1 - rr / X
R_WRL = sp.simplify(R4_expected.subs(A, A_WRL).doit())
check("WR-L is curved with R=6/(X r)", sp.simplify(R_WRL - 6 / (X * rr)) == 0)
check("flat A=1 has zero curvature", sp.simplify(R4_expected.subs(A, 1).doit()) == 0)


# 4. EH restricted before variation is a boundary functional in this one-function family.
L_EH_reduced = sp.expand(rr**2 * R4_expected)
boundary_primitive = -rr**2 * sp.diff(A, rr) - 2 * rr * (A - 1)
check(
    "reciprocal one-function EH radial density is a total derivative",
    sp.simplify(L_EH_reduced - sp.diff(boundary_primitive, rr)) == 0,
)
EL_EH = sp.simplify(
    sp.diff(L_EH_reduced, A)
    - sp.diff(sp.diff(L_EH_reduced, sp.diff(A, rr)), rr)
    + sp.diff(sp.diff(L_EH_reduced, sp.diff(A, rr, 2)), rr, 2)
)
check("reduced EH Euler operator vanishes identically", EL_EH == 0)
L_R2_reduced = sp.expand(rr**2 * R4_expected**2)
EL_R2 = sp.simplify(
    sp.diff(L_R2_reduced, A)
    - sp.diff(sp.diff(L_R2_reduced, sp.diff(A, rr)), rr)
    + sp.diff(sp.diff(L_R2_reduced, sp.diff(A, rr, 2)), rr, 2)
)
check("a curvature-squared action is a distinct nonempty bulk branch", EL_R2 != 0)
check("both R and R^2 densities vanish on flat geometry", R4_expected.subs(A, 1).doit() == 0 and L_R2_reduced.subs(A, 1).doit() == 0)


# 5. A symmetric stress tensor contracted with a Killing antisymmetric derivative vanishes.
Ts = sp.symbols("T00 T01 T02 T03 T11 T12 T13 T22 T23 T33")
T00, T01, T02, T03, T11, T12, T13, T22, T23, T33 = Ts
Tmat = sp.Matrix(
    [
        [T00, T01, T02, T03],
        [T01, T11, T12, T13],
        [T02, T12, T22, T23],
        [T03, T13, T23, T33],
    ]
)
k01, k02, k03, k12, k13, k23 = sp.symbols("k01 k02 k03 k12 k13 k23")
Kmat = sp.Matrix(
    [
        [0, k01, k02, k03],
        [-k01, 0, k12, k13],
        [-k02, -k12, 0, k23],
        [-k03, -k13, -k23, 0],
    ]
)
check("Killing antisymmetry makes the stationary energy current conserved", sp.expand(sum(Tmat[i, j] * Kmat[i, j] for i in range(4) for j in range(4))) == 0)


# 6. Infinite O(2)-symmetric substrate actions share the same kind of Noether charge.
tau = sp.symbols("tau", real=True)
q1 = sp.Function("q1")(tau)
q2 = sp.Function("q2")(tau)
s = q1**2 + q2**2
f = sp.Function("f")(s)
V = sp.Function("V")(s)
v2 = sp.diff(q1, tau) ** 2 + sp.diff(q2, tau) ** 2
L_o2 = sp.Rational(1, 2) * f * v2 - V
p1 = sp.diff(L_o2, sp.diff(q1, tau))
p2 = sp.diff(L_o2, sp.diff(q2, tau))
E1 = sp.diff(p1, tau) - sp.diff(L_o2, q1)
E2 = sp.diff(p2, tau) - sp.diff(L_o2, q2)
Q_o2 = sp.simplify(q1 * p2 - q2 * p1)
check("generic O(2) Noether identity", sp.simplify(sp.diff(Q_o2, tau) - (q1 * E2 - q2 * E1)) == 0)
L_member_1 = sp.Rational(1, 2) * v2 - s
L_member_2 = sp.Rational(1, 2) * (1 + s) * v2 - s**2
check("two distinct actions possess the same O(2) symmetry", sp.simplify(L_member_1 - L_member_2) != 0)
H_o2 = sp.simplify(p1 * sp.diff(q1, tau) + p2 * sp.diff(q2, tau) - L_o2)
static_subs = {sp.diff(q1, tau): 0, sp.diff(q2, tau): 0}
check(
    "internal charge is not automatically energy",
    sp.simplify(Q_o2.subs(static_subs)) == 0 and sp.simplify(H_o2.subs(static_subs) - V) == 0,
)


# 7. Exact recycling ledger, including the no-double-counting test.
fall, release, emerge = sp.symbols("fall release emerge", real=True)
dM_local = emerge - fall
dM_bh = fall - release
dM_reservoir = release - emerge
check("localized + horizon + reservoir transfer ledger closes", sp.simplify(dM_local + dM_bh + dM_reservoir) == 0)
check(
    "uncompensated replacement matter double-counts mass",
    sp.simplify((emerge - fall) + fall + 0) == emerge,
)


# 8. Static L2+L4 scale counting and one-mass calibration.
C2, C4, xi, kap, Rsize, me, c = sp.symbols("C2 C4 xi kap Rsize me c", positive=True)
E2s = C2 * xi * Rsize
E4s = C4 * kap / Rsize
Estat = E2s + E4s
stationary_relation = {kap: C2 * xi * Rsize**2 / C4}
check("Derrick stationarity gives E2=E4", sp.simplify((E2s - E4s).subs(stationary_relation)) == 0)
check("stationary carrier energy equals 2E4", sp.simplify((Estat - 2 * E4s).subs(stationary_relation)) == 0)
product_from_mass = me**2 * c**4 / (4 * C2 * C4)
Eeq_sq = 4 * C2 * C4 * xi * kap
check("one observed mass fixes the product xi*kappa", sp.simplify(Eeq_sq.subs(kap, product_from_mass / xi) - me**2 * c**4) == 0)
scale_free = sp.symbols("scale_free", positive=True)
R2_family = C4 * (product_from_mass / scale_free) / (C2 * scale_free)
check("the coupling ratio and physical size remain free", sp.simplify(sp.diff(R2_family, scale_free)) != 0)


# 9. Existing unrestricted and constrained carrier sources are not the same functional.
rho2, rho4, rho2par, rho4par = sp.symbols("rho2 rho4 rho2par rho4par")
source_unrestricted = 2 * rho4
source_reciprocal = 2 * (rho2par + rho4par)
check("unrestricted and reciprocal-constrained carrier sources differ generically", sp.simplify(source_unrestricted - source_reciprocal) != 0)


# 10. Constant mass is consistent with a constant X closure but does not fix its coefficient.
alpha, G, M, cc = sp.symbols("alpha G M cc", positive=True)
Xclosure = alpha * G * M / cc**2
Mdot = sp.symbols("Mdot")
Xdot = sp.diff(Xclosure, M) * Mdot
check("Mdot=0 implies Xdot=0 in the dimensional closure", sp.simplify(Xdot.subs(Mdot, 0)) == 0)
check("mass conservation does not determine the dimensionless closure coefficient", sp.diff(Xclosure, alpha) != 0)


print(f"\nRESULT: {passed}/{passed} checks pass")
