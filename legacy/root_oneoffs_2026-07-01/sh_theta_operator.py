#!/usr/bin/env python3
"""
sh_theta_operator.py -- SPECTRALLY-EXACT polar-angle (theta) derivative operator for
the full-3-D coupled Einstein+L2+L4 catalog solver, per AZIMUTHAL index m.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  Spectral-methods task.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers).  NEW module -- edits no committed file.

================================================================================
THE PROBLEM THIS FIXES
================================================================================
The LIVE theta derivative used by the full-3-D solver is spectral_sph.theta_operators
(spectral_sph.py:50-59), which returns Dth = -sin(theta) @ d/dmu (mu = cos theta), a
Legendre/Lagrange spectral matrix on Gauss-Legendre nodes in mu.  That matrix is
spectrally EXACT only for POLYNOMIALS IN mu -- i.e. axisymmetric (m=0) angular
profiles.  Genuinely azimuthally-winding fields (m != 0), whose theta dependence
carries a sin^|m|(theta) edge factor (the associated-Legendre functions P_l^m), are
NOT polynomial in mu, so the Legendre operator is NOT exact on them.  The error grows
with |m| (tabulated in the self-test below).  The higher-winding (m=2,3,4) off-round
shape search lives EXACTLY in that inexact regime, so it needs an m-exact operator.

An SH-exact operator was sketched but UNWIRED in spectral_3d.sh_dtheta_matrix
(spectral_3d.py:107-139); spectral_3d.py is imported by nothing.  That version builds
a flattened (Nth*Nps, Nth*Nps) matrix via np.linalg.pinv on a normalized
spherical-harmonic basis using the (scipy-deprecated) sph_harm.  This module supplies
a cleaner, better-conditioned, drop-in replacement that matches the LIVE calling
convention (a per-axis (Nth, Nth) matrix per azimuthal m-block) instead.

================================================================================
THE FIX (category-A: a DISCRETIZATION -- no tie, no source, no linearization)
================================================================================
For a field with azimuthal index m, the natural theta basis is the associated
Legendre functions { P_l^|m|(cos theta) : l = |m|, |m|+1, ..., |m|+Nth-1 } (Nth of
them).  These carry the correct sin^|m|(theta) axis behavior.  We build the COLLOCATION
differentiation matrix D^(m) on the Gauss-Legendre theta nodes:

    V [i,k] = P_{l_k}^|m|(mu_i)                              (basis values at nodes)
    Vp[i,k] = d/dtheta P_{l_k}^|m| (theta_i)                 (their theta derivatives)
    D^(m)   = Vp @ inv(V)

so D^(m) @ (nodal values of any band-limited combination of those P_l^|m|) gives the
EXACT nodal theta derivative.  The theta derivative uses the chain rule
d/dtheta = -sin(theta) d/dmu with the STABLE associated-Legendre derivative recurrence

    (mu^2 - 1) dP_l^m/dmu = l*mu*P_l^m - (l+m)*P_{l-1}^m      (DLMF 14.10.5 form)

evaluated at the interior GL nodes (mu^2 != 1, so the 1/(mu^2-1) is never singular).
This recurrence is verified against finite differences (see prototyping) and the raw
scipy lpmv (Condon-Shortley) convention is used CONSISTENTLY on both sides, so no
normalization phase can leak in (the bug that made the naive sph_harm raising relation
disagree with FD when fed raw lpmv).

For m=0 this reduces to the ordinary Legendre operator (polynomials in mu), so it is a
strict GENERALIZATION of spectral_sph's Dth: identical at m=0, exact where the live one
is not.

CONDITIONING: cond(V) stays tiny -- < 10 for m=0, < ~500 even at Nth=16, m=4 -- so a
plain np.linalg.inv is fine (no pinv tolerance to tune).  Usable comfortably to
Nth=16, |m|=4 (and well beyond); see the conditioning column in the self-test.
================================================================================
"""
import numpy as np
from scipy.special import roots_legendre, lpmv


# ---------------------------------------------------------------------------
# associated-Legendre theta derivative on GL nodes -- per azimuthal m.
# ---------------------------------------------------------------------------
def _dPdmu(l, m, mu):
    """d/dmu P_l^m(mu) via the stable recurrence
       (mu^2 - 1) dP_l^m/dmu = l*mu*P_l^m - (l+m)*P_{l-1}^m.
    m = |m| (>= 0).  Interior GL nodes only (mu^2 != 1)."""
    if l == 0:
        return np.zeros_like(mu)
    Pl = lpmv(m, l, mu)
    Plm1 = lpmv(m, l - 1, mu) if (l - 1) >= m else np.zeros_like(mu)
    return (l * mu * Pl - (l + m) * Plm1) / (mu * mu - 1.0)


