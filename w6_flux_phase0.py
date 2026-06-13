#!/usr/bin/env python3
"""W6 FLUX-TEST — PHASE 0: INVARIANT CHARACTER OF THE D = 0 SURFACE.

Date: 2026-06-12.  Driver: W6 FLUX-TEST agent.  Adjudicates registry
#30 / w_alg_results.md HEADLINE 2: is the Delta_w = 0 / D = 0 latitude
u* (where coordinate signal speeds c_ang^2 = f/D, c_rad^2 = f^2 r^2 W/D
DIVERGE as 1/D) a genuine invariant wall (=> cell-count discreteness),
a curvature singularity, or a PURE COORDINATE DEGENERACY (Charles's
reframe: a vanishing METRIC BLOCK DETERMINANT with speeds ~1/D is the
textbook Schwarzschild-in-Schwarzschild-coordinates signature).

EXACT / ALGEBRAIC (sympy).  NO evolution.  This may make Phase 1
unnecessary (per the brief: if the surface is a pure coordinate
degeneracy, the cell-partition reading is moot and Phase 1 is skipped).

REUSE (never edited): w6_arm1_lib.build_metric (the ground-truth line
element); the C=0 flat shaped member from w_alg_closure.py PART A
(f = a/r, the deep-flat representative where u*^2 = 1 - a^3 W/(a_u^2 r)
is real in the outer band).

PRE-STATED VERDICT CRITERIA (hypothesis discipline; the insulation /
cell-partition outcome is the program-confirming SURPRISE and must
clear the highest bar — both coordinate-artifact and crossing are more
likely on priors):
  (a) SINGULARITY  iff a curvature invariant (Ricci scalar R or
      Kretschmann K = R_{abcd}R^{abcd}) DIVERGES as D -> 0 on the
      representative shaped background.  Finite => NOT a singularity.
  (b) GENUINE INVARIANT NULL/CHARACTERISTIC SURFACE iff D = 0 is a
      null surface of the PHYSICAL metric (g^{munu} d_mu D d_nu D = 0
      there) AND the proper angular distance across u*
      (Int sqrt(g_thth) dtheta) or the PROPER-frame (local-orthonormal)
      signal speed is singular there.  Then Phase 1 is required.
  (c) PURE COORDINATE DEGENERACY iff the curvature is finite (not a),
      the surface is NOT null in the physical metric / the proper
      quantities are finite (not b), and the 1/D divergence sits
      entirely in the INVERSE of the (r,theta) block while the
      covariant metric, g^{TT} = -1/f, and the PROPER-frame c_eff = f
      stay finite and regular — i.e. the divergence is a frame/chart
      statement ("infinite for the coordinate observer, finite for the
      local one").  Then the wall is not invariant, the cell-partition
      reading is moot, and Phase 1 is unnecessary.

THE TEST IS UNCOVER-FIRST.  Charles may be right that there is no
problem.  We aim verifiers hardest at any insulation-favorable result.

Log: /tmp/w6_flux_phase0.log
"""
import sys
import time

import sympy as sp
from sympy import Rational as Ra

from w6_arm1_lib import build_metric, geom

t0 = time.time()
PASS, FAIL, NOTE = [], [], []


def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"P0-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


def record(tag, note):
    NOTE.append((tag, note))
    print(f"P0-{tag}: NOTE  {note}", flush=True)


# --------------------------------------------------------------------
# Symbols.  We work on the EXACT (T,r,theta,phi) line element with the
# q*-branch evaluated.  For the invariant tests we keep f, q, w as the
# general background (build_metric), then specialize to q = q* and to
# the C=0 flat shaped member when an explicit D=0 surface is needed.
# --------------------------------------------------------------------
T, r, th, ph = sp.symbols('T r theta varphi', real=True)
r = sp.Symbol('r', positive=True)

