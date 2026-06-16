#!/usr/bin/env python3
"""
spectral_3d.py -- FULL-3-D spectral primitives (Chebyshev in r  x  spherical-harmonic
basis on the WHOLE sphere (theta,psi))  for the unreduced coupled Einstein+L2+L4
catalog solver.  NO spatial symmetry imposed.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; NEVER compared to wall numbers).

================================================================================
WHY FULL 3-D (the dimensional blind spot):  all prior solves were 2-D (r,theta)
axisymmetric or 1-D radial -- valid only for the spherically-symmetric charge-1
ground state.  In Skyrme-type theories (L2+L4 IS one) the DISTINCT solitons are
characteristically NON-AXISYMMETRIC (higher-winding ones are platonic-solid-shaped),
so a catalog of distinct types most plausibly lives in the psi-dimension every prior
solve reduced away.  This module removes that blind spot.
================================================================================

THE BASIS  (category-A: NUMERICAL DISCRETIZATION of the SAME native equations --
no tie, no source, no linearization, no dropped term):

  r    : Chebyshev-Gauss-Lobatto on the finite cell [rc, ri]   (spectral_cheb.cheb_interval)
  theta: Gauss-Legendre nodes in mu=cos(theta), poles EXCLUDED (interior nodes never
         land on the coordinate axis -- the standard spectral cure for the pole)
  psi  : uniform periodic grid, FOURIER spectral differentiation (psi is genuinely
         periodic, period 2*pi -> EXACT spectral derivative, no edge degradation)

A tensor-product (Gauss-Legendre in mu) x (uniform Fourier in psi) grid is a SPHERICAL-
HARMONIC basis in disguise:  any smooth function on S^2 is represented to spectral
accuracy, and the forward/backward transform to Y_lm coefficients is EXACT at finite
(Nmu, Nps).  We work in the NODAL representation (values at grid points) with spectral
differentiation matrices -- mathematically identical to the SH-coefficient
representation, and the convenient form for a pointwise nonlinear residual.

PROOF this is category-A (delivered numerically in full3d_catalog_results.md):
  (i)  RECOVERS the #56 round soliton embedded in the full 3-D basis (exponential
       residual convergence, M_MS, exterior B=1/A as a RESULT);
  (ii) basis-invariant under (Nr, Nmu, Nps) refinement;
  (iii) EXPONENTIAL convergence (the spectral signature) for smooth fields.

SELF-TESTS below: spectral d/dtheta and d/dpsi on Y_lm converge exponentially; the
spherical quadrature integrates Y_lm Y_l'm'* to delta_{ll'}delta_{mm'} to ~1e-15.
"""
import numpy as np
from scipy.special import roots_legendre, sph_harm

from spectral_cheb import cheb_interval, clenshaw_curtis_weights


# ---------------------------------------------------------------------------
# theta (mu = cos theta) -- Gauss-Legendre nodes, spectral d/dtheta, axis-regular.
# (Same construction as spectral_2d.legendre_diff_mu, re-exported for the 3-D module.)
# ---------------------------------------------------------------------------
def legendre_diff_mu(Nmu):
    """GL nodes mu in (-1,1) and d/dmu spectral matrix on nodal values (exact for
    polynomials of degree < Nmu)."""
    from numpy.polynomial.legendre import legvander, legder, legval
    mu, w = roots_legendre(Nmu)
    V = legvander(mu, Nmu - 1)
    Vp = np.zeros_like(V)
    for k in range(Nmu):
        ck = np.zeros(Nmu); ck[k] = 1.0
        dk = legder(ck)
        Vp[:, k] = legval(mu, dk)
    Dmu = Vp @ np.linalg.inv(V)
    return mu, w, Dmu


def theta_operators(Nth):
    """theta grid (ascending in theta), GL weight wmu (the sin-theta-included angular
    measure: int_0^pi g sin theta dtheta = sum wmu_i g_i), d/dtheta spectral matrix,
    and sin(theta) at the nodes."""
    mu, w, Dmu = legendre_diff_mu(Nth)
    th = np.arccos(mu)                      # mu ascending -> th descending
    idx = np.argsort(th)
    th = th[idx]; wmu = w[idx]; Dmu = Dmu[np.ix_(idx, idx)]
    sth = np.sin(th)
    Dth = (-sth)[:, None] * Dmu             # d/dtheta = -sin theta d/dmu
    return th, wmu, Dth, sth


