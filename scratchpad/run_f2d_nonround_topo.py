"""Thread B: non-round + topological audit of the f2d drain (static). Bounded, ONE process, GPU.
Records for each run: round/non-round, boundary/topology handling, (Nr,Nth), maxit, alpha, final |F|^2,
L, mean/max I_r, winding Q(min,max over r), max|a2| (non-round), q_raw. NO prescribed I_r. NO new coupling."""
import time, torch, cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
ASRC = -0.5  # settled, anchor-verified coefficient

def prm_of(N, alpha):
    return (8.0, 1.0, 1.0, N) if alpha == 0.0 else (8.0, 1.0, 1.0, N, alpha, ASRC)

def run(tag, round_, N, alpha, Nr, Nth, maxit, sealbc="off", a2_amp=0.0, a2_mirror=0.0, budget=90.0):
    ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
    prm = prm_of(N, alpha)
    if round_:
        u0 = M.seed(ctx); n5d = None
    else:
        u0 = M.seed_n5d(ctx, a2_amp=a2_amp); n5d = dict(sealbc=sealbc, a2_mirror=a2_mirror)
    t = time.time()
    u1, hist = M.newton_lm_solve(u0, ctx, prm, maxit=maxit, verbose=False, time_budget=budget, n5d=n5d)
    Q = M.fields(u1, ctx, prm, n5d=n5d)
    Ir = Q["Ir"]; L = float(Q["L"])
    Qw = M.winding_of_r(u1, ctx, prm, n5d=n5d)
    ro = M.readouts(u1, ctx, prm, n5d=n5d)
    a2max = float(Q["a2"].abs().max()) if n5d is not None else 0.0
    rec = dict(tag=tag, round=("round" if round_ else "nonround"), bc=(sealbc if not round_ else "mirror"),
               N=N, Nr=Nr, Nth=Nth, maxit=maxit, alpha=alpha, Phi=hist[-1], iters=len(hist) - 1,
               L=L, Ir_mean=float(Ir.mean()), Ir_max=float(Ir.max()),
               Qw_min=float(Qw.min()), Qw_max=float(Qw.max()), a2max=a2max,
               q_raw=ro["q_raw"], t=time.time() - t)
    print(f"{tag:16s} {rec['round']:8s} bc={rec['bc']:6s} N={N} ({Nr},{Nth}) it={rec['iters']:3d}/{maxit} "
          f"a={alpha:+.1f} Phi={rec['Phi']:.2e} L={L:.4f} Ir={rec['Ir_mean']:.2e}/{rec['Ir_max']:.2e} "
          f"Q=[{rec['Qw_min']:.3f},{rec['Qw_max']:.3f}] a2m={a2max:.2e} q={ro['q_raw']:+.1e} {rec['t']:.0f}s",
          flush=True)
    return rec

RUNS = []
print("=== ROUND baseline + convergence + alpha + resolution ===")
RUNS.append(run("R_a0_it40",   True, 1, 0.0, 16, 8, 40))
RUNS.append(run("R_a0_it120",  True, 1, 0.0, 16, 8, 120))
RUNS.append(run("R_am1_it120", True, 1, -1.0, 16, 8, 120))
RUNS.append(run("R_am2_it120", True, 1, -2.0, 16, 8, 120))
RUNS.append(run("R_Nr12",      True, 1, 0.0, 12, 8, 40))
RUNS.append(run("R_Nr24",      True, 1, 0.0, 24, 8, 40))
RUNS.append(run("R_Nth12",     True, 1, 0.0, 16, 12, 40))
print("=== NON-ROUND (a2 shear live, JC2 free-seal) ===")
RUNS.append(run("NR_a0_it40",  False, 1, 0.0, 16, 8, 40, sealbc="S-JC2", a2_amp=0.15))
RUNS.append(run("NR_a0_it120", False, 1, 0.0, 16, 8, 120, sealbc="S-JC2", a2_amp=0.15))
RUNS.append(run("NR_am1_it120",False, 1, -1.0, 16, 8, 120, sealbc="S-JC2", a2_amp=0.15))
print("=== NON-ROUND enforced boundary (S-Dir, a2 pinned nonzero at seal) ===")
RUNS.append(run("NRdir_it120", False, 1, 0.0, 16, 8, 120, sealbc="S-Dir", a2_amp=0.2, a2_mirror=0.2))
print("=== HIGHER WINDING N=2 ===")
RUNS.append(run("N2_round",    True, 2, 0.0, 16, 8, 120))
RUNS.append(run("N2_nonround", False, 2, 0.0, 16, 8, 120, sealbc="S-JC2", a2_amp=0.15))

print("\n=== SUMMARY TABLE ===")
hdr = "tag | round | bc | N | (Nr,Nth) | it | alpha | Phi | L | Ir_mean | Ir_max | Q[min,max] | a2max | q_raw"
print(hdr)
for r in RUNS:
    print(f"{r['tag']} | {r['round']} | {r['bc']} | {r['N']} | ({r['Nr']},{r['Nth']}) | {r['iters']} | "
          f"{r['alpha']:+.1f} | {r['Phi']:.2e} | {r['L']:.4f} | {r['Ir_mean']:.2e} | {r['Ir_max']:.2e} | "
          f"[{r['Qw_min']:.3f},{r['Qw_max']:.3f}] | {r['a2max']:.2e} | {r['q_raw']:+.2e}")
