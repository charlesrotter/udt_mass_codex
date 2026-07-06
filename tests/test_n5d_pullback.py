"""Pullback / registration-B tests for the FROZEN ell=2 source HELPER (n5d_pilot.build_Tshear +
n5d_shear.source_interp).

STAGE-2 SCOPE (2026-07-06): the frozen sh2(r) profile / stress_profiles.npz is RETIRED from the residual
path -- the Stage-2 residual sources the shear from the LIVE co-relaxed matter's own traceless stress
(-(rho^2/4) T_s, see test_n5d_stage2.py), NOT from an imported flat-hopfion profile.  The build_Tshear /
source_interp helpers REMAIN importable as an OPTIONAL initial-guess SEED / diagnostic (Charles 2026-07-06),
so these tests pin the helper's registration-B correctness as a STANDALONE array builder -- they no longer
couple it to the residual (the src-in-residual + rho^2/2-frame-factor tests were removed with the Stage-1
frozen-source residual path).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import pytest

import cell_solver_f2d as C
import n5d_pilot as P

PRM = P.PRM
Nr, Nth = 12, 8
L0 = 1.0

# a compact synthetic sh2(r) profile (monotone-ish, nonzero on the cell) -- avoids needing the npz
SRC_RC = np.linspace(0.05, 6.0, 64)
SRC_SH2 = np.sin(SRC_RC) * np.exp(-0.3 * SRC_RC) * 10.0


def _old_registration(ctx, L_reg, amp):
    """The ORIGINAL build_Tshear semantics (np.interp at r=rc+(L_reg/2)(zeta+1)), for the old==new check."""
    zeta = ctx["zeta"].cpu().numpy()
    r_phys = ctx["rc"] + 0.5 * L_reg * (zeta + 1.0)
    src2 = np.interp(r_phys, SRC_RC, SRC_SH2, left=0.0, right=0.0)
    src2_t = torch.as_tensor(src2, dtype=torch.float64)
    return amp * src2_t[:, None] * ctx["P2"][None, :]


def test_pullback_L_equals_L0_reproduces_old():
    """At L=L0 the new registration reproduces the OLD frozen-at-L0 source to numerical precision."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    new = P.build_Tshear(ctx, L0, 1.0, SRC_RC, SRC_SH2)          # registration B, evaluated at L=L0
    old = _old_registration(ctx, L0, 1.0)                        # old frozen-at-L0
    assert torch.allclose(new, old, atol=1e-12, rtol=0.0), float((new - old).abs().max())


def test_pullback_interp_matches_standalone_at_L0():
    """The registration-B INTERPOLATION (sh2 at current-L physical r) matches the standalone
    build_Tshear raw array (raw interp * P2, no frame factor -- the helper is a pure array builder)."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)                             # vector carries L = L0 (seed L0=1.0)
    L_vec = float(C.unpack(u, ctx, n5d=True)[-1])
    live_r = ctx["rc"] + 0.5 * L_vec * (ctx["zeta"] + 1.0)
    live_src2 = C.n5d_shear.source_interp(SRC_RC, SRC_SH2, live_r)
    live_T = 1.0 * live_src2[:, None] * ctx["P2"][None, :]       # raw interp * P2 (no frame factor)
    standalone = P.build_Tshear(ctx, L_vec, 1.0, SRC_RC, SRC_SH2)
    assert torch.allclose(live_T, standalone, atol=1e-12, rtol=0.0)


@pytest.mark.parametrize("L1", [0.3, 0.1, 3.0])
def test_pullback_L_ne_L0_differs_expectedly(L1):
    """For L != L0 the source is interpolated at DIFFERENT physical r -> the array differs, and it equals
    the source sampled at r=rc+(L1/2)(zeta+1) (NOT the fixed-zeta-profile from L0)."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    atL1 = P.build_Tshear(ctx, L1, 1.0, SRC_RC, SRC_SH2)
    atL0 = P.build_Tshear(ctx, L0, 1.0, SRC_RC, SRC_SH2)
    assert not torch.allclose(atL1, atL0, atol=1e-8), "L!=L0 must change the source (not a fixed zeta-profile)"
    # and it must equal the source evaluated at the L1 physical nodes (registration B definition)
    expect = _old_registration(ctx, L1, 1.0)                    # old-style eval but at L1 = the B target
    assert torch.allclose(atL1, expect, atol=1e-12, rtol=0.0)


def test_P2_quadrature_norm_still_two_fifths():
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    val = float((ctx["w"] * ctx["P2"] ** 2).sum())
    assert abs(val - 0.4) < 1e-12, val
    assert abs(float((ctx["w"] * ctx["P2"]).sum())) < 1e-12          # orthogonal to P0


def test_frozen_source_is_NOT_in_the_residual():
    """STAGE-2 provenance guard: passing a frozen Tshear/src in the n5d dict must NOT change the residual
    (the frozen-source residual path is retired; the live T_s source is the ONLY matter source)."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    Nr_, Nth_ = ctx["Nr"], ctx["Nth"]
    bogus = 0.05 * ctx["P2"][None, :].repeat(Nr_, 1)            # a nonzero (Nr,Nth) P2 array
    F_plain = C.residual(u, ctx, PRM, n5d=dict(sealbc="S-Dir", a2_mirror=0.0))
    F_Tshear = C.residual(u, ctx, PRM, n5d=dict(sealbc="S-Dir", a2_mirror=0.0, Tshear=bogus))
    F_src = C.residual(u, ctx, PRM, n5d=dict(sealbc="S-Dir", a2_mirror=0.0, src=(SRC_RC, SRC_SH2, 1.0)))
    assert torch.allclose(F_plain, F_Tshear, atol=1e-14), "frozen Tshear leaked into the residual (Stage-2 retired it)"
    assert torch.allclose(F_plain, F_src, atol=1e-14), "frozen src leaked into the residual (Stage-2 retired it)"
