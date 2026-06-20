#!/usr/bin/env python3
"""
p2_residual_fullmetric.py -- PHASE 2 residual: the P1 8-field general-Einstein system
with the matter sector replaced by the NATIVE S^2 carrier whose EL now VARIES ON THE
FULL OFF-DIAGONAL METRIC (the P1 gap closed).

Driver: Claude (Opus 4.8, 1M).  2026-06-19/20.  OBSERVE mode.  DATA-BLIND.  NEW file.
Builds on p1_residual_general_einstein (the validated pole-stable general Einstein +
the live spatial off-diagonals) and p2_matter_s2_fullmetric (the S^2 unit field, the
full-metric autograd EL, the divT field).

DIFFERENCE FROM P1 (exactly the two P2 closures):
  (1) MATTER FIELD: native S^2 UNIT 3-vector n=(sinF cos mps, sinF sin mps, cosF), free
      profile F(r,th,ps) -- NOT the S^3 4-vector field_n of P1.  (Settled carrier.)
  (2) MATTER EL: the autograd EL of S=int sqrt(-g)(L2+L4) on the FULL off-diagonal
      metric g_full -- NOT full3d_spectral.matter_el_3d (which is the DIAGONAL analytic
      EL, blind to e_rt,e_rp,e_tp).  This is the P1 gap P2 closes.

Everything else identical to P1: pole-stable hybrid general Einstein (off-diagonals live
+ back-reacting), deg-1 node core (NO Skyrme m*pi), a=-1 (P3), time row zeroed (P4),
B=1/A FREE.

NOTE on the Jacobian: the autograd EL uses torch.autograd.grad internally, which is NOT
jacrev/vmap-composable.  So the P2 residual is differentiated by FINITE DIFFERENCE (the
matter EL block) where needed, or the whole residual by a column-FD Jacobian.  This is a
TRACTABILITY choice (the no-cache allocator + nested autograd) -- it does not change the
physics; the residual itself is the exact full nonlinear system.  Flagged in the ledger.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import build_metric, T, R, TH, PS, PI
from full3d_newton import inv4x4, det4x4
from p1_residual_general_einstein import einstein_general_hybrid, unpack8, pack8
import p2_matter_s2_fullmetric as P2


def residual_vector_p2(u, G, p, kap8, m=1, wbc=30.0, core_mode="deg1"):
    """P2 residual: P1 general-Einstein system + native S^2 full-metric EL.

    core_mode: "deg1" (native, default) = charge-1 sector, node F[core]=pi -> F[seal]=0
      (pi is a NODE value, sin pi=0; NOT the m*pi ladder).  "free" = agnostic node
      F'(core)=0 (value free) -- the negative control that unwinds to vacuum (stage1a).
    """
    a, b, c, d, F, e_rt, e_rp, e_tp = unpack8(u, G)
    # general (pole-stable hybrid) Einstein, off-diagonals live
    Gmix, g = einstein_general_hybrid(G, a, b, c, d, e_rt, e_rp, e_tp)
    ginv = inv4x4(g)
    # NATIVE S^2 stress on the FULL metric
    dn = P2.field_dn_s2(G, F, m=m)
    Tab, _, _, _ = P2.stress_s2_fullmetric(g, ginv, dn)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8 * Tmix
    # NATIVE S^2 EL on the FULL metric (autograd; sees off-diagonals)  -- THE P2 CLOSURE
    el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg * G.wvol_coord)
    W = W / W[G.body].mean()
    bod = G.body
    rows = []
    for (mm, nn) in [(T, T), (R, R), (TH, TH), (PS, PS), (R, TH), (R, PS), (TH, PS)]:
        rows.append((W * resE[..., mm, nn])[bod])
    rows.append((W * el)[bod])
    # ---- BC rows ----
    if core_mode == "free":
        rows.append(wbc * G.d_r(F)[0, :, :].reshape(-1))           # node, value free
    else:                                                          # deg1 charge-1 sector
        rows.append(wbc * (F[0, :, :].reshape(-1) - PI))           # F(core)=pi (NODE)
    rows.append(wbc * (F[-1, :, :].reshape(-1) - 0.0))             # F(seal)=0 (NODE)
    rows.append(wbc * a[-1, :, :].reshape(-1))                     # gauge a(seal)=0
    rows.append(wbc * (b[0, :, :].reshape(-1) + p))                # depth dial b(core)=-p
    rows.append(wbc * c[0, :, :].reshape(-1)); rows.append(wbc * c[-1, :, :].reshape(-1))
    rows.append(wbc * d[0, :, :].reshape(-1)); rows.append(wbc * d[-1, :, :].reshape(-1))
    for e in (e_rt, e_rp, e_tp):
        rows.append(wbc * e[0, :, :].reshape(-1))
        rows.append(wbc * e[-1, :, :].reshape(-1))
    return torch.cat([r.reshape(-1) for r in rows])


def component_residuals_p2(u, G, p, kap8, m=1, core_mode="deg1"):
    a, b, c, d, F, e_rt, e_rp, e_tp = unpack8(u, G)
    Gmix, g = einstein_general_hybrid(G, a, b, c, d, e_rt, e_rp, e_tp)
    ginv = inv4x4(g)
    dn = P2.field_dn_s2(G, F, m=m)
    Tab, _, _, _ = P2.stress_s2_fullmetric(g, ginv, dn)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8 * Tmix
    el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
    bod = G.body
    names = {(T, T): 'tt', (R, R): 'rr', (TH, TH): 'thth', (PS, PS): 'psps',
             (R, TH): 'rth', (R, PS): 'rps', (TH, PS): 'thps'}
    out = {nm: float(resE[..., mm, nn][bod].abs().max()) for (mm, nn), nm in names.items()}
    out['el'] = float(el[bod].abs().max())
    out['e_rt_max'] = float(e_rt[bod].abs().max())
    out['e_rp_max'] = float(e_rp[bod].abs().max())
    out['e_tp_max'] = float(e_tp[bod].abs().max())
    return out


# ===========================================================================
# COLUMN-FD JACOBIAN + damped Newton/LM.  (The autograd EL is not jacrev-safe;
# we use a column finite-difference Jacobian.  Tractability choice; the residual is
# the exact full nonlinear system.  Step size eps chosen ~1e-6 in field units.)
# ===========================================================================
def jacobian_fd_p2(u, G, p, kap8, m=1, wbc=30.0, core_mode="deg1", eps=1e-6):
    F0 = residual_vector_p2(u, G, p, kap8, m=m, wbc=wbc, core_mode=core_mode)
    nU = u.numel(); nF = F0.numel()
    J = torch.zeros(nF, nU, device=u.device)
    for j in range(nU):
        up = u.clone(); up[j] += eps
        um = u.clone(); um[j] -= eps
        Fp = residual_vector_p2(up, G, p, kap8, m=m, wbc=wbc, core_mode=core_mode)
        Fm = residual_vector_p2(um, G, p, kap8, m=m, wbc=wbc, core_mode=core_mode)
        J[:, j] = (Fp - Fm) / (2*eps)
    return J.detach(), F0.detach()


def newton_solve_p2(u, G, p, kap8, m=1, maxit=30, lam0=1e-3, tol=1e-11,
                    verbose=False, wbc=30.0, core_mode="deg1", eps=1e-6, lam_min=1e-13):
    import numpy as np
    u = u.detach().clone()
    lam = lam0
    F = residual_vector_p2(u, G, p, kap8, m=m, wbc=wbc, core_mode=core_mode)
    Phi = float((F*F).sum()); hist = [Phi]
    nU = u.numel(); I = torch.eye(nU, device=u.device)
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = jacobian_fd_p2(u, G, p, kap8, m=m, wbc=wbc, core_mode=core_mode, eps=eps)
        accepted = False
        for _try in range(12):
            try:
                Jaug = torch.cat([J, math.sqrt(lam)*I], 0)
                Faug = torch.cat([-F, torch.zeros(nU, device=u.device)], 0)
                du = torch.linalg.lstsq(Jaug, Faug).solution
            except Exception:
                lam *= 4.0; continue
            un = u + du
            Pn = float((residual_vector_p2(un, G, p, kap8, m=m, wbc=wbc,
                                           core_mode=core_mode)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.25, lam_min); accepted = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [p2-newton] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    return u.detach(), hist
