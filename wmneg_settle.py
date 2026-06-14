#!/usr/bin/env python3
"""
wmneg_settle.py -- settle the two blind-verifier targets left by exist2:
 (A) at p=-2.75 the fixed-grid th_var=8.5e-2 crossed the round threshold;
     REFINE Nth to confirm it still shrinks ~O(h^2) (artifact, not a lobe).
 (B) the exact-2D-Jacobian min|eig| was DECREASING (0.275->0.0073) with an
     l=1 eigenvector as p deepened. Is it heading to a genuine ZERO (a
     bifurcation = shaped type forming) or is it the RADIAL/boundary mode
     softening because the cell asymptotes? DISCRIMINATE by (i) computing
     min|eig| AT FIXED p under grid refinement (a real near-zero physical
     mode is grid-converged; a boundary-layer/radial mode scales with the
     grid), and (ii) comparing the 2D smallest eigenvalue to the PURELY
     RADIAL (theta-independent) smallest eigenvalue -- if they coincide, the
     softening mode is RADIAL (l=0-character / the energy-anchor direction),
     NOT an angular lobe, even though its 2D eigenvector shows tiny l=1
     numerical leakage.
Driver: Claude (Opus 4.8). 2026-06-13. Built on wmneg_solve2d.py.
Log /tmp/wmneg.log (append).
"""
import time, json
import numpy as np
from wmneg_solve2d import (radial_cell, solve2d, jac_fd, legendre_lobe,
                           R_IN, PHI_AMP)

t0 = time.time()
_fh = open("/tmp/wmneg.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond); (PASS if ok else FAIL).append(tag)
    log(f"WMNEGS-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("\n" + "=" * 74)
log("wmneg_settle -- (A) refine th_var at p=-2.75; (B) is the softening")
log("Jacobian mode radial or angular?")
log("=" * 74)

# ---- (A) refine th_var at the depth that crossed threshold ----
log("\n(A) p=-2.75 th_var under refinement (round seed). O(h^2) shrink to 0")
log("    => the deep th_var is a discretization artifact, NOT a lobe.")
row = []
for (Nr, Nth) in [(161, 65), (241, 97), (321, 129), (481, 193)]:
    r = solve2d(p=-2.75, seed_amp=0.0, Nr=Nr, Nth=Nth)
    if r.get("conv"):
        row.append((Nth, r["th_var"]))
        log(f"    Nr={Nr} Nth={Nth}: th_var={r['th_var']:.4e} "
            f"dom_l={r['dom_l']} maxres={r['maxres']:.1e}")
if len(row) >= 2:
    ratio = row[-1][1] / row[0][1]
    order = np.log(row[0][1] / row[-1][1]) / np.log(row[-1][0] / row[0][0])
    log(f"    -> th_var {row[0][1]:.2e}->{row[-1][1]:.2e}; ratio={ratio:.3f}, "
        f"order~{order:.2f} ({'ARTIFACT (shrinks)' if ratio<0.5 else 'CANDIDATE'})")
    check("A", ratio < 0.5,
          f"p=-2.75 th_var shrinks ~O(h^{order:.1f}) under refinement "
          f"(ratio {ratio:.3f}) => discretization artifact, the cell is "
          f"ROUND at p=-2.75 too; the fixed-grid 'SHAPED?' flag was the "
          f"steep-core discretization residual, not an angular lobe.")

# ---- (B) is the softening 2D Jacobian mode radial or angular? ----
# Build the PURELY RADIAL Jacobian (theta-flat: collapse to 1 angular col)
# and compare its smallest |eig| to the full-2D smallest |eig|. If equal,
# the softening eigenmode lives in the RADIAL sector (the energy-anchor /
# boundary-layer direction), not the angular sector.
log("\n(B) the softening Jacobian mode: RADIAL or ANGULAR? Compare the full-")
log("    2D smallest |eig| to the theta-INDEPENDENT (radial-only) smallest")
log("    |eig| at each p, and refine the 2D min|eig| in the angular grid Nth")
log("    (a physical angular mode is Nth-converged; a radial/boundary mode")
log("    is Nth-INDEPENDENT i.e. identical to the radial-only value).")

def radial_only_min_eig(p, Nr=97):
    """Smallest |eig| of the theta-independent Jacobian (Nth=2 collapse):
    the radial operator with the energy anchor + Neumann/Dirichlet BCs,
    exactly as in the 2D residual but with no angular variation."""
    r = solve2d(p=p, seed_amp=0.0, Nr=Nr, Nth=3)  # minimal theta (flat)
    if not r["conv"]:
        return None
    phi = r["phi"]; rr = r["r"]; th = r["th"]
    dr = rr[1] - rr[0]; dth = th[1] - th[0]
    J, _ = jac_fd(phi, rr, th, dr, dth, PHI_AMP, p)
    w = np.linalg.eigvals(J.toarray())
    return float(np.min(np.abs(w)))

def twod_min_eig(p, Nr=97, Nth=49):
    r = solve2d(p=p, seed_amp=0.0, Nr=Nr, Nth=Nth)
    if not r["conv"]:
        return None
    phi = r["phi"]; rr = r["r"]; th = r["th"]
    dr = rr[1] - rr[0]; dth = th[1] - th[0]
    J, _ = jac_fd(phi, rr, th, dr, dth, PHI_AMP, p)
    w = np.linalg.eigvals(J.toarray())
    return float(np.min(np.abs(w)))

log(f"{'p':>8} {'2D_Nth49':>12} {'2D_Nth97':>12} {'radial_only':>12} "
    f"{'verdict':>10}")
BB = []
for p in [-0.80, -1.50, -2.00, -2.50]:
    e2a = twod_min_eig(p, Nr=97, Nth=49)
    e2b = twod_min_eig(p, Nr=97, Nth=97)
    er = radial_only_min_eig(p, Nr=97)
    # if the 2D min|eig| is ~ Nth-independent AND ~ the radial-only value,
    # the softening mode is RADIAL.
    radial = (e2a and e2b and er and abs(e2a - e2b) < 0.05 * e2a
              and abs(e2a - er) < 0.1 * e2a)
    BB.append(dict(p=p, e2_49=e2a, e2_97=e2b, eradial=er, radial=bool(radial)))
    log(f"{p:8.2f} {e2a:12.5e} {e2b:12.5e} {er:12.5e} "
        f"{'RADIAL' if radial else 'check':>10}")
json.dump(BB, open("/tmp/wmneg_settle.json", "w"))
allrad = all(b["radial"] for b in BB)
check("B", allrad,
      "the softening smallest Jacobian eigenvalue is Nth-INDEPENDENT and "
      "equals the radial-only value at every depth => the mode that softens "
      "as p deepens is the RADIAL/energy-anchor direction (the cell "
      "asymptoting: rstar->const), NOT an angular lobe. The angular sector "
      "has NO softening mode; min|eig| -> small is the radial cell closing, "
      "not a shaped type forming. CONFIRMS one round type."
      if allrad else
      "the 2D smallest eig differs from radial-only or moves with Nth at "
      "some depth -> the softening mode has genuine angular content; "
      "INVESTIGATE a possible forming lobe.")

log(f"\nWMNEG settle: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
if FAIL: log("FAILED: " + str(FAIL))
_fh.close()