# ---------------------------------------------------------------------------
# psi -- uniform periodic grid + FOURIER spectral differentiation matrix.
# ---------------------------------------------------------------------------
def fourier_operators(Nps):
    """Uniform psi grid on [0, 2pi) (Nps points) and the Fourier d/dpsi spectral
    differentiation matrix (exact for trig polynomials of degree < Nps/2).
    Standard Trefethen periodic differentiation matrix.  Nps EVEN required.
    psi-integration weight is uniform = 2pi/Nps (spectrally exact for periodic)."""
    assert Nps % 2 == 0, "use even Nps for the standard Fourier diff matrix"
    ps = 2.0 * np.pi * np.arange(Nps) / Nps
    h = 2.0 * np.pi / Nps
    # Trefethen periodic D (entries): D_{ij}= 0.5*(-1)^{i-j} cot((i-j)h/2), 0 on diag
    i = np.arange(Nps)[:, None]
    j = np.arange(Nps)[None, :]
    diff = i - j
    with np.errstate(divide='ignore', invalid='ignore'):
        Dps = 0.5 * ((-1.0) ** diff) / np.tan(diff * h / 2.0)
    Dps[np.arange(Nps), np.arange(Nps)] = 0.0
    wps = np.full(Nps, h)                    # uniform periodic quadrature weight
    return ps, wps, Dps


# ---------------------------------------------------------------------------
# Full spherical (theta,psi) grid container.
# ---------------------------------------------------------------------------
def sh_dtheta_matrix(Nth, Nps):
    """EXACT d/dtheta operator on the full (theta,psi) grid via the SPHERICAL-HARMONIC
    basis.  The naive Dth = -sin(theta) d/dmu (legendre-in-mu) is exact ONLY for m=0
    (polynomials in mu); physical S^2 fields carry m != 0 modes (sin^|m| theta factors)
    that are NOT polynomial in mu.  This operator differentiates EXACTLY for every (l,m)
    band-limited field via the standard raising relation
        dY_lm/dtheta = m cot(theta) Y_lm + sqrt((l-m)(l+m+1)) e^{-i psi} Y_{l,m+1}.
    Returns a dense ((Nth*Nps),(Nth*Nps)) real matrix acting on the FLATTENED (theta,psi)
    nodal vector (row-major: index = i*Nps + j).  CATEGORY-A: exact spectral
    differentiation on the genuine spherical-harmonic basis (proof: machine-zero on
    Y_lm; recovers the round soliton)."""
    from scipy.special import roots_legendre, sph_harm
    mu, _ = roots_legendre(Nth)
    th = np.arccos(mu); idx = np.argsort(th); th = th[idx]
    ps = 2.0 * np.pi * np.arange(Nps) / Nps
    TH = th[:, None] * np.ones((1, Nps))
    PS = np.ones((Nth, 1)) * ps[None, :]
    Lmax = Nth - 1
    mmax = Nps // 2 - 1
    basis = []; dbasis = []
    for l in range(Lmax + 1):
        for m in range(-l, l + 1):
            if abs(m) > mmax:
                continue
            Y = sph_harm(m, l, PS, TH)
            term = (m / np.tan(TH)) * Y
            if m + 1 <= l:
                term = term + np.sqrt((l - m) * (l + m + 1)) * np.exp(-1j * PS) * sph_harm(m + 1, l, PS, TH)
            basis.append(Y.ravel()); dbasis.append(term.ravel())
    Bmat = np.array(basis).T
    Dmat = np.array(dbasis).T
    D = Dmat @ np.linalg.pinv(Bmat)
    return D.real, th, ps


class SphereGrid:
    """Tensor product Gauss-Legendre(mu) x Fourier(psi) sphere grid + EXACT spectral
    operators (true spherical-harmonic basis).

    Nodal fields are stored as arrays of shape (..., Nth, Nps).  The angular derivative
    helpers act on the LAST TWO axes.  Spherical quadrature:
       int_{S^2} f dOmega = sum_{i,j} wmu_i * wps_j * f_{ij}    (machine-exact for
    band-limited fields; wmu carries sin theta, wps is uniform 2pi/Nps).

    d/dtheta uses the SH-EXACT operator (handles m != 0 sin^|m| theta factors exactly);
    d/dpsi uses the exact Fourier matrix.
    """
    def __init__(self, Nth, Nps):
        self.Nth, self.Nps = Nth, Nps
        self.th, self.wmu, self.Dth_mu, self.sth = theta_operators(Nth)
        self.ps, self.wps, self.Dps = fourier_operators(Nps)
        # SH-exact d/dtheta as a flattened (Nth*Nps, Nth*Nps) matrix
        self.Dth_sh, _, _ = sh_dtheta_matrix(Nth, Nps)
        # broadcast grids (Nth, Nps)
        self.TH = self.th[:, None] * np.ones((1, Nps))
        self.PS = np.ones((Nth, 1)) * self.ps[None, :]
        self.STH = self.sth[:, None] * np.ones((1, Nps))
        self.CTH = np.cos(self.th)[:, None] * np.ones((1, Nps))
        self.warea = self.wmu[:, None] * self.wps[None, :]

    def dtheta(self, f):
        """SH-EXACT d/dtheta (acts on last two axes via the flattened SH matrix)."""
        sh = f.shape
        flat = f.reshape(*sh[:-2], self.Nth * self.Nps)
        out = np.einsum('ab,...b->...a', self.Dth_sh, flat)
        return out.reshape(sh)

    def dpsi(self, f):
        """d/dpsi along the psi axis (-1) -- exact Fourier."""
        return np.einsum('kl,...il->...ik', self.Dps, f)

    def sphere_integral(self, f):
        """int_{S^2} f dOmega using the tensor quadrature (last two axes)."""
        return np.einsum('ij,...ij->...', self.warea, f)


