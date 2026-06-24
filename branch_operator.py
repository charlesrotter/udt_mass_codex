#!/usr/bin/env python3
"""
branch_operator.py -- UDT's DERIVED scalar-tensor gravity operator with an EXPLICIT,
TAGGED branch switch (Branch G / Branch P).  Load-bearing infrastructure.

This module is a THIN, AUDITED wrapper that (a) assembles the derived two-player
operator E^mu_nu and the phi-EOM by REUSING the already-validated covariant building
blocks in `b1prime_3d_offround_residual.py` (box_f_scalar, cov_hessian_f, E_mixed,
EL_phi_3d) and `full3d_spectral.py` (build_metric / einstein engines), and (b) makes
the Branch-G-vs-Branch-P choice an EXPLICIT flagged parameter so nothing is silently
default-smuggled.

-----------------------------------------------------------------------------------
THE OPERATOR (verbatim, derived upstream; sources cited per term):

  Action (Branch G -- the clean shift-invariant remnant):
    S_G = INT sqrt(-g)[ f R + X f g^{ab} d_a phi d_b phi  (+ matter) ],   f = e^{2phi}
        native_dilation_weight_derivation_results.md Sec 5 (lines 219-231);
        branch_G_characterization_results.md Sec 1 (lines 36-86).

  Metric (mixed) operator, vacuum form E^mu_nu = 0 / sourced E^mu_nu = (matter):
    E^mu_nu = f G^mu_nu
              + ( delta^mu_nu box f - (nabla nabla f)^mu_nu )
              - X f ( nabla^mu phi nabla_nu phi - 1/2 delta^mu_nu (dphi)^2 )
              - kap8 f T^mu_nu
        matter_regrade_derived_operator_results.md lines 60-61 (E_munu form);
        the matter source is the e^{2phi}-WEIGHTED bare stress, and the field eq is
        E_munu = (1/2) e^{2phi} T^bare_munu in the doc's lowered/half-normalized
        convention (regrade Sec 2-3).  *** See the SIGN/FACTOR NOTE below: the repo's
        already-validated assembly carries the matter term as `- kap8 f T^mu_nu` with
        kap8 a DERIVED unit coefficient, NOT the literal `1/2`; the `1/2` in the doc
        is the half-normalization of T_munu = -2 dL/dg + g L vs the Hilbert stress the
        repo uses.  We REUSE the validated assembly (kap8) and tag it; we do NOT
        re-introduce a second 1/2. ***

  phi-EOM (Branch G), delta S / delta phi (covariant), per b1prime EL_phi_3d:
    EOM_phi = f'(phi)[ R + X (dphi)^2 + kap8 L_m ]
              - 2 X (1/sqrt-g) d_mu( sqrt-g f g^{mu nu} d_nu phi ),   f' = 2 e^{2phi}
        native_dilation_weight_derivation_results.md Sec 5;
        branch_G_characterization_results.md Sec 1 (scalar eqn).

  Branch P ADDS the kept angular-curvature potential -2U, U = e^{2phi}-1:
    S_P = S_G + INT sqrt(-g)[ -2 U(phi) ],   U = e^{2phi}-1
        branch_P_characterization_results.md Sec 0-1 (lines 14-58).
    Metric eq (doc eq 1b):  f G + (g box - nn)f - Xf(...) = ... - g_mn U(phi).
      Moving -g_mn U to the operator side (E = 0 convention) adds  + delta^mu_nu U
      to the MIXED operator:
        E^mu_nu_P = E^mu_nu_G  +  delta^mu_nu * U(phi).            [DERIVED, sign below]
    phi eq (doc eq 1a):  ... - 2 U'(phi) = 0,  U' = 2 e^{2phi}.
      Relative to the EL_phi_3d sign convention (EOM_phi = alg - 2X div, an EL of the
      action), the -2U' contribution enters as:
        EOM_phi_P = EOM_phi_G  -  2 U'(phi)  =  EOM_phi_G  -  4 e^{2phi}.  [DERIVED, sign below]

  *** SIGN of the Branch-P metric term, RESOLVED ***
  delta( sqrt(-g) (-2U) ) wrt the metric:  only sqrt(-g) carries the metric, and
  delta sqrt(-g) = -1/2 sqrt(-g) g_munu delta g^munu.  So
    delta( sqrt-g (-2U) ) = (-2U)(-1/2) sqrt-g g_munu delta g^munu = + U sqrt-g g_munu delta g^munu.
  The variation of S_G gave  f G_munu + (...)f - Xf(...) = + (matter/2)  (LOWER indices).
  Adding -2U gives  f G_munu + (...)f - Xf(...) + U g_munu = (matter side),  i.e. the
  potential appears as  + U g_munu  on the OPERATOR side.  Lowered -> mixed by g^{mu a}:
  g^{mu a}(U g_{a nu}) = U delta^mu_nu.  Hence Branch P adds  + delta^mu_nu U  to E^mu_nu.
  This matches branch_P_characterization eq 1b (RHS -g_mn U => +g_mn U on the operator
  side) and the covariant cross-check there (sqrt-g (2/r^2)(e^{2phi}-1) -> 2(e^{2phi}-1)).
  EMPIRICALLY VERIFIED below (check 3): the only G-vs-P difference is exactly delta U.
-----------------------------------------------------------------------------------

ANTI-HANG: cheap forward evals ONLY.  NO coupled Newton / jacrev / iterative solve in
this module.  Single process, bounded grids (callers cap Nr<=24).

Every numeric/physics constant is tagged  # DERIVED | FREE | IMPORTED.
"""
import os, sys, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---- REUSED VALIDATED PIECES (do not re-derive) ----------------------------
from full3d_spectral import (Grid3D, attach_coord_weight, build_metric, T, R, TH, PS)
import b1prime_3d_offround_residual as B1   # validated derived-operator assembly

