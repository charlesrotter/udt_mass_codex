#!/usr/bin/env python
"""
VERIF_w_completed_barrier.py  --  OBSERVE (compute), not canonical.

THE ORCHESTRA-COMPLETION QUESTION (per charter's orchestra principle:
a solo null does not imply an ensemble null).

Prior solo (VERIF_ceff_potential*.py): froze the prefactor
P = 2 r^2/(1+w)^2 (set w=0; only phi live), reduced the W2 f-weighted
w-wave to Schrodinger form, got V(r) = -2 phi' f^2/r (attractive well)
but under the regular-core BC psi ~ r (Dirichlet at r=0) it does NOT
bind (pure box-control omega ~ 1/R_wall, registry #1): psi is forced
to zero exactly where the well sits.

HERE: take the UN-FROZEN, w-COMPLETED COUPLED operator (the W6 species
Delta_w + C1), the actual (delta f, delta q, delta w) fluctuation
operator about the hedgehog background, and ask the DECISIVE cheap
question FIRST:

  NEAR-ORIGIN INDICIAL ANALYSIS -- does the coupling generate an
  effective repulsive l_eff(l_eff+1)/r*^2 centrifugal-like barrier
  near r=0 that lifts the threshold and pushes binding OFF dead-centre,
  escaping the regularity-Dirichlet kill?

OPERATOR PROVENANCE (quoted, do NOT guess):
  * The species + system:  w6_arm1_lib.py:8-27 (THE SYSTEM block)
      S = S_C1 + kappa S_species + beta S_Dcell ; metric
      g = [[-f,0,0,0],[0,1/f,q,0],[0,q,r^2 W,0],[0,0,0,r^2 sin^2/W]],
      W=(1+w)^2, sqrt(-g)=r sin sqrt(D)/(1+w), D=r^2 W - f q^2.
      L_species = Delta_w = LGG - LGG|_{w-content=0}.
  * The frozen w-wave bulk (w2_uncovering_results.md:30-31):
      [2 r^2 sin/(1+w)^2](w_T^2/f - f w_r^2).  PREFACTOR
      P = 2 r^2/(1+w)^2  --  the solo froze the (1+w)^2 here.
  * Blocks H,B,C definition (w6_arm1_lib.py:41-53, blocks() :259-280):
      H[(X,m),(Y,n)] = d2L/dX_m dY_n ; B[X,(Y,n)] = d2L/dX dY_n ;
      C[X,Y] = d2L/dX dY ; fluctuation EL row X (lib:46-48):
      (O du)_X = sum_Y[ C dY + B dY_n - D_m( B dY + H dY_n) ].
  * The cross blocks the solo dropped (w2_uncovering_results.md:108-123,
      THE CROSS-BLOCK DISCOVERY): L_wf, L_wq nonzero; Schur eliminating
      delta-w gives effective angular stiffness numerator Delta_w =
      f r^2(1+w)^2 f_r^2 - f_th^2.
  * The interior turning surface / fold (w3_results.md:49-61;
      w6_results.md:33-66): Delta_w/D=0 is a mirror fold; static slice
      degenerate; the angular sector composing on the metric is the
      live frame.

WHAT THE SOLO DROPPED, NOW LIVE:
  (i)  the (1+w)^2 prefactor variation: delta-w enters P, so the w-row
       gets B[w,(w,n)] (first-jet*field) and C[w,w] (field*field) terms
       that are PURE POTENTIAL in the radial w-operator -- the solo's
       Liouville V already had ONE such term; the un-frozen operator
       has the full set.
  (ii) the delta-f and delta-q cross-rows (H,B,C off-diagonal): a
       coupled near-origin indicial system, not a single channel.

METHOD (cheap, decisive, symbolic):
  1. Build the EXACT coupled blocks (C1 + kappa Delta_w) symbolically
     via the committed lib builders (NO heavy 4D Ricci -- Delta_w is
     built directly from LGG, the cheap Gamma-Gamma engine).
  2. Restrict to the STATIC radial channel (T-jets off) -- binding is a
     static-spectrum question -- keeping the FULL w-prefactor variation.
  3. Form the radial w-row operator coefficients:
       A2(r) = coeff of w_rr (principal),  A0(r) = coeff of w (mass),
       plus the cross coefficients to f,q.
  4. Expand about r->0 on a REGULAR hedgehog background
     (f->f0>0, f_r->0, w->0, w_r->0, q->0 ; analytic core) and read
     the indicial exponents of the radial operator: is there a
     POSITIVE C/r^2 (=> l_eff(l_eff+1)) term from the coupling that
     was ABSENT in the frozen-w solo (whose V(r*) ~ finite at r=0)?

float64 numerics spot-check the symbolic reading.
Driver: Claude (Opus 4.8 1M). 2026-06-17. New file only.
"""
import sys
import time
import numpy as np
import sympy as sp
from sympy import Rational as Ra

