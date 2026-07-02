"""cell_solver_f2d_classB_run.py -- the CLASS-B (charged/sourced-core) EMBEDDED finite-cell run.

THE DECISIVE TEST (strictly per the gated + blind-verified spec, embedded_classB_mini_MAP.md):
  The Class-A EMBEDDED run showed a smooth-MIRROR core forces pi_phi,c = 0 (gradient-free) so it
  cannot momentum-match a gradient-carrying ambient (the dilation-flux match R3 / the rho'-continuity
  match R4 got STUCK).  Class B replaces the inner MIRROR for phi with a CHARGED core:
      inner BC   pi_phi,c = (Z rho^2 phi')|_rc = q   (q a Newton unknown = the core dilation flux)
  while rho stays regular (pi_rho,c = 0, rho'_c = 0) and f keeps the pole/degree BCs.  This FREES
  phi'_c (== q via pi_phi = Z rho^2 phi'), adding ONE unknown.  Does q let the momentum-match CLOSE
  where the mirror core could not, and if so do cells appear at ISOLATED ambient values (a band)?

COUNTING (MAP sec.2; Ruling 1 + D1):  at FIXED ambient a the reduced unknowns are (phi_c, rho_c, q,
r_s) = 4 vs the 5 seal conditions (phi, rho, pi_phi, pi_rho continuous + E_ang,cell = m_amb) ->
OVER-by-1 -> cells only at ISOLATED a (the Misner-Sharp band), with q DETERMINED at each.  Equivalently
a-free -> 5 vs 5 -> SQUARE -> isolated (a,q) solutions.

NUMERICAL REALIZATION (declared):  at FIXED (a, L) the interior field BVP is made SQUARE in the
augmented unknown  w_cb = [phi(Nr), rho(Nr), u(Nr*Nth), q]  by imposing
   phi-ODE | pi_phi,c = q (inner, uses q) | phi_s = phi_amb (seal 1, Dirichlet)
   rho-ODE | rho'_c = 0 (inner)           | rho_s = rho_amb (seal 2, Dirichlet)
   f-PDE   | f_r,c = 0 | f_r,s = 0
   pi_phi,s = pi_phi,amb  (SEAL 3, the dilation-flux match -- consumes q; canon "external charge =
                           interior dilation flux through the seal": the seal flux DETERMINES q).
This is exactly one row more than the Class-A field solve (+ the pi_phi,s match) for exactly one more
unknown (q) -> SQUARE.  The LEFTOVER seal conditions are R4 = pi_rho,s - pi_rho,amb  and
R5 = E_ang,s - m_amb.  Two leftover residuals, two knobs (a, L) -> closing R4 = R5 = 0 gives ISOLATED
(a, L) points = the band, with q read off (D3: q = pi_phi,amb - INT 4 e^{-2phi} rho'^2 dr < pi_phi,amb).
(Realization = the OVER-BY-1 SCAN: at fixed a, scanning L can zero one leftover; the other is the
over-by-1 rejection, vanishing only at isolated a.)

THE FREE TEST (R4 ruling, MAP sec.3, CAS+blind-verified pi_rho' = Z rho phi'^2 - xi rho I_r +
kap N^2 I_4th/rho^3):  matching a gradient-carrying ambient with rho'_amb > 0 (=> pi_rho,amb < 0)
FORCES I_r > 0 (the winding MUST carry radial structure); where rho'_amb <= 0 (pi_rho,amb >= 0) the
>=0 non-I_r channels suffice so I_r may -> 0.  To probe BOTH signs we run a SECOND MODEL ambient whose
rho_amb(a) has a TURNING POINT (rho'_amb spans + -> 0 -> -) and check: I_r > 0 iff rho'_amb > 0?
SEED with I_r > 0 (V7: radial structure never appears on its own -- seed it, let the solver keep or
drop it).

ANTI-TARGETING: a band is the EXPECTATION -- it must be EARNED (all 5 residuals -> 0, adapted-Derrick
clean, two-tier stable, seed/grid robust), NOT declared.  NO closure, a CONTINUUM, or a FAILED
I_r-correlation are all first-class honest outcomes.  UNLABELED; no particle/mass labels.

REUSE (verbatim, per spec): operators from cell_solver_f2d (M); the seal-match machinery, MODEL
ambient, adapted-Derrick, seal_diagnostics from cell_solver_f2d_embedded_run (EMB); the two-tier
filter from cell_solver_f2d_N2 (N2); the LM solve / _w_to_v / PHI_CAP from first_build (FB).  Operators
NOT altered.

DISCIPLINE / ANTI-HANG: single clean unbuffered process; NO background; NO nohup.  Bounded (Nr<=24,
Nth<=28, iters<=150/solve, per-solve + hard total wall budget; throughput-limited recorded, never a
hang).  Fixed values tagged CHOSE/THEORY/MODEL.  MODEL ambient, N in {1,2}, one Z -- ONE slice.
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

import cell_solver_f2d as M                    # CAS-verified operators (REUSED verbatim)
import cell_solver_f2d_first_build as FB       # _w_to_v, lm_solve, PHI_CAP (REUSED)
import cell_solver_f2d_N2 as N2                # two-tier stability filter (REUSED)
import cell_solver_f2d_embedded_run as EMB     # MODEL ambient, seal_diagnostics, adapted-Derrick (REUSED)


# =========================================================================================
# SECOND MODEL AMBIENT (the free-test variant): rho_amb(a) with a TURNING POINT so rho'_amb
# spans BOTH signs.  DECLARED coarse rule, labeled MODEL; derived-universe value deferred.
#   radial family:  phi_A(r) = -q_A/r  (native-ish; pi_phi,amb = Z rho_A^2 q_A/r^2),
#                   rho_A(r) = R0 - c (r - r*)^2   (downward parabola; turning point at r=r*)
#   => rho'_A(r) = -2 c (r - r*):  > 0 for r < r*, = 0 at r*, < 0 for r > r*.
#   sample axis a = r (physical ambient radius).  m_amb = mu / rho_amb^2 (density-like in areal radius).
# MODEL CONSTANTS chosen round + rho_A>0 over the scan BEFORE any residual (anti-targeting).
# =========================================================================================
TURN_R0 = 1.5     # MODEL (parabola peak of rho_A)
TURN_C = 0.5      # MODEL (parabola curvature)
TURN_RSTAR = 1.2  # MODEL (turning-point radius; rho'_amb changes sign here)

def model_ambient_turn(a, Z, q=EMB.Q_AMB, mu=EMB.MU_AMB, R0=TURN_R0, c=TURN_C, rstar=TURN_RSTAR):
    """5 MODEL ambient numbers + DERIVED H_amb on the TURNING-POINT family, at axis a (=R_amb>0)."""
    phi_amb = -q / a
    rho_amb = R0 - c * (a - rstar) ** 2
    phip_amb = q / a ** 2
    rhop_amb = -2.0 * c * (a - rstar)                     # spans + -> 0 -> - as a crosses rstar
    pif_amb = Z * rho_amb ** 2 * phip_amb
    pir_amb = -4.0 * math.exp(-2.0 * phi_amb) * rhop_amb  # sign flips with rhop_amb at a=rstar
    m_amb = mu / rho_amb ** 2                             # MODEL density-like (areal); DECLARED
    H_geo = pif_amb ** 2 / (2.0 * Z * rho_amb ** 2) - pir_amb ** 2 * math.exp(2.0 * phi_amb) / 8.0 - 2.0
    H_amb = H_geo + m_amb
    return dict(a=float(a), phi_amb=float(phi_amb), rho_amb=float(rho_amb),
                pif_amb=float(pif_amb), pir_amb=float(pir_amb), m_amb=float(m_amb),
                H_geo=float(H_geo), H_amb=float(H_amb),
                phip_amb=float(phip_amb), rhop_amb=float(rhop_amb))


# =========================================================================================
# CLASS-B AUGMENTED PACK:  w_cb = [ w (=2Nr+Nr*Nth) , q ]   (q appended as the last slot)
# =========================================================================================
def cb_split(w_cb):
    return w_cb[:-1], w_cb[-1]

def cb_seed(ctx, amb, amp=0.05, q0=None):
    """Class-B seed: EMB reduced seed (phi~phi_amb, rho~rho_amb, band-limited radial u activating
    I_r>0) with q appended.  q0 default = pif_amb (D3: q <= pi_phi,amb; a good start).  All CHOSE."""
    w = EMB.emb_seed(ctx, amb, amp=amp)
    if q0 is None:
        q0 = amb["pif_amb"]
    return torch.cat([w, torch.as_tensor([float(q0)], dtype=torch.float64)])


# =========================================================================================
# CLASS-B EMBEDDED FIELD RESIDUAL  (SQUARE in w_cb at fixed (a,L))
#   rows: phi-ODE | pi_phi,c=q | phi_s=phi_amb | rho-ODE | rho'_c=0 | rho_s=rho_amb
#         | f-PDE | f_r,c=0 | f_r,s=0 | pi_phi,s = pi_phi,amb  (consumes q)
# =========================================================================================
def residual_classB(w_cb, ctx, prm, L, amb, wbc=1.0):
    Z = prm[0]
    w, q = cb_split(w_cb)
    Q = M.fields(FB._w_to_v(w, ctx, L), ctx, prm)
    phi, rho, phip, rhop, fr = Q["phi"], Q["rho"], Q["phip"], Q["rhop"], Q["fr"]
    pif_c = Z * rho[0] ** 2 * phip[0]                     # pi_phi at the core
    pif_s = Z * rho[-1] ** 2 * phip[-1]                   # pi_phi at the seal
    rows = [
        Q["phi_ode"][1:-1],                                  # phi-ODE interior
        wbc * (pif_c - q).reshape(1),                        # CHARGED core: pi_phi,c = q (frees phi'_c)
        wbc * (phi[[-1]] - amb["phi_amb"]),                  # phi_s = phi_amb  (seal 1, Dirichlet)
        Q["rho_ode"][1:-1],                                  # rho-ODE interior
        wbc * rhop[[0]],                                     # rho'_c = 0  (regular rho core)
        wbc * (rho[[-1]] - amb["rho_amb"]),                  # rho_s = rho_amb  (seal 2, Dirichlet)
        Q["res_f"][1:-1].reshape(-1),                        # f-PDE interior
        wbc * fr[0, :],                                      # f_r,c = 0  (pole/degree carried by ramp)
        wbc * fr[-1, :],                                     # f_r,s = 0  (natural BC; E_ang point)
        wbc * (pif_s - amb["pif_amb"]).reshape(1),           # SEAL 3: pi_phi,s match -> DETERMINES q
    ]
    return torch.cat([r.reshape(-1) for r in rows])


def seal_diag_classB(w_cb, ctx, prm, L, amb):
    """Leftover matching residuals + q + I_r structure at the solved Class-B config.
       R3 = pi_phi,s - pi_phi,amb (IMPOSED, ~0 -- reported as a check)
       R4 = pi_rho,s - pi_rho,amb (LEFTOVER)
       R5 = E_ang,s - m_amb       (LEFTOVER)
       Ir_int = INT I_r dr ,  Ir_max = max_r I_r  (radial-structure diagnostics; the free test)."""
    Z, XI, KAP, N = prm
    w, q = cb_split(w_cb)
    v = FB._w_to_v(w, ctx, L)
    Q = M.fields(v, ctx, prm)
    phi, rho, phip, rhop = Q["phi"], Q["rho"], Q["phip"], Q["rhop"]
    e2m = Q["e2m"]; Ith, Is, I4th, Ir = Q["Ith"], Q["Is"], Q["I4th"], Q["Ir"]
    rho_s = rho[-1]
    pif_s = Z * rho_s ** 2 * phip[-1]
    pif_c = Z * rho[0] ** 2 * phip[0]
    pir_s = -4.0 * e2m[-1] * rhop[-1]
    Eang_s = (XI / 2.0) * (Ith[-1] + N ** 2 * Is[-1]) + (KAP * N ** 2 / 2.0) * I4th[-1] / rho_s ** 2
    Ir_int = float((ctx["ccw"] * Ir).sum() * (float(L) / 2.0))
    return dict(R3=float(pif_s) - amb["pif_amb"], R4=float(pir_s) - amb["pir_amb"],
                R5=float(Eang_s) - amb["m_amb"], q=float(q), pif_c=float(pif_c), pif_s=float(pif_s),
                pir_s=float(pir_s), Eang_s=float(Eang_s), phi_s=float(phi[-1]), rho_s=float(rho_s),
                phip_s=float(phip[-1]), rhop_s=float(rhop[-1]), phip_c=float(phip[0]),
                Ir_int=Ir_int, Ir_max=float(Ir.abs().max()), Ir_seal=float(Ir[-1]),
                rhop_amb=amb["rhop_amb"])


def solve_classB(w0, ctx, prm, L, amb, wbc=1.0, maxit=140, tol=1e-13, budget=8.0):
    """Relax the SQUARE Class-B embedded BVP at fixed (a,L).  Honest gate identical in spirit to
    EMB.solve_embedded (Phi<tol AND iters<maxit AND |phi| bounded AND rho>0)."""
    resfn = lambda ww: residual_classB(ww, ctx, prm, L, amb, wbc=wbc)
    w_cb, Phi, iters, wall = FB.lm_solve(resfn, w0, maxit=maxit, tol=tol, time_budget=budget)
    w, q = cb_split(w_cb)
    v = FB._w_to_v(w, ctx, L)
    phi, rho, uf, _ = M.unpack(v, ctx)
    finite = bool(torch.isfinite(w_cb).all())
    rho_min = float(rho.min()); phi_absmax = float(phi.abs().max())
    stalled = (iters >= maxit)
    collapsed = (rho_min <= 1e-4) or (not finite)
    runaway = (phi_absmax >= FB.PHI_CAP)
    converged = (Phi < 1e-11) and finite and (rho_min > 1e-4) and (not stalled) and (not runaway)
    outcome = ("converged" if converged else "collapsed" if collapsed
               else "runaway" if runaway else "stall")
    sd = seal_diag_classB(w_cb, ctx, prm, L, amb)
    return dict(w_cb=w_cb, w=w, Phi=float(Phi), iters=int(iters), wall=float(wall),
                converged=converged, collapsed=collapsed, runaway=runaway, stalled=stalled,
                rho_min=rho_min, phi_absmax=phi_absmax, outcome=outcome, **sd)


# =========================================================================================
# adapted Derrick (Ruling 2), REUSED from EMB (takes w WITHOUT q -> pass w_cb[:-1]).
# =========================================================================================
def adapted_derrick_classB(w_cb, ctx, prm, L, amb):
    w, _ = cb_split(w_cb)
    return EMB.adapted_derrick_residual(w, ctx, prm, L, amb)


# =========================================================================================
# tier-b (constraint-respecting coupled re-solve of the Class-B BVP along matter neg-modes)
# =========================================================================================
def cb_resolve_negmode(w_cb_star, v_neg_matter, ctx, prm, L, amb, delta=0.05, budget=10.0):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    vn = v_neg_matter / (v_neg_matter.norm() + 1e-30)
    # embed matter eigenvector into w (zeros for phi,rho); keep q slot unperturbed
    full = torch.cat([torch.zeros(2 * Nr, dtype=torch.float64), vn,
                      torch.zeros(1, dtype=torch.float64)])
    scale = float(w_cb_star.norm()) + 1e-30
    w_pert = w_cb_star + delta * scale * full
    r = solve_classB(w_pert, ctx, prm, L, amb, budget=budget)
    dist_back = float((r["w_cb"] - w_cb_star).norm() / scale)
    return dict(converged=r["converged"], dist_back=dist_back, Phi=r["Phi"], collapsed=r["collapsed"])


def cb_tier_b(w_cb, evec, eig, ctx, prm, L, amb, n_modes=3, delta=0.05, budget=10.0):
    n_neg = int((eig < 0).sum())
    ks = list(range(min(n_modes, max(n_neg, 1))))
    results = []
    for k in ks:
        rr = cb_resolve_negmode(w_cb, evec[:, k].detach(), ctx, prm, L, amb, delta=delta, budget=budget)
        rr["lam"] = float(eig[k]); results.append(rr)
    returns = all(m["converged"] and m["dist_back"] < 0.1 and not m["collapsed"] for m in results)
    return dict(per_mode=results, returns=returns)


# =========================================================================================
# 2D leftover-residual accessor G(a,L) = (R4, R5) via a nested Class-B field solve.
# =========================================================================================
def G_aL(a, L, ctx, prm, Z, amb_fn, budget=8.0, wseed=None):
    amb = amb_fn(a, Z)
    w0 = cb_seed(ctx, amb) if wseed is None else wseed
    r = solve_classB(w0, ctx, prm, L, amb, budget=budget)
    return r, amb


# =========================================================================================
# ONE (N) run over a given MODEL ambient (base or turning); phases 0-4.
# =========================================================================================
def run_N(N, Z, XI, KAP, ctx, a_grid, L_grid, amb_fn, label, budget_left, PER_SOLVE, tag=""):
    prm = (Z, XI, KAP, N)
    a_mid = float(np.median(a_grid)); L_mid = float(np.median(L_grid))
    rec = {}
    print("\n" + "#" * 100, flush=True)
    print(f"### N={N}  Z={Z}  xi=kap=1  |  MODEL AMBIENT = {label}  {tag} ###", flush=True)
    print("#" * 100, flush=True)

    amb_mid = amb_fn(a_mid, Z)
    print(f"[MODEL ambient @ a_mid={a_mid:.3f}]: phi={amb_mid['phi_amb']:+.4f} rho={amb_mid['rho_amb']:.4f} "
          f"pif={amb_mid['pif_amb']:+.4f} pir={amb_mid['pir_amb']:+.4f} m={amb_mid['m_amb']:.4f} "
          f"rhop_amb={amb_mid['rhop_amb']:+.3f} -> H_amb={amb_mid['H_amb']:+.4f}", flush=True)

    # ---- PHASE 0: does q RESCUE the momentum-match the Class-A mirror failed? ----
    print(f"\n--- PHASE 0 [KEY QUESTION @ a={a_mid:.3f}, L={L_mid:.3f}]: Class-B charged core vs Class-A mirror ---",
          flush=True)
    r_cb = solve_classB(cb_seed(ctx, amb_mid), ctx, prm, L_mid, amb_mid, budget=PER_SOLVE)
    # Class-A mirror reference at the SAME point (EMB.solve_embedded imposes phi'_c=0, reads R3 off)
    r_ca = EMB.solve_embedded(EMB.emb_seed(ctx, amb_mid), ctx, prm, L_mid, amb_mid, budget=PER_SOLVE)
    print(f"  CLASS-B: outcome={r_cb['outcome']:9s} Phi={r_cb['Phi']:.2e} it={r_cb['iters']} "
          f"q={r_cb['q']:+.4f} | R3(pif,IMPOSED)={r_cb['R3']:+.2e} R4(pir)={r_cb['R4']:+.3e} "
          f"R5(Eang)={r_cb['R5']:+.3e} | I_r_int={r_cb['Ir_int']:.3e}", flush=True)
    print(f"  CLASS-A: outcome={r_ca['outcome']:9s} Phi={r_ca['Phi']:.2e} "
          f"| R3(pif,READ-OFF)={r_ca['R3']:+.3e} R4(pir)={r_ca['R4']:+.3e} R5(Eang)={r_ca['R5']:+.3e}",
          flush=True)
    q_rescues = (r_cb["outcome"] in ("converged", "stall")) and (abs(r_cb["R3"]) < 1e-6)
    print(f"  => q CLOSES the pi_phi match (R3->0, feasible field solve): {q_rescues}  "
          f"(Class-A mirror R3 stuck at {r_ca['R3']:+.3e})", flush=True)
    rec["phase0"] = dict(a=a_mid, L=L_mid, classB=dict(outcome=r_cb["outcome"], q=r_cb["q"],
                         R3=r_cb["R3"], R4=r_cb["R4"], R5=r_cb["R5"], Ir_int=r_cb["Ir_int"]),
                         classA=dict(outcome=r_ca["outcome"], R3=r_ca["R3"], R4=r_ca["R4"], R5=r_ca["R5"]),
                         q_rescues=bool(q_rescues))

    # ---- PHASE 1: residual structure vs a (at L_mid) -- outcome, R4, R5, q, I_r, sign(rho'_amb) ----
    print(f"\n--- PHASE 1 [residual structure vs a @ L={L_mid:.3f}]: R4,R5,q,I_r + sign(rho'_amb) ---",
          flush=True)
    phase1 = []; wseed = None
    for a in a_grid:
        if budget_left() < PER_SOLVE + 2:
            print(f"    a={a:.3f}  throughput-limited", flush=True)
            phase1.append(dict(a=float(a), outcome="throughput-limited")); continue
        amb = amb_fn(a, Z)
        r = solve_classB(cb_seed(ctx, amb) if wseed is None else wseed, ctx, prm, L_mid, amb, budget=PER_SOLVE)
        sgn = "+" if amb["rhop_amb"] > 0 else ("0" if amb["rhop_amb"] == 0 else "-")
        print(f"    a={a:.3f}: {r['outcome']:9s} q={r['q']:+.3f} R3={r['R3']:+.1e} R4={r['R4']:+.3e} "
              f"R5={r['R5']:+.3e} | rhop_amb={amb['rhop_amb']:+.2f}({sgn}) I_r_int={r['Ir_int']:.3e} "
              f"I_r_max={r['Ir_max']:.3e}", flush=True)
        phase1.append(dict(a=float(a), outcome=r["outcome"], q=r["q"], R3=r["R3"], R4=r["R4"], R5=r["R5"],
                           rhop_amb=amb["rhop_amb"], Ir_int=r["Ir_int"], Ir_max=r["Ir_max"],
                           phi_absmax=r["phi_absmax"], rho_min=r["rho_min"]))
        if r["outcome"] in ("converged", "stall"):
            wseed = r["w_cb"]
    n_fin = sum(1 for p in phase1 if p.get("outcome") in ("converged", "stall"))
    rec["phase1"] = dict(L=L_mid, points=phase1, n_finite=n_fin)

    # ---- PHASE 2: 2D band search -- for each a, L*=argmin_L ||(R4,R5)|| over finite solves ----
    print(f"\n--- PHASE 2 [band search: 2D scan (a,L); leftover residuals R4(pir) R5(Eang)] ---", flush=True)
    table = {}
    for a in a_grid:
        amb = amb_fn(a, Z); row = []; wseed = None
        for L in L_grid:
            if budget_left() < PER_SOLVE + 2:
                row.append(dict(L=float(L), outcome="throughput-limited")); continue
            r = solve_classB(cb_seed(ctx, amb) if wseed is None else wseed, ctx, prm, L, amb, budget=PER_SOLVE)
            row.append(dict(L=float(L), outcome=r["outcome"], R4=r["R4"], R5=r["R5"], q=r["q"],
                            Ir_int=r["Ir_int"], w_cb=r["w_cb"], phi_absmax=r["phi_absmax"], rho_min=r["rho_min"]))
            if r["outcome"] in ("converged", "stall"):
                wseed = r["w_cb"]
        table[float(a)] = row
    phase2 = []
    for a in a_grid:
        row = table[float(a)]
        fin = [c for c in row if c.get("outcome") in ("converged", "stall")
               and all(math.isfinite(c.get(k, float("inf"))) for k in ("R4", "R5"))]
        if not fin:
            print(f"    a={a:.3f}: no finite solve over L-grid ({[c.get('outcome') for c in row]})", flush=True)
            phase2.append(dict(a=float(a), finite=False)); continue
        best = min(fin, key=lambda c: math.hypot(c["R4"], c["R5"]))
        lnorm = math.hypot(best["R4"], best["R5"])
        amb = amb_fn(a, Z)
        print(f"    a={a:.3f}: L*={best['L']:.3f} {best['outcome']:9s} ||(R4,R5)||={lnorm:.3e} "
              f"(R4={best['R4']:+.2e} R5={best['R5']:+.2e}) q={best['q']:+.3f} "
              f"rhop_amb={amb['rhop_amb']:+.2f} I_r_int={best['Ir_int']:.3e}", flush=True)
        phase2.append(dict(a=float(a), finite=True, Lstar=best["L"], outcome=best["outcome"],
                           leftover_norm=lnorm, R4=best["R4"], R5=best["R5"], q=best["q"],
                           Ir_int=best["Ir_int"], rhop_amb=amb["rhop_amb"]))
    def sign_changes(vals):
        xs = [v for v in vals if v is not None and math.isfinite(v)]
        return sum(1 for x, y in zip(xs[:-1], xs[1:]) if x * y < 0)
    aa = [p for p in phase2 if p.get("finite")]
    sc_R4 = sign_changes([p["R4"] for p in aa]); sc_R5 = sign_changes([p["R5"] for p in aa])
    min_norm = min((p["leftover_norm"] for p in aa), default=None)
    print(f"  => along a (at L*): sign-changes R4={sc_R4} R5={sc_R5}; "
          f"min||(R4,R5)||={min_norm if min_norm is None else '%.3e' % min_norm} "
          f"(isolated closures = band candidates)", flush=True)
    rec["phase2"] = dict(per_a=phase2, sc_R4=sc_R4, sc_R5=sc_R5, min_leftover_norm=min_norm)

    # ---- PHASE 3: 2D polish R4=R5=0 in (a,L) from the best coarse bracket; then all-5 + Derrick ----
    print(f"\n--- PHASE 3 [2D polish R4=R5=0 in (a,L); check all-5 matched + adapted-Derrick] ---", flush=True)
    genuine = None
    if aa and budget_left() > 6 * PER_SOLVE:
        seed_pt = min(aa, key=lambda p: p["leftover_norm"])
        a_c, L_c = seed_pt["a"], seed_pt["Lstar"]
        print(f"  start from a={a_c:.3f} L={L_c:.3f} (min ||(R4,R5)||={seed_pt['leftover_norm']:.3e})", flush=True)
        da, dL = 0.02, 0.02; ok_polish = True
        for it in range(8):
            if budget_left() < 6 * PER_SOLVE:
                print("    (budget -> stop polish; throughput-limited)", flush=True); ok_polish = False; break
            r0, amb0 = G_aL(a_c, L_c, ctx, prm, Z, amb_fn, budget=PER_SOLVE)
            if r0["outcome"] not in ("converged", "stall"):
                print(f"    it={it}: base solve {r0['outcome']} -> abort polish", flush=True); ok_polish = False; break
            F = np.array([r0["R4"], r0["R5"]])
            ra, _ = G_aL(a_c + da, L_c, ctx, prm, Z, amb_fn, budget=PER_SOLVE)
            rL, _ = G_aL(a_c, L_c + dL, ctx, prm, Z, amb_fn, budget=PER_SOLVE)
            if ra["outcome"] not in ("converged", "stall") or rL["outcome"] not in ("converged", "stall"):
                print(f"    it={it}: FD probe non-finite -> stop", flush=True); break
            J = np.array([[(ra["R4"] - r0["R4"]) / da, (rL["R4"] - r0["R4"]) / dL],
                          [(ra["R5"] - r0["R5"]) / da, (rL["R5"] - r0["R5"]) / dL]])
            try:
                step = np.linalg.solve(J, -F)
            except Exception:
                print(f"    it={it}: singular J -> stop", flush=True); break
            step = np.clip(step, -0.3, 0.3)
            a_n = float(np.clip(a_c + step[0], a_grid[0], a_grid[-1]))
            L_n = float(np.clip(L_c + step[1], 0.1, 2.5))
            print(f"    it={it}: (a,L)=({a_c:.4f},{L_c:.4f}) ||F||={np.linalg.norm(F):.3e} -> ({a_n:.4f},{L_n:.4f})",
                  flush=True)
            done = math.hypot(a_n - a_c, L_n - L_c) < 1e-5
            a_c, L_c = a_n, L_n
            if done:
                break
        if ok_polish:
            rF, ambF = G_aL(a_c, L_c, ctx, prm, Z, amb_fn, budget=PER_SOLVE)
            if rF["outcome"] in ("converged", "stall"):
                leftF = math.hypot(rF["R4"], rF["R5"])
                dd = adapted_derrick_classB(rF["w_cb"], ctx, prm, L_c, ambF)
                all5 = (abs(rF["R3"]) < 1e-4) and (leftF < 1e-4)
                derrick_clean = abs(dd["adapted_res"]) < 1e-3
                print(f"  POLISHED: a*={a_c:.4f} L*={L_c:.4f} {rF['outcome']} q={rF['q']:+.4f} "
                      f"R3={rF['R3']:+.1e} ||(R4,R5)||={leftF:.3e} | adapted-Derrick={dd['adapted_res']:+.3e} "
                      f"| I_r_int={rF['Ir_int']:.3e} rhop_amb={ambF['rhop_amb']:+.2f}", flush=True)
                print(f"  => all-5 matched (|R3|,||(R4,R5)||<1e-4): {all5};  Derrick-clean: {derrick_clean}",
                      flush=True)
                rec["phase3"] = dict(a_star=a_c, L_star=L_c, q=rF["q"], R3=rF["R3"], leftover_norm=leftF,
                                     adapted_derrick=dd["adapted_res"], all5_matched=bool(all5),
                                     derrick_clean=bool(derrick_clean), outcome=rF["outcome"],
                                     Ir_int=rF["Ir_int"], rhop_amb=ambF["rhop_amb"],
                                     phi_c=float(rF["w"][0]), rho_c=float(rF["w"][ctx["Nr"]]))
                if all5 and derrick_clean:
                    genuine = dict(a=a_c, L=L_c, w_cb=rF["w_cb"], amb=ambF, q=rF["q"], Ir_int=rF["Ir_int"],
                                   rhop_amb=ambF["rhop_amb"])
            else:
                print(f"  polished base solve {rF['outcome']} -> no genuine cell at the polish point", flush=True)
                rec["phase3"] = dict(a_star=a_c, L_star=L_c, outcome=rF["outcome"], all5_matched=False)
    else:
        print("  (no finite solves to seed polish, or budget short -> skipped)", flush=True)
        rec["phase3"] = dict(skipped=True)

    # ---- PHASE 4: on any GENUINE cell -- two-tier stability + seed/grid robustness + free test ----
    if genuine is not None:
        print(f"\n--- PHASE 4 [GENUINE Class-B cell @ a={genuine['a']:.4f} L={genuine['L']:.4f} "
              f"q={genuine['q']:+.4f}]: two-tier stability + robustness ---", flush=True)
        w_cb = genuine["w_cb"]; w = w_cb[:-1]; L = genuine["L"]; amb = genuine["amb"]
        eig, evec, sym, gnorm = N2.tier_a_energy_hessian(w, ctx, prm, L)
        cls = N2.classify_pd(eig)
        print(f"  tier-A (matter ENERGY Hessian): n_neg={cls['n_neg']} n_zero={cls['n_zero']} "
              f"n_pos={cls['n_pos']} lam_min={cls['lam_min']:+.3e} PD={cls['pd']}", flush=True)
        tb = cb_tier_b(w_cb, evec, eig, ctx, prm, L, amb, n_modes=3, budget=min(PER_SOLVE, 10.0))
        print(f"  tier-B (Class-B coupled re-solve, top-{len(tb['per_mode'])} neg modes): RETURNS={tb['returns']} "
              f"{[('lam=%.2e dist=%.2e conv=%s' % (m['lam'], m['dist_back'], m['converged'])) for m in tb['per_mode']]}",
              flush=True)
        seeds = [0.02, 0.08, 0.20]; seed_out = []
        for amp in seeds:
            rr = solve_classB(cb_seed(ctx, amb, amp=amp), ctx, prm, L, amb, budget=PER_SOLVE)
            seed_out.append(dict(amp=amp, outcome=rr["outcome"], left=math.hypot(rr["R4"], rr["R5"]),
                                 q=rr["q"], Ir_int=rr["Ir_int"]))
            print(f"    seed amp={amp:.2f}: {rr['outcome']:9s} ||(R4,R5)||={math.hypot(rr['R4'], rr['R5']):.3e} "
                  f"q={rr['q']:+.3f} I_r_int={rr['Ir_int']:.3e}", flush=True)
        print(f"  FREE TEST @ this cell: rhop_amb={genuine['rhop_amb']:+.3f} -> I_r_int={genuine['Ir_int']:.3e} "
              f"({'I_r>0 present' if genuine['Ir_int'] > 1e-6 else 'I_r~0'}); "
              f"ruling: rhop_amb>0 MUST carry I_r>0", flush=True)
        rec["phase4"] = dict(tierA=cls, tierB=dict(returns=tb["returns"],
                             per_mode=[dict(lam=m["lam"], dist_back=m["dist_back"], converged=m["converged"])
                                       for m in tb["per_mode"]]),
                             seed_independence=seed_out, stable=bool(tb["returns"]),
                             Ir_int=genuine["Ir_int"], rhop_amb=genuine["rhop_amb"])
    else:
        print("\n--- PHASE 4 [stability/robustness]: SKIPPED -- no genuine cell (all-5 + Derrick-clean) ---",
              flush=True)
        rec["phase4"] = dict(skipped="no genuine cell")
    return rec


# =========================================================================================
# FREE TEST (dedicated): scan a across the TURNING point, tabulate I_r vs sign(rho'_amb).
# =========================================================================================
def free_test_scan(N, Z, XI, KAP, ctx, a_grid, L_grid, budget_left, PER_SOLVE):
    prm = (Z, XI, KAP, N)
    print("\n" + "=" * 100, flush=True)
    print(f"FREE TEST [N={N}] -- TURNING-POINT MODEL ambient (rho'_amb spans +/-): I_r vs sign(rho'_amb).", flush=True)
    print(f"  ruling: a matched cell MUST carry I_r>0 where rho'_amb>0 (a<rstar={TURN_RSTAR}); "
          f"I_r may ->0 where rho'_amb<=0 (a>=rstar).  Seed I_r>0 everywhere; solver keeps/drops it.", flush=True)
    print("=" * 100, flush=True)
    rows = []
    for a in a_grid:
        amb = model_ambient_turn(a, Z)
        if budget_left() < PER_SOLVE + 2:
            print(f"    a={a:.3f}  throughput-limited", flush=True)
            rows.append(dict(a=float(a), outcome="throughput-limited")); continue
        # best L over the L-grid (min leftover ||(R4,R5)||) among finite solves
        best = None; wseed = None
        for L in L_grid:
            if budget_left() < PER_SOLVE + 2:
                break
            r = solve_classB(cb_seed(ctx, amb) if wseed is None else wseed, ctx, prm, L, amb, budget=PER_SOLVE)
            if r["outcome"] in ("converged", "stall"):
                wseed = r["w_cb"]
                ln = math.hypot(r["R4"], r["R5"])
                if best is None or ln < best["left"]:
                    best = dict(L=float(L), left=ln, R4=r["R4"], R5=r["R5"], q=r["q"],
                                Ir_int=r["Ir_int"], Ir_max=r["Ir_max"], outcome=r["outcome"])
        sgn = "+" if amb["rhop_amb"] > 1e-9 else ("0" if abs(amb["rhop_amb"]) <= 1e-9 else "-")
        if best is None:
            print(f"    a={a:.3f}: rhop_amb={amb['rhop_amb']:+.3f}({sgn}) -> NO finite solve", flush=True)
            rows.append(dict(a=float(a), rhop_amb=amb["rhop_amb"], sign=sgn, outcome="no-finite")); continue
        print(f"    a={a:.3f}: rhop_amb={amb['rhop_amb']:+.3f}({sgn}) | L*={best['L']:.3f} "
              f"||(R4,R5)||={best['left']:.3e} q={best['q']:+.3f} I_r_int={best['Ir_int']:.3e} "
              f"I_r_max={best['Ir_max']:.3e}", flush=True)
        rows.append(dict(a=float(a), rhop_amb=amb["rhop_amb"], sign=sgn, L=best["L"],
                         leftover_norm=best["left"], q=best["q"], Ir_int=best["Ir_int"],
                         Ir_max=best["Ir_max"], outcome=best["outcome"]))
    # OBSERVE (do NOT target).  The R4 ruling is a statement about MATCHED (closed) cells: a matched
    # cell with rho'_amb>0 MUST carry I_r>0.  So the test is only meaningful on genuinely CLOSED cells
    # (||(R4,R5)||->0).  Report closures FIRST; only assess the correlation on them.  With NO closed
    # cell the test is VACUOUS -- but the I_r data are still recorded and read against the ruling's
    # CONTRAPOSITIVE (I_r~0 => the pi_rho match cannot close where rho'_amb>0).
    CLOSE_TOL = 1e-4; IR_THRESH = 1e-6
    closed = [r for r in rows if r.get("leftover_norm") is not None and r["leftover_norm"] < CLOSE_TOL]
    pos = [r["Ir_int"] for r in rows if r.get("sign") == "+" and "Ir_int" in r]
    neg = [r["Ir_int"] for r in rows if r.get("sign") == "-" and "Ir_int" in r]
    min_norm = min((r["leftover_norm"] for r in rows if r.get("leftover_norm") is not None), default=None)
    print(f"  => matched (closed, ||(R4,R5)||<{CLOSE_TOL:.0e}) cells: {len(closed)}  "
          f"(min ||(R4,R5)|| over scan = {min_norm if min_norm is None else '%.3e' % min_norm})", flush=True)
    if pos:
        print(f"     I_r_int on rho'_amb>0 best-L points: [{min(pos):.2e},{max(pos):.2e}] "
              f"(all>{IR_THRESH:.0e}: {all(x > IR_THRESH for x in pos)})", flush=True)
    if neg:
        print(f"     I_r_int on rho'_amb<0 best-L points: [{min(neg):.2e},{max(neg):.2e}]", flush=True)
    if closed:
        pc = [r for r in closed if r.get("sign") == "+"]
        pos_carry = all(r["Ir_int"] > IR_THRESH for r in pc) if pc else None
        print(f"     FREE TEST (on {len(closed)} matched cells): rho'_amb>0 closures carry I_r>0: {pos_carry}",
              flush=True)
        verdict = "PASS" if pos_carry else ("VACUOUS(no rho'>0 closure)" if pc == [] else "FAILED")
    else:
        print(f"     FREE TEST VACUOUS: no matched cell in scan.  I_r stays ~0 on the rho'_amb>0 branch "
              f"=> pi_rho match cannot close there -- CONSISTENT with the ruling's contrapositive.", flush=True)
        verdict = "VACUOUS(no closure)"
    print(f"     verdict: {verdict}", flush=True)
    corr = dict(n_closed=len(closed), min_norm=min_norm, verdict=verdict,
                pos_Ir_range=[min(pos), max(pos)] if pos else None,
                neg_Ir_range=[min(neg), max(neg)] if neg else None)
    return dict(rows=rows, correlation=corr)


# =========================================================================================
# MAIN (single process, unbuffered, bounded)
# =========================================================================================
if __name__ == "__main__":
    T0 = time.time()
    TOTAL_BUDGET = float(os.environ.get("CB_TOTAL_BUDGET", "1400"))   # hard total wall (s)
    PER_SOLVE = float(os.environ.get("CB_PER_SOLVE", "8"))            # per-solve wall (s)
    Nr = int(os.environ.get("CB_NR", "16"))                          # CHOSE bounded grid (<=24)
    Nth = int(os.environ.get("CB_NTH", "12"))                        # CHOSE bounded grid (<=28)
    Z = 8.0                                                          # CHOSE-fixed (Route-A; OBS-2)
    XI = 1.0; KAP = 1.0                                              # CHOSE-units
    N_LIST = [1, 2]                                                  # DERIVED-topological (this slice)
    a_grid = list(np.linspace(0.55, 2.0, 9))                        # CHOSE ambient-axis scan (R_amb>0)
    L_grid = list(np.linspace(0.30, 1.60, 6))                       # CHOSE cell-length scan
    a_turn = list(np.linspace(0.55, 2.0, 9))                        # CHOSE free-test axis (crosses rstar=1.2)

    def elapsed():
        return time.time() - T0
    def budget_left():
        return TOTAL_BUDGET - elapsed()

    print("=" * 100, flush=True)
    print("CLASS-B (charged/sourced-core) EMBEDDED finite-cell run -- MODEL ambient, N in {1,2}, Z=8, xi=kap=1.",
          flush=True)
    print("Charged core: pi_phi,c=q (q free); rho regular (rho'_c=0); over-by-1 at fixed a -> band, q determined.",
          flush=True)
    print(f"MODEL base ambient: phi_A=-q/r, rho_A=r (rho'_amb=+1 single-signed); q={EMB.Q_AMB} mu={EMB.MU_AMB}.",
          flush=True)
    print(f"MODEL turning ambient (free test): rho_A=R0-c(r-r*)^2, R0={TURN_R0} c={TURN_C} r*={TURN_RSTAR} "
          f"(rho'_amb spans +/-).", flush=True)
    print(f"grid Nr={Nr} Nth={Nth}; a_grid=[{a_grid[0]:.2f}..{a_grid[-1]:.2f}]x{len(a_grid)}; "
          f"L_grid=[{L_grid[0]:.2f}..{L_grid[-1]:.2f}]x{len(L_grid)}; per-solve={PER_SOLVE}s total={TOTAL_BUDGET}s",
          flush=True)
    print("=" * 100, flush=True)

    ctx = M.make_ctx(Nr, Nth, rc=0.5)
    grand = {"meta": dict(Nr=Nr, Nth=Nth, Z=Z, a_grid=a_grid, L_grid=L_grid, a_turn=a_turn,
                          per_solve=PER_SOLVE, total_budget=TOTAL_BUDGET, N_LIST=N_LIST,
                          q_amb=EMB.Q_AMB, mu_amb=EMB.MU_AMB,
                          turn=dict(R0=TURN_R0, c=TURN_C, rstar=TURN_RSTAR)),
             "base_ambient_rule": "phi_A=-q/r, rho_A=r; a=R_amb; rho'_amb=+1 (MODEL)",
             "turn_ambient_rule": "phi_A=-q/r, rho_A=R0-c(r-r*)^2; a=R_amb; rho'_amb=-2c(a-r*) (MODEL)"}

    for N in N_LIST:
        # --- base MODEL ambient (single-signed rho'_amb=+1): phases 0-4 (band + q + rescue) ---
        rec = run_N(N, Z, XI, KAP, ctx, a_grid, L_grid, EMB.model_ambient, "BASE (rho'_amb=+1)",
                    budget_left, PER_SOLVE, tag="[band + q-rescue]")
        grand[f"N{N}_base"] = rec
        # --- turning-point MODEL ambient: the dedicated I_r-vs-sign(rho'_amb) free test ---
        if budget_left() > 4 * PER_SOLVE:
            ft = free_test_scan(N, Z, XI, KAP, ctx, a_turn, L_grid, budget_left, PER_SOLVE)
            grand[f"N{N}_freetest"] = ft
        else:
            print(f"\n[FREE TEST N={N} throughput-limited -> skipped]", flush=True)
            grand[f"N{N}_freetest"] = dict(skipped="throughput-limited")

    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch_f2d_classB_summary.json")
    try:
        with open(outpath, "w") as f:
            json.dump(grand, f, indent=1, default=float)
        print(f"\n[summary JSON -> {outpath}]", flush=True)
    except Exception as e:
        print(f"[JSON dump failed: {e}]", flush=True)

    print(f"\nTOTAL WALL: {elapsed():.1f}s  (budget {TOTAL_BUDGET:.0f}s)", flush=True)
    print("RUN COMPLETE -- MODEL ambient, N in {1,2}, Z=8, ONE slice; NOT a discreteness or frame verdict.",
          flush=True)
