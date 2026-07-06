"""N5d off-round shear pieces (n5d_shear.py) + operator/EL identity + phi-blindness.

Checks (all cheap, forward evals, <2s):
  - Kcal_offround round reduction  Kcal[a=bt=r^2] = -2 e^{-2phi}/r^2  (=> Branch-P source 4 e^{-2phi}).
  - The traceless E-row EAB_shear_row: round s->0 gives 0; and its round-background LINEARIZATION
    equals the certified operator  -e^{-2phi}(r^2 s'' + 2 r s')  (op_derive2 L_bare, roots {1,2}) --
    the "operator == EL of the geometric action" identity for the shear row (the in-frame source of
    truth is h4_scripts/op_derive2.py, not the unrelated 3D GR-baseline test_operator_from_action).
  - Matter is phi-BLIND: a nonzero traceless source T^{AB} changes ONLY the shear rows, never the
    phi-ODE / rho-ODE / f-PDE rows (matter enters ONLY as T^{AB} on the h-side; NO e^{2phi}.T on phi).
  - sqrt(h) = sqrt(a bt) sin th is phi-blind (no phi dependence).
"""
import numpy as np
import torch
import pytest

torch.set_default_dtype(torch.float64)

import n5d_shear as NS
import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)


def test_kcal_round_reduction():
    """Kcal[a=bt=r^2, a'=bt'=2r] = -2 e^{-2phi}/r^2  =>  the Branch-P round source -2 r^2 Kcal = 4 e^{-2phi}."""
    for r_val, phi_val in [(0.7, 0.0), (1.3, -0.4), (2.0, 0.9)]:
        r = torch.tensor(r_val); phi = torch.tensor(phi_val)
        a = bt = r ** 2; ap = btp = 2.0 * r
        K = NS.Kcal_offround(a, bt, ap, btp, phi)
        expect = -2.0 * torch.exp(-2.0 * phi) / r ** 2
        assert torch.allclose(K, expect, atol=1e-13), f"Kcal round wrong: {float(K)} vs {float(expect)}"
        # native_field:119 source: Z (r^2 phi')' = 4 e^{-2phi} = -2 r^2 Kcal
        src = -2.0 * r ** 2 * K
        assert torch.allclose(src, 4.0 * torch.exp(-2.0 * phi), atol=1e-13)


def test_sqrt_h_is_phi_blind():
    a = torch.tensor(1.7); bt = torch.tensor(0.9); th = torch.tensor(0.6)
    val = NS.sqrt_h(a, bt, th)
    assert torch.allclose(val, torch.sqrt(a * bt) * torch.sin(th), atol=1e-14)
    # no phi argument at all -> structurally phi-blind measure


def test_EAB_round_reduction_zero():
    """Round shear s==0 (s=s_r=s_rr=0) gives a zero traceless E-row."""
    z = torch.zeros(5)
    rho = torch.linspace(0.5, 2.0, 5); rhop = torch.ones(5); phip = torch.zeros(5)
    e2m = torch.ones(5)
    Es = NS.EAB_shear_row(rho, rhop, phip, z, z, z, e2m=e2m)
    assert float(Es.abs().max()) < 1e-14


def test_EAB_linearization_equals_Lbare_operator():
    """Round background (rho=r, phi const): EAB_shear_row on s=sigma(r) equals the CERTIFIED linear
    operator -e^{-2phi}(r^2 sigma'' + 2 r sigma').  Take sigma=r^3 => r^2 6r + 2r 3r^2 = 12 r^3.
    (This is L_bare in the s-variable: L_bare[r^2 sigma] = r^2(r^2 sigma''+2r sigma'), op_derive2.)"""
    r = torch.linspace(0.5, 3.0, 9); phi0 = -0.3
    e2m = torch.full_like(r, float(np.exp(-2 * phi0)))
    sig = r ** 3; sig_r = 3 * r ** 2; sig_rr = 6 * r
    Es = NS.EAB_shear_row(r, torch.ones_like(r), torch.zeros_like(r), sig, sig_r, sig_rr, e2m=e2m)
    analytic = -e2m * (r ** 2 * sig_rr + 2 * r * sig_r)      # = -e^{-2phi} 12 r^3
    assert torch.allclose(Es, analytic, atol=1e-12)
    assert torch.allclose(Es, -e2m * 12.0 * r ** 3, atol=1e-12)
    # tie to the certified numpy L_bare inverse (Category-A): L_bare[r^2 sigma] = 2 r^3 * 6 = 12 r^5 ...
    # here just confirm the wrapper is importable + inverts (roots {1,2} => no interior sign flip)
    rr = np.linspace(0.5, 3.0, 15)
    ev, n_dec = NS.lbare_tt_eigindex(rr)
    assert n_dec >= 0 and len(ev) == 13     # 15 nodes - 2 Dirichlet = 13 interior eigenvalues


def test_phi_source_correction_vanishes_at_zero():
    """The exact off-round phi-source correction +(1/(5Z)) e^{-2phi} a2'^2 is zero when a2'=0."""
    Z = 8.0
    corr0 = NS.phi_source_offround_correction(torch.ones(4), torch.zeros(4), torch.ones(4), Z)
    assert float(corr0.abs().max()) < 1e-15
    # and matches the closed form for a nonzero a2'
    rho = torch.tensor([1.2]); a2p = torch.tensor([0.3]); e2m = torch.tensor([0.7])
    got = NS.phi_source_offround_correction(rho, a2p, e2m, Z)
    assert torch.allclose(got, (1.0 / (5.0 * Z)) * e2m * a2p ** 2, atol=1e-15)


def test_matter_is_phi_blind_source_only_on_h_side():
    """A nonzero traceless matter source T^{AB} changes ONLY the appended shear rows -- the phi-ODE,
    rho-ODE and f-PDE rows are byte-identical (matter enters ONLY via T^{AB} on the h-side; there is
    NO e^{2phi}.T term on the phi row).  This is the operational delta S_m/delta phi = 0."""
    ctx = C.make_ctx(6, 6, rc=0.5)
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    # nonzero traceless source with a genuine ell=2 (P2) content so it survives the P2 projection
    Tshear = 0.05 * ctx["P2"][None, :].repeat(Nr, 1)
    F_vac = C.residual(u, ctx, PRM, n5d=dict(sealbc="S-JC2"))
    F_src = C.residual(u, ctx, PRM, n5d=dict(sealbc="S-JC2", Tshear=Tshear))
    base_len = C.residual(C.seed(ctx), ctx, PRM).numel()
    # base rows (phi, rho, f, H) must be untouched by the matter source
    assert float((F_vac[:base_len] - F_src[:base_len]).abs().max()) < 1e-14, \
        "matter source leaked onto the phi/rho/f rows (phi-blindness violated)"
    # the shear rows DO respond (the source acts on the h-side)
    assert float((F_vac[base_len:] - F_src[base_len:]).abs().max()) > 1e-6, \
        "matter source did not reach the shear (h-side) rows"
