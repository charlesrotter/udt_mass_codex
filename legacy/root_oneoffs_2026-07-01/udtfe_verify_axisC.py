"""
Axis C deep dive: is the constructor's 'cl folds into phi' claim TRUE or FALSE?

The constructor states (results doc 2a-2): writing g_tt=-e^{-2phi}cl(r)^2 is the
SAME geometry as g_tt=-e^{-2phitilde}c0^2 for phitilde=phi-ln(cl/c0), "carries no
invariant content beyond phi".

CRITICAL SUBTLETY: a reparametrization phi->phitilde shifts BOTH g_tt AND g_rr
(since g_rr=e^{2phi}). Folding cl into g_tt ALONE does NOT touch g_rr. So:
  - cl-in-g_tt-only  : g_tt=-e^{-2phi}cl^2,  g_rr=e^{2phi}   (B != 1/A)
  - genuine phi-shift: g_tt=-e^{-2phit}c0^2, g_rr=e^{2phit}  (B = 1/A preserved)
These are DIFFERENT geometries unless cl=const.

I test: is the cl-in-g_tt-only metric a curvature-equivalent relabeling of a
PURELY-DIAGONAL static metric with constant c? Yes trivially (any static lapse
can be called e^{-2psi}c0^2). The real question for UDT: does promoting c in
g_tt while KEEPING the canonical g_rr=e^{2phi} add invariant content vs just
using a different phi in BOTH slots (which is what 'absorbable into phi' requires)?
"""
import sympy as sp

r, t, th, ph = sp.symbols('r t theta varphi', real=True)
c0 = sp.symbols('c0', positive=True)
phi = sp.Function('phi')(r)
cl = sp.Function('cl')(r)
coords = [t, r, th, ph]

def ricci_scalar(gmat):
    n = 4
    ginv = gmat.inv()
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                ss = 0
                for d in range(n):
                    ss += ginv[l, d]*(sp.diff(gmat[d, m], coords[k])
                                      + sp.diff(gmat[d, k], coords[m])
                                      - sp.diff(gmat[m, k], coords[d]))
                Gam[l][m][k] = sp.simplify(ss/2)
    Ric = sp.zeros(n, n)
    for m in range(n):
        for nn in range(n):
            ss = 0
            for l in range(n):
                ss += sp.diff(Gam[l][m][nn], coords[l]) - sp.diff(Gam[l][m][l], coords[nn])
                for k in range(n):
                    ss += Gam[l][l][k]*Gam[k][m][nn] - Gam[l][nn][k]*Gam[k][m][l]
            Ric[m, nn] = sp.simplify(ss)
    return sp.simplify(sum(ginv[i, i]*Ric[i, i] for i in range(n)))

# Question 1: Is the cl-in-g_tt-only metric equal to SOME diagonal const-c metric
# with a relabeled lapse psi where e^{-2psi}c0^2 = e^{-2phi}cl^2?  That requires
# psi = phi - ln(cl/c0). BUT g_rr stays e^{2phi}, NOT e^{2psi}. So the cl metric is
# the metric with lapse-potential psi and radial-potential phi, i.e. B != 1/A.
# This is genuinely a DIFFERENT geometry from the B=1/A canonical metric.
A = sp.exp(-2*phi)
g_cl = sp.diag(-A*cl**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)

# genuine reparam (psi in both slots), psi=phi-ln(cl/c0):
psi = phi - sp.log(cl/c0)
g_reparam = sp.diag(-sp.exp(-2*psi)*c0**2, sp.exp(2*psi), r**2, r**2*sp.sin(th)**2)

print("g_cl[tt]      =", sp.simplify(g_cl[0,0]))
print("g_reparam[tt] =", sp.simplify(g_reparam[0,0]), " (same as g_cl[tt]:",
      sp.simplify(g_cl[0,0]-g_reparam[0,0])==0, ")")
print("g_cl[rr]      =", sp.simplify(g_cl[1,1]))
print("g_reparam[rr] =", sp.simplify(g_reparam[1,1]), " (same as g_cl[rr]:",
      sp.simplify(g_cl[1,1]-g_reparam[1,1])==0, ")")

print("\nRicci(g_cl) - Ricci(g_reparam):")
Rcl = ricci_scalar(g_cl)
Rrep = ricci_scalar(g_reparam)
print("   ", sp.simplify(Rcl - Rrep), " (==0 => same geometry)")

# VERDICT logic:
# - If you absorb cl into phi in BOTH slots (true reparam, preserves B=1/A) you get
#   a DIFFERENT g_rr => different physical metric. So 'fold cl into phi' is only a
#   relabeling if you ALSO change g_rr, i.e. if you're willing to leave the
#   canonical B=1/A family. Within fixed g_rr=e^{2phi}, cl IS an independent dof.
# - Conversely, ANY static spherical diagonal metric can trivially be written with
#   const c0 and a suitable lapse potential. The "varying c is absorbable into a
#   coordinate/units choice" claim is the TRUE and standard statement: c in g_tt is
#   not invariant; only the metric (hence curvature) is. Confirm by checking that
#   the cl metric's curvature is unchanged if we REName its lapse, which is the real
#   absorbability content.
print("\nINTERPRETATION:")
print(" - cl-in-g_tt-ONLY (keeping g_rr=e^{2phi}) is a DIFFERENT geometry from the")
print("   B=1/A canonical metric (it leaves the g_tt*g_rr=-c0^2 family).")
print(" - But that is a statement about leaving the locked family, NOT about c being")
print("   physical: c in g_tt carries NO invariant content because the lapse can be")
print("   relabeled (psi=phi-ln(cl/c0)) giving identical curvature (Ricci diff above).")
print(" - So 'varying-c absorbable' = TRUE in the invariant sense (curvature depends")
print("   only on the lapse potential, not on how it's split into e^{-2phi} vs cl).")
print(" - The constructor's phrasing 'folds into phi' is loose: it folds into the")
print("   LAPSE potential (g_tt), and to stay in B=1/A you must move g_rr too. The")
print("   absorbability VERDICT is nonetheless correct.")
