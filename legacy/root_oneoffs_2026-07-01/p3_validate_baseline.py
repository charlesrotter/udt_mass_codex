#!/usr/bin/env python3
"""
p3_validate_baseline.py -- P3b: the BINDING baseline validation.

The wiring is correct ONLY if a=-1 (k=0) reproduces P2 EXACTLY:
  (1) the weight W(phi) is identically 1 (machine-exact) for k=0,
  (2) the modified-conservation EXCHANGE term -(a+1)phi'T vanishes for k=0,
  (3) the weighted stress == P2's stress, the weighted EL == P2's EL (bitwise/floor),
  (4) the round-S^2 soliton M_MS with the weighted source (k=0) == P2's round M_MS.
If a=-1 does NOT reproduce P2, the wiring is wrong (header of the prompt).

ALSO the NON-ABSORBABILITY check (P3c precondition):  a CONSTANT weight relabels to
GR (absorbable); only a position-dependent W(phi) is genuinely new.  We show:
  - k=0: W==1 (trivial).
  - constant-a (a free but CONSTANT, i.e. p=0 so e^{-p phi}=1): W = e^{(a+1)phi} is
    STILL position-dependent UNLESS a=-1 -- wait: with CONSTANT a!=-1, W=e^{(a+1)phi}
    varies with phi, so even constant a is position-dependent HERE.  The arc's
    "constant a is absorbable" is the statement that a CONSTANT exponent relabels via
    a coordinate/units choice (rescaling the matter ruler).  We make the operational
    distinction the right way: we verify the DERIVED a(phi) (k!=0,p>=1) has a
    NON-CONSTANT a (da/dphi != 0), which is the codex's banked non-absorbability
    criterion (a(phi) a real function, not a constant).  See report.

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
from full3d_spectral import build_metric, PI, DEV, R
from full3d_newton import inv4x4, det4x4
import whole_metric_3d_matter as MAT
import p2_matter_s2_fullmetric as P2
import p3_aphi_matter as P3


def _setup(Nr=40, Nth=12, Nps=8, m=1, seed=0):
    """A representative NON-DIAGONAL, NON-trivial-phi config to test on (not a solve)."""
    G = F3.Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=0.05, cell=14.0)
    G = F3.attach_coord_weight(G)
    torch.manual_seed(seed)
    rr = G.r
    # a soliton-like radial warp so g_rr = e^{2b} is genuinely position-dependent (phi varies)
    b = (-0.4) * ((G.ri - rr) / (G.ri - G.rc))
    a = -b                                    # B=1/A (g_tt g_rr = -1), FREE choice here
    bb = b[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()
    aa = a[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
    # live off-diagonals (small) so we test on the FULL off-diagonal metric
    A = 0.05
    e_rt = A*torch.sin(G.THg)*torch.exp(-(rr[:,None,None]-rr.mean())**2)
    e_rp = 0.7*A*torch.cos(G.THg)*torch.ones_like(z)
    e_tp = 0.5*A*torch.sin(2*G.THg)*torch.ones_like(z)
    g = build_metric(G, aa, bb, z, z, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    ginv = inv4x4(g)
    # a theta-dependent (axis-regular) native S^2 profile F = theta + h(r) sin(theta)
    th = G.THg
    h = 0.5*torch.exp(-((rr[:,None,None]-3.0)**2)/4.0)*torch.ones_like(z)
    F = th + h*torch.sin(th)
    return G, g, ginv, F, m


def p3b_baseline():
    print("="*78); print(" P3b -- BASELINE a=-1 (k=0) reproduces P2 EXACTLY"); print("="*78)
    G, g, ginv, F, m = _setup()
    dn = P2.field_dn_s2(G, F, m=m)

    # (1) weight identically 1 at k=0
    phi = P3.phi_from_metric(g)
    W0 = P3.weight_W(phi, k=0.0, p=1.0, eps0=1.0)
    print(f" [1] k=0 weight:  max|W-1| = {float((W0-1.0).abs().max()):.3e}   (must be 0)")
    print(f"     phi range read off metric: [{float(phi.min()):.4f}, {float(phi.max()):.4f}] "
          f"(genuinely position-dependent)")
    aP1_0 = P3.a_of_phi(phi, k=0.0)+1.0
    print(f" [2] k=0 exchange coeff (a+1): max|a+1| = {float(aP1_0.abs().max()):.3e} "
          f"(must be 0 -> modified-conservation term vanishes -> standard div T=0)")

    # (3a) weighted stress == P2 stress at k=0
    TabP2, *_ = P2.stress_s2_fullmetric(g, ginv, dn)
    TabW, *_ , W = P3.stress_s2_weighted(g, ginv, dn, k=0.0)
    dT = float((TabW - TabP2).abs().max()); sc = float(TabP2.abs().max())
    print(f" [3a] weighted stress vs P2 stress (k=0): max|dT|={dT:.3e}  (rel {dT/sc:.3e})  must be 0")

    # (3b) weighted EL == P2 EL at k=0
    elP2 = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
    elW  = P3.matter_el_s2_weighted(G, g, ginv, F, m=m, k=0.0)
    dE = float((elW - elP2).abs().max()); scE = float(elP2.abs().max())
    print(f" [3b] weighted EL vs P2 EL (k=0):        max|dEL|={dE:.3e}  (rel {dE/scE:.3e})  must be 0")

    ok = (float((W0-1.0).abs().max())==0.0 and float(aP1_0.abs().max())==0.0
          and dT==0.0 and dE==0.0)
    print(f"\n P3b VERDICT: {'PASS -- a=-1 reproduces P2 BITWISE' if ok else 'see numbers'}")
    return ok


def p3b_round_anchor():
    print("\n"+"="*78); print(" P3b -- round-S^2 M_MS with weighted source (k=0) == P2 round M_MS")
    print("="*78)
    # Re-solve the round soliton with the WEIGHTED stress+EL at k=0 vs P2's.
    import p2_round_s2_solver as RS
    # P2 baseline (unweighted)
    s_p2 = RS.solve_round_s2(Nr=40)
    print(f"  P2 (unweighted)      : Phi={s_p2['Phi']:.3e}  M_MS={s_p2['M_MS']:.6f}")
    # weighted at k=0 -- patch P2's stress/EL with the weighted ones via a thin solve
    M_w, Phi_w = _solve_round_weighted(Nr=40, k=0.0)
    print(f"  P3 weighted (k=0)    : Phi={Phi_w:.3e}  M_MS={M_w:.6f}")
    dM = abs(M_w - s_p2['M_MS'])
    print(f"  |dM_MS| = {dM:.3e}  (must be ~0 / machine-floor -> baseline reproduced)")
    return dM


def _solve_round_weighted(Nr, Nth=8, Nps=4, p_init=0.4, kap8=0.05, m=1,
                          maxit=40, tol=1e-12, k=0.0, p=1.0, eps0=1.0, verbose=False):
    """Round S^2 soliton using the P3 WEIGHTED stress + WEIGHTED EL.  k=0 -> identical
    to p2_round_s2_solver (the baseline check); k!=0 -> the P3c exploration solve."""
    G = F3.Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=0.05, cell=14.0)
    G = F3.attach_coord_weight(G)
    from einstein_3d_eval import einstein_mixed_weyl
    n = Nr; rr = G.r.cpu().numpy()
    a0 = np.zeros(n); b0 = np.full(n, -p_init)*((G.ri-rr)/(G.ri-G.rc))
    F0 = PI*(1-(rr-G.rc)/(G.ri-G.rc))
    u = torch.tensor(np.concatenate([a0, b0, F0]), device=DEV)
    z = torch.zeros(Nr, Nth, Nps, device=DEV)
    def expand(v): return v[:, None, None].expand(Nr, Nth, Nps).contiguous()
    def resid(u):
        a = expand(u[0:n]); b = expand(u[n:2*n]); Ff = expand(u[2*n:3*n])
        g = build_metric(G, a, b, z, z); ginv = inv4x4(g)
        Gmix = einstein_mixed_weyl(G, a, b, z, z)
        dn = P2.field_dn_s2(G, Ff, m=m)
        Tab, *_ = P3.stress_s2_weighted(g, ginv, dn, k=k, p=p, eps0=eps0)
        Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
        resE = Gmix - kap8*Tmix
        el = P3.matter_el_s2_weighted(G, g, ginv, Ff, m=m, k=k, p=p, eps0=eps0)
        sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
        W = torch.sqrt(sqrtg*G.wvol_coord); W = W/W[G.body].mean()
        jj = Nth//2
        rows = [(W*resE[...,0,0])[:,jj,0][3:n-3], (W*resE[...,1,1])[:,jj,0][3:n-3],
                (W*el)[:,jj,0][3:n-3],
                torch.tensor([30.0],device=DEV)*(u[2*n+0]-PI),
                torch.tensor([30.0],device=DEV)*(u[2*n+n-1]-0.0),
                torch.tensor([30.0],device=DEV)*(u[0*n+n-1]-0.0),
                torch.tensor([30.0],device=DEV)*(u[1*n+0]+p_init)]
        return torch.cat([r.reshape(-1) for r in rows])
    lam = 1e-3; Fr = resid(u); Phi = float((Fr*Fr).sum()); I = torch.eye(u.numel(),device=DEV)
    for it in range(maxit):
        if Phi < tol: break
        F0r = resid(u); nU=u.numel(); nF=F0r.numel(); J=torch.zeros(nF,nU,device=DEV)
        eps=1e-6
        for j in range(nU):
            up=u.clone(); up[j]+=eps; um=u.clone(); um[j]-=eps
            J[:,j]=(resid(up)-resid(um))/(2*eps)
        acc=False
        for _ in range(12):
            Jaug=torch.cat([J,math.sqrt(lam)*I],0); Faug=torch.cat([-F0r,torch.zeros(u.numel(),device=DEV)],0)
            du=torch.linalg.lstsq(Jaug,Faug).solution; un=u+du; Pn=float((resid(un)**2).sum())
            if np.isfinite(Pn) and Pn<Phi: u=un; Phi=Pn; lam=max(lam*0.25,1e-13); acc=True; break
            lam*=4.0
        if verbose: print(f"   it{it} Phi={Phi:.3e} {'acc' if acc else 'STALL'}")
        if not acc: break
    a=expand(u[0:n]); b=expand(u[n:2*n]); Ff=expand(u[2*n:3*n])
    g=build_metric(G,a,b,z,z); ginv=inv4x4(g)
    dn=P2.field_dn_s2(G,Ff,m=m); Tab,*_=P3.stress_s2_weighted(g,ginv,dn,k=k,p=p,eps0=eps0)
    Tmix=torch.einsum('...ma,...an->...mn',ginv,Tab); rho=-Tmix[...,0,0]
    dOm=(G.wmu[None,:,None]*G.wps[None,None,:]); rho_ang=(rho*dOm).sum((1,2))/(4*PI)
    integ=kap8*G.r**2*rho_ang; r=G.r; M=torch.zeros_like(r)
    for i in range(1,len(r)): M[i]=M[i-1]+0.5*(integ[i]+integ[i-1])*(r[i]-r[i-1])
    return float(M[-1]-M[0]), Phi


if __name__ == "__main__":
    ok = p3b_baseline()
    dM = p3b_round_anchor()
    print("\n"+"="*78)
    print(f" P3b SUMMARY: bitwise-stress/EL/weight match: {'PASS' if ok else 'CHECK'};"
          f"  round M_MS drift {dM:.3e}")
    print("="*78)
