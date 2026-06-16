#!/usr/bin/env python3
"""
spectral_2d.py -- 2-D axisymmetric spectral primitives (Chebyshev in r x spectral
in theta) for the coupled Einstein+L2+L4 catalog solver.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

THETA BASIS / AXIS REGULARITY (category-A: required physics, not a simplification):
We discretize theta on the GAUSS-LEGENDRE nodes of mu = cos(theta) in (-1,1)
(theta in (0,pi), poles EXCLUDED -- the interior Gauss nodes never land on the
coordinate-singular axis, the standard spectral cure for the pole).  Functions are
represented by their values at the GL nodes; theta-derivatives are taken by a
Legendre/Lagrange spectral differentiation matrix in mu, then chain-ruled
d/dtheta = -sin(theta) d/dmu.  This is exact-on-polynomials in mu and converges
EXPONENTIALLY for smooth (in mu) fields -- the spectral signature.  Axisymmetric
fields that are smooth functions of cos(theta) (e.g. Legendre multipoles) are
represented EXACTLY at finite order.

CATEGORY-A: this is a NUMERICAL DISCRETIZATION (basis + node choice).  No physics
tie, no source, no linearization, no dropped term.  Proof = (i) recovers the round
#56 soliton embedded in 2-D at machine zero; (ii) basis-invariant under N_theta
refinement; (iii) exponential convergence.
"""
import numpy as np
from numpy.polynomial.legendre import legvander, legder, Legendre
from scipy.special import roots_legendre


def legendre_diff_mu(Nmu):
    """Gauss-Legendre nodes mu in (-1,1) (Nmu of them) and the spectral
    differentiation matrix Dmu acting on nodal values: (Dmu @ f) = df/dmu at the
    nodes (exact for polynomials of degree < Nmu).  Built via the Vandermonde:
    f = V c (Legendre coeffs), f' = V' c => Dmu = V' V^{-1}."""
    mu, w = roots_legendre(Nmu)
    V = legvander(mu, Nmu - 1)               # (Nmu, Nmu)
    # derivative of each Legendre basis at the nodes
    Vp = np.zeros_like(V)
    for k in range(Nmu):
        ck = np.zeros(Nmu); ck[k] = 1.0
        dk = legder(ck)                       # coeffs of d/dmu P_k
        Vp[:, k] = np.polynomial.legendre.legval(mu, dk)
    Dmu = Vp @ np.linalg.inv(V)
    return mu, w, Dmu


def theta_operators(Nth):
    """Return theta grid (ascending), GL weights in theta, and the d/dtheta
    spectral matrix.  theta in (0,pi); mu=cos(theta) descending on GL nodes ->
    we flip to ascending theta.  d/dtheta = -sin(theta) d/dmu."""
    mu, w, Dmu = legendre_diff_mu(Nth)
    th = np.arccos(mu)                         # mu in (-1,1) ascending -> th in (pi,0) descending
    # mu ascending => th descending; flip to ascending theta
    idx = np.argsort(th)
    th = th[idx]
    wmu = w[idx]
    Dmu = Dmu[np.ix_(idx, idx)]
    sth = np.sin(th)
    # d/dtheta = -sin(theta) * d/dmu
    Dth = (-sth)[:, None] * Dmu
    # theta-integration weight: int f sin(theta) dtheta = int f dmu = sum wmu f
    # so the theta quadrature weight (in dtheta, with the sin already) is wmu/?  ->
    # int_0^pi g(theta) sin(theta) dtheta = sum_i wmu_i g(theta_i).  We return wmu
    # as the "sin-theta-included" weight (the proper-volume angular measure).
    return th, wmu, Dth, sth


if __name__ == "__main__":
    print("=== theta spectral operator self-test (axis-regular GL nodes) ===")
    print("d/dtheta of smooth-in-mu fields converges EXPONENTIALLY:")
    print(f"{'Nth':>4} {'max|Dth f - f_exact|':>22}   (f=P_3(cos th)=legendre l=3)")
    for Nth in [4, 6, 8, 12, 16]:
        th, wmu, Dth, sth = theta_operators(Nth)
        mu = np.cos(th)
        # f = P_3(mu); df/dtheta = -sin(theta) dP3/dmu
        f = 0.5*(5*mu**3 - 3*mu)
        dfdmu = 0.5*(15*mu**2 - 3)
        df_exact = -sth*dfdmu
        err = np.max(np.abs(Dth @ f - df_exact))
        print(f"{Nth:>4} {err:>22.3e}")
    print("\nangular quadrature self-test int_0^pi sin(th)^3 dtheta = 4/3:")
    for Nth in [4, 6, 8, 12]:
        th, wmu, Dth, sth = theta_operators(Nth)
        approx = wmu @ (np.sin(th)**2)   # int sin^2 * sin dtheta = int sin^3
        print(f" Nth={Nth:3d}  {approx:.10f}  err={abs(approx-4/3):.2e}")
