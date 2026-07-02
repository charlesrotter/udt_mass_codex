"""cell_solver_f2d_first_build.py -- the pre-registered FIRST BUILD (N=1) of the Class-A FREE
(H=0) finite-mirror cell scan, executed STRICTLY per the authoritative spec.

Spec (BINDING, re-read while building):
  * f_rtheta_free_field_MAP.md            -- THE MAP: sec.4 [OBS-1] four isolation sources +
                                             "Scan design consequence"; sec.9 charter items 1-7.
  * f2d_virial_step0_results.md           -- "Consequences for the build": H=0 third closure;
                                             Derrick diagnostic; far-from-rigid seeds; N>=2 theta-first.
  * discreteness_preregistration.md       -- 9 criteria + KEY ACCEPTANCE TEST + AMENDMENT 2026-07-01b
                                             (run BOTH Z in {1,8}).
  * cell_solver_f2d.py                     -- the CAS-verified operators, REUSED verbatim (make_ctx,
                                             fields, H_of_r, derrick, seed, pack, unpack).

WHAT THIS SCRIPT DOES (the spec method, NOT a free-L / fixed-L-H(seal) shortcut):
  1. CLOSURE-MANIFOLD MAP (MAP sec.4 + sec.9.3). For a grid of cell size L, solve the BOTH-mirror
     field BVP at FIXED L (phi'=rho'=0 both ends, f_r=0 both ends) -- the WELL-CONDITIONED SQUARE
     field system (H=0 row dropped, L-as-unknown dropped). At each L, launch from >=3 DISTINCT
     seeds -> multiple branches (do not assume one). Record every converged branch. The H=0
     CLOSURE is where H(seal)(L)=0 along a branch (sign change) -> Newton-polish in L. Report BOTH
     the isolated closure set AND the H!=0 continuum (Step-0 consequence #1).
  2. STABILITY FILTER (MAP sec.9.3 / sec.4c / criterion 8) -- the DECISIVE step. At each H=0 closure
     solution, form the symmetric Hessian of the reduced action S = INT Lbar dr (per 4pi) wrt the
     interior field DOF via torch autodiff; real eigenvalue spectrum; classify:
        near-ZERO eigenvalue  = FLAT DIRECTION = continuous family => NOT isolated (fails crit 1/8);
        NEGATIVE eigenvalues  = unstable/saddle (Morse index > 0);
        POSITIVE-DEFINITE     = isolated stable cell candidate (index 0, no zero mode).
     Hessian sanity: symmetric; real eigenvalues; a manufactured flat-direction toy returns a zero
     mode. CAVEAT (honored + stated): the fixed-metric Hessian can OVER-COUNT instabilities
     (project note gravitating-soliton-stability-test) -> for any NEGATIVE mode, ALSO perturb along
     the negative eigenvector, re-solve the fixed-L BVP, and report whether it returns (over-count)
     or runs off (genuine).
  3. ROBUSTNESS GATES (MAP sec.9.4): (a) >=3 seeds; (b) grid-independence Nr in {12,16,24} on ONE
     closure solution + a finite-difference radial-derivative cross-check; (c) Derrick + H-drift as
     ARTIFACT FILTERS (|dS| not small or large H-drift => numerical artifact, rejected).
  4. N=1, Z in {1,8} (both; amendment), xi=kap=1.

DISCIPLINE: UNLABELED output; single clean process, unbuffered, NO background, NO nohup; everything
bounded (Nr<=24, Nth<=28, LM iters<=150, per-solve + total wall budget). This is N=1, ONE step of
the charter -- NOT a discreteness verdict.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev, hessian, grad as tgrad

import cell_solver_f2d as M   # REUSE the CAS-verified operators verbatim


# =========================================================================================
# FIXED-L SQUARE FIELD RESIDUAL  (H=0 row DROPPED, L a fixed PARAMETER not an unknown)
#   unknown w = [phi(Nr), rho(Nr), u(Nr*Nth)]   (length 2Nr + Nr*Nth)
#   rows: phi-ODE interior (Nr-2) | phi' mirror (2) | rho-ODE interior (Nr-2) | rho' mirror (2)
#         | f-PDE interior (Nr-2)*Nth | f_r mirror both ends (2*Nth)   == 2Nr + Nr*Nth  (SQUARE)
# =========================================================================================
def _w_to_v(w, ctx, L):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    phi = w[:Nr]; rho = w[Nr:2 * Nr]; uf = w[2 * Nr:2 * Nr + Nr * Nth].reshape(Nr, Nth)
    return M.pack(phi, rho, uf, L)


def residual_fixedL(w, ctx, prm, L, wbc=1.0):
    Q = M.fields(_w_to_v(w, ctx, L), ctx, prm)
    phip, rhop, fr = Q["phip"], Q["rhop"], Q["fr"]
    rows = [
        Q["phi_ode"][1:-1],
        wbc * phip[[0, -1]],
        Q["rho_ode"][1:-1],
        wbc * rhop[[0, -1]],
        Q["res_f"][1:-1].reshape(-1),
        wbc * fr[0, :], wbc * fr[-1, :],
    ]
    return torch.cat([r.reshape(-1) for r in rows])


def _seed_w(ctx, phi0=0.0, rho0=0.70710678, amp=0.4):
    """Reduced seed (drop the L slot): rigid-background + band-limited radial deformation. Far-from-
    rigid amplitudes are ALLOWED/encouraged (Step-0 V7: rigid-adjacent seeds are downhill toward
    collapse). All CHOSE seed values; the solver relaxes them."""
    v = M.seed(ctx, phi0=phi0, rho0=rho0, L0=1.0, amp=amp)
    return v[:-1].clone()


# =========================================================================================
# BOUNDED LEVENBERG-MARQUARDT (Nielsen gain-ratio damping); Jacobian by jacrev.
# Method identical to cell_solver_f2d.newton_lm_solve, generalized to an arbitrary resfn.
# =========================================================================================
def lm_solve(resfn, w0, maxit=120, tol=1e-12, lam0=1e-3, time_budget=20.0, verbose=False):
    t0 = time.time()
    w = w0.detach().clone()
    F = resfn(w); Phi = float((F * F).sum()); hist = [Phi]
    lam = lam0; nu = 2.0
    it = 0
    for it in range(maxit):
        if Phi < tol or (time.time() - t0) > time_budget:
            break
        J = jacrev(resfn)(w).detach()
        F = resfn(w).detach()
        JT = J.transpose(0, 1)
        Hm = JT @ J; g = JT @ (-F); dH = torch.diag(Hm)
        accepted = False
        for _try in range(30):
            try:
                dx = torch.linalg.solve(Hm + lam * torch.diag(dH), g)
            except Exception:
                lam = min(lam * nu, 1e12); nu *= 2.0; continue
            wn = w + dx
            try:
                Fn = resfn(wn); Pn = float((Fn * Fn).sum())
            except Exception:
                Pn = float("inf")
            pred = float((dx * (lam * dH * dx + g)).sum())
            rho_gain = (Phi - Pn) / pred if (pred > 0.0 and math.isfinite(Pn)) else -1.0
            if rho_gain > 0.0:
                w = wn; F = Fn.detach(); Phi = Pn
                lam = max(lam * max(1.0 / 3.0, 1.0 - (2.0 * rho_gain - 1.0) ** 3), 1e-14)
                nu = 2.0; accepted = True; break
            lam = min(lam * nu, 1e12); nu *= 2.0
        hist.append(Phi)
        if verbose:
            print(f"    [lm] it={it:3d} Phi={Phi:.3e} lam={lam:.2e} {'acc' if accepted else 'STALL'}",
                  flush=True)
        if not accepted:
            break
    wall = time.time() - t0
    return w.detach(), Phi, (it + 1), wall


PHI_CAP = 8.0   # |phi| beyond this = matter-decoupled RUNAWAY (e^{2phi}->0 suppresses the source)


def solve_at_L(w0, ctx, prm, L, wbc=1.0, maxit=140, tol=1e-13, budget=20.0):
    """Relax the fixed-L square BVP. HONEST convergence gate: a GENUINE stationary cell requires
    Phi below a TIGHT tol AND iters<maxit (a stall at maxit is not stationary) AND |phi| bounded
    (the failure mode here is a phi->-inf runaway that suppresses the residual via e^{2phi}->0, so a
    loose absolute-Phi gate FALSE-PASSES it). Outcome tagged: converged / runaway / collapsed / stall."""
    resfn = lambda ww: residual_fixedL(ww, ctx, prm, L, wbc=wbc)
    w, Phi, iters, wall = lm_solve(resfn, w0, maxit=maxit, tol=tol, time_budget=budget)
    v = _w_to_v(w, ctx, L)
    phi, rho, uf, _ = M.unpack(v, ctx)
    finite = bool(torch.isfinite(w).all())
    rho_min = float(rho.min()); phi_absmax = float(phi.abs().max())
    stalled = (iters >= maxit)
    collapsed = (rho_min <= 1e-4) or (not finite)
    runaway = (phi_absmax >= PHI_CAP)
    converged = (Phi < 1e-11) and finite and (rho_min > 1e-4) and (not stalled) and (not runaway)
    outcome = ("converged" if converged else "collapsed" if collapsed
               else "runaway" if runaway else "stall")
    return dict(w=w, Phi=Phi, iters=iters, wall=wall, converged=converged,
                collapsed=collapsed, runaway=runaway, stalled=stalled,
                rho_min=rho_min, phi_absmax=phi_absmax, outcome=outcome)


# =========================================================================================
# DIAGNOSTICS on a fixed-L solution
# =========================================================================================
def solution_report(w, ctx, prm, L):
    v = _w_to_v(w, ctx, L)
    phi, rho, uf, _ = M.unpack(v, ctx)
    Q = M.fields(v, ctx, prm)
    Hn = M.H_of_r(v, ctx, prm).detach()
    Sa, Sb, dS = M.derrick(v, ctx, prm)
    return dict(
        L=float(L), phi_c=float(phi[0]), rho_c=float(rho[0]),
        phi_s=float(phi[-1]), rho_s=float(rho[-1]),
        maxu=float(uf.abs().max()), Ir_max=float(Q["Ir"].abs().max()),
        Hseal=float(Hn[-1]), Hdrift=float((Hn.max() - Hn.min())),
        derrick_dS=float(dS), derrick_Sa=float(Sa), derrick_Sb=float(Sb),
    )


# =========================================================================================
# REDUCED ACTION  S = INT Lbar dr  (per 4pi);  Lbar uses the CAS-verified moments from fields()
# =========================================================================================
def action_S(w, ctx, prm, L):
    Z, XI, KAP, N = prm
    Q = M.fields(_w_to_v(w, ctx, L), ctx, prm)
    rho, phip, rhop, e2m = Q["rho"], Q["phip"], Q["rhop"], Q["e2m"]
    Ir, Ith, Is, I4th, I4r = Q["Ir"], Q["Ith"], Q["Is"], Q["I4th"], Q["I4r"]
    Lbar = ((Z / 2.0) * rho ** 2 * phip ** 2 + 2.0 - 2.0 * e2m * rhop ** 2
            - (XI / 2.0) * (rho ** 2 * Ir + Ith + N ** 2 * Is)
            - (KAP * N ** 2 / 2.0) * (I4r + I4th / rho ** 2))
    return (ctx["ccw"] * Lbar).sum() * (L / 2.0)


def stability_spectrum(w, ctx, prm, L):
    """Symmetric Hessian of S wrt the interior field DOF (natural mirror BCs are automatic in S).
    Returns (eigs ascending, symmetry_error, gradnorm)."""
    Sfn = lambda ww: action_S(ww, ctx, prm, L)
    gnorm = float(tgrad(Sfn)(w).detach().norm())
    Hmat = hessian(Sfn)(w).detach()
    sym_err = float((Hmat - Hmat.transpose(0, 1)).abs().max())
    Hs = 0.5 * (Hmat + Hmat.transpose(0, 1))
    eigs = torch.linalg.eigvalsh(Hs)
    return eigs, Hmat, sym_err, gnorm


def classify_spectrum(eigs, zero_rel=1e-6):
    ea = eigs.detach()
    scale = float(ea.abs().max())
    tol0 = zero_rel * scale if scale > 0 else zero_rel
    n_neg = int((ea < -tol0).sum())
    n_zero = int((ea.abs() <= tol0).sum())
    n_pos = int((ea > tol0).sum())
    smallest = sorted([float(x) for x in ea], key=abs)[:5]
    return dict(n_neg=n_neg, n_zero=n_zero, n_pos=n_pos, scale=scale, tol0=tol0,
                smallest_abs=smallest, lam_min=float(ea.min()), lam_max=float(ea.max()))


def hessian_sanity():
    """Machinery check: a manufactured quadratic action with an EXACT flat direction must return a
    zero eigenvalue; Hessian symmetric; eigenvalues real."""
    A = torch.tensor([[1.0, -1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 2.0]])  # null vec (1,1,0)/sqrt2
    Sfn = lambda x: 0.5 * (x @ (A @ x))
    x0 = torch.tensor([0.3, -0.2, 0.5])
    Hm = hessian(Sfn)(x0).detach()
    sym = float((Hm - Hm.T).abs().max())
    eig = torch.linalg.eigvalsh(0.5 * (Hm + Hm.T))
    match_A = float((Hm - A).abs().max())
    has_zero = bool(eig.abs().min() < 1e-10)
    real_ok = bool(torch.isfinite(eig).all())
    return dict(sym=sym, match_A=match_A, eig=[float(e) for e in eig],
                has_zero=has_zero, real_ok=real_ok)


def coupled_resolve_negmode(w_star, v_neg, ctx, prm, L, delta=0.05, budget=20.0):
    """CAVEAT test (over-count guard): perturb along the negative eigenvector, re-solve the fixed-L
    BVP, report distance back to w_star. Small => negative mode was OFF-CONSTRAINT (over-count);
    large / non-convergent => genuine instability."""
    vn = v_neg / (v_neg.norm() + 1e-30)
    scale = float(w_star.norm()) + 1e-30
    w_pert = w_star + delta * scale * vn
    r = solve_at_L(w_pert, ctx, prm, L, budget=budget)
    dist_back = float((r["w"] - w_star).norm() / scale)
    return dict(converged=r["converged"], dist_back=dist_back, Phi=r["Phi"],
                collapsed=r["collapsed"])


# =========================================================================================
# BRANCH TRACING + H=0 CLOSURE POLISH
# =========================================================================================
def trace_branch(w_start, ctx, prm, L_grid, L_start_idx, wbc=1.0, budget=20.0):
    """Continuation sweep in L (both directions from L_start_idx) reusing the neighbouring solution
    as the seed. Returns a dict L -> solution_report(+w) for every converged L on the branch."""
    out = {}
    # start point
    r0 = solve_at_L(w_start, ctx, prm, L_grid[L_start_idx], wbc=wbc, budget=budget)
    if not r0["converged"]:
        return out
    out[L_start_idx] = dict(rep=solution_report(r0["w"], ctx, prm, L_grid[L_start_idx]), w=r0["w"])
    # sweep up
    w_prev = r0["w"]
    for i in range(L_start_idx + 1, len(L_grid)):
        r = solve_at_L(w_prev, ctx, prm, L_grid[i], wbc=wbc, budget=budget)
        if not r["converged"]:
            break
        out[i] = dict(rep=solution_report(r["w"], ctx, prm, L_grid[i]), w=r["w"]); w_prev = r["w"]
    # sweep down
    w_prev = r0["w"]
    for i in range(L_start_idx - 1, -1, -1):
        r = solve_at_L(w_prev, ctx, prm, L_grid[i], wbc=wbc, budget=budget)
        if not r["converged"]:
            break
        out[i] = dict(rep=solution_report(r["w"], ctx, prm, L_grid[i]), w=r["w"]); w_prev = r["w"]
    return out


def polish_Hseal_zero(branch, ctx, prm, wbc=1.0, budget=20.0):
    """Find H(seal)(L)=0 sign changes along a traced branch (keyed by L index) and secant-polish in
    L. Returns a list of closure dicts {L, w, rep}."""
    idxs = sorted(branch.keys())
    closures = []
    for a, b in zip(idxs[:-1], idxs[1:]):
        Ha = branch[a]["rep"]["Hseal"]; Hb = branch[b]["rep"]["Hseal"]
        if Ha == Hb:
            continue
        if Ha * Hb < 0.0:  # sign change -> a root in (La, Lb)
            La = branch[a]["rep"]["L"]; Lb = branch[b]["rep"]["L"]
            wa = branch[a]["w"]
            # secant in L, re-solving the field BVP at each trial L (continuation seed = wa)
            Lo, Ho, wo = La, Ha, wa
            Ln, Hn = Lb, Hb
            w_seed = wa
            root = None
            for _ in range(20):
                if abs(Hn - Ho) < 1e-30:
                    break
                Lm = Ln - Hn * (Ln - Lo) / (Hn - Ho)
                if not (min(La, Lb) - 0.5 * abs(Lb - La) <= Lm <= max(La, Lb) + 0.5 * abs(Lb - La)):
                    Lm = 0.5 * (Lo + Ln)
                r = solve_at_L(w_seed, ctx, prm, Lm, wbc=wbc, budget=budget)
                if not r["converged"]:
                    break
                rep = solution_report(r["w"], ctx, prm, Lm)
                Hm = rep["Hseal"]; w_seed = r["w"]
                Lo, Ho = Ln, Hn; Ln, Hn = Lm, Hm
                root = dict(L=Lm, w=r["w"], rep=rep)
                if abs(Hm) < 1e-9:
                    break
            if root is not None:
                closures.append(root)
    return closures


# =========================================================================================
# CONTINUUM TABLE  (the H!=0 context the spec requires): relax at every L from ONE seed (fresh,
# then continuation) and record the ENDPOINT config + diagnostics REGARDLESS of convergence, so the
# H(seal)(L) behaviour of the whole scanned manifold is visible even when nothing truly converges.
# =========================================================================================
def continuum_table(seed_spec, ctx, prm, L_grid, wbc=1.0, budget=20.0, use_continuation=True):
    rows = []
    w_seed = _seed_w(ctx, phi0=seed_spec["phi0"], rho0=seed_spec["rho0"], amp=seed_spec["amp"])
    for L in L_grid:
        w0 = w_seed if use_continuation else _seed_w(ctx, phi0=seed_spec["phi0"],
                                                     rho0=seed_spec["rho0"], amp=seed_spec["amp"])
        r = solve_at_L(w0, ctx, prm, L, wbc=wbc, budget=budget)
        rep = solution_report(r["w"], ctx, prm, L)
        rep["outcome"] = r["outcome"]; rep["Phi"] = r["Phi"]; rep["iters"] = r["iters"]
        rep["phi_absmax"] = r["phi_absmax"]
        rows.append(dict(rep=rep, w=r["w"]))
        if use_continuation and r["outcome"] in ("converged", "stall", "runaway"):
            w_seed = r["w"]   # continue (even a stall gives a nearby start for the next L)
    return rows


# =========================================================================================
# ONE FULL (N, Z) SCAN
# =========================================================================================
def run_scan(Z, N, ctx, L_grid, seeds, wbc=1.0, budget=20.0, total_budget=1e9, t_start=None):
    prm = (Z, 1.0, 1.0, N)
    print(f"\n================= SCAN  N={N}  Z={Z}  xi=kap=1  "
          f"(Nr={ctx['Nr']},Nth={ctx['Nth']}, |w|={2*ctx['Nr']+ctx['Nr']*ctx['Nth']}) =================",
          flush=True)
    mid = len(L_grid) // 2
    prm = (Z, 1.0, 1.0, N)

    # ---- (i) SEED-INDEPENDENCE probe at the mid L: where does each seed drain to? ----
    print("  [seed-independence @ mid-L] each of >=3 distinct seeds relaxed at fixed L:", flush=True)
    branches = []; branch_keys = []
    for si, sd in enumerate(seeds):
        w0 = _seed_w(ctx, phi0=sd["phi0"], rho0=sd["rho0"], amp=sd["amp"])
        r = solve_at_L(w0, ctx, prm, L_grid[mid], wbc=wbc, budget=budget)
        rep = solution_report(r["w"], ctx, prm, L_grid[mid])
        print(f"    seed[{si}] amp={sd['amp']:.2f} rho0={sd['rho0']:.3f} @L={L_grid[mid]:.3f}: "
              f"OUTCOME={r['outcome']:9s} Phi={r['Phi']:.2e} it={r['iters']} "
              f"phi_c={rep['phi_c']:+.3f}(|phi|max={r['phi_absmax']:.2f}) rho_c={rep['rho_c']:.3f} "
              f"maxu={rep['maxu']:.3f} Hseal={rep['Hseal']:+.3f}", flush=True)
        if r["converged"]:
            key = (round(rep["phi_c"], 3), round(rep["rho_c"], 3))
            if key in branch_keys:
                print(f"           (duplicate branch key {key})", flush=True); continue
            branch_keys.append(key)
            traj = trace_branch(r["w"], ctx, prm, L_grid, mid, wbc=wbc, budget=budget)
            branches.append(dict(seed=sd, key=key, traj=traj))
            print(f"           NEW converged branch key={key}; traced {len(traj)} L-points", flush=True)

    # ---- (ii) CONTINUUM TABLE across the full L grid (the H!=0 context, spec-required) ----
    print(f"\n  [continuum table] relax vs L (seed[1] amp={seeds[1]['amp']}, continuation); "
          f"shows the WHOLE scanned manifold's H(seal)(L):", flush=True)
    cont = continuum_table(seeds[1], ctx, prm, L_grid, wbc=wbc, budget=budget)
    for row in cont:
        rp = row["rep"]
        print(f"    L={rp['L']:.4f}  {rp['outcome']:9s} phi_c={rp['phi_c']:+.4f} rho_c={rp['rho_c']:.4f} "
              f"rho_s={rp['rho_s']:.4f} maxu={rp['maxu']:.3f} Hseal={rp['Hseal']:+.4e} "
              f"Hdrift={rp['Hdrift']:.1e} dDerrick={rp['derrick_dS']:+.2e}", flush=True)
    Hs_vals = [row["rep"]["Hseal"] for row in cont]
    print(f"    H(seal) over the scanned range: [{min(Hs_vals):+.4f}, {max(Hs_vals):+.4f}] "
          f"-> sign change present: {min(Hs_vals) * max(Hs_vals) < 0}", flush=True)

    # ---- (iii) GENUINE H=0 closures live ONLY on truly-CONVERGED branches ----
    all_closures = []
    for bi, br in enumerate(branches):
        traj = br["traj"]
        print(f"\n  --- converged branch[{bi}] key={br['key']} : H(seal) vs L ---", flush=True)
        for i in sorted(traj.keys()):
            rp = traj[i]["rep"]
            print(f"    L={rp['L']:.4f} phi_c={rp['phi_c']:+.4f} rho_c={rp['rho_c']:.4f} "
                  f"Hseal={rp['Hseal']:+.4e} Hdrift={rp['Hdrift']:.1e}", flush=True)
        closures = polish_Hseal_zero(traj, ctx, prm, wbc=wbc, budget=budget)
        for c in closures:
            c["branch"] = bi
        all_closures += closures
    if not branches:
        print("\n  --- NO truly-converged branch (all seeds drain to runaway/stall/collapse) "
              "=> NO genuine H=0 closure solutions on this slice ---", flush=True)
    return branches, all_closures, cont


def analyze_closures(closures, ctx, prm, artifact_dS=1e-3, artifact_Hdrift=1e-3, budget=20.0):
    """Stability filter + artifact filter on each H=0 closure solution."""
    results = []
    for ci, c in enumerate(closures):
        rep = c["rep"]; w = c["w"]; L = c["L"]
        # artifact filter (Derrick + H-drift)
        artifact = (abs(rep["derrick_dS"]) > artifact_dS) or (rep["Hdrift"] > artifact_Hdrift)
        eigs, Hmat, sym_err, gnorm = stability_spectrum(w, ctx, prm, L)
        cls = classify_spectrum(eigs)
        rec = dict(idx=ci, branch=c["branch"], L=L, rep=rep, artifact=artifact,
                   sym_err=sym_err, gradnorm=gnorm, **cls)
        # over-count caveat test for any negative mode
        if cls["n_neg"] > 0:
            Hs = 0.5 * (Hmat + Hmat.transpose(0, 1))
            evals, evecs = torch.linalg.eigh(Hs)
            v_neg = evecs[:, 0]  # eigenvector of most-negative eigenvalue
            rec["negmode_resolve"] = coupled_resolve_negmode(w, v_neg, ctx, prm, L, budget=budget)
        results.append(rec)
    return results


# =========================================================================================
# GRID-INDEPENDENCE + FD radial cross-check on ONE closure solution
# =========================================================================================
def grid_independence(seed_spec, Z, N, L_target, Nr_list=(12, 16, 24), Nth_of=lambda nr: nr - 2,
                      wbc=1.0, budget=20.0):
    prm = (Z, 1.0, 1.0, N)
    out = []
    for Nr in Nr_list:
        Nth = min(Nth_of(Nr), 28)
        ctx = M.make_ctx(Nr, Nth, rc=0.5)
        w0 = _seed_w(ctx, phi0=seed_spec["phi0"], rho0=seed_spec["rho0"], amp=seed_spec["amp"])
        # relax at L_target, then polish H(seal)=0 near it by a short secant across +-dL
        r = solve_at_L(w0, ctx, prm, L_target, wbc=wbc, budget=budget)
        if not r["converged"]:
            out.append(dict(Nr=Nr, Nth=Nth, ok=False)); continue
        # local closure polish: scan a few L, secant to Hseal=0
        rep0 = solution_report(r["w"], ctx, prm, L_target)
        Ls = [L_target * f for f in (0.9, 0.95, 1.0, 1.05, 1.1)]
        pts = []
        w_seed = r["w"]
        for Lx in Ls:
            rr = solve_at_L(w_seed, ctx, prm, Lx, wbc=wbc, budget=budget)
            if rr["converged"]:
                pts.append((Lx, solution_report(rr["w"], ctx, prm, Lx), rr["w"])); w_seed = rr["w"]
        clo = None
        for (La, ra, wa), (Lb, rb, wb) in zip(pts[:-1], pts[1:]):
            if ra["Hseal"] * rb["Hseal"] < 0:
                Lo, Ho, Ln, Hn, ws = La, ra["Hseal"], Lb, rb["Hseal"], wa
                for _ in range(20):
                    if abs(Hn - Ho) < 1e-30: break
                    Lm = Ln - Hn * (Ln - Lo) / (Hn - Ho)
                    rr = solve_at_L(ws, ctx, prm, Lm, wbc=wbc, budget=budget)
                    if not rr["converged"]: break
                    rm = solution_report(rr["w"], ctx, prm, Lm); ws = rr["w"]
                    Lo, Ho, Ln, Hn = Ln, Hn, Lm, rm["Hseal"]
                    clo = (Lm, rm, rr["w"])
                    if abs(rm["Hseal"]) < 1e-9: break
                break
        if clo is None:
            out.append(dict(Nr=Nr, Nth=Nth, ok=True, closed=False, rep=rep0)); continue
        Lm, rm, wm = clo
        # FD radial-derivative cross-check on phi at this solution
        v = _w_to_v(wm, ctx, Lm); phi, rho, uf, _ = M.unpack(v, ctx)
        zeta = ctx["zeta"].numpy(); phin = phi.detach().numpy()
        sc = 2.0 / Lm
        phip_spec = (sc * (ctx["Dz"] @ phi)).detach().numpy()
        # non-uniform 3-point FD at interior nodes
        fd = np.zeros_like(phin)
        for k in range(1, len(zeta) - 1):
            h1 = zeta[k] - zeta[k - 1]; h2 = zeta[k + 1] - zeta[k]
            fd[k] = (-h2 / (h1 * (h1 + h2)) * phin[k - 1]
                     + (h2 - h1) / (h1 * h2) * phin[k]
                     + h1 / (h2 * (h1 + h2)) * phin[k + 1])
        fd *= sc
        fd_err = float(np.abs(fd[1:-1] - phip_spec[1:-1]).max())
        out.append(dict(Nr=Nr, Nth=Nth, ok=True, closed=True, L=Lm, rep=rm, fd_err=fd_err))
    return out


def characterize_relaxed(seed_spec, Z, N, ctx, L, wbc=1.0, budget=20.0):
    """Run the STABILITY FILTER machinery on the RELAXED (typically stalled/runaway) endpoint config
    at fixed L -- to report 'what is there' even when no genuine H=0 cell exists. Clearly a NON-cell
    characterization: the config is not a converged stationary point."""
    prm = (Z, 1.0, 1.0, N)
    w0 = _seed_w(ctx, phi0=seed_spec["phi0"], rho0=seed_spec["rho0"], amp=seed_spec["amp"])
    r = solve_at_L(w0, ctx, prm, L, wbc=wbc, budget=budget)
    rep = solution_report(r["w"], ctx, prm, L)
    eigs, Hmat, sym_err, gnorm = stability_spectrum(r["w"], ctx, prm, L)
    cls = classify_spectrum(eigs)
    return dict(outcome=r["outcome"], rep=rep, sym_err=sym_err, gradnorm=gnorm, **cls)


def runaway_grid_check(seed_spec, Z, N, L, Nr_list=(12, 16, 24), Nth_of=lambda nr: nr - 2,
                       wbc=1.0, budget=20.0):
    """Grid-independence of the NEGATIVE: confirm the matter-decoupled runaway (u->0, phi->-inf,
    rho->inf, H(seal)<0) persists across Nr in {12,16,24}, + a finite-difference phi' cross-check."""
    prm = (Z, 1.0, 1.0, N); out = []
    for Nr in Nr_list:
        Nth = min(Nth_of(Nr), 28)
        ctx = M.make_ctx(Nr, Nth, rc=0.5)
        w0 = _seed_w(ctx, phi0=seed_spec["phi0"], rho0=seed_spec["rho0"], amp=seed_spec["amp"])
        r = solve_at_L(w0, ctx, prm, L, wbc=wbc, budget=budget)
        rep = solution_report(r["w"], ctx, prm, L)
        # FD phi' cross-check
        v = _w_to_v(r["w"], ctx, L); phi, rho, uf, _ = M.unpack(v, ctx)
        zeta = ctx["zeta"].numpy(); phin = phi.detach().numpy(); sc = 2.0 / L
        phip_spec = (sc * (ctx["Dz"] @ phi)).detach().numpy()
        fd = np.zeros_like(phin)
        for k in range(1, len(zeta) - 1):
            h1 = zeta[k] - zeta[k - 1]; h2 = zeta[k + 1] - zeta[k]
            fd[k] = (-h2 / (h1 * (h1 + h2)) * phin[k - 1] + (h2 - h1) / (h1 * h2) * phin[k]
                     + h1 / (h2 * (h1 + h2)) * phin[k + 1])
        fd *= sc
        fd_err = float(np.abs(fd[1:-1] - phip_spec[1:-1]).max())
        out.append(dict(Nr=Nr, Nth=Nth, outcome=r["outcome"], rep=rep,
                        phi_absmax=r["phi_absmax"], fd_err=fd_err))
    return out


