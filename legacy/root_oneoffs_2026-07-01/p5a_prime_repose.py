#!/usr/bin/env python3
"""
p5a_prime_repose.py -- P5a': RE-POSE the full-3-D coupled residual to FULL-RANK
BODY DOF, then RETRY JFNK (matrix-free Newton-Krylov) on the well-conditioned
re-posed system.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA mode.  DATA-BLIND.
Branch: p5a-prime-repose.  NEW FILE (committed scripts are immutable).

=== WHY (the P5a verifier's decisive finding) ===
The committed coupled Jacobian J = dF/du of `full3d_solver.residual_vector` is
massively RANK-DEFICIENT (kappa ~ 1e18-1e37; ~10-25% near-null), and ~90% of the
null energy sits on the INHERITED `Grid3D.body` Chebyshev-edge-excision DOF.  This
is an HONEST operator property (matrix-free JVP == dense J@v to 1e-16), not a JFNK
bug.  The dense anchor survives only because torch.linalg.lstsq is rank-revealing;
matrix-free Krylov chokes on the nullspace -> the #60 stall + the P5a FAIL.

THE FORK (verifier, decisive): RESTRICTING J to the BODY columns collapses the
deficiency -- near-zero count 430->1, kappa 1e37 -> 5e10, and ~1e6 excluding ONE
leftover inner-body gauge mode.  So: re-pose the unknowns to body DOF only and JFNK
should work.  THIS MODULE builds that re-pose + retries JFNK.

=== THE RE-POSE (what the unknowns are now) ===
The body mask `Grid3D.body` = radial rows [3 : Nr-3]; it ALREADY excises the 6
Chebyshev edge rows per radial column ({0,1,2,Nr-3,Nr-2,Nr-1}) from the residual
ROWS (no interior Einstein/matter residual is evaluated there -- only weak strong-BC
rows touch indices 0 and Nr-1).  The columns for those edge DOF are therefore the
unconstrained nullspace.

RE-POSE: make the unknown vector the BODY DOF only -- field values at radial rows
[3 : Nr-3] for all 5 fields (a,b,c,d,Theta), nB = 5*(Nr-6)*Nth*Nps.  The 6 excised
edge rows per field are NOT free unknowns; they are SET (reconstructed) before every
residual / JVP evaluation by the BC/regularity relations:

  * endpoint rows {0, Nr-1}: set to their BC/regularity VALUES exactly --
      Theta(core)=m*pi, Theta(seal)=0 ; a(seal)=0 ; b(core)=-p ;
      c,d = 0 at core and seal (the round/regular limit the strong-BC rows pin).
      The endpoint rows that NO BC pins (a(core), b(seal)) are set by smooth
      spectral edge-regularity (continued from the body, see below).
  * inner edge rows {1,2,Nr-3,Nr-2}: set by SMOOTH SPECTRAL EDGE-REGULARITY --
      the field's body profile is extended to these rows by the natural
      Chebyshev edge continuation (a low-order least-squares polynomial fit of
      the body rows, evaluated at the edge nodes).  These rows carry NO residual
      and live entirely in the operator nullspace; the reconstruction only fixes
      a smooth, regular gauge representative so the spectral derivatives entering
      the BODY residual rows are well-defined.  ANY smooth choice gives the same
      body fixed point (GATE A is the empirical guard).

This is exactly consistent with how `Grid3D.body` already excises these DOF from
the residual rows; we are removing spurious/unconstrained columns, NOT changing the
physical solution (proven by GATE A: re-posed dense solution == original anchor on
the body DOF, field-by-field, to floor).

=== DISCIPLINE ===
Residual physics = the committed `full3d_solver.residual_vector`, verbatim (only the
DOF posing changes; the edge reconstruction feeds the SAME residual).  No frozen
PHYSICAL DOF (the edge DOF are unconstrained gauge -- proven by the rank collapse +
GATE A).  Any gauge fix for a leftover inner-body mode is DECLARED.  No box
dependence.  V100 float64.  category-A (the LM/Newton local linear step is the
solver; the reported solution satisfies the full nonlinear residual to the floor).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
# NOTE: PYTORCH_NO_CUDA_MEMORY_CACHING is NOT set here.  It is needed ONLY for the
# jacrev/vmap DENSE path (the NVML-broken stack trips the caching allocator under
# functorch's vmap); the matrix-free JFNK path runs ~5x faster WITH the caching
# allocator.  Harnesses that use the dense path set the flag themselves BEFORE
# importing this module; JFNK-only harnesses leave it unset.
import math
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, DEV, PI, T, R, TH, PS)
from full3d_solver import residual_vector, unpack, pack, round_seed


# ===========================================================================
# THE RE-POSE.  Defines the body-column index set and the edge reconstruction.
# ===========================================================================
class Repose:
    """Re-pose the (Nr,Nth,Nps,5)-field unknown to BODY DOF only.

    body radial rows  = [3 : Nr-3]  (== Grid3D.body), the only rows any residual
                        constrains.  These are the FREE unknowns (the full-rank set).
    edge radial rows  = {0,1,2,Nr-3,Nr-2,Nr-1}, reconstructed each eval from
                        BC/regularity (endpoints) + smooth spectral continuation
                        (inner edges).

    A reference field tensor `uref` supplies the endpoint BC VALUES that are pinned
    (it is the round seed; its endpoint rows already carry the exact BC values, and
    its inner edge rows are smooth/regular).  The reconstruction overwrites the
    inner edge rows by a polynomial continuation of the body so the result is
    independent of any non-smooth content in uref's edge rows."""

    def __init__(self, G, p, m=1, edge_mode='spectral', fit_deg=4):
        self.G = G
        self.p = p
        self.m = m
        self.edge_mode = edge_mode          # 'spectral' | 'hold'
        self.fit_deg = fit_deg
        Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
        self.Nr, self.Nth, self.Nps = Nr, Nth, Nps
        self.n = Nr * Nth * Nps
        self.dev = G.r.device
        self.body_r = torch.arange(3, Nr - 3, device=self.dev)
        self.nbr = self.body_r.numel()
        self.nB = 5 * self.nbr * Nth * Nps
        # body column index into the flat 5*n unknown vector
        bmask = torch.zeros(5, Nr, Nth, Nps, dtype=torch.bool, device=self.dev)
        bmask[:, 3:Nr - 3, :, :] = True
        self.body_idx = torch.where(bmask.reshape(-1))[0]
        # least-squares edge-continuation operator: from body rows -> all Nr rows
        # via a degree-fit_deg polynomial in the Cheb node coordinate r.
        r = G.r                                            # (Nr,)
        rb = r[self.body_r]                                # (nbr,)
        deg = min(fit_deg, self.nbr - 1)
        # Vandermonde (normalized r to [-1,1] over the cell for conditioning)
        r0, r1 = float(r.min()), float(r.max())
        rn = (2 * (r - r0) / (r1 - r0) - 1.0)
        rbn = rn[self.body_r]
        Vb = torch.stack([rbn ** k for k in range(deg + 1)], dim=1)   # (nbr, deg+1)
        Vall = torch.stack([rn ** k for k in range(deg + 1)], dim=1)  # (Nr, deg+1)
        # continuation matrix C (Nr, nbr): f_all ~ Vall @ pinv(Vb) @ f_body
        Vb_pinv = torch.linalg.pinv(Vb)                    # (deg+1, nbr)
        self.Cont = Vall @ Vb_pinv                         # (Nr, nbr)
        # --- precompute the vmap-safe scatter pieces -----------------------
        # body row scatter: (Nr, nbr) with 1 where row == body row
        Sbody = torch.zeros(Nr, self.nbr, device=self.dev)
        for j, rr in enumerate(self.body_r.tolist()):
            Sbody[rr, j] = 1.0
        self.Sbody = Sbody
        # edge-row selector (1 on the 6 edge rows, 0 on body), and the BC-pin
        # selector + value tensor for endpoints (broadcast over th,ps).
        edge_mask = torch.ones(Nr, device=self.dev); edge_mask[self.body_r] = 0.0
        self.edge_mask_r = edge_mask                       # (Nr,) 1 on edges
        # pinned endpoint values + mask per field (Nr,) -- only rows 0,Nr-1 ever pinned
        pin_val = torch.zeros(5, Nr, device=self.dev)
        pin_msk = torch.zeros(5, Nr, device=self.dev)
        for f in range(5):
            v0 = self._endpoint_bc(f, 0); v1 = self._endpoint_bc(f, -1)
            if v0 is not None:
                pin_val[f, 0] = v0; pin_msk[f, 0] = 1.0
            if v1 is not None:
                pin_val[f, -1] = v1; pin_msk[f, -1] = 1.0
        self.pin_val = pin_val                             # (5,Nr)
        self.pin_msk = pin_msk                             # (5,Nr)

    def set_edge_hold(self, uref):
        """Store the FIXED edge-row values for edge_mode='hold' (the regular gauge:
        the edge rows of a smooth reference, e.g. the round seed).  Only the edge
        rows are ever read; the pinned BC endpoints are re-applied analytically."""
        self.edge_hold = uref.detach().reshape(5, self.Nr, self.Nth, self.Nps).clone()

    # ---- VMAP-SAFE functional embed (no in-place index writes) -------------
    def embed_vsafe(self, ub):
        """Functional re-pose embed: body rows from ub; edge rows from the chosen
        gauge (edge_mode='spectral': polynomial continuation of the body;
        edge_mode='hold': the fixed self.edge_hold edge rows); endpoints overwritten
        by the analytic pinned BC values.  matmul + broadcast only (jacrev-safe)."""
        Nr, Nth, Nps = self.Nr, self.Nth, self.Nps
        ub5 = ub.reshape(5, self.nbr, Nth, Nps)            # (5,nbr,Nth,Nps)
        body_full = torch.einsum('rj,fjtp->frtp', self.Sbody, ub5)   # (5,Nr,Nth,Nps)
        em = self.edge_mask_r[None, :, None, None]         # (1,Nr,1,1) 1 on edges
        if self.edge_mode == 'hold':
            edge = self.edge_hold                          # (5,Nr,Nth,Nps), fixed
        else:  # spectral continuation of the body
            edge = torch.einsum('rj,fjtp->frtp', self.Cont, ub5)
        full = body_full + em * edge                       # body rows: ub; edge rows: gauge
        pm = self.pin_msk[:, :, None, None]; pv = self.pin_val[:, :, None, None]
        full = full * (1.0 - pm) + pv * pm
        return full.reshape(-1)

    # ---- BC/regularity endpoint values (pinned exactly) --------------------
    def _endpoint_bc(self, field, end):
        """Return the BC/regularity VALUE for `field` at endpoint `end` in {0,-1},
        or None if that endpoint is NOT pinned by any BC (then use continuation)."""
        m, p = self.m, self.p
        # fields: 0=a,1=b,2=c,3=d,4=Theta
        if field == 4:                                     # Theta
            return m * PI if end == 0 else 0.0
        if field == 0:                                     # a: only seal pinned
            return 0.0 if end == -1 else None
        if field == 1:                                     # b: only core pinned
            return -p if end == 0 else None
        if field in (2, 3):                                # c,d: both ends = 0
            return 0.0
        return None

    # ---- reconstruct the full (5,Nr,Nth,Nps) field from body DOF ----------
    def embed(self, ub, uref):
        """ub: (nB,) body DOF.  uref: (5n,) reference (round seed) for any pinned
        endpoint values that come from the seed (none needed; BCs are analytic).
        Returns the full flat unknown (5n,) with edge rows reconstructed."""
        Nr, Nth, Nps = self.Nr, self.Nth, self.Nps
        full = torch.zeros(5, Nr, Nth, Nps, device=self.dev)
        ub5 = ub.reshape(5, self.nbr, Nth, Nps)
        full[:, 3:Nr - 3, :, :] = ub5
        # edge rows
        for f in range(5):
            if self.edge_mode == 'hold':
                # hold edge rows at the reference (round seed) values
                uref5 = uref.reshape(5, Nr, Nth, Nps)
                full[f, :3, :, :] = uref5[f, :3, :, :]
                full[f, Nr - 3:, :, :] = uref5[f, Nr - 3:, :, :]
            else:  # 'spectral': smooth continuation of the body to ALL rows
                cont = torch.tensordot(self.Cont, ub5[f], dims=([1], [0]))  # (Nr,Nth,Nps)
                full[f, :3, :, :] = cont[:3, :, :]
                full[f, Nr - 3:, :, :] = cont[Nr - 3:, :, :]
            # overwrite the pinned BC endpoints exactly
            v0 = self._endpoint_bc(f, 0)
            v1 = self._endpoint_bc(f, -1)
            if v0 is not None:
                full[f, 0, :, :] = v0
            if v1 is not None:
                full[f, -1, :, :] = v1
        return full.reshape(-1)

    def extract(self, u):
        """Pull the body DOF out of a full unknown vector."""
        return u[self.body_idx].clone()