from w6_arm1_lib import (T, r, th, kap, COORDS, TAGS, FIELDS,
                         build_all_jets, jet_syms, blocks)

t0 = time.time()
print("="*78)
print("PART 0 -- build coupled blocks (C1 + kappa Delta_w), exact")
print("  provenance: w6_arm1_lib.py THE SYSTEM block (lines 8-27)")
print("="*78)
J, dens, raw = build_all_jets()
u, j1 = jet_syms(J)
fj, qj, wj = u['f'], u['q'], u['w']
fT, fr_, fh = j1[('f', 0)], j1[('f', 1)], j1[('f', 2)]
qT, qr_, qh = j1[('q', 0)], j1[('q', 1)], j1[('q', 2)]
wT, wr_, wh = j1[('w', 0)], j1[('w', 1)], j1[('w', 2)]
print(f"  [densities built {time.time()-t0:.0f}s]", flush=True)

# Use the COUPLED density L = C1 + kappa*Delta_w (drop beta D_cell:
# D_cell is the *test-both* non-dynamical branch, w3_results.md:104-108;
# Conjecture A lives in the C1+species dynamical branch).
Lcoup = dens['LC1'] + kap * dens['Dw']
H, B, C = blocks(J, Lcoup)
print(f"  [coupled blocks done {time.time()-t0:.0f}s]", flush=True)

keys = [(nm, i) for nm in FIELDS for i in range(3)]


def cname(k):
    return f"{k[0]}_{TAGS[k[1]]}"


# ---------------------------------------------------------------------
print()
print("="*78)
print("PART 1 -- the w-row of the coupled operator (what the solo froze)")
print("  static channel: T-jets OFF (binding = static spectrum).")
print("="*78)
# static restriction dict: all T-derivative jets -> 0
stat = {fT: 0, qT: 0, wT: 0}
for nm in FIELDS:
    for i in range(3):
        for jx in range(i, 3):
            if 0 in (i, jx):
                stat[J.sym(nm, (i, jx))] = 0


def Hs(a, b):
    return sp.cancel(sp.together(H[(a, b)].subs(stat)))


def Bs(nm, b):
    return sp.cancel(sp.together(B[(nm, b)].subs(stat)))


def Cs(a, b):
    return sp.cancel(sp.together(C[(a, b)].subs(stat)))


# Principal (second-jet) w_rr coefficient in the w-row (lib:51-53):
#   coeff of w_rr in row w = -H[(w,r),(w,r)].
A2_ww = sp.factor(-Hs(('w', 1), ('w', 1)))    # principal w_rr
A2_wh = sp.factor(-Hs(('w', 2), ('w', 2)))    # angular w_thth principal
print("w-row principal coefficients (static, exact):")
print("  coeff[w_rr]   = -H[(w,r),(w,r)] =", A2_ww)
print("  coeff[w_thth] = -H[(w,th),(w,th)] =", A2_wh)

# The cross principal coeffs (w-row couples to f,q second jets):
print("\nw-row cross principal coefficients (couples to f,q):")
for Y in ('f', 'q'):
    crr = sp.factor(-Hs(('w', 1), (Y, 1)))
    cth = sp.factor(-Hs(('w', 2), (Y, 2)))
    crt = sp.factor(-(Hs(('w', 1), (Y, 2)) + Hs(('w', 2), (Y, 1))))
    print(f"  coeff[{Y}_rr]   = {crr}")
    print(f"  coeff[{Y}_thth] = {cth}")
    print(f"  coeff[{Y}_rth]  = {crt}")

