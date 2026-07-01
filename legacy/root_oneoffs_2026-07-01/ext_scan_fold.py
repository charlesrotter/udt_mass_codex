#!/usr/bin/env python3
"""
ext_scan_fold.py -- THE EXTERIOR EXISTENCE FOLD (clean, fast, robust)
=====================================================================
Driver: Claude (Opus 4.8, 1M). 2026-06-13. Frame CRITICAL_UNIVERSE_FRAME.
Reuses the metric's OWN operators (Box_g, ON source S=Phi(e^{-2phi}-e^{phi}))
verbatim. Adds nothing. New file (ext_scan_* only). Pure CPU scipy
(the decisive result is a 1-parameter existence boundary; no eigensolve).

THE FINDING TO NAIL (flagged by ext_scan_whole PART A + ext_scan_verify Q1):
On the f>1 EXTERIOR (phi<0) the ON matter source is large POSITIVE
(e^{-2phi} dominates), and the static whole-metric equation Box_g phi=S(phi)
admits a smooth static medium ONLY BELOW a CRITICAL SOURCE STRENGTH Phi_c.
Above Phi_c no smooth static solution exists (a Gelfand-Bratu-type fold).
ext_scan_verify Q1 showed: at (Din=0,Dout=-0.5) Phi=0.1 EXISTS (Newton AND
Phi-continuation converge), Phi=0.3 does NOT (Phi-continuation fails even
ramping gently from the Phi=0.1 solution => the branch ends, not a bad
guess). This script:
  (1) maps Phi_c by Phi-continuation (the robust homotopy) on the EXTERIOR
      for several media (Din,Dout), bisecting the last-converged / first-
      failed Phi to locate the fold;
  (2) CONTROLS with the INTERIOR (phi>0) using BOTH boundary closures
      (Dirichlet-Dirichlet AND the native inner-Neumann trust window) to
      scope whether the fold is an exterior-specific phenomenon or a
      general source-strength fold present on both sides;
  (3) checks grid-convergence of Phi_c (real vs discretization artifact).

Honest self-grade in the log. Log /tmp/ext_scan_fold.log.
"""
import time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla

