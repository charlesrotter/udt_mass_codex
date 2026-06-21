#!/usr/bin/env python3
"""
p5e_offround_qep.py -- P5e OFF-ROUND CLASSICAL-DISCRETENESS GATE.

THE ONE QUESTION (OBSERVE mode, DATA-BLIND, nothing banked): is there CLASSICAL
discreteness in the OFF-ROUND (l>=2) channel BEFORE quantization?  P5d showed the
ROUND object is time-frozen (M=0, Birkhoff -> no classical oscillator round).  The
P5d verifier EXHIBITED that the OFF-ROUND channel has NONZERO d_t^2 inertia
(||M||/||K|| ~ 0.09-0.12) via a non-round c1 theta-warp.  So a classical oscillator
EXISTS off-round.  The open question P5e answers: does its spectrum TOWER (intrinsic
discrete levels = classical discreteness) or BOX-CONTROL (continuum, level ~1/R^2,
needs quantization)?

WHY OPEN: the bare vacuum was box-controlled because SCALE-FREE (#62, analytic).  The
MATTER L2+L4 sector HAS an intrinsic length sqrt(kappa/xi).  Matter COULD carry an
intrinsic level the vacuum can't -- not pre-decided.

METHOD (full clean operator, NOT a reduced proxy): reuse the EXACT P5d pipeline
(p5d_timelive.time_rows / assemble_KCM stack = P4 einstein_live pole-stable hybrid +
native S^2 EL coupled to the full metric + a(phi) ruler + the validated live time row),
but on an OFF-ROUND background where M != 0, and sampling ALL theta rows (not just the
midplane) so the l>=2 inertia is genuinely captured.  Then the QEP
        R_time(x; omega) = (K + omega C - omega^2 M) x = 0
is a GENUINE quadratic eigenproblem (M != 0) -> real eigenfrequencies omega.

OFF-ROUND BACKGROUNDS (>=2, so it's not one config):
  (A) c1-WARP: the round S^2 ground state + a controlled l=2 angular warp,
      c0 = d0 = c1 * (3 cos^2 th - 1)/2  (Legendre P2; the verifier's c1 theta-warp,
      the cleanest single-parameter off-round deformation).  Tunable c1.
  (B) BASIN field: the saved off-round coupled solutions (oblate / toroidal), loaded
      from /tmp/p5c_basin_*.pt -- genuine floored off-round metric configs.

THE BOX-CONTROL GATE (decisive): for the lowest eigenfrequency(ies), scan cell R (and
Nr).  Report (a) omega^2 R-independent (intrinsic) vs ~1/R^2 (box); (b) wall-relocation
2x; (c) intrinsic-lock negative control (is the lowest level just l(l+1)W_inf charge
barrier, or a cavity j_l zero -> box -- an intrinsic NEW level is NEITHER).

ANTI-HANG (binding #1): FIXED-BACKGROUND EIGENPROBLEMS = CHEAP.  SINGLE clean process
per solve, SEQUENTIAL, never concurrent.  Nr<=16.  Bounded.  No background poll.  Each
call <~6 min.  Static bg floors in ~5 s; KCM assembly across-theta is ~3*Nr FD columns
of the off-round time rows (still tiny).  If a check exceeds budget: REDUCE, report
"throughput-limited", do NOT hang.

USAGE (one solve per process):
  python3 p5e_offround_qep.py qep   warp NR CELL [C1]   # c1-warp bg QEP, save /tmp
  python3 p5e_offround_qep.py qep   basin NR CELL SEED  # basin bg QEP (SEED=oblate/toroidal)
  python3 p5e_offround_qep.py box   warp NR [C1]        # box-control scan over saved warp cells
  python3 p5e_offround_qep.py box   basin NR SEED       # box-control scan over saved basin cells
  python3 p5e_offround_qep.py probe warp NR CELL [C1]   # quick ||K||,||C||,||M|| only (sanity)

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE.  DATA-BLIND.  Branch offround-classical.
NEW file (p5d_timelive / p4_time_live / p2_* / p3fix / full3d_* reused as IMMUTABLE imports).
"""
import os, sys, math, time, glob
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV, T, R, TH, PS
from full3d_newton import inv4x4, det4x4
import p2_matter_s2_fullmetric as P2
import p4_time_live as P4
import p5d_timelive as P5D