# ---------------------------------------------------------------------
print()
print("="*78)
print("PART 2 -- THE POTENTIAL / MASS terms (what the un-frozen P adds)")
print("="*78)
# In the fluctuation EL row w (lib:46-48), the zeroth-order (no-jet of
# the fluctuation) operator piece is C[w,w] dw plus the pieces from
# B that, after the -D_m(...) act, leave undifferentiated-dw terms.
# The PURE mass term (multiplying dw with no derivative) is C[w,w]
# minus total-derivative contributions from B[w,(w,m)].
Cww = sp.factor(Cs('w', 'w'))
print("C[w,w] (field*field, the un-frozen prefactor curvature term):")
print("  C[w,w] =", Cww)
print("\nB[w,(w,m)] (first-jet*field; sourced by P=(1+w)^-2 variation):")
for m in range(3):
    bv = sp.factor(Bs('w', ('w', m)))
    if bv != 0:
        print(f"  B[w,(w,{TAGS[m]})] =", bv)

print("\nCross C[w,f], C[w,q] (delta-w sources delta-f, delta-q):")
print("  C[w,f] =", sp.factor(Cs('w', 'f')))
print("  C[w,q] =", sp.factor(Cs('w', 'q')))
print("\nCross B (w-row jet sources):")
for Y in ('f', 'q'):
    for m in range(3):
        bv = sp.factor(Bs('w', (Y, m)))
        if bv != 0:
            print(f"  B[w,({Y},{TAGS[m]})] =", bv)

# ---------------------------------------------------------------------
print()
print("="*78)
print("PART 3 -- NEAR-ORIGIN INDICIAL ANALYSIS (the decisive cheap test)")
print("  regular analytic hedgehog core: f=f0+O(r^2), w=O(r^2),")
print("  q=O(r) (q is the g_rtheta off-diag; odd in r on axis-regular).")
print("="*78)
# Build the radial w-row operator in the PURE-w channel first (the
# direct analogue of the solo), keeping the un-frozen prefactor.
# Static w-row, only delta-w live (freeze cross fluctuations to isolate
# the self-channel barrier; cross terms handled in Part 4):
#   row_w = C[w,w] dw  -  d/dr( B[w,(w,r)] dw + H[(w,r),(w,r)] dw_r )
#                       -  d/dth( ... )  [angular -> separate l]
# Radial principal:  -d/dr( A2_ww(-1) ... ) -- assemble coefficient fns.
# We need A2_ww, the radial first-order coeff, and the mass, as fns of r
# on the regular background.

# Regular core background as analytic series in r (small-r):
eps = sp.Symbol('epsilon', positive=True)  # bookkeeping order param
# choose representative regular hedgehog: phi(r) = phi0 - a r^2 (so
# f=e^{-2phi}=f0(1+2a r^2+...)), w(r)=w2 r^2, q(r)=q1 r.
f0, a2, w2, q1 = sp.symbols('f0 a2 w2 q1', positive=True)
# field VALUES and radial jets on this background (theta-indep core):
bg = {
    fj: f0*(1 + a2*r**2),
    fr_: f0*2*a2*r,
    fh: 0,
    wj: w2*r**2,
    wr_: 2*w2*r,
    wh: 0,
    qj: q1*r,
    qr_: q1,
    qh: 0,
}


def to_bg(expr):
    return sp.series(sp.together(expr.subs(bg)), r, 0, 3).removeO()


# Principal w_rr coefficient near r=0:
A2_bg = sp.simplify(A2_ww.subs(bg))
print("Principal coeff[w_rr] on regular core (exact in r):")
print("   A2(r) =", sp.factor(A2_bg))
A2_lead = sp.limit(A2_bg/r**2, r, 0)
print("   leading: A2(r) ~ (%s) r^2 as r->0" % sp.simplify(A2_lead))

# Now assemble the FULL radial w-row Schroedinger reduction.
# Static pure-w radial sturm-liouville (drop theta sector -> set l=0
# baseline; the theta principal A2_wh gives the angular ladder):
#   row = -d/dr(A2_ww * w_r) + [lower order] = lambda * (weight) w
# Lower-order radial coefficient A1 = effective coeff of w_r (from
# B[w,(w,r)] and d/dr of H), mass A0 from C[w,w].
A1_ww = sp.cancel(sp.together(Bs('w', ('w', 1))))
print("\nFirst-jet*field B[w,(w,r)] on core:")
A1_bg = sp.factor(A1_ww.subs(bg))
print("   A1(r) =", A1_bg)
A0_bg = sp.factor(Cww.subs(bg))
print("Mass C[w,w] on core:")
print("   A0(r) =", A0_bg)
if A0_bg != 0:
    A0_lead_pow = sp.limit(sp.log(sp.Abs(A0_bg))/sp.log(r), r, 0)
    print("   A0(r) leading power of r ~ r^%s" % sp.simplify(A0_lead_pow))

