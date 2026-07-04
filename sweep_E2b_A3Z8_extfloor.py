"""sweep_E2b_A3Z8_extfloor.py -- EXTENDED FLOOR on the station-parked wall state (bracket-2
conditioning note: 'extend-floor any parked state ~4000 iters before calling it finite-size' --
bracket 2's decisive diagnostic). Re-solve the saved P2/W5/wall end state for 4000 further
iterations and observe: does r_p stop (an equilibrium) or creep (slow-motion runaway)?
Read the station-lock identity along the way: rho_p, U(rho_p), shell width r_sU - r_p.
Observation only; no knob changes (same grids/conditions, a* HELD)."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys
import json
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

REPO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO)
import cell_solver_composite as C
import sweep_E2b_A3Z8 as S

br = S.br
d = torch.load(os.path.join(REPO, "E2b_A3Z8_P2_W5_wall.pt"), weights_only=False)
prm = tuple(d["prm"])
ctx = C.make_ctx_comp(d["Nr"], d["Nth"], d["Na"], kmap=d["kmap"], device=S.DEV)
v0 = d["w"].to(S.DEV)
resfn = lambda vv: C.residual_comp(vv, ctx, prm, br)
rp_start, rsU_start = float(v0[-2]), float(v0[-1])
S.log(f"EXT-FLOOR P2c-extended/W5/wall/amp0.3 from rp={rp_start:.4f} rsU={rsU_start:.4f} "
      f"width={rsU_start-rp_start:.4f}")
w, info = S.lm_qr_capped(resfn, v0.detach().cpu().numpy().astype(np.longdouble), S.RS,
                         maxit=4000, time_budget=300.0, device=S.DEV)
vf = torch.as_tensor(w.astype(float), device=S.DEV)
Ff = resfn(vf)
blocks = S.block_norms(Ff.detach().cpu().numpy(), S.make_row_blocks(d["Nr"], d["Nth"], d["Na"]))
top3 = sorted(blocks, key=lambda b: -b[2])[:3]
g = C.gates_comp(vf, ctx, prm, br)
phi_c, rho_c, uf, phi_a, rho_a, rp, rsU = C.unpack_comp(vf, ctx)
rec = dict(tag="P2c-extended/W5/wall/amp0.3", Phi_end=info["Phi"],
           maxF_end=float(Ff.abs().max()), iters=info["iters"], ncap=info["ncap"],
           stalled=info["stalled"], wall=info["wall"],
           rp_start=rp_start, rsU_start=rsU_start, width_start=rsU_start - rp_start,
           rp_end=float(w[-2]), rsU_end=float(w[-1]), width_end=float(w[-1] - w[-2]),
           rho_p=float(rho_a[0]), U_rho_p=float(S.U_of(float(rho_a[0]))),
           rho_station=float(S.RHO_STATION),
           rp_traj_every200=[round(x, 3) for x in info["rp_traj"][::200]],
           top_residual_blocks=[(n_, l2, mx) for n_, l2, mx in top3],
           gates=S.json_safe(g))
pt = os.path.join(REPO, "E2b_A3Z8_P2c_extended_W5_wall.pt")
torch.save(dict(w=torch.as_tensor(w.astype(float)), prm=prm, Nr=d["Nr"], Nth=d["Nth"],
                Na=d["Na"], kmap=d["kmap"], tag=rec["tag"]), pt)
rec["saved_pt"] = os.path.basename(pt)
with open(os.path.join(REPO, "microphysics_E2b_A3Z8_extfloor.json"), "w") as fh:
    json.dump(S.json_safe(rec), fh, indent=1)
S.log(f"  -> Phi={rec['Phi_end']:.3e} maxF={rec['maxF_end']:.2e} iters={rec['iters']} "
      f"ncap={rec['ncap']} rp {rp_start:.3f}->{rec['rp_end']:.3f} width "
      f"{rec['width_start']:.4f}->{rec['width_end']:.4f} rho_p={rec['rho_p']:.7f} "
      f"U(rho_p)={rec['U_rho_p']:.7f} H_cell_max={rec['gates']['H_cell_max']:.2f}")
