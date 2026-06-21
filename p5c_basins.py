#!/usr/bin/env python3
"""
p5c_basins.py -- P5c-step-2 BASIN CHARACTERIZATION of the committed 3-D coupled
residual.  DIAGNOSTIC ONLY (map what's there; NO selection principle is added,
NO M_MS is banked).

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.
Branch: p5c-basins.  NEW FILE (committed full3d_*/p5b_* reused as imports only).

WHAT: seed-sweep the FREE full-space dense Newton (full3d_newton.newton_solve --
ALL DOF free, no re-pose hold gauge: P5c-step-1 showed this is the clean, single-
valued anchor at one seed) from MULTIPLE distinct seeds, and record for each
FLOORED branch: committed-Phi, M_MS, Theta amplitude/shape, tvar/psivar asymmetry,
metric-warp magnitudes, and an ENERGY proxy (the matter action S = int sqrt(-g) L
dV evaluated on the floored field).  Then cluster into basins.

Seeds (all are perturbations of the validated round/hedgehog round_seed, so each
remains a legitimate charge-1 winding configuration -- the winding BC rows pin
Theta(core)=pi, Theta(seal)=0 in EVERY solve; the seed only changes the BODY shape
the Newton starts from):
  round    : the #56 round soliton embedded (a=a(r),b=b(r),c=d=0,Th=Th(r))
  oblate   : Theta squashed along the polar (theta) axis  (+eps*cos(2th) shape)
  prolate  : Theta stretched along the polar axis         (-eps*cos(2th) shape)
  pert_s   : small-amplitude random body perturbation     (eps=0.03)
  pert_L   : large-amplitude body perturbation            (eps=0.30) + warp kick
  toroidal : Theta pushed toward an equatorial ring        (+eps*sin^2(th) on a,Th)

ANTI-HANG (binding, #1 priority -- THREE prior agents hung):
  - SINGLE clean process per solve, SEQUENTIAL, never concurrent.
  - HARD CAPS: Nr<=24; this script runs ONE (NR, seed) per invocation; Newton
    maxit<=40; expected <~6 min per call at Nr<=16.  Nr=24 only as a one-off
    confirmation if it floors in budget.
  - Free dense Newton via full3d_newton.newton_solve (jacrev J + lstsq) -- the
    in-budget flooring tool.  NEVER matrix-free LSMR.  NO background poll.

USAGE (one solve per process):
  python3 p5c_basins.py one NR SEED [MAXIT]   # floor one (NR,seed); save /tmp pt
  python3 p5c_basins.py report NR             # load all saved seeds at NR -> table
"""
import os, sys, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")  # jacrev path
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import (Grid3D, attach_coord_weight, residuals, diagnostics,
    build_metric, field_dn, DEV)
from full3d_solver import residual_vector, round_seed, unpack, pack
import whole_metric_3d_matter as MAT
import whole_metric_3d_core as CORE
import full3d_newton as NW

P, KAP8 = 0.4, 0.05
SEEDS = ['round', 'oblate', 'prolate', 'pert_s', 'pert_L', 'toroidal']


def make_grid(NR):
    NTH = 6 if NR == 12 else 8
    NPS = 8
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    return G, NTH, NPS


def build_seed(G, name):
    """Return a packed seed vector.  All are perturbations of round_seed; the BC
    rows (held by the residual, not the seed) keep every solve charge-1 winding.
    A fixed RNG seed makes pert_s/pert_L reproducible."""
    u0, sol = round_seed(G, p=P, kap8=KAP8)
    a, b, c, d, Th = unpack(u0.clone(), G)
    th = G.THg  # (Nr,Nth,Nps) theta grid
    # interior mask: do NOT touch core(0)/seal(-1) radial ends (BC rows pin them)
    rmask = torch.ones_like(Th); rmask[0] = 0.0; rmask[-1] = 0.0
    if name == 'round':
        pass
    elif name == 'oblate':
        Th = Th + 0.25 * rmask * torch.cos(2*th) * torch.sin(np.pi * _rfrac(G))
    elif name == 'prolate':
        Th = Th - 0.25 * rmask * torch.cos(2*th) * torch.sin(np.pi * _rfrac(G))
    elif name == 'pert_s':
        g = torch.Generator(device='cpu').manual_seed(12345)
        for f in (a, b, c, d, Th):
            f += 0.03 * rmask * torch.randn(f.shape, generator=g).to(DEV)
    elif name == 'pert_L':
        g = torch.Generator(device='cpu').manual_seed(67890)
        for f in (a, b, c, d, Th):
            f += 0.30 * rmask * torch.randn(f.shape, generator=g).to(DEV)
    elif name == 'toroidal':
        ring = (torch.sin(th)**2)
        Th = Th + 0.30 * rmask * ring * torch.sin(np.pi * _rfrac(G))
        a = a + 0.10 * rmask * ring
    else:
        raise ValueError(name)
    return pack(a, b, c, d, Th)


