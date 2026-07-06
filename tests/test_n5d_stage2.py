"""N5d STAGE-2 co-relaxed matter gate (pi_2 axisymmetric tile; DESIGN / PROVISIONAL / Outcome D).

The 8 tests that MUST pass BEFORE any Stage-2 pilot is allowed (n5d_stage2_corelaxed_matter_DESIGN.md sec7,
Charles-gated 2026-07-06).  ASSEMBLY / forward-eval + one bounded Jacobian only -- NO pilot solve, NO verdict,
NO Outcome A/B (anti-hang: bounded grid, single foreground process, hard iteration cap).

Pinned formulas (all CAS + blind-verified: n5d_stage2a_cas_results.md, n5d_stage2b_gate05_report.md):
  - off-round f-PDE: A/f_r = xi rho^2 sin th + kap N^2 sin^2 f e^{s}/sin th ; B/f_th = xi e^{-s} sin th + ...
  - live shear source:  Tshear_live = -(rho^2/4) T_s   (matter->geometry coupling lambda = -1/2, NOT +(rho^2/2))
      T_s = (xi/rho^2)[N^2 e^{s} sin^2 f/sin^2 th - f_th^2 e^{-s}] + (kap N^2/rho^2) f_r^2 e^{s} sin^2 f/sin^2 th
  - off-round Hseal: base H + shear kinetic +(1/10)e^{-2phi}rho^2 a2'^2 + e^{+-s}-folded matter moments
  - phi off-round correction: +(1/(5Z)) e^{-2phi} a2'^2  (K = 1/5 pin, shared with the H shear kinetic)

TOPOLOGY (binding): this is the pi_2 axisymmetric S^2 winding tile -- it CANNOT bank Outcome A/B for the
pi_3 hopfion question (an open premise for Charles).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import inspect
import numpy as np
import torch
import pytest

torch.set_default_dtype(torch.float64)

import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)          # (Z, XI, KAP, N)  -- N=1 (rigid-hedgehog reference)


# ---- 1. ROUND-LIMIT RECOVERY: at a2=0 (s=0) every base row equals the current base residual ----------
@pytest.mark.parametrize("sealbc", ["off", "S-Dir", "S-JC2"])
def test_1_roundlimit_base_rows_match_base(sealbc):
    """The off-round f-PDE + off-round Hseal reduce to the base rows at a2=0 (e^{+-s}->1, sh_r=sh_th=0)."""
    ctx = C.make_ctx(8, 8, rc=0.5)
    Fb = C.residual(C.seed(ctx), ctx, PRM)
    base_len = Fb.numel()
    un = C.seed_n5d(ctx, a2_amp=0.0)                              # a2=0, identical base fields to seed()
    Fn = C.residual(un, ctx, PRM, n5d=dict(sealbc=sealbc, a2_mirror=0.0))
    assert Fn.numel() == un.numel(), "Stage-2 residual not square"
    err = float((Fn[:base_len] - Fb).abs().max())
    assert err < 1e-13, f"sealbc={sealbc}: base rows perturbed at a2=0 by {err:.2e}"


# ---- 2. PHI-BLINDNESS: the matter f-PDE, matter moments, and T_s are unchanged under a phi shift -----
def test_2_matter_is_phi_blind():
    """L_m has NO phi (only rho, s, f): shifting phi at fixed rho,f,a2 leaves res_f, T_s and the matter
    moments (off-round Ith_es/Is_es/I4r_es AND round Ir/I4th) unchanged; only geometric pieces move."""
    ctx = C.make_ctx(8, 8, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=2e-3)
    phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=True)
    n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    Q0 = C.fields(u, ctx, PRM, n5d=n5d)
    Q1 = C.fields(C.pack(phi - 0.63, rho, uf, float(L), a2=a2), ctx, PRM, n5d=n5d)
    for key in ("res_f", "Ts", "Tshear_live", "Ith_es", "Is_es", "I4r_es", "Ir", "I4th"):
        assert torch.allclose(Q0[key], Q1[key], atol=1e-14), f"matter piece {key} depends on phi -> NOT phi-blind"
    assert float(Q0["Ts"].abs().max()) > 1e-6, "T_s ~ 0 -> phi-blindness check would be vacuous"
    assert not torch.allclose(Q0["phi_ode"], Q1["phi_ode"], atol=1e-9), "geometric phi-ODE must move with phi"


# ---- 3. SELF-STRESS CONVENTION: the coded source is -(rho^2/4) T_s, NOT the naive +(rho^2/2) T_s -----
def test_3_self_stress_lambda_minus_half():
    """The implemented shear source equals lambda*(rho^2/2)*T_s with lambda=-1/2 (Gate-0.5), i.e.
    -(rho^2/4) T_s -- verified against an INDEPENDENT recomputation of T_s, and DISTINCT from +(rho^2/2)T_s."""
    Z, XI, KAP, N = PRM
    ctx = C.make_ctx(8, 8, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=3e-3)
    phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=True)
    Q = C.fields(u, ctx, PRM, n5d=dict(sealbc="S-Dir", a2_mirror=0.0))
    rho2 = rho[:, None] ** 2

    # independent recomputation of T_s from the primitive fields (guards the coded T_s formula + its sign)
    sc = 2.0 / float(L)
    f = ctx["th"][None, :] + uf
    fr = sc * (ctx["Dz"] @ uf)
    fth = 1.0 + uf @ ctx["DthT"]
    sf2 = torch.sin(f) ** 2
    s2 = (1.0 - ctx["mu"] ** 2)[None, :]
    sh = a2[:, None] * ctx["P2"][None, :]
    e_sp = torch.exp(sh); e_sm = torch.exp(-sh)
    Ts_ind = ((XI / rho[:, None] ** 2) * (N ** 2 * e_sp * sf2 / s2 - fth ** 2 * e_sm)
              + (KAP * N ** 2 / rho[:, None] ** 2) * fr ** 2 * e_sp * sf2 / s2)
    assert torch.allclose(Q["Ts"], Ts_ind, atol=1e-13), "coded T_s != independent recomputation"

    # the coded residual source carries lambda=-1/2: Tshear_live == -(rho^2/4) T_s
    assert torch.allclose(Q["Tshear_live"], -0.25 * rho2 * Q["Ts"], atol=1e-14), "source != -(rho^2/4) T_s"
    # ... and is genuinely DIFFERENT from the naive Hilbert +(rho^2/2) T_s (2x magnitude + opposite sign)
    naive = 0.5 * rho2 * Q["Ts"]
    assert float((Q["Tshear_live"] - naive).abs().max()) > 1e-6, "source coincides with the naive +(rho^2/2)T_s"


# ---- 4. RIGID HEDGEHOG: the L2 shear source (and the whole live source) vanishes at s=0, f=theta, N=1 -
def test_4_rigid_hedgehog_zero_source():
    """At a2=0 AND u=0 (f=theta, N=1) the rigid hedgehog carries NO shear: T_s = 0, Tshear_live = 0, and
    the projected shear row = 0.  (T_s(L2)=xi(1-f_th^2)/rho^2 = 0 at f_th=1; T_s(L4)=0 at f_r=0.)"""
    ctx = C.make_ctx(8, 8, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=0.0, amp=0.0)                     # a2=0 AND u=0
    Q = C.fields(u, ctx, PRM, n5d=dict(sealbc="S-Dir", a2_mirror=0.0))
    assert float(Q["Ts"].abs().max()) < 1e-12, f"rigid hedgehog T_s != 0: {float(Q['Ts'].abs().max()):.2e}"
    assert float(Q["Tshear_live"].abs().max()) < 1e-12, "rigid Tshear_live != 0"
    assert float(Q["shear_res"].abs().max()) < 1e-12, "rigid projected shear row != 0"


# ---- 5. NO FLAT-SOURCE DEPENDENCE: the residual never reads stress_profiles.npz / source_interp --------
def test_5_residual_independent_of_frozen_npz(monkeypatch):
    """The Stage-2 residual sources the shear from the LIVE matter only.  Disabling BOTH the frozen-source
    interpolator (n5d_shear.source_interp) AND np.load must leave the residual byte-for-byte unchanged --
    proving the frozen sh2(r)/npz is out of the residual path (kept only as an optional seed)."""
    ctx = C.make_ctx(8, 8, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=2e-3)
    n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    F0 = C.residual(u, ctx, PRM, n5d=n5d)

    def _boom(*a, **k):
        raise RuntimeError("frozen source must NOT be in the Stage-2 residual path")

    monkeypatch.setattr(C.n5d_shear, "source_interp", _boom)
    monkeypatch.setattr(np, "load", _boom)
    F1 = C.residual(u, ctx, PRM, n5d=n5d)
    assert torch.equal(F0, F1), "residual changed when the frozen-source loaders were disabled"


# ---- 6. HSEAL ROUND LIMIT: the off-round H reduces to the base H at a2=0 -------------------------------
def test_6_hseal_round_limit():
    """H_of_r(n5d) at a2=0 (e^{+-s}->1, a2'=0 -> no shear kinetic) equals the base H_of_r(n5d=None)."""
    ctx = C.make_ctx(8, 8, rc=0.5)
    Hbase = C.H_of_r(C.seed(ctx), ctx, PRM)                      # base H (n5d=None)
    un = C.seed_n5d(ctx, a2_amp=0.0)                             # a2=0, identical base fields
    Hoff = C.H_of_r(un, ctx, PRM, n5d=dict(sealbc="S-Dir", a2_mirror=0.0))
    err = float((Hoff - Hbase).abs().max())
    assert err < 1e-13, f"off-round Hseal != base H at a2=0: {err:.2e}"


# ---- 7. K PIN: the H shear kinetic +(1/10)e^{-2phi}rho^2 a2'^2 shares K=1/5 with the phi correction -----
def test_7_K_pin_shear_kinetic_matches_phi_correction():
    """Coefficient pin: 2*SHEAR_KIN_COEFF == K == Z*(phi-correction coeff 1/(5Z)) = 1/5.  PLUS a numeric
    extraction: at an interior node where a2=0 the matter moments equal the base (e^{+-s}=1 there), so
    H_off - H_base isolates the shear kinetic +(1/10)e^{-2phi}rho^2 a2'^2 -- confirming the coded coefficient."""
    Z, XI, KAP, N = PRM
    # (a) coefficient-level pin: both the H shear kinetic and the certified phi-correction encode K = 1/5
    c_phi = float(C.n5d_shear.phi_source_offround_correction(
        torch.tensor([1.0]), torch.tensor([1.0]), torch.tensor([1.0]), Z))    # = 1/(5Z)
    assert abs(Z * c_phi - 1.0 / 5.0) < 1e-14, "phi-correction coeff != 1/(5Z)"
    assert abs(2.0 * C.SHEAR_KIN_COEFF - 1.0 / 5.0) < 1e-14, "H shear-kinetic coeff != K/2 with K=1/5"
    assert abs(2.0 * C.SHEAR_KIN_COEFF - Z * c_phi) < 1e-14, "H shear kinetic and phi correction do not share K"

    # (b) numeric extraction at a node where a2=0 (moments = base there; only the shear kinetic survives)
    ctx = C.make_ctx(10, 8, rc=0.5)
    k = 4                                                        # an interior radial node
    zeta = ctx["zeta"]
    phi0, rho0, uf0, L0 = C.unpack(C.seed(ctx), ctx)
    cc = 0.3
    a2 = cc * (zeta - zeta[k])                                   # a2[k]=0 exactly; a2'(k) = cc*(2/L) (spectral exact)
    Hoff = C.H_of_r(C.pack(phi0, rho0, uf0, float(L0), a2=a2), ctx, PRM,
                    n5d=dict(sealbc="S-Dir", a2_mirror=0.0))
    Hbase = C.H_of_r(C.pack(phi0, rho0, uf0, float(L0)), ctx, PRM)   # same phi,rho,f; n5d=None
    a2p_k = float(((2.0 / float(L0)) * (ctx["Dz"] @ a2))[k])
    expect = C.SHEAR_KIN_COEFF * float(torch.exp(-2.0 * phi0[k])) * float(rho0[k]) ** 2 * a2p_k ** 2
    got = float(Hoff[k] - Hbase[k])
    assert abs(got - expect) < 1e-10, f"H shear-kinetic at a2=0 node: got {got:.3e} expect {expect:.3e}"


# ---- 8. PREFLIGHT: square residual, finite Jacobian, bounded grid, FIX-1 on, hard cap (NO pilot solve) -
@pytest.mark.parametrize("sealbc", ["S-Dir", "S-JC2"])
def test_8_preflight_assembly_and_conditioning(sealbc):
    """ASSEMBLY-ONLY: the coupled Stage-2 residual is SQUARE with a finite, nonsingular Jacobian on a
    BOUNDED grid (Nr<=24 anti-hang).  No solve is run here."""
    ctx = C.make_ctx(12, 8, rc=0.5)                             # bounded (Nr=12 <= 24)
    n5d = dict(sealbc=sealbc, a2_mirror=0.0)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    F = C.residual(u, ctx, PRM, n5d=n5d)
    assert u.numel() == F.numel(), "Stage-2 residual not square"
    assert bool(torch.isfinite(F).all()), "Stage-2 residual not finite"
    cond, smin, smax, nr_, nc_ = C.jac_condition(u, ctx, PRM, n5d=n5d)
    assert nr_ == nc_ and smin > 0.0, f"Jacobian singular/nonsquare: shape=({nr_},{nc_}) smin={smin}"
    assert np.isfinite(cond), "Jacobian condition number not finite"


def test_8_solver_fix1_on_and_iteration_capped():
    """FIX-1 equilibration defaults ON and the LM solve carries a hard (bounded) iteration cap (anti-hang)."""
    sig = inspect.signature(C.newton_lm_solve)
    assert sig.parameters["equilibrate"].default is True, "FIX-1 equilibration must default ON"
    assert sig.parameters["maxit"].default <= 30, "LM iteration cap must be bounded (anti-hang)"