t0 = time.time()
_fh = open("/tmp/ext_scan_fold.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True)
    _fh.write(s+"\n"); _fh.flush()
log("="*72); log("ext_scan_fold -- exterior ON-source existence fold Phi_c")
log("="*72)

def box_np(phi, r, th, dr, dth):
    w = np.exp(-2.0*phi); R = r[:, None]; sinth = np.sin(th)[None, :]
    a_r = (R**2)*w; am_r = 0.5*(a_r[1:, :]+a_r[:-1, :])
    flux_r = am_r*(phi[1:, :]-phi[:-1, :])/dr
    div_r = np.zeros_like(phi)
    div_r[1:-1, :] = (flux_r[1:, :]-flux_r[:-1, :])/dr/(R[1:-1]**2)
    a_th = sinth*w; am_th = 0.5*(a_th[:, 1:]+a_th[:, :-1])
    flux_th = am_th*(phi[:, 1:]-phi[:, :-1])/dth
    div_th = np.zeros_like(phi)
    div_th[:, 1:-1] = (flux_th[:, 1:]-flux_th[:, :-1])/dth/(R**2*sinth)[:, 1:-1]
    return div_r+div_th

def src(phi, Phi): return Phi*(np.exp(-2*phi)-np.exp(phi))

def resid(phi, r, th, dr, dth, Din, Dout, Phi, inner='dir'):
    F = box_np(phi, r, th, dr, dth) - src(phi, Phi)
    if inner == 'dir': F[0, :] = phi[0, :]-Din
    else:              F[0, :] = phi[0, :]-phi[1, :]
    F[-1, :] = phi[-1, :]-Dout
    F[:, 0]  = phi[:, 0]-phi[:, 1]
    F[:, -1] = phi[:, -1]-phi[:, -2]
    return F

def jac(phi, r, th, dr, dth, Din, Dout, Phi, inner='dir', eps=1e-7):
    Nr, Nth = phi.shape; N = Nr*Nth
    F0 = resid(phi, r, th, dr, dth, Din, Dout, Phi, inner).ravel()
    idx = np.arange(N).reshape(Nr, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nr, Nth), bool); mask[ci::3, cj::3] = True
            ph = phi.copy(); ph[mask] += eps
            dF = ((resid(ph, r, th, dr, dth, Din, Dout, Phi, inner).ravel()-F0)
                  /eps).reshape(Nr, Nth)
            owner = np.full((Nr, Nth), -1, np.int64)
            for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                si = np.clip(np.arange(Nr)[:, None]+di, 0, Nr-1)
                sj = np.clip(np.arange(Nth)[None, :]+dj, 0, Nth-1)
                valid = ((np.arange(Nr)[:, None]+di >= 0) &
                         (np.arange(Nr)[:, None]+di < Nr) &
                         (np.arange(Nth)[None, :]+dj >= 0) &
                         (np.arange(Nth)[None, :]+dj < Nth))
                inc = valid & mask[si, sj] & (owner < 0)
                owner[inc] = idx[si, sj][inc]
            sel = owner >= 0; vv = dF[sel]; nz = vv != 0.0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz]); vals.append(vv[nz])
    return sps.csr_matrix((np.concatenate(vals),
                          (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)), F0

def newton(phi0, r, th, dr, dth, Din, Dout, Phi, inner='dir',
           itmax=120, tol=1e-10):
    phi = phi0.copy()
    for nit in range(itmax):
        J, F0 = jac(phi, r, th, dr, dth, Din, Dout, Phi, inner)
        try: dphi = spsla.spsolve(J, -F0).reshape(phi.shape)
        except Exception: return phi, np.inf, False
        if not np.all(np.isfinite(dphi)): return phi, np.inf, False
        nF0 = np.linalg.norm(F0); lam = 1.0; ok = False
        for _ in range(50):
            tr = phi+lam*dphi
            if np.all(np.abs(tr) < 60):
                Ft = resid(tr, r, th, dr, dth, Din, Dout, Phi, inner)
                if np.isfinite(Ft).all() and np.linalg.norm(Ft) < (1-1e-4*lam)*nF0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            mr = float(np.max(np.abs(resid(phi, r, th, dr, dth, Din, Dout, Phi, inner)[2:-2, 2:-2])))
            return phi, mr, mr < 1e-9
        phi = tr
        mr = float(np.max(np.abs(resid(phi, r, th, dr, dth, Din, Dout, Phi, inner)[2:-2, 2:-2])))
        if mr < tol: return phi, mr, True
    return phi, mr, mr < 1e-9

def grid(Nr, Nth, r_in=1.0, r_star=6.0):
    r = np.linspace(r_in, r_star, Nr); th = np.linspace(0, np.pi, Nth)
    return r, th, r[1]-r[0], th[1]-th[0]

def phi_c(Din, Dout, inner='dir', Nr=161, Nth=81, Phi_hi=4.0, nstep=40):
    """Find the critical source strength by PHI-CONTINUATION: ramp Phi up
    in small steps, warm-starting each Newton from the previous converged
    phi; the last Phi that converges brackets Phi_c; bisect to refine."""
    r, th, dr, dth = grid(Nr, Nth)
    phi = np.tile(np.linspace(Din, Dout, Nr)[:, None], (1, Nth))
    phi, mr, cv = newton(phi, r, th, dr, dth, Din, Dout, 0.0, inner)
    if not cv: return None, None, "Phi=0 base failed"
    last_ok = 0.0; last_phi = phi.copy()
    Phis = np.linspace(0.0, Phi_hi, nstep+1)[1:]
    first_fail = None
    for P in Phis:
        ph2, mr, cv = newton(last_phi.copy(), r, th, dr, dth, Din, Dout, float(P), inner)
        if cv:
            last_ok = float(P); last_phi = ph2
        else:
            first_fail = float(P); break
    if first_fail is None:
        return last_ok, None, f"no fold up to Phi={Phi_hi} (exists throughout)"
    # bisect between last_ok and first_fail, warm-starting from last_phi
    lo, hi = last_ok, first_fail
    for _ in range(18):
        mid = 0.5*(lo+hi)
        ph2, mr, cv = newton(last_phi.copy(), r, th, dr, dth, Din, Dout, mid, inner)
        if cv: lo = mid; last_phi = ph2
        else:  hi = mid
    # invariants at the last converged point
    wth = np.sin(th); wth = wth/wth.sum(); pb = last_phi @ wth
    return lo, dict(Phi_c=lo, bracket=[last_ok, first_fail],
                    phibar_min=float(pb.min()), phibar_max=float(pb.max())), "fold"

log("\nPART 1 -- EXTERIOR (f>1) ON-source existence fold Phi_c, by Din,Dout")
log(f"  {'Din':>5} {'Dout':>6} {'inner':>5} {'Phi_c':>9} {'bracket':>20} {'note'}")
EXT = []
for (Din, Dout) in [(0.0, -0.5), (0.0, -1.0), (0.0, -2.0),
                    (-0.2, -1.0), (-0.5, -2.0)]:
    pc, info, note = phi_c(Din, Dout, inner='dir')
    EXT.append(dict(Din=Din, Dout=Dout, Phi_c=pc, note=note,
                    info=info))
    br = info["bracket"] if info and "bracket" in info else None
    log(f"  {Din:5.1f} {Dout:6.1f} {'dir':>5} "
        f"{(pc if pc is not None else float('nan')):9.4f} "
        f"{str(br):>20} {note}")

log("\nPART 2 -- CONTROL: INTERIOR (f<1, phi>0) fold, BOTH closures")
log("  Does the source-strength fold exist on the INTERIOR too? (scopes")
log("  whether the fold is exterior-specific or a general ON-source fact.)")
log(f"  {'Din':>5} {'Dout':>6} {'inner':>5} {'Phi_c':>9} {'bracket':>20} {'note'}")
INT = []
for (Din, Dout, inner) in [(0.5, 0.5, 'dir'), (0.8, 0.3, 'dir'),
                           (0.5, 0.5, 'neu'), (0.8, 0.3, 'neu')]:
    pc, info, note = phi_c(Din, Dout, inner=inner)
    INT.append(dict(Din=Din, Dout=Dout, inner=inner, Phi_c=pc, note=note, info=info))
    br = info["bracket"] if info and "bracket" in info else None
    log(f"  {Din:5.1f} {Dout:6.1f} {inner:>5} "
        f"{(pc if pc is not None else float('nan')):9.4f} "
        f"{str(br):>20} {note}")

log("\nPART 3 -- GRID CONVERGENCE of Phi_c (real fold vs discretization)")
log(f"  exterior (Din=0,Dout=-1.0): {'Nr':>5} {'Nth':>5} {'Phi_c':>9}")
PC = []
for (Nr, Nth) in [(101, 51), (161, 81), (241, 121)]:
    pc, info, note = phi_c(0.0, -1.0, inner='dir', Nr=Nr, Nth=Nth)
    PC.append(dict(Nr=Nr, Nth=Nth, Phi_c=pc))
    log(f"  {'':>27}{Nr:5d} {Nth:5d} {(pc if pc else float('nan')):9.4f}")

with open("/tmp/ext_scan_fold.json", "w") as fh:
    json.dump(dict(EXT=EXT, INT=INT, PC=PC), fh, indent=0, default=float)

# verdict
log("\n" + "="*72)
extf = [d for d in EXT if d["note"] == "fold"]
intf = [d for d in INT if d["note"] == "fold"]
log(f"  EXTERIOR media with a finite existence fold Phi_c: {len(extf)}/{len(EXT)}")
log(f"  INTERIOR controls with a finite fold:              {len(intf)}/{len(INT)}")
if PC[0]["Phi_c"] and PC[-1]["Phi_c"]:
    drift = abs(PC[-1]["Phi_c"]-PC[0]["Phi_c"])
    log(f"  Phi_c grid drift (coarse->fine): {drift:.4f} "
        f"({'grid-stable, REAL' if drift < 0.15 else 'grid-sensitive'})")
log("="*72)
log(f"ext_scan_fold COMPLETE ({time.time()-t0:.0f}s)  json /tmp/ext_scan_fold.json")
_fh.close()