def _rfrac(G):
    """radial fraction in [0,1] broadcast to grid shape (for a smooth radial bump
    that vanishes at both ends)."""
    r = G.r
    f = (r - r.min()) / (r.max() - r.min())
    return f[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()


def energy_proxy(G, u):
    """Matter action S = int sqrt(-g) (L2+L4) dV_coord on the floored field, plus
    the matter Misner-Sharp-like total |S2|,|S4|.  (matter_action in the committed
    module has a stray undefined `n` in its return -- we recompute the action here,
    same algebra, to avoid it.)"""
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d)
    ginv = CORE.metric_inverse(g)
    dn = field_dn(G, Th, m=1)
    Gmn = MAT.field_metric(dn)
    L, L2, L4, SS = MAT.lagrangian(ginv, Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    dV = G.wvol_coord
    S = float((sqrtg * L * dV).sum())
    S2 = float((sqrtg * L2 * dV).sum())
    S4 = float((sqrtg * L4 * dV).sum())
    return dict(S=S, S2=S2, S4=S4)


def field_character(G, u):
    a, b, c, d, Th = unpack(u, G)
    # Theta amplitude/shape (Theta goes pi->0; report its body extrema + angular
    # spread at the mid-radius shell where the soliton has mass)
    Th_min = float(Th.min()); Th_max = float(Th.max())
    mid = G.Nr // 2
    Th_mid_spread = float(Th[mid].max() - Th[mid].min())   # angular variation @ mid r
    # metric-warp magnitudes (max |.| over body)
    bod = G.body
    warp = dict(a=float(a[bod].abs().max()), b=float(b[bod].abs().max()),
                c=float(c[bod].abs().max()), d=float(d[bod].abs().max()))
    return dict(Th_min=Th_min, Th_max=Th_max, Th_mid_spread=Th_mid_spread, warp=warp)


def core_regularity(G, u):
    """Spurious-branch witness: at a regular charge-1 hedgehog Theta(core)=pi and the
    field is SMOOTH; c,d warps =0 at core (round limit BC).  We measure how far the
    floored solution departs from a regular, monotone, charge-1 profile:
      - winding check: Theta(core)-pi and Theta(seal)-0 residuals (should be ~0 by BC)
      - Theta monotonicity: fraction of radial shells where angle-avg Theta INCREASES
        going outward (a monotone hedgehog is strictly decreasing -> 0 violations)
      - off-diag warp magnitude c,d (non-axisym/shear; large => lobed/toroidal shape)
    """
    a, b, c, d, Th = unpack(u, G)
    win_core = float((Th[0] - np.pi).abs().max())
    win_seal = float((Th[-1]).abs().max())
    # angle-averaged Theta(r)
    dOm = (G.wmu[None, :, None] * G.wps[None, None, :])
    Th_ang = (Th * dOm).sum(dim=(1, 2)) / dOm.sum(dim=(1, 2))
    dTh = Th_ang[1:] - Th_ang[:-1]      # should be <=0 (decreasing) for hedgehog
    n_up = int((dTh > 1e-3).sum())      # # of non-monotone (increasing) steps
    frac_nonmono = n_up / max(len(dTh), 1)
    offdiag = max(float(c[G.body].abs().max()), float(d[G.body].abs().max()))
    return dict(win_core=win_core, win_seal=win_seal,
                frac_nonmono=frac_nonmono, offdiag=offdiag)


def one(NR, name, maxit):
    G, NTH, NPS = make_grid(NR)
    u0 = build_seed(G, name)
    Phi0 = float((residual_vector(u0, G, P, KAP8)**2).sum())
    t0 = time.time()
    u, hist = NW.newton_solve(u0, G, P, KAP8, maxit=maxit, lam0=1e-4, tol=1e-12,
                              verbose=True)
    F = residual_vector(u, G, P, KAP8); Phi = float((F*F).sum())
    out = residuals(G, unpack(u, G), P, KAP8); d = diagnostics(G, out, KAP8)
    E = energy_proxy(G, u)
    fc = field_character(G, u)
    reg = core_regularity(G, u)
    wall = time.time() - t0
    print(f"  BASIN ({NR},{name}): seedPhi={Phi0:.2e} -> Phi={Phi:.3e} "
          f"its={len(hist)-1} M_MS={d['M_MS']:.6f} tvar={d['tvar']:.4e} "
          f"psivar={d['psivar']:.4e} wall={wall:.0f}s", flush=True)
    print(f"    Theta[min,max]=[{fc['Th_min']:.3f},{fc['Th_max']:.3f}] "
          f"mid-shell ang.spread={fc['Th_mid_spread']:.3e}  "
          f"warp a={fc['warp']['a']:.3e} b={fc['warp']['b']:.3e} "
          f"c={fc['warp']['c']:.3e} d={fc['warp']['d']:.3e}", flush=True)
    print(f"    energy S={E['S']:.6e} (S2={E['S2']:.4e} S4={E['S4']:.4e})", flush=True)
    print(f"    regularity: win|core,seal|=[{reg['win_core']:.2e},{reg['win_seal']:.2e}] "
          f"frac_nonmono={reg['frac_nonmono']:.3f} offdiag(c,d)={reg['offdiag']:.3e}",
          flush=True)
    floored = Phi < 1e-9
    if not floored:
        print(f"    *** UNDER-FLOORED (Phi={Phi:.2e} >= 1e-9): flag, not a real branch",
              flush=True)
    rec = dict(NR=NR, NTH=NTH, NPS=NPS, seed=name, Phi0=Phi0, Phi=Phi,
               its=len(hist)-1, M_MS=d['M_MS'], tvar=d['tvar'], psivar=d['psivar'],
               energy=E, fc=fc, reg=reg, floored=floored, wall=wall,
               u=u.cpu())
    torch.save(rec, f"/tmp/p5c_basin_{NR}_{name}.pt")


def report(NR):
    rows = []
    for nm in SEEDS:
        fp = f"/tmp/p5c_basin_{NR}_{nm}.pt"
        if not os.path.exists(fp):
            continue
        rows.append(torch.load(fp))
    if not rows:
        print(f"  no saved basins at NR={NR}"); return
    print(f"\n=== BASIN MAP  Nr={NR} ===", flush=True)
    hdr = ("seed", "Phi", "floor?", "M_MS", "energyS", "Th_min", "Th_max",
           "midspread", "tvar", "psivar", "offdiag", "nonmono", "its")
    print("  " + " | ".join(f"{h:>9}" for h in hdr), flush=True)
    for r in rows:
        print("  " + " | ".join([
            f"{r['seed']:>9}", f"{r['Phi']:>9.2e}",
            f"{str(r['floored']):>9}", f"{r['M_MS']:>9.5f}",
            f"{r['energy']['S']:>9.4e}", f"{r['fc']['Th_min']:>9.3f}",
            f"{r['fc']['Th_max']:>9.3f}", f"{r['fc']['Th_mid_spread']:>9.2e}",
            f"{r['tvar']:>9.2e}", f"{r['psivar']:>9.2e}",
            f"{r['reg']['offdiag']:>9.2e}", f"{r['reg']['frac_nonmono']:>9.3f}",
            f"{r['its']:>9d}"]), flush=True)
    # pairwise field distance between floored branches (cluster witness)
    fl = [r for r in rows if r['floored']]
    if len(fl) >= 2:
        print("\n  pairwise max|u_i - u_j| (floored branches):", flush=True)
        for i in range(len(fl)):
            for j in range(i+1, len(fl)):
                du = float((fl[i]['u'] - fl[j]['u']).abs().max())
                dM = abs(fl[i]['M_MS'] - fl[j]['M_MS'])
                print(f"    {fl[i]['seed']:>9} vs {fl[j]['seed']:<9} "
                      f"max|du|={du:.3e}  dM_MS={dM:.3e}", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]; NR = int(sys.argv[2])
    t0 = time.time()
    if mode == 'one':
        name = sys.argv[3]; maxit = int(sys.argv[4]) if len(sys.argv) > 4 else 40
        one(NR, name, maxit)
    elif mode == 'report':
        report(NR)
    print(f"=== DONE ({mode} {NR} {sys.argv[3] if len(sys.argv)>3 else ''}) "
          f"{time.time()-t0:.0f}s ===", flush=True)
