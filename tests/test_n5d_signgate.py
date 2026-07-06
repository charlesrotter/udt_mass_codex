"""N5d Gate-8 (sign-convention) -- INTERNAL consistency only (NOT sign-correctness; §5/§7).

On the round test case the three readouts must agree with the single pinned whole-cell convention:
  q_raw       = Z_phi rho_s^2 phi'(r_s)     (unambiguous raw seal flux)
  Pi_phi      = Z_phi q_raw                 (Gauss-budget form)
  sign_conv   = -1                          (pinned once from the N5b/N2 flux budget: M = -q)
  M_readout   = sign_conv * q_raw
A hidden sign flip anywhere would break one of these equalities and could otherwise fake a false
positive -- so Gate-8 BLOCKS if they disagree.  It judges PROVENANCE/HONESTY, never MERIT.
"""
import torch
import pytest

torch.set_default_dtype(torch.float64)

import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)          # Z=8


def _round_state(ctx, phi_slope=0.0):
    """A round (a2=0) state with a controllable phi'(r_s) so q_raw is nonzero and sign-testable."""
    Nr = ctx["Nr"]
    # a linear phi ramp gives a nonzero phi'(seal); rho constant, u=0
    zeta = ctx["zeta"]
    phi = phi_slope * (zeta - zeta[0])
    rho = torch.full((Nr,), 0.8, dtype=torch.float64)
    uf = torch.zeros(Nr, ctx["Nth"], dtype=torch.float64)
    a2 = torch.zeros(Nr, dtype=torch.float64)
    return C.pack(phi, rho, uf, 1.0, a2=a2)


@pytest.mark.parametrize("slope", [0.0, 0.7, -1.3])
def test_gate8_sign_convention_internal_consistency(slope):
    ctx = C.make_ctx(6, 6, rc=0.5)
    n5d = dict(sealbc="off")
    v = _round_state(ctx, phi_slope=slope)
    ro = C.readouts(v, ctx, PRM, n5d=n5d)
    Z = PRM[0]
    # 1. sign_convention is the pinned canon value
    assert ro["sign_convention"] == -1.0 == C.SIGN_CONVENTION
    # 2. Pi_phi == Z * q_raw  (Gauss-budget form)
    assert abs(ro["Pi_phi"] - Z * ro["q_raw"]) < 1e-12 * (1 + abs(ro["q_raw"]))
    # 3. M_readout == sign_convention * q_raw  (no hidden flip)
    assert abs(ro["M_readout"] - ro["sign_convention"] * ro["q_raw"]) < 1e-12 * (1 + abs(ro["q_raw"]))
    # 4. q_raw itself is Z rho_s^2 phi'(r_s) recomputed independently
    Q = C.fields(v, ctx, PRM, n5d=n5d)
    q_chk = float(Z * Q["rho"][-1] ** 2 * Q["phip"][-1])
    assert abs(ro["q_raw"] - q_chk) < 1e-12 * (1 + abs(q_chk))


def test_gate8_readouts_finite_and_reported():
    """All three readouts compute (finite) and are reported together -- so no hidden sign flip can
    manufacture a false positive by reporting only one."""
    ctx = C.make_ctx(6, 6, rc=0.5)
    ro = C.readouts(_round_state(ctx, 0.5), ctx, PRM, n5d=dict(sealbc="off"))
    for k in ("q_raw", "Pi_phi", "sign_convention", "M_readout"):
        assert k in ro and abs(ro[k]) < float("inf")