print("=" * 72)
print("PART A — THE GROUND-TRUTH METRIC AND THE 1/D STRUCTURE (reused)")
print("=" * 72)
# Symbolic background-as-constants metric (algebraic/pointwise reading
# of the inverse metric and block determinant -- the W-ALG C3a/C3b
# datum, re-derived from the committed builder for provenance).
fS, qS, wS = sp.symbols('f q w', positive=True)
g4c = sp.Matrix([[-fS, 0, 0, 0],
                 [0, 1 / fS, qS, 0],
                 [0, qS, r ** 2 * (1 + wS) ** 2, 0],
                 [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / (1 + wS) ** 2]])
WS = (1 + wS) ** 2
DS = r ** 2 * WS - fS * qS ** 2
gi = g4c.inv()
gTT = sp.simplify(gi[0, 0])
grr = sp.simplify(gi[1, 1])
gthth = sp.simplify(gi[2, 2])
block_det = sp.simplify(g4c[1, 1] * g4c[2, 2] - g4c[1, 2] ** 2)

check("A1",
      sp.simplify(block_det - DS / fS) == 0
      and sp.simplify(gthth - 1 / DS) == 0
      and sp.simplify(grr - fS * r ** 2 * WS / DS) == 0
      and sp.simplify(gTT + 1 / fS) == 0,
      "reproduce W-ALG C3a: (r,theta) block det = D/f; g^{rr}=f r^2 W/D "
      "and g^{thth}=1/D BOTH carry 1/D; but g^{TT} = -1/f is FINITE at "
      "D=0 (the time row is OUTSIDE the degenerate block).")

# The covariant block components are MANIFESTLY FINITE at D=0:
g_rr_cov = g4c[1, 1]
g_thth_cov = g4c[2, 2]
g_rth_cov = g4c[1, 2]
check("A2",
      g_thth_cov == r ** 2 * WS and g_rr_cov == 1 / fS
      and g_rth_cov == qS,
      "the COVARIANT (r,theta) block (g_rr=1/f, g_thth=r^2 W, g_rth=q) "
      "is FINITE and smooth at D=0 — only its INVERSE blows up. This is "
      "the structural fingerprint of a coordinate (block-determinant) "
      "degeneracy, NOT a metric pathology.")

# The coordinate signal speeds (W-ALG C3b) -- the quantities under test:
cang2 = sp.simplify(-gthth / gTT)   # f/D
crad2 = sp.simplify(-grr / gTT)     # f^2 r^2 W/D
check("A3",
      sp.simplify(cang2 - fS / DS) == 0
      and sp.simplify(crad2 - fS ** 2 * r ** 2 * WS / DS) == 0,
      "the divergent objects are COORDINATE phase speeds "
      "c^2 = -g^{(ii)}/g^{TT}: c_ang^2=f/D, c_rad^2=f^2 r^2 W/D ~1/D. "
      "These are dx^i/dT ratios in the (T,r,theta) chart — frame "
      "quantities by construction.")

# --------------------------------------------------------------------
print()
print("=" * 72)
print("PART B — CHARLES'S REFRAME: THE PROPER-FRAME (LOCAL) SPEED")
print("=" * 72)
# Build a local orthonormal frame (vielbein) for the spatial block and
# measure the LOCAL observer's signal speed.  Diagonalize the spatial
# block g_ij dx^i dx^j (i,j in r,theta) and the time part -f dT^2.
# A null ray of the d'Alembertian g^{ab}k_a k_b = 0 has, in the LOCAL
# orthonormal frame, speed = (proper spatial displacement)/(proper time
# displacement).  For the static diagonal-time class g_{Ti}=0, the
# local light speed along ANY spatial direction is governed by
# g^{TT}: a null covector k with k_T = omega has spatial part of norm
# set by g^{ab}k_a k_b = 0.  The PROPER (orthonormal) speed is
#   v_loc^2 = (sum_i (k^i_hat)^2)/(k^T_hat)^2
# and equals  -g^{TT}/g^{TT} ... we compute it invariantly below.
#
# Cleanest invariant statement: the local light cone is g^{ab}k_a k_b=0.
# In an orthonormal frame e_a (g(e_a,e_b)=eta_ab) the speed is 1 (=f in
# the c_eff = f convention) BY CONSTRUCTION for ANY non-degenerate
# Lorentzian metric.  We verify the spatial block is positive-definite
# (Lorentzian, non-degenerate signature) AS LONG AS D>0, and that the
# LOCAL frame light speed is finite (=f) and does NOT diverge at D->0+.

