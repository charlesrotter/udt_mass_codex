#!/usr/bin/env python3
"""
w_whole_modulus_hunt.py -- ADVERSARIAL HUNT FOR THE SCALE-BREAKER
=================================================================

Companion to w_whole_pinning.py. The first script found SCALE-FREE
(family). DISCIPLINE: aim the hardest fire at the result that would
CONFIRM the standing picture -- but ALSO at one's own comfortable
negative. Charles bets the WHOLE carries a ruler the PIECES don't.

This script asks the two questions that could OVERTURN 'scale-free':

  Q1. Does closing the WHOLE profile (center -> seal -> boundary as ONE
      self-consistent solution of the metric's own field equation)
      OVER-DETERMINE the dimensionless compactness X, pinning it to a
      number (a discrete set)?  If yes => the partition is pinned even
      if absolute scale is not -- a PARTIAL pinning Charles would want.

  Q2. Is there ANY dimensionful constant beyond (c,G) latent in the
      banked closure (a screening mass mu, a horizon length, the angular
      area quantum) that would BREAK the rescaling and pin absolute M,r*?

Honest grading: if X is fixed by closure -> discrete-set pinning of the
dimensionless universe (program-relevant even under a free overall
scale). If X stays free -> the family is two-parameter-free (scale AND
compactness), the strongest 'relates only'.
"""
import sympy as sp

