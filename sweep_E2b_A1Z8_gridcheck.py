"""Grid cross-check (Category-A): re-run two representative configs at Nr=16, Nth=12, Na=256 --
does the runaway + C1c holdout persist at finer resolution? Observation only."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys, json, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cell_solver_composite as C
import sweep_E2b_A1Z8 as S

S.Nr, S.Nth, S.Na = 16, 12, 256
S.MAXIT, S.SOLVE_WALL = 400, 200.0
ctx = C.make_ctx_comp(S.Nr, S.Nth, S.Na, kmap=S.KMAP, device=S.DEV)
br = S.br
out = []
for cname, N, xi, kap, sname, rp0, amp in [
        ("W1", 1, 0.5, 0.1, "wall", 0.95 * S.RS, 0.8),
        ("W6", 2, 0.05, 1.0, "plateau", 100.0, 0.3)]:
    prm = (br["Z"], xi, kap, N)
    v0 = C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=S.DEV)
    tag = f"GRIDCHK-Nr16Nth12Na256/{cname}/{sname}/amp{amp}"
    S.log(f"GRIDCHECK {tag}")
    rec, vf, w = S.run_one(ctx, prm, v0, tag)
    S.log(f"  -> {rec['status']} Phi={rec['Phi_end']:.3e} maxF={rec['maxF_end']:.2e} "
          f"iters={rec['iters']} rp->{rec['rp_end']:.1f} rsU->{rec['rsU_end']:.1f} "
          f"top={rec['top_residual_blocks'][0]}")
    out.append(rec)
with open(os.path.join(S.REPO if hasattr(S,'REPO') else '.', "microphysics_E2b_A1Z8_gridcheck.json"), "w") as fh:
    json.dump(S.json_safe(out), fh, indent=1)
S.log("gridcheck done")
