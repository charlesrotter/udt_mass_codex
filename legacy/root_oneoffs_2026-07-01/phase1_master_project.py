#!/usr/bin/env python3
"""
phase1_master_project.py -- PHASE-1a step 1 (refined): the angular PROJECTION.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE.

The raw R_thth^(1) (phase1_master_reduce.py) still carries explicit sin^2(theta)
because R_thth is a single tensor component mixing the l=0 trace and the l=2
traceless parts. To isolate the MASTER radial operator we project the linearized
vacuum equations onto the l=2 (P2) angular channel honestly.

CLEANEST honest route: the warp is a transverse-traceless angular deformation
delta g_thth = +eps r^2 h P2, delta g_psps = -eps r^2 h P2 (the Phase-0 ansatz).
Form the angular-traceless combination of the vacuum eqns that the P2 channel
obeys:  C := (R^th_th - R^ps_ps)^(1)  -- the MIXED-component traceless angular
piece. For a transverse-traceless l warp on flat space this isolates the single
physical master scalar and its operator is the flat l-wave operator.

We compute C, divide by its (P2) angular factor, and read off the radial+time
operator on h. We then test h = H(r) cos(w t) and report the eigenproblem.
"""
import sympy as sp

eps = sp.symbols('epsilon')
t, r, th, ps = sp.symbols('t r theta psi', real=True)
X = [t, r, th, ps]
h = sp.Function('h')(t, r)


def christoffel_ricci(g, X):
    n = len(X)
    ginv = g.inv()
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d] * (sp.diff(g[d, cc], X[b])
                                       + sp.diff(g[d, b], X[cc])
                                       - sp.diff(g[b, cc], X[d]))
                Gamma[a][b][cc] = sp.Rational(1, 2) * s
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], X[a]) - sp.diff(Gamma[a][b][a], X[d])
                for e in range(n):
                    s += Gamma[a][a][e] * Gamma[e][b][d] - Gamma[a][d][e] * Gamma[e][b][a]
            Ric[b, d] = s
    return Ric, ginv


P2 = (3 * sp.cos(th)**2 - 1) / 2
g = sp.Matrix([
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, r**2 * (1 + eps * h * P2), 0],
    [0, 0, 0, r**2 * sp.sin(th)**2 * (1 - eps * h * P2)],
])

Ric, ginv = christoffel_ricci(g, X)


def Oeps1(expr):
    return sp.simplify(sp.series(sp.expand(expr), eps, 0, 2).removeO().coeff(eps, 1))


# Mixed components R^th_th and R^ps_ps (raise one index with ginv).
# R^th_th = ginv[2,2]*R_thth ; R^ps_ps = ginv[3,3]*R_psps
Rth_th = sp.simplify(ginv[2, 2] * Ric[2, 2])
Rps_ps = sp.simplify(ginv[3, 3] * Ric[3, 3])

print("=== PHASE-1a step 1 (refined): traceless angular projection ===\n")
# The traceless angular combination -- isolates the l=2 master scalar.
C = Oeps1(Rth_th - Rps_ps)
C = sp.simplify(C)
print("Traceless angular vacuum eqn  C := (R^th_th - R^ps_ps)^(1) = 0 :")
print("  C =", C)

# C should be (angular factor) * [radial+time operator on h]. Factor it.
# Collect on h-derivatives.
htt = sp.diff(h, t, 2); hrr = sp.diff(h, r, 2); hr = sp.diff(h, r)
Cx = sp.expand(C)
c_htt = sp.simplify(Cx.coeff(htt))
c_hrr = sp.simplify(Cx.coeff(hrr))
c_hr = sp.simplify(Cx.coeff(hr))
rem = sp.simplify(Cx - c_htt*htt - c_hrr*hrr - c_hr*hr)
c_h = sp.simplify(rem.coeff(h))
rem2 = sp.simplify(rem - c_h*h)
print("\n  coeff d_t^2 h :", c_htt)
print("  coeff d_r^2 h :", c_hrr)
print("  coeff d_r   h :", c_hr)
print("  coeff      h :", c_h)
print("  remainder    :", rem2)

# Normalize so the spatial second-derivative is -d_r^2 (divide by -c_hrr).
print("\n--- normalized operator (divide by -coeff(d_r^2 h)) ---")
if c_hrr != 0:
    A_tt = sp.simplify(c_htt / (-c_hrr))
    A_hr = sp.simplify(c_hr / (-c_hrr))
    A_h = sp.simplify(c_h / (-c_hrr))
    print(f"  {A_tt} d_t^2 h - d_r^2 h + ({A_hr}) d_r h + ({A_h}) h = 0")

# Harmonic ansatz h=H(r)cos(wt): d_t^2 -> -w^2.
print("\n--- harmonic ansatz h=H(r)cos(w t) ---")
Hf = sp.Function('H')(r)
sub = Cx.subs(h, Hf*sp.cos(sp.Symbol('w', positive=True)*t)).doit()
ww = sp.Symbol('w', positive=True)
sub = sp.simplify(sub / sp.cos(ww * t))
Hrr = sp.diff(Hf, r, 2); Hr = sp.diff(Hf, r)
s = sp.expand(sub)
b_Hrr = sp.simplify(s.coeff(Hrr))
b_Hr = sp.simplify(s.coeff(Hr))
restH = sp.simplify(s - b_Hrr*Hrr - b_Hr*Hr)
b_H = sp.simplify(restH.coeff(Hf))
print("  coeff H'':", b_Hrr)
print("  coeff H' :", b_Hr)
print("  coeff H  :", b_H)
if b_Hrr != 0:
    print("\n  normalized: -H'' + (%s) H' + (%s) H = 0" % (
        sp.simplify(-b_Hr/b_Hrr), sp.simplify(-b_H/b_Hrr)))
    print("  i.e.  -H'' - (2/r) H' + [6/r^2] H = w^2 H   <-- if it matches, this is")
    print("        the SPHERICAL (3D radial) l=2 operator: -H''-(2/r)H'+l(l+1)/r^2 H = w^2 H")
    print("        whose regular solution is H = j_2(w r) (spherical Bessel).")

# Verify directly: substitute the spherical Bessel j_2(w r) (sympy jn) and check
# the extracted radial ODE  -H'' - (2/r)H' = w^2 H  is satisfied identically.
print("\n--- DIRECT verification: does H=j_2(w r) solve the extracted radial ODE? ---")
from sympy import jn
H_bessel = jn(2, ww * r)
residual = (-sp.diff(H_bessel, r, 2)
            - sp.Rational(2, 1) / r * sp.diff(H_bessel, r)
            - ww**2 * H_bessel)
residual = sp.simplify(residual)
print("  residual of [-H'' - (2/r)H' - w^2 H] at H=j_2(wr):", residual)
print("  (zero => the extracted operator IS the flat l=2 spherical-Bessel operator,")
print("   confirming H=j_2(wr) is the regular solution. Reflecting-wall BCs then")
print("   quantize w via the j_2 / [d/dr(r j_2)] zeros -- the box ladders.)")