# ---------------------------------------------------------------------------
# OFF-ROUND time-residual rows.  Same physics pieces as P5d.time_rows (the full
# clean stack), but:
#   (1) the background carries an l=2 angular warp c0=d0 (off-round) and may carry
#       theta dependence in a0,b0,F0 (basin fields);
#   (2) the interior residual rows are taken ACROSS ALL theta and psi nodes (not
#       just the midplane), so the l>=2 inertia genuinely enters the operator.
# Linear in the live amplitudes x=(a1,b1,F1) for a fixed background; the omega
# dependence is the harmonic-balance d_t/d_t^2 content (-> M != 0 off-round).
# ---------------------------------------------------------------------------
def build_metric_live_offround(G, A0, B0, C0, D0, a1, b1, c1, d1, omega, cph, sph):
    """Metric VALUE g and its FULL time partials dt_g, dtt_g for the OFF-ROUND live
    fluctuation: ALL FOUR diagonal warps a,b,c,d carry a live harmonic amplitude
    (a=a0+a1 cph, ..., d=d0+d1 cph).  This is the genuine off-round channel: the angular
    warps c,d (g_thth, g_psps) now have d_t/d_t^2 content, so the d_t^2 inertia survives
    in the ANGULAR diagonal rows G^th_th/G^ps_ps (the verifier's nonzero-even-round
    inertia channel) and -- once c1,d1 != round -- in G^t_t/G^r_r too.  All algebraic
    in omega (harmonic balance)."""
    r, sth = G.Rg, G.STHg
    a = A0 + a1*cph; b = B0 + b1*cph; c = C0 + c1*cph; d = D0 + d1*cph
    g = build_metric(G, a, b, c, d)
    at = -omega*a1*sph; att = -omega**2*a1*cph
    bt = -omega*b1*sph; btt = -omega**2*b1*cph
    ct = -omega*c1*sph; ctt = -omega**2*c1*cph
    dt = -omega*d1*sph; dtt = -omega**2*d1*cph
    e2a = torch.exp(torch.clamp(2*a, max=F3.EXP_CLAMP))
    e2b = torch.exp(torch.clamp(2*b, max=F3.EXP_CLAMP))
    e2c = torch.exp(torch.clamp(2*c, max=F3.EXP_CLAMP))
    e2d = torch.exp(torch.clamp(2*d, max=F3.EXP_CLAMP))
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dt_g  = torch.zeros(Nr, Nth, Nps, 4, 4, device=DEV)
    dtt_g = torch.zeros(Nr, Nth, Nps, 4, 4, device=DEV)
    # g_tt=-e^{2a}: d_t=-2at e2a ; d_t^2=-(2att+4at^2)e2a
    dt_g[..., T, T]  = -2*at*e2a;            dtt_g[..., T, T]  = -(2*att + 4*at*at)*e2a
    dt_g[..., R, R]  =  2*bt*e2b;            dtt_g[..., R, R]  =  (2*btt + 4*bt*bt)*e2b
    # g_thth=e^{2c} r^2 ; g_psps=e^{2d} r^2 sth^2
    dt_g[..., TH, TH] =  2*ct*e2c*r**2;      dtt_g[..., TH, TH] = (2*ctt + 4*ct*ct)*e2c*r**2
    dt_g[..., PS, PS] =  2*dt*e2d*r**2*sth**2; dtt_g[..., PS, PS] = (2*dtt + 4*dt*dt)*e2d*r**2*sth**2
    return g, dt_g, dtt_g, a, b, c, d


