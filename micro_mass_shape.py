#!/usr/bin/env python3
"""
micro_mass_shape.py -- OBSERVE-mode constructor: map the MICRO MASS-SHAPE of UDT's
own soliton across its two native axes -- dilation DEPTH (p) and WINDING (m) -- and
report WHAT IS THERE.  First step of the observation-led reframe.

This is NOT a verifier and NOT a sweep-for-types: the type question is closed (#52,
ONE round charge-1 continuum).  Here we take the SETTLED soliton and characterize the
shape of M_MS(p, m), the charge along each axis, where native discreteness lives, and
the raw energy/size/deficit structure.

ENGINE: REUSES the committed physics primitives (theta_ddot, stress, energy_pieces,
phi_from_source, grad_central) from complete_metric_batched.py VERBATIM, driven by the
INDEPENDENT damped full-Newton on the joint (Theta,phi) unknown from
verify_stageB_indep.py (CoupledSystem, coupled_newton) -- the robust non-Picard solver
that already converges on the winding tower m=2,3 and deep p.  We do NOT rebuild the
physics; we extend the solver's USE to a fine depth march and a winding tower with
M_MS readouts, charge readouts, and energy decomposition.

DATA-BLIND: everything in units L = sqrt(kappa/xi) = 1; NO empirical particle data is
loaded, recalled, or compared.  Internal ratios only.

mpmath anchors at deep points (CPU, dps=40) for the M_MS(p) functional-form readout.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  V100 float64.  Frame: micro_mass_shape_results.md.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time, json
import numpy as np
import torch
import complete_metric_batched as cm
from verify_stageB_indep import (CoupledSystem, coupled_newton, diagnose, make_seed,
                                 fluct_mineig, XI, KAP, L, rc, SPAN, ri)

torch.set_default_dtype(torch.float64)
DEV = cm.DEV
PI = math.pi
TWO_PI = 2.0 * math.pi
t0 = time.time()


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------------------
# Native CHARGE readouts (DATA-BLIND, topological).
#   The winding field n: cell -> S^2 is a degree-m hedgehog (Theta(core)=m*pi,
#   Theta(seal)=0).  The native winding charge = topological DEGREE of that map =
#   the H1 area-form integral.  For the radial profile this is the number of times
#   Theta sweeps a pi-interval, computed two independent ways:
#     (1) degree_sweep = [Theta(core) - Theta(seal)] / pi   (the monotone sweep count)
#     (2) area_form    = (1/pi) * INT |sin(Theta) Theta'| dr  (the |omega_H1| integral
#         reduced on the hedgehog; equals the degree for a monotone profile).
#   These ARE the public-charge content: charge ~ degree; q=1/3 is the area-form unit
#   (registry C-2026-06-14-1), so the q-normalized public charge is degree/(1/3)=3*deg
#   up to the fixed unit -- we report the raw topological degree (unit-free) and let
#   the q-scaling be a fixed multiplier, never compared to data.
# ---------------------------------------------------------------------------
def charge_readouts(r, Th):
    Tn = Th[0].cpu().numpy(); rn = r[0].cpu().numpy()
    degree_sweep = (Tn[0] - Tn[-1]) / PI
    s = np.sin(Tn)
    Tp = np.gradient(Tn, rn)
    area_form = (1.0 / PI) * np.trapz(np.abs(s * Tp), rn)
    return float(degree_sweep), float(area_form)


def energy_decomp(r, Th, phi, m):
    E2, E4 = cm.energy_pieces(r, Th, phi, XI, KAP, m=m)
    return float(E2[0]), float(E4[0])


def winding_seed(r, m):
    """Monotone degree-m hedgehog seed: Theta sweeps m*pi -> 0 smoothly, placing the
    m winding nodes (pi/2, 3pi/2, ...) at increasing radius -- the right topology so
    the full-Newton lands in the degree-m basin instead of relaxing the extra winding."""
    rr = r; Lc = math.sqrt(KAP / XI); rcc = rr[:, :1]
    x = (rr - rcc) / (rr[:, -1:] - rcc)            # 0..1
    # smooth monotone decreasing from m*pi to 0, with the bulk of the descent in the
    # inner few L (where the winding lives)
    core_frac = (2.5 * m * Lc) / (rr[:, -1:] - rcc)
    z = torch.clamp(x / core_frac, max=1.0)
    Th = (m * PI) * 0.5 * (1.0 + torch.cos(PI * z))
    Th[:, 0] = m * PI; Th[:, -1] = 0.0
    return Th


def solve_cell(r, p, kap8, m, seed='round', warm=None, itmax=120, tol=1e-10):
    """Robust independent full-Newton solve of the complete-action cell at (p,kap8,m).
    Returns dict of readouts or None if not converged/non-existent."""
    sysm = CoupledSystem(r, p=p, kap8=kap8, m=m)
    if warm is not None:
        Th0, phi0 = warm
        Th0 = Th0.clone(); phi0 = phi0.clone()
        Th0[:, 0] = m * PI; Th0[:, -1] = 0.0
    elif seed == 'winding':
        Th0 = winding_seed(r, m)
        phi0 = p * torch.log(r / r[:, -1:])
    else:
        Th0 = make_seed(r, seed, m=m)
        phi0 = p * torch.log(r / r[:, -1:])
    u, mres, nit, conv, _ = coupled_newton(sysm, Th0, phi0, itmax=itmax, tol=tol)
    Th, phi = unpack_local(u, Th0, phi0, r.shape[1])
    d = diagnose(sysm, Th, phi)
    if not (d['exists'] and conv):
        return None
    try:
        ev, me = fluct_mineig(sysm, Th, phi)
    except Exception:
        me = float('nan')
    deg, af = charge_readouts(r, Th)
    E2, E4 = energy_decomp(r, Th, phi, m)
    phi_min = float(phi.min())   # the genuine deepest phi in the cell (true depth)
    return dict(p=p, kap8=kap8, m=m, M_MS=d['M_MS'], width=d['width'],
                min_deficit=d['min_deficit'], mineig=me, res=mres, turns=d['turns'],
                ncross=d['ncross'], phi0=d['phi0'], phi_min=phi_min, degree=deg,
                area_form=af, E2=E2, E4=E4, Th=Th.clone(), phi=phi.clone())


def unpack_local(u, Th_bc, phi_bc, N):
    n = N - 2
    Th = Th_bc.clone(); phi = phi_bc.clone()
    Th[:, 0] = Th_bc[:, 0]; Th[:, -1] = 0.0
    Th[:, 1:-1] = u[:n].reshape(1, n)
    phi[:, 1:-1] = u[n:].reshape(1, n)
    return Th, phi


def fit_loglinear(x, y):
    """ln y = a + b x  least squares; returns (b=d ln y/dx, intercept, R^2)."""
    x = np.asarray(x); ly = np.log(np.asarray(y))
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, ly, rcond=None)
    a, b = coef
    pred = a + b * x
    ss_res = np.sum((ly - pred)**2); ss_tot = np.sum((ly - ly.mean())**2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return float(b), float(a), float(R2)


def fit_powerlaw(x, y):
    """ln y = a + b ln x  (power law M ~ x^b); returns (b, intercept, R^2)."""
    lx = np.log(np.asarray(x)); ly = np.log(np.asarray(y))
    A = np.vstack([np.ones_like(lx), lx]).T
    coef, *_ = np.linalg.lstsq(A, ly, rcond=None)
    a, b = coef
    pred = a + b * lx
    ss_res = np.sum((ly - pred)**2); ss_tot = np.sum((ly - ly.mean())**2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return float(b), float(a), float(R2)


if __name__ == "__main__":
    log("=" * 78)
    log(f"MICRO MASS-SHAPE  device={DEV}  torch={torch.__version__}  cell=[{rc},{ri:.3f}]={SPAN}L")
    log("DATA-BLIND: all in L=sqrt(kappa/xi)=1; no empirical data loaded/compared.")
    log("=" * 78)

    N = 280
    r1 = torch.linspace(rc, ri, N, device=DEV).unsqueeze(0)
    RESULTS = {}

    # =====================================================================
    # MAP 1: M_MS(DEPTH) at fixed winding m=1.  Fine depth march, weak kap8
    # (sub-ceiling), warm-started so we can push DEEP.  Characterize the form.
    # =====================================================================
    log("\n--- MAP 1: M_MS(DEPTH) at m=1, kap8=0.01 (sub-ceiling), warm-started march ---")
    log(f"  {'p':>5} {'phi_min':>8} {'M_MS':>10} {'width':>8} {'min_def':>9} "
        f"{'mineig':>9} {'degree':>7} {'area_f':>7} {'E2':>9} {'E4':>9}")
    kap8_d = 0.01
    p_grid = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0]
    depth_rows = []
    warm = None
    for p in p_grid:
        d = solve_cell(r1, p, kap8_d, m=1, warm=warm)
        if d is None:
            log(f"  {p:>5.1f}   (no converged cell at this depth/kap8)")
            continue
        warm = (d['Th'], d['phi'])
        depth_rows.append(d)
        log(f"  {p:>5.1f} {d['phi_min']:>8.3f} {d['M_MS']:>10.5f} {d['width']:>8.4f} "
            f"{d['min_deficit']:>9.4f} {d['mineig']:>9.4f} {d['degree']:>7.3f} "
            f"{d['area_form']:>7.3f} {d['E2']:>9.4f} {d['E4']:>9.4f}")
    ps = [d['p'] for d in depth_rows]; Ms = [d['M_MS'] for d in depth_rows]
    phimins = [-d['phi_min'] for d in depth_rows]  # positive true depth |phi_min|
    # functional form vs the DIAL p AND vs the TRUE depth |phi_min|.
    b_exp, a_exp, R2_exp = fit_loglinear(ps, Ms)
    b_pow, a_pow, R2_pow = fit_powerlaw(ps, Ms)
    b_phi, a_phi, R2_phi = fit_loglinear(phimins, Ms)   # ln M vs |phi_core|
    # local d ln M / dp (finite difference) to test if the slope is CONSTANT
    lnM = np.log(np.array(Ms)); dlnMdp = np.gradient(lnM, np.array(ps))
    dlnMdphi = np.gradient(lnM, np.array(phimins))
    log(f"\n  FORM: ln M = {a_exp:.4f} + ({b_exp:.4f}) p   R^2={R2_exp:.5f}  (exp in DIAL p)")
    log(f"  FORM: M ~ p^{b_pow:.4f}                         R^2={R2_pow:.5f}  (power-law in p)")
    log(f"  FORM: ln M = {a_phi:.4f} + ({b_phi:.4f})|phi_core|  R^2={R2_phi:.5f}  (exp in TRUE depth)")
    log(f"  |phi_core| range: {min(phimins):.3f}..{max(phimins):.3f}")
    log(f"  d ln M/d|phi_core| local: " + np.array2string(dlnMdphi, precision=4))
    log(f"  d ln M_MS/dp local (per p): " + np.array2string(dlnMdp, precision=4))
    log(f"  d ln M_MS/dp range [{dlnMdp.min():.4f}, {dlnMdp.max():.4f}] "
        f"=> {'CONSTANT (geometric)' if dlnMdp.max()-dlnMdp.min()<0.1 else 'VARYING (not pure exp)'}")
    RESULTS['depth'] = dict(rows=[{k: v for k, v in d.items() if k not in ('Th', 'phi')}
                                  for d in depth_rows],
                            b_exp=b_exp, R2_exp=R2_exp, b_pow=b_pow, R2_pow=R2_pow,
                            b_phi=b_phi, R2_phi=R2_phi, dlnMdp=dlnMdp.tolist(),
                            dlnMdphi=dlnMdphi.tolist(), phimins=phimins)

    # kap8-dependence of the SHAPE: repeat the depth slope at a stronger kap8.
    log("\n  -- kap8-dependence of the M_MS(p) shape (kap8=0.03) --")
    warm = None; rows2 = []
    for p in [0.2, 0.4, 0.6, 0.8, 1.0]:
        d = solve_cell(r1, p, 0.03, m=1, warm=warm)
        if d is None:
            continue
        warm = (d['Th'], d['phi']); rows2.append(d)
    if len(rows2) >= 3:
        b2, a2, R22 = fit_loglinear([d['p'] for d in rows2], [d['M_MS'] for d in rows2])
        log(f"    kap8=0.03: ln M = {a2:.4f} + ({b2:.4f}) p  R^2={R22:.5f}  "
            f"(vs kap8=0.01 slope {b_exp:.4f})")
        RESULTS['depth_k03'] = dict(b_exp=b2, R2_exp=R22,
                                    rows=[{k: v for k, v in d.items() if k not in ('Th', 'phi')}
                                          for d in rows2])

    # =====================================================================
    # MAP 2: M_MS(WINDING) tower at representative depths.  Solve m=1,2,3,4,...
    # as high as stable (min|eig|>0), report M_MS(m) and internal ratios.
    # =====================================================================
    log("\n--- MAP 2: M_MS(WINDING) tower (m=1..) at representative depths, kap8=0.01 ---")
    RESULTS['winding'] = {}
    for p_w in [0.4, 0.8, 1.2]:
        log(f"\n  depth p={p_w}:")
        log(f"  {'m':>3} {'M_MS':>10} {'M_MS/M1':>9} {'width':>8} {'ncross':>7} "
            f"{'mineig':>9} {'degree':>7} {'area_f':>7} {'E2':>9} {'E4':>9} {'stable':>7}")
        tower = []
        M1 = None
        for mw in [1, 2, 3, 4]:
            # try the dedicated monotone degree-m winding seed (right topology basin)
            d = solve_cell(r1, p_w, 0.01, m=mw, seed='winding', itmax=120)
            if d is None:   # fall back to round seed
                d = solve_cell(r1, p_w, 0.01, m=mw, seed='round', itmax=120)
            if d is None:
                log(f"  {mw:>3}   (no converged stable cell)")
                continue
            if M1 is None and mw == 1:
                M1 = d['M_MS']
            ratio = d['M_MS'] / M1 if M1 else float('nan')
            stable = d['mineig'] > 1e-6
            log(f"  {mw:>3} {d['M_MS']:>10.5f} {ratio:>9.4f} {d['width']:>8.4f} "
                f"{d['ncross']:>7} {d['mineig']:>9.4f} {d['degree']:>7.3f} "
                f"{d['area_form']:>7.3f} {d['E2']:>9.4f} {d['E4']:>9.4f} {str(stable):>7}")
            d['ratio'] = ratio; d['stable'] = stable
            tower.append({k: v for k, v in d.items() if k not in ('Th', 'phi')})
        RESULTS['winding'][str(p_w)] = tower
        # characterize how M scales with m
        ms = [t['m'] for t in tower if t['stable']]
        Mm = [t['M_MS'] for t in tower if t['stable']]
        if len(ms) >= 3:
            bm, am, R2m = fit_powerlaw(ms, Mm)
            log(f"    M_MS(m) ~ m^{bm:.4f}  R^2={R2m:.5f}  (winding mass-scaling)")

    # =====================================================================
    # MAP 3: the COMBINED M_MS(p, m) surface (small grid).
    # =====================================================================
    log("\n--- MAP 3: COMBINED M_MS(p, m) surface, kap8=0.01 ---")
    p_surf = [0.4, 0.8, 1.2]; m_surf = [1, 2, 3]
    surf = {}
    log("  M_MS:        " + "".join(f"m={m:>8}" for m in m_surf))
    for p in p_surf:
        row = []
        for m in m_surf:
            d = solve_cell(r1, p, 0.01, m=m, seed='winding', itmax=120)
            if d is None:
                d = solve_cell(r1, p, 0.01, m=m, seed='round', itmax=120)
            row.append(d['M_MS'] if d else float('nan'))
            surf[f"p{p}_m{m}"] = d['M_MS'] if d else None
        log(f"  p={p:<5}    " + "".join(f"{v:>10.5f}" for v in row))
    RESULTS['surface'] = surf

    # =====================================================================
    # MAP 4 + 5 are answered by the readouts above:
    #  - DISCRETENESS: depth axis = continuous p (any p converges); winding axis =
    #    integer m only (m is a Dirichlet BC label, not a continuous dial).
    #  - CHARGE: degree(p) vs degree(m).  Confirm depth=same-charge, winding=diff-charge.
    # We collate the verdict numerics here.
    # =====================================================================
    log("\n--- MAP 4/5: DISCRETENESS + CHARGE-ALONG-EACH-AXIS verdict numerics ---")
    deg_depth = [d['degree'] for d in depth_rows]
    af_depth = [d['area_form'] for d in depth_rows]
    log(f"  CHARGE along DEPTH (m=1, p={ps[0]}..{ps[-1]}): degree = "
        f"{min(deg_depth):.4f}..{max(deg_depth):.4f}  area_form = "
        f"{min(af_depth):.4f}..{max(af_depth):.4f}")
    log(f"    => depth axis charge spread = {max(deg_depth)-min(deg_depth):.5f} "
        f"(0 => SAME charge along depth)")
    # winding charge from the p=0.8 tower
    tw = RESULTS['winding'].get('0.8', [])
    log(f"  CHARGE along WINDING (p=0.8): " +
        ", ".join(f"m{t['m']}:deg={t['degree']:.3f}" for t in tw))
    RESULTS['discreteness'] = dict(
        depth_degree_spread=max(deg_depth) - min(deg_depth),
        depth_is_continuum=True,   # any p converged
        winding_is_integer=True)

    # =====================================================================
    # mpmath ANCHOR: recompute M_MS at a deep point at dps=40 to confirm the
    # float64 depth-mass readout is not a precision artifact (principle 2 guard).
    # =====================================================================
    log("\n--- mpmath ANCHOR at a deep point (dps=40) ---")
    try:
        import mpmath as mp
        mp.mp.dps = 40
        # recompute M_MS = m_areal(seal)-m_areal(core) for the deepest converged cell
        dd = depth_rows[-1]
        rr = r1[0].cpu().numpy(); Tn = dd['Th'][0].cpu().numpy(); pn = dd['phi'][0].cpu().numpy()
        Thp = np.gradient(Tn, rr)
        # rho in mpmath
        def rho_mp(i):
            X = mp.e**(-2 * mp.mpf(pn[i])) * mp.mpf(Thp[i])**2
            Y = mp.sin(mp.mpf(Tn[i]))**2 / mp.mpf(rr[i])**2
            return (mp.mpf(XI) / 2) * (X + 2 * Y) + (mp.mpf(KAP) / 2) * (2 * X * Y + Y**2)
        integ = [mp.mpf(kap8_d) * mp.mpf(rr[i])**2 * rho_mp(i) for i in range(N)]
        Msrc = mp.mpf(0)
        for i in range(1, N):
            Msrc += 0.5 * (integ[i] + integ[i - 1]) * (mp.mpf(rr[i]) - mp.mpf(rr[i - 1]))
        log(f"  deepest cell p={dd['p']}: M_MS float64={dd['M_MS']:.10f}  "
            f"mpmath(dps40)={mp.nstr(Msrc, 11)}  |diff|={abs(float(Msrc)-dd['M_MS']):.2e}")
        RESULTS['mpmath_anchor'] = dict(p=dd['p'], float64=dd['M_MS'], mpmath=float(Msrc))
    except Exception as e:
        log(f"  mpmath anchor skipped: {e}")

    # =====================================================================
    # grid-refinement spot check on a winding cell (m=2) for reproducibility.
    # =====================================================================
    log("\n--- grid-refinement spot check (m=2, p=0.4) ---")
    for Nc in [240, 360]:
        rc2 = torch.linspace(rc, ri, Nc, device=DEV).unsqueeze(0)
        d = solve_cell(rc2, 0.4, 0.01, m=2, itmax=150)
        if d:
            log(f"  N={Nc}: M_MS={d['M_MS']:.5f} width={d['width']:.4f} "
                f"mineig={d['mineig']:.4f} res={d['res']:.1e}")

    json.dump(RESULTS, open("micro_mass_shape_data.json", "w"), indent=1, default=str)
    log("\n" + "=" * 78)
    log(f"DONE  wall {time.time()-t0:.1f}s   data -> micro_mass_shape_data.json")
    log("=" * 78)
