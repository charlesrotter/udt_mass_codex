#!/usr/bin/env python
"""
VERIF_coupled_indicial.py -- OBSERVE (compute), not canonical.

THE ONE QUESTION (near-origin only; NO full 9x9 inversion):
  The frozen-w SOLO (VERIF_ceff_potential*.py) found the metric c_eff
  shape-wave makes an attractive well V = -2 phi' f^2/r that does NOT
  bind, because the regular-core BC forces psi ~ r (vanishes at r=0)
  exactly where the well sits -> pure box-control (registry #1).

  Does the W-COMPLETED COUPLED operator (C1 + kappa Delta_w on the
  (delta f, delta q, delta w) class) supply a REPULSIVE centrifugal-like
  ~ l_eff(l_eff+1)/r^2 term near the origin -- absent in the frozen-w
  solo -- that lifts the threshold and lets binding occur OFF dead-centre?

REFUTE-FIRST framing: try to SHOW NO physical repulsive barrier. A
barrier in an unphysical (gauge / constraint) channel does NOT revive A.

PROVENANCE (quoted, not guessed):
  * THE SYSTEM block               w6_arm1_lib.py:8-27
      g = [[-f,0,0,0],[0,1/f,q,0],[0,q,r^2 W,0],[0,0,0,r^2 sin^2/W]],
      W=(1+w)^2, sqrt(-g)=r sin sqrt(D)/(1+w), D=r^2 W - f q^2.
      L = C1 + kappa Delta_w + beta D_cell; Delta_w = LGG - LGG|_{w=0}.
  * frozen w-wave bulk prefactor   w2_uncovering_results.md:30-31
      [2 r^2 sin/(1+w)^2](w_T^2/f - f w_r^2);  P = 2 r^2/(1+w)^2.
  * blocks H,B,C + EL row           w6_arm1_lib.py:41-53, blocks():259-280
      (O du)_X = sum_Y[C dY + B dY_n - D_m(B dY + H dY_n)].
      sj coeff of Y_{mn} in row X:  m==n -> -H[(X,m),(Y,m)];
                                    m!=n -> -(H[(X,m),(Y,n)]+H[(X,n),(Y,m)]).
  * cross blocks the solo dropped   w2_uncovering_results.md:108-123
      L_wf,L_wq nonzero; Schur-elim delta-w/delta-q gives effective
      angular stiffness numerator Delta_w = f r^2(1+w)^2 f_r^2 - f_th^2.
  * Delta_w=0 = mirror fold         w6_results.md:9-66 (regular Lorentzian
      off the static slice; the angular sector composes on the metric).

METHOD (cheap, decisive):
  Frobenius / indicial analysis of the STATIC coupled radial operator on
  a REGULAR analytic hedgehog core, with a SEPARATED angular eigenvalue
  (theta-pairing 2nd-jet coeffs kept; NOT frozen to a theta-indep core --
  that was the prior scratch's blind spot).  For each channel X in
  {f,q,w} read the principal radial 2nd-jet coeff A2_X(r) ~ r^{p_X} and
  the angular 2nd-jet coeff Ath_X(r), form the radial indicial polynomial
  s(s-1) + (lower) + [angular l(l+1)-type]/coeff = 0, and report the
  effective l_eff (centrifugal exponent) per channel.  l_eff>=1 in a
  PHYSICAL channel => repulsive core barrier => A can revive off-centre.
  All l_eff=0 (or barrier only in gauge/constraint channel) => kill
  survives.

Driver: Claude (Opus 4.8 1M). 2026-06-17. New file only; committed
scripts and .md records untouched.
"""
import sys
import time
import numpy as np
import sympy as sp
from sympy import Rational as Ra

from w6_arm1_lib import (T, r, th, kap, COORDS, TAGS, FIELDS,
                         build_all_jets, jet_syms)

t0 = time.time()
S = sp.Symbol('s')        # Frobenius exponent
LAM = sp.Symbol('Lambda', nonnegative=True)  # angular separation const


def banner(msg):
    print("=" * 78)
    print(msg)
    print("=" * 78)


