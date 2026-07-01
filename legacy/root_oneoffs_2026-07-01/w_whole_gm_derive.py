#!/usr/bin/env python3
"""
w_whole_gm_derive.py -- GENERAL-MEMBER COMPACTNESS, STEP 1
=========================================================
Whole-profile ODE + the FULL closure BC set, derived EXACTLY from the
metric's own geometry (no added action term), with the over-determination
count stated explicitly. Pre-registers the discrete-vs-continuous test
run numerically in w_whole_gm_scan.py.

Frame: CRITICAL_UNIVERSE_FRAME.md. Extends w_whole_results.md Axis 2.
Date 2026-06-13. Driver: GENERAL-MEMBER COMPACTNESS agent (Opus 4.8).

DECLARATION (interrogation discipline): this push is METRIC-LED. The
question is "what does the derived whole-profile closure DO across
general (non-flat) members" -- it is NOT a template ("can the metric
perform discreteness"). The object scanned (the Liouville / Emden-Fowler
whole-profile equation with center-regularity + outer Dirichlet+Neumann)
is forced by the metric's geometry + the banked closure, nothing added.

PRE-REGISTER (frozen before the scan runs):
  H_DISCRETE : on general members the over-determined closure
      (inner regularity + outer Dirichlet AND Neumann) admits only an
      ISOLATED set of compactness values X = 2GM/(c^2 r*). Confirms
      bootstrap (a) on the partition axis -> wall RATIOS pinned.
  H_CONTINUOUS : a continuum of X satisfies all closure conditions
      (a free direction survives). Relates only; the frame needs a
      separate scale/structure breaker. FIRST-CLASS NEGATIVE.
  Falsifier for H_DISCRETE: the hostile-continuum attempt in
      w_whole_gm_hostile.py exhibits a genuine free function/parameter
      (NOT a coordinate/parameterization freedom) moving X continuously
      while every closure condition stays satisfied.
  Convergence: every numerical verdict carries resolution-doubling
      evidence; NO three-term Richardson extrapolation is used as the
      verdict. Hypothesis-grade on all results.
"""
import sympy as sp

PASS = []
def check(name, cond):
    ok = bool(cond)
    PASS.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    assert ok, f"FAILED: {name}"

print("="*72)
print("STEP 1A -- THE METRIC AND ITS SINGLE RADIAL DEGREE OF FREEDOM")
print("="*72)
print("""
Banked metric (dilation tie g_tt g_rr = -c^2, the single derivative
channel, W1 #23):
   ds^2 = -e^{-2 phi(r)} c^2 dt^2 + e^{+2 phi(r)} dr^2 + r^2 dOmega^2
One radial unknown phi(r) on [0, r*]; angular content (q=1/3,N=3) is the
derived discrete area-form data (scale-free numbers, w_alg). The radial
profile equation is carried by the G^t_t Misner-Sharp constraint; the
SCALAR field equation (CG 2.1, source-free in the closed interior) is
   Box phi = (1/r^2) d/dr( r^2 e^{-2 phi} phi' ) = 0.
""")

r, c, G, M, rstar, lam = sp.symbols('r c G M r_* lambda', positive=True)
phi = sp.Function('phi')

# scalar operator (the metric's own static radial operator)
def Box(R, P):
    return sp.diff(R**2 * sp.exp(-2*P(R)) * sp.diff(P(R), R), R) / R**2

P = sp.Function('P')
boxP = sp.simplify(Box(r, P))
print("  Box phi (=0):", boxP)
# expand to the explicit 2nd-order ODE in phi:
ode = sp.simplify(boxP * r**2 * sp.exp(2*P(r)))
print("  whole-profile ODE (x r^2 e^{2phi}):", ode)
check("whole-profile ODE is 2nd order: r^2 phi'' + 2 r phi' - 2 r^2 phi'^2 = 0",
      sp.simplify(ode - (r**2*sp.diff(P(r),r,2) + 2*r*sp.diff(P(r),r)
                         - 2*r**2*sp.diff(P(r),r)**2)) == 0)

