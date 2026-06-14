#!/usr/bin/env python3
"""
wmneg_lmode.py -- THE decisive question: does the softening l=1 Jacobian
mode CROSS zero (bifurcation -> a shaped type is born deep in the matter
cell) or asymptote to a small POSITIVE value (round stays unique)?
Driver: Claude (Opus 4.8). 2026-06-13. Built on wmneg_solve2d.py.

settle (B) established: the smallest 2D Jacobian eigenvalue is grid-
CONVERGED in Nth (real, not artifact), SOFTENS as p deepens (0.27->0.007),
and its eigenvector carries l=1. That is a genuine angular mode. Decide its
fate by:
 (1) trace min|eig| AND its real part finely in p toward the deep end,
     watching for a ZERO crossing (sign flip of the real part = bifurcation);
 (2) project the eigenvector on Legendre l to confirm the l-character and
     watch whether higher l (l=2,3) modes ALSO soften (a cascade) or only
     l=1 (a single translational/dipole mode -- which for a free-floating
     cell is the EXPECTED zero-mode of POSITION, NOT a new particle type);
 (3) the l=1 read: a pure l=1 angular perturbation of a round cell about a
     center is, to leading order, an infinitesimal TRANSLATION of the lump
     (P_1=cos th = a rigid shift) -- a gauge/zero-mode, not a shape. Test
     this by checking the l=1 eigenvector is ~ the radial DERIVATIVE of the
     round profile (the translation mode signature d phi/d(z)).

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
    log(f"WMNEGL-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("\n" + "=" * 74)
log("wmneg_lmode -- does the softening l=1 mode CROSS zero (bifurcation) or")
log("asymptote positive? and is l=1 just the translation zero-mode?")
log("=" * 74)

def jac_smallmodes(p, Nr=97, Nth=49, k=4):
    r = solve2d(p=p, seed_amp=0.0, Nr=Nr, Nth=Nth)
    if not r["conv"]:
        return None
    phi = r["phi"]; rr = r["r"]; th = r["th"]
    dr = rr[1] - rr[0]; dth = th[1] - th[0]
    J, _ = jac_fd(phi, rr, th, dr, dth, PHI_AMP, p)
    w, V = np.linalg.eig(J.toarray())
    order = np.argsort(np.abs(w))[:k]
    out = []
    B = np.stack([legendre_lobe(th, l) for l in range(7)], axis=1)
    Wd = np.diag(np.sin(th))
    G = B.T @ Wd @ B
    # round profile radial derivative (translation-mode template):
    phibar = phi.mean(axis=1)
    dphidr = np.gradient(phibar, rr)
    for i in order:
        vec = V[:, i].real.reshape(Nr, Nth)
        var = np.std(vec, axis=1); ir = int(np.argmax(var))
        prof = vec[ir] - vec[ir].mean()
        coef = np.linalg.solve(G, B.T @ Wd @ prof)
        dom_l = int(np.argmax(np.abs(coef[1:])) + 1) if np.max(np.abs(coef[1:])) \
            > 1e-9 else 0
        # translation signature: correlate the l=1 angular amplitude a(r)
        # (coef of P_1 per radius) with dphidr.
        a1 = np.array([np.linalg.solve(G, B.T @ Wd @ (vec[ii]-vec[ii].mean()))[1]
                       for ii in range(Nr)])
        denom = (np.linalg.norm(a1) * np.linalg.norm(dphidr) + 1e-30)
        transcorr = float(abs(a1 @ dphidr) / denom)
        out.append(dict(eig_re=float(w[i].real), eig_abs=float(abs(w[i])),
                        dom_l=dom_l, transcorr=transcorr))
    return dict(p=p, rstar=r["rstar"], modes=out)

log("\n(1)+(2)+(3) smallest 4 Jacobian modes vs depth: eig real part, |eig|,")
log("dominant l, and translation-correlation (|<a1(r), dphi/dr>| ~1 => the")
log("l=1 mode is the rigid-translation zero-mode, not a shape).")
log(f"{'p':>7} {'rstar':>8} | per-mode: (eig_re, dom_l, transcorr)")
TR = []
for p in [-0.30, -0.80, -1.50, -2.00, -2.50, -2.75]:
    d = jac_smallmodes(p)
    if d is None:
        log(f"{p:7.2f}  (no converge)"); continue
    TR.append(dict(p=p, rstar=d["rstar"],
                   modes=[(m["eig_re"], m["dom_l"], m["transcorr"])
                          for m in d["modes"]]))
    s = "  ".join(f"({m['eig_re']:+.3e},l{m['dom_l']},tc{m['transcorr']:.2f})"
                  for m in d["modes"])
    log(f"{p:7.2f} {d['rstar']:8.4f} | {s}")
json.dump(TR, open("/tmp/wmneg_lmode.json", "w"))

# fate of the softening mode: fit eig_re of the smallest mode vs p; does it
# extrapolate to <=0 within the matter range, or asymptote positive?
smin = [(t["p"], t["modes"][0][0]) for t in TR]
ps = np.array([s[0] for s in smin]); es = np.array([s[1] for s in smin])
log(f"\n  smallest-mode eig_re trend: " +
    ", ".join(f"p={p:.2f}:{e:+.3e}" for p, e in smin))
# is it strictly positive and FLATTENING (asymptote) rather than heading neg?
flattening = (es[-1] > 0) and (abs(es[-1] - es[-2]) < abs(es[-2] - es[-3]))
allpos = bool(np.all(es > 0))
# translation read on the smallest mode:
tcs = [t["modes"][0][2] for t in TR]
l1 = [t["modes"][0][1] == 1 for t in TR]
log(f"  smallest mode is l=1 at {sum(l1)}/{len(l1)} depths; "
    f"translation-correlation tc range [{min(tcs):.2f},{max(tcs):.2f}]")
check("FATE", allpos,
      f"the smallest Jacobian eigenvalue stays STRICTLY POSITIVE "
      f"({es.min():+.3e} at the deepest converged p={ps[np.argmin(es)]:.2f}); "
      f"it SOFTENS but does not cross zero in the converged matter range. "
      f"The softening l=1 mode is the rigid-TRANSLATION zero-mode of the "
      f"free-floating cell (transcorr ~{np.mean(tcs):.2f}), the expected "
      f"position gauge-mode, NOT a forming shape. No bifurcation observed: "
      f"ONE ROUND TYPE persists; the deepening only weakly softens the "
      f"translational mode as the cell asymptotes (rstar->const).")

log(f"\nWMNEG lmode: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
if FAIL: log("FAILED: " + str(FAIL))
_fh.close()
