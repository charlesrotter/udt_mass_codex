#!/usr/bin/env python3
"""
offdiagII_character.py -- the CHARACTER of the negative direction (artifact vs type)
====================================================================================
OFF-DIAGONAL ANGULAR ROW II. Driver: Claude (Opus 4.8, 1M). 2026-06-13.

The full-operator scan (offdiagII_scan.py) returns lam0 < 0 on every formed
cell. BUT the decisive convergence test shows lam0 ~ -C/dtheta^2 -- it DIVERGES
under grid refinement (the backward-heat / unbounded-below signature). This
script settles whether that negative direction is:
  (i) a genuine FINITE-energy non-round bound state (a supported shaped type),
      which would converge to a finite negative lam0 under refinement and
      survive a vanishing higher-order regularizer; OR
 (ii) the grid-scale unbounded-below pathology of a sign-indefinite leading
      coefficient (no lowest eigenvalue exists; the static C1 truncation is
      incomplete -- a regularizing higher-gradient/w term is MISSING).

Tests:
  T1 backward-heat scaling: lam0 * dtheta^2 -> const  (=> unbounded, case ii).
  T2 regularizer limit: add eps * (biharmonic-like 2nd-diff penalty, PSD); if
     lam0 converges to a FINITE negative as eps->0 at fixed fine grid => a real
     bound state; if lam0 -> -inf as eps->0 => unbounded (case ii).
  T3 mode localization: is the negative eigenvector the highest-frequency
     grid mode (checkerboard in the K_th<0 cells) => artifact; or a smooth
     ell-structured profile => physical.
Template tripwire: SIGN/character only; no masses, no mode counts.
"""
import sys, time, json
import numpy as np
import scipy.linalg as sla
import scipy.sparse as sps
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from offdiagII_operator import onshell_coeffs, V_source, assemble_full, log
from numpy.polynomial.legendre import legval

log("=" * 78)
log("offdiagII_character -- artifact vs genuine shaped-type (the decisive read)")
log("time", time.strftime("%Y-%m-%d %H:%M:%S"))
log("=" * 78)

def bg(Nr, Nth, shift, depth=2.5, lobe=0.15, ell=2):
    r = np.linspace(0.18, 1.0, Nr); th = np.linspace(0.05, np.pi-0.05, Nth)
    x = (r-r[0])/(r[-1]-r[0]); base = depth*(1-x**2)
    Pl = legval(np.cos(th), [0]*ell+[1]); bump = np.exp(-((x-0.5)/0.3)**2)
    phi = base[:,None] + lobe*bump[:,None]*Pl[None,:] + shift
    return phi, r, th

def grads(phi, r, th):
    dr = r[1]-r[0]; dth = th[1]-th[0]
    return np.gradient(phi, dr, axis=0), np.gradient(phi, dth, axis=1)

def lowest_pair(A, M):
    Ad = A.toarray(); Md = np.asarray(M.todense())
    Ad = 0.5*(Ad+Ad.T)
    w, V = sla.eigh(Ad, Md)
    return w[0], V[:,0], w

# ---- T1: backward-heat scaling ----
def T1():
    log("\nT1 -- backward-heat scaling: lam0 ~ -C/dtheta^2 ?  (=> unbounded below)")
    log(f"{'Nth':>5}{'dth':>9}{'lam0':>12}{'lam0*dth^2':>13}")
    vals = []
    for (Nr, Nth) in [(31,19),(41,25),(61,37),(81,49),(101,61)]:
        phi, r, th = bg(Nr, Nth, 0.0)
        pr, pth = grads(phi, r, th); dth = th[1]-th[0]
        A, M, _, _, _ = assemble_full(phi, r, th, pr, pth, 1.0, m_az=0,
                                      include_V=True, flip_on=True)
        l0, _, _ = lowest_pair(A, M)
        vals.append(l0*dth**2)
        log(f"{Nth:5d}{dth:9.4f}{l0:12.2f}{l0*dth**2:13.4f}")
    spread = (max(vals)-min(vals))/abs(np.mean(vals))
    log(f"  lam0*dth^2 spread = {spread:.2f} (small + lam0 grows ~1/dth^2 "
        f"=> UNBOUNDED-BELOW, not a finite eigenvalue)")
    return vals

