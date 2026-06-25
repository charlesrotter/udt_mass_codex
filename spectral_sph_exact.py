#!/usr/bin/env python3
"""
spectral_sph_exact.py -- SPHERICAL-HARMONIC-EXACT d/dtheta on the existing Gauss-Legendre-mu
angular grid.  The grid fix that unblocks the PURE (least-imposed) free S^2 matter (Charles
2026-06-25: "fix the grid, then pure 3-comp").

THE FLAW IT FIXES (spectral_sph.theta_operators):
  d/dtheta = -sin(theta) D_mu, with D_mu the Legendre/Lagrange spectral matrix -- EXACT only for
  POLYNOMIALS IN mu=cos(theta).  It applies the SAME D_mu to every azimuthal mode.  But sin(theta)
  is genuinely an |m|=1 object (the theta-part of a unit-winding harmonic, ~P_1^1), NOT a
  mu-polynomial -> the grid mis-differentiates any winding (sin^|m| theta) matter: error ~0.18,
  NON-convergent (stays ~0.18 from Nth=6..20).  The native S^2 winding n=x/r = (sth cmps, sth smps,
  cth) is exactly this case, so the pure 3-component matter could not be differentiated correctly.

THE FIX (mathematically correct spectral differentiation on the sphere; matter-LOCAL, no global
grid change -- the GL-mu nodes ARE the exact spherical-harmonic quadrature grid):
  differentiate PER AZIMUTHAL MODE m using the ASSOCIATED-LEGENDRE basis {P_l^|m|(mu)} of the
  right order.  For each |m|, build the exact d/dtheta matrix from the ANALYTIC basis derivatives
  dP_l^m/dtheta = -sin(theta) dP_l^m/dmu (analytic, NOT a spectral approx of a non-polynomial):
      Dtheta_m = dStheta @ inv(S),   S[i,j]=P_{m+j}^m(mu_i),  dStheta[i,j]=dP_{m+j}^m/dtheta(mu_i).
  This is EXACT (machine precision) for any band-limited field on the sphere, with FULL freedom --
  it imposes NO polar structure (unlike the analytic-dn carriers in free_s2_matter that fixed the
  polar shape to dodge the grid).

USE: precompute the per-|m| matrices once; apply to a field via psi-FFT -> per-mode Dtheta -> ipsi.
d/dpsi stays the existing Fourier-exact operator (spectral_sph.psi_operators).  Validated in
__main__ (the winding components + a free field, with convergence) -- BUILD/VALIDATE only, no solve.
"""
import functools
import numpy as np
from scipy.special import roots_legendre, assoc_legendre_p_all


def _gl_mu_nodes(Nth):
    """The grid's theta nodes (ascending in (0,pi)) and mu=cos(theta), matching
    spectral_sph.theta_operators' ordering."""
    mu, w = roots_legendre(Nth)
    th = np.arccos(mu)
    idx = np.argsort(th)
    return mu[idx], th[idx], w[idx]


def dtheta_exact_matrix(mu, m):
    """Exact d/dtheta (Nth x Nth) on the GL-mu nodes for azimuthal order m>=0, built from the
    associated-Legendre basis {P_l^m : l=m..m+Nth-1} and its ANALYTIC theta-derivative."""
    N = len(mu)
    th = np.arccos(mu)
    sth = np.sin(th)
    nmax = m + N - 1
    S = np.zeros((N, N))
    dSth = np.zeros((N, N))
    for i, z in enumerate(mu):
        # P[l, order_index], dPdmu[l, order_index]; order axis runs -m..m (length 2m+1)
        P, dPdz = assoc_legendre_p_all(nmax, m, float(z), diff_n=1)
        oi = m  # order axis is FFT-ordered [0,+1,..,+m,-m,..,-1] -> order +m is at index m
        for j in range(N):
            l = m + j
            S[i, j] = P[l, oi]
            dSth[i, j] = -sth[i] * dPdz[l, oi]      # dP/dtheta = -sin th dP/dmu (analytic)
    return dSth @ np.linalg.inv(S)


def build_dtheta_exact(Nth, Mmax):
    """Return {|m|: Dtheta_m (Nth x Nth)} for |m| = 0..Mmax."""
    mu, th, w = _gl_mu_nodes(Nth)
    return {m: dtheta_exact_matrix(mu, m) for m in range(Mmax + 1)}