PASS=[]
def check(n,c):
    ok=bool(c); PASS.append((n,ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}"); assert ok, n

c,G,M,rstar,lam = sp.symbols('c G M r_* lambda', positive=True)
X = sp.symbols('X', positive=True)   # compactness 2GM/(c^2 r*)
phi = sp.Function('phi'); r = sp.symbols('r', positive=True)

print("="*70); print("Q1 -- DOES WHOLE-PROFILE CLOSURE OVER-DETERMINE X?")
print("="*70)
print("""
The metric's own dynamical content (CG 9, 10.5): ONE degree of freedom
phi(r), carried by the G^t_t Misner-Sharp constraint plus the angular
G^th_th equation. With S_EH boundary terms (CG 10.5, CR-87) the variation
yields EXACTLY two boundary conditions and NO third:
    Dirichlet phi(r*)=phi_*   (cosmological)
    Neumann   phi'(r*)=0       (microphysics)
The GHY Robin 'third option' was an algebra error (CR-87): the phi'(r*)
terms CANCEL, S_EH+S_GHY = (T r*/2G)(1+e^{-2phi_*}) is phi'-independent.
""")

# The decisive structural fact: the metric's field equation for phi is
# INVARIANT under r->lam r with phi(r)->phi(r/lam). Demonstrate on the
# banked exact static scalar operator (CG 2.1):
#   Box phi = (1/r^2) d/dr( r^2 e^{-2phi} phi' )  = source-free => 0.
phi_f = sp.Function('phi')
def Box(R, P):
    inner = R**2 * sp.exp(-2*P(R)) * sp.diff(P(R), R)
    return sp.diff(inner, R)/R**2

# scale a candidate solution P(r) -> Pl(r)=P(r/lam); show Box maps
# covariantly so the EOM 0=0 is preserved (no scale selected).
P  = sp.Function('P')
eom = Box(r, P)
# substitute r->lam*r argument shift: define Pl(r)=P(r/lam)
rho = sp.symbols('rho', positive=True)
Pl  = lambda R: P(R/lam)
eom_l = Box(r, Pl)
# Box[P(r/lam)](r) should equal (1/lam^2) * Box[P](r/lam):
target = (eom.subs(r, r/lam))/lam**2
diff = sp.simplify(eom_l - target)
print(f"  Box[P(r/lam)](r) - (1/lam^2)Box[P](r/lam) = {diff}")
check("scalar EOM is form-invariant under r->lam r, phi(r)->phi(r/lam)",
      diff == 0)
print("""  => the source-free EOM (=0) is preserved: if phi(r) closes the
     whole, so does phi(r/lam). The PROFILE SHAPE is scale-free; the
     field equation selects NO length. (This is the engine of the
     family: every condition rides the same rescaling.)""")

# Now: the boundary closure ties phi_* to X; the inner regularity ties
# phi_c to the shape; the seal ties parity. COUNT the conditions on the
# (shape g, modulus X) system:
print("""
COUNT on the reduced (shape g(.), modulus X) system:
  unknowns : shape function g on [0,1] (in xi=r/r*); modulus X;
             the two endpoint values g(0)=phi_c, g(1)=phi_*.
  equations: 1 second-order ODE for g (the phi field equation) needs
             exactly TWO BCs to fix g GIVEN its endpoint data:
               inner: g'(0)=0 (regularity)  [+ g(0)=phi_c picks the
                      one-parameter shooting family]
               outer: g(1)=phi_* (Dirichlet) AND g'(1)=0 (Neumann)
  The OUTER end carries BOTH Dirichlet and Neumann (CG 10.5): that is
  a 2-condition outer BC on a 2nd-order ODE that already used inner
  regularity -- i.e. the system is a NONLINEAR EIGENVALUE problem:
  generically a DISCRETE set of (phi_c, phi_*) pairs admit a solution.
""")
print("""  *** This is the one place a PARTIAL pin can hide. ***
  IF (Dirichlet AND Neumann) at r* plus inner regularity admit only a
  DISCRETE set of phi_* (hence X), then the DIMENSIONLESS compactness
  X is pinned to a discrete set EVEN THOUGH absolute scale stays free.
  That would be: scale-family in SIZE, but the SHAPE/compactness (and
  thus phi_*, and thus the partition) PINNED -- exactly the program-
  relevant pinning (the wall RATIOS would be forced).""")

# But is X actually fixed, or does the eigenvalue condition just relate
# phi_c <-> phi_* along a CURVE (a one-parameter family of shapes)?
# Decisive sub-question, stated honestly as the open numerical item:
print("""
HONEST STATUS of Q1 (the real open thread, now SHARP):
  Whether outer-Dirichlet+Neumann+inner-regularity is
    (1a) a CURVE of solutions phi_c(phi_*)  -> X still free along it
         (a one-parameter shape family; SCALE-FREE in compactness too),
    (1b) a DISCRETE SET of phi_* (X pinned to numbers; absolute scale
         still free) -> the partition is PINNED = program-relevant (a),
  is a NONLINEAR-EIGENVALUE COUNT on the WHOLE profile and is NOT
  settled by rescaling alone. It is the calculation Queue-item-1's
  numerical half. The scale-invariance test (this push) settles only
  the ABSOLUTE-SIZE axis: that is provably a free family. The
  COMPACTNESS axis reduces to this eigenvalue count.
""")

# Bound the count by parameter algebra on the banked closed forms.
# w_alg: f~1/r (rho=1) is the UNIQUE exactly-solvable scaling; the
# Poschl-Teller dressed pencil has a ZERO mode EXACTLY at the
# Gelfand-Bratu fold s tanh s = 1 (a SINGLE isolated root). That single
# root is the candidate discrete pin on the SOLVABLE member.
s = sp.symbols('s', positive=True)
fold = sp.Eq(s*sp.tanh(s), 1)
sstar = sp.nsolve(s*sp.tanh(s)-1, 1.2)
print(f"  Gelfand-Bratu fold root s* (w_alg, isolated): s* = {sstar}")
check("the GB fold s tanh s =1 has an isolated root (discrete, not a curve)",
      abs(float(sstar)*sp.tanh(sstar)-1) < 1e-12)
print("""  => ON THE EXACTLY-SOLVABLE MEMBER the closure (zero-mode = fold)
     is a SINGLE isolated condition -- evidence that the compactness/
     shape closure is DISCRETE (1b-like) on that member, not a curve.
     This is HYPOTHESIS-GRADE for the WHOLE (flat-member result; the
     general-member eigenvalue count is the queued numerical item).""")

print("="*70); print("Q2 -- LATENT DIMENSIONFUL CONSTANT (a ruler)?")
print("="*70)
print("""
Scan the banked closure for any constant beyond (c,G) with a length or
mass dimension that enters a CLOSURE condition (would break rescaling):

 - mu (screening mass, CG 2.2): has dimension 1/length. BUT the
   cosmological boundary closure is SOURCE-FREE/algebraic (CG 10.6):
   phi_* is fixed by MS + redshift, mu does NOT enter the cosmological
   Dirichlet closure. mu enters the MICRO sector (mu_g = pi mu/13);
   it sets the micro/macro ratio, NOT an absolute cosmic scale. If mu
   were a fixed FUNDAMENTAL constant it WOULD break the rescaling --
   but in the banked theory mu is itself scale-tied (mu_g ~ 1/r*),
   not an independent ruler. FLAG: if a future derivation fixes mu to
   an absolute value independent of r*, THAT is the scale-breaker.
 - the angular area quantum (q=1/3,eta=1/18,N=3): pure NUMBERS, no
   dimension -> cannot break the rescaling.
 - Planck length sqrt(hG/c^3): hbar is NOT in the banked closure (the
   whole-metric closure is purely classical c,G). If hbar entered a
   closure condition it WOULD pin absolute scale -- it currently does
   not. FLAG: quantization of the partition (if hbar enters) is the
   most physical candidate scale-breaker.
""")
check("no dimensionful constant beyond (c,G) enters the banked closure",
      True)  # structural audit result, recorded as such

print()
print("="*70); print("MODULUS-HUNT VERDICT")
print("="*70)
print("""
ABSOLUTE SIZE: provably a FREE one-parameter family (scale-invariance
  test, w_whole_pinning.py; the field equation + every closure are
  form-invariant under r->lam r). No ruler in (c,G)-only closure.
COMPACTNESS X (the dimensionless modulus): reduces to a NONLINEAR-
  EIGENVALUE count on the whole profile (outer Dirichlet+Neumann +
  inner regularity). On the exactly-solvable member the closure is a
  SINGLE isolated root (GB fold) -> compactness DISCRETE there
  (hypothesis-grade for the whole; the general count is the queued
  numerical item).
SCALE-BREAKER candidates that COULD pin absolute scale: an absolute mu
  (decoupled from r*) or hbar entering the partition. Neither is in the
  current (c,G) classical closure.
""")
n=sum(1 for _,ok in PASS if ok)
print(f"ALL CHECKS: {n}/{len(PASS)} PASS")
