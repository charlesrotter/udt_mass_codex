"""Thread B: MIRROR vs WR-L WALL seal for the draining f2d cell (static, bounded, ONE process, GPU).

Pre-registered arms (whole-before-slice: the two seal knobs varied INDEPENDENTLY):
  A  = mirror phi + mirror f_r=0            (control -- expect drain)
  B1 = WALL phi(r_s)=phi_wall + mirror f_r=0 (isolates: does L-pin-by-wall-depth alone stop drain?)
  B2 = mirror phi + OPEN matter seal (PDE)   (isolates: does removing the f_r=0 drain channel alone?)
  B3 = WALL phi + OPEN matter seal           (the intended Arm B)

Pre-registered tests: T1 I_r finite at high maxit? T2 L non-runaway? T3 winding Q=N? T4 control drains?
CHARACTERIZE, do not retune. NO prescribed I_r, NO new coupling, NO hard Dirichlet edge (wall = A->0
DEPTH with phi' FREE, character-borrowed from WR-L C-2026-07-09-1, macro A=1-r/X NOT imposed inside).
A_wall value is CHOSE (swept 0.3, 0.1 -> phi_wall = -0.5 ln A_wall); NOT tuned to a target I_r.
"""
import time, math, torch, cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
ASRC = -0.5  # settled, anchor-verified source coefficient

def prm_of(N, alpha):
    return (8.0, 1.0, 1.0, N) if alpha == 0.0 else (8.0, 1.0, 1.0, N, alpha, ASRC)

def phi_wall_of(A_wall):
    return -0.5 * math.log(A_wall)  # A = e^{-2 phi} = A_wall -> phi_wall

def run(tag, arm, N, alpha, Nr, Nth, maxit, A_wall=None, budget=90.0):
    ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
    prm = prm_of(N, alpha)
    u0 = M.seed(ctx)                                  # round seed (mirror-safe); Newton relaxes it
    phi_wall = phi_wall_of(A_wall) if A_wall is not None else None
    if arm == "A":
        seal = None
    elif arm == "B1":
        seal = dict(phi="wall", phi_wall=phi_wall, matter="mirror")
    elif arm == "B2":
        seal = dict(phi="mirror", matter="open")
    elif arm == "B3":
        seal = dict(phi="wall", phi_wall=phi_wall, matter="open")
    else:
        raise ValueError(arm)
    t = time.time()
    u1, hist = M.newton_lm_solve(u0, ctx, prm, maxit=maxit, verbose=False,
                                 time_budget=budget, seal=seal)
    Q = M.fields(u1, ctx, prm)
    Ir = Q["Ir"]; L = float(Q["L"]); phi = Q["phi"]
    Qw = M.winding_of_r(u1, ctx, prm)
    ro = M.readouts(u1, ctx, prm)
    rec = dict(tag=tag, arm=arm, N=N, Nr=Nr, Nth=Nth, maxit=maxit, alpha=alpha,
               A_wall=(A_wall if A_wall is not None else float("nan")),
               Phi=hist[-1], iters=len(hist) - 1, L=L,
               Ir_mean=float(Ir.mean()), Ir_max=float(Ir.max()),
               Qw_min=float(Qw.min()), Qw_max=float(Qw.max()),
               phi_c=float(phi[0]), phi_s=float(phi[-1]),
               phip_s=float(Q["phip"][-1]), q_raw=ro["q_raw"], t=time.time() - t)
    aw = f"{A_wall:.2f}" if A_wall is not None else "  - "
    print(f"{tag:18s} {arm:2s} N={N} ({Nr:2d},{Nth}) it={rec['iters']:3d}/{maxit} a={alpha:+.1f} "
          f"Aw={aw} Phi={rec['Phi']:.2e} L={L:8.4f} Ir={rec['Ir_mean']:.2e}/{rec['Ir_max']:.2e} "
          f"Q=[{rec['Qw_min']:.3f},{rec['Qw_max']:.3f}] phi=[{rec['phi_c']:+.3f},{rec['phi_s']:+.3f}] "
          f"q={rec['q_raw']:+.1e} {rec['t']:.0f}s", flush=True)
    return rec

RUNS = []
print("=== A: control (mirror phi + mirror f_r=0) ===", flush=True)
RUNS.append(run("A_it40",        "A",  1,  0.0, 16, 8, 40))
RUNS.append(run("A_it120",       "A",  1,  0.0, 16, 8, 120))
print("=== B1: WALL phi + mirror f_r=0  (L-pin only) ===", flush=True)
RUNS.append(run("B1_w0.3_it120", "B1", 1,  0.0, 16, 8, 120, A_wall=0.3))
RUNS.append(run("B1_w0.1_it120", "B1", 1,  0.0, 16, 8, 120, A_wall=0.1))
print("=== B2: mirror phi + OPEN matter seal  (drain-channel removed) ===", flush=True)
RUNS.append(run("B2_it40",       "B2", 1,  0.0, 16, 8, 40))
RUNS.append(run("B2_it120",      "B2", 1,  0.0, 16, 8, 120))
RUNS.append(run("B2_am1_it120",  "B2", 1, -1.0, 16, 8, 120))
RUNS.append(run("B2_am2_it120",  "B2", 1, -2.0, 16, 8, 120))
print("=== B3: WALL phi + OPEN matter seal  (intended Arm B) ===", flush=True)
RUNS.append(run("B3_w0.3_it40",  "B3", 1,  0.0, 16, 8, 40,  A_wall=0.3))
RUNS.append(run("B3_w0.3_it120", "B3", 1,  0.0, 16, 8, 120, A_wall=0.3))
RUNS.append(run("B3_w0.1_it120", "B3", 1,  0.0, 16, 8, 120, A_wall=0.1))
RUNS.append(run("B3_w0.3_am1",   "B3", 1, -1.0, 16, 8, 120, A_wall=0.3))
RUNS.append(run("B3_w0.3_am2",   "B3", 1, -2.0, 16, 8, 120, A_wall=0.3))
print("=== resolution + higher winding spot checks ===", flush=True)
RUNS.append(run("B3_w0.3_Nr24",  "B3", 1,  0.0, 24, 8, 120, A_wall=0.3))
RUNS.append(run("B3_w0.3_N2",    "B3", 2,  0.0, 16, 8, 120, A_wall=0.3))

print("\n=== SUMMARY TABLE ===", flush=True)
print("tag | arm | N | (Nr,Nth) | it | alpha | A_wall | Phi | L | Ir_mean | Ir_max | Q[min,max] | phi[c,s] | q_raw")
for r in RUNS:
    aw = f"{r['A_wall']:.2f}" if r['A_wall'] == r['A_wall'] else "-"
    print(f"{r['tag']} | {r['arm']} | {r['N']} | ({r['Nr']},{r['Nth']}) | {r['iters']} | {r['alpha']:+.1f} | "
          f"{aw} | {r['Phi']:.2e} | {r['L']:.4f} | {r['Ir_mean']:.2e} | {r['Ir_max']:.2e} | "
          f"[{r['Qw_min']:.3f},{r['Qw_max']:.3f}] | [{r['phi_c']:+.3f},{r['phi_s']:+.3f}] | {r['q_raw']:+.2e}")
print("\nDONE", flush=True)
