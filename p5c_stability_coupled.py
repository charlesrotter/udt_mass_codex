#!/usr/bin/env python3
"""
p5c_stability_coupled.py -- P5c-step-3, COUPLED-SPACE stability probe.

WHY (mismatch -> solver completeness): the fixed-metric body-Theta Hessian found
n_neg=0 for ALL FIVE basins (round/oblate/pert_s/prolate/toroidal) -- none is a
Theta-sector saddle.  But the multiplicity lives in the FULL COUPLED system (the
basins differ in metric warps a,b,c,d, not just Theta), which the matter-only
Hessian cannot see.  So the family question must be probed in the coupled space.

THREE coupled probes per basin (constraint-respecting throughout -- newton_solve
re-imposes Einstein + matter EL every step):

  (A) IN-PLACE RE-FLOOR: re-solve from the saved floored field.  A true coupled
      fixed point stays put (few iters, dM~0, d_field~0).  Confirms each is a
      genuine coupled solution, not a stalled artifact.

  (B) BASIN-PERSISTENCE under a coupled kick: perturb the WHOLE field (metric+Theta)
      by a small random body kick, re-solve.  If it returns to ITS OWN basin =>
      that basin is a genuine attractor (locally stable distinct object).  If it
      flows to ROUND (or another basin) => it was not a separate stable object.

  (C) INTER-BASIN MELT: seed the coupled solve from a CONVEX BLEND toward round
      (u = (1-s)*basin + s*round, BC rows re-pinned by the residual) at a few s,
      re-solve.  Track whether it relaxes back to the basin (separated by a
      barrier => distinct object) or slides to round (same well => round is the
      one particle, the others are unstable deformations).

m=1 round = reference: under (A)/(B) it must stay round (sign calibration).

ANTI-HANG: ONE basin per invocation, sequential, bounded newton maxit, Nr<=16.
USAGE:
  python3 p5c_stability_coupled.py refloor NR NAME [MAXIT]
  python3 p5c_stability_coupled.py kick    NR NAME [AMP] [MAXIT]
  python3 p5c_stability_coupled.py melt    NR NAME [MAXIT]   # blends s=0.25,0.5,0.75
  python3 p5c_stability_coupled.py report  NR
"""
import os, sys, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import (Grid3D, attach_coord_weight, residuals, diagnostics,
    build_metric, field_dn, DEV)
from full3d_solver import residual_vector, unpack, pack
import whole_metric_3d_matter as MAT
import whole_metric_3d_core as CORE
import full3d_newton as NW

P, KAP8 = 0.4, 0.05


def make_grid(NR):
    NTH = 6 if NR == 12 else 8
    G = Grid3D(NR, NTH, 8, rc=0.05, cell=14.0); return attach_coord_weight(G)


def load_u(NR, name):
    return torch.load(f"/tmp/p5c_basin_{NR}_{name}.pt")['u'].to(DEV)


def diag(G, u):
    return diagnostics(G, residuals(G, unpack(u, G), P, KAP8), KAP8)


