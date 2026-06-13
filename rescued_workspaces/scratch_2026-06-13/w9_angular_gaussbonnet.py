#!/usr/bin/env python3
"""W9 PHASE 2 — script 2: THE ANGULAR 2-SPHERE AS A CLOSED SURFACE.
GEOMETRIC, NO ACTION.  The direct generalisation of the H1 area-form
template: the H1 discreteness came from a GLOBAL condition on the
angular structure (the exterior cube = the area form), not a local
regularity.  Here we ask the analogous GLOBAL question with the
angular sector treated as a co-equal geometric unknown.

THE OBJECT.  At fixed (t, r) the metric induces a 2-metric on the
angular block (the (theta, phi) surface):

   dsigma^2 = g_thth dtheta^2 + g_phiphi dphi^2
            = r^2 (1+w)^2 dtheta^2 + r^2 sin^2(theta)/(1+w)^2 dphi^2 .

(The off-diagonal q lives in the (r,theta) block, not here; the pure
angular surface is orthogonal in (theta,phi) on the static class.)
Factor out the area-radius r^2: the SHAPE of the angular surface is
governed by  w = w(theta)  alone (r is a scale).  Write A=(1+w).

This is a surface of revolution with metric
   dsigma^2 = r^2 [ A^2 dtheta^2 + (sin^2 theta / A^2) dphi^2 ].

GEOMETRIC CLOSURE CONDITIONS (the metric's own, no action):
 (R1) smooth CLOSED surface: regular at both poles theta=0,pi
      (elementary flatness -> A(0)=A(pi)=1, from script 1);
 (R2) GAUSS-BONNET: Int K dArea = 2 pi chi.  For ANY smooth metric on
      a topological 2-sphere, chi=2, so Int K dA = 4 pi IDENTICALLY --
      a TOPOLOGICAL invariant independent of w.  This is the analog of
      "Lambda^3 H1 = the area form": the total curvature is quantised
      (=4pi) by topology.
 The question: does demanding the surface CLOSE SMOOTHLY (a genuine
 embedded/abstract S^2 with no defect) plus the dilation/curvature
 regularity FORCE w(theta) into a DISCRETE family, or leave a continuum?

PRE-STATED CRITERION (frozen):
 * DISCRETE  <=>  closure admits only an integer-indexed family of
   w(theta) profiles (e.g. a quantised number of "lobes"/period, or
   w forced to a discrete set of closed shapes), the way N=3 was forced.
 * CONTINUUM <=>  every smooth w(theta) with w(0)=w(pi)=0 and 1+w>0
   gives a legal closed surface (Gauss-Bonnet auto-satisfied, no
   integer selected) -- closure is a constraint, not a counter.

We compute K(theta) for general A(theta), verify Gauss-Bonnet (the
topological 4pi), and decide.  Exact sympy.
"""
import sys
import sympy as sp

th = sp.Symbol('theta', real=True)
r = sp.Symbol('r', positive=True)

log = []
def out(*a):
    s = ' '.join(str(x) for x in a)
    log.append(s); print(s, flush=True)

out("=" * 70)
out("W9 script 2 : the ANGULAR surface as a closed 2-sphere (geometric)")
out("=" * 70)

A = sp.Function('A')(th)        # A = 1 + w(theta);  axis: A(0)=A(pi)=1
E = r ** 2 * A ** 2                       # g_thth
G = r ** 2 * sp.sin(th) ** 2 / A ** 2     # g_phiphi
out("\nangular 2-metric (surface of revolution):")
out("  E = g_thth   =", E)
out("  G = g_phiphi =", G)

# Gaussian curvature of an orthogonal metric ds^2 = E dth^2 + G dph^2:
#   K = -1/(2 sqrt(EG)) [ d_th( G_th/sqrt(EG) ) + d_ph( E_ph/sqrt(EG) ) ]
# (E,G depend only on theta; phi-term drops).
sqEG = sp.sqrt(E * G)
Gth = sp.diff(G, th)
term = Gth / sqEG
K = sp.simplify(-1 / (2 * sqEG) * sp.diff(term, th))
out("\nGaussian curvature K(theta) =")
out("   ", sp.simplify(K))

# sanity: round sphere A=1 -> K = 1/r^2
K_round = sp.simplify(K.subs({A: sp.Integer(1), sp.Derivative(A, th): 0,
                              sp.Derivative(A, (th, 2)): 0}))
out("\n  check: round sphere (A=1) -> K =", K_round, " (expect 1/r^2)")
assert sp.simplify(K_round - 1 / r ** 2) == 0, K_round

# Gauss-Bonnet area element dA = sqrt(EG) dtheta dphi
dA_over_dphi = sqEG    # integrate phi -> 2pi
out("\narea element sqrt(EG) =", sp.simplify(sqEG),
    "  (= r^2 |sin theta| ; the A's CANCEL -> area is w-blind!)")

