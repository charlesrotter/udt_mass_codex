#!/usr/bin/env python3
"""
full3d_grid_shexact.py -- SH-EXACT-theta variant of the full-3-D coupled
Einstein+L2+L4 grid.  Drops the spectrally-EXACT (per-azimuthal-m) polar-angle
derivative operator (sh_theta_operator.apply_dtheta_exact) into the full-3-D solver
so that ALL theta derivatives -- metric-warp AND matter-profile -- are m-exact for
EVERY azimuthal mode, not just m=0 (the Legendre operator's exact regime).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  Spectral-methods PREP task.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers).  NEW module -- edits no committed file.

================================================================================
WHY (category-A: a DISCRETIZATION-ACCURACY upgrade -- the SAME equations)
================================================================================
The live full-3-D theta derivative is Grid3D.d_th (full3d_spectral.py:139-140), built
on spectral_sph.theta_operators (spectral_sph.py:50-59).  That is the Legendre/Lagrange
operator -sin(th) d/dmu, EXACT only for polynomials in mu = cos th -- i.e. axisymmetric
(azimuthal m=0) shapes.  For genuinely non-axisymmetric / higher-winding fields (the
platonic Skyrmion ground states the downstream search targets), the theta dependence
carries the sin^|m|(theta) edge factor of the associated Legendre P_l^|m|, which is NOT
polynomial in mu, so the Legendre operator is INEXACT (errors 39..9e5 at m=1..4 -- see
sh_theta_operator.py self-test).

sh_theta_operator.apply_dtheta_exact cures this: Fourier-in-psi -> apply the per-m exact
matrix D^(m) to each azimuthal mode -> inverse-Fourier.  At m=0 it equals the Legendre
operator to machine zero, so the round/axisym recovery is bit-for-bit unchanged (the
regression gate).  Off-round it is exact where the Legendre operator is not.

================================================================================
THE WIRING -- ONE ROUTING POINT
================================================================================
Every theta derivative in the coupled residual flows through Grid3D.d_th:
  * metric-warp d/dtheta : einstein_3d_eval.warp_derivs (einstein_3d_eval.py:24-30) and
    full3d_spectral._warp_partials (full3d_spectral.py:290-294) -> both call G.d_th
    (and compose it for ft, ftt, frt, ftp -- so the 2nd theta derivatives are exact too).
  * matter-profile d/dtheta : full3d_spectral.field_dn (full3d_spectral.py:237, Th_t =
    G.d_th(Th)) -- the spectral theta derivative of the SMOOTH profile Theta.
  * div(T) checker : full3d_spectral.divT_identity (full3d_spectral.py:368) -> G.d_th.
So OVERRIDING Grid3D.d_th makes ALL of them exact at once.  No other edit is needed; the
theta NODE grid (th, sth, wmu, wvol, wvol_coord) is byte-identical (we reuse the parent
Grid3D's own grid construction, which calls the SAME spectral_sph.theta_operators), so
every piece of Einstein/matter machinery that reads G.th/G.sth/G.wmu/G.wvol is unaffected.

We deliberately subclass (GridSHExact(Grid3D)) and override ONLY d_th, rather than
duplicating Grid3D, so that node layout cannot drift from the committed grid.

================================================================================
USAGE for the downstream platonic / non-axisym search
================================================================================
The ONLY call that changes vs full3d_newton's usage:

    # before (Legendre theta op -- m=0-exact only):
    from full3d_spectral import Grid3D, attach_coord_weight
    G = Grid3D(Nr, Nth, Nps, rc=0.05, cell=14.0); G = attach_coord_weight(G)

    # after (SH-exact theta op -- m-exact for ALL azimuthal modes):
    from full3d_grid_shexact import make_grid_shexact
    G = make_grid_shexact(Nr, Nth, Nps, rc=0.05, cell=14.0, mmax=Nps//2)

Everything downstream is unchanged: full3d_solver.residual_vector,
full3d_newton.residual_vector_vsafe / newton_solve / continuation all import the matter
and Einstein helpers that route through G.d_th, so they pick up the exact operator
automatically (residual_vector_vsafe imports field_dn / matter_el_3d / einstein_mixed_weyl
from full3d_spectral, all of which take G as their first arg and call G.d_th).

CAVEATS / LIMITS (carry into the search push):
  * mmax: pass mmax >= the highest azimuthal index the field carries.  The rfft over psi
    resolves modes k = 0..Nps//2 (Nps//2 = Nyquist for even Nps).  build_torch_dtheta is
    asked for blocks 0..mmax; any psi Fourier mode k > mmax FALLS BACK to the mmax block
    (sh_theta_operator.apply_dtheta_exact:170) -- exact only if those high modes are ~0
    (a clean band-limited field).  SAFEST: mmax = Nps//2 so EVERY resolvable mode has its
    own exact block (recommended default in make_grid_shexact).
  * rfft Nyquist caveat (even Nps): the Nyquist mode k=Nps//2 is real and represents
    cos(Nyquist*psi); it is differentiated with the |m|=Nps//2 block.  A field with real
    azimuthal content AT Nyquist is under-resolved in psi regardless of the theta op; keep
    the winding mmax strictly below Nps//2 (Nps >= 2*m_winding + 2) so Nyquist carries no
    physical signal -- standard de-aliasing, not specific to this operator.
  * Nth / |m| conditioning: cond(V) of the per-m basis stays < ~500 up to Nth=16, |m|=4
    (sh_theta_operator docstring:57-59), so plain inv is fine; usable comfortably to
    Nth=16, |m|=4 and beyond.
  * COST: d_th changes from a single (Nth,Nth) matmul to an rfft + (Nps//2+1) per-mode
    (Nth,Nth) matmuls + irfft along psi.  This is O(Nps) more theta-matmuls per d_th call
    but each is tiny (Nth<=16); on the validation grids it is a small constant overhead.
    The matrices are built ONCE in __init__ and cached (G.Dth_by_m).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import Grid3D, attach_coord_weight, DEV
from sh_theta_operator import build_torch_dtheta, apply_dtheta_exact


class GridSHExact(Grid3D):
    """Grid3D whose theta derivative is the SH-exact (per-azimuthal-m) operator.

    Identical to Grid3D in EVERY way except d_th: same node grid (th, sth, wmu),
    same r/psi operators, same coordinate fields, same body mask, same weights.
    Only the theta-derivative routing is replaced -- so all Einstein/matter machinery
    that reads the grid or calls G.d_th is transparently upgraded to m-exact theta.

    mmax: highest azimuthal index given its OWN exact theta block.  Defaults to
    Nps//2 (every rfft-resolvable psi mode gets an exact matrix).  See module
    docstring for the Nyquist / fall-back caveats.
    """
    def __init__(self, Nr, Nth, Nps, rc=0.05, cell=14.0, dev=DEV, mmax=None):
        super().__init__(Nr, Nth, Nps, rc=rc, cell=cell, dev=dev)
        if mmax is None:
            mmax = Nps // 2                      # every rfft mode (0..Nps//2) gets a block
        self.mmax_theta = int(mmax)
        # per-azimuthal-m exact theta matrices, built ONCE on the SAME Nth GL nodes.
        self.Dth_by_m = build_torch_dtheta(self.Nth, mmax=self.mmax_theta,
                                           device=dev, dtype=torch.float64)

    # ---- the ONLY override: SH-exact theta derivative ----------------------
    def d_th(self, f):
        """SH-exact d/dtheta: Fourier-in-psi -> per-m exact matrix -> inverse-Fourier.
        f is (Nr, Nth, Nps); theta is axis -2, psi is axis -1 -- apply_dtheta_exact's
        expected (..., Nth, Nps) layout.  Reduces to the Legendre op at m=0 to machine
        zero, so psi-independent (axisym) fields are differentiated identically to the
        committed Grid3D.d_th (the regression gate)."""
        return apply_dtheta_exact(f, self.Dth_by_m)


def make_grid_shexact(Nr, Nth, Nps, rc=0.05, cell=14.0, dev=DEV, mmax=None):
    """Build a SH-exact-theta grid WITH the coordinate quadrature weight attached
    (the one call that replaces `Grid3D(...) ; attach_coord_weight(...)` in the
    downstream search).  Returns a ready-to-use grid."""
    G = GridSHExact(Nr, Nth, Nps, rc=rc, cell=cell, dev=dev, mmax=mmax)
    G = attach_coord_weight(G)          # sets G.wvol_coord (uses G.wr/wmu/sth/wps -- shared)
    return G


# ===========================================================================
# Legendre-grid d_th, standalone, for the ENGAGEMENT contrast in the test harness
# (an exact reproduction of the committed Grid3D.d_th, so we can compare the two
# operators on the SAME state without mutating the committed module).
# ===========================================================================
def legendre_d_th(G, f):
    """The committed Grid3D.d_th (full3d_spectral.py:139-140) applied via the parent's
    Legendre Dth matrix -- single (Nth,Nth) matmul on the theta axis, azimuth-blind."""
    return torch.tensordot(G.Dth, f, dims=([1], [1])).permute(1, 0, 2)


if __name__ == "__main__":
    # quick self-smoke: at m=0 (psi-flat field) the override must equal the Legendre op.
    G = make_grid_shexact(Nr=20, Nth=8, Nps=8, rc=0.05, cell=14.0, mmax=4)
    # psi-independent (axisym) field: a smooth function of (r, th) broadcast over psi
    mu = torch.cos(G.THg)
    f0 = (0.5 * (5 * mu**3 - 3 * mu)) * torch.exp(-G.Rg)        # P3(cos th) * e^{-r}
    d_exact = G.d_th(f0)
    d_leg = legendre_d_th(G, f0)
    print(f"[smoke] axisym field: ||SH-exact d_th - Legendre d_th||_inf = "
          f"{float((d_exact - d_leg).abs().max()):.3e}   (must be ~1e-13: m=0 equality)")
    # psi-dependent field: the two MUST differ (operator is engaged)
    f1 = f0 + torch.sin(G.THg) * torch.cos(2 * G.PSg) * torch.exp(-G.Rg)
    print(f"[smoke] psi-dep field: ||SH-exact d_th - Legendre d_th||_inf = "
          f"{float((G.d_th(f1) - legendre_d_th(G, f1)).abs().max()):.3e}   "
          f"(must be > 0: engagement)")