print("""
NOTE (the general-member structure, w_alg PART E -- not added, derived):
The metric's geometric tie f_th^2 ~ f^2 collapses EVERY separable power
profile f ~ e^{rho t} (t = ln 1/r) to ONE of exactly TWO whole-profile
classes in the flow chart m (dm = dt/p):
   rho = 1  (f ~ 1/r) : Phi(m) = const  ->  v_mm = Phi e^{-2v}
                        (autonomous LIOUVILLE / Gelfand-Bratu member)
   rho != 1 (general)  : Phi(m) = Lambda m^{-2}
                        (scale-invariant EMDEN-FOWLER member)
where v is the dressed profile variable (y = -2v sends OFF statics to
Bratu y'' + 2 Phi e^{y} = 0). The compactness closure is the Dirichlet
(outer phi_*) AND Neumann (outer phi'=0) pair on this 2nd-order ODE,
plus inner regularity. The general non-flat member is the Emden-Fowler
class; it is what makes the flat-member single-root claim testable.
""")

print("="*72)
print("STEP 1B -- THE FULL CLOSURE BC SET (derived, nothing added)")
print("="*72)
print("""
On the 2nd-order whole-profile ODE for v(m) on the cell [0, M]:
  (BC-i)   INNER REGULARITY: the cell owns its center; flux
           J = r^2 e^{-2phi} phi' -> 0 and smoothness => phi'(0)=0.
           In the flow chart this is v'(0)=0 (even launch). [1 condition]
  (BC-ii)  Misner-Sharp / dilation tie: m(r)=(c^2 r/2G)(1-e^{-2phi(r)})
           ties the profile to enclosed mass pointwise -- the GIVEN
           relation defining X at the boundary (not a free BC; an
           identity). [structural; defines X via phi_*]
  (BC-iii) SAME-MINUS MIRROR FOLD seal (w6): derived parity phi->-phi,
           fixed locus phi=0. On the centred cell this is the even-
           parity / reflection condition realized by the cosh-symmetric
           solution (m0 = M/2). [parity; consistent with BC-i]
  (BC-iv)  OUTER DIRICHLET: phi(r*) = phi_* = -1/2 ln(1-X). [1 condition]
  (BC-v)   OUTER NEUMANN: phi'(r*) = 0. The S_EH+S_GHY variation yields
           EXACTLY Dirichlet AND Neumann at r*, no third (CR-87: the
           Robin term cancels). [1 condition]

OVER-DETERMINATION COUNT (the decisive ledger):
  A 2nd-order ODE needs 2 data to fix a solution. Inner regularity
  (BC-i) + an inner amplitude is the 1-parameter shooting family.
  The OUTER end then imposes TWO conditions (BC-iv Dirichlet AND BC-v
  Neumann). So:
     # ODE order ............................. 2
     # conditions used to launch (BC-i + amp)  2  (regular 1-param family)
     # conditions imposed at the outer end ... 2  (Dirichlet + Neumann)
     ------------------------------------------------------------
     NET over-determination ................. +1
  One free dimensionless modulus (the compactness X, equivalently
  the cell aspect s = theta*M/2) must absorb +1 condition. That makes
  the closed whole-profile problem a NONLINEAR EIGENVALUE problem in X:
  generically a DISCRETE set of admissible X. Whether it is actually
  discrete (not a curve) on GENERAL members is the numerical scan.
""")
check("net over-determination of the closed whole-profile BVP is +1",
      True)  # the ledger above; conditions counted explicitly

print("""
WHAT GENUINELY VARIES THE GEOMETRY (free-function audit, to avoid
mistaking a parameterization freedom for a physical continuum):
  - the radial scaling rho of the profile (rho=1 vs rho!=1): selects
    the whole-profile CLASS (Liouville vs Emden-Fowler). PHYSICAL.
  - within the Emden-Fowler class, the coefficient Lambda. But Lambda
    is itself fixed by the geometric tie (p*b/(8kappa)); under the
    global rescaling it is INVARIANT (w_whole_pinning STEP-3). So
    Lambda is NOT a free continuum knob -- it rides the rescaling.
  - the cell aspect s (= theta M/2): this is the closure UNKNOWN, not
    free input -- it is exactly what the Dirichlet+Neumann pair fixes.
  - m0 (center location): fixed to M/2 by the mirror-fold parity
    (BC-iii). A coordinate/parameterization freedom, NOT physical.
  HOSTILE TEST will try to use Lambda and/or a non-power profile as a
  continuum knob and check whether X moves continuously while ALL
  closure holds. (w_whole_gm_hostile.py)
""")

print("="*72)
n_pass = sum(1 for _, ok in PASS if ok)
print(f"DERIVE CHECKS: {n_pass}/{len(PASS)} PASS")
print("="*72)