def dtheta_exact_operator(Nth, Nps):
    """Precompute the SH-exact d/dtheta as a SINGLE real (Nth,Nps,Nth,Nps) tensor M:
        (d_theta f)[I,J] = sum_{i,j} M[I,J,i,j] f[i,j].
    Linear (psi-FFT -> per-mode Dtheta -> ipsi), so the composite is a constant real tensor --
    apply it in torch by contraction (jacrev-/vmap-SAFE, no fft inside the traced residual)."""
    Dmats = build_dtheta_exact(Nth, Nps // 2)
    j = np.arange(Nps); k = np.arange(Nps)
    F = np.exp(-2j * np.pi * np.outer(k, j) / Nps)         # Fhat[k] = sum_j F[k,j] f[j]
    Finv = np.exp(2j * np.pi * np.outer(j, k) / Nps) / Nps  # f[j]    = sum_k Finv[j,k] Fhat[k]
    freqs = np.fft.fftfreq(Nps, d=1.0 / Nps)
    M = np.zeros((Nth, Nps, Nth, Nps), dtype=complex)
    for kk in range(Nps):
        mk = int(abs(round(freqs[kk])))
        M += np.einsum('J,Ii,j->IJij', Finv[:, kk], Dmats[mk], F[kk, :])
    return np.real(M)                                       # real for real fields


@functools.lru_cache(maxsize=None)
def _operator_torch(Nth, Nps, device, dtype_str):
    import torch
    M = dtheta_exact_operator(Nth, Nps)
    return torch.as_tensor(M, device=device, dtype=getattr(torch, dtype_str))


def dtheta_exact_torch(f):
    """SH-exact d/dtheta of a torch field f (..., Nth, Nps).  Applies the cached constant
    operator tensor by contraction -- jacrev/vmap-SAFE (no fft/scipy inside the traced call)."""
    import torch
    M = _operator_torch(f.shape[-2], f.shape[-1], str(f.device), str(f.dtype).split('.')[-1])
    return torch.einsum('IJij,...ij->...IJ', M, f)


def dtheta_exact(f, Dmats):
    """Exact d/dtheta of a real field f (..., Nth, Nps) on the (GL-mu x uniform-psi) grid.
    psi-FFT -> apply the |m|-order Dtheta to each azimuthal mode -> inverse FFT.  Dmats from
    build_dtheta_exact with Mmax >= Nps//2."""
    Nth, Nps = f.shape[-2], f.shape[-1]
    F = np.fft.fft(f, axis=-1)                       # azimuthal modes
    out = np.zeros_like(F)
    freqs = np.fft.fftfreq(Nps, d=1.0 / Nps)         # integer mode numbers (..., -1, 0, 1, ...)
    for k in range(Nps):
        m = int(abs(round(freqs[k])))
        D = Dmats[m]
        out[..., :, k] = np.einsum('ij,...j->...i', D, F[..., :, k])
    return np.real(np.fft.ifft(out, axis=-1))


if __name__ == "__main__":
    from spectral_sph import theta_operators

    def current_dtheta(f, Nth):
        th, wmu, Dth, sth = theta_operators(Nth)
        return np.einsum('ij,...j->...i', Dth, f)

    print("=== SH-EXACT d/dtheta validation (BUILD/VALIDATE only, no solve) ===\n")
    print("(1) the native winding n=x/r = (sth cos m.psi, sth sin m.psi, cth), m=1 -- d/dtheta exact?")
    print(f"{'Nth':>4} {'comp':>6} {'current grid err':>18} {'SH-exact err':>16}")
    for Nth in (8, 12, 16):
        Nps = 8
        mu, th, w = _gl_mu_nodes(Nth)
        Dmats = build_dtheta_exact(Nth, Nps // 2)
        psi = 2 * np.pi * np.arange(Nps) / Nps
        TH, PS = np.meshgrid(th, psi, indexing='ij')
        sth = np.sin(TH); cth = np.cos(TH)
        comps = {'n1=sth.cps': (sth * np.cos(PS), cth * np.cos(PS)),
                 'n2=sth.sps': (sth * np.sin(PS), cth * np.sin(PS)),
                 'n3=cth':     (cth,              -sth)}
        for name, (f, df_ex) in comps.items():
            cur = np.max(np.abs(current_dtheta(f.T, Nth).T - df_ex))   # current uses Nth-only op per psi col
            she = np.max(np.abs(dtheta_exact(f, Dmats) - df_ex))
            print(f"{Nth:>4} {name:>12} {cur:>18.3e} {she:>16.3e}")
        print()

    print("(2) a VALID m=2 spherical field f = sin^2(theta) * cos(2psi)  [must carry sin^2 theta")
    print("    for pole-regularity -- a bare mu-poly*cos2psi is NOT a regular m=2 field]")
    Nth, Nps = 12, 8
    mu, th, w = _gl_mu_nodes(Nth)
    Dmats = build_dtheta_exact(Nth, Nps // 2)
    psi = 2 * np.pi * np.arange(Nps) / Nps
    TH, PS = np.meshgrid(th, psi, indexing='ij')
    f = np.sin(TH)**2 * np.cos(2 * PS)
    df_ex = 2 * np.sin(TH) * np.cos(TH) * np.cos(2 * PS)          # d/dth sin^2 th = 2 sth cth
    print(f"  SH-exact err on sin^2(theta)*cos2psi (valid m=2) = "
          f"{np.max(np.abs(dtheta_exact(f, Dmats) - df_ex)):.3e}")
    print("\nDONE (build + validate only; no Newton/coupled solve).")
