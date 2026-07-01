#!/usr/bin/env python3
"""
a_function_both_extremes.py  --  OBSERVE pass, 2026-06-18, Claude Opus 4.8 (1M)

Treat the matter mass-dilation exponent a as a FUNCTION a(phi) = d(ln m)/dphi,
NOT a constant.  Carry the NONLINEAR time/light dilation + the Compton-vs-metric
scale comparison into BOTH extremes.  NO fitted values.  NO Lambda.  NOT canon.

The three myopic errors this script is built to AVOID:
  E1: solving a as a constant.  -> a(phi) is symbolic-function from line 1.
  E2: carrying only constant log-rate weights (clock e^{-phi}, light e^{-2phi}),
      which can ONLY produce a constant a.  -> we form the dimensionless ratio
      lambda_C / L_metric and let THAT (a genuine function of phi) drive a(phi).
  E3: constraining at one extreme.  -> both phi<0 (core) and phi>0 (cosmic) here.

Definitions (CANON, prior blind-verified):
  ds^2 = -e^{-2phi} c0^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2,  B = 1/A
  proper time   dtau/dt = e^{-phi}          (the CLOCK)
  proper length dL/dr   = e^{+phi}          (the RULER)
  coordinate light speed c(phi) = c0 e^{-2phi}   (NONLINEAR in phi)
  redshift 1+z = e^{phi};  phi<0 core, phi>0 cosmic boundary (phi~7 at z~1101)
  Compton length lambda_C = hbar/(m c0)   (matter's intrinsic scale, Sense-1 local)
"""

import sympy as sp

phi   = sp.symbols('phi', real=True)
r     = sp.symbols('r', positive=True)
c0,hbar = sp.symbols('c0 hbar', positive=True)
m0    = sp.symbols('m0', positive=True)

print("="*78)
print(" PART 0  --  the non-absorbable fingerprint with a(phi) a FUNCTION")
print("="*78)
# a(phi) is a FUNCTION.  m(phi) = m0 exp(int_0^phi a dphi').
a = sp.Function('a')
m = m0*sp.exp(sp.Integral(a(phi), (phi, 0, phi)))   # symbolic, a is a function
# fingerprint F(phi) = exp(-int_0^phi (a+1) dphi') = (matter ruler)/(metric ruler)
F = sp.exp(-sp.Integral(a(phi)+1, (phi, 0, phi)))
print(" m(phi)      =", m)
print(" fingerprint F(phi) = matter-ruler/metric-ruler = exp(-int (a+1) dphi)")
print("   -> dln F/dphi = -(a(phi)+1).  PHYSICS lives wherever a(phi)+1 != 0.")
print("   -> if a(phi) == -1 on an interval, F is flat there = GR on that interval.")
print()

print("="*78)
print(" PART 1  --  the DEPARTURE MECHANISM carried NONLINEARLY (anti-E2)")
print("="*78)
print("""
 Charles's mechanism: a particle has an INTRINSIC scale lambda_C = hbar/(m c0).
 The metric has its OWN local variation scale L_metric = how fast phi changes,
 i.e. the curvature/gradient radius.  The dimensionless control parameter is

       eps(phi) = lambda_C(phi) / L_metric(phi).

 At terrestrial phi this is astronomically tiny (lambda_C microscopic, L_metric
 ~ cosmic) => a(phi) ~ -1, no departure.  At the EXTREME (deep core) eps -> O(1).
 a(phi)+1 is some function of eps that -> 0 as eps -> 0 and turns on as eps -> 1.

 KEY anti-E2 point: a CONSTANT-log-rate weight (clock e^{-phi}) has NO eps in it,
 so it can never produce this.  The eps-dependence is the WHOLE function.
""")

# L_metric from the metric.  Proper-length curvature/gradient scale.
# In PROPER radial length l (dl = e^{phi} dr), phi varies; the natural metric
# variation length is L_metric = 1 / |dphi/dl| = e^{-phi} / |dphi/dr| (PROPER).
# But there is also the AREAL/curvature scale.  We keep BOTH explicit and flag.
dphidr = sp.Function('phip')(r)   # phi'(r), the metric's own gradient (object-set onset depends on its size)
# proper gradient: dphi/dl = (dphi/dr)/(dl/dr) = e^{-phi} phi'(r)
dphi_dl = sp.exp(-phi)*dphidr
L_metric_proper = 1/sp.Abs(dphi_dl)               # = e^{+phi}/|phi'(r)|
print(" L_metric (proper gradient scale) = e^{+phi} / |phi'(r)|   [PROPER]")
print("   NOTE: this carries phi'(r) = the metric's gradient = OBJECT-SET (size).")
print()

