"""VERIFIER-2 TASK 2: seed / solution-space completeness.
Hunt HARD for a CONVERGED (||F||^2 < 1e-4) static solution with SUSTAINED I_r (> 1e-3)
that does NOT drain as maxit increases. mirror seal (seal=None) AND open seal.
Vary seeds: amplitude up to 0.5, different radial/angular shapes, multi-start.
"""
import torch, math, numpy as np
import cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Z, XI, KAP, N = 8.0, 1.0, 1.0, 1
prm = (Z, XI, KAP, N)

def custom_seed(ctx, amp, phi0=0.0, rho0=0.7071, L0=1.0, rshape="cos", ashape="s2", seed_rng=None):
    """Build varied seeds. rshape: radial factor; ashape: angular factor (degree-safe -> vanish at poles)."""
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    zeta = ctx["zeta"]; mu = ctx["mu"]
    x = (zeta + 1.0) / 2.0  # in [0,1]
    if rshape == "cos":
        gr = torch.cos(np.pi * (zeta + 1.0) / 2.0)          # zero-slope both ends
    elif rshape == "cos2":
        gr = torch.cos(np.pi * (zeta + 1.0))                # higher radial mode
    elif rshape == "bump":
        gr = torch.sin(np.pi * x) ** 2                      # interior bump, zero-slope ends
    elif rshape == "flat":
        gr = torch.ones_like(zeta)
    else:
        raise ValueError(rshape)
    s2 = (1.0 - mu ** 2)                                     # sin^2 th
    if ashape == "s2":
        ga = s2
    elif ashape == "s2sq":
        ga = s2 ** 2
    elif ashape == "s2mu":
        ga = s2 * mu                                        # antisym-ish, still vanishes at poles
    else:
        raise ValueError(ashape)
    uf = amp * ga[None, :] * gr[:, None]
    if seed_rng is not None:
        uf = uf + seed_rng * torch.randn(Nr, Nth, dtype=torch.float64, device=zeta.device) * s2[None, :]
    dev = zeta.device
    phi = torch.full((Nr,), float(phi0), dtype=torch.float64, device=dev)
    rho = torch.full((Nr,), float(rho0), dtype=torch.float64, device=dev)
    return M.pack(phi, rho, uf, float(L0))

torch.manual_seed(1234)
Nr, Nth = 16, 8
ctx = M.make_ctx(Nr, Nth, rc=0.5, device=DEV)

SEALS = {"mirror": None, "open": dict(phi="mirror", matter="open")}

cases = []
# amplitude ladder + shape variety + multi-start random
for amp in [0.05, 0.2, 0.4, 0.5]:
    cases.append(dict(amp=amp, rshape="cos", ashape="s2", L0=1.0))
cases += [
    dict(amp=0.3, rshape="cos2", ashape="s2",  L0=1.0),
    dict(amp=0.3, rshape="bump", ashape="s2",  L0=1.0),
    dict(amp=0.3, rshape="cos",  ashape="s2sq",L0=1.0),
    dict(amp=0.3, rshape="cos",  ashape="s2",  L0=3.0),   # larger box
    dict(amp=0.4, rshape="bump", ashape="s2sq",L0=2.0),
    dict(amp=0.3, rshape="cos",  ashape="s2",  L0=1.0, rho0=1.0),
    dict(amp=0.3, rshape="cos",  ashape="s2",  L0=1.0, seed_rng=0.05),
    dict(amp=0.4, rshape="cos",  ashape="s2",  L0=1.0, seed_rng=0.1),
]

best = None
print(f"{'seal':6s} {'seed':40s} {'it':>4s} {'Phi':>10s} {'Ir_mean':>10s} {'Ir_max':>10s} {'L':>9s} conv?")
for sname, seal in SEALS.items():
    for c in cases:
        u0 = custom_seed(ctx, **{k: v for k, v in c.items()})
        Ir0 = float(M.fields(u0, ctx, prm)["Ir"].mean())
        for maxit in [120, 250]:
            u1, hist = M.newton_lm_solve(u0, ctx, prm, maxit=maxit, verbose=False,
                                          time_budget=60.0, seal=seal)
            Q = M.fields(u1, ctx, prm)
            Ir = Q["Ir"]; L = float(Q["L"]); Phi = hist[-1]
            conv = Phi < 1e-4
            sust = float(Ir.mean()) > 1e-3
            desc = f"amp{c['amp']}_{c.get('rshape')}_{c.get('ashape')}_L{c.get('L0')}"
            if c.get('seed_rng'): desc += f"_rng{c['seed_rng']}"
            if c.get('rho0'): desc += f"_rho{c['rho0']}"
            flag = " *** CONVERGED+SUSTAINED ***" if (conv and sust) else ""
            print(f"{sname:6s} {desc:40s} {len(hist)-1:4d} {Phi:10.2e} {float(Ir.mean()):10.2e} "
                  f"{float(Ir.max()):10.2e} {L:9.4f} {str(conv):5s}{flag}")
            # track best CONVERGED candidate by sustained I_r
            if conv and (best is None or float(Ir.mean()) > best['Ir_mean']):
                best = dict(seal=sname, desc=desc, maxit=maxit, Phi=Phi,
                            Ir_mean=float(Ir.mean()), Ir_max=float(Ir.max()), L=L)

print("\n=== BEST CONVERGED (||F||^2<1e-4) CANDIDATE BY SUSTAINED I_r ===")
print(best)
if best and best['Ir_mean'] > 1e-3:
    print("VERDICT-DATA: REFUTED -- a converged solve holds sustained I_r>1e-3")
else:
    print("VERDICT-DATA: every CONVERGED solve drains (I_r_mean of best converged < 1e-3)")
