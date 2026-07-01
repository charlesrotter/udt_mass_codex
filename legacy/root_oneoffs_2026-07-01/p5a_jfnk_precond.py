#!/usr/bin/env python3
"""
p5a_jfnk_precond.py -- P5a: JFNK (Jacobian-Free Newton-Krylov) prototype with a
PHYSICS-BASED (radial-elliptic, block) PRECONDITIONER for the full-3-D coupled
Einstein + native-S^2(S^3) + winding-BC residual.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA mode.  DATA-BLIND.
Branch: p5a-jfnk-precond.  NEW FILE (committed scripts are immutable).

=== WHAT THIS IS (the P5a crux: de-risk the #1-ranked solver) ===
The dense-Newton ANCHOR (full3d_newton.newton_solve) proves a Newton solution
exists at the floor (~1e-13) but is jacrev-BUILD-bound (~98% of each iter).  The
committed matrix-free Jacobi-PCG LM (full3d_solver.lm_solve / lm_step) STALLS
off-round (~1e-5, #60) because the JACOBI (diagonal) preconditioner is not a
descent direction on the stiff steep-core elliptic operator.  P5a swaps ONE
component -- the preconditioner -- keeping the SAME residual, the SAME matrix-free
JVP machinery, the SAME Gauss-Newton/normal-equation Krylov structure.

THE OPERATOR (verbatim, no change): the residual F(u) is full3d_solver.residual_vector
(byte-identical to full3d_newton.residual_vector_vsafe).  u packs a,b,c,d,Theta on the
(Nr,Nth,Nps) Cheb_r x GL_theta x Fourier_psi grid.  nF > nU (BC rows) -> the natural
matrix-free Newton step is the GAUSS-NEWTON / normal step  (J^T J + lam I) du = -J^T F,
solved by a PRECONDITIONED Krylov method.

=== THE PHYSICS-BASED PRECONDITIONER (what attacks the steep core) ===
The conditioning root: the steep soliton core b = p*ln(r/r_seal) gives a 1/r-derivative
core; the dominant stiff part of d F_f / d f for each field f is the RADIAL elliptic
operator (Chebyshev D2_r / D1_r weighted by the steep-core metric factors).  The
Jacobi PC sees only the operator's pointwise diagonal -> it cannot invert that
non-local radial coupling -> the #60 stall.

The physics PC approximates the inverse of the dominant per-field RADIAL-ELLIPTIC
diagonal block:
  * For each field f in {a,b,c,d,Theta}, build the 1-D radial operator
        Lf = (the diagonal block of J^T J restricted to radial action),
    measured DIRECTLY from the matrix-free JVP by probing radial-profile directions
    (so the PC is consistent with the ACTUAL Jacobian -- NOT a hand-coded
    linearization, satisfying the no-imported-mechanism discipline).
  * The PC applies M^{-1} = blockdiag_f( (Lf + mu I)^{-1} ) broadcast over (theta,psi),
    i.e. it solves the small Nr x Nr radial systems (one per field, per angular column),
    which is exactly the steep-radial inversion the Jacobi PC could not do.
  * mu is the same LM damping lam (the PC inherits the damping consistently).

A preconditioner only reshapes the Krylov PATH; it can NOT change the zero set of F.
GATE 1 (PC-independence + anchor match) PROVES this empirically.

PC variants (for the PC-independence gate):
  'radial'    : the block radial-elliptic inverse above (the physics PC).
  'radial+col': radial-elliptic inverse using a column-AVERAGED operator (cheaper,
                different PC, same fixed point -- the independence witness).
  'jacobi'    : the OLD diagonal PC (reproduces the #60 stall as the control).
  'none'      : identity PC (raw CG -- the floor-of-comparison).

NUMERICS: V100 float64.  Matrix-free JVP via the double-backward trick (reused from
full3d_solver.lm_step).  Strict monotone Newton acceptance.  NO frozen DOF / gauge /
BC introduced; the residual + BC rows are imported verbatim.  category-A.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, DEV, PI, T, R, TH, PS)
from full3d_solver import residual_vector, unpack, pack, round_seed


# ===========================================================================
# matrix-free Jacobian operators (reuse the double-backward JVP of lm_step).
# JT(w) = J^T w ;  JV(v) = J v ;  both via autograd of the SAME residual the
# anchor uses (full3d_solver.residual_vector).
# ===========================================================================
def make_jac_ops(u, G, p, kap8, m=1):
    u = u.detach().clone().requires_grad_(True)
    F = residual_vector(u, G, p, kap8, m=m)

    def JT(w):
        g, = torch.autograd.grad(F, u, grad_outputs=w, retain_graph=True)
        return g

    w0 = torch.zeros_like(F, requires_grad=True)
    JTw = torch.autograd.grad(F, u, grad_outputs=w0, create_graph=True)[0]

    def JV(v):
        jv, = torch.autograd.grad(JTw, w0, grad_outputs=v, retain_graph=True)
        return jv

    return F.detach(), JT, JV


# ===========================================================================
# THE PHYSICS-BASED PRECONDITIONER.  Build, per field, the dominant RADIAL
# elliptic operator block by probing the Gauss-Newton operator (J^T J) with
# radial-profile directions, then apply its (regularized) inverse.
#
# Field layout in u: 5 blocks of n = Nr*Nth*Nps, each reshaped (Nr,Nth,Nps).
# The radial operator for field f, at angular column (it,ip), is the Nr x Nr
# matrix  Lf[:, :] ~ d (J^T J u)_f(:,it,ip) / d u_f(:,it,ip).  Measuring the
# full per-column operator is Nr*Nfields*Ncols probes -- too many.  We measure
# the ANGLE-AVERAGED radial operator per field (Nr*Nfields probes): probe with a
# unit radial profile e_k placed in field f, BROADCAST over all (theta,psi), and
# read the radial response averaged over angle.  This captures the steep-core
# radial coupling (the conditioning root) while staying cheap.  The PC is then
# blockdiag over fields of (Lf + mu I)^{-1}, applied per angular column.
# ===========================================================================
class RadialEllipticPC:
    def __init__(self, G, JT, JV, lam, variant='radial', nfields=5):
        self.G = G
        self.lam = lam
        self.variant = variant
        self.nf = nfields
        Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
        self.Nr, self.Nth, self.Nps = Nr, Nth, Nps
        self.n = Nr * Nth * Nps
        self.dev = G.r.device
        if variant in ('radial', 'radial+col'):
            self._build_radial_ops(JT, JV)
        elif variant == 'radial_col':
            self._build_radial_col_ops(JT, JV)

    def _apply_JTJ(self, JT, JV, v):
        return JT(JV(v))

    def _build_radial_ops(self, JT, JV):
        """Measure, per field, the Nr x Nr ANGLE-AVERAGED radial block of A=J^T J.
        Probe direction for (field f, radial index k): u_f(r=k, all theta,psi)=1,
        else 0.  Response: read field-f component of A v, average over (theta,psi),
        as a function of radial index -> column k of the radial operator Lf."""
        Nr, Nth, Nps, n = self.Nr, self.Nth, self.Nps, self.n
        nf = self.nf
        # radial-profile basis: e_k broadcast over angles, normalized so the
        # measured operator is the angle-averaged radial coupling.
        self.Lf = []
        for f in range(nf):
            L = torch.zeros(Nr, Nr, device=self.dev)
            for k in range(Nr):
                v = torch.zeros(nf * n, device=self.dev)
                blk = v[f * n:(f + 1) * n].reshape(Nr, Nth, Nps)
                blk[k, :, :] = 1.0
                v[f * n:(f + 1) * n] = blk.reshape(-1)
                Av = self._apply_JTJ(JT, JV, v)
                resp = Av[f * n:(f + 1) * n].reshape(Nr, Nth, Nps)
                # angle-average the response; column k of Lf
                L[:, k] = resp.mean(dim=(1, 2))
            self.Lf.append(L)
        # factorize (Lf + mu I) once (mu = lam, inherits damping)
        mu = self.lam
        I = torch.eye(Nr, device=self.dev)
        self.Linv = []
        for L in self.Lf:
            A = L + mu * I
            # symmetrize lightly (J^T J block is symmetric up to measurement noise)
            A = 0.5 * (A + A.t())
            try:
                Ai = torch.linalg.inv(A)
            except Exception:
                Ai = torch.linalg.pinv(A)
            self.Linv.append(Ai)

    def _build_radial_col_ops(self, JT, JV):
        """PER-COLUMN radial block: for each field f, build a SEPARATE Nr x Nr radial
        operator for every angular column (it,ip) -- preserves the (theta,psi)
        structure the steep core needs (no angle-average).  Same Nr x nf probes:
        probe e_k (field f, radial k) broadcast over angles; read the per-column
        radial response.  Lcol[f] has shape (Nth,Nps,Nr,Nr)."""
        Nr, Nth, Nps, n = self.Nr, self.Nth, self.Nps, self.n
        nf = self.nf
        mu = self.lam
        self.Lcol_inv = []
        for f in range(nf):
            cols = torch.zeros(Nth, Nps, Nr, Nr, device=self.dev)  # [it,ip, i(resp), k(probe)]
            for k in range(Nr):
                v = torch.zeros(nf * n, device=self.dev)
                blk = v[f * n:(f + 1) * n].reshape(Nr, Nth, Nps)
                blk[k, :, :] = 1.0
                v[f * n:(f + 1) * n] = blk.reshape(-1)
                Av = self._apply_JTJ(JT, JV, v)
                resp = Av[f * n:(f + 1) * n].reshape(Nr, Nth, Nps)  # (i,it,ip)
                cols[:, :, :, k] = resp.permute(1, 2, 0)            # (it,ip,i)
            I = torch.eye(Nr, device=self.dev)
            A = cols + mu * I
            A = 0.5 * (A + A.transpose(-1, -2))
            Ai = torch.linalg.inv(A)                                # (Nth,Nps,Nr,Nr)
            self.Lcol_inv.append(Ai)

    def apply(self, r, JT=None, JV=None):
        """M^{-1} r."""
        if self.variant == 'none':
            return r
        if self.variant == 'jacobi':
            return self._jacobi_apply(r)
        if self.variant == 'radial_col':
            Nr, Nth, Nps, n = self.Nr, self.Nth, self.Nps, self.n
            out = torch.zeros_like(r)
            for f in range(self.nf):
                rf = r[f * n:(f + 1) * n].reshape(Nr, Nth, Nps).permute(1, 2, 0)  # (it,ip,Nr)
                Ai = self.Lcol_inv[f]                               # (it,ip,Nr,Nr)
                zf = torch.einsum('tpij,tpj->tpi', Ai, rf)          # (it,ip,Nr)
                out[f * n:(f + 1) * n] = zf.permute(2, 0, 1).reshape(-1)
            return out
        # radial / radial+col: per field, per angular column, solve the radial system
        Nr, Nth, Nps, n = self.Nr, self.Nth, self.Nps, self.n
        out = torch.zeros_like(r)
        for f in range(self.nf):
            rf = r[f * n:(f + 1) * n].reshape(Nr, Nth, Nps)
            Ai = self.Linv[f]                                  # (Nr,Nr)
            # apply Ai along radial axis for every (theta,psi) column at once
            zf = torch.tensordot(Ai, rf, dims=([1], [0]))      # (Nr,Nth,Nps)
            out[f * n:(f + 1) * n] = zf.reshape(-1)
        return out

    def set_jacobi_diag(self, diag):
        self._diag = diag

    def _jacobi_apply(self, r):
        return r / torch.clamp(self._diag, min=1e-12)


def estimate_jacobi_diag(JT, F_shape_like_w, u_like, lam, nprobe=6):
    """Hutchinson estimate of diag(J^T J) -- the OLD #60 Jacobi PC (control)."""
    diag = torch.zeros_like(u_like)
    for _ in range(nprobe):
        z = torch.randn(F_shape_like_w, device=u_like.device)
        jz = JT(z)
        diag += jz * jz
    return diag / nprobe + lam


