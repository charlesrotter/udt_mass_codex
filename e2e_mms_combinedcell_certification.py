"""e2e_mms_combinedcell_certification.py -- CERTIFY the PHYSICS-INFORMED SEED on the MMS
COMBINED-CELL FIELD AXIS (E2e step 2; solver-first: prove the tool before the sweep).

E2d certified boundary>=30 and u-axis~0.3 but left the COMBINED-CELL field axis (a real seed's core
phi_c/rho_c O(1) off the derived core) UNCERTIFIED.  The E2e claim: a seed built from the DERIVED
core (E_ang(core)=2) collapses that O(1) core distance to the certified small-perturbation regime, so
physics-seed + continuation REACHES field-distant roots the E2d flat seed folds short on.

METHOD (honest, non-circular):
  * v_star = a SOLUTION-SHAPED manufactured root: a PHYSICS-INFORMED base (derived core) + a generic
    bump of size `delta`.  Forcing-subtraction R(v)=residual_comp(v)-residual_comp(v_star) makes
    v_star an EXACT root REGARDLESS of how it was built (standard MMS); the seed is never an
    acceptance criterion.
  * TWO seeds are launched at each delta: the PHYSICS-INFORMED seed (sits ~delta from v_star, in the
    certified regime) and the E2d FLAT seed (sits O(1)+delta from v_star -- the uncertified combined-
    cell distance).  The certification succeeds iff the PHYSICS seed REACHES where the FLAT seed does
    NOT, i.e. the derived core bridges the combined-cell axis.
  * REACH = true-residual max|F|<=1e-8 (GPU) AND CPU spot-check<=1e-7 AND near v_star (dist<5,
    boundary ratio 0.5-2.0 -- a dilation runaway is a FALSE reach, rejected).  Same gate as E2d/E2c.

Bounded: production grid, capped iters/steps, SINGLE process, GPU jacrev + CPU spot-check.  Data-
blind.  NOT committed until blind-verified.  Physics untouched (residual_comp/lm_hardened byte-id).
"""
import os, math, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import e2d_continuation_driver as D
import e2e_physinformed_seed as S

DEV = D.DEV
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5


def generic_bump(ctx, v, delta, device=DEV):
    """Add a solution-shaped generic perturbation of size `delta` (combined-cell: phi_c+rho_c+u
    field modes, the exact E2d 'cell' axis shapes), returning a nontrivial manufactured root base."""
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(device); mu = ctx["cell"]["mu"].to(device); h = ctx["ha"].to(device)
    phi_c = phi_c + delta * torch.cos(math.pi * z)
    rho_c = rho_c + 0.6 * delta * torch.sin(0.5 * math.pi * (z + 1.0))
    uf = uf + delta * (1.0 - mu[None, :] ** 2) * mu[None, :] * torch.cos(math.pi * (z[:, None] + 1.0))
    phi_a = phi_a + 0.3 * delta * torch.sin(math.pi * h)
    rho_a = rho_a + 0.15 * delta * h * (1.0 - h)
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=device)


def build_mms(lab, N, XI, KAP, frac, delta, amp=0.8):
    """v_star = physics-informed base (derived core) + generic bump(delta)."""
    br = C.load_bracket(lab); prm = (br["Z"], XI, KAP, N)
    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
    rp0 = frac * br["r_s"]
    base = S.physinformed_seed(ctx, br, prm, rp0, amp=amp, family="blend", device=DEV)
    v_star = generic_bump(ctx, base, delta)
    F_star = C.residual_comp(v_star, ctx, prm, br).detach()
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star
    return dict(br=br, prm=prm, ctx=ctx, v_star=v_star, resfn=resfn, F_star=F_star,
                n=v_star.numel(), rp0=rp0, amp=amp)


def reach_metrics(mm, w):
    n = mm["n"]; resfn = mm["resfn"]; vstar = mm["v_star"].cpu().numpy().astype(np.longdouble)
    wt = torch.as_tensor(np.asarray(w, dtype=float), device=DEV)
    maxF = float(resfn(wt).abs().max())
    wc = torch.as_tensor(np.asarray(w, dtype=float), device="cpu")
    ctx_c = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device="cpu")
    Fc = C.residual_comp(wc, ctx_c, mm["prm"], mm["br"]) - mm["F_star"].cpu()
    maxF_cpu = float(Fc.abs().max())
    dist = float(np.abs(np.asarray(w, dtype=np.longdouble) - vstar).max())
    rp_ratio = float(abs(w[n - 2]) / abs(vstar[n - 2]))
    return maxF, maxF_cpu, dist, rp_ratio


