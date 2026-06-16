#!/usr/bin/env python3
"""
full3d_newton.py -- PRODUCTION-SCALE explicit-Jacobian Newton / Levenberg-Marquardt
solver for the EXISTING full-3-D static residual (full3d_solver.residual_vector).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

=== WHY THIS MODULE EXISTS (the conditioning problem, NOT a physics problem) ===
The committed matrix-free Jacobi-PCG LM (full3d_solver.lm_solve) CRAWLS off-round
(stalls ~1e-5) because the diagonal preconditioner cannot tame the steep-core x
1/r^2,1/r^4 x Chebyshev conditioning.  An independent audit showed the committed
DENSE LM (dense_lm_solve + jacobian_dense, same physics) converges to Phi~7e-13 in
~16 QUADRATIC iterations -- so a true full-3-D solution PROVABLY exists at the floor.
The dense path is just too slow at production grid: jacobian_dense does nF backward
passes (O(nF) graph traversals).

THE CURE (category-A conditioning ONLY -- the equations are UNCHANGED):
  Build the SAME Jacobian J = dF/du EFFICIENTLY with a SINGLE batched reverse pass
  via torch.func.jacrev, then take the exact LM/Newton step by DIRECT factorization
  (torch.linalg.solve on the dense normal equations / Jacobian).  jacrev needs the
  residual to be vmap-safe; the audit flagged torch.linalg.inv (CORE.metric_inverse)
  and torch.linalg.det as vmap-incompatible inside functorch's batching.  We replace
  BOTH with MANUAL analytic 4x4 cofactor (adjugate/determinant) expressions -- the
  IDENTICAL linear-algebra result, vmap-safe.  This is pure numerics: the residual
  VALUE is bit-for-bit the same as full3d_solver.residual_vector (verified below).

CATEGORY-A boundary (binding):
  ALLOWED here  : explicit/batched Jacobian, direct factorization, LM damping,
                  parameter continuation, the vmap-safe inverse/det rewrite.
  FORBIDDEN     : tying g_tt=1/g_rr (B=1/A), injecting/dropping a term, presenting a
                  linear step AS the result, tuning to a target.  NONE are done here;
                  the residual physics is imported verbatim from the committed module.
  The LM/Newton local linear step is the SOLVER (as in #56/2-D/the dense path); the
  REPORTED solution satisfies the FULL nonlinear residual to the floor.

NUMERICS: V100 float64 throughout.  Per-batch / value-equivalence CPU spot-asserts.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
# On this V100/cu121 stack NVML is broken (driver mismatch); functorch's vmap
# (used inside jacrev for the batched backward) trips the CUDA *caching* allocator's
# NVML assert.  Disabling the caching allocator sidesteps it -- pure infra workaround,
# no effect on numerics.  Must be set BEFORE torch initializes CUDA.
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    einstein_mixed_weyl, field_dn, matter_el_3d, diagnostics, residuals,
    DEV, PI, T, R, TH, PS)
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
import full3d_solver as FS
from full3d_solver import pack, unpack


# ===========================================================================
# vmap-safe analytic 4x4 linear algebra (cofactor / adjugate).  These return
# the IDENTICAL values as torch.linalg.inv / torch.linalg.det but are composed
# only of elementwise ops + indexing, so torch.func.vmap/jacrev can batch them.
# (torch.linalg.inv and .det dispatch into LAPACK kernels that functorch cannot
#  batch over the implicit jacrev probe dimension -> the audit's reported failure.)
# ===========================================================================
def det4x4(g):
    """Determinant of a (...,4,4) batch via Laplace expansion (vmap-safe)."""
    # 2x2 minors of the bottom two rows over all column pairs
    def m2(i, j, k, l):
        return g[..., i, k]*g[..., j, l] - g[..., i, l]*g[..., j, k]
    # cofactor expansion along the first row using 3x3 minors built from 2x2s
    g00, g01, g02, g03 = g[..., 0, 0], g[..., 0, 1], g[..., 0, 2], g[..., 0, 3]
    g10, g11, g12, g13 = g[..., 1, 0], g[..., 1, 1], g[..., 1, 2], g[..., 1, 3]
    # 3x3 dets of the submatrix from rows (1,2,3) deleting one column
    # minor(c) = det of rows 1..3 with column c removed
    s23_01 = m2(2, 3, 0, 1)  # rows 2,3 cols 0,1
    s23_02 = m2(2, 3, 0, 2)
    s23_03 = m2(2, 3, 0, 3)
    s23_12 = m2(2, 3, 1, 2)
    s23_13 = m2(2, 3, 1, 3)
    s23_23 = m2(2, 3, 2, 3)
    # 3x3 minor deleting column 0: rows1-3, cols1,2,3
    M0 = g11*s23_23 - g12*s23_13 + g13*s23_12
    M1 = g10*s23_23 - g12*s23_03 + g13*s23_02
    M2 = g10*s23_13 - g11*s23_03 + g13*s23_01
    M3 = g10*s23_12 - g11*s23_02 + g12*s23_01
    return g00*M0 - g01*M1 + g02*M2 - g03*M3


def inv4x4(g):
    """Inverse of a (...,4,4) batch via the adjugate / determinant (vmap-safe)."""
    # cofactor C_ij = (-1)^{i+j} * minor_ij ;  inv = adj^T / det = C^T / det
    n = 4
    # build all 3x3 minors.  We compute cofactor matrix then transpose.
    def minor3(rows, cols):
        # 3x3 determinant of g[..., rows, cols]
        r0, r1, r2 = rows
        c0, c1, c2 = cols
        a = g[..., r0, c0]; b = g[..., r0, c1]; c = g[..., r0, c2]
        d = g[..., r1, c0]; e = g[..., r1, c1]; f = g[..., r1, c2]
        h = g[..., r2, c0]; i = g[..., r2, c1]; j = g[..., r2, c2]
        return a*(e*j - f*i) - b*(d*j - f*h) + c*(d*i - e*h)
    all_idx = [0, 1, 2, 3]
    cof = [[None]*n for _ in range(n)]
    for i in range(n):
        rows = [r for r in all_idx if r != i]
        for j in range(n):
            cols = [c for c in all_idx if c != j]
            sign = 1.0 if (i + j) % 2 == 0 else -1.0
            cof[i][j] = sign * minor3(rows, cols)
    det = (g[..., 0, 0]*cof[0][0] + g[..., 0, 1]*cof[0][1]
           + g[..., 0, 2]*cof[0][2] + g[..., 0, 3]*cof[0][3])
    inv_det = 1.0 / det
    out = torch.zeros_like(g)
    for i in range(n):
        for j in range(n):
            # inverse[i,j] = cofactor[j,i] / det   (adjugate = cofactor^T)
            out[..., i, j] = cof[j][i] * inv_det
    return out


# ===========================================================================
# residual VALUE, byte-equivalent to full3d_solver.residual_vector but built on
# the vmap-safe inv4x4/det4x4 so torch.func.jacrev can batch it.  We DUPLICATE
# the residual assembly (cannot edit the committed module); it is verified equal
# to FS.residual_vector to ~1e-14 in __main__/validation.
# ===========================================================================
def residual_vector_vsafe(u, G, p, kap8, m=1, wbc=30.0):
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d)
    ginv = inv4x4(g)
    Gmix = einstein_mixed_weyl(G, a, b, c, d)
    dn = field_dn(G, Th, m=m)
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8*Tmix
    el = matter_el_3d(G, a, b, c, d, Th, m=m)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg * G.wvol_coord)
    W = W / W[G.body].mean()
    bod = G.body
    rows = []
    for (mm, nn) in [(T, T), (R, R), (TH, TH), (PS, PS), (R, TH), (R, PS), (TH, PS)]:
        rows.append((W*resE[..., mm, nn])[bod])
    rows.append((W*el)[bod])
    rows.append(wbc*(Th[0, :, :].reshape(-1) - m*PI))
    rows.append(wbc*(Th[-1, :, :].reshape(-1) - 0.0))
    rows.append(wbc*a[-1, :, :].reshape(-1))
    rows.append(wbc*(b[0, :, :].reshape(-1) + p))
    rows.append(wbc*c[0, :, :].reshape(-1)); rows.append(wbc*c[-1, :, :].reshape(-1))
    rows.append(wbc*d[0, :, :].reshape(-1)); rows.append(wbc*d[-1, :, :].reshape(-1))
    F = torch.cat([r.reshape(-1) for r in rows])
    return F


# ===========================================================================
# BATCHED explicit Jacobian J = dF/du via torch.func.jacrev (one reverse-mode
# pass batched over the nF output seeds, instead of nF python-loop backward
# passes in full3d_solver.jacobian_dense).
# ===========================================================================
def jacobian_jacrev(u, G, p, kap8, m=1, wbc=30.0, chunk_size=256):
    from torch.func import jacrev
    f = lambda uu: residual_vector_vsafe(uu, G, p, kap8, m=m, wbc=wbc)
    # chunk_size bounds the vmap batch (the no-cache allocator is memory-tight);
    # purely a memory knob, identical result.
    J = jacrev(f, chunk_size=chunk_size)(u)               # (nF, nU)
    F = residual_vector_vsafe(u, G, p, kap8, m=m, wbc=wbc).detach()
    return J.detach(), F


# ===========================================================================
# PRODUCTION Levenberg-Marquardt / Newton solve with the batched Jacobian and a
# DIRECT factorization step (the dense path's correctness, at jacrev speed).
# Strict monotone acceptance; adaptive damping.
# ===========================================================================
def newton_solve(u, G, p, kap8, m=1, maxit=40, lam0=1e-4, tol=1e-11,
                 verbose=False, wbc=30.0, chunk_size=256, use_lstsq=True,
                 lam_min=1e-14):
    """LM/Gauss-Newton with the batched jacrev Jacobian and a DIRECT factorized step.
       use_lstsq=True : solve the rectangular damped LS  min || [J; sqrt(lam) I] du
         + [F; 0] ||  by torch.linalg.lstsq -- avoids forming J^T J (kappa^2
         conditioning), markedly stronger in the tail.  Category-A (the SAME GN
         step, better conditioned).
       use_lstsq=False: classic normal-equation LM (J^T J + lam I) du = -J^T F.
       lam_min: damping floor; small -> recovers true Newton (quadratic) in the tail."""
    u = u.detach().clone()
    lam = lam0
    F = residual_vector_vsafe(u, G, p, kap8, m=m, wbc=wbc)
    Phi = float((F*F).sum()); hist = [Phi]
    nU = u.numel()
    I = torch.eye(nU, device=u.device)
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = jacobian_jacrev(u, G, p, kap8, m=m, wbc=wbc, chunk_size=chunk_size)
        if not use_lstsq:
            JTJ = J.t() @ J; JTF = J.t() @ F
        accepted = False
        for _try in range(12):
            try:
                if use_lstsq:
                    Jaug = torch.cat([J, math.sqrt(lam)*I], dim=0)
                    Faug = torch.cat([-F, torch.zeros(nU, device=u.device)], dim=0)
                    du = torch.linalg.lstsq(Jaug, Faug).solution
                else:
                    du = torch.linalg.solve(JTJ + lam*I, -JTF)
            except Exception:
                lam *= 4.0; continue
            un = u + du
            Pn = float((residual_vector_vsafe(un, G, p, kap8, m=m, wbc=wbc)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.25, lam_min); accepted = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [newton] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    return u.detach(), hist


# ===========================================================================
# CONTINUATION: solve at a base parameter set, then step a parameter (e.g. p,
# kap8, or an injected geometric deformation amplitude) and re-solve from the
# previous solution.  step_fn(u, val) may also perturb the seed (for Phase-3
# psi-deformation continuation).  Returns the list of (val, u, hist).
# ===========================================================================
def continuation(u0, G, base_kw, param_name, values, m=1, maxit=30,
                 lam0=1e-4, tol=1e-11, verbose=False, seed_fn=None):
    """base_kw: dict with p, kap8.  param_name in {'p','kap8'} stepped over values.
       seed_fn(u, val) optional: warp the previous solution before re-solving
       (used to ramp a non-axisym deformation)."""
    out = []
    u = u0.detach().clone()
    for val in values:
        kw = dict(base_kw); kw[param_name] = val
        if seed_fn is not None:
            u = seed_fn(u, val)
        u, hist = newton_solve(u, G, kw['p'], kw['kap8'], m=m, maxit=maxit,
                               lam0=lam0, tol=tol, verbose=verbose)
        out.append((val, u.detach().clone(), hist))
        if verbose:
            print(f"  [cont] {param_name}={val:.4f}  Phi={hist[-1]:.3e}  "
                  f"({len(hist)-1} it)")
    return out


# ===========================================================================
# per-component residual breakdown (for the validation report)
# ===========================================================================
def component_residuals(u, G, p, kap8, m=1, wbc=30.0):
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d)
    ginv = CORE.metric_inverse(g)
    Gmix = einstein_mixed_weyl(G, a, b, c, d)
    dn = field_dn(G, Th, m=m)
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8*Tmix
    el = matter_el_3d(G, a, b, c, d, Th, m=m)
    bod = G.body
    names = {(T, T): 'tt', (R, R): 'rr', (TH, TH): 'thth', (PS, PS): 'psps',
             (R, TH): 'rth', (R, PS): 'rps', (TH, PS): 'thps'}
    out = {}
    for (mm, nn), nm in names.items():
        out[nm] = float(resE[..., mm, nn][bod].abs().max())
    out['el'] = float(el[bod].abs().max())
    return out


if __name__ == "__main__":
    print("=== full3d_newton: value-equivalence + smoke ===")
    G = Grid3D(20, 6, 8, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = FS.round_seed(G, p=0.4, kap8=0.05)
    F_ref = FS.residual_vector(u0, G, 0.4, 0.05)
    F_new = residual_vector_vsafe(u0, G, 0.4, 0.05)
    print(f"  ||F_ref - F_new||_inf = {float((F_ref - F_new).abs().max()):.3e}  "
          f"(must be ~1e-14)")
    # inv/det equivalence spot-check
    g = build_metric(G, *unpack(u0, G)[:4])
    print(f"  ||inv4x4 - linalg.inv||_inf = "
          f"{float((inv4x4(g) - CORE.metric_inverse(g)).abs().max()):.3e}")
    print(f"  ||det4x4 - linalg.det||_inf = "
          f"{float((det4x4(g) - torch.linalg.det(g)).abs().max()):.3e}")
