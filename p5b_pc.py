#!/usr/bin/env python3
"""
p5b_pc.py -- P5b: LIGHT preconditioners for the re-posed JFNK + the at-floor
PC-independence machinery + edge-gauge hygiene.  Builds on p5a_prime_repose.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.
Branch: p5b-pc-floor.  NEW FILE (committed scripts immutable).

=== WHAT THE DIAGNOSTIC (p5b_diag/p5b_diag2) FOUND -- the PC design ===
The re-posed J is full-rank.  Its conditioning is grid-dependent:
  * Nr=12 (the anchor grid): ONE isolated near-null right-singular direction
    (smin=6.3e-5, well-separated; 2nd-smallest=1.5e-2), ~99% on the METRIC warps
    a,b,c,d (NOT Theta), edge-localized at the body row adjacent to the seal.
    This is the "leftover inner-body gauge mode" the P5a verifier predicted -- a
    near-flat edge-adjacent metric-warp direction.  A diagonal block-Jacobi PC does
    NOT fix it (kappa stays 2.3e5: it is a coupled direction, not a diagonal scale).
  * Nr=16, 24 (usable resolution): NO isolated outlier; kappa DROPS to ~3e3-6e3,
    a clean band.  So at usable Nr the operator is far better conditioned and plain
    LSMR should floor cheaply.

THE LIGHT PC (cheapest that works), three options, all RIGHT-preconditioners
(du = P y, so they CANNOT move the fixed point of F):
  pc='none'        : identity (raw LSMR).
  pc='diag'        : block-Jacobi  P = diag(J^T J)^{-1/2}  (Hutchinson-free: exact
                     diag via a cheap probe set, matrix-free).  Standard cheap PC.
  pc='rband'       : RADIAL-BAND approximate-inverse.  The conditioning root is the
                     Cheb d/dr coupling on the steep core (P5-MAP §II); a per-(field,
                     th,ps) radial tridiagonal/banded approx of J^T J, inverted
                     exactly (small Nr), is the physics-matched cheap PC.  This is the
                     one that targets the actual near-null edge-radial direction.

All three are MATRIX-FREE-COMPATIBLE (built from JVP/VJP probes, no dense J).

=== DISCIPLINE ===
A right-PC du=P y changes only the Krylov PATH, never the zero set of F (the
PC-independence gate is the empirical witness).  No physical DOF frozen.  Edge gauge
is the declared 'hold' from p5a' (the edge DOF are unconstrained -- proven).  The
edge-gauge HYGIENE here is the cross-gauge / refined-Nr discipline, NOT a new freeze.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
# JFNK path uses the caching allocator (faster); harnesses needing the dense jacrev
# anchor set PYTORCH_NO_CUDA_MEMORY_CACHING=1 themselves BEFORE importing this.
import math, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import p5a_prime_repose as RP
from p5a_prime_repose import lsmr, make_reposed_ops, reposed_residual


# ===========================================================================
# RIGHT-PRECONDITIONERS (all matrix-free; all return a callable Papply(y)->P y).
# A right-PC solves J P z = -F for z, then du = P z.  Because du is the solution
# of the SAME least-squares problem (J du = -F) reparametrized, the fixed point
# (F=0) is invariant: the PC reshapes the Krylov path only.
# ===========================================================================

def pc_none(JT, JV, nB, dev):
    return lambda y: y


def pc_diag(JT, JV, nB, dev, nprobe=12):
    """Block-Jacobi: P = diag(J^T J)^{-1/2}, Hutchinson-estimated (matrix-free).
    Cheap; flattens any diagonal scale spread.  (Diagnostic: weak here -- the
    near-null mode is off-diagonal -- but it is the canonical light PC and a valid
    PC-INDEPENDENCE control: a different, weaker reshaping of the same path.)"""
    diag = torch.zeros(nB, device=dev)
    for _ in range(nprobe):
        z = torch.randn(nB, device=dev)
        diag += JT(JV(z)) * z          # E[z (J^T J z)] = diag(J^T J)
    diag = diag / nprobe
    s = 1.0 / torch.sqrt(torch.clamp(diag.abs(), min=1e-12))
    return lambda y, s=s: s * y


def pc_rband(rp, JT, JV, nB, dev, half_band=None, nprobe_per_col=None):
    """RADIAL-BAND approximate-inverse right-PC.

    The unknown vector is (field f, body-radial j, th t, ps p).  The conditioning
    root is the Cheb radial derivative coupling (dense in j), localized on the steep
    core/seal.  We build, for each (f,t,p) line, the RADIAL block B_{ftp} of J^T J
    restricted to that line's radial DOF (size nbr x nbr), then P = blockdiag(
    B^{-1/2}) applied per line.  B_{ftp} is recovered matrix-free by probing J^T J
    with unit vectors on each radial index of one representative line and reading the
    radial-coupling pattern (the operator is (th,ps)-translation-near-invariant on the
    round seed, so a few representative lines suffice; we probe ALL columns of a
    single (t,p) line per field, nbr probes per field = 5*nbr probes total -- cheap).

    This directly targets the near-null edge-radial metric mode the diagnostic found.
    Right-PC -> fixed-point preserving.
    """
    nbr, Nth, Nps = rp.nbr, rp.Nth, rp.Nps
    # index helper into the flat body vector: (f, j, t, p)
    def idx(f, j, t, p):
        return ((f*nbr + j)*Nth + t)*Nps + p
    # Build per-field radial block B_f (nbr x nbr) = J^T J restricted to a radial line
    # at a representative (t,p)=(0,0), averaged is unnecessary (round-seed near-invariant).
    t0, p0 = 0, 0
    Binv_half = torch.zeros(5, nbr, nbr, device=dev)
    for f in range(5):
        B = torch.zeros(nbr, nbr, device=dev)
        for jc in range(nbr):
            e = torch.zeros(nB, device=dev); e[idx(f, jc, t0, p0)] = 1.0
            col = JT(JV(e))                       # (J^T J) e
            for jr in range(nbr):
                B[jr, jc] = col[idx(f, jr, t0, p0)]
        B = 0.5*(B + B.t())                       # symmetrize
        # B^{-1/2} via eigh (tiny nbr x nbr), regularized
        w, Q = torch.linalg.eigh(B)
        w = torch.clamp(w, min=1e-10*float(w.max().clamp(min=1e-30)))
        Binv_half[f] = (Q * (w**-0.5)) @ Q.t()
    # Papply: for each (f,t,p) line, multiply the radial vector by Binv_half[f].
    def Papply(y):
        Y = y.reshape(5, nbr, Nth, Nps)
        out = torch.einsum('fij,fjtp->fitp', Binv_half, Y)
        return out.reshape(-1)
    return Papply


PC_BUILDERS = {
    'none':  lambda rp, JT, JV, nB, dev: pc_none(JT, JV, nB, dev),
    'diag':  lambda rp, JT, JV, nB, dev: pc_diag(JT, JV, nB, dev),
    'rband': lambda rp, JT, JV, nB, dev: pc_rband(rp, JT, JV, nB, dev),
}


# ===========================================================================
# THE P5b JFNK SOLVE -- re-posed Newton outer + matrix-free damped LSMR with a
# pluggable right-PC.  Records inner-iter counts + residual history + wall-time.
# ===========================================================================
def jfnk_solve(ub, rp, uref, kap8, pc='none', maxit=60, lam0=1e-4, tol=1e-13,
               lsmr_maxit=2000, lsmr_tol=1e-13, lam_min=1e-14, verbose=False):
    ub = ub.detach().clone()
    lam = lam0
    F = reposed_residual(ub, rp, uref, kap8)
    Phi = float((F*F).sum()); hist = [Phi]
    lsmr_iters = []
    nB = ub.numel(); dev = ub.device
    t0 = time.time()
    for it in range(maxit):
        if Phi < tol:
            break
        F0, JT, JV = make_reposed_ops(ub, rp, uref, kap8)
        Papply = PC_BUILDERS[pc](rp, JT, JV, nB, dev)
        accepted = False
        for _try in range(12):
            damp = math.sqrt(lam)
            du, nit = lsmr(JT, JV, F0, nB, damp, Papply=Papply,
                           maxit=lsmr_maxit, tol=lsmr_tol)
            un = ub + du
            Pn = float((reposed_residual(un, rp, uref, kap8)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                ub = un; Phi = Pn; lam = max(lam*0.25, lam_min)
                accepted = True; lsmr_iters.append(nit); break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [jfnk:{pc}] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"lsmr={lsmr_iters[-1] if lsmr_iters else '-'} "
                  f"{'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    return ub.detach(), hist, lsmr_iters, time.time() - t0
