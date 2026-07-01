#!/usr/bin/env python3
"""
offdiagIII_derive.py -- THE CONTINUATION GATE of the off-diagonal scan.
=======================================================================
OFF-DIAGONAL ANGULAR ROW III. Driver: Claude (Opus 4.8, 1M). 2026-06-13.
Frame: CRITICAL_UNIVERSE_FRAME.md. METRIC-LED, data-blind. ANTI-INVENTION
(charter principle 1): we may NOT add a regularizer because it would help.
We ask ONLY whether the metric's OWN action contains a native term -- dropped
by the static single-cell C1 second-order truncation -- that (a) is active
where K_th<0 and (b) BOUNDS THE OPERATOR BELOW. A wrong-sign 2nd-order
coefficient is unbounded regardless of any potential V; the bounding term must
be HIGHER-DERIVATIVE (e.g. +(d_th^2 v)^2) or an equivalent native mechanism.

THE GATE established by #38 (build on it): the static single-cell C1
off-diagonal angular operator (q slaved on the metric's own EL, w=0 = the
static stationary point) is UNBOUNDED BELOW where the on-shell flip lives:
the RADIAL gradient drives K_th NEGATIVE on the formed-cell wall, basis-
independent (FEM + spectral diverge). The missing regularizer must be NATIVE
and previously-dropped.

THIS FILE = STEP 1 (DERIVE, anti-invention). It checks each NAMED suspect for
a native higher-derivative bounding term, with provenance, from the metric's
OWN action. It is the CPU sympy anchor; the convergence reproduction is in
offdiagIII_converge.py.

THE ACTION (the metric's own, full provenance): UDT_REBUILD.md sec.1 --
   S_phi = -(c/2) INT e^{-2phi} (d phi)^2 sqrt(-g4),  c=2,  PLUS the ON
   matter potential -Phi((1/2)e^{-2phi}+e^{phi}) sqrt(-g4).
THE METRIC IS phi (DEFINITIONAL, NOT Einstein-matter-sourced; B=1/A forces
G^t_t=G^r_r identically, the Einstein "source" is tautological). THERE IS NO
INDEPENDENT EINSTEIN-HILBERT R TERM in the action -- introducing one to mine a
curvature higher-derivative term would be an IMPORT (forbidden, principle 1).
"""
import sys, time
import sympy as sp
import numpy as np

_fh = open("/tmp/offdiagIII.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

log("=" * 78)
log("offdiagIII_derive -- STEP 1: native bounding term? (anti-invention)")
log("time", time.strftime("%Y-%m-%d %H:%M:%S"))
log("=" * 78)

# =====================================================================
# (0) THE ACTION + EXACT ANCHOR (reproduce K_th=-2.0326 with MY machinery,
#     before any suspect claim is trusted).
# =====================================================================
r_s, th_s, Phi_s = sp.symbols('r theta Phi', positive=True)
phi_s, q_s, w_s, pr_s, pth_s = sp.symbols('phi q w pr pth', real=True)
em2p = sp.exp(-2*phi_s); e2p = sp.exp(2*phi_s)
e2w = sp.exp(2*w_s); em2w = sp.exp(-2*w_s)
# full 4-metric with q=g_rth AND w=sphere-shape (areal scheme):
g = sp.Matrix([[-em2p, 0, 0, 0],
               [0, e2p, q_s, 0],
               [0, q_s, r_s**2*e2w, 0],
               [0, 0, 0, r_s**2*em2w*sp.sin(th_s)**2]])
gi = g.inv(); sqrtmg = sp.sqrt(-g.det())
grad = sp.Matrix([0, pr_s, pth_s, 0])
Kin = (grad.T*gi*grad)[0]
Lsrc = -Phi_s*(sp.Rational(1,2)*em2p + sp.exp(phi_s))
L = em2p*Kin*sqrtmg + Lsrc*sqrtmg     # the metric's OWN density, w live

# reduced density at w=0 (the static stationary point; CHECK 3 below justifies):
L0 = L.subs(w_s, 0)
fdq  = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,q_s), 'numpy')
fd2q = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,q_s,2),'numpy')
fHpp = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,pth_s,2),'numpy')
fHpq = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,pth_s,q_s),'numpy')