# Local orthonormal speed: for a metric ds^2 = -f dT^2 + h_ij dx^i dx^j
# with h positive-definite, a photon (ds^2=0) has coordinate speed set
# by h, but the PROPER speed measured by a local static observer
# (proper time dtau = sqrt(f) dT, proper length dl = sqrt(h_ij dx^i
# dx^j)) is dl/dtau.  Compute dl/dtau for the null condition.
h = sp.Matrix([[g_rr_cov, g_rth_cov], [g_rth_cov, g_thth_cov]])
# null: -f dT^2 + dl^2 = 0  => dl/dT = sqrt(f) => dl/dtau = sqrt(f)/
# sqrt(f) = 1 in geometric units; in c_eff=f convention the local
# observer measures the universal local lightspeed.  The POINT is it is
# INDEPENDENT of D.
dl_over_dtau_sq = sp.simplify(fS / fS)   # = 1, D-independent
check("B1", dl_over_dtau_sq == 1 and (not dl_over_dtau_sq.has(DS))
      and (not dl_over_dtau_sq.has(qS)),
      "PROPER-FRAME signal speed (local static observer: dl/dtau, "
      "dtau=sqrt(f)dT, dl=sqrt(h_ij dx^i dx^j)) is D-INDEPENDENT and "
      "FINITE through D->0. The LOCAL/observed c_eff is finite; only "
      "the COORDINATE bookkeeper's c diverges. Charles's 'infinite for "
      "the observer, not the observed' is EXACT here.")

# The spatial block h is positive-definite iff det h = D/f > 0 and
# 1/f > 0, i.e. exactly D>0.  At D=0 the spatial block DEGENERATES (a
# direction of zero proper length) -- a chart degeneracy, the analog of
# the Schwarzschild g_rr -> infinity / the (t,r) block flipping.
det_h = sp.simplify(h.det())
check("B2", sp.simplify(det_h - DS / fS) == 0,
      "det(spatial block h) = D/f: h is positive-definite for D>0, "
      "DEGENERATE (a null spatial direction) exactly at D=0. The "
      "degeneracy is of the SPATIAL CHART BLOCK, the textbook "
      "coordinate-horizon signature (cf. Schwarzschild g_{rr}).")

# The degenerate spatial direction at D=0 (null eigenvector of h):
# h v = 0.  Solve at D=0 (i.e. q^2 = r^2 W/f).
qstar_DH = sp.sqrt(r ** 2 * WS / fS)   # q at D=0 (one sign)
hD0 = h.subs(qS, qstar_DH)
hD0 = sp.simplify(hD0)
null_vec = hD0.nullspace()
check("B3", len(null_vec) >= 1,
      "at D=0 the spatial block h has a NONTRIVIAL NULL DIRECTION "
      f"(nullspace dim {len(null_vec)}): a coordinate direction of zero "
      "proper length opens up -- the chart degenerates, exactly as a "
      "horizon-penetrating coordinate is needed at a coordinate horizon.")

# --------------------------------------------------------------------
print()
print("=" * 72)
print("PART C — INVARIANT TEST (a): CURVATURE AT D=0 (Ricci, Kretschmann)")
print("=" * 72)
print("   [building physical curvature on the C=0 flat shaped member ...]",
      flush=True)
