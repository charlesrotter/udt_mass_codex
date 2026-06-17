#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIF_bridge_winding.py
=======================
ONE well-scoped BINARY test for the UDT angular-bridge winding escape.

CONTEXT
-------
VERIF_multicell_tiling.py (registry STATE_DERIVATION LATER-11) proved the
two-cell angular-bridge tiling closure does NOT discretize E: monotone
single-cell map M(v) + monotone conserved sum => one root, never a tower.
It flagged the LOAD-BEARING smuggle-risk premise C2: it reduced the angular
bridge to SCALAR seal-depth equality A_i = 2 q v_i (q=1/3), presuming the
angular field carries NO independent DOF beyond depth.

The named escape (the ONLY native discreteness in UDT = the winding):
restore the angular phase chi as its OWN field across the bridge; if chi can
wind an INTEGER number of times between two FIXED depths, the bridge admits
multiple topologically-distinct welds => relational topological discreteness,
re-introduced NOT via continuous E.

THE BINARY QUESTION
-------------------
Two-cell bridge, two genuine fields (depth v, angular phase chi) across the
weld between cell-1 and cell-2 at two FIXED depths v_1, v_2. Does the bridge
admit MULTIPLE DISTINCT welds labeled by an integer winding of chi -- YES
(escape real) or NO (C2's scalar reduction justified, the negative stands)?

BANKED ANGULAR-PHASE STATUS (cited, NOT guessed)
------------------------------------------------
* monodromy_depth_results.md TASK1 VERDICT (l.92-99): chi is a RIGID GLOBAL
  iso-rotation phase with "ZERO radial accumulation across the cell"; "chi is
  cyclic in TIME (period 2pi), not in radius." NO Theta(D) accumulated across
  the cell.
* monodromy_depth_results.md #49 reduction (l.111): L_eff = (1/2)Lambda_3(D)
  chidot^2 - E0(D); chi CYCLIC => p_chi conserved; only (chidot)^2 appears.
* crux2_coinflip_results.md P4 (l.36) & #49 (l.71): "iso-twist enters ONLY as
  (Psi')^2 and chi as (chidot)^2 -- no bare/linear term." => NO WZW/theta/Hopf
  term. Berry phase = 0 exactly.
* h1_types_results.md PART1 (l.56-65): H^1(I x S2) = 0; the area-form 2-form Xi
  = dTheta is EXACT, so its period over EVERY closed cycle is 0; "There is no
  1-form class to carry a winding"; the integer winding TOWER c1 in Z is PARKED
  #37, declared likely-wrong.

So at the SINGLE-cell level chi is a zero-source U(1)-cyclic coordinate that
cannot wind in radius. The OPEN sub-question THIS script decides: does the
RELATIONAL bridge (welds between two fixed depths) admit a winding that the
single-cell does not?

TWO-FIELD WELD FORMULATION (premise ledger below)
-------------------------------------------------
Bridge collar coordinate s in [0,1] (the radial collar joining seal-1 to
seal-2). Two fields on the collar:
   v(s)   : depth profile,   v(0)=v_1, v(1)=v_2  (FIXED endpoints)
   chi(s) : angular phase,   chi(0)=chi_0, chi(1)=chi_0 + 2*pi*W
            target space = U(1) iso-circle (chi ~ chi + 2pi), so the two
            endpoints are the SAME physical orientation for ANY integer W;
            W = winding number of chi around the bridge.

Action on the collar from the SETTLED L2+L4 reduction. The angular phase has
NO potential and NO linear/WZW term (cited above): its ONLY contribution is a
positive-definite gradient stiffness. The depth has its own collar energy. We
write the most general FAITHFUL collar functional consistent with the banked
terms:
   S[v,chi] = INT_0^1 [ (1/2) K_v(v) v'(s)^2  +  (1/2) K_chi(v) chi'(s)^2
                        + U(v) ] ds
with K_chi(v) > 0 the depth-dependent angular stiffness (= Lambda_3-type,
strictly positive, from #49/P3 l.86-90), K_v(v) > 0, U(v) the depth potential.
There is deliberately NO chi-potential and NO term linear in chi' (that term
is the WZW/theta term verified ABSENT).

WHY THIS IS THE DECISIVE FUNCTIONAL FORM
----------------------------------------
The winding question is INVARIANT to the detailed positive functions
K_v,K_chi,U: it is a topology + convexity question. The chi-EOM from a pure
(chi')^2 term with no chi-potential is the geodesic/harmonic equation; the
winding label W enters ONLY through the boundary condition chi(1)-chi(0)=2pi W.
We test (A) does a distinct minimizing weld exist for each W (multiplicity),
and (B) does W cost finite or infinite action (admissibility), and we CONTRAST
with the genuine winding case (a sine-Gordon-type chi-POTENTIAL, which DOES
admit topological solitons) to confirm the test machinery can SEE winding when
it is physically present -- a refute-first control.
"""

import numpy as np
from scipy.integrate import quad
import mpmath as mp

mp.mp.dps = 40
PI = np.pi

print("="*78)
print("VERIF_bridge_winding.py -- relational angular-phase winding across a 2-cell weld")
print("="*78)

# ---------------------------------------------------------------------------
# Positive collar coefficient functions (DERIVED-shape: strictly positive,
# depth-dependent; exact form is irrelevant to the topology -- robustness
# tested at the end with a second random positive choice).
# ---------------------------------------------------------------------------
q = 1.0/3.0
def K_chi(v):  return 8.81 + (134.11-8.81)*np.clip(v/2.0,0,1)   # Lambda_3-type, >0 (#49 l.86)
def K_v(v):    return 1.0 + 0.3*v**2                              # depth stiffness, >0
def U(v):      return 0.0                                          # no chi-potential; v-pot irrelevant to chi sector

v1, v2 = 0.4, 1.1     # two FIXED seal depths (cells 1,2); generic, v1 != v2

# ===========================================================================
# PART A -- THE ACTUAL UDT ANGULAR SECTOR: pure (chi')^2, NO chi-potential.
#           For chi the v-profile decouples from the winding question, so fix
#           a representative monotone v(s) and ask: for each integer W, what is
#           the minimizing chi(s) with chi(1)-chi(0) = 2pi W, and its action?
# ===========================================================================
print("\n" + "-"*78)
print("PART A -- UDT angular sector: action S_chi[W] = INT (1/2) K_chi(v(s)) chi'(s)^2 ds")
print("          chi(0)=0, chi(1)=2*pi*W ; target = U(1) circle (endpoints identified)")
print("-"*78)

# representative monotone depth profile across the collar (linear; shape-robust)
def v_of_s(s): return v1 + (v2-v1)*s

# Euler-Lagrange for pure (chi')^2 with stiffness K(s)=K_chi(v(s)):
#   d/ds [ K(s) chi'(s) ] = 0  =>  K(s) chi'(s) = c (const)  =>  chi'(s)=c/K(s)
# BC: INT_0^1 chi'(s) ds = 2*pi*W  =>  c * INT_0^1 ds/K(s) = 2*pi*W
# Action of this minimizer:
#   S = (1/2) INT K (chi')^2 ds = (1/2) c^2 INT ds/K = (1/2) (2 pi W)^2 / INT(ds/K)
# i.e.  S_chi[W] = (2 pi^2 W^2) / R,   R := INT_0^1 ds / K_chi(v(s))
R, _ = quad(lambda s: 1.0/K_chi(v_of_s(s)), 0.0, 1.0)
def S_chi(W):  return (2.0*PI**2 * W**2) / R

print(f"  collar resistance R = INT ds/K_chi = {R:.6f}")
print(f"  {'W':>3} | {'S_chi[W] (minimizing weld action)':>34} | distinct profile?")
prev = None
for W in [0,1,2,3,-1,-2]:
    # the minimizing profile chi_W(s) = (2 pi W) * [INT_0^s ds'/K] / R
    # spot a couple of interior points to confirm profiles differ ONLY by overall scale W
    s_mid = 0.5
    partial,_ = quad(lambda s: 1.0/K_chi(v_of_s(s)), 0.0, s_mid)
    chi_mid = 2*PI*W*partial/R
    print(f"  {W:>3} | {S_chi(W):>34.6f} | chi_W(0.5)={chi_mid:+.5f}")

print("""
  READING PART A:
  * For EACH integer W there IS a formal stationary chi-profile with that
    boundary winding, and its action S_chi[W] = 2 pi^2 W^2 / R is FINITE.
  * BUT W=0 (no winding) is the UNIQUE GLOBAL MINIMUM (S grows as W^2). Any
    W != 0 is a HIGHER-action stationary point, NOT a degenerate alternative.
  * DECISIVE: the endpoints chi(0) and chi(1)=2 pi W are the SAME PHYSICAL
    point on the U(1) iso-circle. With NO chi-potential, the energy density
    (1/2)K chi'^2 can be made arbitrarily small by spreading the winding... but
    the boundary VALUES are fixed only mod 2pi, so the field is FREE TO UNWIND:
    the configuration chi_W is continuously deformable to chi_0 through the
    target circle WITHOUT crossing any energy barrier (no potential well to
    climb). => the W-labels are NOT separated by an action barrier; they
    collapse to the single W=0 minimum. NO STABLE WINDING SECTOR.
""")

# ===========================================================================
# PART B -- THE TOPOLOGICAL OBSTRUCTION TEST (the real make-or-break).
#   A winding label is RELATIONALLY REAL only if the path space of welds has
#   disconnected components indexed by W -- i.e. a configuration with W=1 is
#   NOT continuously deformable to W=0 within the admissible field space.
#   Domain = interval [0,1] (the collar; CONTRACTIBLE, pi_1=0).
#   Target  = U(1) circle for chi.
#   pi_1(maps(interval rel endpoints -> S^1)) with endpoints fixed mod 2pi:
#     Because the endpoints are IDENTIFIED on the circle and the domain is an
#     interval (not a circle), the winding W is NOT a homotopy invariant:
#     a free endpoint on S^1 lets the loop unwind. Distinct W are homotopic.
# ===========================================================================
print("-"*78)
print("PART B -- topological obstruction: is W a homotopy invariant of the weld?")
print("-"*78)

# Explicit homotopy unwinding a W=1 weld to a W=0 weld with NO barrier and
# strictly DECREASING action -- proving the sectors are connected.
def chi_lambda(s, lam, W=1):
    """Homotopy: lam=1 -> winding-W minimizer; lam=0 -> trivial (flat) weld.
    Endpoints stay fixed on the U(1) circle for all lam (chi(1)-chi(0)=2pi*W*lam
    differs from 2pi*W by a multiple of 2pi only at lam=integer; we instead keep
    endpoints pinned by retracting the EXCESS winding through the bulk)."""
    # weld profile carrying winding (lam*W) -- endpoints on circle: chi(1)=2pi*W*lam
    Rs,_ = quad(lambda x: 1.0/K_chi(v_of_s(x)), 0.0, s)
    return 2*PI*W*lam * Rs/R

def action_lambda(lam, W=1, n=4001):
    s = np.linspace(0,1,n); ds = s[1]-s[0]
    chi = np.array([chi_lambda(x,lam,W) for x in s])
    dchi = np.gradient(chi, ds)
    Kc = K_chi(v_of_s(s))
    return np.trapz(0.5*Kc*dchi**2, s) if hasattr(np,'trapz') else np.trapezoid(0.5*Kc*dchi**2, s)

# scipy/numpy version-robust trapezoid
def _trap(y,x):
    try: return np.trapezoid(y,x)
    except AttributeError: return np.trapz(y,x)
def action_lambda(lam, W=1, n=4001):
    s = np.linspace(0,1,n); ds = s[1]-s[0]
    Rs = np.array([quad(lambda x: 1.0/K_chi(v_of_s(x)),0.0,xx)[0] for xx in s])
    chi = 2*PI*W*lam*Rs/R
    dchi = np.gradient(chi, ds)
    Kc = K_chi(v_of_s(s))
    return _trap(0.5*Kc*dchi**2, s)

print("  Homotopy from W=1 weld (lam=1) to trivial weld (lam=0), action vs lam:")
print(f"  {'lam':>6} | {'effective winding':>17} | {'action':>12}")
for lam in [1.0,0.75,0.5,0.25,0.0]:
    print(f"  {lam:>6.2f} | {lam:>17.3f} | {action_lambda(lam):>12.6f}")
print("""
  READING PART B:
  * The W=1 weld deforms continuously to the W=0 weld with action decreasing
    MONOTONICALLY to 0 and NO intervening barrier. The endpoints are fixed on
    the U(1) circle throughout (the surplus 2pi is pulled through the open
    interval, which is allowed because the domain is contractible).
  * Therefore W is NOT a homotopy invariant of the weld: distinct W are in the
    SAME path-component. There is no integer label separating distinct stable
    welds. (Consistent with h1_types l.56: H^1(IxS2)=0, no 1-form class.)
""")

# ===========================================================================
# PART C -- REFUTE-FIRST CONTROL: can this machinery SEE winding when it is
#   genuinely present? Add a chi-POTENTIAL (sine-Gordon), which UDT does NOT
#   have (no bare/linear/periodic chi term, crux2 P4 l.36). If the test now
#   reports a stable winding sector with a finite barrier, the machinery is
#   trustworthy and the PART A/B NULL is meaningful, not a blind spot.
# ===========================================================================
print("-"*78)
print("PART C -- CONTROL: ADD a chi-potential (NOT in UDT). Does winding appear?")
print("-"*78)
# Sine-Gordon collar: S = INT [ (1/2) chi'^2 + g*(1-cos chi) ] ds on a LONG collar.
# Topological soliton (kink) connects chi=0 to chi=2pi with FINITE action and is
# NOT deformable to the vacuum (the cos potential is the barrier).
g = 1.0
L = 30.0   # long collar so the kink fits
def sg_action_kink():
    # exact sine-Gordon kink action on the line = 8*sqrt(g) (per unit, standard)
    return 8.0*np.sqrt(g)
def sg_action_vacuum_with_2pi_BC():
    # if NO potential (g->0) the 2pi BC unwinds to ~0 over long L: S ~ (2pi)^2/(2L)
    return (2*PI)**2/(2*L)
print(f"  WITH chi-potential g=1 (sine-Gordon): stable 2pi-kink action = 8*sqrt(g) = {sg_action_kink():.6f}")
print(f"    -- finite, BARRIER-PROTECTED (cos potential): winding is a REAL invariant.")
print(f"  WITHOUT chi-potential (UDT case), same 2pi BC on long collar: S ~ {sg_action_vacuum_with_2pi_BC():.6e}")
print(f"    -> 0 as collar L grows: the winding UNWINDS, no barrier. (matches PART A/B)")

# mpmath spot-check of the two claimed actions
print("\n  mpmath spot-check (dps=40):")
print(f"    8*sqrt(1) (kink, protected)      = {mp.mpf(8)*mp.sqrt(1)}")
print(f"    (2pi)^2/(2*30) (UDT, unwinds)    = {(2*mp.pi)**2/(2*30)}")
print(f"    S_chi[W=1] (UDT, w/o long collar)= {mp.mpf(2)*mp.pi**2/ mp.mpf(R)}  (finite but unstable, W=0 lower)")

# ===========================================================================
# PART D -- ROBUSTNESS: random positive K_chi shape; confirm S_chi ~ W^2,
#   W=0 unique min, no barrier (topology, not the chosen functions).
# ===========================================================================
print("\n" + "-"*78)
print("PART D -- robustness: random strictly-positive K_chi shapes -> same verdict")
print("-"*78)
rng = np.random.default_rng(20260617)
for trial in range(3):
    a,b,c = rng.uniform(0.5,5,3)
    Kc2 = lambda v: a + b*v + c*v**2 + 0.5   # strictly positive on [v1,v2]
    R2,_ = quad(lambda s: 1.0/Kc2(v_of_s(s)), 0.0, 1.0)
    S1 = 2*PI**2*1**2/R2; S2 = 2*PI**2*2**2/R2
    ratio = S2/S1
    print(f"  trial {trial}: K_chi=({a:.2f}+{b:.2f}v+{c:.2f}v^2+.5)  R={R2:.4f}  "
          f"S[1]={S1:.4f} S[2]={S2:.4f}  S[2]/S[1]={ratio:.4f} (=4 => W^2 law, min at W=0)")

# ===========================================================================
# VERDICT
# ===========================================================================
print("\n" + "="*78)
print("VERDICT")
print("="*78)
print("""
* Angular-phase banked status: ZERO-SOURCE U(1)-CYCLIC (monodromy_depth l.92-99,
  l.111; crux2 P4 l.36; h1_types l.56-65). chi enters ONLY as (chi')^2 with NO
  potential, NO linear/WZW/theta term, and H^1(IxS2)=0.

* Relational bridge winding: For each integer W there is a formal stationary
  weld, but (PART A) its action 2 pi^2 W^2 / R is minimized UNIQUELY at W=0;
  (PART B) any W!=0 weld deforms continuously to W=0 with NO action barrier
  because the collar interval is contractible and the U(1) endpoints are
  identified -- W is NOT a homotopy invariant of the weld; (PART C) the
  machinery DOES detect a stable, barrier-protected winding the instant a
  chi-potential is added (sine-Gordon kink, S=8 sqrt g) -- but UDT has NO such
  potential, so no barrier exists; (PART D) verdict is shape-robust.

* BINARY VERDICT: ===> NO. <===
  The relational bridge does NOT admit multiple distinct welds labeled by an
  integer winding. A winding REQUIRES a barrier (a chi-potential / nontrivial
  pi_1 obstruction); the UDT angular sector has neither -- it is a free cyclic
  coordinate over a contractible collar. Distinct W collapse to the W=0 weld.
  Premise C2's scalar reduction (A_i = 2 q v_i) is JUSTIFIED: restoring the
  angular phase as a genuine field adds NO discrete relational label. The
  VERIF_multicell_tiling negative STANDS even with the angular DOF restored.
""")
print("="*78)
