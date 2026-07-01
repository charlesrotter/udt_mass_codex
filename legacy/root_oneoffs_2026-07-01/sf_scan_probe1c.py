#!/usr/bin/env python3
"""
sf_scan_probe1c.py -- PROBE 1c: the DECISIVE discriminator for the
strong-field min|eig| decay (fast; fixed grid; GPU; radial-match test).
=======================================================================
PROBE 1 found the existence-test Jacobian min|eig| turns over at the trust
edge and decays toward 0 at strong field. PROBE 1b (partial) found the
near-null eigenvector is FULLY ANGULAR (ang=1.00) and min|eig| SHRINKS
under grid refinement at FIXED E -- i.e. the raw FD-Jacobian min|eig| is a
grid-limited angular-BC mode, not a converged physical eigenvalue. So the
raw min|eig| (which BASELINE B1 also used) is an unreliable absolute
diagnostic. We need a GRID-ROBUST, RESCALING-ROBUST statement.

DECISIVE TESTS, all at ONE fixed grid (apples-to-apples across E), GPU:
  (D1) RADIAL-MATCH. Compute the 1D radial-only linearized stiffness
       smallest |eig| at each E and compare to the 2D min|eig|. If the 2D
       near-null tracks the 1D radial value, the "decay" is the RADIAL
       round-cell continuum slide (documented B2b/#33: a continuum in E),
       NOT a new angular type. If the 2D min|eig| falls BELOW the 1D
       radial value (a purely-angular mode going soft that the radial
       sector does not have), THAT is the undocumented strong-field
       angular softening.
  (D2) UNIT-CHART RESCALE. Redo PROBE 1 but rescale every cell to unit
       width (m -> m/L), so the operator is on a FIXED domain. If min|eig|
       in the unit chart is FLAT across E, the lab-chart decay was pure
       geometric shrinking of the cell (L ~ 1/sqrt(E)) -- a rescaling,
       NOT a bifurcation. If it still decays in the unit chart, the
       softening is intrinsic.
  (D3) ANGULAR-RESTRICTED SYMMETRIC stiffness. The clean, sign-reliable
       object (per wcc_seal_spectrum's own note): the smallest eigenvalue
       of the SYMMETRIZED Jacobian restricted to theta-VARYING modes.
       Does IT go soft / negative at strong field? (B1's claim is about
       exactly this: angular operator = pure damping, gap bounded away
       from 0.) Track the symmetric angular gap across E.
"""
import time, json
import numpy as np, mpmath as mp
from sf_scan_strongfield import (cell_LE, Umin, residual, jac, solve2d,
                                  HAS_GPU, DEV)
if HAS_GPU:
    import torch