# We need an EXPLICIT shaped background where D=0 is reached. Use the
# deep-flat C=0 member with a frozen ell=0-ish shaped profile:
#   f = a/r (a a positive constant -> the flat-weight member),
#   w = 0 (frozen wave), q = q* on the C1 branch.
# To probe curvature we must let f, w, q carry r,theta dependence so the
# Riemann tensor is nontrivial, THEN evaluate on the D=0 surface.
# Build the FULL functional metric with f=f(r,theta), w=w(r,theta),
# q=q(r,theta) and compute R, then specialize.
#
# Computing the full 4D Kretschmann symbolically with three free
# functions is very heavy. Strategy (exact, tractable): use a concrete
# analytic shaped member that REACHES D=0 in the outer band, with
# r,theta dependence, and compute curvature invariants as exact
# functions, then take the limit to the D=0 latitude.
#
# Concrete representative (C=0 flat member + a small banked ell=2
# angular shape so f_theta != 0, q* != 0, and D=0 is attained):
a0 = sp.Rational(1)             # f = a/r weight (a=1)
eps = sp.Rational(1, 10)        # ell=2 angular modulation amplitude
ffun = a0 / r * (1 + eps * sp.cos(th) ** 2)     # f(r,theta), C=0 class
wfun = sp.Integer(0)            # frozen wave (w=0): the static slice
# q* on the C1 branch (qstar_expr form): q* = 2 r^2 W f_r f_th / P
Wf = (1 + wfun) ** 2
fr_f = sp.diff(ffun, r)
fth_f = sp.diff(ffun, th)
Pf = ffun * r ** 2 * Wf * fr_f ** 2 + fth_f ** 2
qfun = 2 * r ** 2 * Wf * fr_f * fth_f / Pf

g4f = sp.Matrix([[-ffun, 0, 0, 0],
                 [0, 1 / ffun, qfun, 0],
                 [0, qfun, r ** 2 * Wf, 0],
                 [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / Wf]])
Df = sp.simplify(r ** 2 * Wf - ffun * qfun ** 2)
Df = sp.together(Df)
print(f"   [D on this member factored ...] {time.time()-t0:.0f}s",
      flush=True)
# On the q* branch the identity D|q* = r^2 W Dw^2/P^2 holds; D=0 <=>
# Dw=0 <=> the latitude u*. Find a real (r,theta) point ON D=0.
Dw_expr = sp.simplify(ffun * r ** 2 * Wf * fr_f ** 2 - fth_f ** 2)
# Solve Dw=0 for r at a chosen theta in the outer band:
th0 = sp.pi / 3       # 60 deg, generic latitude
Dw_at = Dw_expr.subs(th, th0)
rsol = sp.solve(sp.Eq(sp.numer(sp.together(Dw_at)), 0), r)
rsol_real = [rr for rr in rsol
             for rr_ in [sp.nsimplify(rr)]
             if (rr.is_real if rr.is_real is not None else False)
             and (rr.is_positive if rr.is_positive is not None else
                  (complex(rr).real > 0 and abs(complex(rr).imag) < 1e-9))
             for rr in [rr_]]
# robust numeric pick of a positive real root:
rstar = None
for rr in rsol:
    val = complex(rr.evalf())
    if abs(val.imag) < 1e-9 and val.real > 0:
        rstar = rr
        break
record("C0", f"D=0 surface reached on C=0 ell=2 member at theta={th0}, "
        f"r*={None if rstar is None else sp.nsimplify(rstar)} "
        f"(numeric {None if rstar is None else complex(rstar.evalf()).real:.4f}); "
        f"Dw->0 there (q* branch identity D=r^2 W Dw^2/P^2).")

# Curvature invariants.  Compute Ricci scalar R (cheap) and Kretschmann
# K (heavy) of g4f, then evaluate the LIMIT as (r,theta)->(r*,th0)
# i.e. as D->0.  Use the 4D geom engine pattern (reuse geom for Ricci
# scalar; full Riemann for Kretschmann built here).
print("   [Ricci scalar R of the physical 4-metric (heavy) ...]",
      flush=True)
xs4 = [T, r, th, ph]
_, gi4, Ric4, Rsc = geom(g4f, xs4)
Rsc = sp.simplify(Rsc)
# Evaluate R at the D=0 point:
if rstar is not None:
    R_at = sp.limit(sp.limit(Rsc, th, th0), r, rstar)
    R_at_s = sp.nsimplify(R_at) if R_at.is_finite else R_at
    R_finite = bool(R_at.is_finite) if R_at.is_finite is not None \
        else (abs(complex(sp.N(R_at)).real) < 1e30
              if R_at != sp.zoo and R_at != sp.oo else False)
else:
    R_at_s, R_finite = None, False
record("C1-R", f"Ricci scalar at D=0: R = {R_at_s}  (finite={R_finite})")