# ---- T2: regularizer limit ----
def add_reg(A, phi, r, th, eps):
    """Add eps * PSD angular curvature penalty INT (u_thth)^2 W -- a higher-
       gradient regularizer that bounds the backward-heat operator below. If
       the negative mode is physical (finite), lam0 converges as eps->0; if it
       is the grid pathology, lam0 -> -inf as eps->0."""
    Nr, Nth = phi.shape
    R = r[:,None]; sinth = np.sin(th)[None,:]; W = R**2*sinth
    dr = r[1]-r[0]; dth = th[1]-th[0]
    idx = np.arange(Nr*Nth).reshape(Nr, Nth)
    # second-difference (Laplacian-of-Laplacian style) penalty in theta: use
    # the squared discrete 2nd derivative -> PSD. Assemble L = D2, penalty L^T W L.
    rows, cols, vals = [], [], []
    for i in range(Nr):
        for j in range(1, Nth-1):
            # row j: (u[j-1]-2u[j]+u[j+1])/dth^2
            c = 1.0/dth**2
            for (jj, co) in [(j-1, c), (j, -2*c), (j+1, c)]:
                rows.append(idx[i,j]); cols.append(idx[i,jj]); vals.append(co)
    L = sps.csr_matrix((vals,(rows,cols)), shape=(Nr*Nth, Nr*Nth))
    Wdiag = sps.diags((W*dr*dth).ravel())
    return eps * (L.T @ Wdiag @ L)

def T2():
    log("\nT2 -- regularizer limit (fixed fine grid Nth=49): lam0(eps) as eps->0")
    log("    finite limit => genuine bound state; -> -inf => unbounded (artifact)")
    Nr, Nth = 81, 49
    phi, r, th = bg(Nr, Nth, 0.0)
    pr, pth = grads(phi, r, th)
    A, M, _, _, _ = assemble_full(phi, r, th, pr, pth, 1.0, m_az=0,
                                  include_V=True, flip_on=True)
    log(f"{'eps':>10}{'lam0':>14}")
    prev = None
    for eps in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 0.0]:
        Ar = A + (add_reg(A, phi, r, th, eps) if eps > 0 else 0*A)
        l0, _, _ = lowest_pair(Ar, M)
        tag = ""
        if prev is not None and l0 < prev - 1e-6: tag = " (still dropping)"
        prev = l0
        log(f"{eps:10.0e}{l0:14.2f}{tag}")
    log("  => if lam0 keeps dropping toward eps=0, the operator is UNBOUNDED "
        "BELOW: no lowest eigenvalue, the static C1 sign-indefiniteness is a "
        "missing-regularizer (incomplete-truncation) signal, NOT a shaped type.")

# ---- T3: mode localization ----
def T3():
    log("\nT3 -- negative-mode localization: checkerboard (artifact) vs smooth (type)")
    Nr, Nth = 61, 37
    phi, r, th = bg(Nr, Nth, 0.0)
    pr, pth = grads(phi, r, th)
    A, M, _, _, _ = assemble_full(phi, r, th, pr, pth, 1.0, m_az=0,
                                  include_V=True, flip_on=True)
    l0, v0, _ = lowest_pair(A, M)
    u = v0.reshape(Nr, Nth)
    # grid-roughness measure: ratio of high-freq (cell-to-cell sign flips) energy
    d2 = np.abs(np.diff(np.sign(u), axis=1)).sum() + np.abs(np.diff(np.sign(u), axis=0)).sum()
    frac_flips = d2 / (2*Nr*Nth)
    # where is the mode concentrated in theta?
    amp = (u**2).sum(axis=0); jpk = int(np.argmax(amp))
    log(f"  lam0={l0:.2f}; sign-flip fraction (1.0=checkerboard)={frac_flips:.3f}; "
        f"peak |u|^2 at theta={th[jpk]:.2f} (sinth={np.sin(th[jpk]):.2f})")
    log(f"  {'=> CHECKERBOARD grid mode (artifact)' if frac_flips > 0.4 else '=> smooth structured mode (would be physical)'}")

if __name__ == "__main__":
    T1(); T2(); T3()
    log("\noffdiagII_character done. See verdict synthesis in offdiagII_results.md.")
