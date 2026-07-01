#!/usr/bin/env python3
"""
p2_round_s2_solver.py -- the ROUND native-S^2 soliton (the P2 anchor).

The P1/P0 anchor is the S^3/Skyrme round soliton; the native carrier is S^2, whose
radial EL DIFFERS (the tangential pressure parts ways -- coupled_tl_s2_derive.py).  So
the S^3 round profile is NOT an S^2 solution.  This module SOLVES the genuine round S^2
soliton: fields a(r), b(r), F(r) (constant in theta,psi) coupled through the diagonal
Weyl Einstein G^t_t, G^r_r and the native S^2 autograd EL, deg-1 node core
(F(core)=pi -> F(seal)=0; NODE values, NOT the m*pi ladder), B=1/A FREE, a=-1 (P3),
time zeroed (P4).  Column-FD Jacobian over the 3 radial profiles (cheap: 3*Nr unknowns).

This anchor is (a) the P2a round-recovery validation target for the native S^2 EL and
(b) the seed for the P2c shear observation.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  DATA-BLIND.  NEW file.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV
from full3d_newton import inv4x4, det4x4
from einstein_3d_eval import einstein_mixed_weyl
import p2_matter_s2_fullmetric as P2


def solve_round_s2(Nr, Nth=8, Nps=4, p=0.4, kap8=0.05, m=1, maxit=40, tol=1e-12,
                   verbose=False):
    G = F3.Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=0.05, cell=14.0)
    G = F3.attach_coord_weight(G)
    n = Nr
    rr = G.r.cpu().numpy()
    a0 = np.zeros(n)
    b0 = np.full(n, -p) * ((G.ri - rr) / (G.ri - G.rc))
    F0 = PI * (1 - (rr - G.rc) / (G.ri - G.rc))
    u = torch.tensor(np.concatenate([a0, b0, F0]), device=DEV)
    z = torch.zeros(Nr, Nth, Nps, device=DEV)

    def expand(v):
        return v[:, None, None].expand(Nr, Nth, Nps).contiguous()

    def resid(u):
        a = expand(u[0:n]); b = expand(u[n:2*n]); F = expand(u[2*n:3*n])
        g = build_metric(G, a, b, z, z); ginv = inv4x4(g)
        Gmix = einstein_mixed_weyl(G, a, b, z, z)
        dn = P2.field_dn_s2(G, F, m=m); Tab, _, _, _ = P2.stress_s2_fullmetric(g, ginv, dn)
        Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
        resE = Gmix - kap8 * Tmix
        el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
        sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
        W = torch.sqrt(sqrtg * G.wvol_coord); W = W / W[G.body].mean()
        jj = Nth // 2
        rE_tt = (W*resE[..., 0, 0])[:, jj, 0]
        rE_rr = (W*resE[..., 1, 1])[:, jj, 0]
        rel = (W*el)[:, jj, 0]
        wbc = 30.0
        rows = [rE_tt[3:n-3], rE_rr[3:n-3], rel[3:n-3],
                torch.tensor([wbc], device=DEV) * (u[2*n+0] - PI),     # F core node
                torch.tensor([wbc], device=DEV) * (u[2*n+n-1] - 0.0),  # F seal node
                torch.tensor([wbc], device=DEV) * (u[0*n+n-1] - 0.0),  # a(seal)=0
                torch.tensor([wbc], device=DEV) * (u[1*n+0] + p)]      # b(core)=-p
        return torch.cat([r.reshape(-1) for r in rows])

    def jac(u, eps=1e-6):
        F0 = resid(u); nU = u.numel(); nF = F0.numel()
        J = torch.zeros(nF, nU, device=DEV)
        for j in range(nU):
            up = u.clone(); up[j] += eps; um = u.clone(); um[j] -= eps
            J[:, j] = (resid(up) - resid(um)) / (2*eps)
        return J.detach(), F0.detach()

    lam = 1e-3; F = resid(u); Phi = float((F*F).sum())
    I = torch.eye(u.numel(), device=DEV); hist = [Phi]
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = jac(u)
        acc = False
        for _ in range(12):
            Jaug = torch.cat([J, math.sqrt(lam)*I], 0)
            Faug = torch.cat([-F, torch.zeros(u.numel(), device=DEV)], 0)
            du = torch.linalg.lstsq(Jaug, Faug).solution; un = u + du
            Pn = float((resid(un)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.25, 1e-13); acc = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"   [round-s2] it{it} Phi={Phi:.3e} lam={lam:.1e} {'acc' if acc else 'STALL'}")
        if not acc:
            break

    a = u[0:n].clone(); b = u[n:2*n].clone(); F = u[2*n:3*n].clone()
    # M_MS
    av = expand(a); bv = expand(b); Fv = expand(F)
    g = build_metric(G, av, bv, z, z); ginv = inv4x4(g)
    dn = P2.field_dn_s2(G, Fv, m=m); Tab, _, _, _ = P2.stress_s2_fullmetric(g, ginv, dn)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab); rho = -Tmix[..., 0, 0]
    dOm = (G.wmu[None, :, None] * G.wps[None, None, :])
    rho_ang = (rho * dOm).sum((1, 2)) / (4*PI)
    integ = kap8 * G.r**2 * rho_ang; r = G.r; M = torch.zeros_like(r)
    for i in range(1, len(r)):
        M[i] = M[i-1] + 0.5*(integ[i]+integ[i-1])*(r[i]-r[i-1])
    M_MS = float(M[-1] - M[0])
    bw = float((a + b).abs().max())
    return dict(G=G, a=a, b=b, F=F, Phi=Phi, M_MS=M_MS, bw=bw, hist=hist,
                Fcore=float(F[0]), Fseal=float(F[-1]))


if __name__ == "__main__":
    print("=== ROUND native-S^2 soliton (deg-1 node, autograd EL, B=1/A free) ===")
    for Nr in (40, 60, 80):
        s = solve_round_s2(Nr, verbose=(Nr == 40))
        print(f"  Nr={Nr}: Phi={s['Phi']:.3e}  M_MS={s['M_MS']:.5f}  "
              f"max|a+b|={s['bw']:.3f}(B=1/A free)  F(core)={s['Fcore']:.4f}(pi node) "
              f"F(seal)={s['Fseal']:.2e}")