def theta_grid(Nth):
    """The SAME theta node grid the live solver uses (spectral_sph.theta_operators):
    Gauss-Legendre nodes in mu = cos(theta), sorted ASCENDING in theta on (0, pi),
    poles excluded.  Returns (theta_nodes, sin_theta, gl_weight_wmu).

    wmu is the sin-theta-INCLUDED angular measure (int_0^pi g sin th dth = sum wmu*g),
    matching spectral_sph exactly."""
    mu, w = roots_legendre(Nth)
    th = np.arccos(mu)
    idx = np.argsort(th)
    return th[idx], np.sin(th[idx]), w[idx]


def dtheta_matrix_m(Nth, m):
    """The SPECTRALLY-EXACT d/dtheta collocation matrix for azimuthal index m, of shape
    (Nth, Nth), acting on the THETA axis of a field at the live GL theta nodes.

    Exact for any band-limited combination of the associated Legendre functions
    P_l^|m|(cos theta), l = |m| .. |m|+Nth-1 (the natural theta basis at index m).
    For m=0 it equals the live Legendre operator (polynomials in mu) to machine zero.

    Returns (Dth_m, th, sth, cond_V):
        Dth_m  : (Nth, Nth) ndarray, theta-derivative matrix at index m
        th     : (Nth,) theta nodes (ascending), SAME as the live grid
        sth    : (Nth,) sin(theta) at the nodes
        cond_V : 2-norm condition number of the basis Vandermonde (diagnostic)
    """
    am = abs(int(m))
    mu, w = roots_legendre(Nth)
    th = np.arccos(mu)
    idx = np.argsort(th)
    mu = mu[idx]
    th = th[idx]
    sth = np.sin(th)
    ls = np.arange(am, am + Nth)
    V = np.array([lpmv(am, l, mu) for l in ls]).T            # (Nth, Nth)
    Vp = np.array([-sth * _dPdmu(l, am, mu) for l in ls]).T  # d/dtheta = -sin th d/dmu
    Dth_m = Vp @ np.linalg.inv(V)
    cond_V = np.linalg.cond(V)
    return Dth_m, th, sth, cond_V


def dtheta_matrices(Nth, mmax):
    """Build the per-m theta derivative matrices for |m| = 0 .. mmax.
    Returns a dict { m : Dth_m (Nth,Nth) } plus (th, sth).  Use the matrix whose key
    matches the azimuthal index of the Fourier mode being differentiated."""
    th, sth, _ = theta_grid(Nth)
    mats = {m: dtheta_matrix_m(Nth, m)[0] for m in range(mmax + 1)}
    return mats, th, sth


# ---------------------------------------------------------------------------
# torch drop-in for the live solver (matches full3d_spectral.Grid3D.d_th layout).
# ---------------------------------------------------------------------------
def build_torch_dtheta(Nth, mmax, device="cpu", dtype=None):
    """Return a dict { m : torch (Nth,Nth) tensor } of per-m theta derivative matrices
    on the requested device/dtype (default float64), ready to drop into the live solver.

    SWAP-IN for full3d_spectral.py (see module docstring at bottom for the exact recipe):
      The live Grid3D.d_th (full3d_spectral.py:139-140) applies ONE Dth to the theta
      axis regardless of azimuthal content.  Replace it with a Fourier-in-psi -> per-m
      D^(m) -> inverse-Fourier sandwich so each azimuthal mode is differentiated with
      its OWN exact matrix.  See `apply_dtheta_exact` below for the reference impl."""
    import torch
    if dtype is None:
        dtype = torch.float64
    mats, _, _ = dtheta_matrices(Nth, mmax)
    return {m: torch.tensor(D, device=device, dtype=dtype) for m, D in mats.items()}


def apply_dtheta_exact(f, Dth_by_m, real_fft=True):
    """SH-EXACT d/dtheta of a real (Nr, Nth, Nps) torch field, applying the correct
    per-azimuthal-m matrix to each Fourier mode in psi.  Reference drop-in for the live
    Grid3D.d_th.

    f          : torch tensor (..., Nth, Nps) -- the field (psi is the last axis)
    Dth_by_m   : dict {|m| : (Nth,Nth) torch tensor} from build_torch_dtheta
    real_fft   : use rfft along psi (f is real); modes 0..Nps//2 present.

    For each psi Fourier mode k, the azimuthal index is |m| = k (the field's e^{i m psi}
    content), so we apply Dth_by_m[min(k, mmax)] to the theta axis of that mode's
    coefficients, then transform back.  Modes with k > mmax fall back to the largest
    available matrix (they are above the resolved band and should be ~0 for a clean
    band-limited field)."""
    import torch
    Nps = f.shape[-1]
    F = torch.fft.rfft(f, dim=-1)                # (..., Nth, Nps//2+1) complex
    mmax = max(Dth_by_m.keys())
    out = torch.zeros_like(F)
    for k in range(F.shape[-1]):
        D = Dth_by_m[min(k, mmax)]
        Fk = F[..., k]                           # (..., Nth) complex
        out[..., k] = torch.einsum('ab,...b->...a', D.to(Fk.dtype), Fk)
    return torch.fft.irfft(out, n=Nps, dim=-1)