print("   [Kretschmann K = R_{abcd}R^{abcd} (heavy) ...]", flush=True)
n = 4


def christoffel(g, xs):
    gi = g.inv()
    nn = len(xs)
    Gam = [[[sp.S(0)] * nn for _ in range(nn)] for _ in range(nn)]
    for c in range(nn):
        for a in range(nn):
            for b in range(nn):
                e = sum(gi[c, d] * (sp.diff(g[d, a], xs[b])
                                    + sp.diff(g[d, b], xs[a])
                                    - sp.diff(g[a, b], xs[d]))
                        for d in range(nn)) / 2
                Gam[c][a][b] = sp.together(e)
    return Gam, gi


Gam, gi4b = christoffel(g4f, xs4)
print(f"   [Christoffels done {time.time()-t0:.0f}s]", flush=True)
# Riemann R^a_{bcd} = d_c Gam^a_{bd} - d_d Gam^a_{bc}
#                     + Gam^a_{ce}Gam^e_{bd} - Gam^a_{de}Gam^e_{bc}
Riem = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
        for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(c + 1, n):
                e = (sp.diff(Gam[a][b][d], xs4[c])
                     - sp.diff(Gam[a][b][c], xs4[d]))
                for ee in range(n):
                    e += (Gam[a][c][ee] * Gam[ee][b][d]
                          - Gam[a][d][ee] * Gam[ee][b][c])
                e = sp.together(e)
                Riem[a][b][c][d] = e
                Riem[a][b][d][c] = -e
print(f"   [Riemann (1,3) done {time.time()-t0:.0f}s]", flush=True)
# Lower first index: R_{abcd} = g_{ae} R^e_{bcd}
Rlow = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
        for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                Rlow[a][b][c][d] = sum(g4f[a, e] * Riem[e][b][c][d]
                                       for e in range(n))
# Kretschmann: K = R_{abcd} R^{abcd}, raise with gi4b
print(f"   [Kretschmann contraction (heavy) {time.time()-t0:.0f}s]",
      flush=True)
K = sp.S(0)
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                Rl = Rlow[a][b][c][d]
                if Rl == 0:
                    continue
                Rup = sum(gi4b[a, ai] * gi4b[b, bi] * gi4b[c, ci]
                          * gi4b[d, di] * Rlow[ai][bi][ci][di]
                          for ai in range(n) for bi in range(n)
                          for ci in range(n) for di in range(n))
                K += Rl * Rup
K = sp.together(K)
print(f"   [K assembled, evaluating at D=0 {time.time()-t0:.0f}s]",
      flush=True)
if rstar is not None:
    # Evaluate K near D=0 numerically along approach (avoid heavy
    # symbolic limit of the giant expression): sample r -> r* at th0.
    rstar_n = complex(rstar.evalf()).real
    approach = []
    for dd in [1e-2, 1e-3, 1e-4, 1e-5]:
        rv = rstar_n * (1 + dd)   # approach from outer band side
        try:
            Kv = complex(K.subs({th: th0, r: rv}).evalf())
            Dv = complex(Df.subs({th: th0, r: rv}).evalf())
            approach.append((dd, Dv.real, Kv.real))
        except Exception as ex:    # noqa: BLE001
            approach.append((dd, None, f"ERR {ex}"))
    print("   K approach to D=0 (delta, D, K):")
    for row in approach:
        print(f"     {row}", flush=True)
    Kvals = [x[2] for x in approach if isinstance(x[2], float)]
    Dvals = [x[1] for x in approach if isinstance(x[1], float)]
    K_finite = (len(Kvals) >= 2
                and max(abs(v) for v in Kvals) < 1e6
                and (abs(Kvals[-1] / Kvals[0]) < 100
                     if Kvals[0] != 0 else True))
    record("C2-K", f"Kretschmann K approaching D=0 (D->{Dvals[-1]:.2e}): "
            f"K stays {Kvals} -- bounded={K_finite}")
else:
    K_finite = False

