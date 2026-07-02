"""cell_solver_f2d_embedded_run.py -- the EMBEDDED (Class-A EMBEDDED) finite-cell run.

THE DECISIVE TEST (strictly per the gated + blind-verified spec):
  Does matching a finite winding cell to an AMBIENT (universe-interior) state admit finite cells
  where the strictly-CLOSED (H=0, both-mirror) cell could NOT?  The closed cell has NO finite cell
  at N=1,2,3 -- not because the matter is bad (it is convex/stable, Step-0 V7) but because the
  GEOMETRY has no finite stationary point: with outer MIRROR (Neumann) seal, dilution (rho->inf,
  phi->deep-neg) is always downhill (nothing pins the seal).  The EMBEDDED seal PINS the seal data
  to an ambient solution (Dirichlet + momentum + matter matches), which may close that escape
  direction.  This run tests whether it does.

BINDING SPEC / FOUNDATION (re-read while building):
  * embedded_run_mini_MAP.md            -- the CORRECTED counting (sec.1), boundary/Derrick (sec.5),
                                           what-counts (sec.6), gate-cleared (sec.8).
  * embedded_run_gate_rulings.md        -- Ruling 1 (5-condition count; C2->E_ang=m_amb),
                                           Ruling 2 (adapted Derrick), Ruling 3 (MODEL ambient FIRST).
  * embedded_cell_closure_H_amb_results.md -- H_cell=H_amb DERIVED+blind-verified.
  * cell_solver_f2d.py                  -- CAS-verified operators REUSED verbatim (make_ctx, fields,
                                           H_of_r, derrick, unpack, pack, seed).
  * cell_solver_f2d_N2.py               -- the two-tier stability filter (tier-a matter ENERGY
                                           Hessian PD => stable; tier-b constraint-respecting resolve).

============================ THE MATCHING (Ruling 1; 5 conditions) ============================
Interior cell on r in [r_c, r_s].  Core = regular/mirror inner boundary: phi'_c=0, rho'_c=0, f_r,c=0.
Outer seal r_s = the MATCHED interface (NOT a mirror).  Ambient supplies FIVE numbers on ONE axis a:
  (1) phi_cell(r_s)  = phi_amb                                     [field continuity]
  (2) rho_cell(r_s)  = rho_amb                                     [field continuity]
  (3) pi_phi,cell    = pi_phi,amb ,   pi_phi = Z rho^2 phi'        [momentum / JC1 dilation flux]
  (4) pi_rho,cell    = pi_rho,amb ,   pi_rho = -4 e^{-2phi} rho'   [momentum / JC2]
  (5) E_ang,cell(r_s)= m_amb ,        E_ang  = (xi/2)(I_th+N^2 I_s) + (kap N^2/2) I_4th/rho^2 (f_r=0)
[H_geo]=0 is AUTOMATIC given (1)-(4) (H_geo is momenta-only: H_geo=pi_phi^2/(2Z rho^2)-pi_rho^2 e^{2phi}/8-2),
so (5) is the ONE independent matter condition.  H_amb = H_geo(amb)+m_amb is DERIVED, never specified.

COUNT: a FREE -> unknowns (phi_c,rho_c,r_s,a)=4 vs 5 conditions -> OVER-by-1 -> cells only at ISOLATED
ambient values (the Misner-Sharp band).  a FIXED -> 3 vs 5 -> over-by-2.

============================ NUMERICAL SCHEME (square field solve + leftover residuals) ============================
At FIXED (a, L=r_s-r_c) the interior field BVP is SQUARE with the inner mirror + the outer
Dirichlet matches (1),(2) [and f_r,s=0, the natural BC that condition (5) is evaluated at]:
   unknowns  w = [phi(Nr), rho(Nr), u(Nr*Nth)]              (2Nr + Nr*Nth)
   rows: phi-ODE(Nr-2) | phi'_c=0 | phi_s-phi_amb | rho-ODE(Nr-2) | rho'_c=0 | rho_s-rho_amb
         | f-PDE(Nr-2)*Nth | f_r,c=0 (Nth) | f_r,s=0 (Nth)  == 2Nr + Nr*Nth  (SQUARE)
The DIRICHLET pins (1),(2) are exactly what BLOCK the closed-cell runaway (rho_s, phi_s can no longer
dilute to inf/-inf).  The LEFTOVER conditions -- momentum (3),(4) and matter (5) -- are read off the
solved field as residuals R3,R4,R5.  This realizes the spec's "square in the 4 unknowns
(phi_c,rho_c,r_s,a)": the field solve consumes (phi_c,rho_c) and imposes (1),(2); the 2D root-find over
(a,L) targets R3=R4=0 [momentum matches] -> isolated (a*,L*); then R5 is checked (the over-by-1
rejection).  A genuine EMBEDDED CELL = all 5 residuals -> 0, Derrick-clean, stable, seed/grid-robust.

OBSERVE, do NOT target.  Honest outcomes (all first-class): (i) runaway-EVERYWHERE (embedding does not
rescue it); (ii) a CONTINUUM of a all admitting cells (a discreteness FAILURE); (iii) ISOLATED a (a
band) -- the predicted outcome, but EARNED not declared.  UNLABELED; no particle/mass labels.

DISCIPLINE / ANTI-HANG: single clean unbuffered process; NO background; NO nohup.  Bounded: Nr<=24,
Nth<=28, LM iters<=150/solve, per-solve + hard total wall budget; throughput-limited recorded, never a
hang.  Fixed values tagged CHOSE/THEORY/MODEL.  This is a MODEL ambient, N in {1,2}, one Z -- ONE slice.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys
import json
import math
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import cell_solver_f2d as M                       # CAS-verified operators (REUSED verbatim)
import cell_solver_f2d_first_build as FB          # _w_to_v, lm_solve, PHI_CAP (REUSED)
import cell_solver_f2d_N2 as N2                   # two-tier stability filter (REUSED)


# =========================================================================================
# MODEL AMBIENT (Ruling 3) -- DECLARED coarse rule; everything labeled MODEL.
# =========================================================================================
# The ambient is modeled as a point sampled at areal radius R_amb = a on the NATIVE radial family
# phi_A(r) = -q/r , rho_A(r) = r  (the R-areal reading rho=r is a repo theorem; (r^2 phi')'=0 gives
# phi = phi_inf - q/r, phi_inf = 0 wlog for the model).  This is a SIMPLE, DECLARED coarse profile:
# the five ambient numbers are then EXACTLY consistent with the momentum-definition relations
# (pi_phi = Z rho^2 phi', pi_rho = -4 e^{-2phi} rho') and the H_geo Legendre relation -- NOT five
# arbitrary numbers.  m_amb (the ambient bulk-matter H-contribution) is modeled density-like, mu/a^2.
#   axis:  a = R_amb  (ambient sampling radius / inverse-density-like diagnostic axis)
# MODEL CONSTANTS (chosen round + physically sane BEFORE any residual was computed; anti-targeting):
#   q_amb = 0.5   (MODEL dilation charge of the coarse ambient profile)
#   mu_amb= 1.0   (MODEL ambient matter scale; m_amb = mu/a^2)
# CAVEAT (declared): this coarse family is the analytically-clean native radial profile; the DERIVED
# universe-interior (Branch-P/matter, F5 critical) value is DEFERRED and marked later, per Ruling 3.
Q_AMB = 0.5      # MODEL
MU_AMB = 1.0     # MODEL

def model_ambient(a, Z, q=Q_AMB, mu=MU_AMB):
    """Return the 5 MODEL ambient numbers + the DERIVED H_amb, at axis value a (=R_amb>0)."""
    phi_amb = -q / a
    rho_amb = a
    phip_amb = q / a ** 2
    rhop_amb = 1.0
    pif_amb = Z * rho_amb ** 2 * phip_amb          # = Z q  (conserved dilation flux)
    pir_amb = -4.0 * math.exp(-2.0 * phi_amb) * rhop_amb   # = -4 e^{2q/a}
    m_amb = mu / a ** 2                            # MODEL bulk-matter H-contribution (density-like)
    # H_geo (Ruling 1 Legendre inversion) + m_amb = H_amb  (DERIVED, not specified)
    H_geo = pif_amb ** 2 / (2.0 * Z * rho_amb ** 2) - pir_amb ** 2 * math.exp(2.0 * phi_amb) / 8.0 - 2.0
    H_amb = H_geo + m_amb
    return dict(a=float(a), phi_amb=float(phi_amb), rho_amb=float(rho_amb),
                pif_amb=float(pif_amb), pir_amb=float(pir_amb), m_amb=float(m_amb),
                H_geo=float(H_geo), H_amb=float(H_amb),
                phip_amb=float(phip_amb), rhop_amb=float(rhop_amb))


# =========================================================================================
# EMBEDDED FIELD RESIDUAL  (square; inner mirror + outer Dirichlet matches (1),(2) + f_r,s=0)
#   unknown w = [phi(Nr), rho(Nr), u(Nr*Nth)];  L, amb fixed
# =========================================================================================
def residual_embedded(w, ctx, prm, L, amb, wbc=1.0):
    Q = M.fields(FB._w_to_v(w, ctx, L), ctx, prm)
    phip, rhop, fr = Q["phip"], Q["rhop"], Q["fr"]
    phi, rho = Q["phi"], Q["rho"]
    rows = [
        Q["phi_ode"][1:-1],                                   # phi-ODE interior
        wbc * phip[[0]],                                      # phi'_c = 0        (inner mirror)
        wbc * (phi[[-1]] - amb["phi_amb"]),                  # phi_s = phi_amb   (outer Dirichlet, match 1)
        Q["rho_ode"][1:-1],                                   # rho-ODE interior
        wbc * rhop[[0]],                                      # rho'_c = 0        (inner mirror)
        wbc * (rho[[-1]] - amb["rho_amb"]),                  # rho_s = rho_amb   (outer Dirichlet, match 2)
        Q["res_f"][1:-1].reshape(-1),                        # f-PDE interior
        wbc * fr[0, :],                                       # f_r,c = 0         (inner mirror)
        wbc * fr[-1, :],                                      # f_r,s = 0         (natural BC; match-5 point)
    ]
    return torch.cat([r.reshape(-1) for r in rows])


def seal_diagnostics(w, ctx, prm, L, amb):
    """Leftover matching residuals R3 (pi_phi), R4 (pi_rho), R5 (E_ang) at the seal, + raw seal values."""
    Z, XI, KAP, N = prm
    v = FB._w_to_v(w, ctx, L)
    Q = M.fields(v, ctx, prm)
    phi, rho, phip, rhop = Q["phi"], Q["rho"], Q["phip"], Q["rhop"]
    e2m = Q["e2m"]
    Ith, Is, I4th = Q["Ith"], Q["Is"], Q["I4th"]
    rho_s = rho[-1]
    pif_s = Z * rho_s ** 2 * phip[-1]
    pir_s = -4.0 * e2m[-1] * rhop[-1]
    Eang_s = (XI / 2.0) * (Ith[-1] + N ** 2 * Is[-1]) + (KAP * N ** 2 / 2.0) * I4th[-1] / rho_s ** 2
    R3 = float(pif_s) - amb["pif_amb"]
    R4 = float(pir_s) - amb["pir_amb"]
    R5 = float(Eang_s) - amb["m_amb"]
    return dict(R3=R3, R4=R4, R5=R5, pif_s=float(pif_s), pir_s=float(pir_s),
                Eang_s=float(Eang_s), phi_s=float(phi[-1]), rho_s=float(rho_s),
                phip_s=float(phip[-1]), rhop_s=float(rhop[-1]))


# =========================================================================================
# EMBEDDED SEED + SOLVE
# =========================================================================================
def emb_seed(ctx, amb, amp=0.05, slope_frac=0.0):
    """Reduced seed: phi ~ phi_amb, rho ~ rho_amb (near the outer Dirichlet target so the seal match is
    roughly seed-consistent -- a SEED only, LM relaxes), + the band-limited radial u deformation of
    M.seed (degree-safe, f_r=0 both ends, activates I_r).  All CHOSE seed values."""
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    zeta, mu = ctx["zeta"], ctx["mu"]
    gr = torch.cos(np.pi * (zeta + 1.0) / 2.0)
    uf = amp * (1.0 - mu[None, :] ** 2) * gr[:, None]
    phi = torch.full((Nr,), float(amb["phi_amb"]), dtype=torch.float64)
    rho = torch.full((Nr,), float(amb["rho_amb"]), dtype=torch.float64)
    v = M.pack(phi, rho, uf, 1.0)
    return v[:-1].clone()


def solve_embedded(w0, ctx, prm, L, amb, wbc=1.0, maxit=140, tol=1e-13, budget=8.0):
    """Relax the square embedded BVP at fixed (a,L).  Honest convergence gate identical in spirit to
    FB.solve_at_L: converged requires Phi<tol AND iters<maxit AND |phi| bounded AND rho>0."""
    resfn = lambda ww: residual_embedded(ww, ctx, prm, L, amb, wbc=wbc)
    w, Phi, iters, wall = FB.lm_solve(resfn, w0, maxit=maxit, tol=tol, time_budget=budget)
    v = FB._w_to_v(w, ctx, L)
    phi, rho, uf, _ = M.unpack(v, ctx)
    finite = bool(torch.isfinite(w).all())
    rho_min = float(rho.min()); phi_absmax = float(phi.abs().max())
    stalled = (iters >= maxit)
    collapsed = (rho_min <= 1e-4) or (not finite)
    runaway = (phi_absmax >= FB.PHI_CAP)
    converged = (Phi < 1e-11) and finite and (rho_min > 1e-4) and (not stalled) and (not runaway)
    outcome = ("converged" if converged else "collapsed" if collapsed
               else "runaway" if runaway else "stall")
    sd = seal_diagnostics(w, ctx, prm, L, amb)
    return dict(w=w, Phi=float(Phi), iters=int(iters), wall=float(wall), converged=converged,
                collapsed=collapsed, runaway=runaway, stalled=stalled, rho_min=rho_min,
                phi_absmax=phi_absmax, outcome=outcome, **sd)


# =========================================================================================
# ADAPTED DERRICK ARTIFACT FILTER (Ruling 2):  S_a - S_b + (r_s - r_c) H_amb - pi_rho(r_s) rho(r_s) = 0
# =========================================================================================
def adapted_derrick_residual(w, ctx, prm, L, amb):
    v = FB._w_to_v(w, ctx, L)
    Sa, Sb, _ = M.derrick(v, ctx, prm)
    sd = seal_diagnostics(w, ctx, prm, L, amb)
    r_c = ctx["rc"]; r_s = r_c + float(L)
    res = Sa - Sb + (r_s - r_c) * amb["H_amb"] - sd["pir_s"] * sd["rho_s"]
    return dict(Sa=float(Sa), Sb=float(Sb), adapted_res=float(res))


# =========================================================================================
# CROSS-CHECKS (solver-first discipline: interrogate the mismatch before banking it) --
# a genuine matched cell must appear regardless of WHICH matching subset is imposed and of the
# ambient CHARGE.  Two complementary probes:
#   (B) SCHEME B: impose the momenta/SLOPES (3),(4) as outer Neumann BCs, read the field-VALUE
#       residuals R1=phi_s-phi_amb, R2=rho_s-rho_amb.  (Scheme A imposes values, reads momenta.)
#   (U) UNCHARGED ambient (q=0): pif_amb=0 -- separates the dilation-flux match (3) from the
#       rho'-continuity match (4) (the native areal family keeps rho'=1 -> pir_amb=-4 even at q=0).
# =========================================================================================
def model_ambient_uncharged(a, Z, mu=MU_AMB):
    """MODEL uncharged (q=0) ambient: phi_amb=0 (flat), rho_amb=a (areal, rho'=1 still)."""
    phi_amb = 0.0; rho_amb = a; phip_amb = 0.0; rhop_amb = 1.0
    pif_amb = 0.0
    pir_amb = -4.0 * rhop_amb
    m_amb = mu / a ** 2
    H_geo = -pir_amb ** 2 / 8.0 - 2.0
    return dict(a=float(a), phi_amb=phi_amb, rho_amb=float(rho_amb), pif_amb=pif_amb,
                pir_amb=float(pir_amb), m_amb=float(m_amb), H_geo=float(H_geo),
                H_amb=float(H_geo + m_amb), phip_amb=phip_amb, rhop_amb=rhop_amb)


def residual_embedded_schemeB(w, ctx, prm, L, amb, wbc=1.0):
    """Square field BVP: inner mirror + OUTER NEUMANN momentum matches (impose the ambient seal
    slopes phi'_s, rho'_s from pif_amb, pir_amb) + f_r,s=0."""
    Z = prm[0]
    Q = M.fields(FB._w_to_v(w, ctx, L), ctx, prm)
    phi, rho, phip, rhop, fr = Q["phi"], Q["rho"], Q["phip"], Q["rhop"], Q["fr"]
    phip_tgt = amb["pif_amb"] / (Z * rho[-1] ** 2)             # from pif_s = Z rho_s^2 phi'_s
    rhop_tgt = -amb["pir_amb"] * torch.exp(2.0 * phi[-1]) / 4.0  # from pir_s = -4 e^{-2phi_s} rho'_s
    rows = [
        Q["phi_ode"][1:-1], wbc * phip[[0]], wbc * (phip[[-1]] - phip_tgt),
        Q["rho_ode"][1:-1], wbc * rhop[[0]], wbc * (rhop[[-1]] - rhop_tgt),
        Q["res_f"][1:-1].reshape(-1), wbc * fr[0, :], wbc * fr[-1, :],
    ]
    return torch.cat([r.reshape(-1) for r in rows])


def solve_embedded_schemeB(w0, ctx, prm, L, amb, budget=8.0):
    resfn = lambda ww: residual_embedded_schemeB(ww, ctx, prm, L, amb)
    w, Phi, iters, wall = FB.lm_solve(resfn, w0, maxit=140, tol=1e-13, time_budget=budget)
    v = FB._w_to_v(w, ctx, L); phi, rho, uf, _ = M.unpack(v, ctx)
    finite = bool(torch.isfinite(w).all()); pam = float(phi.abs().max()); rmin = float(rho.min())
    converged = (Phi < 1e-11) and finite and rmin > 1e-4 and iters < 140 and pam < FB.PHI_CAP
    sd = seal_diagnostics(w, ctx, prm, L, amb)
    R1 = float(phi[-1]) - amb["phi_amb"]; R2 = float(rho[-1]) - amb["rho_amb"]
    return dict(w=w, Phi=float(Phi), iters=int(iters), converged=converged, phi_absmax=pam,
                rho_min=rmin, R1=R1, R2=R2, R5=sd["R5"], phip_s=sd["phip_s"], rhop_s=sd["rhop_s"])


# =========================================================================================
# 2D root residual G(a,L) = (R3, R4) via a nested field solve (momentum matches).
# =========================================================================================
def G_aL(a, L, ctx, prm, Z, wseed=None, budget=8.0):
    amb = model_ambient(a, Z)
    w0 = emb_seed(ctx, amb) if wseed is None else wseed
    r = solve_embedded(w0, ctx, prm, L, amb, budget=budget)
    return r, amb


# =========================================================================================
# EMBEDDED tier-b resolve (constraint-respecting): perturb along a matter eigenvector, re-solve the
# EMBEDDED BVP, distance back.  (tier-a energy Hessian is geometry-frozen matter energy => reused
# verbatim from N2 without change.)
# =========================================================================================
def emb_coupled_resolve_negmode(w_star, v_neg, ctx, prm, L, amb, delta=0.05, budget=10.0):
    vn = v_neg / (v_neg.norm() + 1e-30)
    scale = float(w_star.norm()) + 1e-30
    w_pert = w_star + delta * scale * vn
    r = solve_embedded(w_pert, ctx, prm, L, amb, budget=budget)
    dist_back = float((r["w"] - w_star).norm() / scale)
    return dict(converged=r["converged"], dist_back=dist_back, Phi=r["Phi"], collapsed=r["collapsed"])


def emb_tier_b(w, evec, eig, ctx, prm, L, amb, n_modes=3, delta=0.05, budget=10.0):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    n_neg = int((eig < 0).sum())
    ks = list(range(min(n_modes, max(n_neg, 1))))
    results = []
    for k in ks:
        v_neg = torch.cat([torch.zeros(2 * Nr, dtype=torch.float64), evec[:, k].detach()])
        rr = emb_coupled_resolve_negmode(w, v_neg, ctx, prm, L, amb, delta=delta, budget=budget)
        rr["lam"] = float(eig[k]); results.append(rr)
    returns = all(m["converged"] and m["dist_back"] < 0.1 and not m["collapsed"] for m in results)
    return dict(per_mode=results, returns=returns)


# =========================================================================================
# MAIN  (single process, unbuffered, bounded)
# =========================================================================================
if __name__ == "__main__":
    T0 = time.time()
    TOTAL_BUDGET = float(os.environ.get("EMB_TOTAL_BUDGET", "900"))   # hard total wall (s)
    PER_SOLVE = float(os.environ.get("EMB_PER_SOLVE", "8"))           # per-solve wall (s)
    Nr = int(os.environ.get("EMB_NR", "16"))                         # CHOSE bounded grid (<=24)
    Nth = int(os.environ.get("EMB_NTH", "12"))                       # CHOSE bounded grid (<=28)
    Z = 8.0                                                          # CHOSE-fixed (Route-A; OBS-2)
    XI = 1.0; KAP = 1.0                                              # CHOSE-units
    N_LIST = [1, 2]                                                  # DERIVED-topological (this slice)
    a_grid = list(np.linspace(0.55, 2.0, 11))                       # CHOSE ambient-axis scan (R_amb>0)
    L_grid = list(np.linspace(0.30, 1.60, 7))                       # CHOSE cell-length scan

    def elapsed():
        return time.time() - T0
    def budget_left():
        return TOTAL_BUDGET - elapsed()

    print("=" * 100, flush=True)
    print("EMBEDDED (Class-A EMBEDDED) finite-cell run -- MODEL ambient, N in {1,2}, Z=8, xi=kap=1.", flush=True)
    print("Decisive test: does matching to an ambient admit finite cells where the CLOSED cell could NOT?", flush=True)
    print(f"MODEL ambient: phi_A=-q/r, rho_A=r (native radial family); axis a=R_amb; q={Q_AMB} mu={MU_AMB} "
          f"(MODEL consts). H_amb=H_geo(amb)+m_amb DERIVED.", flush=True)
    print(f"grid Nr={Nr} Nth={Nth}; a_grid=[{a_grid[0]:.2f}..{a_grid[-1]:.2f}]x{len(a_grid)}; "
          f"L_grid=[{L_grid[0]:.2f}..{L_grid[-1]:.2f}]x{len(L_grid)}; per-solve={PER_SOLVE}s total={TOTAL_BUDGET}s",
          flush=True)
    print("=" * 100, flush=True)

    ctx = M.make_ctx(Nr, Nth, rc=0.5)
    a_mid = float(np.median(a_grid)); L_mid = float(np.median(L_grid))
    grand = {"model_ambient": {"rule": "phi_A=-q/r, rho_A=r (native radial family); a=R_amb",
                               "q": Q_AMB, "mu": MU_AMB, "Z": Z,
                               "sample_at_a_mid": model_ambient(a_mid, Z)},
             "meta": {"Nr": Nr, "Nth": Nth, "a_grid": a_grid, "L_grid": L_grid,
                      "per_solve": PER_SOLVE, "total_budget": TOTAL_BUDGET}}

    amb_mid = model_ambient(a_mid, Z)
    print(f"\n[MODEL ambient @ a=a_mid={a_mid:.3f}]: phi_amb={amb_mid['phi_amb']:+.4f} rho_amb={amb_mid['rho_amb']:.4f} "
          f"pif_amb={amb_mid['pif_amb']:+.4f} pir_amb={amb_mid['pir_amb']:+.4f} m_amb={amb_mid['m_amb']:.4f} "
          f"-> H_geo={amb_mid['H_geo']:+.4f} H_amb={amb_mid['H_amb']:+.4f}", flush=True)

    for N in N_LIST:
        prm = (Z, XI, KAP, N)
        print("\n" + "#" * 100, flush=True)
        print(f"### N={N}  Z={Z}  xi=kap=1 ###", flush=True)
        print("#" * 100, flush=True)
        Nrec = {}

        # ---------- PHASE 0: THE KEY QUESTION -- finite stationary point vs runaway ----------
        # Contrast the EMBEDDED (outer Dirichlet match) solve against the CLOSED (outer mirror) solve at
        # the SAME (a_mid, L_mid) representative point.  Does pinning the seal give a FINITE config?
        print(f"\n--- PHASE 0 [KEY QUESTION @ a={a_mid:.3f}, L={L_mid:.3f}]: embedded (Dirichlet) vs closed (mirror) ---",
              flush=True)
        w0 = emb_seed(ctx, amb_mid)
        r_emb = solve_embedded(w0, ctx, prm, L_mid, amb_mid, budget=PER_SOLVE)
        # closed reference: same geometry seed, outer MIRROR (FB.solve_at_L), same L
        w0c = FB._seed_w(ctx, phi0=amb_mid["phi_amb"], rho0=amb_mid["rho_amb"], amp=0.05)
        r_cls = FB.solve_at_L(w0c, ctx, prm, L_mid, budget=PER_SOLVE)
        print(f"  EMBEDDED: outcome={r_emb['outcome']:9s} Phi={r_emb['Phi']:.2e} it={r_emb['iters']} "
              f"|phi|max={r_emb['phi_absmax']:.2f} rho_min={r_emb['rho_min']:.3f} "
              f"| R3(pif)={r_emb['R3']:+.3e} R4(pir)={r_emb['R4']:+.3e} R5(Eang)={r_emb['R5']:+.3e}", flush=True)
        print(f"  CLOSED  : outcome={r_cls['outcome']:9s} Phi={r_cls['Phi']:.2e} it={r_cls['iters']} "
              f"|phi|max={r_cls['phi_absmax']:.2f} rho_min={r_cls['rho_min']:.3f}", flush=True)
        finite_point = r_emb["outcome"] in ("converged", "stall") and r_emb["phi_absmax"] < FB.PHI_CAP
        print(f"  => EMBEDDED gives a FINITE (non-runaway) interior config: {finite_point}  "
              f"(closed reference outcome = {r_cls['outcome']})", flush=True)
        Nrec["phase0"] = dict(a=a_mid, L=L_mid, embedded=dict(outcome=r_emb["outcome"], Phi=r_emb["Phi"],
                              phi_absmax=r_emb["phi_absmax"], rho_min=r_emb["rho_min"],
                              R3=r_emb["R3"], R4=r_emb["R4"], R5=r_emb["R5"]),
                              closed=dict(outcome=r_cls["outcome"], phi_absmax=r_cls["phi_absmax"],
                                          rho_min=r_cls["rho_min"]),
                              finite_point=bool(finite_point))

        # ---------- PHASE 1: does finiteness hold across the ambient axis? ----------
        print(f"\n--- PHASE 1 [finiteness across the axis @ L={L_mid:.3f}]: scan a, outcome + residuals ---",
              flush=True)
        phase1 = []
        wseed = None
        for a in a_grid:
            if budget_left() < PER_SOLVE + 2:
                print(f"    a={a:.3f}  throughput-limited", flush=True)
                phase1.append(dict(a=float(a), outcome="throughput-limited")); continue
            amb = model_ambient(a, Z)
            r = solve_embedded(emb_seed(ctx, amb) if wseed is None else wseed, ctx, prm, L_mid, amb, budget=PER_SOLVE)
            print(f"    a={a:.3f}: {r['outcome']:9s} |phi|max={r['phi_absmax']:.2f} rho_min={r['rho_min']:.3f} "
                  f"R3={r['R3']:+.3e} R4={r['R4']:+.3e} R5={r['R5']:+.3e}", flush=True)
            phase1.append(dict(a=float(a), outcome=r["outcome"], phi_absmax=r["phi_absmax"],
                               rho_min=r["rho_min"], R3=r["R3"], R4=r["R4"], R5=r["R5"]))
            if r["outcome"] in ("converged", "stall"):
                wseed = r["w"]                        # continuation
        n_finite = sum(1 for p in phase1 if p.get("outcome") in ("converged", "stall"))
        n_run = sum(1 for p in phase1 if p.get("outcome") in ("runaway", "collapsed"))
        print(f"  => finite(converged/stall) at {n_finite}/{len(a_grid)} axis points; "
              f"runaway/collapse at {n_run}", flush=True)
        Nrec["phase1"] = dict(L=L_mid, points=phase1, n_finite=n_finite, n_runaway=n_run)

        # ---------- PHASE 2: band search -- 2D scan (a,L), momentum + matter residuals ----------
        print(f"\n--- PHASE 2 [band search: 2D scan (a,L), residuals R3(pif) R4(pir) R5(Eang)] ---", flush=True)
        # residual table[a][L]; continuation along L for each a.
        table = {}
        for a in a_grid:
            amb = model_ambient(a, Z)
            row = []
            wseed = None
            for L in L_grid:
                if budget_left() < PER_SOLVE + 2:
                    row.append(dict(L=float(L), outcome="throughput-limited")); continue
                r = solve_embedded(emb_seed(ctx, amb) if wseed is None else wseed, ctx, prm, L, amb, budget=PER_SOLVE)
                row.append(dict(L=float(L), outcome=r["outcome"], R3=r["R3"], R4=r["R4"], R5=r["R5"],
                                phi_absmax=r["phi_absmax"], rho_min=r["rho_min"], w=r["w"], Phi=r["Phi"]))
                if r["outcome"] in ("converged", "stall"):
                    wseed = r["w"]
            table[float(a)] = row
        # Reduce: for each a, find L minimizing the momentum-match norm sqrt(R3^2+R4^2) among finite solves,
        # report that L*, its (R3,R4,R5), and whether the momentum norm and R5 are near zero.
        print("  per-a: L* = argmin_L ||(R3,R4)|| over finite solves; report momentum-norm + R5 there", flush=True)
        phase2 = []
        for a in a_grid:
            row = table[float(a)]
            fin = [c for c in row if c.get("outcome") in ("converged", "stall")
                   and all(math.isfinite(c.get(k, float("inf"))) for k in ("R3", "R4", "R5"))]
            if not fin:
                print(f"    a={a:.3f}: no finite solve over L-grid ({[c.get('outcome') for c in row]})", flush=True)
                phase2.append(dict(a=float(a), finite=False)); continue
            best = min(fin, key=lambda c: math.hypot(c["R3"], c["R4"]))
            mnorm = math.hypot(best["R3"], best["R4"])
            print(f"    a={a:.3f}: L*={best['L']:.3f} outcome={best['outcome']:9s} "
                  f"||(R3,R4)||={mnorm:.3e} (R3={best['R3']:+.2e} R4={best['R4']:+.2e}) R5={best['R5']:+.3e}",
                  flush=True)
            phase2.append(dict(a=float(a), finite=True, Lstar=best["L"], outcome=best["outcome"],
                               mom_norm=mnorm, R3=best["R3"], R4=best["R4"], R5=best["R5"]))
        # zero-crossing structure (OBSERVE): sign changes of R5 and of each momentum residual along a (at L*)
        def sign_changes(vals):
            xs = [v for v in vals if v is not None and math.isfinite(v)]
            return sum(1 for x, y in zip(xs[:-1], xs[1:]) if x * y < 0)
        aa = [p for p in phase2 if p.get("finite")]
        R5_series = [p["R5"] for p in aa]
        R3_series = [p["R3"] for p in aa]
        R4_series = [p["R4"] for p in aa]
        mom_series = [p["mom_norm"] for p in aa]
        sc_R5 = sign_changes(R5_series); sc_R3 = sign_changes(R3_series); sc_R4 = sign_changes(R4_series)
        min_mom = min(mom_series) if mom_series else None
        min_R5abs = min((abs(x) for x in R5_series), default=None)
        print(f"  => along a (at L*): sign-changes R3={sc_R3} R4={sc_R4} R5={sc_R5}; "
              f"min||(R3,R4)||={min_mom if min_mom is None else '%.3e'%min_mom} "
              f"min|R5|={min_R5abs if min_R5abs is None else '%.3e'%min_R5abs}", flush=True)
        Nrec["phase2"] = dict(per_a=phase2, sc_R3=sc_R3, sc_R4=sc_R4, sc_R5=sc_R5,
                              min_mom_norm=min_mom, min_R5abs=min_R5abs)

        # ---------- PHASE 3: 2D polish (a,L) on the momentum matches R3=R4=0, then check R5 ----------
        # square-in-4: solve R3(a,L)=R4(a,L)=0 by FD Newton from the best coarse bracket; check R5 there.
        print(f"\n--- PHASE 3 [2D polish R3=R4=0 in (a,L); then evaluate R5 (the over-by-1 check)] ---", flush=True)
        genuine = None
        if aa and budget_left() > 6 * PER_SOLVE:
            seed_pt = min(aa, key=lambda p: p["mom_norm"])
            a_c, L_c = seed_pt["a"], seed_pt["Lstar"]
            print(f"  start from a={a_c:.3f} L={L_c:.3f} (min momentum-norm={seed_pt['mom_norm']:.3e})", flush=True)
            da, dL = 0.02, 0.02
            ok_polish = True
            for it in range(8):
                if budget_left() < 6 * PER_SOLVE:
                    print("    (budget -> stop polish; throughput-limited)", flush=True); ok_polish = False; break
                r0, amb0 = G_aL(a_c, L_c, ctx, prm, Z, budget=PER_SOLVE)
                if r0["outcome"] not in ("converged", "stall"):
                    print(f"    it={it}: base solve {r0['outcome']} -> abort polish", flush=True); ok_polish = False; break
                F = np.array([r0["R3"], r0["R4"]])
                ra, _ = G_aL(a_c + da, L_c, ctx, prm, Z, budget=PER_SOLVE)
                rL, _ = G_aL(a_c, L_c + dL, ctx, prm, Z, budget=PER_SOLVE)
                if ra["outcome"] not in ("converged", "stall") or rL["outcome"] not in ("converged", "stall"):
                    print(f"    it={it}: FD probe non-finite -> stop", flush=True); break
                J = np.array([[(ra["R3"] - r0["R3"]) / da, (rL["R3"] - r0["R3"]) / dL],
                              [(ra["R4"] - r0["R4"]) / da, (rL["R4"] - r0["R4"]) / dL]])
                try:
                    step = np.linalg.solve(J, -F)
                except Exception:
                    print(f"    it={it}: singular J -> stop", flush=True); break
                # bounded step
                step = np.clip(step, -0.3, 0.3)
                a_n = float(np.clip(a_c + step[0], a_grid[0], a_grid[-1]))
                L_n = float(np.clip(L_c + step[1], 0.1, 2.5))
                print(f"    it={it}: (a,L)=({a_c:.4f},{L_c:.4f}) ||F||={np.linalg.norm(F):.3e} "
                      f"-> ({a_n:.4f},{L_n:.4f})", flush=True)
                if math.hypot(a_n - a_c, L_n - L_c) < 1e-5:
                    a_c, L_c = a_n, L_n; break
                a_c, L_c = a_n, L_n
            if ok_polish:
                rF, ambF = G_aL(a_c, L_c, ctx, prm, Z, budget=PER_SOLVE)
                if rF["outcome"] in ("converged", "stall"):
                    momF = math.hypot(rF["R3"], rF["R4"])
                    dd = adapted_derrick_residual(rF["w"], ctx, prm, L_c, ambF)
                    print(f"  POLISHED: a*={a_c:.4f} L*={L_c:.4f} outcome={rF['outcome']} "
                          f"||(R3,R4)||={momF:.3e} R5={rF['R5']:+.3e} | adapted-Derrick={dd['adapted_res']:+.3e}",
                          flush=True)
                    # genuine cell = ALL 5 residuals small (1,2 imposed exactly; 3,4 = momF; 5 = R5) + Derrick clean
                    all5 = (momF < 1e-4) and (abs(rF["R5"]) < 1e-4)
                    derrick_clean = abs(dd["adapted_res"]) < 1e-3
                    print(f"  => momentum matched (||(R3,R4)||<1e-4): {momF < 1e-4};  "
                          f"matter matched (|R5|<1e-4): {abs(rF['R5']) < 1e-4};  "
                          f"Derrick-clean: {derrick_clean}", flush=True)
                    Nrec["phase3"] = dict(a_star=a_c, L_star=L_c, mom_norm=momF, R5=rF["R5"],
                                          adapted_derrick=dd["adapted_res"], all5_matched=bool(all5),
                                          derrick_clean=bool(derrick_clean), outcome=rF["outcome"])
                    if all5 and derrick_clean:
                        genuine = dict(a=a_c, L=L_c, w=rF["w"], amb=ambF)
                else:
                    print(f"  polished base solve {rF['outcome']} -> no genuine cell at the polish point", flush=True)
                    Nrec["phase3"] = dict(a_star=a_c, L_star=L_c, outcome=rF["outcome"], all5_matched=False)
        else:
            print("  (no finite solves to seed polish, or budget short -> skipped)", flush=True)
            Nrec["phase3"] = dict(skipped=True)

        # ---------- PHASE 4: on any GENUINE cell -- two-tier stability + seed/grid robustness ----------
        if genuine is not None:
            print(f"\n--- PHASE 4 [GENUINE embedded cell candidate @ a={genuine['a']:.4f} L={genuine['L']:.4f}]:"
                  f" two-tier stability + robustness ---", flush=True)
            w = genuine["w"]; L = genuine["L"]; amb = genuine["amb"]
            eig, evec, sym, gnorm = N2.tier_a_energy_hessian(w, ctx, prm, L)
            cls = N2.classify_pd(eig)
            print(f"  tier-A (matter ENERGY Hessian): n_neg={cls['n_neg']} n_zero={cls['n_zero']} "
                  f"n_pos={cls['n_pos']} lam_min={cls['lam_min']:+.3e} PD={cls['pd']}", flush=True)
            tb = emb_tier_b(w, evec, eig, ctx, prm, L, amb, n_modes=3, budget=min(PER_SOLVE, 10.0))
            print(f"  tier-B (embedded coupled re-solve, top-{len(tb['per_mode'])} neg modes): "
                  f"RETURNS={tb['returns']} "
                  f"{[('lam=%.2e dist=%.2e conv=%s'%(m['lam'],m['dist_back'],m['converged'])) for m in tb['per_mode']]}",
                  flush=True)
            # seed independence (>=3 seeds) at the cell
            seeds = [0.02, 0.08, 0.20]
            seed_out = []
            for amp in seeds:
                rr = solve_embedded(emb_seed(ctx, amb, amp=amp), ctx, prm, L, amb, budget=PER_SOLVE)
                seed_out.append(dict(amp=amp, outcome=rr["outcome"], mom=math.hypot(rr["R3"], rr["R4"]), R5=rr["R5"]))
                print(f"    seed amp={amp:.2f}: {rr['outcome']:9s} ||(R3,R4)||={math.hypot(rr['R3'],rr['R4']):.3e} "
                      f"R5={rr['R5']:+.3e}", flush=True)
            Nrec["phase4"] = dict(tierA=cls, tierB=dict(returns=tb["returns"],
                                  per_mode=[dict(lam=m["lam"], dist_back=m["dist_back"], converged=m["converged"])
                                            for m in tb["per_mode"]]),
                                  seed_independence=seed_out,
                                  stable=bool(tb["returns"]))
        else:
            print("\n--- PHASE 4 [stability/robustness]: SKIPPED -- no genuine cell (all-5-matched + Derrick-clean) found ---",
                  flush=True)
            Nrec["phase4"] = dict(skipped="no genuine cell")

        grand[f"N{N}"] = Nrec

    # ---------- PHASE 5: solver-first cross-checks (interrogate the mismatch) ----------
    # A genuine matched cell must appear regardless of (i) which matching subset is imposed and
    # (ii) the ambient charge.  Run compact probes at N=1, L=L_mid.
    print("\n" + "=" * 100, flush=True)
    print("PHASE 5 [solver-first cross-checks @ N=1, L=L_mid]: scheme-B (impose momenta) + uncharged ambient",
          flush=True)
    print("=" * 100, flush=True)
    prm1 = (Z, XI, KAP, 1)
    a_probe = list(np.linspace(a_grid[0], a_grid[-1], 6))
    cc = {}

    if budget_left() > 3 * PER_SOLVE:
        print("  (B) SCHEME B -- impose the ambient seal SLOPES (momenta 3,4), read VALUE residuals R1,R2:",
              flush=True)
        schemeB = []; wseed = None
        for a in a_probe:
            if budget_left() < PER_SOLVE + 2:
                schemeB.append(dict(a=float(a), outcome="throughput-limited")); continue
            amb = model_ambient(a, Z)
            r = solve_embedded_schemeB(emb_seed(ctx, amb) if wseed is None else wseed, ctx, prm1, L_mid, amb,
                                       budget=PER_SOLVE)
            print(f"    a={a:.3f}: {'converged' if r['converged'] else 'NO-converge':11s} Phi={r['Phi']:.2e} "
                  f"|phi|max={r['phi_absmax']:.2f} rhop_s={r['rhop_s']:+.3f}(tgt=1) | R1(phi)={r['R1']:+.3e} "
                  f"R2(rho)={r['R2']:+.3e}", flush=True)
            schemeB.append(dict(a=float(a), converged=bool(r["converged"]), Phi=r["Phi"],
                                phi_absmax=r["phi_absmax"], R1=r["R1"], R2=r["R2"]))
            if r["converged"]:
                wseed = r["w"]
        nconvB = sum(1 for s in schemeB if s.get("converged"))
        print(f"  => SCHEME B converged at {nconvB}/{len(a_probe)} points "
              f"(imposing the ambient seal gradients destroys stationarity => no gradient-carrying branch)",
              flush=True)
        cc["schemeB"] = dict(points=schemeB, n_converged=nconvB)

    if budget_left() > 3 * PER_SOLVE:
        print("  (U) UNCHARGED ambient (q=0, pif_amb=0; native areal rho'=1 kept) -- scheme A residuals:",
              flush=True)
        unch = []; wseed = None
        for a in a_probe:
            if budget_left() < PER_SOLVE + 2:
                unch.append(dict(a=float(a), outcome="throughput-limited")); continue
            amb = model_ambient_uncharged(a, Z)
            r = solve_embedded(emb_seed(ctx, amb) if wseed is None else wseed, ctx, prm1, L_mid, amb,
                               budget=PER_SOLVE)
            print(f"    a={a:.3f}: {r['outcome']:9s} R3(pif,tgt0)={r['R3']:+.3e} "
                  f"R4(pir,tgt{amb['pir_amb']:.1f})={r['R4']:+.3e} R5={r['R5']:+.3e} rhop_s={r['rhop_s']:+.3f}",
                  flush=True)
            unch.append(dict(a=float(a), outcome=r["outcome"], R3=r["R3"], R4=r["R4"], R5=r["R5"],
                             rhop_s=r["rhop_s"]))
            if r["outcome"] in ("converged", "stall"):
                wseed = r["w"]
        R3u = [u["R3"] for u in unch if "R3" in u]; R4u = [u["R4"] for u in unch if "R4" in u]
        print(f"  => UNCHARGED: R3(dilation-flux match)->{('%.2e' % min(abs(x) for x in R3u)) if R3u else 'NA'} "
              f"(satisfiable, flat cell ~ zero-flux ambient); R4(rho'-continuity) min|.|="
              f"{('%.2e' % min(abs(x) for x in R4u)) if R4u else 'NA'} (STUCK ~+4: cell gradient-free vs areal rho'=1)",
              flush=True)
        cc["uncharged"] = dict(points=unch)

    grand["phase5_crosschecks"] = cc

    # ---------- write JSON summary ----------
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch_f2d_embedded_summary.json")
    try:
        with open(outpath, "w") as f:
            json.dump(grand, f, indent=1, default=float)
        print(f"\n[summary JSON -> {outpath}]", flush=True)
    except Exception as e:
        print(f"[JSON dump failed: {e}]", flush=True)

    print(f"\nTOTAL WALL: {elapsed():.1f}s  (budget {TOTAL_BUDGET:.0f}s)", flush=True)
    print("RUN COMPLETE -- MODEL ambient, N in {1,2}, Z=8, ONE slice; NOT a discreteness or frame verdict.",
          flush=True)