def time_rows_offround(x, G, n, A0, B0, C0, D0, F0, omega, cph, sph, kap8, m=1, k=0.0,
                       ang=None):
    """OFF-ROUND live time residual rows on a FROZEN off-round background.
    x = (a1,b1,c1,d1,F1) the live amplitude RADIAL coefficients (5 radial functions);
    each multiplies the angular profile `ang(theta)` so the live fluctuation is OFF-ROUND
    (l>=2).  ALL diagonal warps a,b,c,d are live -> the angular diagonal rows G^th_th/
    G^ps_ps carry the d_t^2 inertia the verifier found nonzero off-round.  Pole-stable
    hybrid Einstein (Weyl backbone + kernel time-delta), native S^2 matter EL coupled to
    the full metric, a(phi) ruler (k=0).  Linear in x; quadratic in omega (HB)."""
    if ang is None:
        ang = torch.ones(G.Nr, G.Nth, G.Nps, device=DEV)
    a1 = P5D._expand(G, x[0*n:1*n]) * ang
    b1 = P5D._expand(G, x[1*n:2*n]) * ang
    c1 = P5D._expand(G, x[2*n:3*n]) * ang
    d1 = P5D._expand(G, x[3*n:4*n]) * ang
    F1 = P5D._expand(G, x[4*n:5*n]) * ang
    g, dtg, dttg, a, b, c, d = build_metric_live_offround(G, A0, B0, C0, D0,
                                                          a1, b1, c1, d1, omega, cph, sph)
    ginv = inv4x4(g)
    zer = torch.zeros_like(dtg)
    # pole-stable hybrid: Weyl backbone (static, carries c,d) + kernel time-row DELTA
    Gon,  _, _, _ = P4.einstein_live_kernel(G, g, dtg, dttg)
    Goff, _, _, _ = P4.einstein_live_kernel(G, g, zer, zer)
    Gweyl = F3.einstein_mixed_weyl(G, a, b, c, d)
    Gmix = Gweyl + (Gon - Goff)
    dn, F = P4.field_dn_s2_live(G, F0, F1, omega, cph, sph, m=m)
    Tab, _, _ = P4.stress_live(G, g, ginv, dn, k=k)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8*Tmix
    el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg*G.wvol_coord); W = W/W[G.body].mean()
    sl = slice(3, n-3)
    rows = [
        (W*resE[..., T, T])[sl, :, :],     # G^t_t
        (W*resE[..., R, R])[sl, :, :],     # G^r_r
        (W*resE[..., TH, TH])[sl, :, :],   # G^th_th  (off-round inertia channel)
        (W*resE[..., PS, PS])[sl, :, :],   # G^ps_ps  (off-round inertia channel)
        (W*el)[sl, :, :],                  # matter EL
        (W*resE[..., T, R])[sl, :, :],     # G^t_r momentum (Birkhoff-escape, omega^1)
    ]
    return torch.cat([rr.reshape(-1) for rr in rows])


def amplitude_bc_mask_offround(G, n):
    """Indices in x=(a1,b1,c1,d1,F1) PINNED by regular fluctuation BCs (held=0):
    a1(seal), b1(core), c1(core)/c1(seal), d1(core)/d1(seal), F1(core), F1(seal).
    The angular warps c,d are pinned at both ends (regular at core, sealed at wall)."""
    pinned = set()
    pinned.add(0*n + (n-1))                 # a1(seal)
    pinned.add(1*n + 0)                     # b1(core)
    pinned.add(2*n + 0); pinned.add(2*n + (n-1))   # c1(core), c1(seal)
    pinned.add(3*n + 0); pinned.add(3*n + (n-1))   # d1(core), d1(seal)
    pinned.add(4*n + 0); pinned.add(4*n + (n-1))   # F1(core), F1(seal)
    free = [i for i in range(5*n) if i not in pinned]
    return sorted(pinned), free