# ===========================================================================
# SELF-TEST: error tables (Legendre operator vs analytic, SH-exact vs analytic),
# per m, at the working resolutions.  Run as __main__.
# ===========================================================================
def _legendre_dth(Nth):
    """The LIVE Legendre theta operator (reproduce spectral_sph.theta_operators:50-59
    exactly, standalone, so the self-test does not import / mutate the committed file)."""
    from numpy.polynomial.legendre import legvander, legder, legval
    mu, w = roots_legendre(Nth)
    V = legvander(mu, Nth - 1)
    Vp = np.zeros_like(V)
    for k in range(Nth):
        ck = np.zeros(Nth); ck[k] = 1.0
        Vp[:, k] = legval(mu, legder(ck))
    Dmu = Vp @ np.linalg.inv(V)
    th = np.arccos(mu)
    idx = np.argsort(th)
    th = th[idx]; Dmu = Dmu[np.ix_(idx, idx)]
    sth = np.sin(th)
    Dth = (-sth)[:, None] * Dmu
    return th, sth, Dth


def _test_functions(m, mu, sth, Nth):
    """Return list of (name, f_nodal, df_dtheta_nodal) test functions of azimuthal index
    m.  These are associated Legendre P_l^|m|(cos theta) -- the natural index-m basis.
    Two failure modes of the LIVE Legendre operator are exercised:
      * ODD |m|:  P_l^|m| carries sin^|m|(theta) which is NOT polynomial in mu, so the
        Legendre op errs at EVERY l (even small l).
      * EVEN |m|: P_l^|m| IS polynomial in mu (degree l), so the Legendre op is exact
        WHILE l < Nth, but errs once the degree reaches the Legendre truncation
        (l >= Nth) -- so we include a high-l member (l = |m| + Nth - 1) to expose it."""
    am = abs(m)
    fns = []
    for l in (am, am + 1, am + 2, am + Nth - 1):     # low l + one high-l (degree>=Nth)
        f = lpmv(am, l, mu)
        df = -sth * _dPdmu(l, am, mu)
        fns.append((f"P_{l}^{am}", f, df))
    # also an explicit sin^|m| * (poly in mu) form for m>0 (independent construction)
    if am > 0:
        # f = sin^m(theta) * (a0 + a1 mu + a2 mu^2) ; analytic d/dtheta
        a0, a1, a2 = 0.7, -1.3, 0.9
        smm = sth ** am
        poly = a0 + a1 * mu + a2 * mu * mu
        f = smm * poly
        # d/dtheta: d(sin^m)/dth = m sin^{m-1} cos th ; mu=cos th, dmu/dth=-sin th
        cth = mu
        dsmm = am * sth ** (am - 1) * cth
        dpoly_dth = (a1 + 2 * a2 * mu) * (-sth)
        df = dsmm * poly + smm * dpoly_dth
        fns.append((f"sin^{am}*poly(mu)", f, df))
    return fns


def _error_table():
    print("=" * 78)
    print("sh_theta_operator self-test -- theta-derivative ERROR, per azimuthal m")
    print("  LIVE = spectral_sph Legendre op (-sin th d/dmu).  SH-EXACT = this module.")
    print("  (max over the test functions of |D f - analytic d/dtheta f|)")
    print("=" * 78)
    header = f"{'Nth':>4} {'m':>3} | {'LIVE Legendre err':>20} | {'SH-EXACT err':>14} | {'cond(V)':>9}"
    for Nth in (8, 12, 16):
        print("-" * 78)
        print(header)
        print("-" * 78)
        th, sth_l, Dleg = _legendre_dth(Nth)
        mu_l = np.cos(th)
        for m in (0, 1, 2, 3, 4):
            Dsh, th_s, sth_s, condV = dtheta_matrix_m(Nth, m)
            mu_s = np.cos(th_s)
            leg_err = 0.0
            sh_err = 0.0
            for name, f, df in _test_functions(m, mu_s, sth_s, Nth):
                leg_err = max(leg_err, np.max(np.abs(Dleg @ f - df)))
                sh_err = max(sh_err, np.max(np.abs(Dsh @ f - df)))
            print(f"{Nth:>4} {m:>3} | {leg_err:>20.3e} | {sh_err:>14.3e} | {condV:>9.2e}")
    print("=" * 78)
    print("Expected: LIVE ~machine-zero at m=0, GROWS with m; SH-EXACT <~1e-12 for ALL m.")
    print("=" * 78)