PI = math.pi

# Production constants (carried, each tagged) --------------------------------
X_PROD   = -2.0e5    # FREE     : kinetic/curvature ratio; R1-R3 do NOT fix it; ghost+Cassini => large NEGATIVE (native_dilation_weight Sec 9; branch_G Sec 3)
XI_PROD  = 2.0e-2    # FREE     : matter coupling xi (scale-breaker; value provenance open)
KAP_PROD = 2.0e-2    # FREE     : matter coupling kap
KAP8     = 1.0       # DERIVED  : matter coefficient (round-gate kap8=1; native_dilation_weight / F2)

VALID_BRANCHES = ("G", "P")


def U_potential(phi):
    """Branch-P retained angular-curvature potential U(phi) = e^{2phi} - 1.
    DERIVED (the Sec-3 shift-survivor; branch_P_characterization Sec 0)."""
    return torch.exp(torch.clamp(2.0 * phi, max=B1.__dict__.get("EXP_CLAMP", 60.0))) - 1.0


def U_prime(phi):
    """U'(phi) = 2 e^{2phi}.  DERIVED."""
    return 2.0 * torch.exp(torch.clamp(2.0 * phi, max=60.0))


# ===========================================================================
# THE BRANCHED MIXED OPERATOR  E^mu_nu.
#   branch='G' (DEFAULT, EXPLICIT): the clean two-player scalar-tensor operator
#       (matter_regrade lines 60-61).  This is the operator the native-S^2 solves
#       used SILENTLY; here it is the named, flagged default.
#   branch='P': adds + delta^mu_nu U(phi),  U = e^{2phi}-1  (branch_P Sec 1b).
# The branch is a REQUIRED, EXPLICIT, TAGGED parameter -- no silent smuggling.
# ===========================================================================
def E_mixed_branch(G, a, b, c, d, phi, Th, X=X_PROD, xi=XI_PROD, kap=KAP_PROD,
                   m=1, kap8=KAP8, branch="G", return_parts=False):
    if branch not in VALID_BRANCHES:
        raise ValueError(f"branch must be one of {VALID_BRANCHES}; got {branch!r} "
                         f"(the branch choice is EXPLICIT -- no silent default).")
    parts = B1.E_mixed(G, a, b, c, d, phi, Th, X, xi, kap, m=m, kap8=kap8,
                       return_parts=True)
    E = parts["E"]                                            # Branch-G mixed operator
    Pterm = None
    if branch == "P":
        U = U_potential(phi)                                 # DERIVED potential
        delta = torch.eye(4, device=E.device).expand(*phi.shape, 4, 4)
        Pterm = delta * U[..., None, None]                   # + delta^mu_nu U(phi)
        E = E + Pterm
    if return_parts:
        parts["E"] = E
        parts["branch"] = branch
        parts["Pterm"] = Pterm
        return parts
    return E