def qstar(rr, tt, ph, pr, pth, Phi=1.0):
    qv = 0.0
    for _ in range(400):
        F = float(fdq(rr,tt,Phi,ph,qv,pr,pth)); H = float(fd2q(rr,tt,Phi,ph,qv,pr,pth))
        if abs(F) < 1e-16 or abs(H) < 1e-16: break
        qv += -F/H
        if qv**2*np.exp(-2*ph) > 0.95*rr**2: qv *= 0.5
    return qv

def Kth_onshell(rr, tt, ph, pr, pth, Phi=1.0):
    qs = qstar(rr,tt,ph,pr,pth,Phi); W = rr**2*np.sin(tt)
    Hqq = float(fd2q(rr,tt,Phi,ph,qs,pr,pth))
    Hpp = float(fHpp(rr,tt,Phi,ph,qs,pr,pth)); Hpq = float(fHpq(rr,tt,Phi,ph,qs,pr,pth))
    return (Hpp - Hpq**2/Hqq)/W, qs, Hqq

log("\n(0) ANCHOR (my own machinery): phi=0.5 r=0.5 pr=8 pth=0.5 theta=1.0")
Kth, qs, Hqq = Kth_onshell(0.5, 1.0, 0.5, 8.0, 0.5)
log(f"    q*={qs:.5f}  Hqq={Hqq:.4f}(>0)  on-shell K_th={Kth:.5f}  (target -2.0326)")
assert abs(Kth-(-2.0326)) < 2e-3 and Hqq > 0, "ANCHOR FAILED"
log("    ANCHOR REPRODUCED. The on-shell wrong-sign K_th is real (build on #38).")

# =====================================================================
# SUSPECT (iii): CURVATURE / EH-REMAINDER higher-derivative term.
#   The action is PURE dilation-kinetic + algebraic potential. There is NO
#   sqrt(-g)R term. We CONFIRM the density carries NO second-or-higher
#   derivative of ANY field (so the EL is 2nd-order; no biharmonic native).
# =====================================================================
log("\n" + "="*70)
log("SUSPECT (iii): curvature / EH-remainder higher-derivative term?")
log("="*70)
# Build L with phi,q,w as FUNCTIONS to inspect derivative content of the density:
rF, thF = sp.symbols('r theta', positive=True)
phiF = sp.Function('phi')(rF, thF); qF = sp.Function('q')(rF, thF); wF = sp.Function('w')(rF, thF)
e2pF = sp.exp(2*phiF); em2pF = sp.exp(-2*phiF); e2wF = sp.exp(2*wF); em2wF = sp.exp(-2*wF)
gF = sp.Matrix([[-em2pF,0,0,0],[0,e2pF,qF,0],[0,qF,rF**2*e2wF,0],
                [0,0,0,rF**2*em2wF*sp.sin(thF)**2]])
giF = gF.inv(); sqrtmgF = sp.sqrt(-gF.det())
gradF = sp.Matrix([0, sp.diff(phiF,rF), sp.diff(phiF,thF), 0])
KinF = (gradF.T*giF*gradF)[0]
LF = em2pF*KinF*sqrtmgF - Phi_s*(sp.Rational(1,2)*em2pF+sp.exp(phiF))*sqrtmgF
derivs = LF.atoms(sp.Derivative)
orders = [sum(d.derivative_count for v,n in [(x,1) for x in [0]] for d in [dd]) for dd in []]  # noop
maxorder = 0
for d in derivs:
    tot = sum(n for v, n in d.variable_count)
    maxorder = max(maxorder, tot)
