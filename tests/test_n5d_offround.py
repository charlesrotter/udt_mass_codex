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


def test_matter_source_is_phi_blind_stage2():
    """STAGE-2: the LIVE matter shear source T_s (and the matter f-PDE + matter moments) is phi-BLIND --
    L_m has NO phi (only rho, s, f), so shifting phi at fixed rho,f,a2 leaves T_s, the off-round matter
    moments, and res_f unchanged; only the GEOMETRIC pieces (phi_ode, the e^{-2phi} in Es_geom) move.
    This is the operational delta S_m/delta phi = 0."""
    ctx = C.make_ctx(6, 6, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=True)
    n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    Q0 = C.fields(u, ctx, PRM, n5d=n5d)
    u2 = C.pack(phi + 0.41, rho, uf, float(L), a2=a2)              # shift phi, hold rho,f,a2
    Q1 = C.fields(u2, ctx, PRM, n5d=n5d)
    for key in ("Ts", "Tshear_live", "res_f", "Ith_es", "Is_es", "I4r_es"):
        assert torch.allclose(Q0[key], Q1[key], atol=1e-14), f"matter piece {key} depends on phi -> NOT phi-blind"
    # sanity: the source is genuinely nonzero (else the blindness check is vacuous), and Es_geom DOES move
    assert float(Q0["Ts"].abs().max()) > 1e-6, "live T_s is ~0 -> phi-blindness check would be vacuous"
    assert float((Q0["Es_geom"] - Q1["Es_geom"]).abs().max()) > 1e-9, "geometric E-row must move with phi (e^{-2phi})"
