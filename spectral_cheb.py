#!/usr/bin/env python3
"""
spectral_cheb.py -- Chebyshev pseudospectral primitives for the UDT spectral
coupled Einstein+L2+L4 soliton solver.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers).

CATEGORY-A AUDIT (this module): spectral discretization is a NUMERICAL
DISCRETIZATION of the SAME native equations -- it replaces the finite-difference
derivative operator with the exact-on-polynomials Chebyshev differentiation
matrix.  It introduces NO physics: no tie, no source injection, no linearization,
no dropped term.  Its legitimacy proof (delivered in the results doc) is the
THREE-PART gate: (i) it must recover the corrected #56 round soliton; (ii) the
result must be basis/gauge invariant (matches the FD #56 to its accuracy);
(iii) it must converge under basis (N) refinement -- and EXPONENTIALLY for the
smooth fields, the spectral signature absent in FD.

Chebyshev-Gauss-Lobatto (CGL) nodes x_j = cos(pi j / N), j=0..N on [-1,1],
mapped affinely to a physical radial interval [rc, ri].  The CGL differentiation
matrix is the standard Trefethen cheb() construction (exact derivative of the
interpolating polynomial; spectral accuracy for smooth f).
"""
import numpy as np


def cheb(N):
    """Chebyshev-Gauss-Lobatto nodes x (N+1) on [-1,1] and the (N+1)x(N+1)
    differentiation matrix D (Trefethen, Spectral Methods in MATLAB, cheb.m).
    x[0]=+1 ... x[N]=-1.  D acts as (D @ f) = f'(x)."""
    if N == 0:
        return np.array([1.0]), np.array([[0.0]])
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.ones(N + 1)
    c[0] = 2.0
    c[N] = 2.0
    c *= (-1.0) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1.0 / c) / (dX + np.eye(N + 1))
    D = D - np.diag(D.sum(axis=1))
    return x, D


def cheb_interval(N, lo, hi):
    """CGL nodes mapped to [lo,hi] and the differentiation matrix d/dr on that
    interval (chain rule: r = lo + (hi-lo)*(1-x)/2 ascending; we keep the
    standard descending x but return r ASCENDING with the matched D).

    We build r ascending in physical space so r[0]=lo (core), r[-1]=hi (seal).
    x descends from +1 to -1; r = (hi+lo)/2 + (hi-lo)/2 * x descends too, so we
    FLIP both the node order and the matrix to get an ascending grid."""
    x, D = cheb(N)
    r = 0.5 * (hi + lo) + 0.5 * (hi - lo) * x         # descending (r[0]=hi)
    # chain rule: d/dr = (2/(hi-lo)) d/dx
    Dr = (2.0 / (hi - lo)) * D
    # flip to ascending r (r[0]=lo core, r[-1]=hi seal)
    idx = np.arange(N, -1, -1)
    r = r[idx]
    Dr = Dr[np.ix_(idx, idx)]
    return r, Dr


def clenshaw_curtis_weights(N, lo, hi):
    """Clenshaw-Curtis quadrature weights on the CGL nodes (ASCENDING order to
    match cheb_interval), scaled to [lo,hi].  Integral f dr ~ w . f.
    PROPER for spectral integration of smooth integrands (used for the
    proper-volume residual norm and M_MS by quadrature where needed)."""
    # standard CC weights on [-1,1] for CGL nodes (descending), then flip+scale
    if N == 0:
        return np.array([hi - lo])
    theta = np.pi * np.arange(N + 1) / N
    w = np.zeros(N + 1)
    v = np.ones(N - 1)
    for k in range(1, (N // 2) + 1):
        if 2 * k == N:
            coef = 1.0 / (4.0 * k * k - 1.0)
        else:
            coef = 2.0 / (4.0 * k * k - 1.0)
        v -= coef * np.cos(2.0 * k * theta[1:N])
    w[1:N] = (2.0 / N) * v
    w[0] = 1.0 / (N * N) if N % 2 == 0 else 1.0 / (N * N - 1.0) * 1.0
    # Trefethen clencurt for endpoints:
    w[0] = 1.0 / (N * N - 1 + (N % 2))
    w[N] = w[0]
    # scale to interval; descending x -> flip to ascending r
    w = w * (hi - lo) / 2.0
    return w[::-1].copy()


if __name__ == "__main__":
    # self-test: spectral derivative of a smooth function converges EXPONENTIALLY
    print("Chebyshev primitive self-test (spectral signature on smooth f):")
    print(" N    max|D f - f'|   (f = exp(sin(3r)) on [0.05,14.05])")
    lo, hi = 0.05, 14.05
    for N in [8, 16, 24, 32, 48, 64]:
        r, Dr = cheb_interval(N, lo, hi)
        f = np.exp(np.sin(3 * r))
        fp_exact = 3 * np.cos(3 * r) * f
        err = np.max(np.abs(Dr @ f - fp_exact))
        print(f" {N:3d}   {err:.3e}")
    # quadrature self-test
    print("\nClenshaw-Curtis quadrature self-test (int_0.05^14.05 exp(-r) dr):")
    exact = np.exp(-lo) - np.exp(-hi)
    for N in [16, 32, 48, 64]:
        r, _ = cheb_interval(N, lo, hi)
        w = clenshaw_curtis_weights(N, lo, hi)
        approx = w @ np.exp(-r)
        print(f" N={N:3d}  err={abs(approx-exact):.3e}")
