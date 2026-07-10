"""Q2: B2 (mirror phi + OPEN matter seal). Is the I_r drain REAL or a false pass?
 - drive maxit up 40->120->200; does I_r drain MONOTONICALLY with Phi genuinely small?
 - is the open seal secretly still pinning f_r~0 at the seal? check f_r at seal node.
"""
import torch, cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth = 16, 8
prm = (8.0, 1.0, 1.0, 1)
seal = dict(phi="mirror", matter="open")

def solve(maxit, amp=0.02, seed_scale=None):
    ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
    u0 = M.seed(ctx, amp=amp)
    if seed_scale is not None:
        torch.manual_seed(7)
        u0 = u0 + seed_scale * torch.randn_like(u0)
    u1, hist = M.newton_lm_solve(u0, ctx, prm, maxit=maxit, verbose=False,
                                 time_budget=120.0, seal=seal)
    Q = M.fields(u1, ctx, prm)
    Ir = Q["Ir"]; fr = Q["fr"]
    return dict(Phi=hist[-1], iters=len(hist)-1, Ir_mean=float(Ir.mean()),
                Ir_max=float(Ir.max()),
                fr_seal_absmax=float(fr[-1, :].abs().max()),
                fr_interior_absmax=float(fr[1:-1, :].abs().max()),
                Ir_seal=float(Ir[-1]), L=float(Q["L"]))

print("=== B2 open-seal: maxit sweep (default seed amp=0.02) ===")
for mit in [40, 120, 200, 250]:
    r = solve(mit)
    print(f"maxit={mit:3d} it={r['iters']:3d} Phi={r['Phi']:.3e} Ir_mean={r['Ir_mean']:.3e} "
          f"Ir_max={r['Ir_max']:.3e} Ir_seal={r['Ir_seal']:.3e} "
          f"fr_seal|max|={r['fr_seal_absmax']:.3e} fr_int|max|={r['fr_interior_absmax']:.3e} L={r['L']:.4f}")

print("\n=== B2 open-seal: bigger initial matter amp (amp=0.2) -> does it STILL drain? ===")
for mit in [120, 200]:
    r = solve(mit, amp=0.2)
    print(f"amp=0.2 maxit={mit:3d} it={r['iters']:3d} Phi={r['Phi']:.3e} Ir_mean={r['Ir_mean']:.3e} "
          f"Ir_max={r['Ir_max']:.3e} fr_seal|max|={r['fr_seal_absmax']:.3e}")

print("\n=== B2 open-seal: perturbed seed (random kick) -> basin check ===")
for mit in [120, 200]:
    r = solve(mit, amp=0.1, seed_scale=0.03)
    print(f"kick maxit={mit:3d} it={r['iters']:3d} Phi={r['Phi']:.3e} Ir_mean={r['Ir_mean']:.3e} "
          f"Ir_max={r['Ir_max']:.3e} fr_seal|max|={r['fr_seal_absmax']:.3e}")

# CONTROL: mirror matter seal at same settings, to compare drain magnitude
print("\n=== CONTROL A (mirror f_r=0 both ends), same maxit ===")
def solve_mirror(maxit):
    ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
    u0 = M.seed(ctx)
    u1, hist = M.newton_lm_solve(u0, ctx, prm, maxit=maxit, verbose=False,
                                 time_budget=120.0, seal=None)
    Q = M.fields(u1, ctx, prm); Ir = Q["Ir"]
    return hist[-1], float(Ir.mean()), float(Ir.max())
for mit in [120, 200]:
    p, im, ix = solve_mirror(mit)
    print(f"A maxit={mit:3d} Phi={p:.3e} Ir_mean={im:.3e} Ir_max={ix:.3e}")
