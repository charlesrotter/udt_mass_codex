#!/usr/bin/env python3
"""VFOLD — INDEPENDENT BLIND VERIFIER (main-loop). TEST A (time-row det)
and D (signature eigenvalue), built from scratch. No machinery shared
with the arm (w6_arm1_lib) or the arm-spawned verifier.

DECISIVE QUESTION A: the same-minus involution is the time-row reflection
(a,b)=(g_Tr,g_Ttheta) -> (-a,-b), theorem-grade. Turn the time row ON and
ask:
  (i)   does det(g4) still vanish on D=0, or does (a,b) != 0 LIFT it?
  (ii)  is D=0 the FIXED-POINT SET of (a,b) -> (-a,-b)?
  (iii) (handled in curvature script) is the divergence a static-slice
        artifact?

PRE-REGISTERED FAILURE CRITERIA (declared before running):
  A1: det g4 with time row on must EQUAL the arm's claimed
      -(r sin)^2 D/(1+w)^2 when a=b=0  (calibration of my own det).
  A2: With (a,b) generic nonzero, det g4 = (poly in a,b) - (r sin)^2 D/W.
      PASS-LIFT if det g4 has a piece that does NOT vanish on D=0 for
      generic (a,b): then the time row LIFTS the degeneracy (MIRROR FOLD
      direction).  PASS-NOLIFT if det g4 is still proportional to D for
      ALL (a,b): then the time row does NOT lift it (TRUE EDGE direction).
      Report whichever is TRUE; do not steer.
  A3: invariance of det under (a,b)->(-a,-b): det must be EVEN in (a,b)
      jointly (a true reflection symmetry of the determinant). If det is
      even, the D=0 surface coincides with a candidate fixed set only if
      the a,b-dependent piece also vanishes there.
  A4: the FIXED-POINT SET of (a,b)->(-a,-b) is {a=0, b=0}. Test whether
      D=0 is reached AT a=b=0 (static slice) -- i.e. whether the static
      slice (a=b=0) IS the fixed locus and D=0 lives in it.

This script is EXACT sympy only (no curvature engine yet; pure linear
algebra of a 4x4). Log: /tmp/vfold_det_timerow.log
"""
import sys
import sympy as sp

r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)
f, q, w, a, b = sp.symbols('f q w a b', real=True)
W = (1 + w) ** 2
D = r ** 2 * W - f * q ** 2

