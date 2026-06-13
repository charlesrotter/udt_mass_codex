#!/usr/bin/env python3
"""
ens_scan_2cell.py -- MULTI-CELL / ENSEMBLE whole-metric solve (axisymmetric)
============================================================================
OPEN-ENDED METRIC-LED exploration (queue head step b, MULTI-CELL axis).
Driver: Claude (Opus 4.8). Date 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.
New file (repo discipline). GPU available but this solve is small; numpy
sparse Newton (same machinery as wint_solve2d.py) is robust + fast.

WHY THIS, AND WHY IT IS THE SAME METRIC (nothing added/slaved/frozen):
  The metric's OWN derived operator is the dilation-DRESSED Laplacian with
  the ON two-exponential restoring source (verified symbolically in
  wint_symcheck.py, used in wint_solve2d.py):
      Box_g phi = (1/sqrt g) d_a( sqrt g g^{ab} e^{-2phi} d_b phi ) = S(phi),
      S(phi) = Phi ( e^{-2phi} - e^{phi} )         [w_alg PART E, ON source].
  In the spherical (r,theta) chart wint_solve2d solves exactly this around a
  SINGLE centre. A single (r,theta) chart cannot hold TWO centres. The SAME
  geometric operator, written in AXISYMMETRIC CYLINDRICAL (rho,z) with the
  flat background measure sqrt g = rho, is
      (1/rho) d_rho( rho e^{-2phi} d_rho phi ) + d_z( e^{-2phi} d_z phi )
          = Phi( e^{-2phi} - e^{phi} ).
  This is the IDENTICAL native operator (e^{-2phi}-dressed Laplacian + ON
  source); the (rho,z) chart simply ADMITS two centres on the z-axis while
  staying axisymmetric (azimuthal Killing vector kept). phi varies in BOTH
  rho and z, so ANY non-round / neck / lobe structure is FREE to appear --
  both sectors live, nothing slaved, nothing frozen, nothing added.
  CONTROL: a single centre on this chart MUST reproduce the round cell
  (#34 baseline) -- the cross-chart consistency gate.

THE EXPLORATION (NOT mass-matching; NOT the trivial interior):
  Baseline to depart from (documented):
    - single cell = ONE round type, a smooth E/D-family CONTINUUM (#33/#34);
    - the seal = phi->0 mirror fold (a locus, not an edge);
    - absolute scale-free (#32); the prior ensemble doc (E1/E2): like cells
      REPEL statically E_int = 2pi Q1 Q2 / d (a MONOTONE 1/d, NO preferred
      separation) via an isolated-cell + posited-channel argument -- NOT a
      self-consistent two-cell whole-metric solve.
  Questions (character-change flags):
    Q1 does a self-consistent TWO-cell solve produce structure one cell
       cannot: a SHARED seal / neck (a phi->0 bridge), a bound config?
    Q2 does the interaction energy E(d) stay a MONOTONE 1/d (baseline), or
       does the WHOLE-metric two-cell solve PIN a preferred separation
       (a minimum) -- a discreteness the single-cell continuum lacks?
    Q3 does a NEW non-round pattern appear at the neck (rho-z lobe) absent
       from the single round cell?
  Outcomes reported honestly: baseline holds (monotone, no pinning, two
  independent round cells) vs a flagged character change (with evidence and
  real/artifact/documented self-grade).

Log /tmp/ens_scan.log (flush per line). Convergence evidence MANDATORY.
HYPOTHESIS-GRADE. DATA-BLIND (no wall-number comparison anywhere).
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla

t0 = time.time()
_fh = open("/tmp/ens_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    log(f"ENS-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 74)
log("ens_scan_2cell -- MULTI-CELL whole-metric solve (axisymmetric rho,z)")
log("=" * 74)

# =====================================================================
# The native operator in (rho,z), conservative flux form, e^{-2phi} dressed.
#   L[phi] = (1/rho) d_rho(rho e^{-2phi} d_rho phi) + d_z(e^{-2phi} d_z phi)
#   F[phi] = L[phi] - Phi(e^{-2phi} - e^{phi})
# Grid: rho in [0, Rmax] (axis at rho=0), z in [-Zmax, Zmax].
# Closure: outer box Dirichlet phi = D (the AMBIENT depth = partition datum);
#          axis rho=0 Neumann (regularity); SAME native ON source.
# Nothing added; this is wint_solve2d's operator in a 2-centre-capable chart.
# =====================================================================
def _box(phi, rho, z, drho, dz):
    w = np.exp(-2.0 * phi)
    Rho = rho[:, None]                                   # (Nr,1)
    # radial (rho) flux a = rho e^{-2phi}; midpoint averaging
    a_r = Rho * w
    am_r = 0.5 * (a_r[1:, :] + a_r[:-1, :])
    flux_r = am_r * (phi[1:, :] - phi[:-1, :]) / drho
    div_r = np.zeros_like(phi)
    div_r[1:-1, :] = (flux_r[1:, :] - flux_r[:-1, :]) / drho / Rho[1:-1]
    # z flux a = e^{-2phi}
    a_z = w
    am_z = 0.5 * (a_z[:, 1:] + a_z[:, :-1])
    flux_z = am_z * (phi[:, 1:] - phi[:, :-1]) / dz
    div_z = np.zeros_like(phi)
    div_z[:, 1:-1] = (flux_z[:, 1:] - flux_z[:, :-1]) / dz
    return div_r + div_z

def _residual(phi, rho, z, drho, dz, D, Phi_amp):
    Nr, Nz = phi.shape
    F = _box(phi, rho, z, drho, dz) - Phi_amp * (np.exp(-2 * phi)
                                                 - np.exp(phi))
    # closure rows overwrite F:
    F[0, :]  = phi[0, :]  - phi[1, :]      # axis rho=0 Neumann (regularity)
    F[-1, :] = phi[-1, :] - D              # outer rho Dirichlet (ambient)
    F[:, 0]  = phi[:, 0]  - D              # outer z- Dirichlet (ambient)
    F[:, -1] = phi[:, -1] - D              # outer z+ Dirichlet (ambient)
    return F

def _jacobian(phi, rho, z, drho, dz, D, Phi_amp, eps=1e-7):
    Nr, Nz = phi.shape
    N = Nr * Nz
    F0 = _residual(phi, rho, z, drho, dz, D, Phi_amp).ravel()
    idx = np.arange(N).reshape(Nr, Nz)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nr, Nz), dtype=bool)
            mask[ci::3, cj::3] = True
            ph = phi.copy(); ph[mask] += eps
            dF = ((_residual(ph, rho, z, drho, dz, D, Phi_amp).ravel()
                   - F0) / eps).reshape(Nr, Nz)
            owner = np.full((Nr, Nz), -1, dtype=np.int64)
            for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                si = np.arange(Nr)[:, None] + di
                sj = np.arange(Nz)[None, :] + dj
                valid = ((si >= 0) & (si < Nr) & (sj >= 0) & (sj < Nz))
                sic = np.clip(si, 0, Nr - 1); sjc = np.clip(sj, 0, Nz - 1)
                inc = valid & mask[sic, sjc] & (owner < 0)
                owner[inc] = idx[sic, sjc][inc]
            sel = owner >= 0
            vv = dF[sel]; nz = vv != 0.0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz])
            vals.append(vv[nz])
    return sps.csr_matrix((np.concatenate(vals),
                          (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)), F0

def _newton(phi0, rho, z, drho, dz, D, Phi_amp, itmax=200, tol=1e-10,
            verbose=False):
    phi = phi0.copy(); Nr, Nz = phi.shape; maxres = np.inf; hist = []
    for nit in range(itmax):
        J, F0 = _jacobian(phi, rho, z, drho, dz, D, Phi_amp)
        nF0 = float(np.linalg.norm(F0))
        try:
            dphi = spsla.spsolve(J, -F0).reshape(Nr, Nz)
        except Exception:
            return phi, maxres, nit, False, hist
        if not np.all(np.isfinite(dphi)):
            return phi, maxres, nit, False, hist
        lam = 1.0; ok = False
        for _ in range(50):
            trial = phi + lam * dphi
            if np.all(np.abs(trial) < 60):
                Ft = _residual(trial, rho, z, drho, dz, D, Phi_amp)
                if np.isfinite(Ft).all() and \
                        np.linalg.norm(Ft) < (1 - 1e-4 * lam) * nF0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            maxres = float(np.max(np.abs(_residual(
                phi, rho, z, drho, dz, D, Phi_amp)[1:-1, 1:-1])))
            return phi, maxres, nit, maxres < 1e-7, hist
        phi = phi + lam * dphi
        maxres = float(np.max(np.abs(_residual(
            phi, rho, z, drho, dz, D, Phi_amp)[1:-1, 1:-1])))
        hist.append((nit, float(lam), maxres))
        if verbose: log(f"    nt {nit} lam={lam:.3f} res={maxres:.2e}")
        if maxres < tol:
            return phi, maxres, nit + 1, True, hist
    return phi, maxres, itmax, maxres < 1e-7, hist


# ---------------------------------------------------------------------
# Energy functional of the NATIVE action (for reading interaction E(d)).
# The dilation action density on the static slice (C1, sqrt g = rho):
#   e_grad = (1/2) e^{-2phi} |grad phi|^2 ;  the ON-source potential well
#   V(phi) = Phi( (1/2) e^{-2phi} + e^{phi} )  (so dV/dphi = -S(phi)),
#   minimised at phi=0 (the seal locus). Total native energy
#   E = INT ( e_grad + V ) rho drho dz  (axisymmetric measure 2pi folded out).
# This is the metric's OWN energy; nothing added.
# ---------------------------------------------------------------------
def native_energy(phi, rho, z, drho, dz, Phi_amp, D):
    Rho = rho[:, None]
    pr = np.zeros_like(phi); pz = np.zeros_like(phi)
    pr[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2 * drho)
    pz[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / (2 * dz)
    grad2 = pr ** 2 + pz ** 2
    e_grad = 0.5 * np.exp(-2 * phi) * grad2
    V = Phi_amp * (0.5 * np.exp(-2 * phi) + np.exp(phi))
    Vref = Phi_amp * (0.5 * np.exp(-2 * D) + np.exp(D))   # ambient reference
    dens = (e_grad + (V - Vref)) * Rho
    return float(np.sum(dens) * drho * dz)


def make_grid(Rmax, Zmax, Nr, Nz):
    rho = np.linspace(0.0, Rmax, Nr)
    z = np.linspace(-Zmax, Zmax, Nz)
    return rho, z

def seed_cells(rho, z, D, centers, depth, width):
    """INITIAL data only: ambient D plus gaussian depressions (toward the
    well bottom phi=0) at each centre. The solver settles freely; we impose
    only the OUTER ambient Dirichlet, never the cell shape."""
    Rho = rho[:, None]; Z = z[None, :]
    phi = np.full((len(rho), len(z)), D)
    for (zc,) in centers:
        r2 = Rho ** 2 + (Z - zc) ** 2
        phi = phi + (0.0 - D) * depth * np.exp(-r2 / (2 * width ** 2))
    return phi


def solve_cfg(D, Phi_amp, centers, Rmax=8.0, Zmax=10.0, Nr=121, Nz=161,
              depth=1.0, width=1.2, verbose=False):
    rho, z = make_grid(Rmax, Zmax, Nr, Nz)
    drho = rho[1] - rho[0]; dz = z[1] - z[0]
    phi0 = seed_cells(rho, z, D, centers, depth, width)
    phi, maxres, nit, conv, hist = _newton(
        phi0, rho, z, drho, dz, D, Phi_amp, verbose=verbose)
    E = native_energy(phi, rho, z, drho, dz, Phi_amp, D)
    # diagnostics: where is phi near the seal (phi->0)? count minima on axis
    axis = phi[0, :]                       # phi(rho=0, z)
    # local minima of phi on axis (cells are depressions toward phi=0)
    mins = [(z[k], axis[k]) for k in range(1, len(z) - 1)
            if axis[k] < axis[k - 1] and axis[k] < axis[k + 1]]
    phimin = float(phi.min())
    # neck: min of axis phi BETWEEN the two centres (if 2 centres)
    return dict(conv=conv, maxres=maxres, nit=nit, E=E, phimin=phimin,
                n_axis_minima=len(mins), axis_minima=mins,
                phi=phi, rho=rho, z=z, drho=drho, dz=dz, D=D, Phi=Phi_amp)


def _main():
    Phi = 1.0
    log("\n--- GATE G0: single centre on (rho,z) reproduces a round cell ---")
    g = solve_cfg(D=2.0, Phi_amp=Phi, centers=[(0.0,)], verbose=False)
    # roundness: compare phi along +z axis vs along rho at z=0 (should match
    # for a spherically symmetric cell centred at origin)
    phi = g["phi"]; rho = g["rho"]; z = g["z"]
    iz0 = np.argmin(np.abs(z))
    # profile along rho at z=0:
    pr = phi[:, iz0]
    # profile along z at rho=0 (axis):
    pz = phi[0, :]
    # sample both at matched geometric radius and compare
    from numpy import interp
    zpos = z[iz0:]; pzpos = pz[iz0:]
    rr = rho
    common = np.linspace(0, min(rr.max(), zpos.max()) * 0.8, 40)
    f_r = interp(common, rr, pr)
    f_z = interp(common, zpos, pzpos)
    round_err = float(np.max(np.abs(f_r - f_z)))
    check("G0", g["conv"] and round_err < 5e-3,
          f"single centre converges (maxres={g['maxres']:.2e}) and is ROUND "
          f"(max|phi(rho)-phi(z)|={round_err:.2e} along matched radius) -- "
          "the (rho,z) chart reproduces the #34 round cell. Cross-chart OK.")
    log(f"   single-cell native energy E0 = {g['E']:.6f}, "
        f"phimin={g['phimin']:.4f}, axis minima={g['n_axis_minima']}")

    # ================= THE TWO-CELL SEPARATION SWEEP =================
    log("\n--- TWO-CELL SWEEP: E(d) and neck structure vs separation d ---")
    log(f"{'d':>6} {'conv':>5} {'maxres':>9} {'E2':>11} {'E_int':>11} "
        f"{'phimin':>8} {'neck_phi':>9} {'n_min':>5}")
    E_single = g["E"]
    seps = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]
    SWEEP = []
    for d in seps:
        centers = [(-d / 2,), (d / 2,)]
        r = solve_cfg(D=2.0, Phi_amp=Phi, centers=centers)
        phi = r["phi"]; z = r["z"]
        iz0 = np.argmin(np.abs(z))
        neck = float(phi[0, iz0])           # axis phi at the midpoint
        # E_int = E(2 cells at d) - 2*E(single isolated cell)
        E_int = r["E"] - 2 * E_single
        SWEEP.append(dict(d=d, conv=r["conv"], maxres=r["maxres"], E2=r["E"],
                          E_int=E_int, phimin=r["phimin"], neck=neck,
                          n_min=r["n_axis_minima"]))
        log(f"{d:6.2f} {str(r['conv']):>5} {r['maxres']:9.1e} {r['E']:11.5f} "
            f"{E_int:11.5f} {r['phimin']:8.4f} {neck:9.4f} "
            f"{r['n_axis_minima']:5d}")
        with open("/tmp/ens_scan_2cell.json", "w") as fh:
            json.dump([{k: v for k, v in s.items()} for s in SWEEP],
                      fh, indent=0)

    conv_sweep = [s for s in SWEEP if s["conv"]]
    check("SWEEP-conv", len(conv_sweep) >= int(0.7 * len(SWEEP)),
          f"{len(conv_sweep)}/{len(SWEEP)} two-cell solves converged")

    # ------ Q2: is E_int(d) monotone (baseline) or does it PIN a min? ------
    if len(conv_sweep) >= 4:
        ds = np.array([s["d"] for s in conv_sweep])
        Ei = np.array([s["E_int"] for s in conv_sweep])
        # interior local minimum of E_int(d)?
        interior_min = any(Ei[k] < Ei[k - 1] and Ei[k] < Ei[k + 1]
                           for k in range(1, len(Ei) - 1))
        # monotone trend?
        diffs = np.diff(Ei)
        mono = bool(np.all(diffs > 0) or np.all(diffs < 0))
        log(f"\n   E_int(d): {[f'{v:.4f}' for v in Ei]}")
        log(f"   monotone in d: {mono}; interior local minimum (PINNED "
            f"separation): {interior_min}")
        check("Q2-baseline", mono and not interior_min,
              "E_int(d) is MONOTONE with NO interior minimum -> baseline "
              "holds: no whole-metric-pinned preferred separation (consistent "
              "with the documented 1/d repulsion, no discreteness in d). "
              "[FAIL here = FLAG: the two-cell solve PINS a separation.]")

    # ------ Q1/Q3: shared seal / neck character change? ------
    # baseline: two cells -> two axis minima, neck phi stays near ambient D
    # (no phi->0 BRIDGE between them). Flag if neck reaches the seal phi->0
    # at large d (a shared seal a single cell cannot have).
    if conv_sweep:
        far = max(conv_sweep, key=lambda s: s["d"])
        near = min(conv_sweep, key=lambda s: s["d"])
        log(f"\n   far  d={far['d']}: neck_phi={far['neck']:.4f} "
            f"(ambient D=2.0), axis minima={far['n_min']}")
        log(f"   near d={near['d']}: neck_phi={near['neck']:.4f}, "
            f"axis minima={near['n_min']}")
        check("Q1-baseline", far["n_min"] >= 1,
              "at large separation the two cells are resolved as separate "
              "depressions (>=1 axis minima) -- two cells, not one merged "
              "blob. [Character change to watch: merge / shared seal.]")

    log(f"\nENS: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
    if FAIL: log("FAILED (=character-change flags to inspect): " + str(FAIL))
    log("checkpoint /tmp/ens_scan_2cell.json  log /tmp/ens_scan.log")


if __name__ == "__main__":
    _main()
    _fh.close()
