#!/usr/bin/env python3
"""
p1_residual_general_einstein.py -- PHASE 1 of the everything-on solver build.

GOAL (EVERYTHING_ON_SOLVER_BUILD_MAP.md S III, P1): the production residual
(full3d_solver.residual_vector / full3d_newton.residual_vector_vsafe) calls the
DIAGONAL analytic Einstein `einstein_mixed_weyl`, so although the metric build
ALLOCATES spatial off-diagonal warps (e_rt, e_rp, e_tp), those off-diagonals NEVER
reach the field equations.  P1 RE-ROUTES the residual through the GENERAL 4x4 Einstein
so the spatial off-diagonal metric components become LIVE unknowns whose residual rows
are the corresponding GENERAL-Einstein components (G^r_th, G^r_ps, G^th_ps).

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  OBSERVE mode.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers).

MIGRATED 2026-06-24 (M1): derived scalar-tensor operator (e^{2phi} weight) via the
audited branch_operator; phi is the 6th field; off-diagonals dropped (diagonal target);
X=-1 small/non-stiff (M2 continues to -2e5).

=== THE CONDITIONING REALITY (found this session; honest, load-bearing) ===
A NAIVE swap `einstein_mixed_weyl -> einstein_mixed` (the general spectral Einstein,
which differentiates the Christoffels by a SECOND spectral pass) is NOT clean: on the
steep soliton warps (b = p ln(r/r_seal), with a 1/r derivative) the double spectral
pass is BADLY conditioned near the Chebyshev core edge.  Diagnosed flat-space error
GROWS with Nr (1.2e3 @ Nr=20 -> 3.8e3 @ Nr=40 in the innermost rows), and even the
DEEP-interior diagonal blocks of `einstein_mixed` disagree with the analytic
pole-stable `einstein_mixed_weyl` by O(1-3) on the soliton.  So routing the WHOLE
residual through the raw general Einstein would corrupt the DIAGONAL sector for a
NUMERICAL (conditioning) reason and the round soliton would NOT recover -- a false
"P1 failed" that is really a solver-conditioning artifact, not physics.

THE POLE-STABLE HYBRID (category-A conditioning ONLY; the field equations are
UNCHANGED -- it is the SAME general 4x4 Einstein, evaluated in a pole-stable way):

   G_full = G_weyl(a,b,c,d)  +  [ einstein_mixed(g_full) - einstein_mixed(g_diag) ]

where g_full = build_metric(a,b,c,d, e_rt,e_rp,e_tp) and g_diag = build_metric with
the off-diagonals ZEROED.  The bracket is the off-diagonal CONTRIBUTION to the general
Einstein.  Because both general evaluations share the SAME steep diagonal background,
the dominant core-conditioning error SUBTRACTS OUT in the difference (verified: the
difference is O(1e-3) near the core vs O(1e3) raw), while the genuine off-diagonal
content survives.  When e_rt=e_rp=e_tp=0 the bracket is IDENTICALLY ZERO (verified
machine-0), so G_full == G_weyl EXACTLY -> the diagonal sector and the round soliton
are provably unchanged.  This is the validated #56/2-D pole-stable analytic Einstein
as the BACKBONE plus the general-Einstein off-diagonal DELTA.

WHY THIS IS GENUINELY GENERAL-EINSTEIN (not "still diagonal"): the off-diagonal warps
e_rt,e_rp,e_tp ENTER the field equations through the general Einstein (the bracket),
both in the new OFF-DIAGONAL residual rows AND as their back-reaction onto the DIAGONAL
rows (the bracket has nonzero diagonal-block entries when off-diagonals are present --
the cross terms G^t_t, G^r_r, ... pick up the off-diagonal shear).  Off-diagonals are
therefore LIVE unknowns that feed the full coupled system.  The ONLY thing the analytic
Weyl provides is the pole-stable VALUE of the diagonal background at zero off-diagonal;
every off-diagonal effect is carried by the validated general 4x4 Einstein.

=== MATTER (P1 scope; NO Skyrme, NO B=1/A) ===
Matter stays the native S^2-carrier single-profile field + the general L2+L4 Hilbert
stress (whole_metric_3d_matter) -- the SAME stress the committed residual uses, which
already sources off-diagonal T components when the field is non-axisymmetric.  The CORE
boundary condition is the NATIVE regularity NODE (Theta'(core)=0, value FREE) -- NOT the
Skyrme twist Theta(core)=m*pi.  (The deg-1 homotopy seal value Theta(seal)=0 pins the
charge-1 sector at the OUTER node; that is a homotopy-sector choice, not the m*pi core
ladder.)  See `node_core` flag below.  MIGRATED 2026-06-24 (M1): derived scalar-tensor
operator (e^{2phi} weight) via the audited branch_operator; phi is the 6th field;
off-diagonals dropped (diagonal target); X=-1 small/non-stiff (M2 continues to -2e5).

This module provides the P1 residual + Jacobian; validation/observation live in
p1_validate.py.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
# functorch vmap (jacrev) trips the broken-NVML CUDA caching allocator on this V100;
# disabling the caching allocator sidesteps it (infra workaround, no numerics effect).
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    einstein_mixed, einstein_mixed_weyl, DEV, PI, T, R, TH, PS)
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
import free_s2_matter as S2M               # native S^2 3-component matter (grid-exact dn); the
                                           # imported S^3 field_n/field_dn left the live operator
from full3d_newton import inv4x4, det4x4   # vmap-safe 4x4 algebra (byte-equal to linalg)
from torch.func import grad as _fgrad        # functorch-composable grad (jacrev-safe)
import branch_operator as BR
import b1prime_3d_offround_residual as B1


# ===========================================================================
# PACK / UNPACK -- the 11 LIVE fields of the complete static solver:
#   4 diagonal metric warps (a,b,c,d) + 3 NATIVE-S^2 matter components (n1,n2,n3) +
#   the dilaton phi + 3 spatial off-diagonal warps (e_rt,e_rp,e_tp).  Each (Nr,Nth,Nps).
# The matter is the free unit-3-vector S^2 carrier (nhat=n/|n|); the imported S^3 Theta-profile
# is RETIRED.  (Time-row off-diagonals stay ZEROED -- that is P4, not P1.)
# ===========================================================================
_NFIELD = 11


def pack11(a, b, c, d, n1, n2, n3, phi, e_rt, e_rp, e_tp):
    return torch.cat([x.reshape(-1) for x in
                      (a, b, c, d, n1, n2, n3, phi, e_rt, e_rp, e_tp)])


def unpack11(u, G):
    n = G.Nr * G.Nth * G.Nps
    sh = (G.Nr, G.Nth, G.Nps)
    return [u[i*n:(i+1)*n].reshape(sh) for i in range(_NFIELD)]   # a,b,c,d,n1,n2,n3,phi,e_rt,e_rp,e_tp


def seed_round_native(G, p=1.0, m=1):
    """A clean static SEED: round metric warps (a=-p(1-s) gauge, b,c,d minimal) + the canon
    degree-1 native winding n=x/r (the topological sector the solver then relaxes WITHIN -- the
    winding charge is set by the seed's homotopy class, NOT a Theta-core BC pin).  phi=0, e_*=0."""
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=G.dev)
    s = (G.Rg - G.rc) / (G.ri - G.rc)
    a = -1.0 * (1 - s); b = 1.0 * (1 - s)
    n_raw = S2M.hedgehog_xr_components(G, m=m)          # (Nr,Nth,Nps,3) canon winding
    return pack11(a, b, z.clone(), z.clone(),
                  n_raw[..., 0], n_raw[..., 1], n_raw[..., 2], z.clone(),
                  z.clone(), z.clone(), z.clone())


