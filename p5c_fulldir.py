#!/usr/bin/env python3
"""
p5c_fulldir.py -- P5c-step-4 FULL-DIRECTION stability: close the Theta-only gap.

WHY (solver-completeness): p5c_stability found n_neg=0 for all 5 basins but ONLY in
the fixed-metric Theta Hessian.  The basins differ in METRIC warps (a,b,c,d), which
the Theta-only Hessian cannot see.  This step probes the METRIC directions, two ways:

  (1) METRIC-KICK CONSTRAINT-RESPECTING RE-SOLVE (the binding constraint-respecting
      test -- memory [[gravitating-soliton-stability-test]]: the fixed-metric Hessian
      OVER-COUNTS, so test along a kicked direction by a full coupled re-solve).  Kick
      ONLY the metric warps a,b,c,d (Theta untouched) by +/-amp random, re-pin BCs,
      run the FULL coupled newton_solve (re-imposes Einstein + matter EL every step).
      RETURNS to own basin (d_self small, S ~ same) => stable in the metric directions.
      DESCENDS to lower |S| / different field => a metric-direction instability the
      Theta-only test missed.  Round = calibration: must return to round.

  (2) FINITE-DIFFERENCE coupled-action curvature along each metric channel.  For each
      warp channel ch in {a,b,c,d}: form u(+/-h) by adding +/-h * (smooth body bump)
      to that channel ONLY, re-solve coupled (so Theta + the other metric DOF relax to
      the constraint surface at the displaced warp), and read the matter action S.  The
      central 2nd difference (S(+h) - 2 S(0) + S(-h))/h^2 is the curvature of the
      constrained energy along that metric channel.  POSITIVE (in the |S| convention =
      the basin is a local min along that channel) => stable; NEGATIVE => a downhill
      metric direction.  (h small; 1 coupled re-solve per sign per channel = 8 bounded
      solves; capped.)

ANTI-HANG: ONE basin per invocation.  Test (1) = 1 coupled solve.  Test (2) = up to 8
bounded coupled solves (4 channels x 2 signs) -- each maxit-capped; we cap CHANNELS to
keep budget (default channels='ab' = the dominant warps; pass 'abcd' for full at cost).
Nr<=16 (Nr=12 default = saved basin set).  SEQUENTIAL, never concurrent.  No bg poll.

USAGE (one basin per process):
  python3 p5c_fulldir.py kick NR NAME [AMP] [MAXIT]          # metric-only kick re-solve
  python3 p5c_fulldir.py curv NR NAME [H] [CH] [MAXIT]       # FD metric-channel curvature
  python3 p5c_fulldir.py report NR
"""
import os, sys, time, json, glob
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
BASINS = ['round', 'oblate', 'pert_s', 'prolate', 'toroidal']


def make_grid(NR):
    NTH = 6 if NR == 12 else 8
    G = Grid3D(NR, NTH, 8, rc=0.05, cell=14.0); return attach_coord_weight(G)


def load_u(NR, name):
    return torch.load(f"/tmp/p5c_basin_{NR}_{name}.pt")['u'].to(DEV)


def all_basins(NR):
    out = {}
    for nm in BASINS:
        fp = f"/tmp/p5c_basin_{NR}_{nm}.pt"
        if os.path.exists(fp):
            out[nm] = torch.load(fp)['u'].to(DEV)
    return out


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


def repin_bc(G, u, p=P):
    a, b, c, d, Th = unpack(u, G)
    Th = Th.clone(); Th[0] = np.pi; Th[-1] = 0.0
    a = a.clone(); a[-1] = 0.0
    b = b.clone(); b[0] = -p
    c = c.clone(); c[0] = 0.0; c[-1] = 0.0
    d = d.clone(); d[0] = 0.0; d[-1] = 0.0
    return pack(a, b, c, d, Th)


def classify_landing(G, ur, basins):
    best = (1e30, "?")
    for nm, ub in basins.items():
        dd = fdist(ur, ub)
        if dd < best[0]:
            best = (dd, nm)
    return best