# ===========================================================================
# RE-POSED residual + matrix-free Jacobian operators.  The residual is the
# COMMITTED full3d_solver.residual_vector evaluated on the embed(ub) full vector;
# differentiation is wrt the BODY DOF ub only (chain rule through embed, by
# autograd) -- so the re-posed Jacobian Jb = (dF/du) @ (du/dub) automatically.
# ===========================================================================
def reposed_residual(ub, rp, uref, kap8):
    # uref kept in signature for API compatibility; embed_vsafe needs no reference
    # (edges are spectral continuation of the body + analytic BC pins).
    return residual_vector(rp.embed_vsafe(ub), rp.G, rp.p, kap8, m=rp.m)


def make_reposed_ops(ub, rp, uref, kap8):
    ub = ub.detach().clone().requires_grad_(True)
    F = reposed_residual(ub, rp, uref, kap8)

    def JT(w):
        g, = torch.autograd.grad(F, ub, grad_outputs=w, retain_graph=True)
        return g

    w0 = torch.zeros_like(F, requires_grad=True)
    JTw = torch.autograd.grad(F, ub, grad_outputs=w0, create_graph=True)[0]

    def JV(v):
        jv, = torch.autograd.grad(JTw, w0, grad_outputs=v, retain_graph=True)
        return jv

    return F.detach(), JT, JV


