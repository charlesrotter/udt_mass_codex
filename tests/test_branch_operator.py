"""Guard the DERIVED scalar-tensor operator with the EXPLICIT branch switch (branch_operator.py).

Cheap forward evals only (NO coupled solve / jacrev); bounded grids; <2s.  Checks:
  (1) FLAT (phi=0, warps=0, T=0): E=0 to ~1e-10, BOTH branches.
  (2) BRANCH-G VACUUM: Schwarzschild + CONSTANT phi is an exact two-player vacuum
      (E tracks the bare Einstein tensor; the f-derivative terms vanish for const phi),
      and SLAVED phi'(r)!=0 makes box f != 0 (vacuum != GR) -- both documented facts.
  (3) BRANCH-P vs BRANCH-G: the ONLY operator difference is + delta^mu_nu U(phi),
      U=e^{2phi}-1; the phi-EOM difference is exactly -2 U'(phi).
  (4) The branch parameter is EXPLICIT/validated; an unknown branch raises.

References: matter_regrade_derived_operator_results.md (lines 60-61), branch_G/P_characterization.
"""
import math
import torch
import pytest

torch.set_default_dtype(torch.float64)

from full3d_spectral import Grid3D, attach_coord_weight, T, R, TH, PS
import branch_operator as BO


def _grid(Nr=16, Nth=8, Nps=8, rc=0.3, cell=2.0):
    return attach_coord_weight(Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=rc, cell=cell))


def _dn0(G):
    """Vacuum matter: dn = 0 (...,4,3) -> T = 0 (the operator now takes the matter via dn)."""
    return torch.zeros(G.Nr, G.Nth, G.Nps, 4, 3, device=G.Rg.device)


def _native_dn(G):
    """A native-S^2 matter dn (the canon degree-1 winding n=x/r)."""
    import free_s2_matter as S2M
    return S2M.field_dn_components_exact(G, S2M.hedgehog_xr_components(G, m=1))


# =============================================================================
# (1) FLAT: E = 0 to ~1e-10 for BOTH branches (phi=0 => U=0, so P == G here).
# =============================================================================
@pytest.mark.parametrize("branch", ["G", "P"])
def test_flat_vacuum_E_zero(branch):
    G = _grid()
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=G.Rg.device)
    E = BO.E_mixed_branch(G, z, z, z, z, z, _dn0(G), X=BO.X_PROD, xi=BO.XI_PROD, kap=BO.KAP_PROD, branch=branch)   # phi=0, warps=0, Th=0 (T=0)
    mx = float(E[G.body].abs().max())
    assert mx < 1e-9, f"branch {branch}: flat E != 0, max|E|(body) = {mx:.2e}"


# =============================================================================
# (2) BRANCH-G VACUUM: Schwarzschild + CONSTANT phi.  box f = 0 (const phi) so the
#     non-minimal terms vanish and E reduces to the bare Einstein tensor (= 0 to the
#     spectral resolution on the steep Schwarzschild metric).  This is branch_G 2a:
#     "Schwarzschild with ANY constant phi is an exact Branch-G vacuum solution."
# =============================================================================
def test_branchG_schwarzschild_const_phi_is_vacuum():
    rs = 1.0   # FREE test value (Schwarzschild radius, units L=1)
    G = _grid(Nr=20, Nth=8, Nps=8, rc=1.5, cell=4.0)     # body r all > rs
    f_schw = 1.0 - rs / G.Rg
    a_s = 0.5 * torch.log(f_schw)        # g_tt = -e^{2a} = -(1-rs/r)
    b_s = -0.5 * torch.log(f_schw)       # g_rr =  e^{2b} = 1/(1-rs/r)
    z = torch.zeros_like(G.Rg)
    phi_c = torch.full_like(G.Rg, 0.37)  # ARBITRARY constant phi (pure gauge); FREE
    parts = BO.E_mixed_branch(G, a_s, b_s, z, z, phi_c, _dn0(G), X=BO.X_PROD, xi=BO.XI_PROD, kap=BO.KAP_PROD, branch="G", return_parts=True)
    boxf = float(parts["boxf"][G.body].abs().max())
    Gmag = float(parts["Gmix"][G.body].abs().max())
    Emag = float(parts["E"][G.body].abs().max())
    assert boxf < 1e-10, f"box f for CONSTANT phi must vanish; got {boxf:.2e}"
    # E reduces to bare G (const phi kills f-deriv & kinetic terms); both at the
    # spectral floor for the steep Schwarzschild metric on a small grid.
    assert Emag < 1e-4, f"Branch-G E on Schw+const-phi not ~0: {Emag:.2e}"
    assert Emag < 5.0 * Gmag + 1e-12, "E should reduce to bare G for constant phi"


