#!/usr/bin/env python3
"""
full3d_solver.py -- the FULL-3-D coupled Einstein+L2+L4 solver (matrix-free
Levenberg-Marquardt / Gauss-Newton on the spectral residual system).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

UNKNOWNS: a,b,c,d (diagonal Weyl warps) + Theta, each (Nr,Nth,Nps).  Static.
RESIDUALS (proper-volume-weighted): the four diagonal mixed Einstein G^mu_nu -
kap8 T^mu_nu (tt,rr,thth,psps), the live off-diagonal Einstein residuals (G^r_th,
G^r_ps, G^th_ps - kap8 T-offdiag = 0 since diagonal stress -> these test the metric
must stay axisym-consistent OR carry genuine non-axisym structure), and the matter
EL (matter_el_3d).  Plus strong BC rows: winding Theta(core)=m*pi, Theta(seal)=0;
seal gauge a(seal)=0 (angle-averaged); depth dial b(core)=-p; c,d regular.

CATEGORY-A: Gauss-Newton's local linear step is the SOLVER (as the FD #56 / 2-D
spectral solvers used), NOT a physics linearization; the converged solution satisfies
the FULL nonlinear residual to the floor.  Proper-volume weight conditions descent
without changing the zero set.  Core/axis regularity excision removes a coordinate-
edge artifact.  NO B=1/A tie, NO injected term, NO dropped term, NO tuned dial.

NUMERICS: matrix-free LM -- autograd JVP/VJP build the Gauss-Newton normal-equation
action J^T J + lam I, solved by CG (no dense N^2 storage for the ~1e4 unknowns).
Strict monotone acceptance.  V100 float64.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric, einstein_mixed_weyl,
    field_dn, matter_el_3d, diagnostics, DEV, PI, T, R, TH, PS)
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT


# ---------------------------------------------------------------------------
# pack/unpack the 5 fields <-> a flat parameter vector
# ---------------------------------------------------------------------------
def pack(a, b, c, d, Th):
    return torch.cat([a.reshape(-1), b.reshape(-1), c.reshape(-1),
                      d.reshape(-1), Th.reshape(-1)])


def unpack(u, G):
    n = G.Nr*G.Nth*G.Nps
    sh = (G.Nr, G.Nth, G.Nps)
    a = u[0:n].reshape(sh); b = u[n:2*n].reshape(sh); c = u[2*n:3*n].reshape(sh)
    d = u[3*n:4*n].reshape(sh); Th = u[4*n:5*n].reshape(sh)
    return a, b, c, d, Th


# ---------------------------------------------------------------------------
# residual VECTOR (the objective F; Phi = ||F||^2).  Proper-volume-weighted
# interior Einstein + matter-EL rows; strong BC rows.
# ---------------------------------------------------------------------------
def residual_vector(u, G, p, kap8, m=1, wbc=30.0):
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d)
    ginv = CORE.metric_inverse(g)
    Gmix = einstein_mixed_weyl(G, a, b, c, d)
    dn = field_dn(G, Th, m=m)
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8*Tmix                                # (...,4,4)
    el = matter_el_3d(G, a, b, c, d, Th, m=m)
    # proper-volume weight (normalized) -> conditions the deep-core/near-axis spike
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    W = torch.sqrt(sqrtg * G.wvol_coord)
    W = W / W[G.body].mean()
    bod = G.body
    rows = []
    # the four diagonal Einstein + the three live spatial off-diagonals
    for (mm, nn) in [(T, T), (R, R), (TH, TH), (PS, PS), (R, TH), (R, PS), (TH, PS)]:
        rows.append((W*resE[..., mm, nn])[bod])
    rows.append((W*el)[bod])
    # ---- strong BC rows ----
    # winding Theta(core)=m*pi, Theta(seal)=0 over all (th,ps)
    rows.append(wbc*(Th[0, :, :].reshape(-1) - m*PI))
    rows.append(wbc*(Th[-1, :, :].reshape(-1) - 0.0))
    # seal gauge a(seal)=0 (per angle)
    rows.append(wbc*a[-1, :, :].reshape(-1))
    # depth dial b(core)=-p (per angle)
    rows.append(wbc*(b[0, :, :].reshape(-1) + p))
    # c,d regular at core (=0 there, the round limit) and seal (=0)
    rows.append(wbc*c[0, :, :].reshape(-1)); rows.append(wbc*c[-1, :, :].reshape(-1))
    rows.append(wbc*d[0, :, :].reshape(-1)); rows.append(wbc*d[-1, :, :].reshape(-1))
    F = torch.cat([r.reshape(-1) for r in rows])
    return F


def phi(u, G, p, kap8, m=1):
    F = residual_vector(u, G, p, kap8, m=m)
    return float((F*F).sum())


# ---------------------------------------------------------------------------
# matrix-free Gauss-Newton / LM step:  solve (J^T J + lam I) du = -J^T F  by CG.
# JVP = d/deps F(u+eps v); VJP via autograd.
# ---------------------------------------------------------------------------
def lm_step(u, G, p, kap8, lam, m=1, cg_iters=80, cg_tol=1e-6):
    u = u.detach().clone().requires_grad_(True)
    F = residual_vector(u, G, p, kap8, m=m)
    # VJP closure: J^T w
    def JT(w):
        g, = torch.autograd.grad(F, u, grad_outputs=w, retain_graph=True)
        return g
    # JVP via double-grad trick: J v = d/d? ... use forward over reverse
    # use the identity: J v = grad_w( <JT(w), v> ) but simpler: finite-free via
    # torch.autograd.functional not available cheaply here -> use the standard
    # "double backward": let w be a dummy with grad; <F, w>; grad wrt u gives JT(w);
    # then grad of <JT(w), v> wrt w gives J v.
    w0 = torch.zeros_like(F, requires_grad=True)
    JTw = torch.autograd.grad(F, u, grad_outputs=w0, create_graph=True)[0]
    def JV(v):
        jv, = torch.autograd.grad(JTw, w0, grad_outputs=v, retain_graph=True)
        return jv
    b = JT(-F.detach())                                    # rhs = -J^T F
    # diagonal (Jacobi) preconditioner: estimate diag(J^T J) by Hutchinson probes
    # (cheap, category-A: only conditions the descent, does not change the solution)
    diag = torch.zeros_like(u)
    nprobe = 6
    for _ in range(nprobe):
        z = torch.randn_like(F)
        jz = JT(z)
        diag += jz*jz
    diag = diag/nprobe + lam
    Minv = 1.0/torch.clamp(diag, min=1e-12)
    # preconditioned CG on (J^T J + lam I) x = b
    x = torch.zeros_like(u)
    r = b.clone()
    z = Minv*r
    pdir = z.clone()
    rz = float(r@z); rs0 = float(r@r)
    for _ in range(cg_iters):
        Jp = JV(pdir)
        Ap = JT(Jp) + lam*pdir
        alpha = rz/float(pdir@Ap + 1e-300)
        x = x + alpha*pdir
        r = r - alpha*Ap
        if float(r@r) < cg_tol*rs0:
            break
        z = Minv*r
        rz_new = float(r@z)
        pdir = z + (rz_new/rz)*pdir
        rz = rz_new
    return x.detach(), float((F*F).sum())


def jacobian_dense(u, G, p, kap8, m=1):
    """Full dense Jacobian J = dF/du by VJP rows (robust autograd; functorch vmap
    fails on torch.linalg.inv in the analytic Einstein engine, so we loop rows in
    chunks).  nF backward passes -- fine for small grids."""
    u = u.detach().clone().requires_grad_(True)
    F = residual_vector(u, G, p, kap8, m=m)
    nF = F.numel(); nU = u.numel()
    J = torch.zeros(nF, nU, device=u.device)
    eye = torch.eye(nF, device=u.device)
    for i in range(nF):
        gi, = torch.autograd.grad(F, u, grad_outputs=eye[i], retain_graph=True)
        J[i] = gi
    return J, F.detach()


def dense_lm_solve(u, G, p, kap8, m=1, maxit=40, lam0=1e-3, verbose=False, tol=1e-10):
    """Dense Gauss-Newton/LM (direct normal-equation solve) -- the 2-D-validated
    strategy; converges far better than matrix-free CG.  For small 3-D grids."""
    u = u.detach().clone()
    lam = lam0
    F = residual_vector(u, G, p, kap8, m=m)
    Phi = float((F*F).sum()); hist = [Phi]
    I = torch.eye(u.numel(), device=u.device)
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = jacobian_dense(u, G, p, kap8, m=m)
        JTJ = J.t() @ J; JTF = J.t() @ F
        accepted = False
        for _try in range(8):
            try:
                du = torch.linalg.solve(JTJ + lam*I, -JTF)
            except Exception:
                lam *= 4.0; continue
            un = u + du
            Pn = float((residual_vector(un, G, p, kap8, m=m)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.3, 1e-13); accepted = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [dlm] it={it:3d} Phi={Phi:.3e} lam={lam:.1e} {'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    return u, hist


def lm_solve(u, G, p, kap8, m=1, maxit=40, lam0=1e-3, verbose=False, tol=1e-9):
    u = u.detach().clone()
    lam = lam0
    Phi = phi(u, G, p, kap8, m=m)
    hist = [Phi]
    for it in range(maxit):
        if Phi < tol:
            break
        du, _ = lm_step(u, G, p, kap8, lam, m=m)
        accepted = False
        for _try in range(6):
            un = u + du
            Pn = phi(un, G, p, kap8, m=m)
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.5, 1e-12); accepted = True
                break
            lam *= 4.0
            du, _ = lm_step(u, G, p, kap8, lam, m=m)
        hist.append(Phi)
        if verbose:
            print(f"  [lm] it={it:3d} Phi={Phi:.3e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    return u, hist


# ---------------------------------------------------------------------------
# round #56 seed embedded in the 3-D grid (a=a(r),b=b(r),c=d=0,Theta=Theta(r))
# ---------------------------------------------------------------------------
def round_seed(G, p=0.4, kap8=0.05):
    import spectral_radial_soliton as SR
    sol = SR.solve(G.Nr-1, rc=G.rc, cell=G.ri-G.rc, p=p, kap8=kap8, maxit=80, tol=1e-12)
    assert np.allclose(G.r.cpu().numpy(), sol['r']), "radial node mismatch"
    def E(f):
        return torch.tensor(f, device=DEV)[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
    a, b, c, d, Th = E(sol['a']), E(sol['b']), z.clone(), z.clone(), E(sol['Th'])
    return pack(a, b, c, d, Th), sol


if __name__ == "__main__":
    print("=== full-3-D solver smoke: residual on round seed (should be near floor) ===")
    G = Grid3D(40, 8, 8, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=0.4, kap8=0.05)
    F = residual_vector(u0, G, 0.4, 0.05)
    print(f"  round seed Phi = {float((F*F).sum()):.3e}  (#56 M_MS={sol['M_MS']:.5f})")
