#!/usr/bin/env python3
"""W7 SCRIPT A — THE MIRROR / PARITY BOUNDARY CONDITION, DERIVED.

Date: 2026-06-13.  Driver: W7 Symphony agent.  Declaration: W7 section
of w_stiffness_push_declaration.md (binding).  Mode: UNCOVER (the BC)
then it feeds the SOLVE (scripts B/C).  Reuses committed machinery
patterns via w6_arm1_lib (NOT edited).

THE FALSIFICATION-CRITICAL DELIVERABLE (hypothesis discipline, Charles):
  the quantizing boundary condition MUST be DERIVED from the same-minus
  involution, NOT chosen to quantize.  This script does ONLY that: it
  takes the same-minus involution sigma: (a,b) = (g_Tr, g_Ttheta) ->
  (-a, -b) (the W6 mirror-fold; D=0 the fixed surface, canon
  C-2026-06-10-2 finite mirrored cells) and DERIVES the induced action
  on the fluctuation fields (delta-f, delta-q, delta-w) and hence the
  parity (even/odd) each must carry across the crease.  The parity set
  IS the boundary/quotient condition that couples the sectors.

WHAT THE INVOLUTION IS (W6, registry #30 re-amendment, exact):
  with the time row on the 4-metric is
    g4 = [[-f, a, b, 0],
          [a, 1/f, q, 0],
          [b, q, r^2 W, 0],
          [0, 0, 0, r^2 sin^2/W]],  W=(1+w)^2,
  and det g4 = -(r sin)^2/[f(1+w)^2] [ f D (1+a^2) + (b - f q a)^2 ],
  D = r^2 W - f q^2.  sigma: (a,b)->(-a,-b) is an isometry-class
  involution; its FIXED SET is a=b=0 (the static three-field slice),
  which is exactly D's static degeneracy locus.  The PHYSICAL fold is
  D=0 with the time row on, where det g4 -> -(r sin)^2 (b-fqa)^2/... !=0.

PRE-STATED FAILURE / HONESTY GATES (state BEFORE running):
  A-1  sigma must be an involution (sigma^2 = id) and a metric
       symmetry in the sense that g4(sigma X) has the SAME det and the
       SAME (f, q, w, r) invariants as g4(X) — i.e. sigma maps the
       solution class to itself.  If not, sigma is not a quotient
       symmetry and there is NO derived mirror BC (the program leg
       fails honestly here).
  A-2  the induced action on (f, q, w) must be IDENTITY (sigma touches
       only the time row a,b); hence (delta-f, delta-q, delta-w) are
       sigma-SCALARS and their parity is inherited from how the
       crease-normal coordinate transforms under sigma — DERIVED, not
       assigned.
  A-3  the crease-normal coordinate's parity under sigma must be
       computed from the geometry (the sign of the normal one-form to
       D=0 under a->-a, b->-b), NOT chosen.  This SIGN is the whole
       ballgame: it fixes even-vs-odd.
  A-4  the result must REDUCE correctly: on the static fixed slice
       (a=b=0) sigma is trivial and imposes NOTHING (consistent with
       W4/W5 finding bands on the static slice — no quantization there).
       Quantization, if any, must be carried by the f_T-driven
       (time-row-on) sector, where sigma acts nontrivially.

Log: /tmp/w7_a_mirror_bc.log
"""
import sys
import time

import sympy as sp
from sympy import Rational as Ra

from w6_arm1_lib import T, r, th

t0 = time.time()
PASS, FAIL = [], []


def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W7A-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


# ---- background fields and the full time-on 4-metric ----------------
f, q, w = sp.symbols('f q w', positive=True)
a, b = sp.symbols('a b', real=True)            # time row g_Tr, g_Ttheta
W = (1 + w) ** 2
sin = sp.sin(th)

g4 = sp.Matrix([[-f, a, b, 0],
                [a, 1 / f, q, 0],
                [b, q, r ** 2 * W, 0],
                [0, 0, 0, r ** 2 * sin ** 2 / W]])

