"""e2d_continuation_driver.py -- CONTINUATION + MULTI-START driver for the coupled composite solve.

E2d (PURSUIT_CHARTER §5).  Category-A conditioning ONLY: this file NEVER touches `residual_comp`
(the physics) or `lm_hardened` (the certified corrector).  It composes three standard globalization
techniques AROUND the untouched corrector so a re-sweep can reach the FIELD-DISTANT roots that
single-shot `lm_hardened` stalls on (E2c: intrinsic local-NLLS minima of ||F||^2 on the stiff
coupled system).  All three are always-green lane techniques (charter): they change HOW we solve,
not the equations; the FINAL solve is on the byte-identical residual.

Techniques (composable):
  1. MULTI-START        -- run the corrector from a LIST of seeds, keep the best (lowest max|F|).
  2. NEWTON HOMOTOPY    -- the source/global homotopy  g_s(v) = R(v) - (1-s) R(v0),  s: 0 -> 1.
                           At s=0, v0 is an EXACT root of g_0 (g_0(v0)=R(v0)-R(v0)=0); at s=1,
                           g_1 = R (the true problem).  Track the root continuously with the
                           hardened corrector warm-started at each s.  It uses ONLY the seed v0 --
                           it NEVER peeks at the true root -- so it is an honest sweep technique.
                           The Jacobian of g_s is the Jacobian of R (constant shift), so jacrev is
                           unchanged.  This is the primary escape from the field-axis local minima:
                           the corrector never descends from far, it walks the moving root.
  3. GRID HOMOTOPY      -- solve on a coarse radial/angular grid (fewer field DOFs -> a smoother,
                           lower-dimensional ||F||^2 landscape with a wider basin), barycentric-
                           prolongate the solution to the fine grid, re-solve.  Coarse -> fine.
  4. PARAM CONTINUATION -- ramp the carrier couplings (xi,kap) from a well-conditioned easy point
                           to the target, re-solving warm-started at each step (residual_comp takes
                           prm=(Z,XI,KAP,N) natively -- no residual edit).

Anti-hang: every path is BOUNDED (maxit + wall budget), SINGLE process, GPU jacrev + numpy linalg,
never background-poll.  GPU results get CPU spot-checks (via lm_hardened's own float64 path + the
caller's independent CPU residual).
"""
import os, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C

DEV = "cuda" if torch.cuda.is_available() else "cpu"


# =========================================================================================
# Barycentric interpolation (generic node sets; small N, O(N^2) exact) -- grid prolongation.
# =========================================================================================
def _bary_weights(x):
    x = np.asarray(x, dtype=np.float64); n = x.size
    w = np.ones(n)
    for j in range(n):
        d = x[j] - x; d[j] = 1.0
        w[j] = 1.0 / np.prod(d)
    return w


def interp_matrix(xs, xt):
    """Barycentric-Lagrange interpolation matrix P (len(xt) x len(xs)): f(xt) = P @ f(xs).
    Exact reproduction at coincident nodes."""
    xs = np.asarray(xs, dtype=np.float64); xt = np.asarray(xt, dtype=np.float64)
    w = _bary_weights(xs); P = np.zeros((xt.size, xs.size))
    for i, xi in enumerate(xt):
        diff = xi - xs
        hit = np.where(np.abs(diff) < 1e-14)[0]
        if hit.size:
            P[i, hit[0]] = 1.0
            continue
        num = w / diff; P[i, :] = num / num.sum()
    return P