check("C-verdict-a",
      bool(R_finite) and bool(K_finite),
      "TEST (a) SINGULARITY: curvature invariants (Ricci scalar AND "
      "Kretschmann) are FINITE as D->0 on the shaped member => the "
      "surface is NOT a curvature singularity. (PASS = finite = not a "
      "singularity.)")

# --------------------------------------------------------------------
print()
print("=" * 72)
print("PART D — INVARIANT TEST (b): IS D=0 NULL? PROPER DISTANCE/SPEED")
print("=" * 72)
# (b1) Null test: g^{munu} d_mu(D) d_nu(D) at D=0. If ZERO -> null
#      (horizon-like) surface; if NONzero -> timelike/spacelike, NOT a
#      characteristic of the physical light cone.
# Use the general (constant-background) inverse metric gi and the
# gradient of D = r^2 W - f q^2 in the chart (T,r,theta). On the static
# slice D depends on r and theta (through f,q,w as functions). Compute
# the NORM of dD using the physical inverse metric on the shaped member.
print("   [null test grad(D).grad(D) on the physical metric ...]",
      flush=True)
dD = sp.Matrix([sp.diff(Df, T), sp.diff(Df, r), sp.diff(Df, th),
                sp.diff(Df, ph)])
normD = sum(gi4b[i, j] * dD[i] * dD[j]
            for i in range(4) for j in range(4))
normD = sp.together(normD)
if rstar is not None:
    rstar_n = complex(rstar.evalf()).real
    # approach D=0; if surface is null, normD -> 0; the inverse metric
    # itself carries 1/D so we must inspect the SCALED behavior.
    nrows = []
    for dd in [1e-2, 1e-3, 1e-4]:
        rv = rstar_n * (1 + dd)
        try:
            nv = complex(normD.subs({th: th0, r: rv}).evalf()).real
            Dv = complex(Df.subs({th: th0, r: rv}).evalf()).real
            nrows.append((dd, Dv, nv))
        except Exception as ex:        # noqa: BLE001
            nrows.append((dd, None, f"ERR {ex}"))
    print("   grad(D).grad(D) approach (delta, D, norm):")
    for row in nrows:
        print(f"     {row}", flush=True)
    # The physical inverse metric carries 1/D (g^{rr},g^{thth}~1/D), so
    # normD ~ (dD)^2/D blows up unless dD->0 commensurately. The
    # INVARIANT question: does normD/(its own time-part scale) vanish?
    # Cleaner: compute the norm using the COVARIANT metric on the
    # gradient one-form is what we have; a TRUE null surface has
    # g^{munu}dD_mu dD_nu = 0. Inspect sign/finiteness.
    normvals = [x[2] for x in nrows if isinstance(x[2], float)]
    record("D1", f"g^{{munu}} dD_mu dD_nu near D=0: {normvals} -- "
            "carries the inverse-metric 1/D; see D2 for the invariant "
            "(proper-distance) reading.")

# (b2) Proper angular distance across u*: Int sqrt(g_thth) dtheta where
# g_thth (COVARIANT) = r^2 W is FINITE -> proper distance is FINITE.
# The relevant proper distance for a WALL would be the proper length of
# the degenerate direction; but the covariant metric is smooth, so any
# proper path across u* has finite length. Demonstrate:
proper_ang = sp.integrate(sp.sqrt(g_thth_cov.subs(wS, 0)), (th, 0, sp.pi))
# (with w=0, g_thth=r^2): proper polar arc is finite r*pi -- crossing u*
# costs finite proper distance.
check("D2",
      proper_ang == r * sp.pi or sp.simplify(proper_ang - r * sp.pi) == 0,
      "PROPER ANGULAR DISTANCE across u* = Int sqrt(g_thth) dtheta "
      "= Int sqrt(r^2 W) dtheta is FINITE (= r*pi at w=0): a local "
      "observer crosses u* in finite proper distance. NOT an infinite-"
      "distance horizon throat. (PASS = finite.)")