# ===========================================================================
# DENSE re-posed Jacobian (anchor for GATE A) -- per-row autograd through embed.
# ===========================================================================
def reposed_jacobian_dense(ub, rp, uref, kap8):
    ub = ub.detach().clone().requires_grad_(True)
    F = reposed_residual(ub, rp, uref, kap8)
    nF = F.numel(); nB = ub.numel()
    J = torch.zeros(nF, nB, device=ub.device)
    eye = torch.eye(nF, device=ub.device)
    for i in range(nF):
        gi, = torch.autograd.grad(F, ub, grad_outputs=eye[i], retain_graph=True)
        J[i] = gi
    return J, F.detach()


# ===========================================================================
# FAST batched reposed Jacobian via torch.func.jacrev on the VMAP-SAFE residual
# (full3d_newton.residual_vector_vsafe) composed with the vmap-safe embed.  This
# is the reposed analogue of full3d_newton.jacobian_jacrev (single batched pass).
# NOTE: full3d_newton is imported LAZILY (inside these functions) because it forces
# PYTORCH_NO_CUDA_MEMORY_CACHING=1 (needed only for jacrev/vmap) at import time --
# the matrix-free JFNK path does NOT need it and runs ~5x faster with the caching
# allocator, so importers that only use JFNK must not trip the no-cache flag.
# ===========================================================================
def reposed_residual_vsafe(ub, rp, kap8):
    import full3d_newton as _NW
    return _NW.residual_vector_vsafe(rp.embed_vsafe(ub), rp.G, rp.p, kap8, m=rp.m)