def assemble_KCM_offround(G, n, A0, B0, C0, D0, F0, cph, sph, kap8, m=1, k=0.0, eps=1e-6,
                          ang=None):
    """K,C,M of R_time(x;w) = (K + w C - w^2 M) x on the FROZEN OFF-ROUND background,
    by central FD of the off-round time rows at omega in {0,+w1,-w1} and exact
    omega-power separation (same scheme as P5d.assemble_KCM).  `ang` = live-amplitude
    angular profile (l=2 P2 by default -> off-round inertia survives).  5n DOF."""
    pinned, free = amplitude_bc_mask_offround(G, n)

    def Jac(omega):
        x0 = torch.zeros(5*n, device=DEV)
        R0 = time_rows_offround(x0, G, n, A0, B0, C0, D0, F0, omega, cph, sph, kap8, m=m, k=k, ang=ang)
        nF = R0.numel()
        J = torch.zeros(nF, 5*n, device=DEV)
        for j in range(5*n):
            xp = x0.clone(); xp[j] += eps
            xm = x0.clone(); xm[j] -= eps
            Rp = time_rows_offround(xp, G, n, A0, B0, C0, D0, F0, omega, cph, sph, kap8, m=m, k=k, ang=ang)
            Rm = time_rows_offround(xm, G, n, A0, B0, C0, D0, F0, omega, cph, sph, kap8, m=m, k=k, ang=ang)
            J[:, j] = (Rp - Rm)/(2*eps)
        return J, R0

    w1 = 0.5
    J0, R0_0 = Jac(0.0)
    Jp, _ = Jac(+w1)
    Jm, _ = Jac(-w1)
    Kfull = J0
    Cfull = (Jp - Jm)/(2*w1)
    Mfull = -(Jp + Jm - 2*J0)/(2*w1*w1)
    Kf = Kfull[:, free]; Cf = Cfull[:, free]; Mf = Mfull[:, free]
    return Kf, Cf, Mf, free, pinned, R0_0


# ---------------------------------------------------------------------------
# OFF-ROUND BACKGROUNDS
# ---------------------------------------------------------------------------
def warp_background(NR, NTH, NPS, cell, c1=0.05, p=0.4, kap8=0.05, m=1):
    """Round S^2 ground state at the given cell + an l=2 angular warp c0=d0=c1*P2(cos th).
    P2 = (3 cos^2 th - 1)/2 (Legendre).  Returns FULL (Nr,Nth,Nps) background fields."""
    bg = P5D.static_background_cell(NR, NTH, NPS, cell, p=p, kap8=kap8, m=m)
    G = bg['G']; n = bg['n']
    A0 = P5D._expand(G, bg['a']); B0 = P5D._expand(G, bg['b']); F0 = P5D._expand(G, bg['F'])
    cth = torch.cos(G.THg)
    P2leg = 0.5*(3.0*cth*cth - 1.0)
    C0 = c1 * P2leg                      # l=2 warp on g_thth
    D0 = c1 * P2leg                      # l=2 warp on g_psps
    return dict(G=G, n=n, A0=A0, B0=B0, C0=C0, D0=D0, F0=F0, M_MS=bg['M_MS'],
                Phi=bg['Phi'], cell=cell, c1=c1, kind=f'warp_c1={c1}')


def basin_background(NR, seed, cell=14.0, kap8=0.05, m=1):
    """Load a saved off-round floored basin field (oblate/toroidal/prolate/pert_L) and
    build FULL (Nr,Nth,Nps) background fields from its packed u via the full3d unpack.
    Note: saved basins are at cell=14 (p5c default); cell arg ignored for the field,
    used only for the label.  For box-control on basins we re-warp instead (see box)."""
    fp = f"/tmp/p5c_basin_{NR}_{seed}.pt"
    if not os.path.exists(fp):
        raise FileNotFoundError(fp)
    rec = torch.load(fp, weights_only=False)
    NTH = rec['NTH']; NPS = rec['NPS']
    G = F3.Grid3D(Nr=NR, Nth=NTH, Nps=NPS, rc=0.05, cell=rec['wall'])
    G = F3.attach_coord_weight(G)
    from full3d_solver import unpack
    u = rec['u'].to(DEV)
    # unpack -> the full3d field set.  full3d packs (a,b,c,d,Th) as (Nr,Nth,Nps) blocks.
    A0, B0, C0, D0, TH0 = unpack(u, G)
    n = NR
    return dict(G=G, n=n, A0=A0, B0=B0, C0=C0, D0=D0, F0=TH0, M_MS=rec['M_MS'],
                Phi=rec['Phi'], cell=rec['wall'], seed=seed, kind=f'basin_{seed}')


# ---------------------------------------------------------------------------
# DRIVERS
# ---------------------------------------------------------------------------
def _cph_sph():
    return (torch.tensor(math.cos(math.pi/4), device=DEV),
            torch.tensor(math.sin(math.pi/4), device=DEV))


def legendre_P2(G):
    cth = torch.cos(G.THg)
    return 0.5*(3.0*cth*cth - 1.0)