log(f"    Derivative atoms in the density L: {sorted(str(d) for d in derivs)}")
log(f"    HIGHEST derivative order present in L = {maxorder}  (1 = first-order only)")
log("    => The density is FIRST-ORDER in field gradients. Its EL is at most")
log("       SECOND-ORDER. There is NO native higher-derivative (biharmonic)")
log("       term in the action. A curvature/R^2 term would be an IMPORT.")
log("    VERDICT (iii): NO native higher-derivative bounding term. The metric")
log("       IS phi (B=1/A); the Einstein source is tautological; mining an")
log("       independent EH/Kretschmann term is forbidden by principle 1.")
assert maxorder == 1, "density carries higher derivatives -- re-examine!"

# =====================================================================
# SUSPECT (ii): the phi-angular cross coupling dpr x dpth ~ phi0_r phi0_th.
#   Charles's hunch, named by angular_completeness as the first phi-angular
#   operator coupling. IS IT higher-derivative, or 2nd-order? A 2nd-order
#   cross term CANNOT bound a wrong-sign 2nd-order Laplacian.
# =====================================================================
log("\n" + "="*70)
log("SUSPECT (ii): phi-angular cross coupling dpr x dpth ~ phi0_r phi0_th?")
log("="*70)
# The Hessian of L0 in (pr,pth) is the radial-angular block. The cross term is
# d^2 L0/(dpr dpth). It multiplies (d_r u)(d_th u) in the fluctuation operator
# -- a FIRST-derivative x FIRST-derivative term: 2nd order, NOT higher.
fHrp = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,pr_s,pth_s),'numpy')
qs2 = qstar(0.5,1.0,0.5,8.0,0.5)
cross = float(fHrp(0.5,1.0,1.0,0.5,qs2,8.0,0.5))
log(f"    d^2 L0/(d pr d pth) at the anchor = {cross:.4f}")
log("    This multiplies (d_r u)(d_th u) -- a FIRST x FIRST derivative product.")
log("    DERIVATIVE ORDER = 2 (a mixed 2nd-order term). It modifies the")
log("    principal SYMBOL of the 2nd-order operator; it CANNOT bound a")
log("    wrong-sign 2nd-order angular Laplacian (a higher-derivative term is")
log("    required for that). It enters the SAME order as the pathology.")
log("    VERDICT (ii): real and native, but 2nd-ORDER -- NOT a bounding term.")
log("    (It is part of WHY K_th flips, not a cure: the radial gradient enters")
log("     K_th through exactly this q-channel cross-response.)")

# =====================================================================
# SUSPECT (i): w as a field with a native gradient term (subagent-confirmed).
#   Re-anchor the DECISIVE fact here: L carries NO derivative of w.
# =====================================================================
log("\n" + "="*70)
log("SUSPECT (i): w (sphere-shape) gradient / higher-derivative term?")
log("="*70)
w_derivs = [d for d in derivs if d.expr == wF or (hasattr(d.expr,'func') and d.expr==wF)]
has_wderiv = LF.has(sp.Derivative(wF, rF)) or LF.has(sp.Derivative(wF, thF))
has_qderiv = LF.has(sp.Derivative(qF, rF)) or LF.has(sp.Derivative(qF, thF))
log(f"    L contains a derivative of w: {has_wderiv}")
log(f"    L contains a derivative of q: {has_qderiv}")
log("    => w (and q) enter the density ONLY ALGEBRAICALLY (no gradient).")
log("    A field absent from L as a gradient CANNOT supply ANY gradient or")
log("    higher-derivative term at ANY order of fluctuation expansion")
log("    (expansion differentiates in the FIELD, never manufactures a")
log("    coordinate-derivative the density lacks). Cubic-order w (the")
log("    angular_completeness entry) is an ALGEBRAIC cubic coupling, not a")
log("    kinetic term -- confirmed to eps^3 in /tmp/offdiagIII_wcubic.py.")
# w-stiffness sign at the static stationary point (the Schur shift is bounded):
fLww = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,w_s,pr_s,pth_s), sp.diff(L,w_s,2),'numpy')
Lww = float(fLww(0.5,1.0,1.0,0.5,qs2,0.0,8.0,0.5))
log(f"    L_ww at w=0 (static stationary point) = {Lww:.4f}")
log("    => w is a STIFF ALGEBRAIC (mass) direction. Schur-eliminating it")
log("    shifts the 2nd-order coefficients by a BOUNDED algebraic amount; it")
log("    can NEVER introduce a +(d^2 u)^2 higher-derivative term, so it cannot")
log("    bound the wrong-sign Laplacian. (At w=0 the joint (q,w) Schur EQUALS")
log("    the q-only Schur: K_th stays -2.033 -- verifier-banked, reproduced.)")
assert not has_wderiv and not has_qderiv
log("    VERDICT (i): NO native w-gradient term. w is algebraically stiff;")
log("       its Schur contribution is bounded. NO bounding term from w.")

