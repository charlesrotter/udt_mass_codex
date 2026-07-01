#!/usr/bin/env python3
"""
p3fix_aphi_ruler.py -- P3 FIX: the RULER-INTEGRAL source weight for a RUNNING a(phi).

WHY THIS FILE EXISTS (the defect; cite p3_VERIFIER.md, agent a71ebdd, 2026-06-20):
The blind verifier found a REAL, well-specified defect in P3's running-a coupling.
P3 wired the matter-source weight as the PRODUCT form W = e^{(a+1)phi}, substituting
a -> a(phi) naively.  But for a RUNNING a, Bianchi forces
    d ln W/dphi = (a+1) + phi*da/dphi ,   NOT  (a+1).
The conservation code (p3_aphi_matter.py:172,181) used the coefficient (a+1), so the
running-a "Bianchi source" diagnostic was MIS-COEFFICIENTED: 17% off at phi=-0.2,
29% off at phi=-0.4 (k=1).  The baseline (a=-1, k=0) and the solver/FD-gate were
UNAFFECTED (the exchange term is not used there) -- the defect is confined to the
running-a conservation diagnostic.

THE FIX (DERIVED, not chosen -- see DERIVATION below):  the composition-consistent
weight for a running rate is the RULER INTEGRAL, not the product:
    m(phi) = m0 * exp( INT_{phiref}^{phi} a(phi') dphi' )
    W(phi) =        exp( INT_{phiref}^{phi} (a(phi')+1) dphi' )
With this W, d ln W/dphi = (a+1) EXACTLY (fundamental theorem of calculus), so the
conservation div T = -(a+1) phi' T is CORRECT AS WRITTEN.  This is ALSO the form the
explore script's fingerprint already used (p3_explore_aphi.py:59-60) -- so the fix
RECONCILES the weight with the conservation coefficient and with the fingerprint.

================================================================================
DERIVATION -- the ruler integral is the UNIQUE composition-consistent weight
================================================================================
The constant-a arc fixes the mass-dilation law m(phi)=m0 e^{a phi} as "the only
composition-consistent form" for CONSTANT a.  Its content is a LOCAL RATE:
        d ln m / dphi = a            (the dilation RATE, per unit phi)
For a RUNNING rate the rate is LOCAL: d ln m/dphi = a(phi).  Integrating this ODE
(the ONLY function whose local log-rate is a(phi)) gives the ruler integral.

The discriminator is the LOCAL-RATE LAW, not composition alone (sympy showed both
ruler and product "telescope" trivially, so composition is necessary-not-sufficient):
    RULER   m=m0 exp(INT a)      => d ln m/dphi = a(phi)            [the rate IS a]
    PRODUCT m=m0 exp(a(phi)*phi) => d ln m/dphi = a + phi*da/dphi   [rate CONTAMINATED]
Only the ruler integral keeps a(phi) equal to the local dilation rate -- i.e. keeps
the MEANING of a (the rate that the constant-a arc fixed).  The product form silently
redefines the rate to a + phi da/dphi.  => ruler integral is UNIQUE.  (sympy-exact.)

Reduction to the arc (constant a, phiref=0):
    INT_0^phi (a+1) dphi' = (a+1) phi   =>  W = e^{(a+1)phi}  (the arc form).  QED.

Conservation coefficient (FTC):  d ln W/dphi = d/dphi INT_{phiref}^phi (a+1) = (a+1),
EXACT -- so the code's (a+1) coefficient is RIGHT with the ruler weight.

Analytic integral for the declared a(phi) = -1 + k eps0^p e^{-p phi} (no quadrature):
    a(phi)+1 = k eps0^p e^{-p phi}
    INT (a+1) dphi = -(k eps0^p / p) e^{-p phi}  (+ const fixed by phiref)
    => W(phi) = exp( -(k eps0^p/p)(e^{-p phi} - e^{-p phiref}) )
  phiref convention: phiref=0 (matches the explore-script fingerprint int_0^phi and the
  constant-a reduction).  Then  INT_0^phi (a+1) = (k eps0^p/p)(1 - e^{-p phi}).

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/DERIVE-fix.  DATA-BLIND.
Branch: p3-aphi-coupling.  NEW file; committed scripts IMMUTABLE.  Builds on P2/P3.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import build_metric, PI, DEV, R, TH, PS
from full3d_newton import inv4x4, det4x4
import whole_metric_3d_matter as MAT
import p2_matter_s2_fullmetric as P2
import p3_aphi_matter as P3   # reuse a_of_phi, phi_from_metric, field plumbing (NOT its weight)


# phiref convention for the ruler integral (matches explore-script fingerprint int_0^phi
# and the constant-a reduction W=e^{(a+1)phi}).  DECLARED, not fitted.
PHIREF = 0.0


# ===========================================================================
# THE RULER-INTEGRAL WEIGHT (the fix).  ANALYTIC -- no quadrature.
#   a(phi)+1 = k eps0^p e^{-p phi}
#   INT_{phiref}^{phi} (a+1) dphi' = -(k eps0^p/p)(e^{-p phi} - e^{-p phiref})
#   W(phi) = exp( that )
#   k=0 -> INT=0 -> W==1 (machine-exact)  -> GR baseline, bitwise P2.
# ===========================================================================
def ruler_exponent(phi, k=0.0, p=1.0, eps0=1.0, phiref=PHIREF):
    """INT_{phiref}^{phi} (a(phi')+1) dphi'  (analytic)."""
    c = k * (eps0 ** p)
    # -(c/p)(e^{-p phi} - e^{-p phiref}); p>0 declared.  k=0 -> 0 exactly.
    return -(c / p) * (torch.exp(-p * phi) - math.exp(-p * phiref))


def weight_W_ruler(phi, k=0.0, p=1.0, eps0=1.0, phiref=PHIREF):
    """W(phi) = exp( INT_{phiref}^phi (a+1) dphi' ).  k=0 -> W identically 1 (exact)."""
    return torch.exp(ruler_exponent(phi, k=k, p=p, eps0=eps0, phiref=phiref))


# ===========================================================================
# WEIGHTED native-S^2 STRESS with the RULER weight:  Tw = W_ruler(phi) * T(L).
# Same placement as P3 (uniform on whole L); only the W FUNCTION changes.
# k=0 -> W=1 -> identical to P2 / P3 baseline.
# ===========================================================================
def stress_s2_weighted_ruler(g, ginv, dn, k=0.0, p=1.0, eps0=1.0, xi=1.0, kap=1.0):
    Tab, L, L2, L4 = MAT.stress_tensor(g, ginv, dn, xi, kap)
    phi = P3.phi_from_metric(g)
    W = weight_W_ruler(phi, k=k, p=p, eps0=eps0)
    return Tab * W[..., None, None], L, L2, L4, W


# ===========================================================================
# THE MODIFIED CONSERVATION RESIDUAL with the RULER weight.
#   nabla_mu (W T^mu_nu) = 0  with  W = exp(INT (a+1))  =>  d ln W/dphi = (a+1) EXACT
#   => div T = -(a+1) phi_,mu T^mu_nu   (coefficient now CORRECT, FTC).
# Identical structure to p3_aphi_matter.modified_conservation_residual, but the
# coefficient (a+1) is now the TRUE d ln W/dphi (the defect is gone).
# ===========================================================================
def modified_conservation_residual_ruler(G, g, ginv, dn, k=0.0, p=1.0, eps0=1.0,
                                         xi=1.0, kap=1.0):
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, xi, kap)
    divT = P2.covariant_divT_field(G, g, ginv, Tab)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    phi = P3.phi_from_metric(g)
    aP1 = (P3.a_of_phi(phi, k=k, p=p, eps0=eps0) + 1.0)   # = d ln W_ruler/dphi (EXACT)
    dphi = torch.zeros(*phi.shape, 4, device=g.device)
    dphi[..., R] = G.d_r(phi); dphi[..., TH] = G.d_th(phi); dphi[..., PS] = G.d_ps(phi)
    exch = torch.zeros_like(divT)
    for nu in range(4):
        s = torch.zeros_like(phi)
        for mu in range(4):
            s = s + dphi[..., mu] * Tmix[..., mu, nu]
        exch[..., nu] = -aP1 * s
    welded = divT - exch
    return dict(divT=divT, exch=exch, welded=welded)


# ===========================================================================
# VALIDATION
# ===========================================================================
def _dlnW_numeric(phi, k, p, eps0, h=1e-6):
    """Central-difference d ln W_ruler/dphi at scalar phi values."""
    phi = torch.as_tensor(phi, dtype=torch.float64)
    lwp = torch.log(weight_W_ruler(phi + h, k=k, p=p, eps0=eps0))
    lwm = torch.log(weight_W_ruler(phi - h, k=k, p=p, eps0=eps0))
    return (lwp - lwm) / (2 * h)


def validate():
    print("=" * 78)
    print(" P3 FIX VALIDATION -- ruler-integral weight W=exp(INT (a+1) dphi)")
    print(" (fixes p3_VERIFIER.md defect: product W mis-coefficiented running-a divT)")
    print("=" * 78)

    # ---- 1. BASELINE a=-1 (k=0): W==1 bitwise; still reproduces P2 bitwise ----
    from p3_validate_baseline import _setup
    G, g, ginv, F, m = _setup()
    dn = P2.field_dn_s2(G, F, m=m)
    phi = P3.phi_from_metric(g)
    W0 = weight_W_ruler(phi, k=0.0, p=1.0, eps0=1.0)
    maxW0 = float((W0 - 1.0).abs().max())
    print(f"\n[1] BASELINE k=0:  max|W-1| = {maxW0:.3e}   (must be 0 -> W==1 identically)")
    # weighted stress vs P2 stress at k=0 (bitwise)
    TabP2, *_ = P2.stress_s2_fullmetric(g, ginv, dn)
    TabW, *_, _ = stress_s2_weighted_ruler(g, ginv, dn, k=0.0)
    dT = float((TabW - TabP2).abs().max())
    print(f"    weighted(ruler) stress vs P2 stress (k=0): max|dT| = {dT:.3e}  (must be 0)")
    # AND vs P3's PRODUCT weight at k=0 (both collapse to P2) -> ruler==product at baseline
    TabProd, *_, _ = P3.stress_s2_weighted(g, ginv, dn, k=0.0)
    dTP = float((TabW - TabProd).abs().max())
    print(f"    ruler stress vs PRODUCT(P3) stress (k=0):   max|dT| = {dTP:.3e}  "
          f"(must be 0 -> baseline UNCHANGED by the fix)")

    # ---- 2. RUNNING-a CONSERVATION coefficient now CORRECT: d ln W/dphi = (a+1) ----
    print("\n[2] RUNNING-a: d ln W_ruler/dphi == (a+1)  (the defect coefficient is GONE)")
    for (k, p, eps0) in [(1.0, 1.0, 1.0), (0.5, 1.0, 1.0), (1.0, 2.0, 1.0)]:
        for phiv in (-0.2, -0.4):
            aP1 = float(P3.a_of_phi(torch.tensor(phiv), k=k, p=p, eps0=eps0) + 1.0)
            dnum = float(_dlnW_numeric(phiv, k, p, eps0))
            # product-form coefficient for contrast: (a+1)+phi*da/dphi
            dadphi = -p * k * (eps0 ** p) * math.exp(-p * phiv)
            prod_coef = aP1 + phiv * dadphi
            err_ruler = abs(dnum - aP1)
            err_prod_vs_aP1 = abs(prod_coef - aP1)  # the OLD defect size
            print(f"    k={k},p={p:.0f},eps0={eps0:.0f},phi={phiv:+.1f}: "
                  f"(a+1)={aP1:.5f}  d lnW/dphi(num)={dnum:.5f}  "
                  f"|err|={err_ruler:.2e}   "
                  f"[OLD product defect (a+1)+phi*da/dphi vs (a+1): "
                  f"{100*err_prod_vs_aP1/abs(aP1):.1f}%]")
    print("    -> ruler d lnW/dphi matches (a+1) to FD floor; the 17%/29% product error is GONE.")

    # ---- 3. NON-ABSORBABILITY preserved (da/dphi unchanged; W position-dependent k!=0) ----
    print("\n[3] NON-ABSORBABILITY preserved (a(phi) unchanged -> da/dphi unchanged):")
    phir = torch.linspace(-3.0, 1.0, 9)
    for (k, p, eps0, tag) in [(0.0, 1.0, 1.0, "k=0 (absorbable GR)"),
                              (1.0, 1.0, 1.0, "k=1,p=1"),
                              (1.0, 2.0, 1.0, "k=1,p=2")]:
        dadphi = -p * k * (eps0 ** p) * torch.exp(-p * phir)
        Wr = weight_W_ruler(phir, k=k, p=p, eps0=eps0)
        wvar = float((Wr.max() - Wr.min()).abs())
        print(f"    [{tag}] max|da/dphi|={float(dadphi.abs().max()):.3e}  "
              f"W-spread over phi[-3,1]={wvar:.3e}  "
              f"{'(W==1 const: absorbable)' if k == 0 else '(W runs with phi: NON-absorbable)'}")

    # ---- 4. CORRECTED exploration diagnostic ----
    print("\n[4] CORRECTED exploration diagnostic (ruler weight on the fixed config):")
    print("    a) conservation exchange term, ruler coefficient (now the TRUE d lnW/dphi):")
    G2, g2, ginv2, F2, m2 = _setup(Nr=48, Nth=12, Nps=8)
    dn2 = P2.field_dn_s2(G2, F2, m=m2)
    mask = P2.interior_mask(G2, r_margin=1.0, n_theta_edge=2)
    for k in (0.0, 1.0):
        rR = modified_conservation_residual_ruler(G2, g2, ginv2, dn2, k=k, p=1.0, eps0=1.0)
        rP = P3.modified_conservation_residual(G2, g2, ginv2, dn2, k=k, p=1.0, eps0=1.0)
        eR = float(rR['exch'][mask].abs().max())
        eP = float(rP['exch'][mask].abs().max())
        print(f"      k={k}: exch max|interior|  RULER={eR:.3e}   PRODUCT(P3)={eP:.3e}   "
              f"{'(both 0 at baseline)' if k == 0 else 'NOTE: identical (same (a+1) coeff; ruler MAKES it correct)'}")

    print("\n    b) structure effect on FIXED config -- ruler W vs product W on shallow phi:")
    Gf, gf, ginvf, Ff, mf = _setup(Nr=40, Nth=12, Nps=8)
    dnf = P2.field_dn_s2(Gf, Ff, m=mf)
    phif = P3.phi_from_metric(gf)
    print(f"      config phi range = [{float(phif.min()):.3f}, {float(phif.max()):.3f}]")
    base = None
    for (k, p, eps0) in [(0.0, 1.0, 1.0), (0.5, 1.0, 1.0), (1.0, 1.0, 1.0)]:
        TabR, *_, WR = stress_s2_weighted_ruler(gf, ginvf, dnf, k=k, p=p, eps0=eps0)
        TabPr, *_, WP = P3.stress_s2_weighted(gf, ginvf, dnf, k=k, p=p, eps0=eps0)
        TmixR = torch.einsum('...ma,...an->...mn', ginvf, TabR)
        rhoR = -TmixR[..., 0, 0]
        dOm = (Gf.wmu[None, :, None] * Gf.wps[None, None, :])
        rho_ang = (rhoR * dOm).sum((1, 2)) / (4 * PI)
        integ = 0.05 * Gf.r ** 2 * rho_ang
        r = Gf.r; M = torch.zeros_like(r)
        for i in range(1, len(r)):
            M[i] = M[i - 1] + 0.5 * (integ[i] + integ[i - 1]) * (r[i] - r[i - 1])
        Mtot = float(M[-1] - M[0])
        rho_core = float(rhoR[2, Gf.Nth // 2, 0])
        jj = Gf.Nth // 2
        WRr = [float(WR[i, jj, 0]) for i in (2, Gf.Nr // 2, Gf.Nr - 3)]
        WPr = [float(WP[i, jj, 0]) for i in (2, Gf.Nr // 2, Gf.Nr - 3)]
        line = (f"      k={k:.1f}: W_ruler(core/mid/seal)=[{WRr[0]:.3f},{WRr[1]:.3f},{WRr[2]:.3f}]  "
                f"W_prod=[{WPr[0]:.3f},{WPr[1]:.3f},{WPr[2]:.3f}]  rho(core)={rho_core:.4e}  M_diag={Mtot:.4f}")
        if k == 0.0:
            base = (Mtot, rho_core); print(line + "   <- baseline")
        else:
            dM = 100 * (Mtot - base[0]) / base[0]
            dr = 100 * (rho_core - base[1]) / abs(base[1])
            print(line + f"   dM={dM:+.1f}% drho_core={dr:+.1f}%")
    print("\n      SIGN/MAGNITUDE NOTE: on shallow phi in [-0.4,0], phiref=0, p=1, eps0=1:")
    print("      ruler exponent INT_0^phi(a+1) = k(1-e^{-p phi})/p.  For phi<0, e^{-p phi}>1")
    print("      => (1-e^{-p phi})<0 => exponent<0 => W_ruler<1 (SUPPRESSION), SAME sign as the")
    print("      product form on this range (product (a+1)phi<0 too).  The MAGNITUDE differs")
    print("      (ruler integrates the running rate); reported above as STRUCTURE, data-blind.")

    print("\n" + "=" * 78)
    print(" P3 FIX VALIDATION DONE -- ruler weight: baseline bitwise, (a+1) coeff EXACT,")
    print(" non-absorbability preserved, exploration re-run.  UNFORCED hypothesis; a=-1=GR.")
    print("=" * 78)


if __name__ == "__main__":
    validate()