def report_qep(tag, G, n, A0, B0, C0, D0, F0, kap8, M_MS, cell, save_key, extra=None, ang=None):
    cph, sph = _cph_sph()
    if ang is None:
        ang = legendre_P2(G)
    t0 = time.time()
    Kf, Cf, Mf, free, pinned, R0 = assemble_KCM_offround(G, n, A0, B0, C0, D0, F0,
                                                         cph, sph, kap8, ang=ang)
    nK = float(torch.linalg.norm(Kf)); nC = float(torch.linalg.norm(Cf)); nM = float(torch.linalg.norm(Mf))
    print(f"[qep] {tag}  ||K||={nK:.4e} ||C||={nC:.4e} ||M||={nM:.4e}  "
          f"||M||/||K||={nM/(nK+1e-30):.4e}  freeDOF={len(free)}  R0={float(torch.linalg.norm(R0)):.3e}  "
          f"({time.time()-t0:.0f}s)", flush=True)
    ws, sig, wmax = P5D.qep_scan(Kf, Cf, Mf)
    mins = P5D.find_minima(ws, sig)
    sig0 = float(sig[0]); gi = int(np.argmin(sig))
    print(f"[qep] sig_min(w=0)={sig0:.4e}  global-min: w={ws[gi]:.5f} sig={sig[gi]:.4e}  "
          f"wmax={wmax:.3f}", flush=True)
    print(f"[qep] local minima of sigma_min(w):", flush=True)
    for (w, s) in mins[:10]:
        tag2 = "  <-- candidate eigenfreq" if s < 0.2*sig0 + 1e-9 else ""
        print(f"      w={w:8.4f}  sigma_min={s:.4e}{tag2}", flush=True)
    rec = dict(tag=tag, cell=cell, n=n, M_MS=M_MS, normK=nK, normC=nC, normM=nM,
               sig0=sig0, ws=ws, sig=sig, wmax=wmax, mins=mins, R=cell,
               w_globalmin=float(ws[gi]), sig_globalmin=float(sig[gi]))
    if extra: rec.update(extra)
    torch.save(rec, save_key)
    print(f"[qep] saved {save_key}", flush=True)
    return rec


def run_qep(kind, NR, cell, c1=0.05, seed=None):
    NTH = 6 if NR == 12 else 8; NPS = 4
    t0 = time.time()
    if kind == 'warp':
        print(f"[bg] warp bg  Nr={NR} cell={cell} c1={c1} ...", flush=True)
        bg = warp_background(NR, NTH, NPS, cell, c1=c1)
        key = f"/tmp/p5e_qep_warp_{NR}_{int(round(cell*100))}_{int(round(c1*1000))}.pt"
        tag = f"warp Nr={NR} cell={cell} c1={c1}"
        report_qep(tag, bg['G'], bg['n'], bg['A0'], bg['B0'], bg['C0'], bg['D0'], bg['F0'],
                   0.05, bg['M_MS'], cell, key, extra=dict(c1=c1, kind='warp'))
    elif kind == 'basin':
        print(f"[bg] basin bg  Nr={NR} seed={seed} ...", flush=True)
        bg = basin_background(NR, seed)
        key = f"/tmp/p5e_qep_basin_{NR}_{seed}.pt"
        tag = f"basin {seed} Nr={NR} cell={bg['cell']}"
        report_qep(tag, bg['G'], bg['n'], bg['A0'], bg['B0'], bg['C0'], bg['D0'], bg['F0'],
                   0.05, bg['M_MS'], bg['cell'], key, extra=dict(seed=seed, kind='basin'))
    print(f"=== run_qep {kind} DONE  {time.time()-t0:.0f}s ===", flush=True)


def run_probe(kind, NR, cell, c1=0.05):
    """Quick ||K||,||C||,||M|| only (sanity that M!=0 off-round; the cheap pre-check)."""
    NTH = 6 if NR == 12 else 8; NPS = 4
    cph, sph = _cph_sph()
    bg = warp_background(NR, NTH, NPS, cell, c1=c1)
    ang = legendre_P2(bg['G'])
    Kf, Cf, Mf, free, pinned, R0 = assemble_KCM_offround(bg['G'], bg['n'], bg['A0'], bg['B0'],
                                                         bg['C0'], bg['D0'], bg['F0'], cph, sph, 0.05, ang=ang)
    nK = float(torch.linalg.norm(Kf)); nC = float(torch.linalg.norm(Cf)); nM = float(torch.linalg.norm(Mf))
    print(f"[probe] warp Nr={NR} cell={cell} c1={c1}: ||K||={nK:.4e} ||C||={nC:.4e} "
          f"||M||={nM:.4e}  ||M||/||K||={nM/(nK+1e-30):.4e}", flush=True)


