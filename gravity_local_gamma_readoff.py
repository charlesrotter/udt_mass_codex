"""
gravity_local_gamma_readoff.py (2026-06-18)
Clean PPN gamma read-off from the linearized solutions found in
gravity_local_ppn_direct.py.

Metric (areal): g_tt = -A c0^2, g_rr = B, A=1+a, B=1+b, a=alpha/r, b=beta/r.

PPN standard form (areal/Schwarzschild coords):
  g_tt = -(1 - 2U + ...),   g_rr = 1 + 2 gamma U + ...
with U = +GM/(r c^2) > 0 the Newtonian potential magnitude.

So:  A = 1 - 2U  => a = alpha/r = -2U  => U = -alpha/(2r), need alpha<0 (attractive).
     B = 1 + 2 gamma U => b = beta/r = 2 gamma U = 2 gamma (-alpha/2r) = -gamma alpha / r
     => beta = -gamma alpha  => gamma = -beta/alpha.
"""
import sympy as sp
al, be = sp.symbols('alpha beta')

def gamma_of(rel_beta_in_alpha):
    # rel: beta = rel_beta_in_alpha (expression in al)
    g = sp.simplify(-rel_beta_in_alpha/al)
    return g

# GR:  alpha = -beta  -> beta = -alpha
print("GR:   beta = -alpha   => gamma =", gamma_of(-al), " (expect 1)")
# Honest: alpha = -beta/9  -> beta = -9 alpha
print("Honest f(phi)R: beta = -9 alpha => gamma =", gamma_of(-9*al), " (PPN gamma)")
print()
g_udt = gamma_of(-9*al)
print("PPN gamma (honest UDT f(phi)R, static SSS weak field) =", g_udt)
print("|gamma - 1| =", abs(g_udt-1))
print("Cassini bound |gamma-1| < 2.3e-5.  Violation factor =", float(abs(g_udt-1)/2.3e-5))
print()
print("Light bending / Shapiro scale as (1+gamma)/2 vs GR's 1:")
print("  (1+gamma)/2 =", (1+g_udt)/2, " => light bending =", float((1+g_udt)/2), "x GR value")
print("  GR light bending 1.7517 arcsec -> UDT predicts", float((1+g_udt)/2*1.7517), "arcsec.")
print("  Cassini measured (1+gamma)/2 = 1.0000 +/- 1.1e-5.")