# =====================================================================
# SUSPECT (iv): the seal area-form (#36) -- bulk-bounding or only a BC?
#   (Subagent /tmp/offdiagIII_sealbound.py: a maximal boundary term does NOT
#    bound the bulk wrong-sign Laplacian; #36 is bulk-invisible by Stokes.)
# =====================================================================
log("\n" + "="*70)
log("SUSPECT (iv): seal area-form #36 -- does it bound the BULK operator?")
log("="*70)
log("    #36 (registry, its own words): d ln f ^ omega_H1 = d[(ln f) omega_H1]")
log("    is an EXACT BOUNDARY TRANSGRESSION, 'invisible to the bulk EL',")
log("    delivered AT THE CLOSURE. By Stokes an exact bulk integrand reduces")
log("    to a pure BOUNDARY integral => ZERO contribution to the bulk EL =>")
log("    it cannot modify the bulk K_th or add a bulk higher-derivative term.")
log("    NUMERICAL PROOF (/tmp/offdiagIII_sealbound.py): the bulk wrong-sign")
log("    Laplacian's lam0 -> -inf is driven by HIGH-FREQUENCY INTERIOR modes")
log("    that vanish at the endpoints; even the MAXIMAL boundary term")
log("    (Dirichlet, alpha->inf) leaves lam0 bit-identical -> -inf. A pure BC")
log("    CANNOT bound a bulk wrong-sign Laplacian. #37 confirms the area form")
log("    is sigma-even, EXACT, adds no bulk higher-derivative structure.")
log("    VERDICT (iv): #36 enters as a BOUNDARY datum only -- NOT a bulk")
log("       regularizer. It does not bound the operator.")

# =====================================================================
# STEP-1 CONSOLIDATED VERDICT
# =====================================================================
log("\n" + "#"*70)
log("STEP-1 CONSOLIDATED VERDICT (anti-invention):")
log("  The metric's OWN action -- pure dilation-kinetic + algebraic potential,")
log("  the metric IS phi, NO independent EH/curvature term -- supplies NO")
log("  native HIGHER-DERIVATIVE (or equivalent) term, dropped by the static")
log("  single-cell C1 truncation, that bounds the wrong-sign angular operator")
log("  below in the K_th<0 region:")
log("    (i)   w-gradient:        ABSENT (w algebraic at all orders; stiff mass,")
log("                             bounded Schur shift). NO.")
log("    (ii)  phi-angular cross: PRESENT but 2nd-ORDER (same order as the")
log("                             pathology; part of its cause). NOT bounding.")
log("    (iii) curvature/EH:      ABSENT from the action (density 1st-order in")
log("                             gradients; EL 2nd-order). Mining one = IMPORT.")
log("    (iv)  seal area-form:    BOUNDARY-only (#36 bulk-invisible; Dirichlet")
log("                             does not bound the bulk). NOT bounding.")
log("  => NO native bounding term in the static single-cell C1 class.")
log("  This is the honest, valuable answer (STEP 3): the static single-cell")
log("  class genuinely CANNOT host the completion. The particle question moves")
log("  to the CLOSED-CELL(#36 as the WHOLE)/NONSTATIONARY(C-2026-06-13-1)")
log("  WHOLE -- a domino, NOT a failure, and NOT a license to invent a term.")
log("#"*70)
_fh.close()
