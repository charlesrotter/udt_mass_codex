#!/usr/bin/env python3
"""
sf_scan_probe1b.py -- PROBE 1 ADVERSARIAL: is the strong-field min|eig|
decay REAL (approaching a bifurcation) or an ARTIFACT?
=======================================================================
PROBE 1 found the existence-test Jacobian min|eig| TURNS OVER at the trust
edge (E/Um~6) and DECAYS toward 0 as field strength rises (0.145 -> 0.0019
at E/Um=1000). Baseline B1 (E/Um<=6 only) saw monotone RISE and called it
"no bifurcation ever". The character changes past the trust window. Before
flagging: prosecute the decay HARD.

Three discriminators (each separates real-bifurcation from artifact):
  (T1) GRID REFINEMENT. If min|eig| is a true approaching-zero mode it is
       grid-converged (stable as Nm,Nth -> up). If it is a discretization
       artifact of the SHRINKING cell width L (L ~ 1/sqrt(E)), it moves
       with the grid.
  (T2) IS IT JUST TRACKING L? The radial operator d^2/dm^2 on a cell of
       width L has a smallest eigenvalue ~ (pi/L)^2... no -- the BC is
       Neumann so the smallest STIFFNESS eigenvalue scales differently.
       Compute min|eig| * L^2 and min|eig| * L: if either is ~constant the
       decay is pure geometric rescaling (NOT a bifurcation -- a
       bifurcation is min|eig| -> 0 at FIXED operator family). Also do the
       solve in a RESCALED chart (fix the cell to unit width) and see if
       min|eig| is then flat -- that would prove rescaling.
  (T3) THE EIGENVECTOR. A real new-TYPE bifurcation has its near-null mode
       ANGULAR (theta-varying = a shaped type born). Measure the angular
       content of the smallest-|eig| eigenvector at each E. If the
       near-null mode is RADIAL/round (angular content ~0) it is NOT a new
       shaped type -- it is the round-cell family's own zero-mode
       (translation/scaling of the E-continuum), which B2/#33 already
       documents as a CONTINUUM (the cell can slide in E for free).

VERDICT logic: decay is a DOCUMENTED-CONTINUUM artifact if it rescales
with L (T2) AND the mode is angular-free (T3); it is an UNDOCUMENTED
STRONG-FIELD BIFURCATION only if it survives refinement (T1), does NOT
pure-rescale (T2), and the near-null mode goes ANGULAR (T3).
"""
import sys, time, json
import numpy as np, mpmath as mp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from sf_scan_strongfield import (cell_LE, Umin, residual, jac, newton,
                                  solve2d, HAS_GPU, DEV)
if HAS_GPU:
    import torch

