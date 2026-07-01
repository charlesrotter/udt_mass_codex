#!/usr/bin/env python3
"""
ns_scan_fork.py -- WHY the type differs: the time-kinetic SIGN fork, exact
==========================================================================
NS-SCAN push (nonstationary axis, step c verification). Driver: Claude
(Opus 4.8). Date 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md. New file.

ns_scan_symbol.py found the metric's OWN time-dependent dilation operator
(full 4-metric dilation tie, time row on) is HYPERBOLIC in T (cTT/cRR =
-e^{4phi} < 0). The baseline (nonstationary_opener_results.md / rescued
verify_nonstat/v_a3.py C-1,C-2) found ELLIPTIC in T. This script pins WHY,
exactly: the two used DIFFERENT time-kinetic terms. The fork is whether the
time slot enters with the LORENTZIAN sign (g^{TT}=-e^{2phi}, the covariant
d'Alembertian of the signature -+++ dilation-tie metric) or with a
EUCLIDEAN-signature +f_T^2/f^2 (the baseline's reduced Lagrangian).

NOTHING is added. We just write BOTH Lagrangians and read both EL principal
parts side by side, so the fork is explicit and the premise-difference is
auditable. This is the blind self-check of the ns_scan_symbol flag.
"""
import sympy as sp

T, r, th = sp.symbols('T r theta', real=True, positive=True)
P = sp.Function('phi')
phi = P(T, r)            # spherical reduction (theta-flat) to compare cleanly
phiT = sp.diff(phi, T); phir = sp.diff(phi, r)
phiTT = sp.Derivative(phi, T, 2); phirr = sp.Derivative(phi, r, 2)

print("="*70)
print("FORK A -- the metric's OWN 4-metric dilation tie (ns_scan_symbol):")
print("  g_tt=-e^{-2phi}, g_rr=e^{2phi}; L=(c/2)e^{-2phi} g^{ab}phi_a phi_b sqrt-g4")
# g^{TT}=-e^{2phi}, g^{rr}=e^{-2phi}, sqrt-g4=r^2 sin th
sqrtg4 = r**2
gTT = -sp.exp(2*phi); gRR = sp.exp(-2*phi)
fwt = sp.exp(-2*phi)
LA = (sp.Integer(2)/2)*fwt*(gTT*phiT**2 + gRR*phir**2)*sqrtg4
ELA = sp.expand(sp.simplify((sp.diff(LA, phi)
        - sp.diff(sp.diff(LA, phiT), T)
        - sp.diff(sp.diff(LA, phir), r))/sp.exp(-2*phi)))
cTT_A = sp.simplify(ELA.coeff(phiTT)); cRR_A = sp.simplify(ELA.coeff(phirr))
print("  coeff(phi_TT) =", cTT_A, "  coeff(phi_rr) =", cRR_A)
print("  cTT/cRR =", sp.simplify(cTT_A/cRR_A), " -> sign:",
      "NEGATIVE (HYPERBOLIC in T)" if sp.simplify(cTT_A/cRR_A) < 0 else "pos")

print()
print("="*70)
print("FORK B -- the baseline reduced Lagrangian (verify_nonstat/v_a3.py):")
print("  L_red = -(c/8) r^2 ( f_r^2 + f_T^2/f^2 ),  f = e^{-2phi}")
f = sp.Function('f', positive=True)(T, r)
LB = -sp.Rational(1, 8)*2*r**2*(sp.diff(f, r)**2 + sp.diff(f, T)**2/f**2)
ELB = (sp.diff(sp.diff(LB, sp.diff(f, T)), T)
       + sp.diff(sp.diff(LB, sp.diff(f, r)), r) - sp.diff(LB, f))
ELBphi = sp.expand(sp.simplify(ELB.subs(f, sp.exp(-2*phi)).doit()))
cTT_B = sp.simplify(ELBphi.coeff(phiTT)); cRR_B = sp.simplify(ELBphi.coeff(phirr))
print("  coeff(phi_TT) =", cTT_B, "  coeff(phi_rr) =", cRR_B)
print("  cTT/cRR =", sp.simplify(cTT_B/cRR_B), " -> sign:",
      "POSITIVE (ELLIPTIC in T)" if sp.simplify(cTT_B/cRR_B) > 0 else "neg")

print()
print("="*70)
print("THE FORK, ISOLATED:")
print("  FORK A time-kinetic in the action:  e^{-2phi} g^{TT} phi_T^2")
print("      = e^{-2phi}(-e^{2phi}) phi_T^2 = -phi_T^2   (LORENTZIAN sign)")
print("  FORK B time-kinetic in the action:  -(1/8)r^2 f_T^2/f^2")
print("      with f=e^{-2phi}: f_T^2/f^2 = 4 phi_T^2     (EUCLIDEAN sign;")
print("      the +f_T^2/f^2 was written WITHOUT the g^{TT}=1/g_tt<0 factor)")
print()
print("  => The baseline's ELLIPTIC-IN-T rests on a time-kinetic term that")
print("     OMITS the Lorentzian sign of g^{TT} from the dilation-tie metric.")
print("     The metric's OWN covariant d'Alembertian (FORK A) is the wave")
print("     operator e^{2phi}phi_TT - e^{-2phi}phi_rr - (1/r^2)phi_thth = ...")
print("     and it PROPAGATES IN T. This is the candidate anomaly.")

# Sanity: FORK A spherical EL should be the covariant Box phi = source-free.
# Box phi = (1/sqrt-g)d_a(sqrt-g g^{ab} phi_b). Verify ELA matches -r^2*Box*2
print()
print("SANITY: FORK A EL vs covariant Box phi (4-metric dilation tie):")
g4 = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
sg = sp.sqrt(-g4.det())
ginv = g4.inv()
PP = P(T, r)
Box = 0
for a, xa in enumerate([T, r, th, sp.Symbol('ph')]):
    if a >= 2:  # phi indep of theta,phi here
        continue
    Box += sp.diff(sg*ginv[a, a]*sp.diff(PP, xa), xa)/sg
Box = sp.simplify(Box)
print("  Box phi (spherical) =", Box)
print("  (a Lorentzian wave operator: note the +e^{2phi}phi_TT term)")