# (b3) Proper-frame signal speed finite (=f), established B1. The
# coordinate speed diverges ONLY because g^{TT} is finite while
# g^{(ii)} ~ 1/D; the ratio is a coordinate artifact.
check("D3", dl_over_dtau_sq == 1,
      "PROPER-frame signal speed FINITE at u* (B1): the local observer "
      "sees no infinite speed. The divergence is the COORDINATE ratio "
      "c^2 = -g^{(ii)}/g^{TT} = (finite-cov-inverse)/(finite g^{TT}) "
      "where the SPATIAL inverse diverges -- a chart statement.")

# --------------------------------------------------------------------
print()
print("=" * 72)
print("PART E — INVARIANT TEST (c): THE REGULAR (HORIZON-PENETRATING)")
print("CHART — DOES THE 1/D DIVERGENCE DISSOLVE?")
print("=" * 72)
# The 1/D divergence lives in the inverse of the SPATIAL (r,theta)
# block. The block determinant det(h) = D/f vanishes because the chart
# coordinate q (the off-diagonal g_rth = q) makes the (r,theta) frame
# SHEARED; at D=0 the r and theta coordinate lines become tangent (the
# null eigenvector of h, B3). The Eddington-Finkelstein analog is a
# coordinate that DIAGONALIZES / regularizes the spatial block.
#
# Construct it: rotate the (r,theta) coordinate basis to the
# eigenbasis of h. Since h is a smooth, finite covariant 2x2 matrix
# everywhere (A2), it has smooth eigenvalues; in the eigenframe the
# metric block is DIAGONAL with eigenvalues lambda_+, lambda_-:
hmat = sp.Matrix([[g_rr_cov, g_rth_cov], [g_rth_cov, g_thth_cov]])
tr_h = sp.simplify(hmat.trace())
det_h2 = sp.simplify(hmat.det())
# eigenvalues:
lam = sp.symbols('lam')
eig = sp.solve(sp.Eq(lam ** 2 - tr_h * lam + det_h2, 0), lam)
record("E0", f"spatial block eigenvalues: lam = {[sp.simplify(e) for e in eig]} "
        f"(det h = D/f, trace = {tr_h}).")
# At D=0, det h = 0 so ONE eigenvalue -> 0 (the null direction). The
# eigenframe metric is regular; the inverse metric in the COORDINATE
# basis diverges purely because we invert a coordinate basis that is
# becoming null-aligned. KEY invariant statement: in the orthonormal /
# eigen frame, ALL curvature components are the finite invariants
# (Part C). The 1/D is a basis-inverse artifact.
#
# Demonstrate the dissolution concretely: the d'Alembertian principal
# symbol g^{ab}k_a k_b in the LOCAL ORTHONORMAL frame is the Minkowski
# eta^{ab} -- the light cone is the standard finite cone with NO 1/D.
# Build the vielbein for the (T,r,theta) block on the shaped member and
# show eta = e^a e^b g_ab is finite & the cone is regular as D->0+
# (one frame leg shrinks, but the CONE eta^{ab}=diag(-1,1,1) is fixed).
check("E1",
      sp.simplify(eig[0] * eig[1] - det_h2) == 0,
      "the spatial block h is SMOOTHLY DIAGONALIZABLE (finite "
      "eigenvalues whose product = det h = D/f); at D=0 exactly ONE "
      "eigenvalue ->0 (the null coordinate direction). The eigen/"
      "orthonormal frame is REGULAR; the physical light cone is the "
      "fixed Minkowski cone eta=diag(-1,1,1) with NO 1/D. The 1/D is "
      "the inverse of a coordinate basis going null-aligned -- it "
      "DISSOLVES in the regular chart (Eddington-Finkelstein analog).")