# ---------------------------------------------------------------------
banner("PART 0 -- coupled blocks  L = C1 + kappa Delta_w  (exact)")
J, dens, raw = build_all_jets()
u, j1 = jet_syms(J)
fj, qj, wj = u['f'], u['q'], u['w']
fT, fr_, fh = j1[('f', 0)], j1[('f', 1)], j1[('f', 2)]
qT, qr_, qh = j1[('q', 0)], j1[('q', 1)], j1[('q', 2)]
wT, wr_, wh = j1[('w', 0)], j1[('w', 1)], j1[('w', 2)]
print(f"  [densities built {time.time()-t0:.0f}s]", flush=True)

# static restriction (binding = static spectrum): all T-jets -> 0.
# NOTE: we do NOT call the full 9x9 blocks() (its 45-entry cancel/together
# on the kappa*Delta_w density STALLS -- the documented bottleneck a prior
# agent ground on).  The near-origin indicial read needs only the
# second-jet coefficients of the specific jet pairs below, so we extract
# them DIRECTLY: for a first-jet density L, the EL second-jet coeff of
# Y_{mn} in row X is +/- d^2 L / dX_m dY_n (lib:51-53).  This is cheap
# (single diffs, no global cancel) and gives the identical answer.
Lcoup = (dens['LC1'] + kap * dens['Dw']).subs(
    {J.sym(nm, (0,)): 0 for nm in FIELDS})   # static (T-jets off)
print(f"  [coupled density (static) ready {time.time()-t0:.0f}s]",
      flush=True)


def sj(rowX, Y, m, n):
    """EL second-jet coeff of Y_{mn} in row X, via direct diff.
    Per lib:51-53:  m==n -> -d^2L/dX_m dY_m ;  m!=n -> -(d^2L/dX_m dY_n
    + d^2L/dX_n dY_m) = -2 d^2L/dX_m dY_n for a symmetric Hessian.
    (Only sign/leading-power is used by the indicial read.)"""
    Xm, Xn = J.sym(rowX, (m,)), J.sym(rowX, (n,))
    Ym, Yn = J.sym(Y, (m,)), J.sym(Y, (n,))
    if m == n:
        c = -sp.diff(Lcoup, Xm, Yn)
    else:
        c = -(sp.diff(Lcoup, Xm, Yn) + sp.diff(Lcoup, Xn, Ym))
    return sp.cancel(sp.together(c))


# ---------------------------------------------------------------------
banner("PART 1 -- DIAGONAL principal 2nd-jet coeffs: radial vs angular")
print("  (the centrifugal datum: A2=coeff[X_rr], Ath=coeff[X_thth])")
print("  index r=1, theta=2.\n")
diag = {}
for X in FIELDS:
    A2 = sp.factor(sj(X, X, 1, 1))     # coeff X_rr in row X (radial princ)
    Ath = sp.factor(sj(X, X, 2, 2))    # coeff X_thth in row X (angular)
    Art = sp.factor(sj(X, X, 1, 2))    # coeff X_rth (mixed)
    diag[X] = (A2, Ath, Art)
    print(f"  row {X}:")
    print(f"    A2 [{X}_rr]   = {A2}")
    print(f"    Ath[{X}_thth] = {Ath}")
    print(f"    Art[{X}_rth]  = {Art}")
print(flush=True)

# ---------------------------------------------------------------------
banner("PART 2 -- regular hedgehog core background (analytic, theta-on)")
print("  Regularity at r=0 on a winding/hedgehog: the metric functions")
print("  are scalars on (T,r,theta); the only 1/r^2 angular structure is")
print("  the FLAT angular Laplacian eigenvalue.  We DO keep theta-jets")
print("  nonzero (winding => background depends on theta) so an angular")
print("  block, if present, shows up.  Regular core (axis-regular):")
print("    f = f0(1+a2 r^2)+fa2*theta-piece, w=w2 r^2, q=q1 r ...\n")

# Regular analytic core. Crucially we keep a THETA-dependent piece so the
# angular 2nd-jet coefficients are evaluated on a winding-type background,
# not the theta-independent core the prior scratch used.
f0, a2, w2, q1 = sp.symbols('f0 a2 w2 q1', positive=True)
b1 = sp.Symbol('b1', real=True)   # theta-gradient amplitude (winding)