def body_bump(G):
    """smooth radial bump vanishing at both ends (for a clean metric-channel FD kick)."""
    r = G.r
    f = (r - r.min()) / (r.max() - r.min())
    bump = torch.sin(np.pi * f)
    return bump[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous().to(DEV)


def cmd_kick(NR, name, amp, maxit):
    """Kick ONLY the metric warps (a,b,c,d); Theta untouched.  Constraint-respecting
       coupled re-solve.  Tests metric-direction stability the Theta-only Hessian
       missed."""
    G = make_grid(NR); u = load_u(NR, name); basins = all_basins(NR)
    a, b, c, d, Th = unpack(u, G)
    rmask = torch.ones_like(a); rmask[0] = 0; rmask[-1] = 0
    g = torch.Generator(device='cpu').manual_seed(7777)
    a2, b2, c2, d2 = (f + amp*rmask*torch.randn(f.shape, generator=g).to(DEV)
                      for f in (a, b, c, d))
    useed = repin_bc(G, pack(a2, b2, c2, d2, Th.clone()))  # Theta NOT kicked
    M0 = diag(G, u)['M_MS']; S0 = action_S(G, u)
    t0 = time.time()
    ur, hr = NW.newton_solve(useed, G, P, KAP8, m=1, maxit=maxit, lam0=1e-4, tol=1e-12)
    Mr = diag(G, ur)['M_MS']; Sr = action_S(G, ur)
    land_d, land_nm = classify_landing(G, ur, basins)
    d_self = fdist(ur, u)
    # constraint-respecting verdict: returned (stable metric dir) vs descended/flowed
    dS_rel = (abs(Sr) - abs(S0)) / max(abs(S0), 1.0)
    if land_nm == name and land_d < 0.05:
        verdict = "RETURNED to own basin (metric-stable)"
    elif dS_rel < -1e-2:
        verdict = f"DESCENDED to lower |S| basin '{land_nm}' (d={land_d:.3f})"
    else:
        verdict = f"FLOWED to '{land_nm}' (d={land_d:.3f}, dS_rel={dS_rel:+.2e})"
    print(f"[mkick {NR} {name} amp={amp}] M {M0:.5f}->{Mr:.5f}  S {S0:.4e}->{Sr:.4e}"
          f"  Phi={hr[-1]:.1e} its={len(hr)-1}", flush=True)
    print(f"  d_self={d_self:.3f} nearest='{land_nm}'(d={land_d:.3f}) dS_rel={dS_rel:+.2e}"
          f"  => {verdict}  wall={time.time()-t0:.0f}s", flush=True)
    json.dump(dict(NR=NR, name=name, kind='mkick', amp=amp, M0=M0, Mr=Mr, S0=S0, Sr=Sr,
                   d_self=d_self, land_nm=land_nm, land_d=land_d, dS_rel=dS_rel,
                   Phi=hr[-1], verdict=verdict),
              open(f"/tmp/p5c_fulldir_mkick_{NR}_{name}.json", "w"))


def cmd_curv(NR, name, h, channels, maxit):
    """FD curvature of the CONSTRAINED matter action along each metric channel.  For
       each ch in channels: u(+/-h) = base with ch += +/- h*bump, then COUPLED re-solve
       (Theta + other DOF relax to the constraint surface), read S.  Curvature in the
       |S| convention; NEGATIVE => downhill metric direction (instability)."""
    G = make_grid(NR); u = load_u(NR, name)
    a, b, c, d, Th = unpack(u, G)
    base = dict(a=a, b=b, c=c, d=d, Th=Th)
    bump = body_bump(G)
    S0 = action_S(G, u); aS0 = abs(S0)
    print(f"[curv {NR} {name}] base S={S0:.4e} h={h} channels={channels}", flush=True)
    recs = {}
    for ch in channels:
        Sp = Sm = None
        for sgn in (+1.0, -1.0):
            fields = {k: v.clone() for k, v in base.items()}
            rmask = torch.ones_like(fields[ch]); rmask[0] = 0; rmask[-1] = 0
            fields[ch] = fields[ch] + sgn * h * rmask * bump
            useed = repin_bc(G, pack(fields['a'], fields['b'], fields['c'],
                                     fields['d'], fields['Th']))
            ur, hr = NW.newton_solve(useed, G, P, KAP8, m=1, maxit=maxit,
                                     lam0=1e-4, tol=1e-12)
            Sx = action_S(G, ur); axS = abs(Sx)
            if sgn > 0:
                Sp, Php = axS, hr[-1]
            else:
                Sm, Phm = axS, hr[-1]
        curv = (Sp - 2*aS0 + Sm) / (h*h)   # |S|-convention curvature
        sign = "STABLE(min)" if curv > 0 else "DOWNHILL(neg curv)"
        print(f"  ch={ch}: |S|(+h)={Sp:.4e}(Phi{Php:.0e}) |S|0={aS0:.4e} "
              f"|S|(-h)={Sm:.4e}(Phi{Phm:.0e}) curv={curv:+.3e} {sign}", flush=True)
        recs[ch] = dict(Sp=Sp, Sm=Sm, aS0=aS0, curv=curv, sign=sign)
    n_neg_ch = sum(1 for r in recs.values() if r['curv'] < 0)
    verdict = ("metric-stable (all channels +curv)" if n_neg_ch == 0
               else f"{n_neg_ch} downhill metric channel(s)")
    print(f"[curv {NR} {name}] => {verdict}", flush=True)
    json.dump(dict(NR=NR, name=name, kind='curv', h=h, channels=channels, S0=S0,
                   recs=recs, n_neg_ch=n_neg_ch, verdict=verdict),
              open(f"/tmp/p5c_fulldir_curv_{NR}_{name}.json", "w"))


def cmd_report(NR):
    print(f"\n=== P5c-step-4 FULL-DIRECTION (metric) STABILITY  Nr={NR} ===", flush=True)
    for nm in BASINS:
        line = f"  {nm:>9}:"
        fk = f"/tmp/p5c_fulldir_mkick_{NR}_{nm}.json"
        fc = f"/tmp/p5c_fulldir_curv_{NR}_{nm}.json"
        if os.path.exists(fk):
            r = json.load(open(fk)); line += f" [mkick: {r['verdict']}]"
        if os.path.exists(fc):
            r = json.load(open(fc))
            chs = " ".join(f"{c}:{v['curv']:+.1e}" for c, v in r['recs'].items())
            line += f" [curv {r['verdict']} | {chs}]"
        print(line, flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]; NR = int(sys.argv[2]); t0 = time.time()
    if mode == 'kick':
        amp = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
        cmd_kick(NR, sys.argv[3], amp, int(sys.argv[5]) if len(sys.argv) > 5 else 25)
    elif mode == 'curv':
        h = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
        ch = sys.argv[5] if len(sys.argv) > 5 else 'ab'
        cmd_curv(NR, sys.argv[3], h, ch, int(sys.argv[6]) if len(sys.argv) > 6 else 20)
    elif mode == 'report':
        cmd_report(NR)
    print(f"=== DONE ({mode} {NR} {sys.argv[3] if len(sys.argv)>3 else ''}) "
          f"{time.time()-t0:.0f}s ===", flush=True)
