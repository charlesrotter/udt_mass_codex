#!/usr/bin/env python3
"""
sf_scan_anggap.py -- the TRUSTWORTHY angular bifurcation gap across the
STRONG-FIELD family, using the BLIND-VERIFIED wcc_seal_spectrum diagnostic.
=======================================================================
Queue-head step (b)/(c). Driver: Claude (Opus 4.8). 2026-06-13. New file.

PROBE 1 found the raw min|eig| decays at strong field; PROBE 1b/1c found
the near-null mode is ANGULAR and the radial sector STIFFENS (so the soft
mode is not radial). The raw non-symmetric FD min|eig| and my hand-deflated
symmetric gap are BOTH unreliable (BC-row contamination; my D3 gave huge
spurious negatives even in the trust window -- a self-evident artifact).

The TRUSTWORTHY object is wcc_seal_spectrum.gaps(): symmetric part
Js=(J+J^T)/2, eigh (real spectrum), then the smallest |eig| whose
eigenvector is dominantly ANGULAR (theta-varying). This is the
blind-verified (ab035deeb...) diagnostic that established B1/#36's
"angular gap bounded away from zero (min ~0.65)" -- IN THE TRUST WINDOW
(E/Um up to 4). THIS SCRIPT runs the SAME diagnostic at STRONG FIELD
(E/Um up to 1000, nonlin up to 3000), the bulkN (interior) closure,
to answer: does the angular bifurcation gap STAY bounded away from 0
(B1 holds) or does it SOFTEN / go NEGATIVE (undocumented strong-field
angular bifurcation = a shaped type born deep in the core)?

We use the wint (open-interior) machinery -- the same trust-window object
B1 was proven on -- just driven strong-field. Convergence + the
trust-window cross-check at E/Um<=4 (must reproduce the banked ~0.65) are
mandatory before trusting the strong-field numbers. GPU eigh for speed.
"""
import time, json
import numpy as np
from sf_scan_strongfield import solve2d, jac, HAS_GPU, DEV
if HAS_GPU:
    import torch

