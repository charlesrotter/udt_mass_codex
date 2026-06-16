#!/usr/bin/env python3
"""
full3d_validate_matter.py -- VALIDATION GATE part (c): the 3-D matter EL.
  (1) ROUND hedgehog: the autograd matter EL is machine-zero (the #56 gate).
  (2) OFF-ROUND div-identity: div_mu T^mu_nu = -(EL_F F_nu + EL_G G_nu + EL_H H_nu)
      on a GENUINELY psi-dependent field+metric (the bug-exposing test that exposed
      the 2-D L4 bug).  T^mu_nu from the verified whole_metric_3d_matter.stress_tensor.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.  Runs IN-PROCESS.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch

torch.set_default_dtype(torch.float64)
DEV = "cpu"   # validation on CPU for clean asserts (small grids)
PI = math.pi

from spectral_cheb import cheb_interval, clenshaw_curtis_weights
from spectral_3d import SphereGrid
import full3d_matter as M
import whole_metric_3d_matter as WM
import radial_Bfree_soliton as RS


def build_round_soliton_grid(Nr, Nth, Nps, rc=0.05, cell=14.0, p=0.4, kap8=0.05,
                             xi=1.0, kap=1.0):
    """Solve the validated radial #56 soliton, interpolate (a,b,Theta) onto the
    Chebyshev radial nodes, and embed on the full 3-D (r,theta,psi) grid as the round
    hedgehog (F=Theta(r), G=theta, H=psi).  Returns grids + metric + field."""
    ri = rc + cell
    # solve radial soliton on a fine uniform grid, then interpolate to Cheb nodes
    rfine = RS.make_grid(1, 2000, rc=rc, rint=ri, geom=False, device='cpu')
    out = RS.selfconsistent_Bfree(rfine, xi, kap, p=p, kap8=kap8, iters=300,
                                  relax=0.4, verbose=False)
    rf = rfine[0].numpy()
    a_f = out['a'][0].numpy(); b_f = out['b'][0].numpy(); Th_f = out['Th'][0].numpy()
    # Cheb radial nodes on [rc, ri]
    rcheb, Dr = cheb_interval(Nr - 1, rc, ri)
    wr = clenshaw_curtis_weights(Nr - 1, rc, ri)
    a_r = np.interp(rcheb, rf, a_f)
    b_r = np.interp(rcheb, rf, b_f)
    Th_r = np.interp(rcheb, rf, Th_f)
    # sphere grid
    sg = SphereGrid(Nth, Nps)
    th = sg.th; ps = sg.ps
    # broadcast to (Nr,Nth,Nps)
    R = rcheb[:, None, None] * np.ones((1, Nth, Nps))
    TH = th[None, :, None] * np.ones((Nr, 1, Nps))
    PS = ps[None, None, :] * np.ones((Nr, Nth, 1))
    A = a_r[:, None, None] * np.ones((1, Nth, Nps))
    Bb = b_r[:, None, None] * np.ones((1, Nth, Nps))
    # round hedgehog: C=D=0 metric (a(r),b(r) only); F=Theta(r), G=theta, H=psi
    C = np.zeros((Nr, Nth, Nps))
    D = np.zeros((Nr, Nth, Nps))
    F = Th_r[:, None, None] * np.ones((1, Nth, Nps))
    G = TH.copy()
    H = PS.copy()
    return dict(rcheb=rcheb, Dr=Dr, wr=wr, sg=sg, R=R, TH=TH, PS=PS,
                A=A, B=Bb, C=C, D=D, F=F, G=G, H=H, xi=xi, kap=kap,
                M_MS=out['M_MS'].item())


def diag_metric(A, B, C, D, R, TH):
    """Diagonal Weyl metric g (...,4,4), inverse-diag (...,4), sqrt(-g) (...)."""
    sth = np.sin(TH)
    glow = np.stack([-np.exp(2*A), np.exp(2*B), np.exp(2*C)*R**2,
                     np.exp(2*D)*R**2*sth**2], axis=-1)  # (...,4)
    ginv_diag = 1.0/glow
    sqrtg = np.exp(A + B + C + D) * R**2 * sth
    return glow, ginv_diag, sqrtg


def t(x):
    return torch.tensor(x, dtype=torch.float64, device=DEV)


if __name__ == "__main__":
    print("=== full3d matter-EL VALIDATION (gate c) ===\n")
    Nr, Nth, Nps = 28, 8, 8
    print(f"grid Nr={Nr} Nth={Nth} Nps={Nps}; building round #56 soliton on 3-D basis...")
    S = build_round_soliton_grid(Nr, Nth, Nps)
    print(f"  radial soliton M_MS (reference) = {S['M_MS']:.6f}")

    Dr = t(S['Dr']); Dth = t(S['sg'].Dth_sh); Dps = t(S['sg'].Dps)
    wr = t(S['wr']); wOm = t(S['sg'].warea)
    F = t(S['F']); G = t(S['G']); H = t(S['H'])
    glow, ginv_diag, sqrtg = diag_metric(S['A'], S['B'], S['C'], S['D'], S['R'], S['TH'])
    ginv_diag = t(ginv_diag); sqrtg = t(sqrtg)
    xi, kap = S['xi'], S['kap']

    # ---- (1) ROUND hedgehog: matter EL machine-zero in the body? ----
    gF, gG, gH, w = M.matter_EL(F, G, H, ginv_diag, sqrtg, wr, wOm, Dr, Dth, Dps, xi, kap)
    # interior body: exclude the 2 Chebyshev edge rows (core/seal coordinate edge)
    body = slice(2, Nr-2)
    # pointwise EL density = grad / measure-weight
    elF = (gF/w)[body]; elG = (gG/w)[body]; elH = (gH/w)[body]
    print("\n[1] ROUND hedgehog matter EL (pointwise density, interior body):")
    print(f"    max|EL_F| = {elF.abs().max().item():.3e}")
    print(f"    max|EL_G| = {elG.abs().max().item():.3e}")
    print(f"    max|EL_H| = {elH.abs().max().item():.3e}")
    print("    (EL_F is the chiral-profile eqn = the radial Theta-EL; EL_G,EL_H should")
    print("     vanish because G=theta,H=psi is the hedgehog stationary point.)")

    # ---- (2) OFF-ROUND div-identity ----
    print("\n[2] OFF-ROUND div-identity  div_mu T^mu_nu = -(EL.dphi):")
    # perturb the field genuinely off-round AND psi-dependently
    rng = np.random.default_rng(3)
    pert = 0.15*np.cos(2*S['PS'])*np.sin(S['TH'])*np.exp(-((S['R']-3)/2)**2)
    F2 = t(S['F'] + 0.10*pert)
    G2 = t(S['G'] + 0.08*np.sin(S['PS'])*np.sin(S['TH']))
    H2 = t(S['H'] + 0.05*np.cos(S['TH']))
    # also perturb the metric off-round (psi-dependent C,D) to make it a real off-round test
    C2 = 0.06*np.cos(S['PS'])*np.sin(S['TH'])**2*np.exp(-((S['R']-3)/2.5)**2)
    D2 = 0.04*np.sin(2*S['PS'])*np.sin(S['TH'])**2*np.exp(-((S['R']-3)/2.5)**2)
    glow2, ginv2, sqrtg2 = diag_metric(S['A'], S['B'], C2, D2, S['R'], S['TH'])
    ginv2_t = t(ginv2); sqrtg2_t = t(sqrtg2)

    # matter EL on the off-round config
    gF2, gG2, gH2, w2 = M.matter_EL(F2, G2, H2, ginv2_t, sqrtg2_t, wr, wOm, Dr, Dth, Dps, xi, kap)
    elF2 = gF2/w2; elG2 = gG2/w2; elH2 = gH2/w2

    # stress tensor T^mu_nu from the verified module, same dn
    dn2, n2 = M.build_dn(F2, G2, H2, Dr, Dth, Dps)
    g2_t = t(glow2)  # diagonal entries
    g2full = torch.diag_embed(g2_t)
    ginv2full = torch.diag_embed(ginv2_t)
    Tab, _, _, _ = WM.stress_tensor(g2full, ginv2full, dn2, xi, kap)   # T_{mu nu} lower
    Tmix = torch.einsum('...mk,...kn->...mn', ginv2full, Tab)          # T^mu_nu

    # div_mu T^mu_nu  (covariant) computed SPECTRALLY -- independent of the EL.
    # Need Christoffel of the diagonal metric (spectral derivatives).
    # dg[k,mu,nu] = d_k g_{mu nu};  build for the 3 spatial coords.
    Nr_, Nth_, Nps_, _, _ = g2full.shape
    dg = torch.zeros(Nr_, Nth_, Nps_, 4, 4, 4, dtype=torch.float64)
    for mu in range(4):
        for nu in range(4):
            comp = g2full[..., mu, nu]
            dg[..., 1, mu, nu] = M.d_r(comp, Dr)
            dg[..., 2, mu, nu] = M.d_th(comp, Dth)
            dg[..., 3, mu, nu] = M.d_ps(comp, Dps)
    # Christoffel Gamma^a_{bc} = 0.5 g^{ad}(d_b g_{dc}+d_c g_{db}-d_d g_{bc})
    A_ = torch.einsum('...bdc->...dbc', dg)
    Bp = torch.einsum('...cdb->...dbc', dg)
    Cp = dg
    Tterm = A_ + Bp - Cp
    Gamma = 0.5*torch.einsum('...ad,...dbc->...abc', ginv2full, Tterm)
    # div_mu T^mu_nu = d_mu T^mu_nu + Gamma^mu_{mu l} T^l_nu - Gamma^l_{mu nu} T^mu_l
    dT = torch.zeros(Nr_, Nth_, Nps_, 4, dtype=torch.float64)  # d_mu T^mu_nu (sum over mu)
    for nu in range(4):
        s = torch.zeros(Nr_, Nth_, Nps_, dtype=torch.float64)
        # mu=1 (r), 2 (theta), 3 (psi); mu=0 (t) static -> 0
        s = s + M.d_r(Tmix[..., 1, nu], Dr)
        s = s + M.d_th(Tmix[..., 2, nu], Dth)
        s = s + M.d_ps(Tmix[..., 3, nu], Dps)
        dT[..., nu] = s
    divT = dT.clone()
    divT = divT + torch.einsum('...mml,...ln->...n', Gamma, Tmix)
    divT = divT - torch.einsum('...lmn,...ml->...n', Gamma, Tmix)

    # RHS: -(EL_F dF + EL_G dG + EL_H dH) for each nu
    dF = torch.zeros(Nr_, Nth_, Nps_, 4, dtype=torch.float64)
    dG = torch.zeros_like(dF); dH = torch.zeros_like(dF)
    for fld, dst in [(F2, dF), (G2, dG), (H2, dH)]:
        dst[..., 1] = M.d_r(fld, Dr); dst[..., 2] = M.d_th(fld, Dth); dst[..., 3] = M.d_ps(fld, Dps)
    rhs = -(elF2[..., None]*dF + elG2[..., None]*dG + elH2[..., None]*dH)

    body3 = (slice(2, Nr-2), slice(None), slice(None))
    for nu, lbl in enumerate(['t', 'r', 'theta', 'psi']):
        d = (divT[..., nu] - rhs[..., nu])[body3]
        scale = max(divT[..., nu][body3].abs().max().item(), 1e-30)
        print(f"    nu={lbl:5s}: max|divT - (-EL.dphi)| = {d.abs().max().item():.3e}"
              f"   (rel {d.abs().max().item()/scale:.3e})")
    print("\n(If [1] EL_G,EL_H ~ machine-zero and the radial EL_F is small, AND [2] the")
    print(" div-identity holds off-round, the 3-D matter EL is CORRECT off-round.)")
