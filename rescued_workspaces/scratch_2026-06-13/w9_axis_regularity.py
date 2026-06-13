#!/usr/bin/env python3
"""W9 PHASE 2 — script 1: AXIS REGULARITY of the both-sector metric.

GEOMETRIC, NO ACTION. We treat the W6 both-sector metric

  g4 = diag-block[[-f,0,0,0],[0,1/f,q,0],[0,q,r^2 W,0],
                  [0,0,0,r^2 sin^2(th)/W]],  W=(1+w)^2,
  f, q, w  co-equal geometric unknowns of (r, theta) (static slice
  here; time row added in a later script).

reused VERBATIM from committed w6_arm1_lib.py (imported, NOT edited):
  build_fields, build_metric, geom (Christoffel/Ricci/Ricci scalar).

THE GEOMETRIC QUESTION (analyze, do not invent): the H1 area-form
template says a discrete integer falls out when a REGULARITY/CLOSURE
condition on the ANGULAR embedding admits only special configurations
(there: dim Lambda^3 V = 1 unique at N=3; the area form = the exterior
cube of the ell=1 triple).  Here the analog closure condition on the
2D (r x theta) geometry is ELEMENTARY FLATNESS at the symmetry axis
theta = 0, pi: the proper circumference of a small loop around the
axis divided by 2 pi times the proper radius must -> 1 (no conical
defect).  This is a PURE GEOMETRY condition (no action, no eigenvalue).

  cone ratio  C(r,theta->0) = lim  (proper circumference)/(2 pi * proper radius)
            = lim_{th->0}  sqrt(g_phiphi) / [ th * sqrt(g_thth) ]   (axis at th=0)

For the round metric (w=q=0): g_phiphi = r^2 sin^2 th, g_thth = r^2,
sqrt(g_phiphi)/(th sqrt(g_thth)) = sin(th)/th -> 1.  Regular.

With the angular block on (w,q != 0): does axis regularity CONSTRAIN
(w, q) at the axis, and is the admissible set DISCRETE or CONTINUOUS?

PRE-STATED CRITERION (frozen before the computation):
  * DISCRETE-FROM-GEOMETRY  <=>  the cone-regularity (and the companion
    finite-curvature) conditions admit only a COUNTABLE/INTEGER-indexed
    family of axis behaviours of (w,q) -- e.g. w(axis) forced to a set
    of isolated values, or an integer winding/period selected.
  * CONTINUUM  <=>  the conditions are satisfied on an OPEN set of
    (w,q) axis data (one inequality / one smooth constraint that leaves
    free functions), i.e. axis regularity fixes a RELATION but not a
    discrete list.

Output: exact cone ratio as a function of the axis data of (w,q); the
regularity constraint; verdict discrete vs continuum WITH the geometric
reason.  All hypothesis-grade; assert-laden.
"""
import sys
import sympy as sp

sys.path.insert(0, '/home/udt-admin/udt_mass_codex')
from w6_arm1_lib import build_metric  # committed; imported, not edited

T, r, th = sp.symbols('T r theta', real=True)
r = sp.Symbol('r', positive=True)

log = []
def out(*a):
    s = ' '.join(str(x) for x in a)
    log.append(s)
    print(s, flush=True)

out("=" * 70)
out("W9 script 1 : AXIS REGULARITY (elementary flatness) of g4(f,q,w)")
out("=" * 70)

# Build the metric with f,q,w as GENERAL functions of (r,theta) -- the
# static slice.  We want the axis (theta->0) behaviour, so make f,q,w
# functions of theta explicitly.
f = sp.Function('f')(r, th)
q = sp.Function('q')(r, th)
w = sp.Function('w')(r, th)
g4, D, sq = build_metric(f, q, w)

out("\nmetric blocks (static slice, T-row off):")
out("  g_tt      =", g4[0, 0])
out("  g_rr      =", g4[1, 1])
out("  g_rth     =", g4[1, 2], "   (= q : the angular SHEAR / off-diagonal)")
out("  g_thth    =", g4[2, 2])
out("  g_phiphi  =", g4[3, 3])

# ---- Elementary flatness about the theta=0 axis. -------------------
# The 2-surface transverse to the axis at fixed (t,r) is spanned by
# (theta, phi).  Near theta=0 the proper radial coordinate from the
# axis is  rho_prop = Int_0^theta sqrt(g_thth) dth'  ~  sqrt(g_thth)|_0 * theta
# and the proper circumference is 2 pi sqrt(g_phiphi).  Regularity:
#   lim_{th->0} sqrt(g_phiphi) / (rho_prop) = 1.
# With g_phiphi = r^2 sin^2(th)/W,  g_thth = r^2 W,  W=(1+w)^2:

W = (1 + w) ** 2
g_phiphi = r ** 2 * sp.sin(th) ** 2 / W
g_thth = r ** 2 * W

# proper radius derivative at axis: sqrt(g_thth) ~ r*(1+w(r,0)) (finite,
# w smooth).  circumference factor sqrt(g_phiphi) ~ r*sin(th)/(1+w).
sqrt_pp = sp.sqrt(g_phiphi)         # = r |sin th| /(1+w)
sqrt_tt = sp.sqrt(g_thth)           # = r (1+w)

# cone ratio C(th) = sqrt(g_phiphi) / ( theta * sqrt(g_thth) )
# (proper radius ~ theta*sqrt(g_thth) to leading order, w smooth at axis)
C_ratio = sp.simplify(sqrt_pp / (th * sqrt_tt))
out("\ncone ratio  C(th) = sqrt(g_phiphi)/(theta*sqrt(g_thth)) =")
out("   ", C_ratio)

# leading limit theta->0 with w -> w0(r) := w(r,0):
w0 = sp.Symbol('w_0', real=True)   # axis value of w
C_lead = sp.limit((sp.sin(th) / th) * 1 / (1 + w0) ** 2, th, 0)
out("\n  lim_{th->0} C  with w(r,0)=w0  =", C_lead, "  ( = 1/(1+w0)^2 )")

# REGULARITY CONDITION: C_lead = 1  =>  (1+w0)^2 = 1  =>  w0 = 0 or w0 = -2.
cond = sp.Eq((1 + w0) ** 2, 1)
sols = sp.solve(cond, w0)
out("\nAXIS REGULARITY (no conical defect) demands (1+w0)^2 = 1:")
out("   solutions for the axis value w0 :", sols)
assert set(sols) == {0, -2}, sols

# Signature legality 1+w>0 (banked) picks w0 = 0 (w0=-2 flips the sign
# of the angular block -> signature illegal).  So:
out("\n  signature-legality (1+w>0, banked) selects  w0 = 0.")
out("  => the SHEAR/conformal angular factor must VANISH ON THE AXIS.")

# Is this discrete or continuum?  It fixes w at the axis to a single
# value (0) -- a BOUNDARY CONDITION on a continuous field, NOT a
# discrete spectrum of cells.  The interior w(r,theta) for theta>0 is
# unconstrained by axis regularity alone.
out("\n--- VERDICT (axis regularity alone) -------------------------------")
out("Axis regularity fixes ONE boundary value  w(r,0)=w(r,pi)=0 on the")
out("conformal angular factor; it is a CONSTRAINT (one relation at the")
out("axis), not a discrete list.  By the pre-stated criterion this is")
out("CONTINUUM at the axis-regularity level: an open set of interior")
out("angular profiles w(r,theta>0) all share w=0 at the axis.")
out("This is the EXPECTED behaviour of a smooth boundary condition and")
out("matches the H1 lesson: discreteness did NOT come from a local")
out("regularity inequality -- it came from a GLOBAL closure/counting")
out("condition (the exterior-cube/area-form).  So the discreteness, if")
out("present, must live in a GLOBAL condition, tested in later scripts.")

# ---- companion: does the OFF-DIAGONAL q produce a conical defect? --
# The (r,theta) 2-metric has off-diagonal g_rth = q.  Its area element
# is sqrt(g_rr g_thth - q^2) = sqrt( (1/f) r^2 W - q^2 ) = r sqrt(D)/(1+w)
# /sqrt(f)... let's get the (r,theta) 2-block determinant D2:
D2 = sp.simplify(g4[1, 1] * g4[2, 2] - g4[1, 2] ** 2)
out("\n(r,theta) 2-block determinant  g_rr g_thth - q^2 =", D2,
    "  (= D/f, D = r^2 W - f q^2)")
out("Positive-definiteness of the spatial block needs D>0 (banked")
out("signature-legal condition).  D=0 is the same-minus mirror fold")
out("(w6_results.md) -- a GLOBAL closure surface, analysed next.")

with open('/tmp/w9_axis_regularity.log', 'w') as fh:
    fh.write('\n'.join(log) + '\n')
out("\n[done] log -> /tmp/w9_axis_regularity.log")
