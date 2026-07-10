"""Q3: wall-arm (phi Dirichlet at wall depth). Is the NON-CONVERGENCE a structural obstruction
or a numeric artifact?
 (a) verify Phi ~ (phi_wall - phi_s)^2 for A_wall=0.3, and that the wall-depth row dominates.
 (b) REFUTE attempts: more iters, different lam0, CONTINUATION in phi_wall (ramp A_wall 1.0->0.3),
     better seed. If ANY reaches wall depth with Phi small -> structural claim FALSE.
"""
import math, torch, cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth = 16, 8
prm = (8.0, 1.0, 1.0, 1)

def phi_wall_of(A): return -0.5 * math.log(A)

def wall_seal(A, matter="mirror"):
    return dict(phi="wall", phi_wall=phi_wall_of(A), matter=matter)

def analyze(u1, ctx, A, matter):
    """Return Phi decomposition + phi_s, and the wall-row residual."""
    seal = wall_seal(A, matter)
    F = M.residual(u1, ctx, prm, seal=seal)
    Phi = float((F*F).sum())
    Q = M.fields(u1, ctx, prm)
    phi_s = float(Q["phi"][-1]); pw = phi_wall_of(A)
    wall_row = phi_s - pw
    # locate wall row: index (Nr-2)+1 = Nr-1 (phi_ode interior Nr-2, then phi_bc[0]=phip[0], phi_bc[1]=wall)
    idx_wall = (Nr-2) + 1
    return dict(Phi=Phi, phi_s=phi_s, phi_wall=pw, wall_row=wall_row,
                wall_row_sq=wall_row**2, F_wall=float(F[idx_wall]),
                Ir_mean=float(Q["Ir"].mean()), L=float(Q["L"]),
                Fmax_abs=float(F.abs().max()), Fmax_idx=int(F.abs().argmax()))

print("=== Q3a: verify Phi ~ (phi_wall - phi_s)^2 dominance, A_wall=0.3 ===")
for matter in ["mirror", "open"]:
    for lam0 in [1e-3, 1e-1, 1e-6]:
        for mit in [120, 250]:
            ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
            u0 = M.seed(ctx)
            u1, hist = M.newton_lm_solve(u0, ctx, prm, maxit=mit, lam0=lam0, verbose=False,
                                         time_budget=120.0, seal=wall_seal(0.3, matter))
            d = analyze(u1, ctx, 0.3, matter)
            print(f"matter={matter:6s} lam0={lam0:.0e} mit={mit:3d} it={len(hist)-1:3d} "
                  f"Phi={d['Phi']:.3e} wallrow^2={d['wall_row_sq']:.3e} "
                  f"phi_s={d['phi_s']:+.4f}(target {d['phi_wall']:.4f}) "
                  f"Fmax={d['Fmax_abs']:.2e}@{d['Fmax_idx']}(wall@{(Nr-2)+1}) Ir={d['Ir_mean']:.2e} L={d['L']:.4f}")

print("\n=== Q3b: CONTINUATION in phi_wall (ramp A_wall 1.0 -> 0.3), warm-started ===")
for matter in ["mirror", "open"]:
    ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)
    u = M.seed(ctx)
    ramp = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3]
    print(f"-- matter={matter} --")
    for A in ramp:
        u, hist = M.newton_lm_solve(u, ctx, prm, maxit=120, verbose=False,
                                    time_budget=120.0, seal=wall_seal(A, matter))
        d = analyze(u, ctx, A, matter)
        reached = abs(d['wall_row']) < 1e-3
        print(f"  A={A:.2f} phi_wall={d['phi_wall']:.4f} it={len(hist)-1:3d} Phi={d['Phi']:.3e} "
              f"phi_s={d['phi_s']:+.4f} wallrow={d['wall_row']:+.3e} REACHED={reached} "
              f"Ir={d['Ir_mean']:.2e} L={d['L']:.4f}")

print("\n=== Q3c: does phi_s track ~toward wall as A decreases, or stick? (mirror) ===")
print("If phi_s climbs to meet phi_wall for MODERATE A but detaches only at deep A -> continuation")
print("boundary; if it NEVER climbs -> immediate structural block.")