def prolongate(v_src, ctx_src, ctx_dst):
    """Barycentric-prolongate a composite state from ctx_src grid to ctx_dst grid.  Radial (zeta,
    Cheb-GL), angular (mu, Legendre-GL) and ambient (za, Cheb-GL) each get their own interp matrix.
    r_p, r_sU carried through.  Category-A: a warm-start construction, not a solve."""
    ps = C.unpack_comp(v_src, ctx_src)
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = [x.detach().cpu().numpy() if torch.is_tensor(x)
                                                 else x for x in ps]
    r_p = float(r_p); r_sU = float(r_sU)
    zs = ctx_src["cell"]["zeta"].cpu().numpy(); zt = ctx_dst["cell"]["zeta"].cpu().numpy()
    ms = ctx_src["cell"]["mu"].cpu().numpy();   mt = ctx_dst["cell"]["mu"].cpu().numpy()
    zas = ctx_src["za"].cpu().numpy();          zat = ctx_dst["za"].cpu().numpy()
    Pr = interp_matrix(zs, zt); Pm = interp_matrix(ms, mt); Pa = interp_matrix(zas, zat)
    phi_c2 = Pr @ phi_c; rho_c2 = Pr @ rho_c
    uf2 = Pr @ uf @ Pm.T                                    # (Nr_dst, Nth_dst)
    phi_a2 = Pa @ phi_a; rho_a2 = Pa @ rho_a
    tt = lambda a: torch.as_tensor(np.asarray(a, dtype=float), device=ctx_dst["device"])
    return C.pack_comp(tt(phi_c2), tt(rho_c2), tt(uf2), tt(phi_a2), tt(rho_a2),
                       r_p, r_sU, device=ctx_dst["device"])


# =========================================================================================
# Single hardened corrector call (thin wrapper -> returns numpy-longdouble w + info).
# =========================================================================================
def _correct(resfn_t, v0, n, maxit=200, budget=90.0, Delta0=8.0, verbose=False):
    w, info = C.lm_hardened(resfn_t, v0, maxit=maxit, time_budget=budget, device=DEV,
                            pos_idx=[n - 2, n - 1], order_idx=(n - 2, n - 1),
                            Delta0=Delta0, verbose=verbose)
    return w, info


def _as_np(w):
    return np.asarray(w, dtype=np.longdouble)


# =========================================================================================
# NEWTON (source) HOMOTOPY -- the primary field-axis escape.  g_s(v) = R(v) - (1-s) R(v0).
# =========================================================================================
def newton_homotopy(resfn_t, v0_np, n, s_steps=16, maxit_step=100, maxit_final=300,
                    budget=240.0, ds_min=1.0 / 4096, ds_max=0.25, verbose=False):
    """Track the root of R from the seed v0 (exact root of g_0) to s=1 (g_1 = R).  Adaptive s:
    grow ds on a clean corrector step, halve on stall; crawl through hard regions down to ds_min
    (never breaks the run for small ds -- only a budget/floor exhaustion stops it).  Returns
    (w, info)."""
    t0 = time.time()
    v0_t = torch.as_tensor(np.asarray(v0_np, dtype=float), device=DEV)
    F0 = resfn_t(v0_t).detach()                            # constant shift (root of g_0 is v0)
    w = _as_np(v0_np).copy()
    s = 0.0; ds = 1.0 / s_steps; nsteps = 0; nfail = 0
    path = [(0.0, float(F0.abs().max()))]
    while s < 1.0 - 1e-12:
        if (time.time() - t0) > budget:
            break
        s_try = min(s + ds, 1.0)
        final = s_try >= 1.0 - 1e-12
        c = 1.0 - s_try
        g = (lambda vv, c=c: resfn_t(vv) - c * F0)         # Jacobian(g) = Jacobian(R)
        mi = maxit_final if final else maxit_step
        wn, info = _correct(g, w, n, maxit=mi, budget=max(5.0, budget - (time.time() - t0)))
        target = 1e-8 if final else 1e-6
        ok = info["maxF"] <= target or (info["maxF"] < 30 * target and info["iters"] < mi)
        if ok:
            w = _as_np(wn); s = s_try; nsteps += 1; path.append((s, info["maxF"]))
            if info["iters"] < mi // 3:                     # easy step -> grow
                ds = min(ds * 1.5, ds_max)
        else:
            ds *= 0.5; nfail += 1
            if ds < ds_min:                                 # hard region: take final push from best
                if final:
                    w = _as_np(wn)
                break
        if verbose:
            print(f"    [homotopy] s={s:.4f} ds={ds:.4f} maxF={info['maxF']:.2e} "
                  f"it={info['iters']} ({time.time()-t0:.0f}s)", flush=True)
    # final clean corrector on the TRUE residual (s=1) from the tracked point
    wf, infof = _correct(resfn_t, w, n, maxit=maxit_final,
                         budget=max(5.0, budget - (time.time() - t0)))
    return _as_np(wf), dict(maxF=infof["maxF"], iters=infof["iters"], s_reached=s,
                            nsteps=nsteps, nfail=nfail, path=path, wall=time.time() - t0)