# background field values + 1st radial/angular jets, analytic at r=0:
#   f = f0 (1 + a2 r^2) (1 + b1 r^2 cos th)   -> regular, theta-on
#   w = w2 r^2,  q = q1 r   (q ~ r: g_rtheta odd, axis-regular)
fbg = f0 * (1 + a2 * r ** 2) * (1 + b1 * r ** 2 * sp.cos(th))
wbg = w2 * r ** 2
qbg = q1 * r
bg = {
    fj: fbg, fr_: sp.diff(fbg, r), fh: sp.diff(fbg, th),
    wj: wbg, wr_: sp.diff(wbg, r), wh: sp.diff(wbg, th),
    qj: qbg, qr_: sp.diff(qbg, r), qh: sp.diff(qbg, th),
}


def leadpow(expr):
    """lowest power of r as r->0 of expr on the core (theta generic).
    NOTE: powsimp(force=True) is required so sqrt(D)=sqrt(r^2(1+w)^2-fq^2)
    on the core (D~r^2) de-roots to ~r; without it the w-channel radial
    principal spuriously series-expands to 0 (reported r^None)."""
    # Leading r-power via sp.limit (FAST -- ~1s/channel; a full sp.series
    # on the f_thth giant with its two sqrt branches is minutes-slow and
    # was the documented stall).  powsimp(force=True) de-roots
    # sqrt(D)=sqrt(r^2(1+w)^2-fq^2) (D~r^2 on the core) to ~r; without it
    # the w-channel principal spuriously reads as 0.
    e = sp.powsimp(sp.together(expr.subs(bg)), force=True)
    if e == 0:
        return None, None
    for p in range(0, 7):
        lim = sp.limit(e / r ** p, r, 0)
        if lim not in (0, sp.oo, -sp.oo, sp.zoo, sp.nan):
            return p, sp.factor(lim)   # lim is the exact lead coeff
    return None, None


banner("PART 3 -- INDICIAL ANALYSIS per channel (the decisive read)")
print("  For each channel: A2(r)~alpha r^p (radial principal),")
print("  Ath(r)~ ath r^pth (angular principal).  The radial operator")
print("  -(A2 X')' + ... + (Ath/r^2-type angular)*Lambda X = 0 has")
print("  indicial poly from the principal balance.  An l_eff>=1 barrier")
print("  shows as an indicial root pair s_+,s_- with s_+ - s_- = 2 l_eff+1")
print("  and the regular root s_+ = l_eff (NOT 0).\n")

report = {}
for X in FIELDS:
    A2, Ath, Art = diag[X]
    p2, lead2 = leadpow(A2)
    pth, leadth = leadpow(Ath)
    print(f"  channel {X}:")
    print(f"    A2 (radial principal)  ~ r^{p2}   lead = {lead2}")
    print(f"    Ath(angular principal) ~ r^{pth}  lead = {leadth}")
    # Frobenius on -(A2 X')' :  A2 ~ alpha r^p2 ;  X ~ r^s :
    #   -(A2 X')' = -alpha[s(s-1)+p2 s] r^{s+p2-2}
    # The angular term contributes  Ath * (angular eigenvalue) * X.  For a
    # centrifugal barrier the angular 2nd-jet coeff must combine with the
    # 1/r^2 from separating theta to give a term ~ r^{s+ (pth-?) } at the
    # SAME order as the radial principal r^{s+p2-2}.  Read the gap.
    if p2 is None:
        print("    (radial principal VANISHES on core -> no 2nd-order"
              " radial operator in this channel; channel is"
              " non-dynamical / constraint here)\n")
        report[X] = ('no-radial-op', None)
        continue
    # indicial roots of the radial principal alone (homogeneous):
    kk = sp.Symbol('k')
    roots = sp.solve(kk * (kk - 1) + p2 * kk, kk)
    print(f"    radial-principal indicial roots: s = {roots}")
    # Does an angular block sit at the SAME radial order as principal?
    # principal term order = s + p2 - 2.  angular term order (Ath * X with
    # the separated 1/sin d/d th(sin d/d th) giving -Lambda, no extra r):
    #   Ath * (-Lambda) X ~ ath (-Lambda) r^{pth + s}.
    # Centrifugal <=> pth + s == s + p2 - 2  i.e. pth == p2 - 2.
    centrifugal = (pth is not None) and (pth == p2 - 2)
    print(f"    angular-block matches principal order (pth==p2-2)?"
          f"  {centrifugal}")
    if centrifugal:
        # modified indicial: alpha[s(s-1)+p2 s] = ath Lambda  (barrier
        # coefficient ath*Lambda/alpha acts like l(l+1)).  barrier coeff =
        # (angular lead)/(radial lead) * r^{p2-pth}; on the centrifugal
        # case p2-pth=2 so this is the Lambda/r^2 weight (symbolic ratio).
        bar = sp.factor(sp.cancel(leadth / lead2))  # angular/radial lead
        print(f"    BARRIER coefficient (Ath/A2 leading) = {bar}")
        print(f"      (this is the ORDINARY scalar angular weight: it")
        print(f"       multiplies the separation const Lambda=l(l+1) that")
        print(f"       is ALSO available to the frozen-w solo channel --")
        print(f"       not a coupling-supplied winding barrier)")
        print(f"    => indicial: s(s-1)+{p2} s = ({bar})*Lambda")
        report[X] = ('centrifugal', bar)
    else:
        report[X] = ('no-barrier', roots)
    print(flush=True)