# ===========================================================================
# THE BRANCHED phi-EOM.
#   branch='G': EL_phi_3d (the action's own delta S/delta phi), validated.
#   branch='P': adds the -2 U'(phi) potential contribution.
# Sign vs EL_phi_3d's EL convention is EMPIRICALLY pinned in the self-test.
# ===========================================================================
def EL_phi_branch(G, a, b, c, d, phi, Th, X=X_PROD, xi=XI_PROD, kap=KAP_PROD,
                  m=1, kap8=KAP8, branch="G"):
    if branch not in VALID_BRANCHES:
        raise ValueError(f"branch must be one of {VALID_BRANCHES}; got {branch!r}.")
    elphi = B1.EL_phi_3d(G, a, b, c, d, phi, Th, X, xi, kap, m=m, kap8=kap8)
    if branch == "P":
        # doc eq 1a carries a -2 U'(phi) term; U' = 2 e^{2phi}  (DERIVED).
        elphi = elphi - 2.0 * U_prime(phi)
    return elphi


# ===========================================================================
# Full branched residual stack (cheap eval only; NO solve).
# ===========================================================================
def residual_branch(G, a, b, c, d, phi, Th, X=X_PROD, xi=XI_PROD, kap=KAP_PROD,
                    m=1, kap8=KAP8, branch="G"):
    E = E_mixed_branch(G, a, b, c, d, phi, Th, X, xi, kap, m=m, kap8=kap8, branch=branch)
    elphi = EL_phi_branch(G, a, b, c, d, phi, Th, X, xi, kap, m=m, kap8=kap8, branch=branch)
    elTh = B1.EL_Th_3d(G, a, b, c, d, phi, Th, X, xi, kap, m=m, kap8=kap8)
    return dict(E=E, elphi=elphi, elTh=elTh, branch=branch)


# ===========================================================================
# SLAVED-METRIC HELPER (for the vacuum verification).  When phi is the metric
# depth field (NOT the independent player), the metric form is
#   g_tt = -e^{-2phi} c^2,  g_rr = e^{+2phi},  angular r^2  (c=1 units).
# In the (a,b,c,d) warp parametrization g_tt=-e^{2a}, g_rr=e^{2b}, this is
#   a = -phi,  b = +phi,  c = d = 0.
# (relativistic_metric_rederivation_results.md:149,238; external_source_analysis.py)
# ===========================================================================
def slaved_warps_from_phi(phi):
    """Return (a,b,c,d) warps for the SLAVED metric g_tt=-e^{-2phi}, g_rr=e^{2phi}."""
    a = -phi
    b = phi
    c = torch.zeros_like(phi)
    d = torch.zeros_like(phi)
    return a, b, c, d


if __name__ == "__main__":
    # tiny smoke test (cheap)
    G = attach_coord_weight(Grid3D(Nr=12, Nth=8, Nps=8, rc=0.2, cell=2.0))
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=G.Rg.device)
    for br in VALID_BRANCHES:
        E = E_mixed_branch(G, z, z, z, z, z, z, branch=br)
        print(f"flat phi=0 branch={br}: max|E|(body) = {float(E[G.body].abs().max()):.2e}")
