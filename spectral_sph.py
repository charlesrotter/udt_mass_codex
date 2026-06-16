#!/usr/bin/env python3
"""
spectral_sph.py -- FULL-SPHERE angular spectral primitives (theta x psi) for the
full-3-D coupled Einstein+L2+L4 catalog solver.  NO axisymmetry imposed: psi is a
LIVE coordinate.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers).

BASIS / AXIS REGULARITY (category-A: required physics + the standard spectral cure
for the coordinate pole, NOT a simplification):
  theta : Gauss-Legendre nodes of mu=cos(theta) in (-1,1) (poles EXCLUDED -- the
          interior nodes never land on the singular axis).  d/dtheta by the
          Legendre/Lagrange spectral matrix (reused from spectral_2d), chain-ruled
          d/dtheta = -sin(theta) d/dmu.  Exact-on-polynomials in mu, EXPONENTIALLY
          convergent for smooth fields.
  psi   : UNIFORM nodes on [0,2pi), GENUINELY periodic.  d/dpsi by the FOURIER
          spectral differentiation matrix (exact for band-limited fields, spectrally
          accurate, NO edge -- the cleanest possible representation of the live
          azimuth).  This is the criterion-4 (psi) blind-spot opener.

CATEGORY-A PROOF (delivered in the results doc on the OWN machinery):
  (i)  recovers the round #56 soliton embedded in the 3-D basis at machine zero
       (psi-independent fields differentiate to exactly 0 in psi);
  (ii) basis-invariant under (Nth, Nps) refinement;
  (iii) exponential convergence for smooth fields; Fourier d/dpsi machine-exact on
       trig modes; angular quadrature int over the full sphere exact on harmonics.
No physics tie, no source, no linearization, no dropped term -- a discretization.
"""
import numpy as np
from scipy.special import roots_legendre
from numpy.polynomial.legendre import legvander, legder


# ---------------------------------------------------------------------------
# theta operators (reused construction from spectral_2d, self-contained here)
# ---------------------------------------------------------------------------
def legendre_diff_mu(Nmu):
    mu, w = roots_legendre(Nmu)
    V = legvander(mu, Nmu - 1)
    Vp = np.zeros_like(V)
    for k in range(Nmu):
        ck = np.zeros(Nmu); ck[k] = 1.0
        dk = legder(ck)
        Vp[:, k] = np.polynomial.legendre.legval(mu, dk)
    Dmu = Vp @ np.linalg.inv(V)
    return mu, w, Dmu


def theta_operators(Nth):
    """theta grid (ascending in (0,pi)), GL weight wmu (=int ... sin th dtheta),
    d/dtheta spectral matrix, sin(theta)."""
    mu, w, Dmu = legendre_diff_mu(Nth)
    th = np.arccos(mu)
    idx = np.argsort(th)
    th = th[idx]; wmu = w[idx]; Dmu = Dmu[np.ix_(idx, idx)]
    sth = np.sin(th)
    Dth = (-sth)[:, None] * Dmu
    return th, wmu, Dth, sth


# ---------------------------------------------------------------------------
# psi operators: uniform periodic nodes + Fourier spectral differentiation matrix
# ---------------------------------------------------------------------------
def psi_operators(Nps):
    """Uniform nodes psi_j = 2 pi j / Nps on [0,2pi), the Fourier spectral d/dpsi
    matrix (Trefethen, even-N formula), and the uniform quadrature weight
    (2 pi / Nps) -- spectrally accurate for periodic integrands.

    Even-N Fourier diff matrix (Trefethen Spectral Methods in MATLAB, p.24):
      D[j,k] = 0.5 (-1)^(j-k) cot((j-k) h / 2),  j!=k ;  D[j,j]=0,  h=2pi/Nps.
    For ODD N use csc instead of cot.  We build whichever N is given."""
    if Nps == 1:
        return np.array([0.0]), np.array([[0.0]]), np.array([2*np.pi])
    h = 2*np.pi/Nps
    psi = h*np.arange(Nps)
    D = np.zeros((Nps, Nps))
    for j in range(Nps):
        for k in range(Nps):
            if j == k:
                D[j, k] = 0.0
            else:
                m = j - k
                if Nps % 2 == 0:
                    D[j, k] = 0.5*((-1)**m)/np.tan(m*h/2)
                else:
                    D[j, k] = 0.5*((-1)**m)/np.sin(m*h/2)
    w = np.full(Nps, h)
    return psi, D, w


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== psi (Fourier) spectral operator self-test ===")
    print("d/dpsi of band-limited fields is MACHINE-EXACT:")
    for Nps in [4, 8, 16]:
        psi, Dps, wps = psi_operators(Nps)
        # f = cos(2 psi) + sin(3 psi) [needs Nps>=8 to resolve mode 3 exactly]
        if Nps >= 8:
            f = np.cos(2*psi) + np.sin(3*psi)
            df_ex = -2*np.sin(2*psi) + 3*np.cos(3*psi)
        else:
            f = np.cos(psi)
            df_ex = -np.sin(psi)
        err = np.max(np.abs(Dps @ f - df_ex))
        print(f"  Nps={Nps:3d}  max|Dps f - f'| = {err:.3e}")

    print("\npsi quadrature self-test  int_0^2pi (1+cos^2 psi) dpsi = 3 pi:")
    for Nps in [4, 8, 16]:
        psi, Dps, wps = psi_operators(Nps)
        approx = wps @ (1 + np.cos(psi)**2)
        print(f"  Nps={Nps:3d}  {approx:.10f}  err={abs(approx-3*np.pi):.2e}")

    print("\n=== theta operator self-test (re-check, axis-regular GL) ===")
    for Nth in [4, 6, 8]:
        th, wmu, Dth, sth = theta_operators(Nth)
        mu = np.cos(th)
        f = 0.5*(5*mu**3 - 3*mu)        # P_3
        df_ex = -sth*0.5*(15*mu**2 - 3)
        err = np.max(np.abs(Dth @ f - df_ex))
        print(f"  Nth={Nth:3d}  max|Dth P3 - exact| = {err:.3e}")

    print("\nfull-sphere quadrature  int Y_00^2 dOmega = 1 (with 1/4pi norm)"
          "  -> int dOmega = 4 pi:")
    for (Nth, Nps) in [(6, 8), (8, 12), (12, 16)]:
        th, wmu, Dth, sth = theta_operators(Nth)
        psi, Dps, wps = psi_operators(Nps)
        # int dOmega = int sin th dth int dpsi = (sum wmu)(sum wps)
        area = wmu.sum()*wps.sum()
        print(f"  Nth={Nth} Nps={Nps}: area={area:.10f}  err={abs(area-4*np.pi):.2e}")
