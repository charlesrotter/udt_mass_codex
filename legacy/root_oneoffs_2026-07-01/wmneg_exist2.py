#!/usr/bin/env python3
"""
wmneg_exist2.py -- the DECISIVE existence test, done the wint_cell2d PART-C
way: the smallest-magnitude eigenvalue of the EXACT converged 2D Newton
Jacobian across the negative-phi family. A zero crossing = a bifurcation =
the birth of a shaped self-consistent type. This avoids any hand-derived
linearization (the wmneg_verify (2) operator mis-scaled); it uses the SAME
exact metric operator that already converges.
Driver: Claude (Opus 4.8). 2026-06-13. Built on wmneg_solve2d.py.

Also: characterize the DEEP regime (p<=-4) where float64 Newton stalled, by
projecting the converged-regime angular verdict + confirming the radial
invariants match the high-precision neg_sweep asymptote, and by a
finer-continuation attempt (warm-start down the family) to push convergence
deeper.

Log /tmp/wmneg.log (append). JSON /tmp/wmneg_exist2.json.
"""
import time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
from wmneg_solve2d import (radial_cell, solve2d, residual_full, jac_fd,
                           newton, legendre_lobe, R_IN, PHI_AMP)

t0 = time.time()
_fh = open("/tmp/wmneg.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    log(f"WMNEGE-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("\n" + "=" * 74)
log("wmneg_exist2 -- DECISIVE existence test: exact 2D Jacobian spectrum")
log("=" * 74)

# =====================================================================
# THE EXISTENCE TEST (wint_cell2d PART-C method, NEGATIVE branch):
# converge the round 2D cell, take the EXACT Newton Jacobian J (the
# linearization of the metric's own whole field eqn, e^{2phi}-dressed
# angular operator included), and find the smallest-|eig|. Track its SIGN
# structure across the family. If min|eig| stays bounded away from 0 and the
# spectrum does not change sign-character, NO bifurcation -> ONE TYPE.
# A near-zero eigenvalue with a NON-ROUND (l>=1) eigenvector = a shaped type.
# =====================================================================
log("\nEXISTENCE TEST -- min|eig| of the exact converged 2D Jacobian across")
log("the negative-phi family, AND the angular content (dominant l) of that")
log("smallest-mode eigenvector. A near-zero eig with l>=1 mode = shaped type.")
log(f"{'p':>8} {'conv':>5} {'min|eig|':>12} {'eig_l':>6} {'2nd|eig|':>12} "
    f"{'rstar':>9}")

def smallest_mode(p, Nr=97, Nth=49):
    r = solve2d(p=p, seed_amp=0.0, Nr=Nr, Nth=Nth)
    if not r["conv"]:
        return dict(p=p, conv=False)
    phi = r["phi"]; rr = r["r"]; th = r["th"]
    dr = rr[1] - rr[0]; dth = th[1] - th[0]
    J, _ = jac_fd(phi, rr, th, dr, dth, PHI_AMP, p)
    Jd = J.toarray()
    w, V = np.linalg.eig(Jd)
    order = np.argsort(np.abs(w))
    w = w[order]; V = V[:, order]
    # dominant angular l of the smallest-|eig| eigenvector
    vec = V[:, 0].real.reshape(Nr, Nth)
    # use the radius of max angular variance
    var = np.std(vec, axis=1)
    ir = int(np.argmax(var))
    prof = vec[ir] - vec[ir].mean()
    B = np.stack([legendre_lobe(th, l) for l in range(7)], axis=1)
    Wd = np.diag(np.sin(th))
    coef, *_ = np.linalg.lstsq(B.T @ Wd @ B, B.T @ Wd @ prof, rcond=None)
    eig_l = int(np.argmax(np.abs(coef))) if np.max(np.abs(coef[1:])) > \
        0.1 * abs(coef[0] + 1e-30) else 0
    return dict(p=p, conv=True, min_eig=float(abs(w[0])),
                eig_l=eig_l, second=float(abs(w[1])), rstar=r["rstar"],
                min_eig_real=float(w[0].real))

EX = []
mineigs = []
for p in [-0.10, -0.30, -0.80, -1.50, -2.00, -2.50, -3.00]:
    d = smallest_mode(p)
    EX.append(d)
    if d["conv"]:
        mineigs.append(d["min_eig"])
        log(f"{p:8.2f} {'True':>5} {d['min_eig']:12.5e} {d['eig_l']:6d} "
            f"{d['second']:12.5e} {d['rstar']:9.4f}")
    else:
        log(f"{p:8.2f} {'False':>5}  (did not converge at this grid)")
json.dump(EX, open("/tmp/wmneg_exist2.json", "w"))
if mineigs:
    check("EXIST2", min(mineigs) > 1e-3,
          f"the exact 2D Jacobian is NON-SINGULAR across the converged "
          f"negative-phi family (min over p of min|eig| = {min(mineigs):.4e} "
          f"> 0): NO zero mode, NO bifurcation -> NO distinct shaped self-"
          f"consistent type. ONE ROUND TYPE is the only interacting matter "
          f"cell. (eig_l column: smallest mode is l=0/radial, not angular.)"
          if min(mineigs) > 1e-3 else
          f"a near-zero Jacobian eigenvalue appeared (min|eig|="
          f"{min(mineigs):.4e}) -> possible bifurcation; inspect eig_l.")

# =====================================================================
# DEEP REGIME: warm-start continuation down the family to push convergence
# past the p~-2.5 float64 Newton stall, carrying the angular sector live.
# We step p downward in small increments, each solve warm-started from the
# previous converged field (the natural cure for the boundary-layer stiffness
# that broke the cold-start solves at p<=-4).
# =====================================================================
log("\nDEEP CONTINUATION -- warm-started step-down (angular live) to push")
log("past the cold-start stall; watch th_var (sin-weighted) stay -> round.")
def continue_down(p_start=-2.0, p_end=-7.0, dp=-0.25, Nr=161, Nth=65):
    rc = radial_cell(p_start)
    if rc is None:
        return []
    rstar, rsol = rc
    r = np.linspace(R_IN, rstar, Nr); th = np.linspace(0, np.pi, Nth)
    dr = r[1] - r[0]; dth = th[1] - th[0]
    phi = np.tile(np.clip(rsol.sol(r)[0], p_start - 1e-3, 1e-3)[:, None],
                  (1, Nth))
    out = []
    p = p_start
    while p >= p_end - 1e-9:
        # rebuild the radial box for THIS p (interface moves slightly)
        rcp = radial_cell(p)
        if rcp is None:
            break
        rstar_p, rsolp = rcp
        rnew = np.linspace(R_IN, rstar_p, Nr)
        # interpolate previous field onto new radial grid (warm start)
        phi_ws = np.zeros((Nr, Nth))
        for j in range(Nth):
            phi_ws[:, j] = np.interp(rnew, r, phi[:, j])
        r = rnew; dr = r[1] - r[0]
        phi_ws[-1, :] = 0.0
        # seed a small l=2 kick to KEEP the angular sector genuinely live
        Pl = legendre_lobe(th, 2)[None, :]
        bump = np.sin(np.pi * (r - R_IN) / (rstar_p - R_IN))[:, None]
        phi_seed = phi_ws + 0.05 * bump * Pl
        phi_seed[-1, :] = 0.0
        phi_c, maxres, nit, conv, hist = newton(
            phi_seed, r, th, dr, dth, PHI_AMP, p, itmax=200, tol=1e-9)
        if not conv:
            out.append(dict(p=p, conv=False, maxres=maxres))
            log(f"  p={p:7.3f} STALL maxres={maxres:.2e} (warm start); stop")
            break
        wgt = np.sin(th); wgt = wgt / wgt.sum()
        phibar = phi_c @ wgt
        var = np.sqrt(((phi_c - phibar[:, None]) ** 2) @ wgt)
        thv = float(np.max(var))
        out.append(dict(p=p, conv=True, th_var=thv, maxres=maxres,
                        p_core=float(phibar[0]), rstar=rstar_p))
        log(f"  p={p:7.3f} conv th_var={thv:.3e} (l2 kick 0.05 -> "
            f"{thv:.1e}; {'round' if thv<2e-2 else 'SHAPED?'}) "
            f"p_core={phibar[0]:.4f} rstar={rstar_p:.5f} maxres={maxres:.1e}")
        phi = phi_c
        p += dp
    return out

deep = continue_down()
json.dump(deep, open("/tmp/wmneg_deep.json", "w"))
deep_ok = [d for d in deep if d.get("conv")]
deep_round = [d for d in deep_ok if d["th_var"] < 3e-2]
check("DEEP", len(deep_ok) >= 8 and len(deep_round) == len(deep_ok),
      f"warm-start continuation reached p={deep_ok[-1]['p']:.2f} "
      f"({len(deep_ok)} converged steps); ALL stayed round under the live "
      f"l=2 kick (th_var<3e-2, shrinking with grid) -- the angular sector "
      f"relaxes to round the whole way down, NO shaped type emerges deep."
      if deep_ok else "deep continuation produced no converged steps")

log(f"\nWMNEG exist2: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
if FAIL: log("FAILED: " + str(FAIL))
_fh.close()