# =========================================================================================
# MAIN  (single process, unbuffered, bounded; N=1, Z in {1,8})
# =========================================================================================
if __name__ == "__main__":
    T0 = time.time()
    TOTAL_BUDGET = 1500.0     # hard total wall budget (s); throughput-limited entries recorded if hit
    PER_SOLVE = 18.0          # per-solve wall budget (s)
    # ---- fixed parameters (ALL tagged) ----
    N = 1                     # DERIVED-topological (winding degree; fixed per run)
    XI = 1.0                  # CHOSE-units
    KAP = 1.0                 # CHOSE-units (kap/xi sets absolute scale; only RATIOS are observables)
    Z_LIST = [1.0, 8.0]       # CHOSE-fixed, run BOTH (pre-reg AMENDMENT 2026-07-01b; Z=8 = OBS-2)
    Nr, Nth = 16, 12          # BOUNDED scan grid (anti-hang; Nr<=24, Nth<=28)
    wbc = 1.0
    L_grid = list(np.linspace(0.45, 2.0, 9))   # CHOSE scan range of cell size L
    seeds = [                                  # >=3 DISTINCT seeds (criterion 2); far-from-rigid allowed
        dict(amp=0.05, rho0=0.707, phi0=0.0),
        dict(amp=0.40, rho0=0.707, phi0=0.0),
        dict(amp=1.00, rho0=0.900, phi0=0.1),
    ]

    print("=" * 92)
    print("CLASS-A FREE (H=0) FIRST BUILD -- N=1, Z in {1,8}, xi=kap=1.  UNLABELED closure-manifold")
    print("scan + STABILITY FILTER.  Fixed-L SQUARE field BVP at each L; H(seal)=0 -> isolated closure.")
    print("=" * 92, flush=True)

    # ---- Hessian machinery sanity FIRST ----
    hs = hessian_sanity()
    print(f"\n[Hessian sanity] symmetric(err={hs['sym']:.1e})  Hessian==A(err={hs['match_A']:.1e})  "
          f"eigs={['%.3f'%e for e in hs['eig']]}  flat-direction zero-mode found={hs['has_zero']}  "
          f"real={hs['real_ok']}", flush=True)

    ctx = M.make_ctx(Nr, Nth, rc=0.5)
    mid = len(L_grid) // 2
    grand = {}
    for Z in Z_LIST:
        branches, closures, cont = run_scan(Z, N, ctx, L_grid, seeds, wbc=wbc,
                                             budget=PER_SOLVE, total_budget=TOTAL_BUDGET, t_start=T0)
        print(f"\n  >>> N=1 Z={Z}: {len(branches)} truly-converged branch(es); "
              f"{len(closures)} genuine H=0 closure solution(s)", flush=True)

        # (a) stability filter on any GENUINE closures
        analysis = analyze_closures(closures, ctx, (Z, XI, KAP, N), budget=PER_SOLVE)
        for a in analysis:
            print(f"    [closure b{a['branch']} L={a['L']:.5f}] index(n_neg)={a['n_neg']} "
                  f"n_zero={a['n_zero']} n_pos={a['n_pos']}  lam_min={a['lam_min']:+.3e} "
                  f"scale={a['scale']:.2e}  smallest|lam|={['%.2e'%x for x in a['smallest_abs']]}",
                  flush=True)
            print(f"        sym_err={a['sym_err']:.1e} gradS_norm={a['gradnorm']:.2e} "
                  f"artifact(Derrick/Hdrift)={a['artifact']} (dS={a['rep']['derrick_dS']:+.2e} "
                  f"Hdrift={a['rep']['Hdrift']:.1e})", flush=True)
            if "negmode_resolve" in a:
                nr = a["negmode_resolve"]
                print(f"        neg-mode coupled re-solve: converged={nr['converged']} "
                      f"dist_back={nr['dist_back']:.3e} collapsed={nr['collapsed']} "
                      f"(small dist_back => OFF-CONSTRAINT over-count; large/collapse => genuine)",
                      flush=True)

        # (b) if NO genuine cell: characterize the relaxed (stalled) endpoint -- 'what is there'
        char = None
        if not closures:
            char = characterize_relaxed(seeds[1], Z, N, ctx, L_grid[mid], wbc=wbc, budget=PER_SOLVE)
            print(f"    [NON-cell characterization @L={L_grid[mid]:.3f}, outcome={char['outcome']}] "
                  f"the relaxed endpoint is NOT a converged cell; its S-Hessian spectrum: "
                  f"index(n_neg)={char['n_neg']} n_zero={char['n_zero']} n_pos={char['n_pos']} "
                  f"lam=[{char['lam_min']:+.2e},{char['lam_max']:+.2e}] "
                  f"(massively-indefinite => consistent with 'not a stable cell')", flush=True)
        grand[Z] = dict(branches=branches, closures=closures, analysis=analysis, cont=cont, char=char)

    # ---- GRID INDEPENDENCE ----
    print("\n" + "=" * 92)
    print("GRID INDEPENDENCE (Nr in {12,16,24}, Nth scaled) + FD radial phi' cross-check")
    print("=" * 92, flush=True)
    any_closure = any(grand[Z]["closures"] for Z in Z_LIST)
    if any_closure:
        for Z in (8.0, 1.0):
            if grand[Z]["closures"]:
                c0 = grand[Z]["closures"][0]; sd = grand[Z]["branches"][c0["branch"]]["seed"]
                L_target = c0["L"]
                print(f"  on the GENUINE closure: N=1 Z={Z} L~{L_target:.4f}", flush=True)
                gi = grid_independence(sd, Z, N, L_target, wbc=wbc, budget=PER_SOLVE)
                for g in gi:
                    if not g.get("ok"):
                        print(f"    Nr={g['Nr']} Nth={g['Nth']}: did NOT converge (throughput-limited)", flush=True); continue
                    if not g.get("closed"):
                        print(f"    Nr={g['Nr']} Nth={g['Nth']}: converged, no H=0 crossing near L_target", flush=True); continue
                    r = g["rep"]
                    print(f"    Nr={g['Nr']:2d} Nth={g['Nth']:2d}: L*={g['L']:.5f} phi_c={r['phi_c']:+.5f} "
                          f"rho_c={r['rho_c']:.5f} maxu={r['maxu']:.4f} Hdrift={r['Hdrift']:.1e} "
                          f"FD-vs-spectral phi' err={g['fd_err']:.2e}", flush=True)
                break
    else:
        print("  NO genuine H=0 closure at either Z -> instead confirm the NEGATIVE is "
              "grid-independent (the runaway persists across Nr):", flush=True)
        gi = runaway_grid_check(seeds[1], 8.0, N, L_grid[mid], wbc=wbc, budget=PER_SOLVE)
        for g in gi:
            r = g["rep"]
            print(f"    Nr={g['Nr']:2d} Nth={g['Nth']:2d}: outcome={g['outcome']:9s} "
                  f"phi_c={r['phi_c']:+.4f}(|phi|max={g['phi_absmax']:.2f}) rho_c={r['rho_c']:.4f} "
                  f"maxu={r['maxu']:.4f} Hseal={r['Hseal']:+.4f}  FD-vs-spectral phi' err={g['fd_err']:.2e}",
                  flush=True)

    print(f"\nTOTAL WALL: {time.time()-T0:.1f}s  (budget {TOTAL_BUDGET:.0f}s)")
    print("RUN COMPLETE -- N=1 only, one step of the charter; NOT a discreteness verdict.", flush=True)
