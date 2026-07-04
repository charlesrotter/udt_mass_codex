"""e2d_mms_fieldaxis_certification.py -- CERTIFY the E2d continuation+multi-start driver on the
MMS FIELD-AXIS problem BEFORE any real re-sweep (charter §5 E2d step 2; solver-first: prove the
tool before spending it).

The E2c certification fixed the BOUNDARY (soft-dilation) axis to radius >=30 but left the FIELD axis
UNCERTIFIED (single-shot lm_hardened stalls at spurious ||F||^2 local minima for combined field
perturbations >~0.1).  This script asks: does the E2d driver (Newton homotopy + pseudo-arclength +
multi-start; independent fixed-point homotopy cross-check) REACH the field-distant manufactured
roots?

Method: forcing-subtraction MMS (exact root v* guaranteed), perturb by FIELD amounts, run each
method, and measure BOTH (i) end true-residual max|F| and (ii) distance to v* (a runaway gives
small max|F| at infinity -- a FALSE reach; the dist gate + boundary check reject it).  For the
homotopy path we also report s_max (the path's global homotopy-parameter maximum) and whether it
FOLDED before s=1 -- the diagnostic of component separation.

Bounded: production grid, capped iters/steps, single process, GPU jacrev + CPU spot-check on every
declared reach.  Data-blind (synthetic, no observational numbers).  NOT committed as a result until
blind-verified.
"""
import os, math, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import e2d_continuation_driver as D

DEV = D.DEV
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5


def build_mms(label, rp0_frac, amp, bulge=0.0):
    br = C.load_bracket(label); prm = (br["Z"], 0.5, 0.1, 1)
    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
    rp0 = rp0_frac * br["r_s"] if rp0_frac <= 1.0 else rp0_frac

    def genericize(v):
        phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
        z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
        phi_c = phi_c + 0.05 * torch.cos(math.pi * z)
        rho_c = rho_c + 0.03 * torch.sin(0.5 * math.pi * (z + 1.0))
        uf = uf + 0.05 * (1.0 - mu[None, :] ** 2) * mu[None, :] * torch.cos(math.pi * (z[:, None] + 1.0))
        uf = uf + bulge * (1.0 - mu[None, :] ** 2) * torch.sin(math.pi * (z[:, None] + 1.0) / 2.0)
        phi_a = phi_a + 0.02 * torch.sin(math.pi * h)
        rho_a = rho_a + 0.01 * h * (1.0 - h)
        return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)

    v_star = genericize(C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=DEV))
    F_star = C.residual_comp(v_star, ctx, prm, br).detach()
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star
    return dict(br=br, prm=prm, ctx=ctx, v_star=v_star, resfn=resfn, F_star=F_star,
                n=v_star.numel())


def perturb(mm, axis, sc):
    """axis in {u, phi_c, rho_c, cell (all three), ambient, boundary}."""
    ctx = mm["ctx"]; v = mm["v_star"]
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
    dr = 0.0
    if axis in ("u", "cell"):
        uf = uf + sc * (1.0 - mu[None, :] ** 2) * torch.sin(0.5 * math.pi * (z[:, None] + 1.0))
    if axis in ("phi_c", "cell"):
        phi_c = phi_c + sc * torch.sin(math.pi * (z + 1.0))
    if axis in ("rho_c", "cell"):
        rho_c = rho_c + sc * torch.cos(0.5 * math.pi * z)
    if axis == "ambient":
        phi_a = phi_a + sc * torch.sin(2 * math.pi * h) * 0.5
        rho_a = rho_a + sc * torch.cos(math.pi * h) * 0.5
    if axis == "boundary":
        dr = sc
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p) + dr, float(r_sU) + 1.1 * dr,
                       device=DEV)


def reach_metrics(mm, w):
    """True-residual max|F| (GPU) + CPU spot-check + distance-to-v* + boundary ratio."""
    n = mm["n"]; resfn = mm["resfn"]; vstar = mm["v_star"].cpu().numpy().astype(np.longdouble)
    wt = torch.as_tensor(np.asarray(w, dtype=float), device=DEV)
    maxF = float(resfn(wt).abs().max())
    # CPU independent path
    wc = torch.as_tensor(np.asarray(w, dtype=float), device="cpu")
    ctx_c = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device="cpu")
    Fc = C.residual_comp(wc, ctx_c, mm["prm"], mm["br"]) - mm["F_star"].cpu()
    maxF_cpu = float(Fc.abs().max())
    dist = float(np.abs(np.asarray(w, dtype=np.longdouble) - vstar).max())
    rp_ratio = float(abs(w[n - 2]) / abs(vstar[n - 2]))
    return maxF, maxF_cpu, dist, rp_ratio