# =========================================================================================
# PSEUDO-ARCLENGTH continuation on the Newton homotopy -- passes s-TURNING POINTS (folds).
# The plain s-homotopy above stalls at s-folds (the shifted problem R(v)=(1-s)F0 turns back in s);
# arclength parametrizes the path (v,s) by arclength so s may decrease/increase to go AROUND a
# fold.  Augmented square system (dim n+1): [ R(v)-(1-s)F0 ; t.(y-y_pred) ], solved by the SAME
# hardened corrector (jacrev handles the +F0 column and the constant plane row automatically).
# Category-A numerical technique (charter always-green: continuation/homotopy).
# =========================================================================================
def _tangent(resfn_t, v_np, n, F0, ts_sign=1.0):
    """Path tangent (tv, ts) at (v, s): nullspace of [J_R | F0].  Solve J_R tv = -F0 ts (ts=1),
    normalize, orient by ts_sign."""
    from torch.func import jacrev
    vt = torch.as_tensor(np.asarray(v_np, dtype=float), device=DEV)
    J = jacrev(resfn_t)(vt).detach().cpu().numpy().astype(np.float64)
    dr, dc = C._ruiz_equilibrate(J)
    Aeq = dr[:, None] * J * dc[None, :]; beq = -dr * np.asarray(F0.cpu().numpy(), dtype=np.float64)
    y, *_ = np.linalg.lstsq(Aeq, beq, rcond=None)
    tv = dc * y                                            # unscale
    t = np.concatenate([tv, [1.0]]); t = t / np.linalg.norm(t)
    if t[-1] * ts_sign < 0:
        t = -t
    return t


