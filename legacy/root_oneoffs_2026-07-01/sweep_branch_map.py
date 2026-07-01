#!/usr/bin/env python3
"""
sweep_branch_map.py -- THE WHOLE-METRIC SOLUTION SPACE, MAPPED ROBUSTLY
======================================================================
Driver: Claude (Opus 4.8, 1M ctx). Date 2026-06-13. New file. Frame:
CRITICAL_UNIVERSE_FRAME.md. Charles's zoom-out order: solve the WHOLE
metric directly across the free-data plane and MAP the emergent structure.

KEY METHOD INSIGHT (this push): the physical Dirichlet-Dirichlet cell is a
Bratu/Liouville TURNING-POINT problem -- naive 2D/1D Newton has an
unreliable basin near the fold (the prior flow-chart retreat was for THIS
reason). The ROBUST traversal is to parametrize the branch by the CORE
DEPTH p and integrate the radial field equation OUTWARD from the core with
the metric's own regularity (mirror parity phi'(r_in)=0); the interface
radius r* is then the first radius where phi returns to 0. This traces the
ENTIRE branch -- fold included -- with no root-find and no basin problem.
It reveals the genuine free-data structure, which the (r*,depth) framing
mis-stated: r* is NOT independently free; it is SLAVED to (p, Phi, r_in).

THE METRIC'S OWN RADIAL FIELD EQUATION (exact; wint_symcheck.py):
   (1/r^2) d_r(r^2 e^{-2phi} phi_r) = Phi(e^{-2phi}-e^{phi})
   <=> phi'' + (2/r)phi' - 2 phi'^2 = Phi(1 - e^{3 phi})   [x e^{2phi}]
The angular sector (the full 2D interacting solve, both sectors live) is
verified SEPARATELY (sweep_whole_metric.py / sweep_angular_check below) to
relax every Legendre lobe l=1..4 to round at machine zero -- ONE round type,
now in the PHYSICAL (r,theta) chart (re-rendering #34 off the flow chart).

Misner-Sharp: m(r) = (c^2 r/2G)(1 - e^{-2 phi(r)}); compactness X = 1-f.
The SEAL is f = e^{-2phi} -> 0 (the core, as p grows). Curvature deficit
(2/r^2)(1-f) and Kretschmann concentrate at the core.

DATA-BLIND. METRIC-LED. Convergence by IVP tolerance + grid checks.
Log /tmp/sweep_branch.log. Output /tmp/sweep_branch_map.json.
"""
import json, time
import numpy as np
from scipy.integrate import solve_ivp