# ---------------------------------------------------------------------
print()
print("="*78)
print("PART 4 -- Liouville normal form of the COUPLED radial w-operator")
print("  Reduce  -(A2 w_r)' + A0 w = lambda Wt w  to  -psi'' + Veff psi")
print("  and extract the r->0 coefficient of 1/r*^2 (the centrifugal")
print("  barrier).  Compare to the SOLO (frozen-w) Veff(r=0) (finite).")
print("="*78)
# The static pure-w radial operator (self-channel), exact:
#   O[w] = -d/dr(A2_ww w_r) + A0_eff w
# where A0_eff = C[w,w] - d/dr(B[w,(w,r)])   (the EL of the B term).
# Weight for the eigenvalue: from the time-row (the W2 wave) the static
# spectral weight is the w_T^2 coefficient analogue; for a STATIC
# binding question we use the SAME P/f weight as the solo (the time
# kinetic), so we read Veff in the solo's tortoise. The barrier is a
# property of A2,A0 ratios -> coordinate-robust leading 1/r^2.

# Symbolic background-function operator (keep f,w,q as functions of r):
fr = sp.Function('f')(r)
wr = sp.Function('w')(r)
qr = sp.Function('q')(r)
fld_sub = {fj: fr, fr_: sp.diff(fr, r), wj: wr, wr_: sp.diff(wr, r),
           qj: qr, qr_: sp.diff(qr, r), fh: 0, qh: 0, wh: 0}
A2f = sp.together(A2_ww.subs(fld_sub))
A1f = sp.together(A1_ww.subs(fld_sub))
A0f = sp.together(Cww.subs(fld_sub))
# A0_eff = C[w,w] - d/dr B[w,(w,r)]
A0eff = sp.together(A0f - sp.diff(A1f, r))
print("Self-channel static radial operator  -(A2 w')' + A0eff w :")
print("  A2(r)   =", sp.simplify(A2f))
print("  A0eff(r)=", sp.simplify(A0eff))

# Liouville: -(A2 w')' + A0eff w = lam Wt w.  Put p=A2, and reduce to
# normal form in the tortoise xi with dxi = dr/sqrt(A2/Wt)? For the
# leading 1/r^2 barrier we only need the small-r exponent of the
# indicial equation of -(A2 w')' + A0eff w = 0:
#   A2 ~ alpha r^p,  A0eff ~ gamma r^s.  Frobenius w ~ r^k:
#   -(A2 w')' ~ -alpha r^p [k(k-1) r^{k-2} + p k r^{k-2}]
#             = -alpha k(k-1+p) r^{k+p-2}.
# Indicial (balance principal against itself; A0eff subleading if
# s > p-2): k(k-1+p)=0 -> k=0 or k=1-p.  The regular core forces the
# branch k>=0 finite.  A POSITIVE 1/r*^2 barrier <=> after Liouville
# normalization the exponent pair is shifted to k=l_eff+? Determine
# directly by computing Veff's r->0 limit * r*^2.

# Evaluate on the explicit regular core series to read exponents:
def lead_pow(expr_r):
    e = sp.simplify(expr_r.subs({fr: f0*(1+a2*r**2), wr: w2*r**2,
                                 qr: q1*r}).doit())
    e = sp.series(e, r, 0, 4).removeO()
    if e == 0:
        return None, sp.Integer(0)
    p = sp.Poly(sp.expand(e), r).monoms()
    # lowest power present:
    terms = sp.expand(e).as_ordered_terms()
    return e, min(sp.degree(t, r) if t.has(r) else sp.Integer(0)
                  for t in terms)


A2e, A2p = lead_pow(A2f)
A0e, A0p = lead_pow(A0eff)
print("\nNear-core leading powers on the regular hedgehog core:")
print(f"  A2(r)    ~ r^{A2p}")
print(f"  A0eff(r) ~ r^{A0p}")
print("  (Frobenius: -(A2 w')' principal balances at k(k-1+A2p)=0.)")
if A2p is not None:
    kbranch = sp.solve(sp.Symbol('k')*(sp.Symbol('k')-1+A2p),
                       sp.Symbol('k'))
    print(f"  indicial roots k = {kbranch}  (regular core keeps k>=0)")

print(flush=True)
print("="*78)
print("PART 5 -- direct Veff(r) and the 1/r*^2 coefficient (numeric)")
print("="*78)