def arclength_homotopy(resfn_t, v0_np, n, ds0=0.04, ds_min=2e-4, ds_max=0.4, maxsteps=400,
                       maxit_corr=40, maxit_final=300, budget=240.0, s_target=1.0,
                       fold_abort=0.03, runaway_cap=None, verbose=False):
    """Track the Newton-homotopy path from (v0, s=0) around any s-folds to s>=s_target, then polish
    on the TRUE residual.  Honest: uses only v0 (never the root).  Early stops: s>=s_target reached;
    the path FOLDED back below its global s-max by > fold_abort (the component does not reach
    s_target); or a boundary runaway exceeds runaway_cap."""
    t0 = time.time()
    v0_t = torch.as_tensor(np.asarray(v0_np, dtype=float), device=DEV)
    F0 = resfn_t(v0_t).detach()
    y = np.concatenate([_as_np(v0_np), [0.0]]).astype(np.longdouble)      # [v; s]
    tang = _tangent(resfn_t, v0_np, n, F0, ts_sign=1.0)
    ds = ds0; nstep = 0; nfail = 0; s_max = 0.0; path = [(0.0, float(F0.abs().max()))]

    def Gaug_factory(y_pred, tvec):
        tt = torch.as_tensor(tvec, device=DEV)
        yp = torch.as_tensor(np.asarray(y_pred, dtype=float), device=DEV)
        def Gaug(yy):
            v = yy[:n]; s = yy[n]
            R = resfn_t(v) - (1.0 - s) * F0
            plane = (tt * (yy - yp)).sum().reshape(1)
            return torch.cat([R, plane])
        return Gaug

    while nstep < maxsteps and (time.time() - t0) < budget:
        y_pred = (y + ds * tang).astype(np.longdouble)
        Gaug = Gaug_factory(y_pred, tang)
        # corrector on the augmented system (boundaries r_p,r_sU at n-2,n-1 within v)
        wy, info = C.lm_hardened(Gaug, y_pred, maxit=maxit_corr,
                                 time_budget=max(4.0, budget - (time.time() - t0)), device=DEV,
                                 pos_idx=[n - 2, n - 1], order_idx=(n - 2, n - 1), Delta0=6.0)
        wy = _as_np(wy)
        # physics residual (first n rows), independent of the plane row
        vt = torch.as_tensor(wy[:n].astype(float), device=DEV)
        physF = float((resfn_t(vt) - (1.0 - wy[n]) * F0).abs().max())
        if info["maxF"] <= 5e-7 and physF <= 5e-7 and np.isfinite(wy).all():
            tang_new = (wy - y); nrm = np.linalg.norm(np.asarray(tang_new, dtype=float))
            if nrm > 0:
                tang_new = np.asarray(tang_new / nrm, dtype=np.float64)
                if float(tang_new @ tang) < 0:
                    tang_new = -tang_new
                tang = tang_new
            y = wy; nstep += 1; s_now = float(y[n]); s_max = max(s_max, s_now)
            path.append((s_now, physF))
            if info["iters"] < maxit_corr // 2:
                ds = min(ds * 1.4, ds_max)
            if verbose:
                print(f"    [arclen] step {nstep} s={s_now:.4f} ds={ds:.4f} "
                      f"physF={physF:.2e} it={info['iters']} ({time.time()-t0:.0f}s)", flush=True)
            if s_now >= s_target:
                break
            if nstep > 4 and s_now < s_max - fold_abort:      # path folded past its s-max
                break
            if runaway_cap is not None and max(abs(float(y[n - 2])), abs(float(y[n - 1]))) > runaway_cap:
                break
        else:
            ds *= 0.5; nfail += 1
            if ds < ds_min:
                break
    # polish on the TRUE residual R from the tracked point (v at s nearest 1)
    wf, infof = _correct(resfn_t, y[:n], n, maxit=maxit_final,
                         budget=max(5.0, budget - (time.time() - t0)))
    return _as_np(wf), dict(maxF=infof["maxF"], iters=infof["iters"], s_reached=float(y[n]),
                            s_max=s_max, nsteps=nstep, nfail=nfail, path=path,
                            wall=time.time() - t0)