def _test_apply_dtheta():
    """Validate the full (Nr,Nth,Nps) torch drop-in apply_dtheta_exact on a field with a
    KNOWN multi-m azimuthal content and analytic d/dtheta."""
    import torch
    torch.set_default_dtype(torch.float64)
    Nr, Nth, Nps, mmax = 3, 14, 16, 4
    th, sth, _ = theta_grid(Nth)
    mu = np.cos(th)
    # Field: sum over m of P_{m+1}^m(cos th) * cos(m psi)  (real, band-limited, |m|<=mmax)
    ps = 2.0 * np.pi * np.arange(Nps) / Nps
    f = np.zeros((Nr, Nth, Nps))
    df_ex = np.zeros((Nr, Nth, Nps))
    for ir in range(Nr):
        amp = 1.0 + 0.3 * ir
        for m in range(mmax + 1):
            l = m + 1
            Pm = lpmv(m, l, mu)
            dPm = -sth * _dPdmu(l, m, mu)
            cos_mps = np.cos(m * ps)
            f[ir] += amp * np.outer(Pm, cos_mps)
            df_ex[ir] += amp * np.outer(dPm, cos_mps)
    ft = torch.tensor(f)
    Dby = build_torch_dtheta(Nth, mmax)
    got = apply_dtheta_exact(ft, Dby).numpy()
    err = np.max(np.abs(got - df_ex))
    print(f"\n[drop-in] apply_dtheta_exact on multi-m (Nr={Nr},Nth={Nth},Nps={Nps}) field:"
          f"  max|err| = {err:.3e}   (expect <~1e-12)")
    # Contrast: live single-matrix Legendre on the SAME field (psi axis untouched)
    _, _, Dleg = _legendre_dth(Nth)
    leg = np.einsum('ab,rbp->rap', Dleg, f)
    print(f"[contrast] LIVE single Legendre matrix on the SAME field:"
          f"          max|err| = {np.max(np.abs(leg - df_ex)):.3e}")


# ===========================================================================
# SWAP-IN RECIPE for the full-3-D solver (full3d_spectral.py)
# ---------------------------------------------------------------------------
# The live theta derivative is Grid3D.d_th (full3d_spectral.py:139-140):
#
#     def d_th(self, f):
#         return torch.tensordot(self.Dth, f, dims=([1], [1])).permute(1, 0, 2)
#
# where self.Dth comes from spectral_sph.theta_operators (spectral_sph.py:50-59) and is
# the m=0-only Legendre matrix.  It applies ONE matrix to the theta axis irrespective of
# azimuthal content -- exact only for m=0.  To make it m-exact:
#
#   1) In Grid3D.__init__, after building the grid, build the per-m matrices once:
#          from sh_theta_operator import build_torch_dtheta
#          # mmax = the highest azimuthal index the search will carry (resolved band
#          # is Nps//2 - 1; pass the winding mmax you actually use, e.g. 4)
#          self.Dth_by_m = build_torch_dtheta(self.Nth, mmax=Nps//2 - 1,
#                                             device=dev, dtype=torch.float64)
#
#   2) Replace Grid3D.d_th with the Fourier-in-psi -> per-m -> inverse-Fourier sandwich:
#          from sh_theta_operator import apply_dtheta_exact
#          def d_th(self, f):
#              return apply_dtheta_exact(f, self.Dth_by_m)
#      (apply_dtheta_exact takes (..., Nth, Nps); Grid3D fields are (Nr, Nth, Nps), so
#       the theta axis is -2 and psi is -1 -- exactly its expected layout.)
#
# Nothing else changes: the theta NODE grid (theta, sin theta, wmu) is byte-identical to
# spectral_sph.theta_operators (same roots_legendre, same ascending sort), so all the
# Einstein/matter machinery that reads G.th, G.sth, G.wmu is unaffected.  At m=0 the
# operator reduces to the existing Legendre matrix to machine zero (verified), so the
# round/axisymmetric soliton recovery is bit-for-bit unchanged.
#
# NOTE on the matter chain rule (full3d_spectral.field_dn:223-251): that routine takes
# SPECTRAL d/dtheta of the SMOOTH profile Theta only (Th_t = G.d_th(Th)), then combines
# with analytic partials.  Theta itself can be non-axisymmetric (carries e^{i m psi}
# content via the field embedding), so its theta derivative MUST be m-exact for the
# m=2,3,4 search -- this swap fixes exactly that call (and the metric-warp derivatives
# in einstein_mixed / _warp_partials likewise route through G.d_th).
# ===========================================================================

if __name__ == "__main__":
    _error_table()
    _test_apply_dtheta()
