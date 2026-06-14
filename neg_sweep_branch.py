#!/usr/bin/env python3
"""
neg_sweep_branch.py -- THE NEGATIVE-PHI MATTER-CELL BOUNDARY SWEEP
=================================================================
Driver: Claude (Opus 4.8, 1M ctx). Date 2026-06-13. New file. Frame:
CRITICAL_UNIVERSE_FRAME.md + CANON C-2026-06-10-2 (matter cells inside-out,
phi:0 at the interface -> NEGATIVE toward the core; the whole structure the
MIRROR across phi->-phi of the universe cell, whose boundary is the CMB at
phi=+7.004=ln(1101)).

CORRECTS a regime error: the prior sweep (sweep_branch_map.py / #39) ran in
POSITIVE phi (core depth p>0). By canon MATTER LIVES AT NEGATIVE PHI. This
sweep flips the core into negative phi.

THE METRIC'S OWN RADIAL FIELD EQUATION (exact; wint_symcheck.py; identical
operator, NOT re-derived -- built on, per the order):
   (1/r^2) d_r(r^2 e^{-2phi} phi_r) = Phi(e^{-2phi}-e^{phi})
   <=> phi'' + (2/r)phi' - 2 phi'^2 = Phi(1 - e^{3 phi})   [x e^{2phi}]

INSIDE-OUT MATTER CELL: phi(r_in)=p with p<0 (NEGATIVE core), phi'(r_in)=0
(the metric's mirror-parity regularity at the core). r* = the first radius
where phi returns to 0 (the outer interface). The field INCREASES outward
from p<0 to 0.

Wave speeds (CANON C-2026-06-13-1): c_r^2 = e^{-4phi}, c_th^2 = e^{-2phi}/r^2.
At NEGATIVE phi these RUN AWAY LARGE (the reciprocal of the frozen CMB side).
Lapse / time-rate = sqrt(-g_tt) = e^{-phi}: at p<0, e^{-phi}>1 -> time runs
FAST (reciprocal mirror of the CMB freeze e^{-7}).

This script: MAP the negative branch p: 0 -> deep negative; instrument
c_eff, lapse, mass (BOTH sign conventions), compactness, curvature; and
LOCATE where the solution stops existing (the candidate finite boundary).
float64 here for the map; mpmath high-precision refinement lives in
neg_sweep_mpmath.py (so a float OVERFLOW is never mistaken for the physical
boundary). DATA-BLIND. METRIC-LED.

Log /tmp/neg_sweep.log. Output /tmp/neg_sweep_branch.json.
"""
import json, time
import numpy as np
from scipy.integrate import solve_ivp

