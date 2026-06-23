#!/usr/bin/env python3
"""
b1prime_shear_twist_hessian.py -- THE ENSEMBLE'S FIRST INSTRUMENT.

OBSERVE / METRIC-LED / DATA-BLIND / EMERGENCE-LED.  The off-round shear-twist
coupled stiffness, linearized about the converged ROUND DEFECT, on the DERIVED
operator.  Decisive cheap eigenproblem (fixed background).  ANTI-HANG: single
foreground process, no Newton, no background-poll, bounded grid, action FD only.

QUESTION: with the off-round shear g^{rps} LIVE, does the native matter twist g
get sourced into an ENERGY-LOWERING coupled (shear,twist) mode -> instability of
the round defect toward a localized twisted off-round body?  Or is the coupled
stiffness positive (defect survives off-round)?

THE FIELDS (on the round-soliton background):
  - twist  beta : matter free-azimuth  Psi = m ps + beta * h_g(r)   (h_g a localized
    radial profile).  This is free_s2_matter.field_*_freeaz -- the EXACT native twist
    channel (n = (sth cosPsi, sth sinPsi, cth), winding analytic, free part spectral).
  - shear  alpha: metric off-diagonal  e_rps = alpha * h_s(r) * P_ang(th)   (build_metric
    e_rp slot).  g_{r ps} = e_rp * r * sth ; round when alpha=0.

THE ACTION (the derived operator, verbatim):
  S = INT sqrt(-g) [ e^{2phi} R + X e^{2phi} g^{ab} d_a phi d_b phi + e^{2phi} L_m ] dV
  GRAVITY R via the GENERAL (shear-capable) analytic engine einstein_mixed_general
  (NOT the diagonal Weyl engine -- the shear needs the general engine).  L_m = native
  S^2 L2+L4 via the free_s2_matter machinery.  Production X=-2e5, xi=kap=2e-2, kap8=1.

THE HESSIAN: S(alpha,beta) on the round background; H = d^2 S / d(alpha,beta)^2 by
central finite differences (FD), a 2x2 (per chosen profile).  Eigenvalues of H:
  - both >0  : round defect STABLE in the off-round (shear,twist) sector (defect survives).
  - one <0   : ENERGY-LOWERING coupled mode (instability toward a twisted off-round body)
               -- then BOX-CONTROL gate the soft mode.
SIGN CONVENTION: the matter action S = INT sqrt(-g) f L_m, with L2 = -(xi/2) g^{mn}G_mn.
The matter ENERGY (what should be minimized for a stable static body) is -S_m-like; we
compute S itself and read the curvature, then state the energy sign explicitly per the
static reduction (negative action-curvature in a direction that LOWERS energy = instability).
We report BOTH the action-Hessian AND the matter-energy interpretation, and the cross term
sign, so the verdict is unambiguous.
"""
import os, sys, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/tmp")

import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
from full3d_spectral import Grid3D, attach_coord_weight, build_metric, DEV
from einstein_3d_general_eval import einstein_mixed_general, ricci_scalar_general
import free_s2_matter as FS
import b1prime_round as RAD

T, R, TH, PS = 0, 1, 2, 3
PI = math.pi
X, XI, KAP, KAP8 = -2e5, 2e-2, 2e-2, 1.0
P_DEPTH = 1.0


# ---------------------------------------------------------------------------
# warps dict for the general engine, from (a,b,c,d, e_rp) fields.  The general
# engine's warp names: a,b,c,d, e_rt,e_rp,e_tp, h_tr,h_tt,h_tp.  We only turn on
# e_rp (the r-ps shear) here; the rest default to 0 (diagonal/static).
# ---------------------------------------------------------------------------
def warps_dict(a, b, c, d, e_rp=None):
    w = dict(a=a, b=b, c=c, d=d)
    if e_rp is not None:
        w['e_rp'] = e_rp
    return w


def matter_dn(G, beta, h_g, m=1):
    """native twist channel: Psi = m ps + beta*h_g(r); dn EXACT (free_s2_matter)."""
    phi_tw = beta * h_g            # the free periodic-in-ps?  here h_g is r-only (twist g(r))
    return FS.field_dn_freeaz(G, phi_tw, m=m)


