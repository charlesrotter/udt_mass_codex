"""P2 -- OPERATOR FROM THE ACTION (SOLVER_INTEGRITY_UPGRADES_SPEC P2, GR-baseline scope).

Asserts the LIVE operator IS the Euler-Lagrange content of the single source-of-truth action
in `solver_action.py` (the a=-1 GR-baseline: S = integral sqrt(-g)[(1/2kap8)R + L2 + L4]).
Goal (spec): minimize hand-coded operator pieces; prove generated == EL of the action to
machine precision, so an import can't hide in a hand-written operator term.

SCOPE (Charles 2026-06-23): GR-baseline only. The DERIVED e^{2phi}/a(phi) theory + the curvature
Branch G/P fork + the untraced matter weight are MIGRATION-DEFERRED (tripwired by the P1 xfails +
solver_action.ACTION_TERMS migration_notes). Do NOT wire them here to pass a test.

Anti-hang: forward evals only, small bounded grids, <1s.
"""
import torch
import pytest

torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric, einstein_mixed_weyl,
                             field_dn, matter_el_3d, matter_el_autograd, T, R, TH, PS)
import whole_metric_3d_matter as MAT
from einstein_3d_general_eval import einstein_mixed_general
from full3d_newton import inv4x4, det4x4
from p1_residual_general_einstein import residual_vector_p1, einstein_general_hybrid, pack8
import solver_action as ACT

VALID_TAGS = {"DERIVED", "FREE", "IMPORTED", "MIGRATION-DEFERRED"}


def _grid(Nr=12, Nth=8, Nps=8, rc=0.1, cell=2.0):
    return attach_coord_weight(Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=rc, cell=cell))


def _smooth(G, amp):
    return amp * (torch.cos(G.THg) * 0.3 + torch.sin(2 * G.PSg) * 0.2
                  + torch.exp(-((G.Rg - 1.0)) ** 2))


# =============================================================================
# 1. MATTER STRESS == the exact Hilbert variation of the matter action
#    T_{mu nu} = -2 d L_m / d g^{mu nu} + g_{mu nu} L_m   (no metric-derivative coupling).
#    The hand-coded stress_tensor must equal the autograd variation of the SAME L_m.
# =============================================================================
def test_matter_stress_is_action_variation():
    G = _grid()
    a, b, c, d = _smooth(G, 0.05), _smooth(G, 0.04), _smooth(G, 0.03), _smooth(G, 0.02)
    Th = 0.6 * torch.exp(-(G.Rg - 0.1)) * (1.0 + 0.1 * torch.cos(G.THg))
    g = build_metric(G, a, b, c, d)
    ginv = inv4x4(g)
    dn = field_dn(G, Th, m=1)

    # hand-coded operator (via the action file's hook)
    Tab_hand, _, _, _ = ACT.matter_stress(g, ginv, dn, xi=1.0, kap=1.0)

    # autograd the action density L_m w.r.t. the (inverse) metric -> Hilbert stress
    gi = ginv.detach().clone().requires_grad_(True)
    Gmn = MAT.field_metric(dn.detach())
    L, _, _, _ = ACT.matter_lagrangian(gi, Gmn, 1.0, 1.0)
    (dL_dgi,) = torch.autograd.grad(L.sum(), gi)
    Tab_auto = -2.0 * dL_dgi + g.detach() * L.detach()[..., None, None]

    err = float((Tab_hand - Tab_auto)[G.body].abs().max())
    assert err < 1e-12, f"matter stress != EL of the action: max|diff|(body) = {err:.2e}"


# =============================================================================
# 2. GRAVITY operator == the EL of sqrt(-g) R (the Einstein tensor G^mu_nu).
#    Two INDEPENDENTLY-generated analytic engines (general-sheared vs diagonal-Weyl) must
#    agree to machine precision on a smooth diagonal metric -> no hand-coding drift.
#    (Correctness vs exact solutions is anchored by P1: de Sitter G=-Lam, Schwarzschild G=0.)
# =============================================================================
def test_gravity_engines_agree():
    G = _grid(Nr=20, Nth=10, Nps=8, rc=0.3, cell=1.4)
    a, b, c, d = _smooth(G, 0.05), _smooth(G, 0.04), _smooth(G, 0.03), _smooth(G, 0.02)
    G_general = ACT.gravity_operator_general(G, dict(a=a, b=b, c=c, d=d))
    G_weyl = einstein_mixed_weyl(G, a, b, c, d)
    err = float((G_general - G_weyl)[G.body].abs().max())
    scale = float(G_weyl[G.body].abs().max())
    assert err < 1e-10, f"two gravity engines disagree (drift): max|diff|={err:.2e} (scale {scale:.2e})"