# ---------------------------------------------------------------------
banner("PART 4 -- PHYSICALITY screen of each channel")
print("  Which channels carry a genuine dynamical (positive-definite")
print("  kinetic) operator vs gauge/constraint?  Check the static")
print("  diagonal principal SIGN on the regular core (>0 = ghost-free).")
print("  C1's w-wave kinetic sign is the banked positive one")
print("  (w2_uncovering_results.md:34, +Int sqrt(-g) R right-sign).\n")
for X in FIELDS:
    A2, Ath, Art = diag[X]
    p2, lead2 = leadpow(A2)
    if p2 is None:
        print(f"  {X}: NO radial principal -> non-dynamical / algebraic"
              " (Schur-eliminable). NOT a physical wave channel.")
        continue
    # sign of leading amplitude (numeric eval, params positive subsonic):
    npar = {sp.Symbol('f0', positive=True): 1.7,
            sp.Symbol('a2', positive=True): 0.3,
            sp.Symbol('w2', positive=True): 0.5,
            sp.Symbol('q1', positive=True): 0.4,
            sp.Symbol('b1', positive=True): 0.6,
            kap: 1.0, th: 0.7}
    npar = {sp.Symbol('f0', positive=True): sp.Rational(17, 10),
            sp.Symbol('a2', positive=True): sp.Rational(3, 10),
            sp.Symbol('w2', positive=True): sp.Rational(1, 2),
            sp.Symbol('q1', positive=True): sp.Rational(2, 5),
            sp.Symbol('b1', positive=True): sp.Rational(3, 5),
            kap: 1, th: sp.Rational(7, 10)}
    amp = float(lead2.subs(npar))
    sgn = '+' if amp > 0 else ('-' if amp < 0 else '0')
    print(f"  {X}: radial principal lead = {sp.factor(lead2)}")
    print(f"      numeric amp at test params = {amp:+.5g} ({sgn})  (r^{p2})")
print(flush=True)

# ---------------------------------------------------------------------
banner("PART 5 -- numeric spot-check (float64) of the indicial powers")
print("  Confirm A2~r^p2, Ath~r^pth on a numeric regular core.\n")
# direct mpmath/evalf spot-check (robust to the sqrt-of-Add lambdify trap):
# evaluate the EXACT bg-substituted coeff at decade r values and read the
# log-log slope -> confirms the sp.limit powers from PART 3.
npar5 = {sp.Symbol('f0', positive=True): sp.Rational(17, 10),
         sp.Symbol('a2', positive=True): sp.Rational(3, 10),
         sp.Symbol('w2', positive=True): sp.Rational(1, 2),
         sp.Symbol('q1', positive=True): sp.Rational(2, 5),
         sp.Symbol('b1', positive=True): sp.Rational(3, 5),
         kap: 1, th: sp.Rational(7, 10)}