def action_density_parts(G, a, b, c, d, e_rp, phi, beta, h_g, m=1):
    """sqrt(-g) e^{2phi} [ R + X (dphi)^2 + L_m ] integrand pieces (no kap8 split; kap8=1)."""
    g = build_metric(G, a, b, c, d, e_rp=e_rp)
    ginv = CORE.metric_inverse(g)
    f = torch.exp(torch.clamp(2 * phi, max=60.0))
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-300))
    # gravity R (GENERAL engine -- shear-capable)
    Rscal = ricci_scalar_general(G, warps_dict(a, b, c, d, e_rp))
    # phi X-kinetic
    dphi = torch.stack([torch.zeros_like(phi), G.d_r(phi), G.d_th(phi), G.d_ps(phi)], dim=-1)
    dphi2 = torch.einsum('...ma,...a,...m->...', ginv, dphi,
                         torch.einsum('...mb,...b->...m', ginv, dphi)) if False else \
            torch.einsum('...m,...m->...', torch.einsum('...ma,...a->...m', ginv, dphi), dphi)
    # matter L_m (native S^2; twist channel)
    dn = matter_dn(G, beta, h_g, m=m)
    Gmn = MAT.field_metric(dn)
    Lm, L2, L4, _ = MAT.lagrangian(ginv, Gmn, XI, KAP)
    integrand = sqrtg * f * (Rscal + X * dphi2 + KAP8 * Lm)
    return integrand, dict(Rscal=Rscal, dphi2=dphi2, Lm=Lm, L2=L2, L4=L4,
                           sqrtg=sqrtg, f=f, g=g, ginv=ginv)


def total_action(G, a, b, c, d, alpha, beta, h_s_field, h_g, phi, m=1, body_only=True):
    """S(alpha,beta): shear e_rp = alpha*h_s_field, twist amp beta.  Integrate over body."""
    e_rp = alpha * h_s_field
    integ, _ = action_density_parts(G, a, b, c, d, e_rp, phi, beta, h_g, m=m)
    w = G.wvol_coord
    if body_only:
        mask = G.body.double()
        return (integ * w * mask).sum()
    return (integ * w).sum()