t0 = time.time()
_fh = open("/tmp/sf_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

log("\n" + "=" * 72)
log("PROBE 1b -- ADVERSARIAL: strong-field min|eig| decay real vs artifact")
log("=" * 72)

def eig_and_vec(r):
    v = r["v"]; m = r["m"]; th = r["th"]; dm = r["dm"]; dth = r["dth"]
    vlo = r["vlo"]; Nm, Nth = v.shape
    J, _ = jac(v, m, th, dm, dth, 1.0, vlo)
    Jd = J.toarray()
    if HAS_GPU:
        Jt = torch.tensor(Jd, dtype=torch.float64, device=DEV)
        ev, evec = torch.linalg.eig(Jt)
        ev = ev.cpu().numpy(); evec = evec.cpu().numpy()
    else:
        ev, evec = np.linalg.eig(Jd)
    i0 = int(np.argmin(np.abs(ev)))
    w = np.real(evec[:, i0]).reshape(Nm, Nth)
    interior = w[2:-2, 1:-1]
    if np.linalg.norm(interior) < 1e-14:
        ang = 0.0
    else:
        thmean = interior.mean(axis=1, keepdims=True)
        ang = float(np.linalg.norm(interior - thmean) / np.linalg.norm(interior))
    return float(np.abs(ev[i0])), ang

# ---- T1 + T3: grid refinement of min|eig| and its eigenvector angular content
log("\nT1+T3 -- grid refinement of min|eig| and near-null eigenvector "
    "angular content, across field strength")
log(f"{'E/Um':>8} {'nonlin':>10} {'L':>8} | "
    f"{'(81,29)':>22} {'(121,41)':>22} {'(161,55)':>22}")
log(f"{'':>8} {'':>10} {'':>8} | "
    f"{'mineig  ang':>22} {'mineig  ang':>22} {'mineig  ang':>22}")
grids = [(81, 29), (121, 41), (161, 55)]
T1rows = []
for Ef in [2.0, 6.0, 50.0, 200.0, 1000.0]:
    cells = []
    nonlin = L = None
    for (Nm, Nth) in grids:
        r = solve2d(Ef, Nm=Nm, Nth=Nth)
        if not r["conv"]:
            cells.append((np.nan, np.nan)); continue
        nonlin = r["nonlin"]; L = r["L"]
        me, ang = eig_and_vec(r)
        cells.append((me, ang))
    T1rows.append(dict(Ef=Ef, nonlin=nonlin, L=L, cells=cells))
    cs = "  ".join(f"{me:9.5f} {ang:5.2f}" for (me, ang) in cells)
    log(f"{Ef:8.1f} {nonlin if nonlin else 0:10.2e} {L if L else 0:8.4f} | {cs}")

# ---- T2: does min|eig| * L^a track? and a unit-width rescaled solve ----
log("\nT2 -- geometric rescaling test: min|eig| vs L (the cell shrinks "
    "~1/sqrt(E)). If min|eig|*L^2 or *L is ~constant the decay is pure "
    "rescaling of a FIXED operator (a CONTINUUM slide, NOT a bifurcation).")
log(f"{'E/Um':>8} {'L':>8} {'min|eig|':>11} {'me*L':>11} {'me*L^2':>11}")
for row in T1rows:
    me = row["cells"][1][0]  # the (121,41) grid value
    L = row["L"]
    if not np.isfinite(me): continue
    log(f"{row['Ef']:8.1f} {L:8.4f} {me:11.6f} {me*L:11.6f} {me*L*L:11.6f}")

# A cleaner rescaling probe: the RADIAL-only stiffness smallest eigenvalue.
# The full Jacobian's near-null mode -- is it the radial round-cell
# zero-mode (the E-continuum, documented B2b/#33) re-expressed at strong
# field? Compute the smallest eigenvalue of the 1D RADIAL operator (theta
# averaged) at each E; if the 2D min|eig| equals the 1D radial min|eig| the
# near-null is RADIAL (continuum slide), not a shaped angular type.
log("\nT2b -- 1D radial stiffness smallest |eig| vs 2D min|eig|: if they "
    "MATCH, the near-null mode is the RADIAL round-cell continuum slide "
    "(documented B2b/#33), not a new angular type.")
def radial_min_eig(Ef, Nm=121):
    r = solve2d(Ef, Nm=Nm, Nth=29)
    if not r["conv"]: return None, None, None
    # theta-averaged 1D field; build the 1D radial Jacobian d^2/dm^2 linearized
    v = r["v"]; m = r["m"]; dm = r["dm"]
    vbar = v.mean(axis=1)
    Nm = len(m)
    # linearization of v_mm - Phi(e^{-2v}-e^v) about vbar with Neumann/anchor
    Jr = np.zeros((Nm, Nm))
    for i in range(1, Nm-1):
        Jr[i, i-1] += 1/dm**2
        Jr[i, i]   += -2/dm**2 - (-2*np.exp(-2*vbar[i]) - np.exp(vbar[i]))
        Jr[i, i+1] += 1/dm**2
    Jr[0,0] = 1.0                      # center anchor
    Jr[-1,-1] = 1.0; Jr[-1,-2] = -1.0  # Neumann
    ev = np.linalg.eigvals(Jr)
    return float(np.min(np.abs(ev))), r["nonlin"], r
log(f"{'E/Um':>8} {'nonlin':>10} {'1D radial min|eig|':>20} {'2D min|eig|':>13}")
for Ef in [2.0, 6.0, 50.0, 200.0, 1000.0]:
    rme, nl, r = radial_min_eig(Ef)
    if rme is None:
        log(f"{Ef:8.1f}  no conv"); continue
    me2d, _ = eig_and_vec(r)
    log(f"{Ef:8.1f} {nl:10.2e} {rme:20.6f} {me2d:13.6f}")

log(f"\nPROBE 1b done ({time.time()-t0:.0f}s)")
_fh.close()