def is_reach(maxF, maxF_cpu, dist, rp_ratio):
    """REACHED v* iff residual at floor AND near v* (not a runaway false floor)."""
    return maxF <= 1e-8 and maxF_cpu <= 1e-7 and dist < 5.0 and 0.5 < rp_ratio < 2.0


def run_case(mm, axis, sc, methods=("direct", "arclen"), budget=60.0, verbose=False):
    v0 = perturb(mm, axis, sc)
    v0n = v0.cpu().numpy().astype(np.longdouble)
    n = mm["n"]; resfn = mm["resfn"]
    seedF = float(resfn(v0).abs().max())
    dv0 = float(np.abs(v0n - mm["v_star"].cpu().numpy().astype(np.longdouble)).max())
    out = dict(axis=axis, sc=sc, seedF=seedF, seed_dist=dv0)
    for m in methods:
        t0 = time.time()
        if m == "direct":
            w, info = D._correct(resfn, v0n, n, maxit=250, budget=budget)
            extra = {}
        elif m == "arclen":
            w, info = D.arclength_homotopy(resfn, v0n, n, budget=budget, maxsteps=150,
                                           s_target=1.0, fold_abort=0.03, runaway_cap=1e5)
            extra = dict(s_max=info["s_max"], s_reached=info["s_reached"],
                         folded=bool(info["s_max"] < 0.999))
        elif m == "fp":
            w, info = D.fixedpoint_homotopy(resfn, v0n, n, budget=budget)
            extra = dict(s_reached=info["s_reached"])
        maxF, maxF_cpu, dist, rp_ratio = reach_metrics(mm, w)
        reached = is_reach(maxF, maxF_cpu, dist, rp_ratio)
        rec = dict(method=m, maxF=maxF, maxF_cpu=maxF_cpu, dist=dist, rp_ratio=rp_ratio,
                   reached=bool(reached), wall=round(time.time() - t0, 1), **extra)
        out[m] = rec
        smx = f" s_max={extra.get('s_max'):.3f}" if 's_max' in extra else ""
        print(f"  [{axis:8s} sc={sc:<5}] {m:7s} seedF={seedF:.1e} d0={dv0:5.2f} -> "
              f"maxF={maxF:.2e} cpu={maxF_cpu:.1e} dist={dist:.2e} rp={rp_ratio:.2f}{smx} "
              f"{'REACH' if reached else 'no'} ({rec['wall']}s)", flush=True)
    return out


if __name__ == "__main__":
    results = {}
    t_all = time.time()
    for tag, (lab, rpf, amp, bulge) in {
            "MMS1_A1Z8_wall": ("A1 m=3 Z=8", 0.95, 0.8, 0.0),
            "MMS2_A3Z1_plateau_bulge": ("A3 Z=1", 100.0, 0.8, 0.4)}.items():
        print(f"\n{'='*72}\n{tag}  ({lab})")
        mm = build_mms(lab, rpf, amp, bulge)
        print(f"  n={mm['n']}  root max|F(v*)|={float(mm['resfn'](mm['v_star']).abs().max()):.1e}")
        cases = []
        # (A) BOUNDARY axis spot-check -- confirm the E2c-certified axis is NOT regressed by the driver
        print(" -- BOUNDARY axis (E2c-certified >=30; driver must not regress) --")
        for dr in [10.0, 20.0, 30.0]:
            cases.append(run_case(mm, "boundary", dr, methods=("direct",), budget=60.0))
        # (B) FIELD-axis RADIUS LADDER -- direct (single-shot) vs arclen (continuation)
        print(" -- FIELD axis radius ladder (u / cell-combined) direct vs arclength --")
        for axis in ["u", "cell"]:
            for sc in [0.05, 0.1, 0.15, 0.2, 0.3]:
                cases.append(run_case(mm, axis, sc, methods=("direct", "arclen"), budget=55.0))
        # (C) robustness: an INDEPENDENT homotopy on one field-distant case
        print(" -- robustness: fixed-point homotopy on one field-distant case (cell 0.3) --")
        cases.append(run_case(mm, "cell", 0.3, methods=("fp",), budget=90.0))
        results[tag] = dict(bracket=lab, n=mm["n"], cases=cases)
        print(f"  [{tag}] elapsed {time.time()-t_all:.0f}s")

    with open("e2d_mms_fieldaxis_certification.json", "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    print(f"\nDONE certification  total {time.time()-t_all:.0f}s  -> e2d_mms_fieldaxis_certification.json")