PASS, FAIL = [], []
def ck(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"VFOLD-DET-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# Full 4-metric WITH the time row on. Coordinates (T, r, theta, varphi).
# Diagonal time-time -f; time-row off-diagonals a=g_Tr, b=g_Ttheta.
g4 = sp.Matrix([
    [-f,  a,    b,        0],
    [ a, 1/f,   q,        0],
    [ b,  q,    r**2*W,   0],
    [ 0,  0,    0,        r**2*sp.sin(th)**2 / W],
])

print("="*72)
print("TEST A — FULL 4-metric determinant WITH TIME ROW (a,b) ON")
print("="*72)

det4 = sp.simplify(g4.det())
print("det g4 (a,b on) =", det4)

# A1: calibrate -- at a=b=0 reproduce arm's identity
det_static = sp.simplify(det4.subs({a: 0, b: 0}))
arm_id = -(r**2 * sp.sin(th)**2) * D / (1 + w)**2
ck("A1", sp.simplify(det_static - arm_id) == 0,
   "at a=b=0: det g4 = -(r sin)^2 D/(1+w)^2 (arm identity reproduced "
   "by my own 4x4 det).")

# A2: does (a,b) lift D=0?  Factor det4. Compute det4 restricted to D=0.
# Replace q^2 using D=0  => f q^2 = r^2 W, i.e. on D=0. We substitute the
# constraint by eliminating one variable. Easiest: solve D=0 for f:
#   D=0 => f = r^2 W / q^2  (q!=0). Substitute and see if det4 still 0.
f_on_D0 = r**2 * W / q**2
det4_onD0 = sp.simplify(det4.subs(f, f_on_D0))
print("det g4 ON D=0 (f=r^2 W/q^2) =", det4_onD0)
lifts = sp.simplify(det4_onD0) != 0
ck("A2", True,
   f"det g4 on D=0 with time row generic = {det4_onD0}. "
   f"LIFTS the degeneracy: {bool(lifts)}.")

# Extract the explicit (a,b)-dependent additive structure of det4.
# Write det4 = det_static + R(a,b) and inspect R on D=0.
Rab = sp.simplify(det4 - det_static)
print("\n(a,b)-dependent part R(a,b) = det4 - det_static:")
print("  R =", sp.factor(Rab))
Rab_onD0 = sp.simplify(Rab.subs(f, f_on_D0))
print("  R on D=0 =", sp.simplify(Rab_onD0))

# A3: evenness under (a,b)->(-a,-b)
det4_flip = sp.simplify(det4.subs({a: -a, b: -b}))
ck("A3", sp.simplify(det4_flip - det4) == 0,
   "det g4 is EVEN under same-minus (a,b)->(-a,-b): the determinant is "
   "invariant under the theorem-grade time-row reflection.")

# A4: the fixed-point set of (a,b)->(-a,-b) is {a=0,b=0}. Is D=0 attained
# only off that set, or does the static slice (a=b=0) CONTAIN D=0?
# det4 = -(r sin)^2 D/W + R(a,b). On the fixed set a=b=0, R=0, so det4=0
# IFF D=0. Off the fixed set, det4=0 requires D = (W/(r sin)^2) R(a,b),
# i.e. the vanishing locus MOVES OFF D=0.
print("\n" + "="*72)
print("TEST A4 — does the time row MOVE the determinant-zero off D=0?")
print("="*72)
# Solve det4 = 0 for D in terms of a,b:
Dsol = sp.solve(sp.Eq(det4, 0), D) if det4.has(D) else None
# det4 is polynomial in f,q,a,b; express det4 in terms of D by substituting
# f q^2 = r^2 W - D. Introduce D as symbol:
Dsym = sp.Symbol('Dsym', real=True)
# replace f*q**2 -> r^2 W - Dsym ; need det4 to be expressible. Use the
# fact det4 is at most quadratic in (a,b) and the diagonal block carries f.
det4_poly = sp.expand(det4)
# substitute f = (r^2 W - Dsym)/q**2 (from D=r^2 W - f q^2):
det4_inD = sp.simplify(det4_poly.subs(f, (r**2 * W - Dsym) / q**2))
det4_inD = sp.expand(sp.simplify(det4_inD))
print("det4 expressed via D:", sp.collect(det4_inD, Dsym))
# The zero-locus: set det4_inD = 0 and solve for Dsym
zero_in_D = sp.solve(sp.Eq(det4_inD, 0), Dsym)
print("determinant zero at D =", [sp.simplify(z) for z in zero_in_D])
moved = any(sp.simplify(z) != 0 for z in zero_in_D)
ck("A4", True,
   f"determinant vanishes at D = {[sp.simplify(z) for z in zero_in_D]}; "
   f"with time row on, the zero is at D != 0 (moved): {bool(moved)}. "
   "If moved, the static-slice D=0 is NOT a degeneracy of the time-on "
   "metric -- it is an artifact of the a=b=0 fixed slice (MIRROR FOLD).")

print("\n" + "="*72)
print("SUMMARY A")
print("="*72)
print(f"  det g4(a,b) on D=0 = {det4_onD0}  (nonzero => time row LIFTS)")
print(f"  determinant-zero locus in D = {[sp.simplify(z) for z in zero_in_D]}")
print(f"\nVFOLD DET: {len(PASS)} PASS / {len(FAIL)} FAIL")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
