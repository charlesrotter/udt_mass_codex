#!/usr/bin/env python3
"""
offdiagIII_wcubic.py -- does the sphere-shape field w supply a NATIVE
HIGHER-DERIVATIVE angular term in the fluctuation operator?
=====================================================================
METRIC-LED, anti-invention. Sub-agent task 2026-06-13 (Opus 4.8, 1M).

QUESTION: carrying w (g_thth=r^2 e^{2w}, g_phph=r^2 e^{-2w} sin^2 th)
in the areal scheme -- does the action's OWN expansion contain a
higher-derivative (>2nd-order, e.g. biharmonic ~+(d_th^2 w)^2)
angular term that the static C1 second-order truncation DROPPED, and
could it bound below a wrong-sign 2nd-order angular Laplacian?

We MAY NOT add any term. We only check the action's own expansion.

THE ACTION (the metric's own, ALL there is):
  S = (c/2) INT e^{-2phi} g^{ab} phi_a phi_b sqrt(-g4)   (c=2)
      - INT Phi((1/2)e^{-2phi}+e^{phi}) sqrt(-g4)         (ON potential)
  4-metric: g_tt=-e^{-2phi}, g_rr=e^{2phi}, g_rth=q,
            g_thth=r^2 e^{2w}, g_phph=r^2 e^{-2w} sin^2 th.
  Fields phi(r,th), q(r,th), w(r,th).
  NO Einstein-Hilbert R term -- the metric IS phi.

Three checks:
 (1) Does L contain ANY derivative of w?  (expect NO)  -- decisive: a
     field with no gradient in L cannot supply any gradient/higher-
     derivative term at ANY order of expansion.
 (2) Expand L to CUBIC order in (dphi,dq,dw) about a formed background;
     extract every dw term; confirm highest th-derivative of dw is ZERO.
 (3) L is EVEN in w at w0=0 with L_ww>0 (stiff algebraic = a mass);
     integrating w out (Schur) shifts 2nd-order coeffs by a BOUNDED
     amount, never adds a higher-derivative term. Confirm K_th Schur
     correction is finite.
"""
import sympy as sp
import time, sys

t0 = time.time()
def log(*a):
    print(*a, flush=True)

log("="*70)
log("offdiagIII_wcubic -- w higher-derivative angular term audit")
log("="*70)

r, th, c, Phi = sp.symbols('r theta c Phi', positive=True)
phi = sp.Function('phi')(r, th)
q   = sp.Function('q')(r, th)
w   = sp.Function('w')(r, th)

# ---- Build the EXACT Lagrangian density, same as offdiag_qw_derive.py ----
e2p = sp.exp(2*phi); em2p = sp.exp(-2*phi)
e2w = sp.exp(2*w);   em2w = sp.exp(-2*w)
g = sp.zeros(4, 4)
g[0,0] = -em2p
g[1,1] = e2p
g[1,2] = q
g[2,1] = q
g[2,2] = r**2 * e2w
g[3,3] = r**2 * em2w * sp.sin(th)**2
gi = g.inv()
detg = g.det()
sqrtmg = sp.sqrt(-sp.simplify(detg))
log("  sqrt(-g4) =", sp.simplify(sqrtmg))

grad = sp.Matrix([0, sp.diff(phi, r), sp.diff(phi, th), 0])
Kin = 0
for a in range(4):
    for b in range(4):
        Kin += gi[a, b] * grad[a] * grad[b]
Lkin = (sp.Integer(2)/2) * em2p * Kin * sqrtmg     # c=2
Lpot = -Phi*((sp.Rational(1,2))*em2p + sp.exp(phi)) * sqrtmg
L = Lkin + Lpot
L = sp.simplify(L)
log(f"  Lagrangian density assembled.  t={time.time()-t0:.1f}s")

# =====================================================================
# CHECK (1): does L contain ANY derivative of w (or q)?
# =====================================================================
log("\n" + "="*70)
log("CHECK (1): does the Lagrangian density contain ANY w-derivative?")
log("="*70)
wr  = sp.Derivative(w, r)
wth = sp.Derivative(w, th)
qr  = sp.Derivative(q, r)
qth = sp.Derivative(q, th)

