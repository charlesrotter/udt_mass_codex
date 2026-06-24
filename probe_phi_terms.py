#!/usr/bin/env python3
"""
probe_phi_terms.py -- IS THE phi-EQUATION SINGULARLY STIFF? (infrastructure)

Driver: Claude (Opus 4.8). 2026-06-23. INFRASTRUCTURE AUDIT. NO solve -- only
evaluates EL_phi's constituent terms on SAVED floored fields.

HYPOTHESIS: EL_phi = alg - 2*X*div [- 2 U'(phi)] with X=-2e5.  If |alg| and
|2X*div| are each O(1e5) and nearly CANCEL to leave an O(1) residual, the phi
equation is singularly stiff (huge X multiplies phi's Laplacian) -> EL_phi ~
X*(curvature discretization error) -> cannot floor on a coarse grid.  That is a
NUMERICS/METHOD problem (continuation-in-X / non-dimensionalization), NOT
physics -> the scale-free read is UNTRUSTWORTHY until fixed.

TEST: decompose EL_phi term-by-term, report norms + the cancellation ratio.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import _grid
from branchGP_native_s2_coupled_OBSERVE import (
    build_metric, christoffel_vsafe, coord_grad, coord_hess, det4x4,
    einstein_mixed_weyl, s2_Tmix_and_Lm, R, TH)

G = _grid(10)
X, XI, KAP, KAP8, M = B.X_PROD, B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
log = lambda s: print(s, flush=True)


def decompose(u, branch):
    a, b, c, d, phi, gtw = B.unpack6(u)
    g = build_metric(G, a, b, c, d)
    Gamma, ginv = christoffel_vsafe(G, g)
    f = torch.exp(torch.clamp(2*phi, max=60.0)); fp = 2.0*f
    Gmix_w = einstein_mixed_weyl(G, a, b, c, d)
    Rscal = -torch.einsum('...mm->...', Gmix_w)
    dphi = coord_grad(G, phi)
    dphi_up = torch.einsum('...ma,...a->...m', ginv, dphi)
    dphi2 = torch.einsum('...m,...m->...', dphi_up, dphi)
    _, Lm = s2_Tmix_and_Lm(G, g, ginv, gtw, xi=XI, kap=KAP, m=M)
    alg = fp*(Rscal + X*dphi2 + KAP8*Lm)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    Hphi = coord_hess(G, phi); df = coord_grad(G, f)
    term_hess = f*torch.einsum('...mn,...mn->...', ginv, Hphi)
    term_fdphi = torch.einsum('...mn,...m,...n->...', ginv, df, dphi)
    conn = torch.zeros_like(f); SGgup = sqrtg[..., None, None]*ginv
    for mu in range(1, 4):
        for nu in range(1, 4):
            comp = SGgup[..., mu, nu]
            dcomp = G.d_r(comp) if mu == R else (G.d_th(comp) if mu == TH else G.d_ps(comp))
            conn = conn + dcomp*dphi[..., nu]
    conn = f*conn/torch.clamp(sqrtg, min=1e-30)
    div = term_hess + term_fdphi + conn
    twoXdiv = 2.0*X*div
    Up = 2.0*(2.0*torch.exp(torch.clamp(2*phi, max=60.0))) if branch == "P" else torch.zeros_like(f)
    elphi = alg - twoXdiv - (Up if branch == "P" else 0.0)
    bod = G.body
    nrm = lambda t: float(t[bod].norm())
    log(f"  [{branch}] term norms on body:")
    log(f"     |alg|              = {nrm(alg):.4e}")
    log(f"     |2*X*div|          = {nrm(twoXdiv):.4e}   (X={X:.1e})")
    log(f"     |2*U'(phi)| (P)    = {nrm(Up):.4e}")
    log(f"     |EL_phi residual|  = {nrm(elphi):.4e}")
    log(f"     |div| alone        = {nrm(div):.4e}   -> *2|X| = {2*abs(X)*nrm(div):.3e}")
    big = max(nrm(alg), nrm(twoXdiv))
    log(f"     CANCELLATION: residual/max(|alg|,|2Xdiv|) = {nrm(elphi)/max(big,1e-30):.3e}  "
        f"(<<1 => catastrophic cancellation of two O({big:.0e}) terms)")
    log(f"     phi range body = [{float(phi[bod].min()):+.3e}, {float(phi[bod].max()):+.3e}]  "
        f"|grad phi| max = {float(dphi[bod].abs().max()):.3e}")


for tag, path in [("uP_jfnk_equil(Phi~8421)", "/tmp/uP_jfnk_equil.pt"),
                  ("uP_stall(Phi~3.49)", "/tmp/uP_stall.pt"),
                  ("uP_equil(Phi~569)", "/tmp/uP_equil.pt")]:
    if os.path.exists(path):
        log("=" * 60); log(f"FIELD: {tag}")
        u = torch.load(path).to('cuda' if torch.cuda.is_available() else 'cpu')
        decompose(u, "P")
        # control: same field read on Branch G (no U', no scale-breaker)
        decompose(u, "G")
log("\n=== probe done ===")