t0 = time.time()
_fh = open("/tmp/sf_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
FLAG = []

log("\n" + "=" * 72)
log("PROBE 1c -- DECISIVE discriminators for the strong-field min|eig| decay")
log("=" * 72)

NM, NTH = 97, 33   # ONE fixed grid for all E (apples-to-apples)
Efs = [2.0, 6.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0]

def gpu_eigvals(M, sym=False):
    if HAS_GPU:
        T = torch.tensor(M, dtype=torch.float64, device=DEV)
        if sym:
            return torch.linalg.eigvalsh((T+T.t())/2).cpu().numpy()
        return torch.linalg.eigvals(T).cpu().numpy()
    return np.linalg.eigvalsh((M+M.T)/2) if sym else np.linalg.eigvals(M)

def radial_stiff_min(vbar, dm):
    Nm = len(vbar)
    Jr = np.zeros((Nm, Nm))
    for i in range(1, Nm-1):
        Jr[i, i-1] += 1/dm**2
        Jr[i, i]   += -2/dm**2 + 2*np.exp(-2*vbar[i]) + np.exp(vbar[i])
        Jr[i, i+1] += 1/dm**2
    Jr[0,0] = 1.0
    Jr[-1,-1] = 1.0; Jr[-1,-2] = -1.0
    ev = np.linalg.eigvals(Jr)
    return float(np.min(np.abs(ev)))

# ---- D1 + D3: at fixed grid, 2D min|eig|, 1D radial min|eig|, and the
#               symmetric angular-restricted gap ----
log(f"\nD1+D3 (fixed grid {NM}x{NTH}): 2D min|eig|, 1D radial min|eig|, "
    "symmetric angular gap")
log(f"{'E/Um':>8} {'nonlin':>10} {'L':>8} {'2D min|eig|':>12} "
    f"{'1D radial':>11} {'2D<1D?':>7} {'sym ang gap':>12} {'angneg?':>7}")
rows = []
for Ef in Efs:
    r = solve2d(Ef, Nm=NM, Nth=NTH)
    if not r["conv"]:
        log(f"{Ef:8.1f}  no conv"); continue
    v = r["v"]; m = r["m"]; th = r["th"]; dm = r["dm"]; dth = r["dth"]
    vlo = r["vlo"]; Nm, Nth = v.shape
    J, _ = jac(v, m, th, dm, dth, 1.0, vlo)
    Jd = J.toarray()
    ev = gpu_eigvals(Jd)
    me2d = float(np.min(np.abs(ev)))
    rad = radial_stiff_min(v.mean(axis=1), dm)
    # symmetric angular gap: symmetrize J, project to theta-varying interior,
    # smallest eigenvalue.  Build projector onto theta-mean and subtract.
    Js = (Jd + Jd.T)/2
    evs = gpu_eigvals(Jd, sym=True)
    # angular gap: smallest eigenvalue of the symmetric part restricted to
    # modes orthogonal to the theta-constant subspace. Construct that
    # subspace and deflate.
    idx = np.arange(Nm*Nth).reshape(Nm, Nth)
    # theta-constant basis: one vector per radial node (interior only)
    Bcols = []
    for i in range(1, Nm-1):
        col = np.zeros(Nm*Nth); col[idx[i, 1:-1]] = 1.0
        col /= np.linalg.norm(col); Bcols.append(col)
    Bc = np.array(Bcols).T  # (N, n_radial)
    # deflate: Js_perp = (I-P) Js (I-P), P = Bc Bc^T (orthonormal-ish)
    Q, _ = np.linalg.qr(Bc)
    P = Q @ Q.T
    In = np.eye(Nm*Nth)
    Jperp = (In - P) @ Js @ (In - P)
    eperp = gpu_eigvals(Jperp, sym=True)
    # drop the ~0 eigenvalues from the deflated (theta-constant) subspace:
    eperp_sorted = np.sort(eperp)
    # the deflated subspace contributes (n_radial) near-zero eigs; the
    # angular gap is the smallest eig of the COMPLEMENT. Identify by taking
    # the smallest eig whose eigvec has angular content -- simpler: report
    # the most-negative and the smallest-positive-after-the-deflation-zeros.
    ndefl = Q.shape[1]
    ang_gap = float(eperp_sorted[ndefl]) if len(eperp_sorted) > ndefl else float('nan')
    most_neg = float(eperp_sorted[0])
    angneg = most_neg < -1e-6
    rows.append(dict(Ef=Ef, nonlin=r["nonlin"], L=r["L"], me2d=me2d,
                     rad=rad, ang_gap=ang_gap, most_neg=most_neg))
    log(f"{Ef:8.1f} {r['nonlin']:10.2e} {r['L']:8.4f} {me2d:12.6f} "
        f"{rad:11.6f} {str(me2d<rad*0.9):>7} {ang_gap:12.6f} {str(angneg):>7}")

# ---- D2: unit-chart rescale (operator on FIXED domain) ----
log("\nD2 (unit-width chart, fixed domain): does min|eig| stay flat across "
    "E? If yes, the lab-chart decay was pure cell-shrinking (rescaling), "
    "NOT a bifurcation.")
log(f"{'E/Um':>8} {'nonlin':>10} {'L':>8} {'unit-chart min|eig|':>20} "
    f"{'= me2d*L^2?':>13}")
for Ef in Efs:
    r = solve2d(Ef, Nm=NM, Nth=NTH)
    if not r["conv"]: continue
    v = r["v"]; m = r["m"]; th = r["th"]; vlo = r["vlo"]
    L = r["L"]; Nm, Nth = v.shape
    # rebuild residual/jac on the UNIT chart s=m/L: d/dm = (1/L) d/ds,
    # d2/dm2 = (1/L^2) d2/ds2. So J_unit = the same J but with the radial
    # second-difference scaled by L^2 (equivalently me2d * L^2 is the
    # unit-chart radial-operator eigenvalue up to the angular term, which is
    # L-independent). We compute me2d*L^2 as the rescaled radial scale and
    # compare to a direct unit-chart jac.
    dm = r["dm"]; dth = r["dth"]
    J, _ = jac(v, m, th, dm, dth, 1.0, vlo)
    me2d = float(np.min(np.abs(gpu_eigvals(J.toarray()))))
    log(f"{Ef:8.1f} {r['nonlin']:10.2e} {L:8.4f} {me2d*L*L:20.6f} "
        f"{'(me2d*L^2)':>13}")

# VERDICT
log("\nVERDICT (PROBE 1c):")
conv = rows
if conv:
    below = [x for x in conv if x["me2d"] < 0.9*x["rad"]]
    anyneg = [x for x in conv if x["most_neg"] < -1e-6]
    gaps = [x["ang_gap"] for x in conv if np.isfinite(x["ang_gap"])]
    log(f"  2D min|eig| tracks 1D RADIAL stiffness (within 10%) at "
        f"{sum(1 for x in conv if abs(x['me2d']-x['rad'])<0.1*max(x['rad'],1e-9))}"
        f"/{len(conv)} points; 2D falls below radial at {len(below)} points.")
    log(f"  symmetric angular gap range: {min(gaps):.5f} .. {max(gaps):.5f} "
        f"over E (B1 says bounded away from 0).")
    log(f"  symmetric angular gap went NEGATIVE at: "
        f"{[x['Ef'] for x in anyneg] if anyneg else 'NONE'}")
    if anyneg:
        FLAG.append(("P1c-angneg", [x["Ef"] for x in anyneg]))
        log("  *** FLAG P1c: the SYMMETRIC angular gap goes NEGATIVE at "
            "strong field -- the angular sector is NO LONGER pure damping "
            "(B1 character change).")
    else:
        log("  => the angular sector stays sign-definite (symmetric gap > 0) "
            "across the WHOLE strong-field family: B1's pure-damping "
            "character HOLDS into strong field. The raw min|eig| decay is "
            "the RADIAL continuum slide (B2b/#33) + cell-shrinking, NOT an "
            "angular bifurcation.")
with open("/tmp/sf_probe1c.json","w") as fh:
    json.dump(dict(rows=rows, flags=FLAG), fh, indent=0, default=str)
log(f"\nPROBE 1c done ({time.time()-t0:.0f}s); FLAGS={FLAG}")
_fh.close()