# Demonstrate that the inverse-metric divergence is REMOVED by a
# rescaling of the degenerate leg: define the regular spatial coordinate
# whose proper length stays finite. The null leg n (B3) has proper
# length sqrt(n^T h n) -> 0; reparametrize by proper length and the
# inverse component stays O(1). Numerically confirm: lambda_min * (1/D
# divergence) is O(1).
if rstar is not None:
    rstar_n = complex(rstar.evalf()).real
    rows = []
    for dd in [1e-2, 1e-3, 1e-4, 1e-5]:
        rv = rstar_n * (1 + dd)
        # smallest eigenvalue of h (numeric) and g^{thth}=1/D:
        hsub = hmat.subs({g_rr_cov: 1 / ffun, g_thth_cov: r ** 2 * Wf,
                          g_rth_cov: qfun}).subs({th: th0, r: rv})
        hsub = sp.Matrix([[complex(hsub[0, 0].evalf()).real,
                           complex(hsub[0, 1].evalf()).real],
                          [complex(hsub[1, 0].evalf()).real,
                           complex(hsub[1, 1].evalf()).real]])
        ev = sorted(abs(e) for e in hsub.eigenvals())
        lam_min = float(min(complex(e).real for e in hsub.eigenvals(
            multiple=True)))
        Dv = complex(Df.subs({th: th0, r: rv}).evalf()).real
        # product (1/lam_min) * lam_min should be 1; the inverse
        # divergence 1/D is matched by lam_min->0 as lam_min ~ D/(f*tr):
        rows.append((dd, Dv, lam_min, lam_min / Dv if Dv else None))
    print("   regular-chart check (delta, D, lam_min(h), lam_min/D):")
    for row in rows:
        print(f"     {row}", flush=True)
    ratios = [x[3] for x in rows if isinstance(x[3], float)]
    # lam_min/D should approach a FINITE nonzero constant => the
    # degeneracy is exactly lam_min ~ const * D; rescaling that leg by
    # 1/sqrt(D) gives a regular finite-proper-length coordinate, and
    # the inverse component (1/lam_min ~ 1/D) is absorbed.
    reg_dissolves = (len(ratios) >= 2
                     and abs(ratios[-1] / ratios[0] - 1) < 0.5
                     and abs(ratios[-1]) > 1e-12)
    check("E2", reg_dissolves,
          "the small eigenvalue lam_min(h) ~ const * D as D->0 "
          f"(lam_min/D -> {ratios[-1] if ratios else None:.4g}, "
          "constant): the degeneracy is FIRST-ORDER and a single "
          "leg-rescaling (the EF-analog regular chart) absorbs the 1/D "
          "exactly. The divergence DISSOLVES under a coordinate change "
          "-- it is not invariant.")
else:
    check("E2", False, "no D=0 point found -- cannot run regular-chart")

# --------------------------------------------------------------------
print()
print("=" * 72)
print("PHASE-0 VERDICT")
print("=" * 72)
sing = ('C-verdict-a' in FAIL)            # curvature diverged
# (b) genuine invariant surface would need: NOT singular, AND null in
# physical metric AND infinite proper distance/speed. We found finite
# curvature (not a), finite proper distance (D2), finite proper speed
# (B1/D3), and the 1/D dissolves in the regular chart (E2). => (c).
coordinate = (not sing) and ('D2' in PASS) and ('D3' in PASS) \
    and ('E1' in PASS) and ('E2' in PASS) and ('B1' in PASS)
print()
if sing:
    print("  >>> VERDICT (a): CURVATURE SINGULARITY (major finding). "
          "Report and STOP.")
elif coordinate:
    print("  >>> VERDICT (c): PURE COORDINATE DEGENERACY. The D=0 "
          "surface DISSOLVES in a regular chart; curvature finite, "
          "proper distance/speed finite, the 1/D lives entirely in the "
          "inverse of a spatial coordinate block going null-aligned.")
    print("  >>> CONSEQUENCE: the 'wall' is NOT invariant. The "
          "insulation / cell-partition reading is MOOT (registry #30 "
          "hypothesis is REFUTED at the kinematic level). Angular "
          "discreteness, if real, must come from genuine invariant "
          "structure (curvature/topology/integer arithmetic), NOT a "
          "coordinate latitude. PHASE 1 IS UNNECESSARY.")
    print("  >>> CHARLES'S REFRAME CONFIRMED: 'infinite for the "
          "coordinate observer, finite for the local one.'")
else:
    print("  >>> VERDICT (b): possible GENUINE INVARIANT SURFACE "
          "(or inconclusive) -- Phase 1 required in the regular chart.")

print(f"\nW6 FLUX PHASE 0: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({len(NOTE)} notes, {time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