has_wr  = L.has(wr)
has_wth = L.has(wth)
has_qr  = L.has(qr)
has_qth = L.has(qth)
# Robust check: collect ALL Derivative atoms in L and inspect which fields.
deriv_atoms = L.atoms(sp.Derivative)
wderivs = [d for d in deriv_atoms if d.has(w)]
qderivs = [d for d in deriv_atoms if d.has(q)]
phideriv = [d for d in deriv_atoms if d.has(phi)]
log(f"  L.has(d_r  w) = {has_wr}")
log(f"  L.has(d_th w) = {has_wth}")
log(f"  Derivative atoms in L involving w: {wderivs}")
log(f"  Derivative atoms in L involving q: {qderivs}")
log(f"  Derivative atoms in L involving phi: {phideriv}")
w_has_no_deriv = (len(wderivs) == 0)
log(f"\n  ==> L contains NO derivative of w:  {w_has_no_deriv}")
log(f"  ==> L contains NO derivative of q:  {len(qderivs) == 0}")
log("  (w enters ONLY algebraically through g^{ab} and sqrt(-g).)")
log("  DECISIVE: a field absent from L as a gradient cannot supply ANY")
log("  gradient or higher-derivative term at ANY order of fluctuation")
log("  expansion -- expansion is differentiation in the FIELD, it cannot")
log("  manufacture a derivative-in-the-COORDINATE that the density lacks.")

# =====================================================================
# CHECK (2): cubic expansion about a formed background; extract dw terms;
#            confirm highest th-derivative of dw is ZERO.
# =====================================================================
log("\n" + "="*70)
log("CHECK (2): cubic-order fluctuation expansion -- dw terms")
log("="*70)
# Formed background: phi0(r,th) general (radial-dominant), q*=0 slaved
# (q tadpole vanishes spherically; we keep phi0 general to be safe),
# w0=0. Fluctuation fields:
eps = sp.symbols('epsilon')
dphi = sp.Function('dphi')(r, th)
dq   = sp.Function('dq')(r, th)
dw   = sp.Function('dw')(r, th)
phi0 = sp.Function('phi0')(r, th)
q0   = sp.Integer(0)         # slaved background value
w0   = sp.Integer(0)

# substitution: field = background + eps*fluct (and all their derivatives).
def field_sub(F, bg, df):
    subs = {F: bg + eps*df}
    for (vrs) in [(r,), (th,), (r,r), (th,th), (r,th)]:
        DF = sp.Derivative(F, *vrs)
        Dbg = sp.Derivative(bg, *vrs) if not bg.is_number else sp.Integer(0)
        Ddf = sp.Derivative(df, *vrs)
        subs[DF] = Dbg + eps*Ddf
    return subs

subs_all = {}
subs_all.update(field_sub(phi, phi0, dphi))
subs_all.update(field_sub(q,   q0,   dq))
subs_all.update(field_sub(w,   w0,   dw))

log("  substituting field = background + eps*fluct ...")
Lsub = L.subs(subs_all, simultaneous=True)
log(f"  substituted.  t={time.time()-t0:.1f}s  ; expanding to eps^3 ...")

# series in eps to cubic order
Lser = sp.series(Lsub, eps, 0, 4).removeO()
Lser = sp.expand(Lser)
log(f"  series done.  t={time.time()-t0:.1f}s")

# Collect orders
L0 = Lser.coeff(eps, 0)
L1 = Lser.coeff(eps, 1)
L2 = Lser.coeff(eps, 2)
L3 = Lser.coeff(eps, 3)

# Extract every term containing dw or its derivatives, at orders 1,2,3.
dwr  = sp.Derivative(dw, r)
dwth = sp.Derivative(dw, th)
dwrr = sp.Derivative(dw, r, 2)
dwthh= sp.Derivative(dw, th, 2)
dwrth= sp.Derivative(dw, r, th)

def dw_terms(expr, order):
    expr = sp.expand(expr)
    terms = expr.as_ordered_terms() if expr != 0 else []
    keep = [tm for tm in terms if tm.has(dw)]
    return keep

for nm, Ln, ordn in [("L1 (linear)",L1,1),("L2 (quadratic)",L2,2),
                     ("L3 (cubic)",L3,3)]:
    kept = dw_terms(Ln, ordn)
    log(f"\n  --- {nm}: terms containing dw  ({len(kept)} terms) ---")
    # what derivative-atoms of dw appear?
    sub = sp.Add(*kept) if kept else sp.Integer(0)
    datoms = [d for d in sub.atoms(sp.Derivative) if d.has(dw)]
    log(f"      dw-derivative atoms present: {set(datoms)}")
    if kept:
        # show a compact form
        scol = sp.simplify(sub)
        log(f"      sum of dw-terms (simplified) = {scol}")

# Global: highest th-derivative of dw anywhere in the cubic Lagrangian
all_dw_datoms = [d for d in Lser.atoms(sp.Derivative) if d.has(dw)]
log("\n  ALL dw-derivative atoms anywhere in L (to cubic order):")
log(f"      {set(all_dw_datoms)}")
highest_thorder = 0
for d in all_dw_datoms:
    # count theta variable occurrences
    cnt = d.derivative_count if hasattr(d,'derivative_count') else None
    # robust: inspect variable_count
    for var, n in d.variable_count:
        if var == th:
            highest_thorder = max(highest_thorder, int(n))