# =========================================================================================
# FIXED-POINT (regularized) HOMOTOPY -- an INDEPENDENT homotopy for robustness cross-checks.
#   H(v,s) = s R(v) + (1-s) (v - v0),  s: 0 -> 1.  At s=0: v=v0 (trivial); at s=1: R(v)=0.
#   Jacobian = s J_R + (1-s) I (the identity regularizes early steps).  A DIFFERENT path than
#   Newton homotopy -- if BOTH fail to reach the root from a seed, the obstruction is the landscape
#   (component separation), not the homotopy choice.
# =========================================================================================
def fixedpoint_homotopy(resfn_t, v0_np, n, s_steps=16, maxit_step=80, maxit_final=300,
                        budget=180.0, ds_min=1.0 / 2048, ds_max=0.25, verbose=False):
    t0 = time.time()
    v0_t = torch.as_tensor(np.asarray(v0_np, dtype=float), device=DEV)
    w = _as_np(v0_np).copy()
    s = 0.0; ds = 1.0 / s_steps; nstep = 0; nfail = 0
    while s < 1.0 - 1e-12 and (time.time() - t0) < budget:
        s_try = min(s + ds, 1.0); final = s_try >= 1.0 - 1e-12
        H = (lambda vv, ss=s_try: ss * resfn_t(vv) + (1.0 - ss) * (vv - v0_t))
        mi = maxit_final if final else maxit_step
        wn, info = _correct(H, w, n, maxit=mi, budget=max(4.0, budget - (time.time() - t0)))
        target = 1e-8 if final else 1e-6
        ok = info["maxF"] <= target or (info["maxF"] < 30 * target and info["iters"] < mi)
        if ok:
            w = _as_np(wn); s = s_try; nstep += 1
            if info["iters"] < mi // 3:
                ds = min(ds * 1.5, ds_max)
        else:
            ds *= 0.5; nfail += 1
            if ds < ds_min:
                break
        if verbose:
            print(f"    [fp-homotopy] s={s:.4f} ds={ds:.4f} maxF={info['maxF']:.2e} "
                  f"it={info['iters']}", flush=True)
    wf, infof = _correct(resfn_t, w, n, maxit=maxit_final,
                         budget=max(5.0, budget - (time.time() - t0)))
    return _as_np(wf), dict(maxF=infof["maxF"], iters=infof["iters"], s_reached=s,
                            nsteps=nstep, nfail=nfail, wall=time.time() - t0)


# =========================================================================================
# MULTI-START orchestration: try each seed with (optionally) homotopy; keep the best.
# =========================================================================================
def multistart(resfn_t, seeds, n, use_homotopy=True, s_steps=8, maxit=250,
               budget_per=90.0, total_budget=600.0, verbose=False, tag=""):
    """seeds: list of numpy-longdouble v0.  Returns (best_w, best_info, all_runs)."""
    t0 = time.time(); best = None; runs = []
    for k, v0 in enumerate(seeds):
        if (time.time() - t0) > total_budget:
            runs.append(dict(seed=k, status="budget-skip")); continue
        rem = total_budget - (time.time() - t0)
        try:
            if use_homotopy:
                w, info = newton_homotopy(resfn_t, v0, n, s_steps=s_steps, maxit_final=maxit,
                                          budget=min(budget_per, rem), verbose=verbose)
                method = "homotopy"
            else:
                w, info = _correct(resfn_t, v0, n, maxit=maxit, budget=min(budget_per, rem))
                method = "direct"
        except Exception as e:
            runs.append(dict(seed=k, status=f"error:{type(e).__name__}:{e}")); continue
        maxF = info["maxF"]
        rec = dict(seed=k, method=method, maxF=maxF, iters=info.get("iters"),
                   s_reached=info.get("s_reached"), wall=info.get("wall"))
        runs.append(rec)
        if verbose:
            print(f"  [{tag}] seed {k}: {method} maxF={maxF:.2e} "
                  f"s={info.get('s_reached')} ({info.get('wall',0):.0f}s)", flush=True)
        if best is None or maxF < best[1]["maxF"]:
            best = (w, dict(maxF=maxF, seed=k, method=method, info=info))
    return (best[0], best[1], runs) if best is not None else (None, None, runs)