def test_branchG_slaved_phi_breaks_freeze():
    """SLAVED Schwarzschild phi (phi'(r)!=0, phi tied to g_rr) => box f != 0 => vacuum != GR.
    The full two-player E is NOT zero on slaved-Schwarzschild (f-derivative hair survives)."""
    rs = 1.0
    G = _grid(Nr=20, Nth=8, Nps=8, rc=1.5, cell=4.0)
    f_schw = 1.0 - rs / G.Rg
    phi_sl = -0.5 * torch.log(f_schw)     # e^{2phi} = g_rr (slaved)
    a, b, c, d = BO.slaved_warps_from_phi(phi_sl)
    z = torch.zeros_like(G.Rg)
    parts = BO.E_mixed_branch(G, a, b, c, d, phi_sl, _dn0(G), X=BO.X_PROD, xi=BO.XI_PROD, kap=BO.KAP_PROD, branch="G", return_parts=True)
    boxf = float(parts["boxf"][G.body].abs().max())
    assert boxf > 1e-2, f"slaved phi'(r)!=0 must give box f != 0 (vacuum != GR); got {boxf:.2e}"


# =============================================================================
# (3) BRANCH-P vs BRANCH-G differ by EXACTLY + delta^mu_nu U(phi); phi-EOM by -2U'.
# =============================================================================
def _smooth_config(G):
    Rg = G.Rg
    a = 0.04 * torch.cos(G.THg) * torch.exp(-(Rg - 1.0) ** 2)
    b = 0.03 * torch.exp(-(Rg - 1.0) ** 2)
    c = 0.02 * torch.sin(2 * G.PSg) * torch.exp(-(Rg - 1.0) ** 2)
    d = 0.01 * torch.exp(-(Rg - 1.0) ** 2)
    phi = 0.2 * torch.exp(-(Rg - 1.0) ** 2) * (1 + 0.1 * torch.cos(G.THg))
    dn = _native_dn(G)
    return a, b, c, d, phi, dn


def test_branchP_minus_branchG_is_potential():
    G = _grid()
    a, b, c, d, phi, dn = _smooth_config(G)
    EG = BO.E_mixed_branch(G, a, b, c, d, phi, dn, X=BO.X_PROD, xi=BO.XI_PROD, kap=BO.KAP_PROD, branch="G")
    EP = BO.E_mixed_branch(G, a, b, c, d, phi, dn, X=BO.X_PROD, xi=BO.XI_PROD, kap=BO.KAP_PROD, branch="P")
    U = BO.U_potential(phi)
    delta = torch.eye(4, device=EG.device).expand(*phi.shape, 4, 4)
    expected = delta * U[..., None, None]
    err = float((EP - EG - expected)[G.body].abs().max())
    assert err < 1e-11, f"E_P - E_G != +delta*U: max|diff|(body) = {err:.2e}"
    # and the difference is genuinely nonzero (U is O(0.1) here)
    assert float(U[G.body].abs().max()) > 1e-3


def test_branchP_phi_eom_adds_minus_2Uprime():
    G = _grid()
    a, b, c, d, phi, dn = _smooth_config(G)
    elG = BO.EL_phi_branch(G, a, b, c, d, phi, dn, X=BO.X_PROD, xi=BO.XI_PROD, kap=BO.KAP_PROD, branch="G")
    elP = BO.EL_phi_branch(G, a, b, c, d, phi, dn, X=BO.X_PROD, xi=BO.XI_PROD, kap=BO.KAP_PROD, branch="P")
    expected = -2.0 * BO.U_prime(phi)
    diff = elP - elG
    scale = float(elG[G.body].abs().max()) + 1.0
    rel = float((diff - expected)[G.body].abs().max() / scale)
    assert rel < 1e-9, f"phi-EOM P-G != -2U': rel err = {rel:.2e}"


# =============================================================================
# (4) The branch switch is EXPLICIT and validated -- no silent default-smuggling.
# =============================================================================
def test_branch_is_explicit_and_validated():
    G = _grid()
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=G.Rg.device)
    # default is the named Branch G (the operator the native-S^2 solves used)
    import inspect
    sig = inspect.signature(BO.E_mixed_branch)
    assert sig.parameters["branch"].default == "G", "default branch must be explicit 'G'"
    # an unknown branch must RAISE (no silent fallback)
    with pytest.raises(ValueError):
        BO.E_mixed_branch(G, z, z, z, z, z, _dn0(G), branch="Q")
    with pytest.raises(ValueError):
        BO.EL_phi_branch(G, z, z, z, z, z, _dn0(G), branch="Q")