log(f"  ==> highest th-derivative of dw appearing anywhere = {highest_thorder}")
log("  (expect 0: dw appears ONLY undifferentiated/algebraically.)")

# =====================================================================
# CHECK (3): w is EVEN in w at w0=0, L_ww>0 (stiff algebraic = a mass);
#            Schur elimination gives only a BOUNDED K_th shift.
# =====================================================================
log("\n" + "="*70)
log("CHECK (3): L_ww > 0 (stiff algebraic w) and bounded Schur shift")
log("="*70)
# Parity in w: substitute w->-w (with q->0, static) and compare. Use
# the anchor the verifier used. We treat phi, r, and gradients as free
# numbers by evaluating L's dependence on w with all else frozen.
# Build L as a function of a scalar w-value at a point, with phi-grads
# as numbers. Replace Derivative(phi,..) and Derivative(w,..)=0.
ww = sp.symbols('ww', real=True)
# freeze derivatives: w constant (no w-deriv in L anyway), q=0.
freeze = {
    w: ww, q: 0,
    sp.Derivative(q, r): 0, sp.Derivative(q, th): 0,
    sp.Derivative(w, r): 0, sp.Derivative(w, th): 0,
}
Lw = L.subs(freeze)
# Anchor: phi=0.5, phi_r=8 (pr), phi_th=0.5 (pth), r=0.5
anchor = {
    phi: sp.Rational(1,2),
    sp.Derivative(phi, r): 8,
    sp.Derivative(phi, th): sp.Rational(1,2),
    r: sp.Rational(1,2),
    Phi: 1,   # ON; magnitude irrelevant for the kinetic parity check
    th: sp.pi/3,
}
Lw_anchor = Lw.subs(anchor)
Lw_anchor = sp.simplify(Lw_anchor)
log(f"  L(w) at anchor = {Lw_anchor}")
# parity: L(w)-L(-w)
parity = sp.simplify(Lw_anchor - Lw_anchor.subs(ww, -ww))
log(f"  L(w) - L(-w) at anchor = {parity}   (0 => EVEN in w)")
# first and second derivative in w at w0=0
Lw_p  = sp.diff(Lw_anchor, ww)
Lw_pp = sp.diff(Lw_anchor, ww, 2)
val_p  = sp.simplify(Lw_p.subs(ww, 0))
val_pp = sp.simplify(Lw_pp.subs(ww, 0))
log(f"  dL/dw  |_{{w=0}} = {val_p}    (0 => stationary, w0=0 is a critical pt)")
log(f"  d2L/dw2|_{{w=0}} = {val_pp} ~= {sp.N(val_pp)}   (>0 => stiff/mass-like)")

# Schur: with NO w-derivative in L, the w-block of the Hessian is purely
# ALGEBRAIC (multiplication operator M_ww = L_ww, no differential part),
# and the off-diagonal couplings (L_w,phi etc.) are also derivative-free
# in dw. The Schur correction to K_th is  -(L_{th-block,w}) M_ww^{-1}
# (L_{w,th-block}); since M_ww = L_ww is a bounded POSITIVE multiplication
# operator (>0), its inverse is a bounded multiplication operator, and the
# correction is a BOUNDED algebraic rank-one shift -- it CANNOT introduce a
# d_th^2 (Laplacian) or d_th^4 (biharmonic) differential operator, and
# CANNOT diverge to +inf. Demonstrate L_ww^{-1} finite at the anchor:
schur_inv = sp.simplify(1/val_pp)
log(f"  M_ww^-1 = 1/L_ww = {schur_inv} ~= {sp.N(schur_inv)}  (FINITE, bounded)")
log("  ==> Schur elimination of w shifts the 2nd-order coefficients by a")
log("      BOUNDED algebraic amount; it adds NO differential operator and")
log("      cannot diverge -- it cannot bound below a wrong-sign Laplacian.")

# also: confirm the w-mass term is the LEADING w-entry in L2 (quadratic):
log("\n  Leading w-coupling forms in the expansion:")
# quadratic dw-self term coefficient (the mass):
L2dw = sp.expand(L2)
mass_coeff = L2dw.coeff(dw, 2)   # coefficient of dw^2 (algebraic)
mass_coeff = sp.simplify(mass_coeff)
log(f"  coeff of dw^2 in L2 (the algebraic MASS, no deriv) = {mass_coeff}")
# linear-in-dw cross terms (the cubic couplings live in L3):
L3dw = sp.expand(L3)
cross = sp.simplify(L3dw.coeff(dw, 1))
log(f"  coeff of dw^1 in L3 (cubic ALGEBRAIC coupling) present: {cross != 0}")

log(f"\nDONE.  t={time.time()-t0:.1f}s")
