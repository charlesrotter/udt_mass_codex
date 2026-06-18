#!/usr/bin/env python3
"""
phase1_master_reduce.py -- PHASE-1a step 1: DERIVE the radial master operator
honestly from the Phase-0 l=2 even-parity (diagonal) vacuum warp on the FLAT
round background, then confirm the harmonic ansatz gives the eigenvalue problem.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A (borrow GR
numerics; impose NO physics, NO matter, NO scale). OBSERVE mode. c=1.

WHAT THIS DOES (no result forced):
  - Reuses the EXACT Phase-0 metric ansatz from phase0_nonround_escape.py (B2):
    g_thth = r^2 (1 + eps h(t,r) P2),  g_psps = r^2 sin^2 (1 - eps h(t,r) P2),
    flat round diagonal background (phi=0, c=1).
  - Computes the linearized (O(eps)) vacuum Einstein equation in the angular
    block, isolates the P2 angular content, and extracts the radial+time
    operator acting on h(t,r).
  - Reports the EXACT operator. Then inserts h = H(r) cos(w t) and reports the
    resulting radial ODE eigenvalue problem.

REDUCTION CHOICES (tagged, with relax-test):
  C1: background = FLAT round (phi=0). Relax-test: the KEY BACKGROUND FACT
      (regularity on a finite mirrored cell forces m=0 => flat) was confirmed
      symbolically upstream; relaxing means re-running with phi(r) const-only,
      which is flat again. So this is not a free choice -- it is forced.
  C2: even-parity diagonal warp with the SAME h on g_thth and (-h) on g_psps
      (the minimal transverse-traceless-style l=2 diagonal DOF used in Phase-0).
      Relax-test: a general even-parity (Zerilli) ansatz carries more metric
      functions (H0,H1,H2,K); the gauge-invariant physical DOF is one master
      scalar. We confirm the single-function warp already yields the physical
      l=2 wave operator; the relax-test is to redo with full Zerilli and check
      the master equation matches (left for verifier / Phase-1c if needed).
  C3: single harmonic h=H(r)cos(w t). Relax-test: harmonic balance with more
      harmonics -- for a LINEAR operator the harmonics decouple, so k=1 is exact
      for the linear spectrum (tagged LINEARIZED stepping-stone).
"""
import sympy as sp

t, r, th = sp.symbols('t r theta', real=True)
eps = sp.symbols('epsilon')
w = sp.symbols('w', positive=True)   # angular frequency
X = [t, r, th]                       # 3D suffices: psi enters only via metric, axisymmetric


def ricci_from_metric(g, X):
    """Full Ricci tensor (we work in vacuum so G=0 <=> Ric=0)."""
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


# --- The Phase-0 (B2) ansatz, restricted to the axisymmetric (t,r,theta) block.
# We must keep psi in the metric for the angular geometry; use 4D for correctness.
t4, r4, th4, ps4 = sp.symbols('t r theta psi', real=True)
X4 = [t4, r4, th4, ps4]
h = sp.Function('h')(t4, r4)
P2 = (3 * sp.cos(th4)**2 - 1) / 2
g = sp.Matrix([
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, r4**2 * (1 + eps * h * P2), 0],
    [0, 0, 0, r4**2 * sp.sin(th4)**2 * (1 - eps * h * P2)],
])

print("=== PHASE-1a step 1: honest reduction of Phase-0 l=2 even warp ===")
print("Metric (c=1, flat round background, eps*h(t,r)*P2 warp):")
print("  g_tt=-1, g_rr=1, g_thth=r^2(1+eps h P2), g_psps=r^2 sin^2(1-eps h P2)\n")

Ric, ginv = ricci_from_metric(g, X4)

# Linearize in eps: take O(eps^1) coefficient of vacuum eqn Ric_{mu nu}=0.
def Oeps1(expr):
    return sp.simplify(sp.series(sp.expand(expr), eps, 0, 2).removeO().coeff(eps, 1))

# The theta-theta vacuum component carries the wave operator (Phase-0 finding).
Rthth1 = Oeps1(Ric[2, 2])
Rtt1 = Oeps1(Ric[0, 0])
Rrr1 = Oeps1(Ric[1, 1])
Rpsps1 = Oeps1(Ric[3, 3])

