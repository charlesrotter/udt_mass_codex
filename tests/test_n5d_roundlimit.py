"""N5d round-limit recovery: with the shear amplitude a2==0 the N5d extension is byte-for-byte the
base cell_solver_f2d round-trace system, and the base bounded smoke (assemble + one LM step decreases
Phi) is unchanged.  This is the ADDITIVITY gate (a frozen shear DOF must NOT perturb the base rows).

Anti-hang: forward residual evals + at most ONE LM step, bounded Nr,Nth<=8, single process, <5s.
"""
import torch
import pytest

torch.set_default_dtype(torch.float64)

import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)          # (Z, XI, KAP, N)  -- the base smoke parameters


@pytest.mark.parametrize("sealbc", ["off", "S-Dir", "S-JC2"])
def test_roundlimit_base_rows_identical(sealbc):
    """With a2==0 the N5d residual's base block == the base residual to machine precision, for every
    shear seal BC (the off-round phi-source correction ~ a2'^2 vanishes; the base rows keep position)."""
    ctx = C.make_ctx(6, 6, rc=0.5)
    n5d = dict(sealbc=sealbc)
    ub = C.seed(ctx)                              # base state
    un = C.seed_n5d(ctx, a2_amp=0.0)             # base state + a2==0
    Fb = C.residual(ub, ctx, PRM, wbc=1.0)
    Fn = C.residual(un, ctx, PRM, wbc=1.0, n5d=n5d)
    assert Fn.numel() == un.numel(), "N5d system not square"
    base_len = Fb.numel()
    err = float((Fn[:base_len] - Fb).abs().max())
    assert err < 1e-14, f"base rows perturbed by frozen shear (sealbc={sealbc}): max|diff|={err:.2e}"


def test_roundlimit_shear_rows_vanish_at_rigid_hedgehog():
    """STAGE-2: with a2==0 AND rigid matter (u=0, f=theta, N=1) the appended shear rows are identically 0
    -- both the geometric E-row (s=0) AND the live matter source T_s (rigid hedgehog carries no shear).

    NOTE (Stage-2 co-relaxation): at a2==0 with NON-rigid matter (u!=0) the shear rows are NOT zero -- the
    live matter's own P2-projected traceless stress SOURCES the shear (that is the whole point of Stage-2;
    the frozen-vacuum 'shear rows vanish at a2=0' statement was Stage-1 only).  So the round null requires
    rigid matter too."""
    ctx = C.make_ctx(6, 6, rc=0.5)
    ub = C.seed(ctx); base_len = C.residual(ub, ctx, PRM).numel()
    for sealbc in ("S-Dir", "S-JC2", "off"):
        un = C.seed_n5d(ctx, a2_amp=0.0, amp=0.0)         # a2=0 AND u=0 (rigid hedgehog)
        Fn = C.residual(un, ctx, PRM, n5d=dict(sealbc=sealbc))
        shear_block = Fn[base_len:]
        assert float(shear_block.abs().max()) < 1e-13, \
            f"shear rows nonzero at rigid a2=u=0 (sealbc={sealbc}): {float(shear_block.abs().max()):.2e}"


def test_base_smoke_one_lm_step_decreases():
    """The base bounded smoke is unchanged by the extension: residual assembles, Jacobian finite,
    ONE LM step decreases Phi (Nr=Nth=6, single foreground process)."""
    ctx = C.make_ctx(6, 6, rc=0.5)
    u0 = C.seed(ctx)
    F0 = C.residual(u0, ctx, PRM)
    assert u0.numel() == F0.numel() and bool(torch.isfinite(F0).all())
    u1, hist = C.newton_lm_solve(u0, ctx, PRM, maxit=1, verbose=False, time_budget=30.0)
    assert len(hist) >= 2 and hist[1] < hist[0], f"one LM step did not decrease Phi: {hist[:2]}"


def test_n5d_assembles_and_is_finite():
    """The coupled N5d residual + shear BCs ASSEMBLE square with a finite Jacobian (assembly only;
    NO pilot solve)."""
    ctx = C.make_ctx(6, 6, rc=0.5)
    n5d = dict(sealbc="S-JC2")
    u = C.seed_n5d(ctx, a2_amp=1e-3)             # nonzero shear so the shear rows are exercised
    F = C.residual(u, ctx, PRM, n5d=n5d)
    assert u.numel() == F.numel() and bool(torch.isfinite(F).all())
    cond, smin, smax, nr_, nc_ = C.jac_condition(u, ctx, PRM, n5d=n5d)
    assert nr_ == nc_ and smin > 0.0, f"N5d Jacobian singular/nonsquare: shape=({nr_},{nc_}) smin={smin}"