# =============================================================================
# 2b. MATTER FIELD-EOM (Theta equation) is consistent with the action.
#    The strong-form analytic EL (matter_el_3d, sympy codegen) must agree with the WEAK-form
#    autograd variation of the SAME action (-matter_el_autograd; note the sign convention) --
#    two INDEPENDENT routes to delta S / delta Theta.  They converge with resolution (same
#    continuum operator) and a codegen-class bug (e.g. the historical L4 bug) breaks them by
#    O(1).  CONSISTENCY check (~bulk 0.4%, converging), NOT a machine-precision proof: the two
#    are strong- vs weak-form discretizations, so pole-theta nodes (1/sin^2 structure) and the
#    coordinate edges are excluded.
# =============================================================================
def test_matter_field_eom_consistent_with_action():
    G = _grid(Nr=20, Nth=12, Nps=8, rc=0.3, cell=1.4)
    a, b, c, d = _smooth(G, 0.05), _smooth(G, 0.04), _smooth(G, 0.03), _smooth(G, 0.02)
    Th = 0.5 + 0.3 * torch.cos(G.THg) * torch.exp(-((G.Rg - 1.0)) ** 2)
    g = build_metric(G, a, b, c, d)
    ginv = inv4x4(g)
    el_strong = matter_el_3d(G, a, b, c, d, Th, m=1)          # analytic sympy codegen
    el_weak = matter_el_autograd(G, g, ginv, Th, m=1)         # autograd of the action
    bulk = torch.zeros_like(G.body)
    bulk[5:G.Nr - 5, 2:G.Nth - 2, :] = True                   # exclude coord edges + pole-theta
    rel = float((el_strong + el_weak)[bulk].abs().max() / (el_strong[bulk].abs().max() + 1e-30))
    assert rel < 2e-2, f"matter field-EOM (strong) != -autograd(action) (weak): bulk rel = {rel:.2e}"


# =============================================================================
# 3. REGRESSION LOCK on the field-equation ASSEMBLY (NOT an independent EL proof).
#    The field-equation rows of residual_vector_p1 must equal (W * (G - kap8 T))[body]
#    recomputed with the SAME engine -> locks the assembly RECIPE (the W weighting, the
#    kap8 sign/order, the component list, G - kap8 T not G - 2 kap8 T).  Tautological as an
#    EL proof (same engine on both sides); valuable as a drift/regression guard.
# =============================================================================
def test_residual_assembles_einstein_eq():
    G = _grid()
    a, b, c, d = _smooth(G, 0.05), _smooth(G, 0.04), _smooth(G, 0.03), _smooth(G, 0.02)
    Th = 0.6 * torch.exp(-(G.Rg - 0.1)) * (1.0 + 0.1 * torch.cos(G.THg))
    z = torch.zeros_like(a)
    u = pack8(a, b, c, d, Th, z, z, z)
    p, kap8 = 0.4, 0.05

    F = residual_vector_p1(u, G, p, kap8)

    # independent reconstruction of the field-equation rows (same engine + weight)
    Gmix, g = einstein_general_hybrid(G, a, b, c, d, z, z, z)
    ginv = inv4x4(g)
    dn = field_dn(G, Th, m=1)
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    Tmix = torch.einsum("...ma,...an->...mn", ginv, Tab)
    resE = Gmix - kap8 * Tmix                         # <-- the action's EOM: G - kap8 T
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg * G.wvol_coord)
    W = W / W[G.body].mean()

    nbody = int(G.body.sum())
    comps = [(T, T), (R, R), (TH, TH), (PS, PS), (R, TH), (R, PS), (TH, PS)]
    for i, (mm, nn) in enumerate(comps):
        expected = (W * resE[..., mm, nn])[G.body]
        got = F[i * nbody:(i + 1) * nbody]
        err = float((expected - got).abs().max())
        assert err < 1e-12, f"residual field-row {(mm, nn)} != (W*(G-kap8 T)): {err:.2e}"


# =============================================================================
# 4. PROVENANCE of the action source: every term tagged; deferred terms not wired; the
#    untraced matter weight is flagged (not silently present).
# =============================================================================
def test_action_terms_tagged():
    for t in ACT.ACTION_TERMS:
        assert t["tag"] in VALID_TAGS, f"{t['name']}: bad/absent provenance tag {t['tag']!r}"
        assert t.get("evidence"), f"{t['name']}: missing provenance evidence"
        # MIGRATION-DEFERRED terms must NOT be wired into the live operator
        if t["tag"] == "MIGRATION-DEFERRED":
            assert t["operator"] is None, f"{t['name']}: deferred term is wired into the operator!"


def test_matter_weight_is_flagged_not_used():
    """The spec's e^{2phi} matter weight is a flagged CHOSE/posit for field matter (P4 cross-model
    verified, PARTIALLY-TRACED) -- it must be recorded as a deferred, flagged not-derived term, and
    must NOT be in the live matter operator."""
    mw = ACT.term("matter_weight")
    assert mw["tag"] == "MIGRATION-DEFERRED"
    assert "CHOSE" in mw["evidence"]          # flagged as a posit, NOT derived for field matter
    assert mw["operator"] is None


def test_baseline_terms_are_traced():
    """Every term the GR-baseline operator ACTUALLY uses (operator != None) must be traced
    (DERIVED or FREE) -- no UNTRACED/IMPORTED term silently live."""
    for t in ACT.ACTION_TERMS:
        if t["operator"] is not None:
            assert t["tag"] in {"DERIVED", "FREE"}, \
                f"{t['name']} is LIVE but tagged {t['tag']} -- untraced term in the operator"