# lambda_C from afar vs proper.  Sense-1: local lambda_C = hbar/(m0 c0) is the
# LOCAL proper Compton length.  As the afar observer attributes mass m(phi),
# the PROPER Compton length the object actually has, measured by proper ruler:
lamC_local = hbar/(m0*c0)                          # local proper Compton (Sense-1, fixed)
print(" lambda_C (local proper, Sense-1) = hbar/(m0 c0)   [intrinsic, FIXED locally]")
print()

# The control ratio eps = lambda_C / L_metric (both PROPER, same ruler -> dimensionless, frame-clean)
eps = lamC_local / L_metric_proper
eps = sp.simplify(eps)
print(" eps(phi) = lambda_C / L_metric =", eps)
print("   = (hbar/(m0 c0)) * |phi'(r)| * e^{-phi}")
print("   -> the e^{-phi} is the NONLINEAR carrier: for phi<0 (core), e^{-phi}>1")
print("      GROWS the ratio; for phi>0 (cosmic), e^{-phi}<1 SHRINKS it.")
print("   -> SIGN-of-phi asymmetry is automatic & opposite at the two extremes.")
print()

print("="*78)
print(" PART 2  --  ANCHOR a(0) = -1 from equivalence principle (the MIDDLE)")
print("="*78)
print("""
 At phi=0: eps = (hbar/(m0 c0))|phi'(r)|.  For any macroscopic/terrestrial object
 lambda_C << L_metric so eps -> 0.  The Bianchi exchange force (a+1)phi' T -> 0
 requires a(0)+1 = 0  <=>  a(0) = -1.  This is the EP anchor: lab/solar matter
 free-falls with the metric, no fifth force.  DERIVED, forced.  (the MIDDLE)
""")

print("="*78)
print(" PART 3  --  SHAPE of the departure: a(phi)+1 = f(eps), f(0)=0")
print("="*78)
print("""
 We do NOT get to INVENT f.  But we CAN ask what the metric's own structure makes
 available, and bound the SHAPE by the two physical requirements + nonlinearity:
   (i)  f(eps) -> 0 as eps -> 0   (EP / GR in the middle)        [DERIVED requirement]
   (ii) f turns on at eps ~ O(1)  (intrinsic scale meets metric scale) [the mechanism]
   (iii) eps(phi) = eps0 * e^{-phi}, eps0 = (hbar/m0 c0)|phi'|   [DERIVED carrier]

 The MINIMAL non-trivial analytic f with f(0)=0 is f(eps)=k*eps^p (p>=1).  Then
       a(phi)+1 = k * eps0^p * e^{-p phi}        [the SHAPE, up to (k,p,eps0)]
 -> a(phi) = -1 + k eps0^p e^{-p phi}.
 This is a GENUINE FUNCTION: -1 in the middle, departing EXPONENTIALLY toward the
 core (phi<0, e^{-p phi} blows up) and DECAYING toward cosmic (phi>0, e^{-p phi}->0).
 The DIRECTION is fixed by the metric (sign of phi); (k,p) and eps0 are the open
 shape/onset parameters -- (k,p) UNIVERSAL-candidate, eps0 OBJECT-SET (carries m0,phi').
""")
# demonstrate the function and its fingerprint for symbolic (k,p,eps0)
k,p,eps0 = sp.symbols('k p eps0', positive=True)
a_phi = -1 + k*eps0**p*sp.exp(-p*phi)
ap1   = a_phi + 1
F_shape = sp.exp(-sp.integrate(ap1, (phi, 0, phi)))
print(" a(phi) (minimal shape) =", a_phi)
print(" a(phi)+1               =", sp.simplify(ap1))
print(" fingerprint F(phi)     =", sp.simplify(F_shape))
print()
# verify a(0)+1 in the eps0->0 (terrestrial) limit
print(" check a(0)+1 =", sp.simplify(ap1.subs(phi,0)), " (= k eps0^p; -> 0 as eps0->0). EP anchor OK in terrestrial limit.")
print()

