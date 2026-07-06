"""Pullback correctness (registration B) regression tests.
The frozen ell=2 source must be pulled back at the CURRENT physical cell coordinate r(zeta)=rc+(L/2)(zeta+1),
not frozen at the seed L0.  These pin: L=L0 reproduces the old registration; L!=L0 differs in the expected
way; P2 normalization stays 2/5; the source enters ONLY the shear row (no direct phi-source)."""
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
    build_Tshear raw array (both WITHOUT the rho^2/2 frame factor, which is applied separately in
    fields with access to the rho field -- see the frame-factor tests)."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)                             # vector carries L = L0 (seed L0=1.0)
    L_vec = float(C.unpack(u, ctx, n5d=True)[-1])
    live_r = ctx["rc"] + 0.5 * L_vec * (ctx["zeta"] + 1.0)
    live_src2 = C.n5d_shear.source_interp(SRC_RC, SRC_SH2, live_r)
    live_T = 1.0 * live_src2[:, None] * ctx["P2"][None, :]       # raw interp * P2 (no frame factor)
    standalone = P.build_Tshear(ctx, L_vec, 1.0, SRC_RC, SRC_SH2)
    assert torch.allclose(live_T, standalone, atol=1e-12, rtol=0.0)


def _source_projection(u, ctx, n5d_src, n5d_none):
    """The ell=2 projected source contribution = shear_res(with src) - shear_res(no src)."""
    Q1 = C.fields(u, ctx, PRM, n5d=n5d_src)
    Q0 = C.fields(u, ctx, PRM, n5d=n5d_none)
    return (Q1["shear_res"] - Q0["shear_res"])


def test_frame_factor_rho2_over_2_applied():
    """fields() applies the DERIVED rho^2/2 frame factor: the projected source contribution equals
    amp * (rho^2/2) * sh2(r) * sum_j w_j P2_j^2  (= (rho^2/2)*sh2*(2/5)), node by node."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=True)
    n5d_src = dict(sealbc="S-Dir", src=(SRC_RC, SRC_SH2, 1.0), a2_mirror=0.0)
    n5d_none = dict(sealbc="S-Dir", a2_mirror=0.0)
    got = _source_projection(u, ctx, n5d_src, n5d_none)
    r_phys = ctx["rc"] + 0.5 * float(L) * (ctx["zeta"] + 1.0)
    sh2 = C.n5d_shear.source_interp(SRC_RC, SRC_SH2, r_phys)
    wP2sq = float((ctx["w"] * ctx["P2"] ** 2).sum())            # = 2/5
    expect = (0.5 * rho ** 2) * sh2 * wP2sq                     # (rho^2/2)*sh2*(2/5)
    assert torch.allclose(got, expect, atol=1e-12, rtol=1e-10), float((got - expect).abs().max())


def test_frame_factor_scales_as_rho_squared():
    """Scaling rho -> 2*rho multiplies the projected source contribution by exactly 4 (rho^2)."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=True)
    n5d_none = dict(sealbc="S-Dir", a2_mirror=0.0)
    n5d_src = dict(sealbc="S-Dir", src=(SRC_RC, SRC_SH2, 1.0), a2_mirror=0.0)
    s1 = _source_projection(u, ctx, n5d_src, n5d_none)
    u2 = C.pack(phi, 2.0 * rho, uf, float(L), a2=a2)            # double rho
    # subtract the no-source shear_res at the SAME rho-scaled state (E_s_geom also changes with rho)
    n5d_none2 = dict(sealbc="S-Dir", a2_mirror=0.0)
    s2 = _source_projection(u2, ctx, n5d_src, n5d_none2)
    ratio = (s2 / s1)[s1.abs() > 1e-12]
    assert torch.allclose(ratio, 4.0 * torch.ones_like(ratio), atol=1e-8), float(ratio.mean())


def test_frame_factor_is_phi_blind():
    """The rho^2/2 factor is phi-BLIND: changing phi (not rho) leaves the projected source unchanged."""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    phi, rho, uf, a2, L = C.unpack(u, ctx, n5d=True)
    n5d_none = dict(sealbc="S-Dir", a2_mirror=0.0)
    n5d_src = dict(sealbc="S-Dir", src=(SRC_RC, SRC_SH2, 1.0), a2_mirror=0.0)
    s1 = _source_projection(u, ctx, n5d_src, n5d_none)
    u2 = C.pack(phi + 0.37, rho, uf, float(L), a2=a2)          # shift phi, keep rho
    s2 = _source_projection(u2, ctx, n5d_src, n5d_none)
    assert torch.allclose(s1, s2, atol=1e-12), "source depends on phi -> NOT phi-blind!"


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


def test_source_is_phi_blind_no_direct_phi_source():
    """The source enters ONLY the shear (h_AB) row: adding it must NOT change phi_ode / rho_ode / res_f;
    only shear_res changes.  (a2 is held fixed, so the phi off-round a2'^2 correction is unchanged too.)"""
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    n5d_no = dict(sealbc="S-Dir", a2_mirror=0.0)                              # vacuum shear (no source)
    n5d_src = dict(sealbc="S-Dir", src=(SRC_RC, SRC_SH2, 1.0), a2_mirror=0.0)  # with source
    Q0 = C.fields(u, ctx, PRM, n5d=n5d_no)
    Q1 = C.fields(u, ctx, PRM, n5d=n5d_src)
    assert torch.allclose(Q0["phi_ode"], Q1["phi_ode"], atol=1e-14), "source leaked into phi-ODE!"
    assert torch.allclose(Q0["rho_ode"], Q1["rho_ode"], atol=1e-14), "source leaked into rho-ODE!"
    assert torch.allclose(Q0["res_f"], Q1["res_f"], atol=1e-14), "source leaked into matter f-PDE!"
    assert not torch.allclose(Q0["shear_res"], Q1["shear_res"], atol=1e-8), "source did NOT reach shear row!"


def test_live_source_jacobian_finite_and_L_dependent():
    """The live source must be differentiable (jacrev works) and the residual's dependence on L must
    include the source (registration B: source moves with L)."""
    from torch.func import jacrev
    ctx = C.make_ctx(Nr, Nth, rc=0.5)
    u = C.seed_n5d(ctx, a2_amp=1e-3)
    n5d = dict(sealbc="S-Dir", src=(SRC_RC, SRC_SH2, 1.0), a2_mirror=0.0)
    J = jacrev(lambda uu: C.residual(uu, ctx, PRM, n5d=n5d))(u).detach()
    assert bool(torch.isfinite(J).all())
    # the shear rows must have a NONZERO derivative wrt L (last column) -> source tracks L
    shear_rows = slice(J.shape[0] - Nr, J.shape[0])
    dL_col = J[shear_rows, -1]
    assert float(dL_col.abs().max()) > 0.0, "shear rows do not depend on L -> source not tracking L (not B)"