# =========================================================================================
# GRID HOMOTOPY: solve coarse, prolongate, refine.  levels = list of (Nr,Nth) coarse->fine.
# =========================================================================================
def grid_homotopy(build_resfn, seeds_coarse, levels, Na, kmap, br, prm, n_of,
                  use_homotopy=True, s_steps=6, maxit=250, budget_per=90.0,
                  total_budget=600.0, verbose=False, tag=""):
    """build_resfn(ctx) -> (resfn_t, n).  seeds_coarse: seeds on the FIRST (coarsest) level.
    Returns (best_w, best_info, ctx_fine, trace)."""
    t0 = time.time(); trace = []
    ctx = C.make_ctx_comp(levels[0][0], levels[0][1], Na, kmap=kmap, device=DEV)
    resfn_t, n = build_resfn(ctx)
    w, info, runs = multistart(resfn_t, seeds_coarse, n, use_homotopy=use_homotopy,
                               s_steps=s_steps, maxit=maxit, budget_per=budget_per,
                               total_budget=min(total_budget, 0.5 * total_budget),
                               verbose=verbose, tag=f"{tag}/L0")
    trace.append(dict(level=levels[0], maxF=(info["maxF"] if info else None), runs=runs))
    if w is None:
        return None, None, ctx, trace
    for lvl in levels[1:]:
        if (time.time() - t0) > total_budget:
            break
        ctx_f = C.make_ctx_comp(lvl[0], lvl[1], Na, kmap=kmap, device=DEV)
        resfn_f, nf = build_resfn(ctx_f)
        v0f = prolongate(torch.as_tensor(np.asarray(w, dtype=float), device=DEV), ctx, ctx_f)
        w, info2 = newton_homotopy(resfn_f, _as_np(v0f.cpu().numpy()), nf, s_steps=s_steps,
                                   maxit_final=maxit,
                                   budget=min(budget_per, total_budget - (time.time() - t0))) \
            if use_homotopy else _correct(resfn_f, _as_np(v0f.cpu().numpy()), nf, maxit=maxit,
                                          budget=min(budget_per, total_budget - (time.time() - t0)))
        info = info2; ctx = ctx_f
        trace.append(dict(level=lvl, maxF=info["maxF"]))
        if verbose:
            print(f"  [{tag}] grid {lvl}: maxF={info['maxF']:.2e}", flush=True)
    return _as_np(w), info, ctx, trace


# =========================================================================================
# PARAMETER CONTINUATION in (xi,kap): easy point -> target, warm-started.
# =========================================================================================
def param_continuation(ctx, br, target_prm, seed_v0, n, easy_prm=None, nsteps=4,
                       use_homotopy=True, s_steps=6, maxit=250, budget=240.0, verbose=False):
    """Ramp (xi,kap) from easy_prm to target_prm.  residual_comp takes prm natively -- no edit.
    Returns (w, info)."""
    Z, XI_t, KAP_t, N = target_prm
    if easy_prm is None:
        easy_prm = (Z, min(0.05, XI_t), min(0.01, KAP_t), N)
    _, XI_0, KAP_0, _ = easy_prm
    w = _as_np(seed_v0); info = None; t0 = time.time()
    for k in range(nsteps + 1):
        if (time.time() - t0) > budget:
            break
        frac = k / nsteps
        xi = XI_0 + frac * (XI_t - XI_0); kap = KAP_0 + frac * (KAP_t - KAP_0)
        prm = (Z, xi, kap, N)
        resfn_t = (lambda vv, prm=prm: C.residual_comp(vv, ctx, prm, br))
        if use_homotopy:
            w, info = newton_homotopy(resfn_t, w, n, s_steps=s_steps, maxit_final=maxit,
                                      budget=min(90.0, budget - (time.time() - t0)))
        else:
            w, info = _correct(resfn_t, w, n, maxit=maxit,
                               budget=min(90.0, budget - (time.time() - t0)))
        if verbose:
            print(f"  [param] step {k}/{nsteps} (xi={xi:.3f},kap={kap:.3f}) "
                  f"maxF={info['maxF']:.2e}", flush=True)
    return _as_np(w), info


def cpu_residual_check(w, ctx, prm, br, F_shift=None):
    """Independent CPU float64 residual of a declared solution (GPU/CPU cross-check)."""
    wt = torch.as_tensor(np.asarray(w, dtype=float), device="cpu")
    ctx_c = C.make_ctx_comp(ctx["Nr"], ctx["Nth"], ctx["Na"], kmap=ctx["kmap"], device="cpu")
    F = C.residual_comp(wt, ctx_c, prm, br)
    if F_shift is not None:
        F = F - F_shift.cpu()
    return float(F.abs().max())