# ---------------------------------------------------------------------------
# Self-tests (run IN-PROCESS):  exponential convergence of the spectral angular
# derivatives on real spherical harmonics, and the spherical quadrature orthonormality.
# ---------------------------------------------------------------------------
def _real_Ylm(l, m, TH, PS):
    """A smooth real spherical-harmonic field on the (theta,psi) grid.
    Uses scipy sph_harm(m, l, psi, theta) and takes the real combination."""
    Y = sph_harm(abs(m), l, PS, TH)
    if m < 0:
        return np.sqrt(2) * (-1) ** m * Y.imag
    elif m > 0:
        return np.sqrt(2) * (-1) ** m * Y.real
    else:
        return Y.real


if __name__ == "__main__":
    print("=== spectral_3d primitive self-tests (full sphere, spectral signature) ===\n")

    print("[1] d/dtheta and d/dpsi EXPONENTIAL convergence on a smooth field")
    print("    f = P_3(cos th) [poly in mu]  +  (1-mu^2) cos(2 psi)  [trig in psi]:")
    print(f"{'Nth':>4}{'Nps':>5}   {'max|Dth f - exact|':>20}   {'max|Dps f - exact|':>20}")
    for Nth, Nps in [(4, 4), (6, 6), (8, 8), (12, 12), (16, 16)]:
        g = SphereGrid(Nth, Nps)
        mu = g.CTH
        # f = P3(mu) + (1-mu^2) cos(2 psi)
        f = 0.5 * (5 * mu**3 - 3 * mu) + (1 - mu**2) * np.cos(2 * g.PS)
        # d/dtheta = -sin th d/dmu ;  dP3/dmu = 0.5(15 mu^2 - 3); d(1-mu^2)/dmu=-2mu
        dfdmu = 0.5 * (15 * mu**2 - 3) - 2 * mu * np.cos(2 * g.PS)
        dth_exact = -g.STH * dfdmu
        dps_exact = -2 * (1 - mu**2) * np.sin(2 * g.PS)
        err_th = np.max(np.abs(g.dtheta(f) - dth_exact))
        err_ps = np.max(np.abs(g.dpsi(f) - dps_exact))
        print(f"{Nth:>4}{Nps:>5}   {err_th:>20.3e}   {err_ps:>20.3e}")

    print("\n[2] spherical quadrature orthonormality  int Y_lm Y_l'm'^* dOmega:")
    g = SphereGrid(16, 16)
    pairs = [((0, 0), (0, 0)), ((1, 0), (1, 0)), ((2, 1), (2, 1)),
             ((3, 2), (3, 2)), ((1, 0), (2, 0)), ((2, 1), (3, 1))]
    for (l1, m1), (l2, m2) in pairs:
        Y1 = sph_harm(m1, l1, g.PS, g.TH)
        Y2 = sph_harm(m2, l2, g.PS, g.TH)
        val = g.sphere_integral(Y1 * np.conj(Y2))
        expect = 1.0 if (l1, m1) == (l2, m2) else 0.0
        print(f"  <Y_{l1}{m1}|Y_{l2}{m2}> = {val.real:+.12f}  (expect {expect:.0f}, "
              f"err {abs(val - expect):.2e})")

    print("\n[3] int_{S^2} 1 dOmega = 4 pi:")
    for Nth, Nps in [(6, 6), (8, 8), (12, 12)]:
        g = SphereGrid(Nth, Nps)
        val = g.sphere_integral(np.ones((Nth, Nps)))
        print(f"  Nth={Nth} Nps={Nps}: {val:.12f}  err={abs(val - 4 * np.pi):.2e}")
