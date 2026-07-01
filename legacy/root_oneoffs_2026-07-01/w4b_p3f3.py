"""W4 SOLVER AGENT B — script 7: P3-F3 TARGETED THRESHOLD CHECK.

Pre-registered in w4b_gates.py / w4b_p3_core.py: the DYNAMICAL
instability threshold of the D_cell-ON kappa > 0 branch must match the
SPECTRAL kappa_c within 10%, else the band claim is not banked.

The core catalog seeds a mid-cell bump (x0 = 0.55 x_max), which has
weak overlap with the near-threshold unstable mode (localized toward
the seal end on the near-pole ray) - the catalog's apparent dynamical
threshold is therefore biased LOW at finite T_end. This script does
the honest measurement: seal-end-weighted initial data (x0 = 0.15
x_max), amp 1e-4 (linear regime), T_end = 4x the catalog window,
kappa in {0.85, 0.95, 1.05, 1.15} x kappa_c per member; the measured
growth/decay rate of the energy-weighted amplitude is compared with
the spectral omega^2_min(kappa) (w4b_lingap.npz).

CRITERIA (pre-stated):
  F3-a: sign(instability) flips between 0.95 kc and 1.05 kc
        (threshold within 10% of spectral) for each member; OR the
        run-measured rates, fit to rate^2 = -omega^2_min(kappa),
        locate the zero within 10% of kc.
  F3-b: in the unstable cells the measured exponential rate matches
        sqrt(-omega^2_min) within 25% (mode-overlap and finite-T
        tolerance, pre-stated).
Log: /tmp/w4b_p3f3.log. New file. 2026-06-12, W4-B agent.
"""
import numpy as np
import w4b_evolib as ev


def log(*a):
    print(*a, flush=True)


npz = np.load("/tmp/w4b_bg.npz")
lin = np.load("/tmp/w4b_lingap.npz")
PASS, FAIL = [], []


def check(label, ok):
    (PASS if ok else FAIL).append(label)
    log(("PASS" if ok else "FAIL"), label)


AMP = 1e-4
results = {}
for tag in ("M1", "M2", "M4"):
    geo = ev.Geo(npz, tag, Nu=24, Nx=1024)
    kc = float(lin[f"{tag}_kc"])
    kgrid = np.array([0.85, 0.95, 1.05, 1.15]) * kc
    v0 = ev.bump_profile(geo, AMP, "g1", x0frac=0.15, sig_frac=0.10)
    v0b = np.array([v0] * len(kgrid))
    T_end = 48.0 * float(np.max(geo.xmax))
    resb = ev.evolve_torch(geo, v0b, np.zeros_like(v0b), kgrid, True,
                           T_end, log=log)
    rates = []
    for b, kk in enumerate(kgrid):
        env = resb["env"][b]
        T = resb["T"]
        n = len(env)
        # rate from the final half (clean of transients)
        sl = np.polyfit(T[n // 2:],
                        np.log(np.maximum(env[n // 2:], 1e-300)), 1)[0]
        lab, diag = ev.classify_batch(resb, b, AMP)
        w2 = None
        rates.append((float(kk), float(sl), lab))
        log(f"{tag} k={kk:.5f} ({kk/kc:.2f} kc): rate={sl:+.4f} "
            f"label={lab} env_max={diag.get('env_max', np.nan):.3g} "
            f"drift={diag.get('edrift', np.nan):.1e}")
    results[tag] = (kc, rates)
    # threshold from rate sign flip (linear interp in kappa)
    rs = np.array([r[1] for r in rates])
    ks = np.array([r[0] for r in rates])
    if rs[0] > 0 and rs[-1] <= 0.005:
        # find crossing of rate -> 0 between grid points
        idx = np.where(np.diff(np.sign(rs - 0.002)))[0]
        if len(idx):
            i = idx[0]
            kdyn = ks[i] + (0.002 - rs[i]) * (ks[i + 1] - ks[i]) \
                / (rs[i + 1] - rs[i])
        else:
            kdyn = np.nan
    else:
        kdyn = np.nan
    log(f"{tag}: spectral kc={kc:.5f}, dynamical threshold ~ "
        f"{kdyn:.5f} ({kdyn/kc:.3f} kc)" if np.isfinite(kdyn) else
        f"{tag}: no clean rate sign flip (rates: {rs})")
    check(f"{tag} F3-a dynamical threshold within 10% of spectral "
          f"kappa_c", np.isfinite(kdyn) and abs(kdyn - kc) / kc <= 0.10)
    # F3-b rate magnitude at 0.85 kc vs spectral
    geo512 = geo
    # spectral omega^2_min at 0.85 kc on the most unstable ray
    import scipy.linalg as sla
    kray = int(lin[f"{tag}_kray"])
    dx = geo.dx[kray]
    r2 = geo.r[kray]**2
    fth2 = geo.fth2[kray]
    N = geo.Nx
    r2m = 0.5 * (r2[1:] + r2[:-1])
    A = np.zeros((N, N))
    ii = np.arange(N - 1)
    A[ii, ii] += r2m / dx
    A[ii + 1, ii + 1] += r2m / dx
    A[ii, ii + 1] -= r2m / dx
    A[ii + 1, ii] -= r2m / dx
    wxs = np.full(N, dx)
    wxs[0] = wxs[-1] = dx / 2
    B = np.diag(3 * geo.c / 16 * fth2 * wxs)
    M = np.diag(r2 * wxs)
    keep = np.arange(N)[1:]
    A, B, M = (Z[np.ix_(keep, keep)] for Z in (A, B, M))
    w2min = sla.eigh(A - B / (0.85 * kc), M, eigvals_only=True,
                     subset_by_index=[0, 0])[0]
    pred = np.sqrt(max(-w2min, 0.0))
    meas = rates[0][1]
    log(f"{tag} F3-b at 0.85 kc: predicted rate {pred:.4f}, measured "
        f"{meas:.4f}")
    check(f"{tag} F3-b unstable-cell rate within 25% of spectral",
          pred > 0 and abs(meas - pred) / pred <= 0.25)

log("")
log(f"PASS: {len(PASS)}  FAIL: {len(FAIL)}")
if FAIL:
    log("FAILED: " + "; ".join(FAIL))