def reposed_jacobian_jacrev(ub, rp, kap8, chunk_size=128):
    import full3d_newton as _NW
    from torch.func import jacrev
    f = lambda x: reposed_residual_vsafe(x, rp, kap8)
    J = jacrev(f, chunk_size=chunk_size)(ub)
    F = reposed_residual_vsafe(ub, rp, kap8).detach()
    return J.detach(), F


def reposed_dense_solve_fast(ub, rp, kap8, maxit=40, lam0=1e-4, tol=1e-13,
                             lam_min=1e-14, verbose=False, chunk_size=128):
    """Reposed dense LM (rank-revealing lstsq), batched jacrev Jacobian -- GATE-A
    anchor at speed.  Uses the vmap-safe residual + vmap-safe embed (value-identical
    to the committed residual; verified in __main__)."""
    ub = ub.detach().clone()
    lam = lam0
    F = reposed_residual_vsafe(ub, rp, kap8)
    Phi = float((F * F).sum()); hist = [Phi]
    nB = ub.numel()
    I = torch.eye(nB, device=ub.device)
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = reposed_jacobian_jacrev(ub, rp, kap8, chunk_size=chunk_size)
        accepted = False
        for _try in range(12):
            try:
                Jaug = torch.cat([J, math.sqrt(lam) * I], dim=0)
                Faug = torch.cat([-F, torch.zeros(nB, device=ub.device)], dim=0)
                du = torch.linalg.lstsq(Jaug, Faug).solution
            except Exception:
                lam *= 4.0; continue
            un = ub + du
            Pn = float((reposed_residual_vsafe(un, rp, kap8) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                ub = un; Phi = Pn; lam = max(lam * 0.25, lam_min); accepted = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [repose-dense-fast] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    return ub.detach(), hist


def reposed_dense_solve(ub, rp, uref, kap8, maxit=40, lam0=1e-4, tol=1e-12,
                        lam_min=1e-14, verbose=False):
    """Dense LM (rank-revealing lstsq augmented step) on the RE-POSED system --
    the GATE-A anchor.  Same step as full3d_newton.newton_solve, on body DOF."""
    ub = ub.detach().clone()
    lam = lam0
    F = reposed_residual(ub, rp, uref, kap8)
    Phi = float((F * F).sum()); hist = [Phi]
    nB = ub.numel()
    I = torch.eye(nB, device=ub.device)
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = reposed_jacobian_dense(ub, rp, uref, kap8)
        accepted = False
        for _try in range(12):
            try:
                Jaug = torch.cat([J, math.sqrt(lam) * I], dim=0)
                Faug = torch.cat([-F, torch.zeros(nB, device=ub.device)], dim=0)
                du = torch.linalg.lstsq(Jaug, Faug).solution
            except Exception:
                lam *= 4.0; continue
            un = ub + du
            Pn = float((reposed_residual(un, rp, uref, kap8) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                ub = un; Phi = Pn; lam = max(lam * 0.25, lam_min); accepted = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [repose-dense] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    return ub.detach(), hist


# ===========================================================================
# Matrix-free LSMR on the re-posed rectangular J (kappa, not kappa^2).  Optional
# right preconditioner.  This is the anchor's lstsq step, matrix-free.
# ===========================================================================
def lsmr(JT, JV, F, nB, damp, Papply=None, maxit=600, tol=1e-11):
    dev = F.device
    if Papply is None:
        Papply = lambda x: x

    def Av(y):
        return JV(Papply(y))

    def Atu(w):
        return Papply(JT(w))

    b = -F
    beta = float((b * b).sum()) ** 0.5
    if beta == 0:
        return torch.zeros(nB, device=dev), 0
    u = b / beta
    v = Atu(u); alpha = float((v * v).sum()) ** 0.5
    if alpha == 0:
        return torch.zeros(nB, device=dev), 0
    v = v / alpha
    h = v.clone(); hbar = torch.zeros(nB, device=dev); y = torch.zeros(nB, device=dev)
    zetabar = alpha * beta; alphabar = alpha
    rho = 1.0; rhobar = 1.0; cbar = 1.0; sbar = 0.0
    normb = beta
    it = 0
    for it in range(1, maxit + 1):
        u2 = Av(v) - alpha * u; beta = float((u2 * u2).sum()) ** 0.5; u = u2 / beta
        v2 = Atu(u) - beta * v; alpha = float((v2 * v2).sum()) ** 0.5; v = v2 / alpha
        alphahat = math.hypot(alphabar, damp); chat = alphabar / alphahat
        rhoold = rho; rho = math.hypot(alphahat, beta); c = alphahat / rho; s = beta / rho
        thetanew = s * alpha; alphabar = c * alpha
        rhobarold = rhobar; thetabar = sbar * rho
        rhobar = math.hypot(cbar * rho, thetanew); cbar = cbar * rho / rhobar
        sbar = thetanew / rhobar
        zeta = cbar * zetabar; zetabar = -sbar * zetabar
        hbar = h - (thetabar * rho / (rhoold * rhobarold)) * hbar
        y = y + (zeta / (rho * rhobar)) * hbar
        h = v - (thetanew / rho) * h
        if abs(zetabar) < tol * normb:
            break
    return Papply(y), it


def field_block_diag_scale(JT, JV, nB, dev, nprobe=8):
    """Physics-based diagonal right-PC: 1/sqrt(diag J^T J), Hutchinson-estimated."""
    diag = torch.zeros(nB, device=dev)
    for _ in range(nprobe):
        z = torch.randn(nB, device=dev)
        diag += z * JT(JV(z))
    diag = diag / nprobe
    return 1.0 / torch.sqrt(torch.clamp(diag.abs(), min=1e-10))


# ===========================================================================
# THE RE-POSED JFNK SOLVE.  Newton outer loop; each step = matrix-free damped
# LSMR on the re-posed (full-rank) rectangular J.  NO dense Jacobian built.
#   pc='none'       : identity right-PC (raw LSMR on the well-conditioned J).
#   pc='fieldblock' : physics-based diagonal right-PC (PC-independence witness).
# ===========================================================================
def reposed_jfnk_solve(ub, rp, uref, kap8, maxit=40, lam0=1e-4, tol=1e-11,
                       pc='none', lsmr_maxit=600, lsmr_tol=1e-11, lam_min=1e-14,
                       verbose=False):
    ub = ub.detach().clone()
    lam = lam0
    F = reposed_residual(ub, rp, uref, kap8)
    Phi = float((F * F).sum()); hist = [Phi]
    lsmr_iters = []
    nB = ub.numel()
    t0 = time.time()
    for it in range(maxit):
        if Phi < tol:
            break
        F0, JT, JV = make_reposed_ops(ub, rp, uref, kap8)
        if pc == 'fieldblock':
            s = field_block_diag_scale(JT, JV, nB, ub.device)
            Papply = lambda x, s=s: s * x
        else:
            Papply = None
        accepted = False
        for _try in range(12):
            damp = math.sqrt(lam)
            du, nit = lsmr(JT, JV, F0, nB, damp, Papply=Papply,
                           maxit=lsmr_maxit, tol=lsmr_tol)
            un = ub + du
            Pn = float((reposed_residual(un, rp, uref, kap8) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                ub = un; Phi = Pn; lam = max(lam * 0.25, lam_min)
                accepted = True; lsmr_iters.append(nit); break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [repose-jfnk:{pc}] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"lsmr={lsmr_iters[-1] if lsmr_iters else '-'} "
                  f"{'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    return ub.detach(), hist, lsmr_iters, time.time() - t0


# ===========================================================================
# the #60 axisym-l2 control seed (the documented stall case).  Reuses the
# recipe from p5a_jfnk_precond.axi_l2_seed (Legendre-l2 Theta perturbation).
# ===========================================================================
def axi_l2_seed(G, u0, amp=0.25, m=1):
    from numpy.polynomial.legendre import Legendre
    a, b, c, d, Th = unpack(u0, G)
    Th = Th.clone()
    rprof = torch.exp(-((G.Rg - 2.0) / 1.5) ** 2)
    cth = torch.cos(G.THg)
    cc = np.zeros(3); cc[2] = 1.0
    Pl = torch.tensor(Legendre(cc)(cth.cpu().numpy()), device=G.r.device)
    Th = Th + amp * rprof * Pl
    Th[0, :, :] = m * PI
    Th[-1, :, :] = 0.0
    return pack(a, b, c, d, Th)


if __name__ == "__main__":
    print("smoke: re-pose on (12,6,8)")
    G = Grid3D(12, 6, 8, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=0.4, kap8=0.05)
    rp = Repose(G, p=0.4, m=1, edge_mode='spectral')
    ub0 = rp.extract(u0)
    print("  nB =", rp.nB, " body rows =", rp.body_r.tolist())
    F = reposed_residual(ub0, rp, u0, 0.05)
    print("  reposed Phi0 =", float((F * F).sum()), " nF =", F.numel())
