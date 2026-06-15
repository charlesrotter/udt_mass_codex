#!/usr/bin/env python3
"""
complete_metric_stageB_fast.py -- FAST batched engine for the Stage-B sweep.

Repo discipline: the committed Stage-A engine complete_metric_batched.py is
IMMUTABLE (commit 33d3a50).  This module does NOT edit it -- it REUSES its exact
physics (theta_ddot, stress, energy_pieces, phi_from_source, grad_central) verbatim
and only REPLACES the linear-algebra inner kernel: the committed engine solves the
TRIDIAGONAL Newton system with a DENSE (B,N,N) torch.linalg.solve (O(N^3) per
member -- ~28 s/member at N=700, B=1, which makes the full sweep intractable).
Here the SAME tridiagonal Newton system is solved with a batched THOMAS algorithm
(O(N) per member; the V100-safe explicit path -- NO solve_triangular with a
broadcast Cholesky factor, the known cu121 corruption).  The PHYSICS is identical;
only the solver speed changes.  Cross-checked against the committed engine to
machine precision in the Stage-B script (must match res + profile).

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  DATA-BLIND.  torch float64, V100.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
import complete_metric_batched as cm   # REUSE the committed physics verbatim

torch.set_default_dtype(torch.float64)
DEV = cm.DEV
PI = math.pi
TWO_PI = cm.TWO_PI

theta_ddot   = cm.theta_ddot
grad_central = cm.grad_central
stress       = cm.stress
energy_pieces = cm.energy_pieces
phi_from_source = cm.phi_from_source


def thomas_batched(a, b, c, d):
    """Batched tridiagonal solve by PARALLEL CYCLIC REDUCTION (PCR): ~log2(N)
    vectorized GPU passes instead of N sequential ones (the sequential Thomas is
    launch-bound on the V100 -- 600 kernels/solve).  a=sub (B,N) [a[:,0]=0],
    b=diag (B,N), c=super (B,N) [c[:,-1]=0], d=rhs (B,N).  Returns x (B,N).
    Explicit elementwise ops only -- V100-safe (no solve_triangular, no Cholesky).
    Cross-checked vs the committed dense LU to machine precision in the Stage-B run."""
    a = a.clone(); b = b.clone(); c = c.clone(); d = d.clone()
    B, N = b.shape
    a[:, 0] = 0.0; c[:, -1] = 0.0
    idx = torch.arange(N, device=b.device)
    span = 1
    def shift_down(t, s):   # value of node i-s (0 where none)
        out = torch.zeros_like(t); out[:, s:] = t[:, :-s]; return out
    def shift_up(t, s):     # value of node i+s (0 where none)
        out = torch.zeros_like(t); out[:, :-s] = t[:, s:]; return out
    while span < N:
        has_dn = (idx - span >= 0)
        has_up = (idx + span < N)
        b_dn = shift_down(b, span); a_dn = shift_down(a, span)
        c_dn = shift_down(c, span); d_dn = shift_down(d, span)
        b_up = shift_up(b, span);  a_up = shift_up(a, span)
        c_up = shift_up(c, span);  d_up = shift_up(d, span)
        # alpha_i = -a_i/b_{i-span} (0 if no down neighbour); beta_i = -c_i/b_{i+span}
        alpha = torch.where(has_dn, -a / torch.where(b_dn == 0, torch.ones_like(b_dn), b_dn),
                            torch.zeros_like(a))
        beta = torch.where(has_up, -c / torch.where(b_up == 0, torch.ones_like(b_up), b_up),
                           torch.zeros_like(c))
        b = b + alpha*c_dn + beta*a_up
        d = d + alpha*d_dn + beta*d_up
        a = alpha*a_dn
        c = beta*c_up
        span *= 2
    return d / b


def solve_theta_fast(r, phi, xi, kap, m=1, Th_init=None, iters=200, tol=1e-12,
                     damp=1.0):
    """Same nonlinear angular EL Newton solve as cm.solve_theta_batched, but the
    tridiagonal Jacobian is solved by Thomas (O(N)) instead of dense LU.  Returns
    (Th, max|F|_interior).  Physics (theta_ddot, stencil) reused verbatim."""
    B, N = r.shape
    phip = grad_central(phi, r)
    if Th_init is None:
        L = math.sqrt(kap/xi); rc = r[:, :1]
        Th = (m*PI)*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
    else:
        Th = Th_init.clone()
    Th[:, 0] = m*PI; Th[:, -1] = 0.0
    h_m = r[:, 1:-1] - r[:, :-2]; h_p = r[:, 2:] - r[:, 1:-1]
    a_lo = 2.0*h_p/(h_m*h_p*(h_m+h_p))
    a_di = -2.0*(h_m+h_p)/(h_m*h_p*(h_m+h_p))
    a_hi = 2.0*h_m/(h_m*h_p*(h_m+h_p))

    def residual(Tcur):
        Thp = grad_central(Tcur, r)
        Thpp = torch.zeros_like(Tcur)
        Thpp[:, 1:-1] = a_lo*Tcur[:, :-2] + a_di*Tcur[:, 1:-1] + a_hi*Tcur[:, 2:]
        rhs = theta_ddot(r, Tcur, Thp, phi, phip, xi, kap, m=m)
        F = torch.zeros_like(Tcur)
        F[:, 1:-1] = Thpp[:, 1:-1] - rhs[:, 1:-1]
        F[:, 0] = Tcur[:, 0] - m*PI
        F[:, -1] = Tcur[:, -1] - 0.0
        return F

    last = None; eps = 1e-7
    for it in range(iters):
        F = residual(Th)
        last = F[:, 1:-1].abs().amax(dim=1).max().item()
        if last < tol:
            break
        # Tridiagonal Jacobian bands (B,N).  Analytic d2 stencil + colored-FD of
        # the -rhs(Th,Thp) coupling (rhs depends on Th_i and, via central-diff Thp,
        # on Th_{i-1},Th_{i+1}; both land on the tridiagonal band).
        sub = torch.zeros(B, N, device=r.device)
        dia = torch.zeros(B, N, device=r.device)
        sup = torch.zeros(B, N, device=r.device)
        dia[:, 1:-1] += a_di; sub[:, 1:-1] += a_lo; sup[:, 1:-1] += a_hi
        Thp0 = grad_central(Th, r)
        rhs0 = theta_ddot(r, Th, Thp0, phi, phip, xi, kap, m=m)
        for color in range(3):
            cols = torch.arange(color, N, 3, device=r.device)
            cols = cols[(cols >= 1) & (cols <= N-2)]
            if cols.numel() == 0:
                continue
            Tp = Th.clone(); Tp[:, cols] += eps
            drhs = (theta_ddot(r, Tp, grad_central(Tp, r), phi, phip, xi, kap, m=m)
                    - rhs0)/eps
            # row c: d/dTh_c -> diag; rows c-1,c+1 see Tp via central diff -> off-diag.
            dia[:, cols] += -drhs[:, cols]
            lo = cols[cols-1 >= 1];  sup[:, lo-1] += -drhs[:, lo-1]   # J[lo-1, lo]
            hi = cols[cols+1 <= N-2]; sub[:, hi+1] += -drhs[:, hi+1]  # J[hi+1, hi]
        # BC rows
        dia[:, 0] = 1.0; sup[:, 0] = 0.0
        dia[:, -1] = 1.0; sub[:, -1] = 0.0
        dia = dia + 1e-12
        dTh = thomas_batched(sub, dia, sup, -F)
        Th = Th + damp*dTh
        Th[:, 0] = m*PI; Th[:, -1] = 0.0
        Th = torch.clamp(Th, -0.5, m*PI + 0.5)
    return Th, last


def selfconsistent_fast(r, xi, kap, m=1, p=0.8, kap8=8*math.pi, iters=80,
                        relax=0.5, tol=1e-10, Th_init=None, theta_iters=120):
    """Two-way self-consistent solve, identical structure to cm.selfconsistent_batched
    but using solve_theta_fast (Thomas).  phi update reuses cm.phi_from_source."""
    B, N = r.shape
    L = math.sqrt(kap/xi); rc = r[:, :1]
    if Th_init is None:
        Th = (m*PI)*0.5*(1 - torch.tanh((r - (rc + 2*L))/(0.8*L)))
    else:
        Th = Th_init.clone()
    phi = p*torch.log(r/r[:, -1:])
    hist = []
    for it in range(iters):
        Th_new, res_th = solve_theta_fast(r, phi, xi, kap, m=m, Th_init=Th,
                                           iters=theta_iters, tol=1e-12, damp=1.0)
        Thp = grad_central(Th_new, r)
        phi_new, m_areal, m_closed = phi_from_source(r, Th_new, Thp, phi, xi, kap, p, kap8)
        dphi = (phi_new - phi).abs().amax(dim=1).max().item()
        dTh = (Th_new - Th).abs().amax(dim=1).max().item()
        phi = (1-relax)*phi + relax*phi_new
        Th = Th_new
        hist.append((it, dphi, dTh, res_th))
        if dphi < tol and dTh < tol:
            break
    Thp = grad_central(Th, r)
    X, Y, rho, pr = stress(r, Th, Thp, phi, xi, kap)
    E2, E4 = energy_pieces(r, Th, phi, xi, kap, m=m)
    phi_f, m_areal, m_closed = phi_from_source(r, Th, Thp, phi, xi, kap, p, kap8)
    M_MS = m_areal[:, -1] - m_areal[:, :1].squeeze(1)
    return dict(r=r, Th=Th, Thp=Thp, phi=phi, X=X, Y=Y, rho=rho, pr=pr,
                E2=E2, E4=E4, M_MS=M_MS, m_areal=m_areal, m_closed=m_closed, hist=hist)