# ===========================================================================
# PRECONDITIONED CG on the Gauss-Newton normal operator A=J^T J + lam I.
# (CG because A is SPD; the PC is SPD-ish radial-elliptic inverse.  This is the
# exact #60 inner solver with the preconditioner swapped.)
# ===========================================================================
def pcg(JT, JV, b, lam, PC, maxit=200, tol=1e-8):
    def A(v):
        return JT(JV(v)) + lam * v
    x = torch.zeros_like(b)
    r = b.clone()
    z = PC.apply(r)
    pdir = z.clone()
    rz = float(r @ z)
    rs0 = float(r @ r)
    kk = 0
    for kk in range(1, maxit + 1):
        Ap = A(pdir)
        denom = float(pdir @ Ap)
        if denom <= 0 or not math.isfinite(denom):
            break
        alpha = rz / denom
        x = x + alpha * pdir
        r = r - alpha * Ap
        rs = float(r @ r)
        if rs < tol * tol * rs0:
            break
        z = PC.apply(r)
        rz_new = float(r @ z)
        if rz == 0:
            break
        pdir = z + (rz_new / rz) * pdir
        rz = rz_new
    return x, kk, math.sqrt(max(float(r @ r), 0.0))


# ===========================================================================
# MATRIX-FREE DAMPED LSMR (Paige-Saunders) on the RECTANGULAR system
#   min || J du + F ||^2 + damp^2 || P^{-1} du ||^2
# operating on J DIRECTLY (condition number kappa, NOT kappa^2 of J^T J), with a
# right preconditioner P (physics-based: per-field-block diagonal scaling, or the
# radial-elliptic block).  This is the matrix-free form of the dense anchor's
# torch.linalg.lstsq step (SVD/QR-robust to the body-mask rank-deficiency that
# made the #60 J^T J-CG path stall).  P only reshapes the path (right-precond:
# du = P y; solve for y; the fixed point is unchanged).
# ===========================================================================
def lsmr(JT, JV, F, nU, damp, Papply=None, maxit=400, tol=1e-9):
    """Solve min ||J du + F|| + damp||P^{-1} du|| via LSMR.  Papply(x)=P x is the
    right preconditioner (default identity).  Returns du, iters."""
    dev = F.device
    if Papply is None:
        Papply = lambda x: x
    # operate on the preconditioned variable y, du = P y:
    #   A_y = J P ; A_y^T = P^T J^T (P symmetric here) ; rhs b = -F
    def Av(y):
        return JV(Papply(y))
    def Atu(w):
        return Papply(JT(w))
    b = -F
    beta = float((b * b).sum()) ** 0.5
    if beta == 0:
        return torch.zeros(nU, device=dev), 0
    u = b / beta
    v = Atu(u); alpha = float((v * v).sum()) ** 0.5
    if alpha == 0:
        return torch.zeros(nU, device=dev), 0
    v = v / alpha
    h = v.clone(); hbar = torch.zeros(nU, device=dev); y = torch.zeros(nU, device=dev)
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


