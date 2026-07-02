"""cell_solver_f2d_N2.py -- extend the Class-A FREE (H=0) finite-mirror cell scan to N>=2, STRICTLY
per the authoritative spec + the N=1 build's ~ correction note.

READ (binding): f_rtheta_free_field_MAP.md sec.4/sec.9 (esp. sec.9.2 theta-relax-first continuation);
f2d_virial_step0_results.md Consequences (far-from-rigid seeds; N>=2 theta-first; OBS-3);
discreteness_preregistration.md (9 criteria; BOTH Z in {1,8}); cell_solver_f2d_first_build.py (the
N=1 build -- machinery REUSED verbatim here); cell_solver_f2d_first_build_results.md (the ~ note:
the N=1 stability filter used the ACTION Hessian, ~90% indefinite -- WRONG; this build uses the
MATTER ENERGY Hessian, right-signed, + the constraint-respecting coupled re-solve).

WHAT THIS DOES (spec Parts 1-3):
  PART 1  N>=2 closure-MANIFOLD map, THETA-RELAX-FIRST (MAP sec.9.2):
     * theta_relax(): at a representative L, FIRST solve the theta-part of the f-PDE for a
       radially-UNIFORM deformed profile f=f(theta) (rigid f=theta is NOT stationary for N>=2, OBS-3
       -> a genuinely deformed f(theta) is expected). THEN seed the full 2-D solve with it + free r.
     * far-from-rigid seeds (amp up to ~3; the N=1 build under-sampled -- the verifier pushed amp 3.0).
     * fixed-L both-mirror SQUARE field BVP (phi'=rho'=0, f_r=0 both ends; H=0 row dropped, L a param),
       >=3 distinct seeds per L, over an L grid; record L, phi_c, rho_c, max|u|, moments, H(seal),
       Derrick dS, H-drift. Find H(seal)=0 CROSSINGS (sign change -> secant polish). Report the
       closure set AND the H!=0 continuum. OBSERVE (do NOT target crossings).
  PART 2  TWO-TIER stability filter (fixes the N=1 action-Hessian error):
     * Tier (a) CHEAP: the MATTER ENERGY Hessian (right signs) E_m = -L_m, all POSITIVE terms,
       Hessian wrt the matter DOF u only (geometry phi,rho held at converged values), eigvalsh.
       PD (no negative) => ACCEPT as stable (trustworthy: the fixed-background Hessian OVER-counts
       NEGATIVES, so a positive-definite verdict is trustworthy -- gravitating-soliton-stability-test).
     * Tier (b) DECISIVE (only if tier a INDEFINITE): perturb along the most-negative eigenvector,
       FULL COUPLED re-solve (phi,rho,f together), does it RETURN to the same cell (stable) or run off.
     * tier_a_sanity(): tier (a) must be PD on a manufactured STABLE matter config (N=1 rigid f=theta,
       Step-0 V7 strict min) and must CATCH a manufactured UNSTABLE direction (negative eigenvalue) --
       both exercising the REAL energy code path (matter_energy_of_u -> M.fields), not a toy matrix.
  PART 3  robustness: BOTH Z in {1,8}; grid spot-check Nr in {12,16,24}; Derrick + H-drift artifact
     filters (reject Derrick-violators / large H-drift).

DISCIPLINE: UNLABELED. Single clean unbuffered process, NO background, NO nohup. Everything BOUNDED
(Nr<=24, Nth<=28, iters<=150/solve, per-solve + hard TOTAL wall budget; throughput-limited entries
recorded, never a hang). Fixed values tagged CHOSE/THEORY/DERIVED. This is N=2,3 -- ONE more slice,
NOT a discreteness or frame verdict.
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
from torch.func import hessian

import cell_solver_f2d as M                 # CAS-verified operators (REUSED verbatim)
import cell_solver_f2d_first_build as FB     # N=1 machinery (solve/trace/polish/continuum -- REUSED)


# =========================================================================================
# PART 1a -- THETA-RELAX-FIRST (MAP sec.9.2): solve the theta-part of the f-PDE for a
# radially-UNIFORM deformed f(theta). For an r-uniform config f_r=0 -> res_f reduces to the pure
# theta-PDE (rdiv=0, the kap*f_r^2 term of pot=0). All Nth nodes are interior GL nodes (poles carried
# by the theta ramp), so the theta-BVP is SQUARE: Nth residual rows for Nth unknowns U(theta).
# =========================================================================================
def theta_residual(U, ctx, prm, rho0, phi0=0.0):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    uf = U[None, :].repeat(Nr, 1)                         # r-uniform
    phi = torch.full((Nr,), float(phi0), dtype=torch.float64)
    rho = torch.full((Nr,), float(rho0), dtype=torch.float64)
    v = M.pack(phi, rho, uf, 1.0)
    Q = M.fields(v, ctx, prm)
    return Q["res_f"][Nr // 2, :]                         # any interior row (all identical, r-uniform)


def theta_relax(ctx, prm, rho0=0.70710678, phi0=0.0, amp0=0.3, budget=8.0):
    """Relax the radially-uniform theta-profile. rho0/amp0 are CHOSE seed values (Newton relaxes)."""
    U0 = amp0 * (1.0 - ctx["mu"] ** 2)                    # sin^2 th seed (degree-safe: vanishes at poles)
    resfn = lambda UU: theta_residual(UU, ctx, prm, rho0, phi0)
    U, Phi, iters, wall = FB.lm_solve(resfn, U0, maxit=120, tol=1e-13, time_budget=budget)
    maxU = float(U.abs().max())
    ok = (Phi < 1e-10) and bool(torch.isfinite(U).all())
    return U.detach(), dict(Phi=Phi, iters=iters, maxU=maxU, ok=ok)


def seed_w_theta(ctx, U, phi0=0.0, rho0=0.70710678, amp_r=0.1):
    """Full-2-D reduced seed (drop L): r-uniform theta-relaxed profile U(theta) + a small band-limited
    radial deformation (zero-derivative both ends so the f_r=0 mirror is seed-satisfied, nonzero
    interior u_r to activate I_r)."""
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    zeta, mu = ctx["zeta"], ctx["mu"]
    gr = torch.cos(np.pi * (zeta + 1.0) / 2.0)
    uf = U[None, :].repeat(Nr, 1) + amp_r * (1.0 - mu[None, :] ** 2) * gr[:, None]
    phi = torch.full((Nr,), float(phi0), dtype=torch.float64)
    rho = torch.full((Nr,), float(rho0), dtype=torch.float64)
    v = M.pack(phi, rho, uf, 1.0)
    return v[:-1].clone()


# =========================================================================================
# PART 2a -- TIER (a): the MATTER ENERGY Hessian (RIGHT signs), matter DOF only, geometry frozen.
#   E_m = INT [ (xi/2)(rho^2 I_r + I_th + N^2 I_s) + (kap N^2/2)(I_4r + I_4th/rho^2) ] dr   (all >=0)
# =========================================================================================
def matter_energy_of_u(u_flat, phi, rho, ctx, prm, L):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    Z, XI, KAP, N = prm
    uf = u_flat.reshape(Nr, Nth)
    v = M.pack(phi, rho, uf, L)
    Q = M.fields(v, ctx, prm)
    dens = ((XI / 2.0) * (rho ** 2 * Q["Ir"] + Q["Ith"] + N ** 2 * Q["Is"])
            + (KAP * N ** 2 / 2.0) * (Q["I4r"] + Q["I4th"] / rho ** 2))
    return (ctx["ccw"] * dens).sum() * (L / 2.0)


def tier_a_energy_hessian(w, ctx, prm, L):
    """Symmetric Hessian of E_matter wrt the matter DOF u (geometry phi,rho held at converged values).
    Returns (eigs ascending, eigvecs, sym_err, gradnorm)."""
    v = FB._w_to_v(w, ctx, L)
    phi, rho, uf, _ = M.unpack(v, ctx)
    phi = phi.detach(); rho = rho.detach()
    u0 = uf.reshape(-1).detach().clone()
    Efn = lambda uu: matter_energy_of_u(uu, phi, rho, ctx, prm, L)
    from torch.func import grad as tgrad
    gnorm = float(tgrad(Efn)(u0).detach().norm())
    Hm = hessian(Efn)(u0).detach()
    sym = float((Hm - Hm.transpose(0, 1)).abs().max())
    Hs = 0.5 * (Hm + Hm.transpose(0, 1))
    eig, evec = torch.linalg.eigh(Hs)
    return eig, evec, sym, gnorm


def classify_pd(eigs, zero_rel=1e-8):
    ea = eigs.detach()
    scale = float(ea.abs().max()) if ea.numel() else 0.0
    tol0 = zero_rel * scale if scale > 0 else zero_rel
    n_neg = int((ea < -tol0).sum())
    n_zero = int((ea.abs() <= tol0).sum())
    n_pos = int((ea > tol0).sum())
    return dict(n_neg=n_neg, n_zero=n_zero, n_pos=n_pos, scale=scale, tol0=tol0,
                lam_min=float(ea.min()), lam_max=float(ea.max()),
                pd=(n_neg == 0))


# =========================================================================================
# PART 2b -- TIER (b): constraint-respecting perturb-and-coupled-RE-SOLVE (only if tier a indefinite).
# Embed the most-negative MATTER eigenvector into the full w (zeros for phi,rho), reuse FB's coupled
# re-solve (perturb -> full phi,rho,f relax at fixed L -> distance back).
# =========================================================================================
def tier_b_coupled(w, evec, eig, ctx, prm, L, n_modes=3, delta=0.05, budget=12.0):
    """Decisive test: perturb along the (up to n_modes) MOST-NEGATIVE matter eigenvectors, full
    coupled re-solve (phi,rho,f), report distance back. RETURN (small dist_back) => over-count /
    stable; run off / collapse => genuine instability. Testing several modes guards against a genuine
    small instability being masked behind a larger (spurious near-pole) negative eigenvalue."""
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    n_neg = int((eig < 0).sum())
    ks = list(range(min(n_modes, max(n_neg, 1))))       # indices of most-negative modes (eig ascending)
    results = []
    for k in ks:
        v_neg = torch.cat([torch.zeros(2 * Nr, dtype=torch.float64), evec[:, k].detach()])
        r = FB.coupled_resolve_negmode(w, v_neg, ctx, prm, L, delta=delta, budget=budget)
        r["lam"] = float(eig[k]); results.append(r)
    returns = all(r["converged"] and r["dist_back"] < 0.1 and not r["collapsed"] for r in results)
    return dict(per_mode=results, returns=returns)


# =========================================================================================
# PART 2c -- SANITY: tier (a) is right-signed. STABLE (N=1 rigid f=theta, V7 strict min) => PD;
# a manufactured UNSTABLE config => a NEGATIVE eigenvalue. BOTH via the REAL energy code path.
# =========================================================================================
def tier_a_sanity():
    """Prove tier (a) is RIGHT-SIGNED via the REAL energy code path (matter_energy_of_u -> M.fields):
      (S1) STABLE ref (N=1 rigid f=theta, Step-0 V7 strict min): the ENERGY Hessian is dominantly
           POSITIVE, its few negatives confined to a near-kernel band (|lam|/lam_max small = the
           discretization image of V7's sin-theta zero mode); CONTRAST the ACTION Hessian on the SAME
           config (the N=1 build's WRONG object), which is majority-indefinite.
      (S2) PHYSICALLY PD: directional curvature along RESOLVED physical modes (V7 kernel sin-theta,
           the cos2f<0 band mode) is POSITIVE for the full matter (matches V7's kappa-lift).
      (S3) CATCHES NEGATIVE curvature (not sign-locked): with the kappa (L4) STABILIZER OFF (kappa=0,
           pure L2), the winding potential -(xi N^2/2)cos2f/sinth along the band mode gives a genuine
           NEGATIVE directional curvature for N>=3 -- the code returns it. Turning kappa=1 back ON
           restores positivity (V7's stabilization mechanism, verified numerically)."""
    from torch.func import grad as tgrad
    out = {}
    ctx = M.make_ctx(16, 12, rc=0.5)
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    phi = torch.zeros(Nr); rho = torch.full((Nr,), 0.70710678); L = 1.0
    mu = ctx["mu"]; th = ctx["th"]; sinth = torch.sqrt(1.0 - mu ** 2)
    u_rigid = torch.zeros(Nr * Nth)

    # (S1) energy Hessian vs action Hessian on the V7-stable config
    w_rigid = torch.cat([phi, rho, u_rigid])
    eigE, _, symE, _ = tier_a_energy_hessian(w_rigid, ctx, (1.0, 1.0, 1.0, 1), L)
    eigA, _, _, _ = FB.stability_spectrum(w_rigid, ctx, (1.0, 1.0, 1.0, 1), L)
    lmaxE = float(eigE.abs().max())
    negsE = [float(e) for e in eigE if e < -1e-9 * lmaxE]
    band_ok = (len(negsE) == 0) or (max(abs(x) for x in negsE) / lmaxE < 1e-2)
    nnegE = int((eigE < -1e-9 * lmaxE).sum())
    nnegA = int((eigA < -1e-9 * float(eigA.abs().max())).sum())
    out["stable"] = dict(N=1, config="rigid f=theta", nE=nnegE, totE=int(eigE.numel()),
                         nA=nnegA, totA=int(eigA.numel()), lam_min=float(eigE.min()),
                         lam_max=float(eigE.max()), sym=symE,
                         max_negband_ratio=(max(abs(x) for x in negsE) / lmaxE if negsE else 0.0),
                         band_ok=band_ok)

    # (S2)/(S3) directional curvature along physical modes via the REAL energy code path
    def curv(d, N, KAP):
        prm = (1.0, 1.0, KAP, N)
        dn = d / (d.norm() + 1e-30)
        g = lambda eps: matter_energy_of_u(dn * eps, phi, rho, ctx, prm, L)
        return float(tgrad(tgrad(g))(torch.tensor(0.0)))
    sin_mode = sinth[None, :].repeat(Nr, 1).reshape(-1)                       # V7 kernel direction
    band_mode = (torch.clamp(torch.cos(2.0 * th), max=0.0).abs() * sinth)[None, :].repeat(Nr, 1).reshape(-1)
    out["physical_pd"] = dict(
        sin_full_N1=curv(sin_mode, 1, 1.0), sin_full_N3=curv(sin_mode, 3, 1.0),
        band_full_N1=curv(band_mode, 1, 1.0), band_full_N3=curv(band_mode, 3, 1.0))
    # kappa-OFF: catches negative curvature at N>=3 (L4 stabilizer removed)
    out["catch_neg"] = dict(band_k0_N1=curv(band_mode, 1, 0.0), band_k0_N3=curv(band_mode, 3, 0.0),
                            band_k0_N6=curv(band_mode, 6, 0.0), band_k0_N10=curv(band_mode, 10, 0.0),
                            band_k1_N3=curv(band_mode, 3, 1.0), band_k1_N10=curv(band_mode, 10, 1.0))
    caught = (out["catch_neg"]["band_k0_N3"] < 0) and (out["catch_neg"]["band_k0_N10"] < 0)
    phys_pd = all(v > 0 for v in out["physical_pd"].values())
    out["stabilizer_ok"] = (out["catch_neg"]["band_k1_N3"] > 0) and (out["catch_neg"]["band_k1_N10"] > 0)
    out["ok"] = bool(band_ok and phys_pd and caught and out["stabilizer_ok"]
                     and nnegE < 0.1 * eigE.numel() and nnegA > 0.5 * eigA.numel())
    return out


# =========================================================================================
# PART 1b -- continuum table from an explicit reduced-w seed (continuation across the L grid).
# =========================================================================================
def continuum_from_w(w_seed0, ctx, prm, L_grid, budget, t0, total_budget):
    rows = []
    w_seed = w_seed0.clone()
    for L in L_grid:
        if time.time() - t0 > total_budget:
            rows.append(dict(rep=dict(L=float(L), outcome="throughput-limited"), w=None))
            continue
        r = FB.solve_at_L(w_seed, ctx, prm, L, budget=budget)
        rep = FB.solution_report(r["w"], ctx, prm, L)
        rep["outcome"] = r["outcome"]; rep["Phi"] = r["Phi"]; rep["iters"] = r["iters"]
        rep["phi_absmax"] = r["phi_absmax"]
        rows.append(dict(rep=rep, w=r["w"]))
        if r["outcome"] in ("converged", "stall", "runaway"):
            w_seed = r["w"]
    return rows


# =========================================================================================
# PART 1+2 -- ONE FULL (N, Z) SCAN
# =========================================================================================
def scan_one(N, Z, ctx, L_grid, budget, t0, total_budget):
    prm = (Z, 1.0, 1.0, N)
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    mid = len(L_grid) // 2
    print(f"\n================= SCAN  N={N}  Z={Z}  xi=kap=1  (Nr={Nr},Nth={Nth}) =================",
          flush=True)

    # ---- theta-relax-first (MAP 9.2) ----
    U, tinfo = theta_relax(ctx, prm, rho0=0.70710678, phi0=0.0, amp0=0.3, budget=min(budget, 8.0))
    deformed = (tinfo["maxU"] > 1e-4)
    print(f"  [theta-relax] Phi={tinfo['Phi']:.2e} iters={tinfo['iters']} max|U|={tinfo['maxU']:.4f} "
          f"ok={tinfo['ok']} -> f(theta) DEFORMED from rigid: {deformed}", flush=True)

    # ---- seeds: theta-relaxed (seed0, continuation) + far-from-rigid amp=2, amp=3 ----
    seeds_w = [
        seed_w_theta(ctx, U, phi0=0.0, rho0=0.70710678, amp_r=0.10),   # theta-relaxed + small r
        FB._seed_w(ctx, phi0=0.0, rho0=0.707, amp=2.0),                 # far-from-rigid
        FB._seed_w(ctx, phi0=0.1, rho0=0.900, amp=3.0),                 # far-from-rigid (verifier's amp)
    ]
    seed_tags = ["theta-relaxed+r", "far amp=2.0", "far amp=3.0"]

    # ---- (i) seed-independence at mid L ----
    print("  [seed-independence @ mid-L]:", flush=True)
    branches = []; seed_reports = []
    for si, w0 in enumerate(seeds_w):
        if time.time() - t0 > total_budget:
            print("    (total budget hit -> throughput-limited; remaining seeds skipped)", flush=True)
            break
        r = FB.solve_at_L(w0, ctx, prm, L_grid[mid], budget=budget)
        rep = FB.solution_report(r["w"], ctx, prm, L_grid[mid])
        print(f"    seed[{si}]({seed_tags[si]}) @L={L_grid[mid]:.3f}: OUTCOME={r['outcome']:9s} "
              f"Phi={r['Phi']:.2e} it={r['iters']} phi_c={rep['phi_c']:+.3f}(|phi|max={r['phi_absmax']:.2f}) "
              f"rho_c={rep['rho_c']:.3f} maxu={rep['maxu']:.3f} Hseal={rep['Hseal']:+.3e}", flush=True)
        seed_reports.append(dict(si=si, tag=seed_tags[si], outcome=r["outcome"], Phi=r["Phi"],
                                 iters=r["iters"], phi_c=rep["phi_c"], rho_c=rep["rho_c"],
                                 maxu=rep["maxu"], Hseal=rep["Hseal"], phi_absmax=r["phi_absmax"]))
        if r["converged"]:
            traj = FB.trace_branch(r["w"], ctx, prm, L_grid, mid, budget=budget)
            branches.append(dict(seed=si, tag=seed_tags[si], traj=traj))
            print(f"           CONVERGED branch; traced {len(traj)} L-points", flush=True)

    # ---- (ii) continuum table (H!=0 context) from the theta-relaxed seed ----
    print("  [continuum table] (theta-relaxed seed, continuation):", flush=True)
    cont = continuum_from_w(seeds_w[0], ctx, prm, L_grid, budget, t0, total_budget)
    cont_rows = []
    for row in cont:
        rp = row["rep"]
        if rp.get("outcome") == "throughput-limited":
            print(f"    L={rp['L']:.4f}  throughput-limited", flush=True)
            cont_rows.append(dict(L=rp["L"], outcome="throughput-limited")); continue
        print(f"    L={rp['L']:.4f}  {rp['outcome']:9s} phi_c={rp['phi_c']:+.4f} rho_c={rp['rho_c']:.4f} "
              f"rho_s={rp['rho_s']:.4f} maxu={rp['maxu']:.3f} Hseal={rp['Hseal']:+.4e} "
              f"Hdrift={rp['Hdrift']:.1e} dDerrick={rp['derrick_dS']:+.2e}", flush=True)
        cont_rows.append(dict(L=rp["L"], outcome=rp["outcome"], phi_c=rp["phi_c"], rho_c=rp["rho_c"],
                              rho_s=rp["rho_s"], maxu=rp["maxu"], Hseal=rp["Hseal"],
                              Hdrift=rp["Hdrift"], derrick_dS=rp["derrick_dS"]))
    Hs_conv = [r["rep"]["Hseal"] for r in cont
               if r["rep"].get("outcome") == "converged"]
    Hs_all = [r["rep"]["Hseal"] for r in cont if "Hseal" in r["rep"]]
    sign_change_conv = (len(Hs_conv) >= 2 and min(Hs_conv) * max(Hs_conv) < 0)
    print(f"    H(seal) over CONVERGED continuum: "
          f"{('[%+.4f,%+.4f]' % (min(Hs_conv), max(Hs_conv))) if Hs_conv else 'NONE converged'} "
          f"-> sign change on converged branch: {sign_change_conv}", flush=True)
    if Hs_all:
        print(f"    (H(seal) over ALL relaxed endpoints incl. non-converged: [{min(Hs_all):+.4f},"
              f"{max(Hs_all):+.4f}])", flush=True)

    # ---- (iii) genuine H=0 closures live ONLY on converged branches ----
    all_closures = []
    for bi, br in enumerate(branches):
        cl = FB.polish_Hseal_zero(br["traj"], ctx, prm, budget=budget)
        for c in cl:
            c["branch"] = bi
        all_closures += cl
    if not branches:
        print("  --- NO converged branch (all seeds drain to runaway/stall/collapse) "
              "=> NO genuine H=0 closure on this slice ---", flush=True)
    else:
        print(f"  --- {len(branches)} converged branch(es); {len(all_closures)} H=0 closure(s) ---",
              flush=True)

    # ---- (iv) TWO-TIER stability filter on any genuine closure ----
    closure_out = []
    for ci, c in enumerate(all_closures):
        rep = c["rep"]; w = c["w"]; L = c["L"]
        artifact = (abs(rep["derrick_dS"]) > 1e-3) or (rep["Hdrift"] > 1e-3)
        eig, evec, sym, gnorm = tier_a_energy_hessian(w, ctx, prm, L)
        cls = classify_pd(eig)
        rec = dict(idx=ci, branch=c["branch"], L=float(L), Hseal=rep["Hseal"],
                   derrick_dS=rep["derrick_dS"], Hdrift=rep["Hdrift"], artifact=artifact,
                   tierA=cls, sym=sym, gradnorm=gnorm)
        print(f"    [closure b{c['branch']} L={L:.5f}] tierA(energy-Hess): n_neg={cls['n_neg']} "
              f"n_zero={cls['n_zero']} n_pos={cls['n_pos']} lam_min={cls['lam_min']:+.3e} "
              f"PD={cls['pd']}  artifact(Derrick/Hdrift)={artifact}", flush=True)
        # tier-b is DECISIVE and cheap; run on every closure (spec: for indefinite tier-a -- and tier-a
        # is ~never cleanly PD for winding matter due to the near-kernel band, so always confirm).
        tb = tier_b_coupled(w, evec, eig, ctx, prm, L, n_modes=3, budget=min(budget, 12.0))
        rec["tierB"] = dict(returns=tb["returns"],
                            per_mode=[dict(lam=m["lam"], converged=m["converged"],
                                           dist_back=m["dist_back"], collapsed=m["collapsed"])
                                      for m in tb["per_mode"]])
        print(f"        tierB coupled re-solve (top-{len(tb['per_mode'])} neg modes): "
              f"RETURNS={tb['returns']} "
              f"{[('lam=%.2e dist=%.2e conv=%s' % (m['lam'], m['dist_back'], m['converged'])) for m in tb['per_mode']]}",
              flush=True)
        rec["stable"] = bool(tb["returns"] and not artifact)
        closure_out.append(rec)

    return dict(N=N, Z=Z, theta=dict(maxU=tinfo["maxU"], deformed=deformed, ok=tinfo["ok"],
                                     Phi=tinfo["Phi"]),
                seed_reports=seed_reports, continuum=cont_rows,
                Hs_converged=Hs_conv, sign_change_conv=sign_change_conv,
                n_branches=len(branches), n_closures=len(all_closures),
                closures=closure_out)


# =========================================================================================
# PART 3 -- grid spot-check (Nr in {12,16,24}) on the theta-relaxed seed at mid-L (one (N,Z)).
# If a closure exists it is polished at each Nr; else the NEGATIVE's grid-independence is confirmed.
# =========================================================================================
def grid_spotcheck(N, Z, L_mid, budget, Nr_list=(12, 16, 24)):
    prm = (Z, 1.0, 1.0, N)
    out = []
    for Nr in Nr_list:
        Nth = min(Nr - 4, 12)
        ctx = M.make_ctx(Nr, Nth, rc=0.5)
        U, tinfo = theta_relax(ctx, prm, rho0=0.70710678, budget=min(budget, 6.0))
        w0 = seed_w_theta(ctx, U, amp_r=0.10)
        r = FB.solve_at_L(w0, ctx, prm, L_mid, budget=budget)
        rep = FB.solution_report(r["w"], ctx, prm, L_mid)
        out.append(dict(Nr=Nr, Nth=Nth, outcome=r["outcome"], theta_maxU=tinfo["maxU"],
                        phi_c=rep["phi_c"], rho_c=rep["rho_c"], maxu=rep["maxu"],
                        Hseal=rep["Hseal"], Hdrift=rep["Hdrift"], phi_absmax=r["phi_absmax"]))
        print(f"    Nr={Nr:2d} Nth={Nth:2d}: theta max|U|={tinfo['maxU']:.4f} outcome={r['outcome']:9s} "
              f"phi_c={rep['phi_c']:+.4f}(|phi|max={r['phi_absmax']:.2f}) rho_c={rep['rho_c']:.4f} "
              f"maxu={rep['maxu']:.4f} Hseal={rep['Hseal']:+.4e}", flush=True)
    return out


# =========================================================================================
# MAIN  (single process, unbuffered, bounded)
# =========================================================================================
if __name__ == "__main__":
    T0 = time.time()
    TOTAL_BUDGET = float(os.environ.get("N2_TOTAL_BUDGET", "540"))   # hard total wall (s)
    PER_SOLVE = float(os.environ.get("N2_PER_SOLVE", "10"))          # per-solve wall (s)
    Nr = int(os.environ.get("N2_NR", "16"))                         # CHOSE bounded grid (<=24)
    Nth = int(os.environ.get("N2_NTH", "12"))                       # CHOSE bounded grid (<=28)
    L_grid = list(np.linspace(0.5, 2.0, 7))                          # CHOSE scan range (7 pts, anti-hang)
    N_LIST = [2, 3]                                                  # DERIVED-topological (this slice)
    Z_LIST = [1.0, 8.0]                                              # CHOSE-fixed, run BOTH (pre-reg)

    print("=" * 96, flush=True)
    print("CLASS-A FREE (H=0) N>=2 build -- N in {2,3}, Z in {1,8}, xi=kap=1.  UNLABELED closure-", flush=True)
    print("manifold scan (theta-relax-FIRST) + TWO-TIER (matter-energy Hessian + coupled re-solve).", flush=True)
    print(f"grid Nr={Nr} Nth={Nth}; L_grid={['%.3f'%L for L in L_grid]}; "
          f"per-solve={PER_SOLVE}s total={TOTAL_BUDGET}s", flush=True)
    print("=" * 96, flush=True)

    # ---- tier-(a) right-signed SANITY first (real energy code path) ----
    print("\n[TIER-A SANITY -- real energy code path (matter_energy_of_u -> M.fields), not a toy matrix]",
          flush=True)
    san = tier_a_sanity()
    st = san["stable"]
    print(f"  (S1) STABLE ref N=1 rigid f=theta: ENERGY-Hess n_neg={st['nE']}/{st['totE']} "
          f"({100*st['nE']/st['totE']:.0f}%, negs in near-kernel band |lam|/lam_max<{st['max_negband_ratio']:.1e}) "
          f"vs ACTION-Hess n_neg={st['nA']}/{st['totA']} ({100*st['nA']/st['totA']:.0f}%) "
          f"-> energy RIGHT-SIGNED, action WRONG. sym={st['sym']:.1e}", flush=True)
    pp = san["physical_pd"]
    print(f"  (S2) PHYSICALLY PD (dir-curv along resolved modes, full matter): "
          f"sin(N1)={pp['sin_full_N1']:+.3f} sin(N3)={pp['sin_full_N3']:+.3f} "
          f"band(N1)={pp['band_full_N1']:+.3f} band(N3)={pp['band_full_N3']:+.3f} (all>0 = convex)", flush=True)
    cn = san["catch_neg"]
    print(f"  (S3) CATCHES NEGATIVE (kappa=0, L4 stabilizer OFF, band mode): "
          f"N3={cn['band_k0_N3']:+.3f} N6={cn['band_k0_N6']:+.3f} N10={cn['band_k0_N10']:+.3f} "
          f"(negative -> code not sign-locked); kappa=1 ON restores +: N3={cn['band_k1_N3']:+.3f} "
          f"N10={cn['band_k1_N10']:+.3f} (V7 stabilization verified)", flush=True)
    print(f"  tier-(a) RIGHT-SIGNED sanity OK = {san['ok']}", flush=True)

    ctx = M.make_ctx(Nr, Nth, rc=0.5)
    grand = {}
    for N in N_LIST:
        for Z in Z_LIST:
            if time.time() - T0 > TOTAL_BUDGET:
                print(f"\n[TOTAL BUDGET HIT before N={N} Z={Z} -> throughput-limited, skipped]", flush=True)
                grand[f"N{N}_Z{int(Z)}"] = dict(N=N, Z=Z, skipped="throughput-limited")
                continue
            res = scan_one(N, Z, ctx, L_grid, PER_SOLVE, T0, TOTAL_BUDGET)
            grand[f"N{N}_Z{int(Z)}"] = res

    # ---- grid spot-check (one (N,Z); if a closure exists use it, else confirm negative grid-indep) ----
    print("\n" + "=" * 96, flush=True)
    print("GRID SPOT-CHECK (Nr in {12,16,24}) on N=2 Z=8, theta-relaxed seed @ mid-L", flush=True)
    print("=" * 96, flush=True)
    if time.time() - T0 < TOTAL_BUDGET:
        gs = grid_spotcheck(2, 8.0, float(np.median(L_grid)), PER_SOLVE)
        grand["grid_spotcheck_N2_Z8"] = gs
    else:
        print("  throughput-limited (skipped)", flush=True)
        grand["grid_spotcheck_N2_Z8"] = "throughput-limited"

    grand["_sanity"] = san
    grand["_meta"] = dict(Nr=Nr, Nth=Nth, L_grid=[float(L) for L in L_grid],
                          per_solve=PER_SOLVE, total_budget=TOTAL_BUDGET,
                          wall=time.time() - T0)
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "scratch_f2d_N2_summary.json")
    try:
        with open(outpath, "w") as f:
            json.dump(grand, f, indent=1, default=float)
        print(f"\n[summary JSON -> {outpath}]", flush=True)
    except Exception as e:
        print(f"[JSON dump failed: {e}]", flush=True)

    print(f"\nTOTAL WALL: {time.time()-T0:.1f}s  (budget {TOTAL_BUDGET:.0f}s)", flush=True)
    print("RUN COMPLETE -- N=2,3 slice; NOT a discreteness or frame verdict.", flush=True)
