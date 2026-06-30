#!/usr/bin/env python3
"""
kte_grid_measure.py -- CATEGORY-A numerical-conditioning MEASUREMENT (NO solve).

QUESTION: does a Kosloff-Tal-Ezer (KTE) mapped radial grid reduce the conditioning
of the determined-posing Jacobian (currently smax~7e6, cond~8e10), which is driven
by the O(N^2) Chebyshev endpoint differentiation-matrix amplification?

This is a STANDALONE measurement: it does NOT modify the production Grid3D and runs
NO nonlinear solve.  It rebuilds the determined Jacobian (via jacrev) at the analytic
seed on (a) the standard Chebyshev grid and (b) KTE-mapped grids for a sweep of alpha,
and reports smax / smin / cond (svdvals) plus a differentiation-accuracy self-test.

KTE map (Kosloff & Tal-Ezer JCP 104:457 (1993); Don & Solomonoff SIAM 1995):
  standard CGL nodes xi_j in [-1,1] with standard Cheb matrix D_xi;
  s_j = g(xi_j) = arcsin(alpha*xi_j)/arcsin(alpha),  alpha in (0,1)
        (alpha->0 recovers Chebyshev; alpha->1 -> equispaced);
  g'(xi) = alpha / (arcsin(alpha) * sqrt(1 - alpha^2 xi^2));
  D_s = diag(1/g'(xi_j)) @ D_xi;
  affine s in [-1,1] -> r in [rc,ri]:  r = rc + (ri-rc)(s+1)/2,
        so Dr_KTE = (2/(ri-rc)) diag(1/g'(xi)) @ D_xi.
The endpoint rows shrink because 1/g'(+-1) = arcsin(alpha) sqrt(1-alpha^2)/alpha is small.

CHOSE-OR-DERIVED (the FREE PHYSICS constants this linearization rides -- unchanged
from d1_determined_posing_check.py; we only swap the GRID MAP, a category-A param):
  X=-2e5 (CHOSEN placeholder, ledgered), xi=1.0 kap=1.0 (THEORY: units L=1),
  branch='G', kap8=1.0, p=1.0, m=1.  alpha = category-A grid map (soundness, not derivation).

Driver: Claude (Opus 4.8, 1M).  2026-06-29.  OBSERVE mode (measure, do not target).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from spectral_cheb import cheb, clenshaw_curtis_weights
from full3d_spectral import Grid3D, attach_coord_weight
import p1_residual_general_einstein as P1
from torch.func import jacrev


# ---------------------------------------------------------------------------
# KTE radial primitive (mirrors spectral_cheb.cheb_interval's flip-to-ascending,
# but inserts the KTE coordinate map between the CGL nodes and the affine [rc,ri]).
# ---------------------------------------------------------------------------
def kte_interval(N, lo, hi, alpha):
    """KTE-mapped nodes on [lo,hi] (ASCENDING) + matched d/dr matrix + CC weights.
    alpha->0 -> recovers cheb_interval(N,lo,hi) exactly."""
    xi, D = cheb(N)                                   # standard CGL nodes (desc) + Cheb D
    asin_a = np.arcsin(alpha)
    s = np.arcsin(alpha * xi) / asin_a                # KTE coordinate s in [-1,1] (desc)
    gp = alpha / (asin_a * np.sqrt(1.0 - (alpha * xi) ** 2))   # g'(xi) on the nodes
    Ds = (1.0 / gp)[:, None] * D                      # D_s = diag(1/g') @ D_xi
    r = 0.5 * (hi + lo) + 0.5 * (hi - lo) * s          # affine s->r (desc, r[0]=hi)
    Dr = (2.0 / (hi - lo)) * Ds                        # chain rule onto [lo,hi]
    # KTE quadrature weights: int f dr = int f * (dr/dxi) dxi; standard CC w_xi scaled by
    # (hi-lo)/2 already (= clenshaw on [lo,hi] for the affine map), times the extra g'(xi).
    w_aff = clenshaw_curtis_weights(N, lo, hi)         # ASCENDING, = w_xi*(hi-lo)/2
    gp_asc = gp[::-1]                                  # g' on ascending nodes
    # flip nodes+matrix to ascending r (r[0]=lo core)
    idx = np.arange(N, -1, -1)
    r = r[idx]
    Dr = Dr[np.ix_(idx, idx)]
    wr = w_aff * gp_asc                                # KTE integration weight
    return r, Dr, wr


# ---------------------------------------------------------------------------
# Build a KTE-mapped Grid3D variant: identical to Grid3D except the radial
# nodes / Dr / wr are KTE-mapped.  alpha=None -> untouched standard grid.
# ---------------------------------------------------------------------------
def make_grid(Nr, Nth, Nps, rc, cell, alpha=None):
    G = Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=rc, cell=cell)
    if alpha is not None:
        r, Dr, wr = kte_interval(Nr - 1, rc, rc + cell, alpha)
        dev = G.dev
        G.r = torch.tensor(r, device=dev)
        G.Dr = torch.tensor(Dr, device=dev)
        G.wr = torch.tensor(wr, device=dev)
        # rebroadcast radial coordinate field and recompute the coordinate volume weight
        G.Rg = G.r[:, None, None].expand(Nr, Nth, Nps).contiguous()
        G.wvol = (G.wr[:, None, None] * G.wmu[None, :, None]
                  * G.wps[None, None, :])
    attach_coord_weight(G)    # sets wvol_coord from (possibly KTE) G.wr
    return G


# ---------------------------------------------------------------------------
# conditioning measurement on a given grid
# ---------------------------------------------------------------------------
def jac_cond(G, u, label):
    f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=-2e5, branch='G',
                                         determined=True)
    J = jacrev(f, chunk_size=128)(u)
    sv = torch.linalg.svdvals(J.double()).cpu().numpy()
    smax, smin = sv[0], sv[-1]
    cond = smax / smin
    print(f"  [{label}] rows={J.shape[0]} smax={smax:.4e} smin={smin:.4e} "
          f"cond={cond:.4e}", flush=True)
    return smax, smin, cond


def accuracy_test(G, Nr, rc, ri):
    """Differentiate two smooth test fns with G.Dr (radial 1-D) vs analytic.
    f1 = exp(-r) (gently varying); f2 = 1/r (core-steep)."""
    r = G.r.cpu().numpy()
    Dr = G.Dr.cpu().numpy()
    f1 = np.exp(-r); f1p = -np.exp(-r)
    e1 = np.max(np.abs(Dr @ f1 - f1p))
    f2 = 1.0 / r; f2p = -1.0 / r ** 2
    e2 = np.max(np.abs(Dr @ f2 - f2p))
    return e1, e2


def main():
    Nr, Nth, Nps, rc, cell = 8, 6, 8, 0.1, 8.0
    ri = rc + cell
    ncols = 11 * Nr * Nth * Nps
    print("=" * 78)
    print("KTE CONDITIONING MEASUREMENT (determined Jacobian, jacrev, svdvals)")
    print(f"grid Nr={Nr} Nth={Nth} Nps={Nps} rc={rc} cell={cell}  cols={ncols}")
    print("linearization point = seed_round_native (analytic in the nodes; adapts to map)")
    print("=" * 78)

    # ---- 1. STANDARD-GRID BASELINE ----
    print("\n[1] STANDARD CHEBYSHEV GRID (baseline / sanity):")
    Gstd = make_grid(Nr, Nth, Nps, rc, cell, alpha=None)
    u = P1.seed_round_native(Gstd, p=1.0, m=1)
    base = jac_cond(Gstd, u, "std,seed")
    torch.manual_seed(0)
    u_n = P1.seed_round_native(Gstd, p=1.0, m=1) + 1e-3 * torch.randn(ncols, device=Gstd.dev)
    jac_cond(Gstd, u_n, "std,seed+1e-3noise")
    e1, e2 = accuracy_test(Gstd, Nr, rc, ri)
    print(f"  accuracy: max|Dr exp(-r) - f'|={e1:.3e}   max|Dr (1/r) - f'|={e2:.3e}")

    # ---- 2+3. KTE SWEEP (conditioning + accuracy together) ----
    print("\n[2/3] KTE SWEEP (alpha -> smax, smin, cond, d-matrix accuracy):")
    hdr = f"  {'alpha':>7} | {'smax':>11} {'smin':>11} {'cond':>11} | {'err exp(-r)':>12} {'err 1/r':>12}"
    print(hdr); print("  " + "-" * (len(hdr) - 2))
    a_std, b_std, c_std = base
    e1_std, e2_std = accuracy_test(Gstd, Nr, rc, ri)
    print(f"  {'cheb':>7} | {a_std:11.3e} {b_std:11.3e} {c_std:11.3e} | "
          f"{e1_std:12.3e} {e2_std:12.3e}")
    results = []
    for alpha in (0.9, 0.95, 0.99, 0.999):
        G = make_grid(Nr, Nth, Nps, rc, cell, alpha=alpha)
        uK = P1.seed_round_native(G, p=1.0, m=1)
        smax, smin, cond = jac_cond(G, uK, f"alpha={alpha}")
        ea, eb = accuracy_test(G, Nr, rc, ri)
        print(f"  {alpha:7.3f} | {smax:11.3e} {smin:11.3e} {cond:11.3e} | "
              f"{ea:12.3e} {eb:12.3e}")
        results.append((alpha, smax, smin, cond, ea, eb))

    # ---- 4. VERDICT ----
    print("\n[4] SUMMARY")
    print(f"  baseline (cheb): smax={a_std:.3e} smin={b_std:.3e} cond={c_std:.3e} "
          f"| err exp(-r)={e1_std:.3e} err 1/r={e2_std:.3e}")
    for (alpha, smax, smin, cond, ea, eb) in results:
        tag = "WORKABLE(cond<1e6 & smooth-err<1e-6)" if (cond < 1e6 and ea < 1e-6) else ""
        print(f"  alpha={alpha}: smax={smax:.3e} cond={cond:.3e} "
              f"err_smooth={ea:.3e} {tag}")
    print("=" * 78)


if __name__ == "__main__":
    main()