# ===========================================================================
# THE GENERAL (POLE-STABLE HYBRID) MIXED EINSTEIN.  Returns G^mu_nu (...,4,4) for
# the FULL metric with off-diagonals live, computed pole-stably (see header).
# ===========================================================================
def einstein_general_hybrid(G, a, b, c, d, e_rt, e_rp, e_tp):
    g_full = build_metric(G, a, b, c, d, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    # off-diagonal delta from the validated general 4x4 Einstein
    g_diag = build_metric(G, a, b, c, d)
    Ggen_full, _, _, _ = einstein_mixed(G, g_full)
    Ggen_diag, _, _, _ = einstein_mixed(G, g_diag)
    delta = Ggen_full - Ggen_diag                 # the off-diagonal contribution
    Gweyl = einstein_mixed_weyl(G, a, b, c, d)    # pole-stable diagonal backbone
    return Gweyl + delta, g_full


# ===========================================================================
# THE P1 RESIDUAL VECTOR.  Off-diagonals LIVE.  Field eqns use the GENERAL Einstein.
#  Rows:
#    diagonal Einstein:  G^t_t, G^r_r, G^th_th, G^ps_ps  - kap8 T^mu_nu   (now incl.
#       off-diagonal back-reaction via the hybrid)
#    OFF-DIAGONAL Einstein: G^r_th, G^r_ps, G^th_ps      - kap8 T^mu_nu   (THE P1 rows
#       -- these are what the off-diagonal warps e_rt,e_rp,e_tp solve)
#    matter EL (matter_el_3d)
#    BC rows (Theta core/seal, gauge a(seal), depth b(core), c,d regular, off-diag
#       regular at core+seal).
# ===========================================================================
def _el_matter_s2_weighted(G, a, b, c, d, phi, n_raw, xi, kap, kap8=1.0,
                           e_rt=None, e_rp=None, e_tp=None):
    """jacrev-SAFE e^{2phi}-weighted NATIVE-S^2 matter EOM density over the 3 components n_raw:
    = kap8 * (1/measure) dS_m/dn,  S_m = INT sqrt-g e^{2phi} L_m,  L_m = L2+L4 of nhat=n/|n| with
    the GRID-EXACT dn (field_dn_components_exact).  torch.func.grad (functorch-composable) -> nests
    cleanly under jacrev.  The action depends ONLY on nhat, so dS/dn is automatically TANGENT to
    the sphere (the radial |n| direction is a null mode, pinned by the |n|=1 constraint row).  Off-
    diagonals flow into the FULL metric (consistent matter sector); e_*=0 => diagonal regression."""
    z = torch.zeros_like(a)
    e_rt = z if e_rt is None else e_rt
    e_rp = z if e_rp is None else e_rp
    e_tp = z if e_tp is None else e_tp
    g = build_metric(G, a, b, c, d, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp); ginv = inv4x4(g)
    f = torch.exp(torch.clamp(2 * phi, max=60.0))
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    fw = f * sqrtg * G.wvol_coord
    def action_of_n(nr):
        dn = S2M.field_dn_components_exact(G, nr)
        Gmn = MAT.field_metric(dn)
        Lm, _, _, _ = MAT.lagrangian(ginv, Gmn, xi, kap)
        return (fw * Lm).sum()
    gradN = _fgrad(action_of_n)(n_raw)
    return kap8 * gradN / torch.clamp(fw, min=1e-30)[..., None]    # (...,3) tangential EOM density


def residual_vector_p1(u, G, p, kap8, m=1, wbc=30.0, X=-1.0, xi=1.0, kap=1.0, branch="G"):
    """NATIVE-S^2 matter: the 3-component unit-3-vector carrier nhat=n/|n| with the GRID-EXACT dn.
    The winding CHARGE is set by the SEED's homotopy class (degree-1 = n=x/r) and CONSERVED by
    continuous relaxation -- there is NO Theta-core pin; the matter CORE IS FREE (the imported S^3
    deg1/Skyrme core BC is RETIRED).  Off-diagonals live.
    Rows: 4 diagonal + 3 off-diagonal Einstein; phi-EL; 3 native matter-EOM components; the |n|=1
    constraint (radial gauge-fix); metric/dilaton BCs; off-diagonal regularity."""
    a, b, c, d, n1, n2, n3, phi, e_rt, e_rp, e_tp = unpack11(u, G)
    n_raw = torch.stack([n1, n2, n3], dim=-1)
    dn = S2M.field_dn_components_exact(G, n_raw)
    E = BR.E_mixed_branch(G, a, b, c, d, phi, dn, X=X, xi=xi, kap=kap, m=m,
                          kap8=kap8, branch=branch, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    elphi = BR.EL_phi_branch(G, a, b, c, d, phi, dn, X=X, xi=xi, kap=kap, m=m,
                             kap8=kap8, branch=branch, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    elN = _el_matter_s2_weighted(G, a, b, c, d, phi, n_raw, xi, kap, kap8=kap8,
                                 e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)        # (...,3) tangential EOM
    g = build_metric(G, a, b, c, d, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg * G.wvol_coord)
    W = W / W[G.body].mean()
    bod = G.body
    rows = []
    # FOUR diagonal + THREE off-diagonal Einstein rows (the off-diagonal rows are the field
    # equations the e_rt/e_rp/e_tp warps solve; identically the diagonal target when e_*=0).
    for (mm, nn) in [(T, T), (R, R), (TH, TH), (PS, PS),
                     (R, TH), (R, PS), (TH, PS)]:
        rows.append((W * E[..., mm, nn])[bod])
    rows.append((W * elphi)[bod])                         # phi-EL
    # native S^2 matter: the 3 EOM components (tangential) + the |n|=1 constraint (radial gauge-fix)
    for ai in range(3):                                      # DERIVED: 3 = the S^2 target's components
        rows.append((W * elN[..., ai])[bod])
    rows.append((wbc * ((n_raw ** 2).sum(-1) - 1.0))[bod])   # DERIVED: |n|=1 unit-sphere constraint
    # ---- metric/dilaton BC rows (NO Theta pin -- the matter core is FREE; winding from seed) ----
    rows.append(wbc * a[-1, :, :].reshape(-1))            # a(seal)=0 gauge
    rows.append(wbc * (b[0, :, :].reshape(-1) + p))       # b(core)=-p depth dial
    rows.append(wbc * c[0, :, :].reshape(-1)); rows.append(wbc * c[-1, :, :].reshape(-1))
    rows.append(wbc * d[0, :, :].reshape(-1)); rows.append(wbc * d[-1, :, :].reshape(-1))
    rows.append(wbc * phi[-1, :, :].reshape(-1))          # phi(seal)=0
    # off-diagonal warps regular (=0) at core + seal (mirror c,d; the off-diagonal sector's BCs)
    for e in (e_rt, e_rp, e_tp):
        rows.append(wbc * e[0, :, :].reshape(-1)); rows.append(wbc * e[-1, :, :].reshape(-1))
    F = torch.cat([r.reshape(-1) for r in rows])
    return F


# ===========================================================================
# BATCHED Jacobian via torch.func.jacrev (one batched reverse pass).  Same pattern
# as full3d_newton.jacobian_jacrev; the residual is vmap-safe (inv4x4/det4x4, no
# linalg.inv/det/solve inside).
# ===========================================================================
def jacobian_p1(u, G, p, kap8, m=1, wbc=30.0,
                X=-1.0, xi=1.0, kap=1.0, branch="G", chunk_size=128):
    from torch.func import jacrev
    f = lambda uu: residual_vector_p1(uu, G, p, kap8, m=m, wbc=wbc,
                                      X=X, xi=xi, kap=kap, branch=branch)
    J = jacrev(f, chunk_size=chunk_size)(u)
    F = residual_vector_p1(u, G, p, kap8, m=m, wbc=wbc, X=X, xi=xi, kap=kap,
                           branch=branch).detach()
    return J.detach(), F


# ===========================================================================
# PRODUCTION LM / Newton solve (direct factorized damped LS step; strict monotone
# accept).  Identical control flow to full3d_newton.newton_solve.
# ===========================================================================
def newton_solve_p1(u, G, p, kap8, m=1, maxit=40, lam0=1e-4, tol=1e-11,
                    verbose=False, wbc=30.0,
                    X=-1.0, xi=1.0, kap=1.0, branch="G",
                    chunk_size=128, lam_min=1e-14):
    import numpy as np
    u = u.detach().clone()
    lam = lam0
    F = residual_vector_p1(u, G, p, kap8, m=m, wbc=wbc, X=X, xi=xi, kap=kap, branch=branch)
    Phi = float((F * F).sum()); hist = [Phi]
    nU = u.numel()
    I = torch.eye(nU, device=u.device)
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = jacobian_p1(u, G, p, kap8, m=m, wbc=wbc,
                           X=X, xi=xi, kap=kap, branch=branch,
                           chunk_size=chunk_size)
        accepted = False
        for _try in range(12):
            try:
                Jaug = torch.cat([J, math.sqrt(lam) * I], dim=0)
                Faug = torch.cat([-F, torch.zeros(nU, device=u.device)], dim=0)
                du = torch.linalg.lstsq(Jaug, Faug).solution
            except Exception:
                lam *= 4.0; continue
            un = u + du
            Pn = float((residual_vector_p1(un, G, p, kap8, m=m, wbc=wbc,
                                           X=X, xi=xi, kap=kap, branch=branch) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam * 0.25, lam_min); accepted = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"  [p1-newton] it={it:3d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    return u.detach(), hist


# ===========================================================================
# CONTINUATION IN X (M2): the X-kinetic coefficient is large-negative at the
# production value (X=-2e5, Cassini-bounded) and SINGULARLY STIFF there (the
# branchGP prototype could not floor it cold).  Warm-start up a geometric X-ladder
# from a small/non-stiff X to the target so each step stays on the solution
# manifold.  This is the in-built fix for the stiffness; the guard checks
# N-convergence at the production X.
# ===========================================================================
def continuation_solve_p1(u0, G, p, kap8, X_target=-2.0e5, X_start=-1.0, n_steps=10,
                          m=1, maxit=12, xi=1.0, kap=1.0,
                          branch="G", step_tol=1e-8, verbose=False):
    """ADAPTIVE geometric X-ladder: warm-start each step; if a step fails to floor
    below step_tol, SUBDIVIDE (halve the X-jump in log space) and retry, so a stalled
    step cannot cascade.  Finer ladder + more iters than the first cut (the larger
    grids need it -- worse conditioning at large |X|)."""
    import numpy as np
    logs = list(-np.geomspace(abs(X_start), abs(X_target), n_steps))  # endpoints incl target
    u = u0; hist = [None]; Xprev = None
    i = 0
    while i < len(logs):
        X = logs[i]
        u_try, h = newton_solve_p1(u, G, p, kap8, m=m, maxit=maxit, X=float(X),
                                   xi=xi, kap=kap, branch=branch, verbose=False)
        if h[-1] > step_tol and Xprev is not None and abs(X - Xprev) > 1e-9 * abs(X):
            # stalled -> insert a midpoint (log) and retry from the last good u
            Xmid = -math.exp(0.5 * (math.log(abs(Xprev)) + math.log(abs(X))))
            logs.insert(i, Xmid)
            if verbose:
                print(f"  [X-cont] X={float(X):.3e} stalled Phi={h[-1]:.2e} "
                      f"-> subdivide at {Xmid:.3e}", flush=True)
            continue
        u, hist, Xprev = u_try, h, X
        if verbose:
            print(f"  [X-cont] X={float(X):.3e} Phi={hist[-1]:.3e}", flush=True)
        i += 1
    return u, hist, float(logs[-1])


# ===========================================================================
# per-component residual breakdown (validation report)
# ===========================================================================
def component_residuals_p1(u, G, p, kap8, m=1, X=-1.0, xi=1.0, kap=1.0, branch="G"):
    a, b, c, d, n1, n2, n3, phi, e_rt, e_rp, e_tp = unpack11(u, G)
    n_raw = torch.stack([n1, n2, n3], dim=-1)
    dn = S2M.field_dn_components_exact(G, n_raw)
    E = BR.E_mixed_branch(G, a, b, c, d, phi, dn, X=X, xi=xi, kap=kap, m=m,
                          kap8=kap8, branch=branch, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    elphi = BR.EL_phi_branch(G, a, b, c, d, phi, dn, X=X, xi=xi, kap=kap, m=m,
                             kap8=kap8, branch=branch, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    elN = _el_matter_s2_weighted(G, a, b, c, d, phi, n_raw, xi, kap, kap8=kap8,
                                 e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
    bod = G.body
    names = {(T, T): 'tt', (R, R): 'rr', (TH, TH): 'thth', (PS, PS): 'psps',
             (R, TH): 'rth', (R, PS): 'rps', (TH, PS): 'thps'}
    out = {nm: float(E[..., mm, nn][bod].abs().max()) for (mm, nn), nm in names.items()}
    out['elphi'] = float(elphi[bod].abs().max())
    out['elN'] = float(elN[bod].abs().max())
    out['phi_max'] = float(phi[bod].abs().max())
    out['nnorm_err'] = float(((n_raw ** 2).sum(-1) - 1.0)[bod].abs().max())  # DERIVED: |n|=1
    out['eoff_max'] = max(float(x[bod].abs().max()) for x in (e_rt, e_rp, e_tp))
    return out
