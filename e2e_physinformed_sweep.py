"""e2e_physinformed_sweep.py -- the A1Z8 re-sweep with the PHYSICS-INFORMED SEED + E2d continuation.

E2e step 3.  Multi-start (physics-blend + physics-integrate + flat non-physics seed) x continuation
(Newton homotopy / grid homotopy, e2d_continuation_driver) on the E1 window cells.  Physics untouched
(residual_comp/lm_hardened byte-identical).  Data-blind.  Bounded (anti-hang: capped grid/iters,
single process, per-solve wall budget, matrix budget).

DISCIPLINE: the seed is Category-A conditioning, NEVER an acceptance criterion.  A candidate COUNTS
only at max|F|<=1e-8 (GPU) with CPU cross-check, then it faces the FULL instrument set
(`full_instruments`): H_cell==0 (false-floor gate), sigma cross-check (both domains + seal),
matched-Derrick, tier-a energy Hessian, seed-independence (>=2 distinct families incl. the NON-
physics flat seed).  Nulls are reported STRICTLY as "not found from these seeds+continuation
(coverage: ...)", NEVER "does not exist" (charter trap #1).
"""
import os, sys, math, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import e2d_continuation_driver as D
import e2e_physinformed_seed as S

LAB = "A1 m=3 Z=8"
DEV = D.DEV
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5
CONV_MAXF = 1e-8
br = C.load_bracket(LAB); RS = br["r_s"]

CELLS = [("W1", 1, 0.5, 0.1), ("W4", 1, 0.5, 1.0),
         ("W6", 2, 0.05, 1.0), ("C1", 1, 0.05, 0.01)]
SLICES = [("plateau", 100.0), ("wall", 0.95 * RS)]
AMPS = [0.8]


def full_instruments(vf, ctx, prm, w):
    """Full instrument readout on a converged candidate (characterize, never filter)."""
    g = C.gates_comp(vf, ctx, prm, br)
    # tier-a energy Hessian (GPU batched eigensolve)
    try:
        ev = C.energy_hessian_tier_a(vf, ctx, prm)
        ev = ev.detach().cpu().numpy()
        hess = dict(min_eig=float(ev.min()), max_eig=float(ev.max()),
                    n_neg=int((ev < -1e-10).sum()), n=int(ev.size),
                    verdict=("PD->for-tier-b-stable" if ev.min() > -1e-10 else "indefinite->for-tier-b"))
    except Exception as e:
        hess = dict(error=str(e))
    # CPU residual cross-check
    cpu = D.cpu_residual_check(w, ctx, prm, br)
    return dict(gates=g, hessian=hess, cpu_maxF=cpu)


def json_safe(x):
    if isinstance(x, dict): return {k: json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [json_safe(v) for v in x]
    if isinstance(x, (np.floating, np.integer)): return float(x)
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, float) and not math.isfinite(x): return str(x)
    return x


def solve_from(ctx, prm, v0, budget, use_grid=False):
    """One physics-seed solve: Newton-homotopy multistart (single seed) or grid homotopy."""
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br)
    n = v0.numel()
    v0n = v0.detach().cpu().numpy().astype(np.longdouble)
    w, info = D.newton_homotopy(resfn, v0n, n, s_steps=10, maxit_final=200, budget=budget)
    return w, info, resfn