def is_reach(maxF, maxF_cpu, dist, rp_ratio):
    return maxF <= 1e-8 and maxF_cpu <= 1e-7 and dist < 5.0 and 0.5 < rp_ratio < 2.0


def run_seed(mm, seedname, v0, methods=("direct", "arclen"), budget=45.0):
    v0n = v0.cpu().numpy().astype(np.longdouble)
    n = mm["n"]; resfn = mm["resfn"]
    seedF = float(resfn(v0).abs().max())
    d0 = float(np.abs(v0n - mm["v_star"].cpu().numpy().astype(np.longdouble)).max())
    out = dict(seed=seedname, seedF=seedF, seed_dist=d0, methods={})
    for m in methods:
        t0 = time.time()
        if m == "direct":
            w, info = D._correct(resfn, v0n, n, maxit=200, budget=budget); extra = {}
        elif m == "arclen":
            w, info = D.arclength_homotopy(resfn, v0n, n, budget=budget, maxsteps=120,
                                           s_target=1.0, fold_abort=0.03, runaway_cap=1e5)
            extra = dict(s_max=info["s_max"], folded=bool(info["s_max"] < 0.999))
        maxF, maxF_cpu, dist, rp = reach_metrics(mm, w)
        reached = is_reach(maxF, maxF_cpu, dist, rp)
        rec = dict(method=m, maxF=maxF, maxF_cpu=maxF_cpu, dist=dist, rp_ratio=rp,
                   reached=bool(reached), wall=round(time.time() - t0, 1), **extra)
        out["methods"][m] = rec
        smx = f" s_max={extra.get('s_max'):.3f}" if 's_max' in extra else ""
        print(f"    [{seedname:8s} {m:7s}] d0={d0:6.3f} seedF={seedF:.1e} -> maxF={maxF:.2e} "
              f"cpu={maxF_cpu:.1e} dist={dist:.2e} rp={rp:.2f}{smx} "
              f"{'REACH' if reached else 'no'} ({rec['wall']}s)", flush=True)
    return out


if __name__ == "__main__":
    # two MMS cells: W1-like (rho_c=0.18 -> big O(0.8) core offset) and W6-like (rho_c~1.03 -> small).
    MMS = {
        "M_W1_plateau": dict(lab="A1 m=3 Z=8", N=1, XI=0.5, KAP=0.1, frac=0.5),
        "M_W6_wall":    dict(lab="A1 m=3 Z=8", N=2, XI=0.05, KAP=1.0, frac=0.95),
    }
    DELTAS = [0.1, 0.3]
    results = {}; t_all = time.time()
    for tag, cfg in MMS.items():
        print(f"\n{'='*74}\n{tag}  ({cfg['lab']}  N={cfg['N']} xi={cfg['XI']} kap={cfg['KAP']} "
              f"frac={cfg['frac']})")
        rc_der, base = S.derived_rho_c((8.0, cfg["XI"], cfg["KAP"], cfg["N"]))
        print(f"  derived core rho_c={rc_der:.4f}")
        cell = []
        for delta in DELTAS:
            mm = build_mms(cfg["lab"], cfg["N"], cfg["XI"], cfg["KAP"], cfg["frac"], delta)
            rootF = float(mm["resfn"](mm["v_star"]).abs().max())
            print(f"  --- delta={delta}  n={mm['n']}  root max|F(v*)|={rootF:.1e} ---")
            prm, br, ctx, rp0 = mm["prm"], mm["br"], mm["ctx"], mm["rp0"]
            v_phys = S.physinformed_seed(ctx, br, prm, rp0, amp=mm["amp"], family="blend", device=DEV)
            v_flat = S.flat_seed(ctx, br, rp0, amp=mm["amp"], device=DEV)
            rec = dict(delta=delta, rootF=rootF)
            rec["phys"] = run_seed(mm, "PHYS", v_phys, methods=("direct", "arclen"))
            rec["flat"] = run_seed(mm, "FLAT", v_flat, methods=("direct", "arclen"))
            cell.append(rec)
        results[tag] = dict(cfg=cfg, rho_c_derived=rc_der, deltas=cell)
        print(f"  [{tag}] elapsed {time.time()-t_all:.0f}s")

    with open("e2e_mms_combinedcell_certification.json", "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    print(f"\nDONE certification total {time.time()-t_all:.0f}s -> e2e_mms_combinedcell_certification.json")