def action_S(G, u):
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d); ginv = CORE.metric_inverse(g)
    dn = field_dn(G, Th, m=1); Gmn = MAT.field_metric(dn)
    L, _, _, _ = MAT.lagrangian(ginv, Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    return float((sqrtg * L * G.wvol_coord).sum())


def fdist(u1, u2):
    return float((u1 - u2).abs().max())


def classify_landing(G, ur, basins):
    """which saved basin (by field distance) is ur closest to?"""
    best = (1e30, "?")
    for nm, ub in basins.items():
        d = fdist(ur, ub)
        if d < best[0]:
            best = (d, nm)
    return best  # (dist, name)


def all_basins(NR):
    out = {}
    for nm in ['round', 'oblate', 'pert_s', 'prolate', 'toroidal']:
        fp = f"/tmp/p5c_basin_{NR}_{nm}.pt"
        if os.path.exists(fp):
            out[nm] = torch.load(fp)['u'].to(DEV)
    return out


def repin_bc(G, u, p=P):
    """re-pin the BC rows of a blended/perturbed seed so it starts charge-1 winding
       (the residual enforces them anyway; this just gives a clean seed)."""
    a, b, c, d, Th = unpack(u, G)
    Th = Th.clone(); Th[0] = np.pi; Th[-1] = 0.0
    a = a.clone(); a[-1] = 0.0
    b = b.clone(); b[0] = -p
    c = c.clone(); c[0] = 0.0; c[-1] = 0.0
    d = d.clone(); d[0] = 0.0; d[-1] = 0.0
    return pack(a, b, c, d, Th)


def cmd_refloor(NR, name, maxit):
    G = make_grid(NR); u = load_u(NR, name)
    d0 = diag(G, u); S0 = action_S(G, u)
    F = residual_vector(u, G, P, KAP8); Phi0 = float((F*F).sum())
    t0 = time.time()
    ur, hr = NW.newton_solve(u, G, P, KAP8, m=1, maxit=maxit, lam0=1e-4, tol=1e-12)
    dr = diag(G, ur); Sr = action_S(G, ur)
    print(f"[refloor {NR} {name}] base M={d0['M_MS']:.5f} S={S0:.4e} Phi={Phi0:.1e}"
          f" -> reM={dr['M_MS']:.5f} reS={Sr:.4e} Phi={hr[-1]:.1e} "
          f"its={len(hr)-1} dM={dr['M_MS']-d0['M_MS']:+.2e} "
          f"d_field={fdist(ur,u):.2e} wall={time.time()-t0:.0f}s", flush=True)
    json.dump(dict(NR=NR, name=name, kind='refloor', M0=d0['M_MS'], Mr=dr['M_MS'],
                   S0=S0, Sr=Sr, dfield=fdist(ur, u), Phi=hr[-1]),
              open(f"/tmp/p5c_coupled_refloor_{NR}_{name}.json", "w"))


def cmd_kick(NR, name, amp, maxit):
    G = make_grid(NR); u = load_u(NR, name); basins = all_basins(NR)
    a, b, c, d, Th = unpack(u, G)
    rmask = torch.ones_like(Th); rmask[0] = 0; rmask[-1] = 0
    g = torch.Generator(device='cpu').manual_seed(2024)
    a2, b2, c2, d2, Th2 = (f + amp*rmask*torch.randn(f.shape, generator=g).to(DEV)
                           for f in (a, b, c, d, Th))
    useed = repin_bc(G, pack(a2, b2, c2, d2, Th2))
    d0 = diag(G, u); S0 = action_S(G, u)
    t0 = time.time()
    ur, hr = NW.newton_solve(useed, G, P, KAP8, m=1, maxit=maxit, lam0=1e-4, tol=1e-12)
    dr = diag(G, ur); Sr = action_S(G, ur)
    land_d, land_nm = classify_landing(G, ur, basins)
    d_self = fdist(ur, u)
    verdict = ("RETURNED to own basin" if land_nm == name and land_d < 0.05
               else f"FLOWED to '{land_nm}' (d={land_d:.3f})")
    print(f"[kick {NR} {name} amp={amp}] base M={d0['M_MS']:.5f} S={S0:.4e} -> "
          f"M={dr['M_MS']:.5f} S={Sr:.4e} Phi={hr[-1]:.1e} its={len(hr)-1}",
          flush=True)
    print(f"  d_self={d_self:.3f} nearest_basin='{land_nm}'(d={land_d:.3f}) "
          f"=> {verdict}  wall={time.time()-t0:.0f}s", flush=True)
    json.dump(dict(NR=NR, name=name, kind='kick', amp=amp, M0=d0['M_MS'],
                   Mr=dr['M_MS'], S0=S0, Sr=Sr, d_self=d_self, land_nm=land_nm,
                   land_d=land_d, Phi=hr[-1], verdict=verdict),
              open(f"/tmp/p5c_coupled_kick_{NR}_{name}.json", "w"))


def cmd_melt(NR, name, maxit):
    G = make_grid(NR); u = load_u(NR, name); basins = all_basins(NR)
    u_round = basins['round']
    d0 = diag(G, u); S0 = action_S(G, u)
    Sround = action_S(G, u_round); Mround = diag(G, u_round)['M_MS']
    print(f"[melt {NR} {name}] basin M={d0['M_MS']:.5f} S={S0:.4e}  "
          f"round M={Mround:.5f} S={Sround:.4e}", flush=True)
    recs = []
    for s in (0.25, 0.5, 0.75):
        blended = repin_bc(G, (1 - s) * u + s * u_round)
        t0 = time.time()
        ur, hr = NW.newton_solve(blended, G, P, KAP8, m=1, maxit=maxit,
                                 lam0=1e-4, tol=1e-12)
        dr = diag(G, ur); Sr = action_S(G, ur)
        d_basin = fdist(ur, u); d_round = fdist(ur, u_round)
        land_d, land_nm = classify_landing(G, ur, basins)
        if d_round < 0.05:
            where = "-> ROUND (melted; not a separate well)"
        elif d_basin < 0.05:
            where = "-> back to OWN basin (barrier; distinct well)"
        else:
            where = f"-> '{land_nm}' d={land_d:.3f} (d_basin={d_basin:.2f} d_round={d_round:.2f})"
        print(f"  s={s:.2f}: M={dr['M_MS']:.5f} S={Sr:.4e} Phi={hr[-1]:.1e} "
              f"its={len(hr)-1}  {where}  wall={time.time()-t0:.0f}s", flush=True)
        recs.append(dict(s=s, M=dr['M_MS'], S=Sr, d_basin=d_basin, d_round=d_round,
                         land_nm=land_nm, land_d=land_d, Phi=hr[-1], where=where))
    json.dump(dict(NR=NR, name=name, kind='melt', M0=d0['M_MS'], S0=S0,
                   Mround=Mround, Sround=Sround, recs=recs),
              open(f"/tmp/p5c_coupled_melt_{NR}_{name}.json", "w"))


def cmd_report(NR):
    print(f"\n=== COUPLED STABILITY  Nr={NR} ===", flush=True)
    for nm in ['round', 'oblate', 'pert_s', 'prolate', 'toroidal']:
        line = f"  {nm:>9}:"
        for kind in ('refloor', 'kick', 'melt'):
            fp = f"/tmp/p5c_coupled_{kind}_{NR}_{nm}.json"
            if not os.path.exists(fp):
                continue
            r = json.load(open(fp))
            if kind == 'refloor':
                line += f" [refloor dM={r['Mr']-r['M0']:+.1e} dfield={r['dfield']:.1e}]"
            elif kind == 'kick':
                line += f" [kick:{r['verdict']}]"
            elif kind == 'melt':
                tags = "/".join(x['where'].split('(')[0].strip().replace('-> ', '')
                                for x in r['recs'])
                line += f" [melt s.25/.5/.75: {tags}]"
        print(line, flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]; NR = int(sys.argv[2]); t0 = time.time()
    if mode == 'refloor':
        cmd_refloor(NR, sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 15)
    elif mode == 'kick':
        amp = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
        cmd_kick(NR, sys.argv[3], amp, int(sys.argv[5]) if len(sys.argv) > 5 else 25)
    elif mode == 'melt':
        cmd_melt(NR, sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 25)
    elif mode == 'report':
        cmd_report(NR)
    print(f"=== DONE ({mode} {NR} {sys.argv[3] if len(sys.argv)>3 else ''}) "
          f"{time.time()-t0:.0f}s ===", flush=True)