t0 = time.time()
_fh = open("/tmp/sf_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
FLAG = []

log("\n" + "=" * 72)
log("sf_scan_anggap -- TRUSTWORTHY angular gap across the STRONG-FIELD family")
log("=" * 72)

def gaps(r, n_report=10):
    """wcc_seal_spectrum.gaps adapted to the wint open-interior jac.
    Symmetric part, eigh, smallest |eig| with a dominantly-angular
    eigenvector. Returns global min|eig|, angular min|eig|, and its sign."""
    v = r["v"]; m = r["m"]; th = r["th"]; dm = r["dm"]; dth = r["dth"]
    vlo = r["vlo"]; Nm, Nth = v.shape
    J, _ = jac(v, m, th, dm, dth, 1.0, vlo)
    Jd = J.toarray(); Js = 0.5*(Jd + Jd.T)
    if HAS_GPU:
        T = torch.tensor(Js, dtype=torch.float64, device=DEV)
        evt, evect = torch.linalg.eigh(T)
        ev = evt.cpu().numpy(); evec = evect.cpu().numpy()
    else:
        ev, evec = np.linalg.eigh(Js)
    gmin = float(np.min(np.abs(ev)))
    angmin = np.inf; angmin_signed = np.nan; angmin_frac = 0.0
    # collect a few smallest-|eig| angular modes for reporting
    order = np.argsort(np.abs(ev))
    found = []
    for k in order:
        w = evec[:, k].reshape(Nm, Nth)
        interior = w[1:-1, 1:-1]
        nrm = np.linalg.norm(interior)
        if nrm < 1e-12: continue
        thmean = interior.mean(axis=1, keepdims=True)
        ang_frac = np.linalg.norm(interior - thmean)/nrm
        if ang_frac > 0.5:
            found.append((float(ev[k]), float(ang_frac)))
            if abs(ev[k]) < angmin:
                angmin = abs(ev[k]); angmin_signed = float(ev[k])
                angmin_frac = float(ang_frac)
        if len(found) >= n_report: break
    return dict(gmin=gmin, angmin=float(angmin), angmin_signed=angmin_signed,
                angmin_frac=angmin_frac, found=found[:5])

# ---- trust-window cross-check FIRST (must reproduce the banked behavior) ----
log("\nTRUST-WINDOW CROSS-CHECK (E/Um<=4): the angular gap must be POSITIVE "
    "and bounded away from 0 (B1/#36 banked ~0.65 over the trust E-family).")
log(f"{'E/Um':>6} {'nonlin':>9} {'gmin':>10} {'ang gap':>10} "
    f"{'ang signed':>11} {'ang frac':>9}")
tw_ok = True
for Ef in [1.3, 2.0, 3.0, 4.0]:
    r = solve2d(Ef, Nm=81, Nth=41)
    if not r["conv"]: log(f"{Ef:6.2f} no conv"); tw_ok=False; continue
    g = gaps(r)
    log(f"{Ef:6.2f} {r['nonlin']:9.2e} {g['gmin']:10.5f} {g['angmin']:10.5f} "
        f"{g['angmin_signed']:11.5f} {g['angmin_frac']:9.3f}")
    if not (g['angmin_signed'] > 0):
        tw_ok = False
log(f"  trust-window angular gap positive everywhere: {tw_ok}")

# ---- STRONG FIELD: the same diagnostic, pushed deep ----
log("\nSTRONG FIELD (E/Um up to 1000, nonlin up to 3000): does the angular "
    "gap stay positive/bounded (B1 holds) or soften/flip (new shaped type)?")
log(f"{'E/Um':>8} {'nonlin':>10} {'L':>8} {'gmin':>10} {'ang gap':>10} "
    f"{'ang signed':>12} {'ang frac':>9}")
rows = []
for Ef in [2.0, 4.0, 6.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0]:
    r = solve2d(Ef, Nm=81, Nth=41)
    if not r["conv"]: log(f"{Ef:8.1f} no conv"); continue
    g = gaps(r)
    rows.append(dict(Ef=Ef, nonlin=r["nonlin"], L=r["L"], **{
        k: g[k] for k in ('gmin','angmin','angmin_signed','angmin_frac')}))
    log(f"{Ef:8.1f} {r['nonlin']:10.2e} {r['L']:8.4f} {g['gmin']:10.5f} "
        f"{g['angmin']:10.5f} {g['angmin_signed']:12.5f} {g['angmin_frac']:9.3f}")

# ---- grid-refinement of the angular gap at the strongest field ----
log("\nGRID REFINEMENT of the angular gap at strong field (E/Um=200): is "
    "the gap value grid-converged (real) or grid-limited (artifact)?")
log(f"{'grid':>14} {'ang gap':>10} {'ang signed':>12}")
for (Nm, Nth) in [(61,31),(81,41),(121,51)]:
    r = solve2d(200.0, Nm=Nm, Nth=Nth)
    if not r["conv"]: log(f"  {Nm}x{Nth} no conv"); continue
    g = gaps(r)
    log(f"  {Nm:4d}x{Nth:<4d}   {g['angmin']:10.5f} {g['angmin_signed']:12.5f}")

# VERDICT
log("\nVERDICT (sf_scan_anggap):")
if rows:
    signs = [x['angmin_signed'] for x in rows]
    neg = [x['Ef'] for x in rows if x['angmin_signed'] < -1e-6]
    soft = [x['Ef'] for x in rows if 0 < x['angmin_signed'] < 0.05]
    log(f"  angular gap (signed) across strong field: "
        f"{min(signs):.5f} .. {max(signs):.5f}")
    if neg:
        FLAG.append(("anggap-negative", neg))
        log(f"  *** FLAG: angular gap goes NEGATIVE at E/Um={neg} -- the "
            "angular sector is NO LONGER pure damping at strong field; a "
            "shaped angular mode is unstable/born. CHARACTER CHANGE vs B1.")
    elif soft:
        FLAG.append(("anggap-soft", soft))
        log(f"  angular gap stays POSITIVE but SOFTENS toward 0 at E/Um="
            f"{soft} (strong field). Approaching but not reaching a "
            "bifurcation in the scanned range -- a flagged trend.")
    else:
        log("  angular gap stays POSITIVE and bounded away from 0 across the "
            "WHOLE strong-field family: B1 (pure angular damping, no shaped "
            "type) HOLDS into strong field. Baseline holds on this axis.")
with open("/tmp/sf_anggap.json","w") as fh:
    json.dump(dict(rows=rows, flags=FLAG, tw_ok=tw_ok), fh, indent=0, default=str)
log(f"\nsf_scan_anggap done ({time.time()-t0:.0f}s); FLAGS={FLAG}")
_fh.close()