t0 = time.time()
_fh = open("/tmp/neg_sweep.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

PHI = 1.0
R_IN = 1.0


def rhs(r, y, Phi):
    phi, phip = y
    # phi'' = Phi(1 - e^{3phi}) - (2/r)phi' + 2 phi'^2
    return [phip, Phi * (1.0 - np.exp(3.0 * phi)) - (2.0 / r) * phip + 2.0 * phip ** 2]


def branch(p, r_in=R_IN, Phi=PHI, rmax=1e9, phi_blow=80.0):
    """Integrate OUTWARD from a NEGATIVE core (phi(r_in)=p<0, phi'(r_in)=0+).
    For p<0 the field rises toward 0; we seed phi' slightly POSITIVE so the
    integrator climbs. r* = first radius where phi crosses 0 from below.
    Returns dict or None. phi_blow guards |phi|; we report WHY it stopped."""
    # mirror-parity regularity: phi'(r_in)=0. Seed an infinitesimal positive
    # slope (rising toward the interface) -- matches the prior sweep's -1e-7
    # convention mirrored.
    def hit0(r, y):
        return y[0]
    hit0.terminal = True
    hit0.direction = +1  # crossing 0 from below (rising)
    def blow(r, y):
        return abs(y[0]) - phi_blow
    blow.terminal = True

    sol = solve_ivp(lambda r, y: rhs(r, y, Phi), [r_in, rmax],
                    [p, +1e-7], events=[hit0, blow],
                    rtol=1e-12, atol=1e-14, method='Radau',
                    dense_output=True, max_step=(rmax - r_in))
    reason = None
    if sol.t_events[0].size > 0:
        rstar = float(sol.t_events[0][0])
        reason = "interface (phi->0)"
        rr = np.linspace(r_in, rstar, 800)
        phi = sol.sol(rr)[0]; phip = sol.sol(rr)[1]
        return dict(ok=True, reason=reason, rstar=rstar, rr=rr, phi=phi, phip=phip)
    # no interface
    if sol.t_events[1].size > 0:
        reason = f"|phi| hit {phi_blow} at r={sol.t[-1]:.4g} (runaway, no interface)"
    elif sol.status == 0:
        reason = f"reached rmax={rmax:.2g} without returning to 0"
    else:
        reason = f"integrator stop status={sol.status} at r={sol.t[-1]:.4g}, phi={sol.y[0,-1]:.4g}"
    return dict(ok=False, reason=reason, r_end=float(sol.t[-1]),
                phi_end=float(sol.y[0, -1]), phip_end=float(sol.y[1, -1]))


def instrument(res, Phi=PHI):
    """All diagnostics at every depth for a converged cell."""
    rr = res['rr']; phi = res['phi']; phip = res['phip']
    f = np.exp(-2.0 * phi)                     # = g_tt magnitude factor
    # wave speeds (CANON): radial c_r = e^{-2phi}; angular c_th = e^{-phi}/r
    c_r = np.exp(-2.0 * phi)                   # sqrt(e^{-4phi})
    c_th = np.exp(-phi) / rr                   # sqrt(e^{-2phi}/r^2)
    lapse = np.exp(-phi)                       # sqrt(-g_tt)=e^{-phi}; time-rate
    # mass: Misner-Sharp dilation tie m=(c^2 r/2G)(1-e^{-2phi}); two sign convs
    # convention A: (e^{-2phi}-1)  -> at phi<0, e^{-2phi}>1 -> POSITIVE
    eA = np.exp(-2.0 * phi) - 1.0
    # convention B: (1-e^{-2phi})  -> at phi<0 -> NEGATIVE
    eB = 1.0 - np.exp(-2.0 * phi)
    msA = 0.5 * rr * eA
    msB = 0.5 * rr * eB
    comp = 1.0 - np.exp(-2.0 * phi.min())      # uses extremal phi (the core, min)
    # curvature
    phipp = np.gradient(phip, rr)
    Kdef = ((1.0 - f) / rr ** 2) ** 2
    Krt = (f * (phipp - 2.0 * phip ** 2)) ** 2
    Kret = 4.0 * Kdef + 4.0 * Krt
    # Ricci scalar proxy (sign-agnostic magnitude): use deficit curvature
    iK = int(np.argmax(Kret))
    Kloc = float((rr[iK] - rr[0]) / (rr[-1] - rr[0]))  # 0=core 1=interface
    return dict(
        rstar=res['rstar'], p=float(phi[0]),
        c_r_core=float(c_r[0]), c_r_max=float(c_r.max()),
        c_th_core=float(c_th[0]), c_th_max=float(c_th.max()),
        lapse_core=float(lapse[0]), lapse_max=float(lapse.max()),
        msA_core=float(msA[0]), msA_ext=float(msA.max() if abs(msA.max())>abs(msA.min()) else msA.min()),
        msB_core=float(msB[0]),
        comp=float(comp), f_core=float(f[0]),
        Kmax=float(Kret.max()), Kloc=Kloc,
    )


def main():
    log("=" * 72)
    log("neg_sweep_branch -- NEGATIVE-PHI matter cell (inside-out, p<0)")
    log("=" * 72)
    log("equation: phi'' + (2/r)phi' - 2phi'^2 = Phi(1 - e^{3phi}); Phi=%g r_in=%g" % (PHI, R_IN))
    log("core phi(r_in)=p<0 (mirror-parity phi'=0); interface r*=first phi->0.\n")

    # ---- (A) THE NEGATIVE BRANCH: sweep p downward into negative phi ----
    log("[A] NEGATIVE-PHI BRANCH (core depth p<0). Hadronic phi0~-0.80 is here.")
    hdr = (f"{'p(core)':>9}{'r*':>10}{'comp':>10}{'f_core':>11}"
           f"{'c_r_core':>11}{'c_th_max':>11}{'lapse_c':>10}"
           f"{'msA_core':>11}{'Kmax':>11}{'Kloc':>6}  status")
    log(hdr)
    ps = [-0.01, -0.05, -0.1, -0.2, -0.3, -0.5, -0.7, -0.80, -1.0, -1.5,
          -2.0, -3.0, -4.0, -5.0, -6.0, -6.5, -7.0, -7.004, -7.5, -8.0,
          -9.0, -10.0, -12.0, -15.0, -20.0]
    A = []
    last_ok = None
    first_fail = None
    for p in ps:
        res = branch(p)
        if res['ok']:
            d = instrument(res)
            A.append(d)
            log(f"{p:9.4f}{d['rstar']:10.4f}{d['comp']:10.5f}{d['f_core']:11.3e}"
                f"{d['c_r_core']:11.3e}{d['c_th_max']:11.3e}{d['lapse_core']:10.3e}"
                f"{d['msA_core']:11.3e}{d['Kmax']:11.3e}{d['Kloc']:6.2f}  OK")
            last_ok = p
        else:
            log(f"{p:9.4f}{'--':>10}{'--':>10}{'':>11}{'':>11}{'':>11}{'':>10}"
                f"{'':>11}{'':>11}{'':>6}  FAIL: {res['reason']}")
            if first_fail is None:
                first_fail = p
    json.dump(A, open("/tmp/neg_sweep_branch.json", "w"))
    log(f"\nlast OK p = {last_ok}; first FAIL p = {first_fail}")

    # ---- (B) does a finite boundary exist? Bisection on p between last_ok
    #          and first_fail (float64; refined hard in mpmath separately) ----
    if last_ok is not None and first_fail is not None:
        log("\n[B] BISECTION for the boundary p between last-OK and first-FAIL "
            "(float64; mpmath refinement in neg_sweep_mpmath.py).")
        lo, hi = last_ok, first_fail   # lo OK (less negative), hi FAIL (more negative)
        for it in range(60):
            mid = 0.5 * (lo + hi)
            res = branch(mid)
            tag = "OK" if res['ok'] else "FAIL"
            if res['ok']:
                lo = mid
            else:
                hi = mid
            if it % 5 == 0 or abs(hi - lo) < 1e-6:
                log(f"  it={it:2d} p={mid:.8f} -> {tag}  [lo={lo:.8f} hi={hi:.8f}]"
                    + (f"  ({res['reason']})" if not res['ok'] else ""))
            if abs(hi - lo) < 1e-9:
                break
        log(f"  => float64 boundary p* in [{lo:.9f}, {hi:.9f}]; |gap|={hi-lo:.2e}")
        log(f"  => DATA-BLIND boundary p* ~ {0.5*(lo+hi):.6f}")
        json.dump(dict(p_boundary_lo=lo, p_boundary_hi=hi), open("/tmp/neg_sweep_boundary.json", "w"))

    log(f"\n[done] {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