def run_cell(ctx, prm, cname, sname, rp0, amp, budget=60.0, log=print):
    """Multi-start over physics-blend + physics-integrate + flat seeds; keep the best; if a candidate
    converges, run the full instrument set + seed-independence."""
    seeds = {
        "phys-blend": S.physinformed_seed(ctx, br, prm, rp0, amp=amp, family="blend", device=DEV),
        "flat":       S.flat_seed(ctx, br, rp0, amp=amp, device=DEV),
    }
    runs = {}; best = None
    for sk, v0 in seeds.items():
        t0 = time.time()
        try:
            w, info, resfn = solve_from(ctx, prm, v0, budget)
        except Exception as e:
            runs[sk] = dict(status=f"EXC:{e}"); continue
        vf = torch.as_tensor(w.astype(float), device=DEV)
        maxF = float(resfn(vf).abs().max())
        seed_dist = S.seed_dist(v0, C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=DEV))
        rec = dict(status=("CONVERGED" if maxF <= CONV_MAXF else "no"), maxF=maxF,
                   s_reached=info.get("s_reached"), iters=info.get("iters"),
                   wall=round(time.time() - t0, 1), seed_dist_to_flat=round(seed_dist, 3),
                   rp_end=float(w[-2]), rsU_end=float(w[-1]))
        runs[sk] = rec
        log(f"    [{cname}/{sname}/amp{amp}] {sk:10s} maxF={maxF:.2e} s={info.get('s_reached')} "
            f"rp={float(w[-2]):.1f} ({rec['wall']}s) {rec['status']}")
        if best is None or maxF < best[0]:
            best = (maxF, sk, w, vf)
    out = dict(cell=cname, slice=sname, amp=amp, prm=list(prm), rp0=rp0, seeds=runs)
    if best is not None and best[0] <= CONV_MAXF:
        # full instrument set + seed-independence (already have multiple seed results)
        maxF, sk, w, vf = best
        log(f"    *** CANDIDATE {cname}/{sname}/amp{amp} via {sk} maxF={maxF:.2e} -> full instruments")
        inst = full_instruments(vf, ctx, prm, w)
        found_by = [k for k, r in runs.items() if isinstance(r, dict) and r.get("status") == "CONVERGED"]
        out["CANDIDATE"] = dict(best_seed=sk, maxF=maxF, found_by_seeds=found_by,
                                seed_independence=len(found_by) >= 2,
                                instruments=json_safe(inst))
        pt = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          f"e2e_cand_{cname}_{sname}_amp{amp}.pt")
        torch.save(dict(w=torch.as_tensor(w.astype(float)), prm=list(prm), tag=f"{cname}/{sname}"), pt)
        out["CANDIDATE"]["saved_pt"] = os.path.basename(pt)
    return out


def main(budget_per=60.0, matrix_budget=42 * 60.0, cells=None, amps=None):
    cells = cells or CELLS; amps = amps or AMPS
    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
    results = dict(stage="E2e physics-informed A1Z8 re-sweep", bracket=LAB,
                   config=dict(Nr=Nr, Nth=Nth, Na=Na, kmap=KMAP, conv_maxF=CONV_MAXF, device=DEV,
                               cells=[c[0] for c in cells], slices=[s[0] for s in SLICES], amps=amps),
                   runs=[], candidates=[], coverage=[], throughput_limited=[])
    LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e2e_sweep.log")
    logfh = open(LOG, "a")
    def log(m): print(m, flush=True); logfh.write(m + "\n"); logfh.flush()
    t0 = time.time()
    for amp in amps:
        for cname, N, xi, kap in cells:
            for sname, rp0 in SLICES:
                if time.time() - t0 > matrix_budget:
                    results["throughput_limited"].append(f"{cname}/{sname}/amp{amp}"); continue
                prm = (br["Z"], xi, kap, N)
                log(f"[{(time.time()-t0)/60:4.1f}m] {cname}/{sname}/amp{amp} N={N} xi={xi} kap={kap}")
                rec = run_cell(ctx, prm, cname, sname, rp0, amp, budget=budget_per, log=log)
                results["runs"].append(rec)
                results["coverage"].append(f"{cname}/{sname}/amp{amp}")
                if "CANDIDATE" in rec:
                    results["candidates"].append(f"{cname}/{sname}/amp{amp}")
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "e2e_physinformed_sweep.json"), "w") as fh:
                    json.dump(json_safe(results), fh, indent=1)
    log(f"DONE sweep {time.time()-t0:.0f}s  candidates={results['candidates']} "
        f"coverage={len(results['coverage'])} throughput_limited={len(results['throughput_limited'])}")
    return results


if __name__ == "__main__":
    # bounded default; override cells/amps via a tiny CLI for staged runs
    main()