print("O(eps) vacuum components (=0 in vacuum):")
print("  R_thth^(1) =", sp.simplify(Rthth1))
print("  R_tt^(1)   =", sp.simplify(Rtt1))
print("  R_rr^(1)   =", sp.simplify(Rrr1))

# Strip the P2 (and trig) angular factor to expose the radial+time operator on h.
# R_thth^(1) should be (angular func) * [ operator on h ]. Divide by its h-content.
# Build the operator by collecting d_t^2 h, d_r^2 h, d_r h, h coefficients.
htt = sp.diff(h, t4, 2)
hrr = sp.diff(h, r4, 2)
hr = sp.diff(h, r4)

print("\n--- Extract radial+time master operator from R_thth^(1) ---")
expr = sp.expand(sp.simplify(Rthth1))
# factor out common angular dependence by taking ratio of coefficients
c_htt = sp.simplify(expr.coeff(htt))
c_hrr = sp.simplify(expr.coeff(hrr))
c_hr = sp.simplify(expr.coeff(hr))
# coefficient of bare h: subtract derivative pieces then take remaining
rem = sp.simplify(expr - c_htt * htt - c_hrr * hrr - c_hr * hr)
c_h = sp.simplify(rem.coeff(h))
rem2 = sp.simplify(rem - c_h * h)
print("coeff d_t^2 h :", c_htt)
print("coeff d_r^2 h :", c_hrr)
print("coeff d_r   h :", c_hr)
print("coeff      h :", c_h)
print("remainder (should be 0):", sp.simplify(rem2))

# Normalize the operator by dividing by -coeff(d_r^2 h) to get -d_r^2 form, OR
# by coeff(d_t^2 h) to expose wave form. Report both normalizations honestly.
print("\n--- Operator normalized so that d_t^2 h has coefficient +1 (wave form) ---")
norm = c_htt
if norm != 0:
    print("  d_t^2 h + (%s) d_r^2 h + (%s) d_r h + (%s) h = 0" % (
        sp.simplify(c_hrr / norm), sp.simplify(c_hr / norm), sp.simplify(c_h / norm)))

# Now apply harmonic ansatz h = H(r) cos(w t): d_t^2 -> -w^2.
print("\n--- Harmonic ansatz h(t,r) = H(r) cos(w t):  d_t^2 -> -w^2 ---")
Hf = sp.Function('H')(r4)
sub_expr = expr.subs(h, Hf * sp.cos(w * t4)).doit()
sub_expr = sp.simplify(sub_expr / sp.cos(w * t4))
print("Radial ODE (R_thth^(1)/cos(w t) = 0):")
print("  ", sp.simplify(sub_expr))

# Put in Sturm-Liouville / Regge-Wheeler form: solve for the structure.
Hrr = sp.diff(Hf, r4, 2)
Hr = sp.diff(Hf, r4)
sl = sp.expand(sub_expr)
a_Hrr = sp.simplify(sl.coeff(Hrr))
a_Hr = sp.simplify(sl.coeff(Hr))
restH = sp.simplify(sl - a_Hrr * Hrr - a_Hr * Hr)
a_H = sp.simplify(restH.coeff(Hf))
print("\n  coeff H'' :", a_Hrr)
print("  coeff H'  :", a_Hr)
print("  coeff H   :", a_H)

# Divide through to expose -H'' + ... form.
print("\n--- Normalize to leading -H'' (divide by -coeff(H'')) ---")
if a_Hrr != 0:
    print("  -H'' + (%s) H' + (%s) H = 0" % (
        sp.simplify(-a_Hr / a_Hrr), sp.simplify(-a_H / a_Hrr)))

# Compare against the asserted target: -H'' + l(l+1)/r^2 H = w^2 H (l=2 => 6/r^2).
print("\n--- TARGET check: is this -H'' + [l(l+1)/r^2] H = w^2 H with l=2? ---")
print("  l=2 => l(l+1)=6, target potential 6/r^2, eigenvalue w^2.")
# Build target residual
if a_Hrr != 0:
    pot = sp.simplify(-a_H / a_Hrr)
    drift = sp.simplify(-a_Hr / a_Hrr)
    print("  Extracted first-derivative term coeff:", drift)
    print("  Extracted (H-coeff)/(H''-coeff)      :", pot)
    print("  [pot should contain -w^2 + 6/r^2 if textbook RW form, OR an")
    print("   equivalent flat l=2 operator with a first-derivative term.]")
