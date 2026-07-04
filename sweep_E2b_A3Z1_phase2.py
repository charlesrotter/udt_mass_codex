"""sweep_E2b_A3Z1_phase2.py -- E2b bracket-4 FLOORING phase (observation; Category-A only).

Same protocol as brackets 1-3 (adapted from sweep_E2b_A3Z8_phase2.py):
  P2-a  for each (cell x slice): re-run the best-Phi phase-1 config with maxit=2000,
        wall<=240 s -- observe where the trajectory FLOORS (or that it doesn't).
  P2-b  ONE widened-guard observation run (r_sU < 25*r_s, per-iteration caps unchanged) on the
        best guard-presser -- measure THIS bracket's dilation exponent (so far -1.31 A1Z8,
        -0.99 A1Z1, -1.00 A3Z8; this bracket DISCRIMINATES the U_seal/wall-admissible correlate:
        prediction ~ -1.0 if it holds, a -1.3-class reading breaks it).
  P2-c  every phase-2 end state saved as .pt (recompute-on-saved discipline).
No physics knob changes: same grids, same conditions, same anchor treatment (a* HELD).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys
import json
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

REPO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO)
import cell_solver_composite as C
import sweep_E2b_A3Z1 as S

OUT = os.path.join(REPO, "microphysics_E2b_A3Z1_phase2.json")
br = S.br
RS = S.RS

with open(S.OUT_JSON) as fh:
    p1 = json.load(fh)

# best phase-1 run per (cell x slice), bulge seeds only (deterministic re-run from same seed)
best = {}
for r in p1["runs"]:
    if r.get("status") == "EXCEPTION" or "bulge" not in r["tag"]:
        continue
    cname, sname, seed = r["tag"].split("/")
    key = (cname, sname)
    if key not in best or r["Phi_end"] < best[key]["Phi_end"]:
        best[key] = r

results = dict(stage="E2b bracket sweep phase 2 (flooring)", bracket=S.LAB,
               config=dict(maxit=2000, wall=240.0, note="same grids/conditions as phase 1"),
               runs=[])

def save():
    with open(OUT, "w") as fh:
        json.dump(S.json_safe(results), fh, indent=1)

ctx = C.make_ctx_comp(S.Nr, S.Nth, S.Na, kmap=S.KMAP, device=S.DEV)
S.MAXIT, S.SOLVE_WALL = 2000, 240.0

t0 = time.time()
guard_pressers = []
for (cname, sname), r in sorted(best.items()):
    amp = float(r["tag"].split("amp")[1])
    cell = p1["config"]["cells"][cname]
    prm = (br["Z"], cell["xi"], cell["kap"], cell["N"])
    rp0 = p1["config"]["slices"][sname]
    v0 = C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=S.DEV)
    tag = f"P2/{cname}/{sname}/amp{amp}"
    S.log(f"[{(time.time()-t0)/60:5.1f}m] FLOOR {tag} (N={cell['N']} xi={cell['xi']} "
          f"kap={cell['kap']} rp0={rp0:.1f}) [p1 Phi_end={r['Phi_end']:.2e}]")
    rec, vf, w = S.run_one(ctx, prm, v0, tag)
    S.log(f"  -> {rec['status']} Phi={rec['Phi_end']:.3e} maxF={rec['maxF_end']:.2e} "
          f"iters={rec['iters']} ncap={rec['ncap']} rp->{rec['rp_end']:.2f} "
          f"rsU->{rec['rsU_end']:.2f} rho_p={rec['rho_p']:.6f} U(rho_p)={rec['U_rho_p']:.6f} "
          f"dev(seed)={rec['dev_from_seed_height']:+.2e} dev(stn)={rec['dev_from_station']:+.2e} "
          f"wall={rec['wall']}s")
    S.log(f"     top blocks: {rec['top_residual_blocks']}")
    pt = os.path.join(REPO, f"E2b_A3Z1_P2_{cname}_{sname}.pt")
    torch.save(dict(w=torch.as_tensor(w.astype(float)), prm=prm, Nr=S.Nr, Nth=S.Nth,
                    Na=S.Na, kmap=S.KMAP, tag=tag), pt)
    rec["saved_pt"] = os.path.basename(pt)
    results["runs"].append(rec)
    if rec["rsU_end"] > 4.5 * RS:
        guard_pressers.append((rec["Phi_end"], cname, sname, amp))
    save()

# P2-b: ONE widened-guard observation run for the best guard-presser
if guard_pressers:
    guard_pressers.sort()
    _, cname, sname, amp = guard_pressers[0]
    cell = p1["config"]["cells"][cname]
    prm = (br["Z"], cell["xi"], cell["kap"], cell["N"])
    rp0 = p1["config"]["slices"][sname]
    v0 = C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=S.DEV)
    tag = f"P2b-wideguard/{cname}/{sname}/amp{amp}"
    S.log(f"[{(time.time()-t0)/60:5.1f}m] WIDE-GUARD OBSERVATION {tag} (r_sU < 25*r_s)")
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br)
    F0 = resfn(v0)
    w, info = S.lm_qr_capped(resfn, v0.detach().cpu().numpy().astype(np.longdouble),
                             RS * 5.0,          # scales cap (0.5*r_s/it) AND bound (25*r_s)
                             maxit=2000, time_budget=240.0, device=S.DEV, cap_frac=0.02)
    # cap_frac=0.02 on 5*RS => per-iteration boundary cap 0.1*RS (unchanged); bound = 25*RS
    vf = torch.as_tensor(w.astype(float), device=S.DEV)
    Ff = resfn(vf)
    blocks = S.block_norms(Ff.detach().cpu().numpy(), S.make_row_blocks(S.Nr, S.Nth, S.Na))
    top3 = sorted(blocks, key=lambda b: -b[2])[:3]
    g = C.gates_comp(vf, ctx, prm, br)
    phi_c, rho_c, uf, phi_a, rho_a, rp, rsU = C.unpack_comp(vf, ctx)
    rec = dict(tag=tag, Phi0=float((F0*F0).sum()), Phi_end=info["Phi"],
               maxF_end=float(Ff.abs().max()), iters=info["iters"], ncap=info["ncap"],
               stalled=info["stalled"], wall=round(info["wall"], 1),
               rp_end=float(w[-2]), rsU_end=float(w[-1]),
               rho_p=float(rho_a[0]), U_rho_p=float(S.U_of(float(rho_a[0]))),
               rho_station=float(S.RHO_STATION), rho_seed_height=float(S.RHO_SEED_HEIGHT),
               rp_traj_every50=[round(x, 2) for x in info["rp_traj"][::50]],
               rsU_traj_every50=[round(x, 2) for x in info["rsU_traj"][::50]],
               top_residual_blocks=[(n_, l2, mx) for n_, l2, mx in top3],
               gates=S.json_safe(g))
    pt = os.path.join(REPO, f"E2b_A3Z1_P2b_wideguard_{cname}_{sname}.pt")
    torch.save(dict(w=torch.as_tensor(w.astype(float)), prm=prm, Nr=S.Nr, Nth=S.Nth,
                    Na=S.Na, kmap=S.KMAP, tag=tag), pt)
    rec["saved_pt"] = os.path.basename(pt)
    results["runs"].append(rec)
    S.log(f"  -> Phi={rec['Phi_end']:.3e} maxF={rec['maxF_end']:.2e} iters={rec['iters']} "
          f"rp->{rec['rp_end']:.2f} rsU->{rec['rsU_end']:.2f} (25*r_s bound={25*RS:.0f})")
    save()

S.log(f"phase 2 done at {(time.time()-t0)/60:.1f} min")
save()