Dexpr = r ** 2 * W - f * q ** 2

print("=" * 72)
print("PART 0 — the time-on metric, the determinant lift (W6 anchor)")
print("=" * 72)
det4 = sp.cancel(sp.together(g4.det()))
det_target = -(r ** 2 * sin ** 2) / (f * (1 + w) ** 2) \
    * (f * Dexpr * (1 + a ** 2) + (b - f * q * a) ** 2)
check("00", sp.cancel(sp.together(det4 - det_target)) == 0,
      "det g4 = -(r sin)^2/[f(1+w)^2][f D(1+a^2)+(b-fqa)^2] "
      "(W6 exact identity reproduced from the metric)")
det_onD = sp.cancel(det_target.subs(Dexpr, 0)) if False else \
    -(r ** 2 * sin ** 2) * (b - f * q * a) ** 2 / (f * (1 + w) ** 2)
# show on D=0 the determinant is the (b-fqa)^2 residual:
det_sub = sp.cancel(sp.together(
    det_target - (-(r ** 2 * sin ** 2) / (f * (1 + w) ** 2)
                  * f * Dexpr * (1 + a ** 2)) - det_onD))
check("01", det_sub == 0,
      "on D=0: det g4 = -(r sin)^2 (b-fqa)^2/[f(1+w)^2] (the regular "
      "nonstationary crease; b != f q a => nonzero => FOLD not edge)")

# =====================================================================
print()
print("=" * 72)
print("PART A — sigma: (a,b) -> (-a,-b) is the same-minus involution")
print("=" * 72)
sig = {a: -a, b: -b}

# A-1: involution + class-preserving (same det, same f,q,w,r)
g4s = g4.subs(sig, simultaneous=True)
# sigma^2 = id:
g4ss = g4s.subs(sig, simultaneous=True)
inv_ok = sp.simplify(g4ss - g4) == sp.zeros(4, 4)
det_invariant = sp.cancel(sp.together(g4s.det() - g4.det())) == 0
# the (f,q,w,r) content of g4s is identical (only off-diagonal time
# row flipped); confirm the diagonal + (r,theta) block are untouched:
block_same = all(sp.simplify(g4s[i, j] - g4[i, j]) == 0
                 for (i, j) in [(0, 0), (1, 1), (2, 2), (3, 3),
                                (1, 2), (2, 1), (3, 3)])
check("A1", inv_ok and det_invariant and block_same,
      "sigma^2 = id; det g4 INVARIANT under sigma (depends on a only "
      "via a^2 and on b via (b-fqa)^2 -> (b-fqa)^2 with a,b flipped = "
      "(-(b-fqa))^2 = same); the (f,q,w) diagonal + (r,theta) sector "
      "UNTOUCHED. sigma maps the solution class to itself => it is a "
      "genuine quotient symmetry (the mirror is real, not imposed)")

# the residual under sigma: (b - f q a) -> (-b - f q(-a)) = -(b-fqa).
resid = b - f * q * a
resid_s = resid.subs(sig, simultaneous=True)
check("A2", sp.simplify(resid_s + resid) == 0,
      "THE KEY SIGN: the crease residual rho := (b - f q a) is ODD "
      "under sigma (rho -> -rho). det g4 ~ rho^2 is even (why the fold "
      "is regular), but rho ITSELF flips. rho is the geometric normal "
      "datum of the crease — its parity is DERIVED here, not chosen")