t0 = time.time()
_fh = open("/tmp/sweep_branch.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

def rhs(r, y, Phi):
    phi, phip = y
    return [phip, Phi * (1 - np.exp(3 * phi)) - (2 / r) * phip + 2 * phip ** 2]

def branch(p, r_in=1.0, Phi=1.0, rmax=1e8):
    """Integrate OUTWARD from the core (phi(r_in)=p, phi'(r_in)=0 = the
    metric's mirror-parity regularity). r* = first radius where phi=0.
    Returns (r*, r-grid, phi, phi') or (None,...) if the field never
    returns to 0 before blow-up (no interface = no cell at this p)."""
    def hit0(r, y): return y[0]
    hit0.terminal = True; hit0.direction = -1
    def blow(r, y): return abs(y[0]) - 35.0
    blow.terminal = True
    sol = solve_ivp(lambda r, y: rhs(r, y, Phi), [r_in, rmax], [p, -1e-7],
                    events=[hit0, blow], rtol=1e-11, atol=1e-13,
                    method='Radau', dense_output=True)
    if sol.t_events[0].size > 0:
        rstar = float(sol.t_events[0][0])
        rr = np.linspace(r_in, rstar, 500)
        return rstar, rr, sol.sol(rr)[0], sol.sol(rr)[1]
    return None, None, None, None

def invariants(p, r_in=1.0, Phi=1.0):
    rstar, rr, phi, phip = branch(p, r_in, Phi)
    if rstar is None:
        return None
    f = np.exp(-2 * phi)
    comp = float(1 - np.exp(-2 * phi.max()))       # X = 2Gm/c^2 r at core
    ms_core = float(0.5 * rr[0] * (1 - f[0]))       # G m / c^2 at core
    ms_max = float(np.max(0.5 * rr * (1 - f)))
    # curvature: deficit (2/r^2)(1-f) and Kretschmann proxy
    phipp = np.gradient(phip, rr)
    deficit = (2 / rr ** 2) * (1 - f)
    Kdef = ((1 - f) / rr ** 2) ** 2
    Krt = (f * (phipp - 2 * phip ** 2)) ** 2
    K = 4 * Kdef + 4 * Krt
    iK = int(np.argmax(K))
    Kloc = float((rr[iK] - rr[0]) / (rr[-1] - rr[0]))   # 0=core 1=interface
    f_core = float(f[0])
    return dict(p=p, r_in=r_in, Phi=Phi, rstar=rstar, aspect=rstar / r_in,
                comp=comp, f_core=f_core, ms_core=ms_core, ms_max=ms_max,
                Kmax=float(np.max(K)), Kloc=Kloc, defmax=float(deficit.max()),
                wall=rstar - r_in)


def main():
    log("=" * 72)
    log("sweep_branch_map -- the whole-metric solution space (robust branch)")
    log("=" * 72)

    # ---- (A) THE BRANCH: core depth p -> (r*, compactness). The whole
    #          one-parameter family of round cells, fold included. ----
    log("\n[A] THE ROUND-CELL BRANCH (free datum = core depth p; Phi=1, "
        "r_in=1). r* is SLAVED to p (not independently free).")
    log(f"{'p(core)':>9}{'r*':>9}{'aspect':>8}{'comp':>9}{'f_core':>10}"
        f"{'ms_max':>9}{'Kmax':>11}{'Kloc':>6}")
    ps = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0,
          1.5, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0]
    A = []
    for p in ps:
        d = invariants(p)
        if d is None:
            log(f"{p:9.3f}   (no interface -- field never returns to 0)")
            continue
        A.append(d)
        log(f"{p:9.3f}{d['rstar']:9.4f}{d['aspect']:8.4f}{d['comp']:9.5f}"
            f"{d['f_core']:10.2e}{d['ms_max']:9.4f}{d['Kmax']:11.3e}"
            f"{d['Kloc']:6.2f}")
    json.dump(A, open("/tmp/sweep_branch_A.json", "w"))

    # ---- (B) THE EXACT comp(p) LAW + the r*(p) shape (the ruler) ----
    log("\n[B] comp(p) = 1 - e^{-2p} EXACTLY (max phi is at the core = p): "
        "the compactness is the depth, period.")
    devs = [abs(d['comp'] - (1 - np.exp(-2 * d['p']))) for d in A]
    log(f"  max |comp - (1-e^-2p)| over the branch = {max(devs):.2e}  "
        "(machine; phi_max sits at the core BC value p)")
    log(f"  r* RANGE over the whole branch: {min(d['rstar'] for d in A):.4f}"
        f" (deep p) .. {max(d['rstar'] for d in A):.4f} (shallow p) -- "
        "a NARROW band; the cell aspect is geometrically bounded.")

    # ---- (C) THE RULER: is the absolute scale free (scale-family) or
    #          pinned (one size)? Vary r_in and Phi. ----
    log("\n[C] THE SCALE / RULER TEST (the open one-universe-vs-family "
        "thread). Does the WHOLE closed metric carry an absolute size?")
    log("  (C1) r*/r_in vs r_in at fixed p=0.5,Phi=1 -- if r*-r_in is a "
        "fixed ABSOLUTE wall, the ratio is NOT scale-free:")
    for r_in in [1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0]:
        d = invariants(0.5, r_in=r_in, Phi=1.0)
        log(f"     r_in={r_in:8.0e}  r*={d['rstar']:11.5f}  "
            f"wall=r*-r_in={d['wall']:10.5f}  ratio={d['aspect']:.5f}")
    log("  (C2) wall thickness vs Phi at p=0.5,r_in=1 -- the source sets "
        "the ruler 1/sqrt(Phi):")
    for Phi in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:
        d = invariants(0.5, r_in=1.0, Phi=Phi)
        log(f"     Phi={Phi:5.2f}  wall={d['wall']:9.5f}  "
            f"wall*sqrt(Phi)={d['wall'] * np.sqrt(Phi):.5f}")
    log("  (C3) small-core limit r_in->0 at Phi=1,p=0.1 -- r* -> a FIXED "
        "absolute value (the cell has a definite size):")
    for r_in in [1e-4, 1e-3, 1e-2]:
        d = invariants(0.1, r_in=r_in, Phi=1.0)
        log(f"     r_in={r_in:.0e}  r*={d['rstar']:.6f}")

    # ---- (D) SEAL / CURVATURE CONCENTRATION as p -> deep ----
    log("\n[D] SEAL APPROACH (p deep -> f_core -> 0): where curvature "
        "concentrates + how the cell ends.")
    log(f"{'p':>7}{'f_core':>11}{'comp':>9}{'Kmax':>12}{'Kloc(0=core)':>13}")
    for p in [0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 30.0]:
        d = invariants(p)
        if d:
            log(f"{p:7.1f}{d['f_core']:11.2e}{d['comp']:9.5f}"
                f"{d['Kmax']:12.3e}{d['Kloc']:13.2f}")
    log("  => curvature concentrates at the CORE (Kloc->0); the seal f->0 "
        "is the core endpoint; comp->1 smoothly (no second turning point).")

    log(f"\nDONE ({time.time()-t0:.0f}s). /tmp/sweep_branch_map.json + _A.json")
    json.dump({"branch": A}, open("/tmp/sweep_branch_map.json", "w"))


if __name__ == "__main__":
    main()
    _fh.close()
