#!/usr/bin/env python3
"""CLAIM 1: independent Hilbert stress tensor for the deg-1 hedgehog.

I vary the action S = INT sqrt(-g) [ -(xi/2) g^{ab} d_a n . d_b n - (kap/4)|S|^2 ]
w.r.t. the metric to get T_{mn} = -(2/sqrt(-g)) dS/dg^{mn}, then raise to T^m_n.
Hedgehog: n = (sinTheta(r) nhat), with nhat = (sin th cos ph, sin th sin ph, cos th).
Metric: ds^2 = -e^{2a}dt^2 + e^{2b}dr^2 + r^2 dOmega^2.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi', real=True)
a = sp.Function('a')(r)
b = sp.Function('b')(r)
Th = sp.Function('Theta')(r)
xi, kap = sp.symbols('xi kappa', positive=True)

# metric (diagonal) and inverse
g = sp.diag(-sp.exp(2*a), sp.exp(2*b), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
sqrtg = sp.sqrt(-g.det())
coords = [t, r, th, ph]

# hedgehog unit field n in R^3 (target S^2): n depends on Th(r), th, ph
n1 = sp.sin(Th)*sp.sin(th)*sp.cos(ph)
n2 = sp.sin(Th)*sp.sin(th)*sp.sin(ph)
n3 = sp.cos(Th)
n = [n1, n2, n3]

# d_a n
dn = [[sp.diff(ni, c) for c in coords] for ni in n]  # dn[i][a]

# G_ab = d_a n . d_b n   (4x4)
Gmat = sp.zeros(4, 4)
for A in range(4):
    for Bb in range(4):
        Gmat[A, Bb] = sum(dn[i][A]*dn[i][Bb] for i in range(3))
Gmat = sp.simplify(Gmat)

# sigma model Lagrangian density (scalar): L2 = -(xi/2) g^{ab} G_ab
L2 = -sp.Rational(1, 2)*xi*sum(ginv[A, Bb]*Gmat[A, Bb] for A in range(4) for Bb in range(4))
L2 = sp.simplify(L2)

# Skyrme term: S_{mn} = d_m n x d_n n  (antisymmetric, vector-valued)
# |S|^2 = S_{mn} . S^{mn} = S_{mn}.S_{pq} g^{mp} g^{nq}
def cross(u, v):
    return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
S = [[None]*4 for _ in range(4)]
for A in range(4):
    for Bb in range(4):
        uA = [dn[i][A] for i in range(3)]
        uB = [dn[i][Bb] for i in range(3)]
        S[A][Bb] = cross(uA, uB)  # 3-vector

S2 = 0
for A in range(4):
    for Bb in range(4):
        for P in range(4):
            for Q in range(4):
                dotS = sum(S[A][Bb][i]*S[P][Q][i] for i in range(3))
                S2 += ginv[A, P]*ginv[Bb, Q]*dotS
S2 = sp.simplify(S2)
L4 = -sp.Rational(1, 4)*kap*S2
L4 = sp.simplify(L4)

Ltot = L2 + L4

# Hilbert stress: T_{mn} = -(2/sqrt-g) d(sqrt-g L)/dg^{mn} = -2 dL/dg^{mn} + g_{mn} L
# We need L as a function of independent g^{mn}. Easier: T_{mn} = -2 dL/dg^{mn} + g_{mn} L,
# treating each metric appearance. Build L in terms of symbolic inverse-metric entries.
# Use the standard variational result by differentiating L w.r.t. g^{AB} with g_{AB}=metric.
# Construct L symbolically with placeholder inverse metric components.
gi = sp.MatrixSymbol('gi', 4, 4)
giM = sp.Matrix(gi)
# rebuild L2, S2 with giM (symmetric) -- enforce symmetry by using giM but only diagonal here.
# Simpler robust route: since metric is diagonal, use diagonal inverse symbols.
gtt, grr, gthth, gphph = sp.symbols('gtt grr gthth gphph')
gidiag = sp.diag(gtt, grr, gthth, gphph)

L2s = -sp.Rational(1, 2)*xi*sum(gidiag[A, A]*Gmat[A, A] for A in range(4))
S2s = 0
for A in range(4):
    for Bb in range(4):
        dotS = sum(S[A][Bb][i]*S[A][Bb][i] for i in range(3))
        S2s += gidiag[A, A]*gidiag[Bb, Bb]*dotS
L4s = -sp.Rational(1, 4)*kap*S2s
Ls = sp.simplify(L2s + L4s)

# metric (lower) diagonal values to substitute after differentiation
glow = {gtt: -sp.exp(2*a), grr: sp.exp(2*b), gthth: r**2, gphph: r**2*sp.sin(th)**2}
gilow = {gtt: -sp.exp(-2*a), grr: sp.exp(-2*b), gthth: 1/r**2, gphph: 1/(r**2*sp.sin(th)**2)}
glow_mat = sp.diag(*[glow[s] for s in (gtt, grr, gthth, gphph)])

# T_{AA} = -2 dL/dg^{AA} + g_{AA} L   (diagonal). Mixed T^A_A = g^{AA} T_{AA}.
syms = [gtt, grr, gthth, gphph]
T_mixed = {}
for i, s in enumerate(syms):
    dLdg = sp.diff(Ls, s)
    T_low = -2*dLdg + glow_mat[i, i]*Ls
    T_low = T_low.subs(gilow)  # substitute inverse-metric values
    T_low = sp.simplify(T_low)
    Tmixed = sp.simplify(gilow[s]*T_low)
    T_mixed[s] = sp.simplify(Tmixed)

# Now express in X, Y form. X = e^{-2b} Th'^2, Y = sin^2 Th / r^2.
Thp = sp.diff(Th, r)
X = sp.exp(-2*b)*Thp**2
Y = sp.sin(Th)**2/r**2

Ttt = T_mixed[gtt]   # = T^t_t = -rho
Trr = T_mixed[grr]   # = T^r_r =  p_r
Tthth = T_mixed[gthth]

rho_claim = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
pr_claim = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)
pT_claim = (kap/2)*Y**2 - (xi/2)*X

print("=== CLAIM 1: Hilbert stress, independently derived ===")
d_rho = sp.simplify(Ttt + rho_claim)   # T^t_t = -rho  => T^t_t + rho = 0
d_pr = sp.simplify(Trr - pr_claim)
d_pT = sp.simplify(Tthth - pT_claim)
print("T^t_t + rho_claim  (should be 0):", d_rho)
print("T^r_r - pr_claim   (should be 0):", d_pr)
print("T^th_th - pT_claim (should be 0):", d_pT)

# p_r + rho identity
pr_plus_rho = sp.simplify(pr_claim + rho_claim - X*(xi + 2*kap*Y))
print("\n(p_r+rho) - X(xi+2 kap Y)  (should be 0):", pr_plus_rho)
print("X(xi+2 kap Y) >= 0 since xi,kap>0, X=e^{-2b}Th'^2>=0, Y=sin^2/r^2>=0 : structurally nonneg")

# also print derived T^t_t in raw form
print("\nDerived T^t_t =", sp.simplify(Ttt))
print("Derived T^r_r =", sp.simplify(Trr))
print("Derived T^th_th =", sp.simplify(Tthth))