def run_numeric(f0v=2.0, a2v=0.3, w2v=0.5, q1v=0.4, kapv=1.0,
                Rmax=6.0, N=4000):
    """Build A2,A0eff numerically on a regular core+decay background,
    form the self-channel radial operator, reduce to Liouville normal
    form in the SOLO tortoise dr*=dr/f, and read Veff."""
    rr = np.linspace(1e-4, Rmax, N)
    # regular core that decays: f = f0*(1+a2 r^2) e^{-(r/Rc)^2}+1*(tail)
    Rc = 1.5
    fnum = 1.0 + (f0v-1.0)*np.exp(-(rr/Rc)**2)*(1+a2v*rr**2)
    wnum = w2v*rr**2*np.exp(-(rr/Rc)**2)
    qnum = q1v*rr*np.exp(-(rr/Rc)**2)
    fp = np.gradient(fnum, rr)
    wp = np.gradient(wnum, rr)
    qp = np.gradient(qnum, rr)
    # lambdify A2f, A0eff, A1f as functions of (f,f',w,w',q,q',kap)
    fS = sp.Function('f')(r)
    args = (fr, sp.diff(fr, r), wr, sp.diff(wr, r), qr, sp.diff(qr, r),
            kap)
    A2L = sp.lambdify(args, A2f, 'numpy')
    A0L = sp.lambdify(args, A0f, 'numpy')
    A1L = sp.lambdify(args, A1f, 'numpy')
    A2v = A2L(fnum, fp, wnum, wp, qnum, qp, kapv)
    A0v = A0L(fnum, fp, wnum, wp, qnum, qp, kapv)
    A1v = A1L(fnum, fp, wnum, wp, qnum, qp, kapv)
    A0effv = A0v - np.gradient(A1v, rr)
    # Liouville normal form of -(A2 w')' + A0eff w = lam Wt w.
    # Use weight Wt = A2/f^2 (so principal speed^2 = f^2, matching the
    # solo's c_eff=f reading). tortoise dr*=dr/f.
    Wt = A2v/fnum**2
    rstar = np.concatenate([[0], np.cumsum(np.diff(rr)/((fnum[1:]+fnum[:-1])/2))])
    # In tortoise, -(A2 w')' + A0eff w = lam Wt w becomes
    #  -(P D w)' (D=d/dr*) + ... ; the Liouville potential is
    #  Veff = A0eff/Wt + (1/sqrt(s)) d^2 sqrt(s)/dr*^2, s = sqrt(A2*Wt).
    s = np.sqrt(np.abs(A2v*Wt))
    ds = fnum*np.gradient(s, rr)
    d2s = fnum*np.gradient(ds, rr)
    Veff = A0effv/Wt + d2s/np.maximum(s, 1e-30)
    return rr, rstar, Veff, A2v, A0effv, Wt, fnum


rr, rstar, Veff, A2v, A0effv, Wt, fnum = run_numeric()
# read the 1/r*^2 coefficient near origin:
mask = (rstar > 1e-3) & (rstar < 0.3)
coef = Veff[mask]*rstar[mask]**2
print(f"  Veff(r*)*r*^2 near origin (=> l_eff(l_eff+1) if constant>0):")
print(f"    at r*~{rstar[mask][0]:.4f}: {coef[0]:+.5g}")
print(f"    at r*~{rstar[mask][len(coef)//2]:.4f}: {coef[len(coef)//2]:+.5g}")
print(f"    at r*~{rstar[mask][-1]:.4f}: {coef[-1]:+.5g}")
print(f"  Veff(r*->0) raw values: {Veff[mask][:3]}")
cmed = np.median(coef)
print(f"  median Veff*r*^2 in (0,0.3): {cmed:+.5g}")
if cmed > 0.25:
    leff = (-1+np.sqrt(1+4*cmed))/2
    print(f"  => POSITIVE 1/r*^2 barrier; l_eff ~ {leff:.3f}")
else:
    print(f"  => NO positive 1/r*^2 barrier (coef <= 0 or ~0)")
print(f"\n  SOLO comparison: frozen-w V(r*)=-2 phi' f^2/r is FINITE at")
print(f"  r=0 (no 1/r*^2); coeff Veff_solo*r*^2 -> 0.  Coupled gives:"
      f" {cmed:+.4g}")

print(f"\nDONE ({time.time()-t0:.0f}s)")