print("="*78)
print(" PART 4a  --  NEGATIVE-phi extreme (hadronic core): the EXPECTED departure")
print("="*78)
# hadronic phi0 ~ -0.8 to -1.14 (e^{-2phi}~5-10).  For a FUNDAMENTAL particle at the
# core, lambda_C ~ the cell/particle size ~ L_metric  =>  eps ~ O(1).  This is the
# regime where the departure is O(1), NOT tiny.  We do NOT fit; we characterize.
print("""
 At the core a FUNDAMENTAL particle has lambda_C ~ its own size ~ L_metric (the
 cell over which phi varies) => eps ~ O(1) => a(phi)+1 ~ O(k) = O(1) DEPARTURE.
 With phi0 < 0, the carrier e^{-p phi0} > 1 AMPLIFIES it.  So:
   - core a(phi) DEPARTS from -1 by an O(1) amount (NOT a tiny peel).
   - direction: e^{-p phi} growing => |a+1| grows toward deeper core (more negative phi).
   - the ONSET (where eps crosses 1) is set by eps0 = (hbar/m0 c0)|phi'| = the
     object's Compton vs its confinement gradient => OBJECT-SET.
 This is exactly Charles's 'where lambda_C ~ metric scale, a departs' -- and it is
 a FUNCTION, growing into the core, NOT a constant.
""")
# illustrate magnitude with eps~1 at core (NO fitted number; eps=1 is the mechanism's
# own definition of 'the extreme', not a fit)
print(" At the definitional extreme eps=1: a(phi_core)+1 = k  (an O(1) departure).")
print(" => a(phi_core) = -1 + k, k = O(1).  GENUINE a != -1 at the core. (shape-level)")
print()

print("="*78)
print(" PART 4b  --  POSITIVE-phi extreme (cosmic): SNe pins a ~ -1 to phi~1")
print("="*78)
print("""
 SNe: d_L = r e^{phi}, shape mu_g-M-degenerate, MATCHES GR/LCDM out to z~2 i.e.
 phi up to ~1 (1+z=e^phi).  Read as a HARD BOUND:
   the fingerprint F(phi) must stay ~flat (a+1 ~ 0) across 0 <= phi <~ 1.
 In our shape a(phi)+1 = k eps0^p e^{-p phi}: on the POSITIVE side e^{-p phi}
 DECAYS, so if a+1 is small at phi=0 (terrestrial eps0 tiny), it is even SMALLER
 at phi~1.  => the cosmic side is AUTOMATICALLY GR-compatible for a localized
 object whose terrestrial eps0 is tiny.  SNe is satisfied with room to spare;
 it BOUNDS any positive-side departure to onset DEEPER than phi~1 (toward the
 boundary phi~7), where a DIFFERENT object (the cosmic-scale content) could have
 eps0 ~ O(1).  i.e. positive-side departure is possible ONLY for a cosmic-scale
 ruler, not for the lab object SNe standard-candles ride on.
""")
# quantify: the fractional fingerprint departure integrated 0..1 on positive side
val_pos = sp.integrate(ap1, (phi, 0, 1))   # = k eps0^p (1 - e^{-p})/p
print(" integral_0^1 (a+1) dphi =", sp.simplify(val_pos))
print("   -> ln of the cumulative matter/metric ruler mismatch across SNe range.")
print("   -> bounded by SNe shape match (~0.06 mag RMS vs LCDM, validated doc).")
print("   -> for terrestrial eps0<<1 this is << 1: SNe trivially satisfied.")
print()

print("="*78)
print(" PART 5  --  UNIVERSAL SHAPE vs OBJECT-SET ONSET split")
print("="*78)
print("""
 a(phi) = -1 + k * eps0^p * e^{-p phi}.   Split the three knobs:

   - e^{-p phi}  : the CARRIER.  DERIVABLE NOW.  Its DIRECTION (grows into core
                   phi<0, decays toward cosmic phi>0) is fixed by the metric's
                   nonlinear dilation -- NO object needed.  This is the universal
                   asymmetry: the SAME |delta phi| does MORE at the core than at
                   cosmic.  (the e^{-phi} in eps is the nonlinear c/clock carrier.)
   - p (exponent of eps in f): the SHAPE near the extreme.  UNIVERSAL-CANDIDATE:
                   set by HOW the intrinsic length couples to the metric variation
                   (a curvature/gradient response) -- a property of the field
                   equations, not the specific object.  DERIVABLE IN PRINCIPLE
                   from the matter action's response to a varying phi, WITHOUT a
                   full soliton (it is the leading response order).  p=1 is the
                   minimal/default; p could be 2 (curvature, even) -- OPEN, but a
                   small DISCRETE set, gradient(p=1) vs curvature(p=2).
   - eps0 = (hbar/m0 c0)|phi'(r)| : the ONSET LOCATION.  OBJECT-SET.  Carries the
                   object's mass m0 (Compton) AND the metric gradient phi'(r) at
                   its location (its size/confinement).  The phi where eps crosses
                   1 -- i.e. WHERE a departs -- needs the object.  CANNOT be fixed
                   without it.

 SO: the SHAPE/DIRECTION of the departure (exponential, steeper into the core,
 flat-then-on) is DERIVABLE NOW from the metric + hbar.  The ONSET phi (and the
 magnitude k) is OBJECT-GATED.  This is the clean split the prior passes collapsed.
""")
print("DONE.")