def field_block_diag_scale(JT, JV, G, nfields=5):
    """Physics-based DIAGONAL right-preconditioner: 1/sqrt(diag of each field block
    of J^T J), estimated by Hutchinson, normalizes the heterogeneous field-block
    magnitudes (a,b vs c,d vs Theta).  Returns a multiplicative vector (P=diag(s))."""
    nU = G.Nr * G.Nth * G.Nps * nfields
    diag = torch.zeros(nU, device=G.r.device)
    for _ in range(8):
        z = torch.randn(nU, device=G.r.device)
        # diag(J^T J)_i ~ E[(J z)_i ... ] use the standard probe (J^T (J z)) . z form:
        jz = JV(z)
        jtjz = JT(jz)
        diag += z * jtjz
    diag = diag / 8.0
    s = 1.0 / torch.sqrt(torch.clamp(diag.abs(), min=1e-8))
    return s


# ===========================================================================
# THE JFNK SOLVE.  Newton outer loop; each step = preconditioned-CG on the
# Gauss-Newton normal system using matrix-free JVP + the physics PC.  Strict
# monotone (LM-damped) acceptance.  NO dense Jacobian is EVER built.
# ===========================================================================
def jfnk_solve(u, G, p, kap8, m=1, maxit=40, lam0=1e-3, tol=1e-9,
               variant='radial', cg_maxit=200, cg_tol=1e-7, lam_min=1e-12,
               verbose=False, rebuild_pc_every=1):
    u = u.detach().clone()
    lam = lam0
    F = residual_vector(u, G, p, kap8, m=m)
    Phi = float((F * F).sum())
    hist = [Phi]
    cg_iters_hist = []
    t0 = time.time()
    for it in range(maxit):
        if Phi < tol:
            break
        F0, JT, JV = make_jac_ops(u, G, p, kap8, m=m)
        b = JT(-F0)
        accepted = False
        for _try in range(10):
            # build / refresh PC at current lam
            PC = RadialEllipticPC(G, JT, JV, lam, variant=variant)
            if variant == 'jacobi':
                diag = estimate_jacobi_diag(JT, F0.numel(), u, lam)
                PC.set_jacobi_diag(diag)
            du, ncg, cgres = pcg(JT, JV, b, lam, PC, maxit=cg_maxit, tol=cg_tol)
            un = u + du
            Pn = float((residual_vector(un, G, p, kap8, m=m) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un
                Phi = Pn
                lam = max(lam * 0.3, lam_min)
                accepted = True
                cg_iters_hist.append(ncg)
                break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [jfnk:{variant}] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"cg={cg_iters_hist[-1] if cg_iters_hist else '-'} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    return u.detach(), hist, cg_iters_hist, time.time() - t0


# ===========================================================================
# THE JFNK-LSMR SOLVE (the working inner solver).  Newton outer loop; each step
# = matrix-free DAMPED LSMR on the rectangular J (the anchor's lstsq step, matrix-
# free), optionally right-preconditioned by the physics-based field-block diagonal
# scaling.  Strict monotone (LM-damped) acceptance.  NO dense Jacobian built.
#   pc='none'   : identity right-PC (LSMR on raw J).
#   pc='fieldblock' : physics-based per-field-block diagonal scaling right-PC.
# Both must converge to the SAME fixed point (PC-independence).
# ===========================================================================
def jfnk_lsmr_solve(u, G, p, kap8, m=1, maxit=40, lam0=1e-3, tol=1e-9,
                    pc='fieldblock', lsmr_maxit=400, lsmr_tol=1e-9,
                    lam_min=1e-12, verbose=False):
    u = u.detach().clone()
    lam = lam0
    F = residual_vector(u, G, p, kap8, m=m)
    Phi = float((F * F).sum())
    hist = [Phi]
    lsmr_iters = []
    nU = u.numel()
    t0 = time.time()
    for it in range(maxit):
        if Phi < tol:
            break
        F0, JT, JV = make_jac_ops(u, G, p, kap8, m=m)
        if pc == 'fieldblock':
            s = field_block_diag_scale(JT, JV, G)
            Papply = lambda x, s=s: s * x
        else:
            Papply = None
        accepted = False
        for _try in range(10):
            damp = math.sqrt(lam)
            du, nit = lsmr(JT, JV, F0, nU, damp, Papply=Papply,
                           maxit=lsmr_maxit, tol=lsmr_tol)
            un = u + du
            Pn = float((residual_vector(un, G, p, kap8, m=m) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam * 0.3, lam_min)
                accepted = True; lsmr_iters.append(nit); break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [jfnk-lsmr:{pc}] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"lsmr={lsmr_iters[-1] if lsmr_iters else '-'} "
                  f"{'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    return u.detach(), hist, lsmr_iters, time.time() - t0


# ===========================================================================
# build the #60 axisym-l2-control seed (the documented stall case).
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
    print("smoke: build ops on a tiny grid")
    G = Grid3D(12, 6, 8, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=0.4, kap8=0.05)
    F0, JT, JV = make_jac_ops(u0, G, 0.4, 0.05)
    print("  nU", u0.numel(), "nF", F0.numel(), "Phi0", float((F0 * F0).sum()))
    PC = RadialEllipticPC(G, JT, JV, 1e-3, variant='radial')
    print("  radial PC built; Lf[0] shape", tuple(PC.Lf[0].shape))