def run_box(kind, NR, c1=0.05, seed=None):
    if kind == 'warp':
        fps = sorted(glob.glob(f"/tmp/p5e_qep_warp_{NR}_*_{int(round(c1*1000))}.pt"))
    else:
        fps = sorted(glob.glob(f"/tmp/p5e_qep_basin_{NR}_*.pt"))
    if not fps:
        print(f"  no saved p5e QEP records for kind={kind} Nr={NR}"); return
    print(f"\n=== P5e OFF-ROUND BOX-CONTROL SCAN  kind={kind} Nr={NR} c1={c1} ===", flush=True)
    print(f"  {'cell R':>8} | {'M_MS':>9} | {'||M||':>10} | {'||M||/||K||':>11} | "
          f"{'w_gmin':>9} | {'sig_gmin':>10} | {'w^2':>10} | {'w^2*R^2':>10}", flush=True)
    rows = []
    for fp in fps:
        r = torch.load(fp, weights_only=False)
        w = r['w_globalmin']; s = r['sig_globalmin']; Rc = r['cell']
        rows.append((Rc, r['M_MS'], r['normM'], r['normM']/(r['normK']+1e-30), w, s))
        print(f"  {Rc:>8.3f} | {r['M_MS']:>9.5f} | {r['normM']:>10.3e} | "
              f"{r['normM']/(r['normK']+1e-30):>11.4e} | {w:>9.5f} | {s:>10.3e} | "
              f"{w*w:>10.4e} | {w*w*Rc*Rc:>10.4e}", flush=True)
    if len(rows) >= 2:
        cells = np.array([x[0] for x in rows]); wmins = np.array([x[4] for x in rows])
        msk = wmins > 1e-7
        if msk.sum() >= 2:
            sl, _ = np.polyfit(np.log(cells[msk]), np.log(wmins[msk]), 1)
            print(f"\n  d(log w)/d(log R) = {sl:+.3f}   "
                  f"(0=intrinsic/R-independent; -1=box-controlled ~1/R)", flush=True)
            sl2, _ = np.polyfit(np.log(cells[msk]), np.log(wmins[msk]**2), 1)
            print(f"  d(log w^2)/d(log R) = {sl2:+.3f}   (0=intrinsic; -2=box ~1/R^2)", flush=True)
        w2R2 = [x[4]**2 * x[0]**2 for x in rows if x[4] > 1e-7]
        if w2R2:
            print(f"  w^2*R^2 spread: min={min(w2R2):.4e} max={max(w2R2):.4e} "
                  f"(CONSTANT => box-controlled ~1/R^2; GROWING ~R^2 => intrinsic)", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]; t0 = time.time()
    if mode == "qep":
        kind = sys.argv[2]; NR = int(sys.argv[3])
        if kind == 'warp':
            cell = float(sys.argv[4]); c1 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.05
            run_qep('warp', NR, cell, c1=c1)
        else:
            cell = float(sys.argv[4]); seed = sys.argv[5]
            run_qep('basin', NR, cell, seed=seed)
    elif mode == "probe":
        kind = sys.argv[2]; NR = int(sys.argv[3]); cell = float(sys.argv[4])
        c1 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.05
        run_probe('warp', NR, cell, c1=c1)
    elif mode == "box":
        kind = sys.argv[2]; NR = int(sys.argv[3])
        if kind == 'warp':
            c1 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
            run_box('warp', NR, c1=c1)
        else:
            seed = sys.argv[4] if len(sys.argv) > 4 else None
            run_box('basin', NR, seed=seed)
    else:
        print(__doc__)
    print(f"=== p5e {mode} total {time.time()-t0:.0f}s ===", flush=True)