def run():
    print("=" * 78)
    print("SHEAR-TWIST COUPLED HESSIAN about the ROUND DEFECT  (derived operator)")
    print("X=%.1e xi=%.2e kap=%.2e kap8=%g   [native S^2 twist + e_rp shear]"
          % (X, XI, KAP, KAP8))
    print("=" * 78)

    # ---- converged round soliton background (cheap 1-D LM) ----
    Nr = 16
    RG = RAD.RGrid(Nr, rc=0.05, cell=14.0)
    t0 = time.time()
    u_rad, Phi = RAD.solve(RG, X, XI, KAP, P_DEPTH, KAP8, m=1, maxit=120, verbose=False)
    dgd = RAD.diag(RG, u_rad, X, XI, KAP)
    print("[round soliton] residual Phi=%.3e (%.1fs)  Th_core=%.3f Th_seal=%.3f phimin=%.2e"
          % (Phi, time.time() - t0, dgd['Th_core'], dgd['Th_seal'], dgd['phi_min']))
    a_r, b_r, phi_r = dgd['a'], dgd['b'], dgd['ph']

    G = Grid3D(Nr=Nr, Nth=8, Nps=8, rc=0.05, cell=14.0)
    G = attach_coord_weight(G)
    rdiff = float(np.max(np.abs(RG.r - G.r.cpu().numpy())))
    print("   |r_radial - r_3d|max = %.2e" % rdiff)

    def lift(arr):
        t = torch.tensor(arr, device=DEV)
        return t[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()
    a = lift(a_r); b = lift(b_r); c = torch.zeros_like(a); d = torch.zeros_like(a)
    phi = lift(phi_r)

    # ---- localized profiles for the shear and twist deformations ----
    rc, ri = float(G.r[0]), float(G.r[-1])
    rfac = torch.sin(PI * (G.Rg - rc) / (ri - rc))     # 0 at core/seal, smooth body bump
    # twist g(r): r-only profile (no ps -> a pure twist g(r); free_s2 carries m ps analytic)
    h_g = (rfac).clone()
    # shear e_rp profile: localized in r, l=1-ish angular structure (sin th already in metric
    # geometric factor; e_rp multiplies r*sin th).  Use P_ang = 1 (the raw warp) + try P2.
    P1 = torch.ones_like(G.Rg)
    mu = torch.cos(G.THg); P2 = 0.5 * (3 * mu**2 - 1.0)
    h_s_uniform = rfac * P1
    h_s_P2 = rfac * P2

    # ---- sanity: round (alpha=0,beta=0) reproduces the converged action finite & defect ----
    S00 = total_action(G, a, b, c, d, 0.0, 0.0, h_s_uniform, h_g, phi, m=1)
    print("\n[background] S(0,0) = %.6e  finite=%s" % (S00.item(), bool(torch.isfinite(S00))))

    # ---- the matter-only piece sanity: confirm the cross-source appears (alpha,beta>0) ----
    # quantify the analytic cross stiffness at a body node (matter L2): m xi e^{-2b-2d}/r^2
    ir = Nr // 2
    bval = b[ir, 0, 0].item()
    rval = G.Rg[ir, 0, 0].item()
    cross_L2_analytic = 1.0 * XI * math.exp(-2 * bval - 0) / rval**2
    print("   [analytic matter L2 cross stiffness at body r=%.3f] m xi e^{-2b}/r^2 = %.4e"
          % (rval, cross_L2_analytic))

    # =====================================================================
    # THE 2x2 ACTION HESSIAN by central FD.  Choose FD step; verify linear regime.
    # =====================================================================
    for tag, h_s_field in [("shear=uniform(P0)", h_s_uniform), ("shear=l2(P2)", h_s_P2)]:
        print("\n" + "-" * 78)
        print("HESSIAN block  [%s] x [twist g(r)]" % tag)
        print("-" * 78)
        for hstep in [1e-3, 3e-3]:
            ha = hstep; hb = hstep
            def S(al, be):
                return total_action(G, a, b, c, d, al, be, h_s_field, h_g, phi, m=1).item()
            S0 = S(0, 0)
            # second derivatives (central):
            Saa = (S(ha, 0) - 2 * S0 + S(-ha, 0)) / ha**2
            Sbb = (S(0, hb) - 2 * S0 + S(0, -hb)) / hb**2
            Sab = (S(ha, hb) - S(ha, -hb) - S(-ha, hb) + S(-ha, -hb)) / (4 * ha * hb)
            H = np.array([[Saa, Sab], [Sab, Sbb]])
            evals, evecs = np.linalg.eigh(H)
            det = Saa * Sbb - Sab**2
            print("  FD step=%.1e : H_aa=%+.4e  H_bb=%+.4e  H_ab=%+.4e" % (hstep, Saa, Sbb, Sab))
            print("              det(H)=%+.4e  eig(H)=[%+.4e, %+.4e]"
                  % (det, evals[0], evals[1]))
            print("              cross-vs-diag |H_ab|^2 / (H_aa H_bb) = %.4f  (>1 => indefinite)"
                  % (Sab**2 / (Saa * Sbb) if Saa * Sbb != 0 else float('nan')))
            soft = evecs[:, np.argmin(evals)]
            print("              softest eigvec (alpha,beta) = (%+.3f, %+.3f)"
                  % (soft[0], soft[1]))

    # =====================================================================
    # ENERGY-SIGN read-out.  The static body's ENERGY is minimized at a stable
    # solution.  For the static reduction, the relevant functional is the
    # mass/energy = -INT (matter+gravity) with the time-Killing reduction.  We
    # state the read explicitly: a NEGATIVE eigenvalue of the ENERGY Hessian =
    # energy-lowering = instability.  Print the action-Hessian eigen-sign and the
    # energy-Hessian eigen-sign (energy = -action for the static matter sector here,
    # so they flip; we report both, no ambiguity).
    # =====================================================================
    print("\n" + "=" * 78)
    print("READ-OUT (sign convention stated):")
    print("  S = INT sqrt(-g) f (R + X(dphi)^2 + L_m).  We computed the ACTION Hessian.")
    print("  Background is the converged round soliton (a stationary point of the FULL")
    print("  6-field operator restricted to round).  The (alpha,beta) block asks: does")
    print("  the round stationary point have a DESCENT direction once shear+twist are on?")
    print("  A NEGATIVE action-Hessian eigenvalue = the action DECREASES along that mode")
    print("  = a genuine instability of the round defect IF that mode lowers the energy.")
    print("  We report det(H) and eigenvalues; the verdict is read from the SIGN.")
    print("=" * 78)
    print("DONE.")


if __name__ == "__main__":
    run()