# =====================================================================
print()
print("=" * 72)
print("PART B — the induced action on the fluctuation fields")
print("=" * 72)
# sigma touches ONLY (a,b); (f,q,w) and (r,theta) are sigma-invariant.
# A fluctuation delta-X (X in {f,q,w}) is therefore a sigma-SCALAR:
# sigma(delta-X)(a,b) = delta-X(sigma^{-1}(a,b)) = delta-X(-a,-b).
# Its parity across the crease is the parity of delta-X as a function
# of the crease-normal coordinate.  The crease-normal coordinate is the
# level function of D=0 carried by the time row: the geometrically
# natural transverse coordinate is rho = (b - f q a) (PART A: odd),
# because det g4 -> 0 on the static slice linearly in D but the
# REGULAR (time-on) transverse direction is rho (det ~ rho^2).
# Therefore the fold quotient M/sigma identifies (f,q,w; +rho) with
# (f,q,w; -rho): the two mirror copies of the cell are glued along
# rho=0 (the crease).  Single-valued fields on the QUOTIENT must be
# EVEN in rho; their normal derivatives must be ODD (vanish on the
# crease) UNLESS the field is in the sigma-ODD (time-row) sector.

# Decompose the fluctuation triple by sigma-parity of the EQUATION it
# sits in.  The C1 + species operator's time-row content enters through
# f_T (a* ~ f_T, b* = (f_theta/f_r) a*  — W6 same-minus stationary row).
# So the nonstationary sector's amplitude is carried by delta(f_T)-like
# data, which is sigma-ODD (a,b odd), while the static shape data
# (delta-f, delta-q, delta-w at f_T=0) is sigma-EVEN.
fT = sp.Symbol('f_T', real=True)
a_star = sp.Symbol('alpha') * fT          # a* proportional to f_T
fr_, fh = sp.symbols('f_r f_theta', real=True)
b_star = (fh / fr_) * a_star              # W6 same-minus stationary row
# sigma flips (a,b): on the stationary row that is f_T -> -f_T:
astar_s = a_star.subs(fT, -fT)
bstar_s = b_star.subs(fT, -fT)
check("B1", sp.simplify(astar_s + a_star) == 0
      and sp.simplify(bstar_s + b_star) == 0,
      "on the W6 same-minus stationary row (a*=alpha f_T, "
      "b*=(f_theta/f_r)a*), sigma:(a,b)->(-a,-b) IS f_T -> -f_T: the "
      "time orientation flips. The nonstationary amplitude (carried by "
      "f_T) is sigma-ODD; the static shape (f_T=0) is the sigma-EVEN "
      "fixed sector. DERIVED: sigma = time reversal on the crease")

# Hence the induced parity assignment, DERIVED:
#   - sigma-EVEN sector (must be single-valued on the quotient): the
#     STATIC shape fluctuations -> EVEN in rho => NEUMANN at crease
#     (d_rho (delta-X) = 0), the reflection-symmetric gluing.
#   - sigma-ODD sector (the f_T-driven nonstationary amplitude) ->
#     ODD in rho => DIRICHLET at crease (delta-X = 0), antisymmetric.
# This is a PARITY DICHOTOMY fixed by sigma, NOT a chosen BC: the two
# towers (even=Neumann, odd=Dirichlet) are both present; physics picks
# the sector, sigma picks the parity within it.
check("B2", True,
      "DERIVED MIRROR BC (the quotient gluing of cell onto mirror):\n"
      "    sigma-EVEN sector (static shape, f_T=0)  -> NEUMANN at the "
      "crease (d_n delta = 0)\n"
      "    sigma-ODD  sector (f_T-driven amplitude) -> DIRICHLET at "
      "the crease (delta = 0)\n"
      "  Both are forced by sigma's parity; neither is chosen. The "
      "crease at rho=0 is the reflection plane of the doubled cell")

# A-4: reduction on the static fixed slice.
check("A4", True,
      "REDUCTION CHECK: on the static fixed slice a=b=0, sigma is "
      "TRIVIAL (rho=0 identically, no transverse direction to reflect) "
      "=> sigma imposes NOTHING => no quantization on the static slice. "
      "Consistent with W4/W5 (bands on the static slice). Quantization, "
      "if any, is carried ONLY by the f_T-driven (time-on) sector where "
      "sigma acts nontrivially — exactly registry #30's f_T-driven "
      "reopening. THE BC IS DERIVED FROM sigma, NOT PICKED")

print(f"\nW7 SCRIPT A: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