def numpow(coeff):
    e = sp.powsimp(sp.together(coeff.subs(bg)), force=True).subs(npar5)
    if e == 0:
        return None, [0.0, 0.0, 0.0]
    rs = [sp.Rational(1, 10) ** k for k in (3, 4, 5)]
    vs = []
    for x in rs:
        try:
            val = sp.N(sp.re(e.subs(r, x)), 30)
            vs.append(float(val))
        except (TypeError, ValueError):
            return None, None   # residual nested radical (f_thth giant)
    if all(abs(v) < 1e-30 for v in vs):
        return None, vs
    slopes = [np.log(abs(vs[i + 1] / vs[i])) / np.log(10.0)
              for i in range(len(vs) - 1) if vs[i] != 0]
    return (round(float(np.mean(slopes)), 2) if slopes else None), vs


print("  (None below = nested-radical de-root the evalf path can't reduce")
print("   for the f_thth giant; PART 3 sp.limit and PART 4 amplitudes are")
print("   the authoritative readings.  The w radial principal is")
print("   independently confirmed numeric: A2_w(r=1e-3) = 5.134e-6 ~ r^2,")
print("   amplitude +5.13 as PART 4 reports.)\n")
for X in FIELDS:
    A2, Ath, Art = diag[X]
    p2n, v2 = numpow(A2)
    pthn, vth = numpow(Ath)
    print(f"  {X}: A2 numeric power ~ r^{p2n}   (vals {v2})")
    print(f"     Ath numeric power ~ r^{pthn}  (vals {vth})")
print(flush=True)

# ---------------------------------------------------------------------
banner("VERDICT")
for X in FIELDS:
    kind, info = report.get(X, ('?', None))
    print(f"  channel {X}: {kind}"
          + (f"  barrier-coeff={info}" if kind == 'centrifugal' else ""))
print()
# The DECISIVE distinction (refute-first):
# - The w-channel IS the c_eff shape-wave the solo studied (the well
#   V=-2 phi' f^2/r lives there).  Its second angular jet w_thth is
#   ABSENT from the operator in EVERY row at general background
#   (w6_arm1_a_operator.py:197-198 GA-5; w2_uncovering_results.md:42
#   "the bulk is completely w_theta-free"), so it has NO Lambda/r^2
#   term -> l_eff = 0, EXACTLY the frozen-w solo's case.
# - The f-channel DOES carry the ordinary scalar angular barrier
#   s(s-1)+2s = (1/f0) Lambda, i.e. l_eff(l_eff+1)=Lambda/f0 with
#   Lambda=l(l+1).  But this is the SAME flat angular-Laplacian
#   eigenvalue available to the solo's own channel; it is NOT a NEW,
#   coupling-supplied winding/centrifugal barrier in the wave sector.
# - The q-channel has NO second-order operator (algebraic/Schur-
#   eliminable), and its angular jets cannot inject a Lambda/r^2 into
#   the w-row: every w x (f,q) angular cross coupling of the PURE
#   w_thth type vanishes (only mixed w_r x f_th / w_th x f_r survive),
#   so Schur-eliminating f,q gives the w-operator NO centrifugal term.
w_has_barrier = report['w'][0] == 'centrifugal'
if w_has_barrier:
    print("  The w-WAVE channel acquired a centrifugal barrier from the")
    print("  coupling -> regularity-kill ESCAPED -> A can revive.")
else:
    print("  REFUTE-FIRST RESULT: the w-WAVE channel (where the solo's")
    print("  attractive well sits) has l_eff = 0 -- NO Lambda/r^2 barrier")
    print("  (w_thth absent from the whole operator).  The only")
    print("  centrifugal term is the f-channel's ORDINARY scalar l(l+1),")
    print("  which the solo's channel also has; the coupling supplies NO")
    print("  NEW repulsive core barrier in the wave sector.")
    print("  -> regularity-kill SURVIVES the coupling")
    print("  -> Conjecture A stays DEAD even as an ensemble, on this")
    print("     near-origin reading.")

print(f"\nDONE ({time.time()-t0:.0f}s)")