# ---- The decisive structural fact: sqrt(EG) = r^2 sin(theta) -------
# Because g_thth * g_phiphi = r^2 A^2 * r^2 sin^2/A^2 = r^4 sin^2, the
# A's CANCEL.  The area form of the angular surface is EXACTLY the
# round area form r^2 sin(theta) dtheta dphi for ANY w(theta).
sqEG_simpl = sp.simplify(sqEG)
assert sp.simplify(sqEG_simpl - r ** 2 * sp.Abs(sp.sin(th))) == 0, sqEG_simpl
out("\n*** KEY GEOMETRIC FACT: det of the angular block is w-INDEPENDENT.")
out("    sqrt(g_thth g_phiphi) = r^2 sin(theta)  for ALL w.")
out("    -> total angular AREA = 4 pi r^2  for every w(theta).")
out("    This is the SAME area-blindness as sqrt(-g)=r^2 sin(theta)")
out("    (negative_phi line 78): the conformal angular factor w is a")
out("    pure SHEAR between dtheta and dphi that preserves area.")

# ---- Gauss-Bonnet: integrate K over the surface --------------------
# Int K dA = Int_0^pi K * sqrt(EG) dtheta * (2pi).  This must = 4pi for
# any smooth A with A(0)=A(pi)=1 (topological S^2).  Verify with a
# concrete smooth profile to confirm the topological invariance.
out("\nGauss-Bonnet test Int K dA = 4 pi  (topological; w-independent):")
integrand = sp.simplify(K * sqEG)
out("  K * sqrt(EG) =", integrand)

# test profile: A = 1 + e*sin^2(theta) (smooth, A(0)=A(pi)=1, 1+w>0 for
# e>-1).  Compute Int_0^pi (K sqEG) dtheta * 2pi for a symbolic e.
eps = sp.Symbol('epsilon', real=True)
Atest = 1 + eps * sp.sin(th) ** 2
subs_map = {A: Atest,
            sp.Derivative(A, th): sp.diff(Atest, th),
            sp.Derivative(A, (th, 2)): sp.diff(Atest, th, 2)}
integ_test = sp.simplify(integrand.subs(subs_map))
out("\n  test profile A = 1 + eps*sin^2(theta):")
out("    K*sqrt(EG) =", integ_test)
GB = sp.integrate(integ_test, (th, 0, sp.pi))
GB = sp.simplify(GB)
out("    Int_0^pi (K sqrt(EG)) dtheta =", GB)
total = sp.simplify(2 * sp.pi * GB)
out("    Int K dA = 2pi * above =", total, "  (expect 4 pi for all eps)")
assert sp.simplify(total - 4 * sp.pi) == 0, total
out("    -> CONFIRMED 4 pi for ALL eps : Gauss-Bonnet is satisfied")
out("       automatically; the integer chi=2 is NOT a selector of w.")

# second, qualitatively different profile to be safe: A=1+eps*sin^4
Atest2 = 1 + eps * sp.sin(th) ** 4
subs2 = {A: Atest2, sp.Derivative(A, th): sp.diff(Atest2, th),
         sp.Derivative(A, (th, 2)): sp.diff(Atest2, th, 2)}
GB2 = sp.simplify(2 * sp.pi * sp.integrate(sp.simplify(integrand.subs(subs2)),
                                           (th, 0, sp.pi)))
out("\n  second profile A=1+eps*sin^4(theta): Int K dA =", GB2)
assert sp.simplify(GB2 - 4 * sp.pi) == 0, GB2

out("\n--- VERDICT (angular Gauss-Bonnet / closure) ----------------------")
out("The angular block is an AREA-PRESERVING (w-blind determinant) shear")
out("of the round sphere.  Closing it smoothly as an S^2 (poles regular,")
out("Gauss-Bonnet) imposes chi=2 -> Int K dA = 4 pi for EVERY admissible")
out("w(theta) -- a topological identity, NOT a counter that selects w.")
out("By the pre-stated criterion: CONTINUUM.  The integer here (chi=2)")
out("is fixed by topology and does NOT discretise the angular shape, in")
out("sharp contrast to the H1 area-form where the integer (N=3) was the")
out("DIMENSION of the carrier space, selected by uniqueness of Lambda^3,")
out("not by the value of an area integral.")
out("\nGEOMETRIC REASON this differs from H1: H1's discreteness was a")
out("LINEAR-ALGEBRAIC dimension count on the harmonic CARRIER (which ell,")
out("hence which N), forced by 'unique antisymmetric triple' + finite-")
out("action endpoint admissibility.  The metric's angular SHAPE w(theta)")
out("is a continuous conformal/shear deformation that closure does not")
out("quantise.  Discreteness, if native, sits in WHICH HARMONIC SECTOR")
out("the shape belongs to (the ell-count, H1), not in the shape's")
out("amplitude/profile -- which is exactly what the H1 result already")
out("says, and is consistent with CATALOG_FRAME (q=1/3,N=3 are the")
out("angular numbers; the shape amplitude is a continuous cell parameter).")

with open('/tmp/w9_angular_gaussbonnet.log', 'w') as fh:
    fh.write('\n'.join(log) + '\n')
out("\n[done] log -> /tmp/w9_angular_gaussbonnet.log")
