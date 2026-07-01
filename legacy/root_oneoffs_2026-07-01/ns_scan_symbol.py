#!/usr/bin/env python3
"""
ns_scan_symbol.py -- the NONSTATIONARY whole-metric field equation, EXACT
=========================================================================
NS-SCAN push (queue-head step b, NONSTATIONARY axis). Driver: Claude
(Opus 4.8). Date 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md. New file.

GOAL: derive the metric's OWN time-dependent dilation field equation with
BOTH sectors live (radial-phi AND the e^{2phi}-dressed angular operator
with the -phi_th^2 nonlinearity), the time row ON, NOTHING added/slaved/
frozen. Then read its PRINCIPAL SYMBOL across the regime: is the (T,r,theta)
operator ELLIPTIC everywhere (registry #22 baseline: "no sector propagates
hyperbolically in T", elliptic-in-T, Hadamard-ill-posed Cauchy), or does
the CHARACTER CHANGE (a region where the symbol becomes hyperbolic in T,
i.e. T turns timelike) once BOTH sectors are live with the ON source?

This is the SYMBOLIC anchor (CPU sympy, exact). The GPU scan (ns_scan_gpu)
maps it numerically across the nonstationary whole-metric solution space.

The C1 dilation action, time row LIVE (the metric's OWN, symcheck-derived):
  L = (c/2) e^{-2phi} g^{ab} phi_a phi_b sqrt(-g4),  c = 2.
4-metric (dilation tie, areal canon): g_tt = -e^{-2phi}, g_rr = e^{2phi},
  g_thth = r^2, g_phph = r^2 sin^2 th.  sqrt(-g4) = r^2 sin th (e^{+-2phi}
  cancel between g_tt and g_rr).  phi = phi(T, r, theta).
This EXTENDS wint_symcheck.py (which froze the time row) by turning it on.
"""
import sympy as sp

PASS = []
def check(n, c):
    ok = bool(c); PASS.append((n, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}", flush=True)

T, r, th = sp.symbols('T r theta', real=True)
P = sp.Function('phi')
phi = P(T, r, th)

# 4-metric (dilation tie). The TIME ROW IS ON: g_tt = -e^{-2phi}.
gtt = -sp.exp(-2 * phi)
grr = sp.exp(2 * phi)
gthth = r**2
gphph = r**2 * sp.sin(th)**2
# inverse diagonal:
gTT = 1 / gtt          # = -e^{2phi}
gRR = 1 / grr          # =  e^{-2phi}
gThTh = 1 / gthth      # =  1/r^2
# theta in (0,pi) so sin th > 0; declare it to avoid Abs() from sqrt:
sqrtg4 = r**2 * sp.sin(th)  # = sqrt(-g4); dilation weights cancel (verified
                            # in wint_symcheck.py); time row on does not change
                            # this since g_tt*g_rr = -1.
check("sqrt(-g4) = r^2 sin th (g_tt g_rr=-1; dilation weights cancel)",
      sp.simplify(-(gtt * grr * gthth * gphph) - sqrtg4**2) == 0)

# C1 dilation kinetic scalar, time row on:
fwt = sp.exp(-2 * phi)
K = (gTT * sp.diff(phi, T)**2 + gRR * sp.diff(phi, r)**2
     + gThTh * sp.diff(phi, th)**2)
L = (sp.Integer(2) / 2) * fwt * K * sqrtg4

phiT = sp.diff(phi, T); phir = sp.diff(phi, r); phith = sp.diff(phi, th)
EL = (sp.diff(L, phi)
      - sp.diff(sp.diff(L, phiT), T)
      - sp.diff(sp.diff(L, phir), r)
      - sp.diff(sp.diff(L, phith), th))
# normalize by the common dilation weight e^{-2phi} (>0), as in symcheck:
EL = sp.simplify(EL / sp.exp(-2 * phi))

# Build the EXPECTED form: the static symcheck gave (per -2 sin th):
#   r^2 e^{-2phi}( phi_rr + (2/r)phi_r - 2 phi_r^2 ) + (phi_thth + cot phi_th - phi_th^2)
# The time row adds a g^{TT} e^{-2phi} kinetic piece. g^{TT} = -e^{2phi};
# the C1 weight on the time kinetic is e^{-2phi} * g^{TT} = e^{-2phi}*(-e^{2phi})
# = -1, so the time second-derivative coefficient is structurally DIFFERENT
# from the radial e^{-2phi}*g^{rr}=e^{-2phi}*e^{-2phi}=e^{-4phi}. We let sympy
# tell us the exact EL and then READ the principal symbol.
phiTT = sp.Derivative(phi, T, 2)
phirr = sp.Derivative(phi, r, 2)
phithh = sp.Derivative(phi, th, 2)
cot = sp.cos(th) / sp.sin(th)

# Extract the coefficients of the three SECOND derivatives (principal part).
# EL still carries the |sin th| weight; divide it out first (sin th>0).
EL = sp.simplify(EL / sp.sin(th))
ELx = sp.expand(EL)
def coeff_of(expr, der):
    return sp.simplify(expr.coeff(der))
cTT = coeff_of(ELx, phiTT)
cRR = coeff_of(ELx, phirr)
cThTh = coeff_of(ELx, phithh)
print("\nPRINCIPAL-PART coefficients of EL (time row ON):")
print("  coeff(phi_TT)   =", cTT)
print("  coeff(phi_rr)   =", cRR)
print("  coeff(phi_thth) =", cThTh)

# remainder (lower order: first derivatives, squares, source-free C1):
rem = sp.simplify(ELx - cTT * phiTT - cRR * phirr - cThTh * phithh)
print("  lower-order remainder =", rem)

# THE PRINCIPAL SYMBOL: replace d_T->i kT, d_r->i kr, d_th->i kth (mod sign).
# For a 2nd-order operator sum c_a phi_aa, the symbol is -(cTT kT^2 + cRR kr^2
# + cThTh kth^2). The TYPE is set by the SIGNS of cTT, cRR, cThTh:
#   all same sign  -> ELLIPTIC (no real characteristics; #22 baseline)
#   cTT opposite to spatial -> HYPERBOLIC in T (T propagates; CHANGE OF
#   CHARACTER -- a departure from the baseline).
print("\nSIGN STRUCTURE (the type test):")
print("  sign reading is on cTT vs (cRR, cThTh).")
# factor out a positive common weight to compare signs cleanly:
print("  cTT/cRR     =", sp.simplify(cTT / cRR))
print("  cTT/cThTh   =", sp.simplify(cTT / cThTh))
print("  cRR/cThTh   =", sp.simplify(cRR / cThTh))

# The decisive ratio cTT/cRR: if NEGATIVE, T and r enter with OPPOSITE signs
# => hyperbolic (Lorentzian) principal part => T PROPAGATES. If POSITIVE =>
# elliptic, baseline holds.
ratio = sp.simplify(cTT / cRR)
print("\n  ==> cTT/cRR =", ratio,
      "  (NEGATIVE => hyperbolic-in-T = CHANGE OF CHARACTER vs #22;",
      "POSITIVE => elliptic = baseline holds)")

n = sum(1 for _, ok in PASS if ok)
print(f"\nNS_SCAN_SYMBOL: {n}/{len(PASS)} structural checks PASS")
