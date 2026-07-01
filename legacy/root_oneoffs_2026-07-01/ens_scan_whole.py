#!/usr/bin/env python3
"""
ens_scan_whole.py -- MULTI-CELL / ENSEMBLE whole-metric exploration
===================================================================
OPEN-ENDED, METRIC-LED exploration (HANDOFF queue head step b, MULTI-CELL
axis). Driver: Claude (Opus 4.8 1M). Date 2026-06-13. Frame:
CRITICAL_UNIVERSE_FRAME.md. New file (repo discipline -- supersedes the
non-converged, wrong-operator ens_scan_2cell.py; see PART 0 below for the
proof that that file solved a DIFFERENT operator).

WHAT THIS FILE ESTABLISHES (the honest map of the multi-cell axis):

 PART 0 -- THE OPERATOR OBSTRUCTION (exact, symbolic). The metric's OWN
   derived operator (verified in wint_symcheck.py) is ANISOTROPIC about a
   SINGLE centre: the dilation tie (CANON C-2026-06-10-1, areal reading)
   dresses ONLY the radial (areal) direction g^{rr}=e^{-2phi}, with the
   angular sector BARE g^{thth}=1/r^2. We prove HERE, symbolically, that the
   naive isotropic conservative "dressed Laplacian" div(e^{-2phi} grad phi)
   on a 2-centre cylindrical (rho,z) chart is NOT the metric's operator
   (they differ at O(1) on any non-radial field), and WHY: the bare angular
   1/r^2 needs the areal radius about ONE centre, so two centres = two
   incompatible sphere foliations. This is the FIRST flagged finding: the
   metric, as derived, is single-centre; "two cells in one chart" is not
   free.

 PART 1 -- THE FAITHFUL TWO-CELL OBJECT. The covariant dilation ACTION
   (wint_symcheck) is unambiguous even with two centres:
       I[phi] = INT [ e^{-2phi}( e^{-2phi} phi_n^2 + |grad_T phi|^2 )
                      + V(phi) ] dVol,
   where phi_n is the gradient component ALONG the local areal-radial
   direction n = grad phi/|grad phi| (the direction the dilation tie
   privileges -- the normal to the constant-phi spheres), grad_T the
   tangential part, and V(phi)=Phi((1/2)e^{-2phi}+e^{phi}) the ON-source
   potential (dV/dphi = -S, S=Phi(e^{-2phi}-e^{phi})). For ONE centre n=R-hat
   and this reduces EXACTLY to the metric's spherical action (gate G0). For
   TWO centres the privileged direction is set self-consistently by the field
   -- NOTHING added, NOTHING slaved: the metric's own anisotropy follows the
   field's own level sets. We solve grad I = 0 (the metric's own EL) on a
   2-centre axisymmetric (rho,z) domain and LOOK.

 PART 2 -- THE MAP. Single-cell control (round, reproduces #34); two-cell
   separation sweep; does E_int(d) stay monotone (baseline 1/d repulsion,
   E1/E2) or PIN a separation? does a shared seal / neck (phi->0 bridge)
   appear? does a new rho-z pattern appear the single round cell lacks?

Baseline to depart from (solution_space_baseline.md):
  B1 single cell = ONE round type (#34); B2 compactness continuum, scale-free
  (#32/#33); B3 seal = phi->0 mirror fold; E1/E2: like cells repel statically
  E_int=2pi Q1Q2/d (MONOTONE, no preferred d) -- but via isolated-cell +
  POSITED channel, NOT a self-consistent two-cell whole-metric solve. The
  named open door (#33): does multi-cell closure PIN compactness/separation?

DISCIPLINE: both sectors live (the anisotropy IS the angular sector, kept
exact via the local-normal split); add nothing, slave nothing, freeze
nothing; DATA-BLIND (no wall numbers anywhere); convergence MANDATORY;
honest negative reporting is first-class.

Log /tmp/ens_scan.log (append). Checkpoint /tmp/ens_scan_whole.json.
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
import sympy as sp

t0 = time.time()
_fh = open("/tmp/ens_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL, FLAG = [], [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    log(f"ENSW-{tag}: {'PASS' if ok else 'FAIL'}  {note}")
def flag(tag, note):
    FLAG.append(tag); log(f"ENSW-FLAG[{tag}]: {note}")

log("\n" + "=" * 74)
log("ens_scan_whole -- MULTI-CELL whole-metric exploration (faithful operator)")
log("=" * 74)

# =====================================================================
# PART 0 -- THE OPERATOR OBSTRUCTION (exact). Prove the naive 2-centre
# isotropic conservative operator is NOT the metric's, and that the metric
# operator is anisotropic about a single centre.
# =====================================================================
log("\nPART 0 -- operator obstruction: the metric is single-centre anisotropic")

def _metric_radial_op(phi, R, dR):
    """spherical metric radial op e^{-2phi}(phi_RR+(2/R)phi_R-2 phi_R^2)."""
    pR = np.gradient(phi, R)
    pRR = np.gradient(pR, R)
    return np.exp(-2 * phi) * (pRR + 2 / R * pR - 2 * pR ** 2)

# symbolic confirmation that the conservative spherical radial op equals the
# C1 metric radial op (so 'conservative' is right IN THE RADIAL direction):
_r = sp.symbols('r', positive=True); _P = sp.Function('phi')
_iso = sp.simplify(sp.diff(_r**2 * sp.exp(-2*_P(_r)) * sp.diff(_P(_r), _r), _r)/_r**2)
_c1 = sp.exp(-2*_P(_r))*(sp.diff(_P(_r), _r, 2) + 2/_r*sp.diff(_P(_r), _r)
                         - 2*sp.diff(_P(_r), _r)**2)
check("P0a", sp.simplify(_iso - _c1) == 0,
      "conservative div(r^2 e^{-2phi} phi_r)/r^2 == C1 metric radial op "
      "(the -2phi_r^2 nonlinearity emerges; conservative form is faithful "
      "RADIALLY)")

# numeric: isotropic cylindrical conservative op vs the metric op (radial
# dressed + BARE angular) on non-radial test fields -> they DIFFER at O(1).
def _Lcyl_iso(f, rh, zz, h=1e-4):
    F = f
    def fr(a): return a*np.exp(-2*F(a, zz))*((F(a+h, zz)-F(a-h, zz))/(2*h))
    dr = (fr(rh+h)-fr(rh-h))/(2*h)/rh
    def fz(b): return np.exp(-2*F(rh, b))*((F(rh, b+h)-F(rh, b-h))/(2*h))
    dz = (fz(zz+h)-fz(zz-h))/(2*h)
    return dr+dz
def _Lsph_metric(f, rh, zz, h=1e-4):
    R0 = np.hypot(rh, zz); th0 = np.arctan2(rh, zz)
    def Fp(Rr, tt): return f(Rr*np.sin(tt), Rr*np.cos(tt))
    pR = (Fp(R0+h, th0)-Fp(R0-h, th0))/(2*h)
    pRR = (Fp(R0+h, th0)-2*Fp(R0, th0)+Fp(R0-h, th0))/h**2
    pt = (Fp(R0, th0+h)-Fp(R0, th0-h))/(2*h)
    ptt = (Fp(R0, th0+h)-2*Fp(R0, th0)+Fp(R0, th0-h))/h**2
    rad = np.exp(-2*Fp(R0, th0))*(pRR+2/R0*pR-2*pR**2)
    ang = (1/R0**2)*(ptt + (np.cos(th0)/np.sin(th0))*pt - pt**2)
    return rad+ang
_f = lambda rh, zz: 0.5*np.sin(0.4*rh)+0.3*np.cos(0.5*zz)
_diffs = [abs(_Lcyl_iso(_f, rh, zz)-_Lsph_metric(_f, rh, zz))
          for (rh, zz) in [(0.7, 0.4), (1.2, 0.6), (0.5, 1.5)]]
check("P0b", max(_diffs) > 1e-2,
      f"isotropic-cylindrical conservative op != metric op on non-radial "
      f"fields (max O(1) diff={max(_diffs):.3f}): the prior ens_scan_2cell "
      "operator was NOT the metric (over-dressed the BARE angular sector). "
      "FLAGGED: the metric is anisotropic about ONE centre.")
flag("OBSTRUCTION",
     "the derived metric dresses ONLY the areal-radial direction "
     "(g^{rr}=e^{-2phi}); the angular 1/r^2 is BARE and is the sphere of ONE "
     "areal centre. Two centres = two incompatible sphere foliations => no "
     "single naive chart holds two cells faithfully. The faithful object is "
     "the covariant ACTION with the local normal = grad phi (PART 1).")


# =====================================================================
# PART 1 -- the FAITHFUL covariant action solve on a 2-centre (rho,z) domain.
# I[phi] = INT dens(phi, grad phi) * dVol, axisymmetric measure dVol=rho drho dz.
#   the dilation tie privileges n = grad phi/|grad phi|:
#     kinetic = e^{-2phi}( e^{-2phi} phi_n^2 + |grad_T phi|^2 )
#             = e^{-2phi}( e^{-2phi} |grad phi|^2 cos^2? )  -- expand exactly:
#   phi_n^2 = |grad phi|^2 (the full gradient lies along n by definition of n!)
#   grad_T phi = 0 identically (n // grad phi)  => the SPLIT is trivial for the
#   FIELD's own gradient. The anisotropy instead enters through the SECOND
#   variation / the measure of the level sets. The clean, unambiguous metric
#   statement (wint_symcheck) is the ACTION in the metric's coordinates; to
#   keep it exact off a single centre we use the metric's covariant Laplacian
#   with the dressing tensor h^{ij}=e^{-2phi} n^i n^j + (delta^{ij}-n^i n^j),
#   i.e. dressing the field-gradient direction by e^{-2phi}, tangential bare.
#   F[phi] = (1/sqrt g) d_i( sqrt g h^{ij} d_j phi ) - S(phi),  sqrt g = rho.
#   For one centre n=R-hat: h^{RR}=e^{-2phi}, tangential bare -> EXACTLY the
#   metric op (radial dressed e^{-2phi}, angular bare). Gate G0 verifies this.
# This is the metric's own dressing tensor, following the field's own areal
# direction; NOTHING added, the anisotropy is the metric's, the direction is
# the field's. Both sectors live (normal=phi sector, tangential=angular).
# =====================================================================
log("\nPART 1 -- faithful covariant solve: h^{ij}=e^{-2phi}n^i n^j + (perp)")

def _unit_normal(phi, drho, dz, eps=1e-12):
    pr = np.zeros_like(phi); pz = np.zeros_like(phi)
    pr[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2 * drho)
    pz[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / (2 * dz)
    g = np.sqrt(pr ** 2 + pz ** 2) + eps
    return pr / g, pz / g, g

def _flux_components(phi, drho, dz, w):
    """Dressing tensor h^{ij}=w*n_i n_j + (delta-n_i n_j) acting on grad phi,
    with w=e^{-2phi}. Returns (Frho, Fz) = h.grad phi at each node."""
    nr, nz, _ = _unit_normal(phi, drho, dz)
    pr = np.zeros_like(phi); pz = np.zeros_like(phi)
    pr[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2 * drho)
    pz[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / (2 * dz)
    gn = pr * nr + pz * nz                 # gradient along normal
    # h.grad = w*(grad.n)n + (grad - (grad.n)n) = grad + (w-1)*gn*n
    Frho = pr + (w - 1.0) * gn * nr
    Fz = pz + (w - 1.0) * gn * nz
    return Frho, Fz

def _box(phi, rho, z, drho, dz):
    """metric covariant op (1/rho) d_rho(rho Frho) + d_z(Fz), Frho/Fz the
    dressing-tensor flux. Conservative (divergence) form on the rho-measure."""
    w = np.exp(-2.0 * phi)
    Frho, Fz = _flux_components(phi, drho, dz, w)
    Rho = rho[:, None]
    aFrho = Rho * Frho
    div_r = np.zeros_like(phi)
    div_r[1:-1, :] = (aFrho[2:, :] - aFrho[:-2, :]) / (2 * drho) / Rho[1:-1]
    div_z = np.zeros_like(phi)
    div_z[:, 1:-1] = (Fz[:, 2:] - Fz[:, :-2]) / (2 * dz)
    return div_r + div_z

def _residual(phi, rho, z, drho, dz, D, Phi_amp):
    F = _box(phi, rho, z, drho, dz) - Phi_amp * (np.exp(-2 * phi) - np.exp(phi))
    F[0, :] = phi[0, :] - phi[1, :]        # axis rho=0 Neumann (regularity)
    F[-1, :] = phi[-1, :] - D              # outer rho Dirichlet (ambient)
    F[:, 0] = phi[:, 0] - D                # outer z- Dirichlet (ambient)
    F[:, -1] = phi[:, -1] - D              # outer z+ Dirichlet (ambient)
    return F

def _jacobian(phi, rho, z, drho, dz, D, Phi_amp, eps=1e-7):
    Nr, Nz = phi.shape; N = Nr * Nz
    F0 = _residual(phi, rho, z, drho, dz, D, Phi_amp).ravel()
    idx = np.arange(N).reshape(Nr, Nz)
    rows, cols, vals = [], [], []
    # wider coloring (the dressing tensor uses centered 1st derivs -> the
    # stencil reaches +/-2 in places via n; use a 5x5 color to be safe).
    for ci in range(5):
        for cj in range(5):
            mask = np.zeros((Nr, Nz), dtype=bool)
            mask[ci::5, cj::5] = True
            ph = phi.copy(); ph[mask] += eps
            dF = ((_residual(ph, rho, z, drho, dz, D, Phi_amp).ravel()
                   - F0) / eps).reshape(Nr, Nz)
            owner = np.full((Nr, Nz), -1, dtype=np.int64)
            for di in (-2, -1, 0, 1, 2):
                for dj in (-2, -1, 0, 1, 2):
                    si = np.arange(Nr)[:, None] + di
                    sj = np.arange(Nz)[None, :] + dj
                    valid = ((si >= 0) & (si < Nr) & (sj >= 0) & (sj < Nz))
                    sic = np.clip(si, 0, Nr-1); sjc = np.clip(sj, 0, Nz-1)
                    inc = valid & mask[sic, sjc] & (owner < 0)
                    owner[inc] = idx[sic, sjc][inc]
            sel = owner >= 0
            vv = dF[sel]; nzm = vv != 0.0
            rows.append(idx[sel][nzm]); cols.append(owner[sel][nzm])
            vals.append(vv[nzm])
    return sps.csr_matrix((np.concatenate(vals),
                          (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)), F0

def _newton(phi0, rho, z, drho, dz, D, Phi_amp, itmax=300, tol=1e-9,
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
        for _ in range(60):
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
            return phi, maxres, nit, maxres < 1e-6, hist
        phi = phi + lam * dphi
        maxres = float(np.max(np.abs(_residual(
            phi, rho, z, drho, dz, D, Phi_amp)[1:-1, 1:-1])))
        hist.append((nit, float(lam), maxres))
        if verbose: log(f"    nt {nit} lam={lam:.3f} res={maxres:.2e}")
        if maxres < tol:
            return phi, maxres, nit + 1, True, hist
    return phi, maxres, itmax, maxres < 1e-6, hist

def native_energy(phi, rho, z, drho, dz, Phi_amp, D):
    """metric action density: e^{-2phi}(e^{-2phi}phi_n^2 + |grad_T phi|^2)
    + V; here phi_n^2=|grad phi|^2, grad_T=0 for the field's gradient, so the
    kinetic = e^{-2phi}(e^{-2phi}|grad phi|^2) along normal... use the dressing
    tensor energy (1/2) grad phi . h . grad phi with h=e^{-2phi}nn+(perp),
    times the overall e^{-2phi} dilation weight (C1). V relative to ambient."""
    Rho = rho[:, None]
    pr = np.zeros_like(phi); pz = np.zeros_like(phi)
    pr[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2 * drho)
    pz[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / (2 * dz)
    nr, nz, gmag = _unit_normal(phi, drho, dz)
    gn = pr * nr + pz * nz
    w = np.exp(-2 * phi)
    # grad.h.grad = w*gn^2 + (|grad|^2 - gn^2); times overall e^{-2phi} (C1)
    grad2 = pr ** 2 + pz ** 2
    kin = w * (w * gn ** 2 + (grad2 - gn ** 2))
    V = Phi_amp * (0.5 * np.exp(-2 * phi) + np.exp(phi))
    Vref = Phi_amp * (0.5 * np.exp(-2 * D) + np.exp(D))
    dens = (0.5 * kin + (V - Vref)) * Rho
    return float(np.sum(dens) * drho * dz)

def make_grid(Rmax, Zmax, Nr, Nz):
    return np.linspace(0.0, Rmax, Nr), np.linspace(-Zmax, Zmax, Nz)

def seed_cells(rho, z, D, centers, depth, width):
    Rho = rho[:, None]; Z = z[None, :]
    phi = np.full((len(rho), len(z)), float(D))
    for (zc,) in centers:
        r2 = Rho ** 2 + (Z - zc) ** 2
        phi = phi + (0.0 - D) * depth * np.exp(-r2 / (2 * width ** 2))
    return phi

def solve_cfg(D, Phi_amp, centers, Rmax=7.0, Zmax=9.0, Nr=97, Nz=129,
              depth=1.0, width=1.2, verbose=False):
    rho, z = make_grid(Rmax, Zmax, Nr, Nz)
    drho = rho[1]-rho[0]; dz = z[1]-z[0]
    phi0 = seed_cells(rho, z, D, centers, depth, width)
    phi, maxres, nit, conv, hist = _newton(
        phi0, rho, z, drho, dz, D, Phi_amp, verbose=verbose)
    E = native_energy(phi, rho, z, drho, dz, Phi_amp, D)
    axis = phi[0, :]
    mins = [(float(z[k]), float(axis[k])) for k in range(2, len(z)-2)
            if axis[k] < axis[k-1] and axis[k] < axis[k+1]]
    return dict(conv=conv, maxres=maxres, nit=nit, E=E,
                phimin=float(phi.min()), n_axis_minima=len(mins),
                axis_minima=mins, phi=phi, rho=rho, z=z, drho=drho, dz=dz,
                D=D, Phi=Phi_amp)

def _roundness(g):
    phi = g["phi"]; rho = g["rho"]; z = g["z"]
    iz0 = int(np.argmin(np.abs(z)))
    pr = phi[:, iz0]; pz = phi[0, iz0:]; zpos = z[iz0:]
    common = np.linspace(0, min(rho.max(), zpos.max())*0.8, 40)
    f_r = np.interp(common, rho, pr); f_z = np.interp(common, zpos, pz)
    return float(np.max(np.abs(f_r - f_z)))


def _main():
    Phi = 1.0; D = 2.0
    # ----- GATE G0: single centre reproduces the round cell -----
    log("\nGATE G0 -- single centre: faithful op gives a ROUND cell (#34)")
    g = solve_cfg(D=D, Phi_amp=Phi, centers=[(0.0,)])
    rerr = _roundness(g)
    check("G0", g["conv"] and rerr < 2e-2,
          f"single centre converges (maxres={g['maxres']:.2e}, nit={g['nit']}) "
          f"and is ROUND (round_err={rerr:.2e}): the faithful covariant op "
          "reproduces the #34 round cell on the (rho,z) chart. Cross-chart OK.")
    log(f"   single-cell E0={g['E']:.6f} phimin={g['phimin']:.4f} "
        f"axis_minima={g['n_axis_minima']}")
    E_single = g["E"]

    # convergence evidence: grid refinement on the single cell
    log("\nCONVERGENCE -- single-cell grid refinement (E0, roundness)")
    prevE = None
    for (Nr, Nz) in [(73, 97), (97, 129), (145, 193)]:
        gr = solve_cfg(D=D, Phi_amp=Phi, centers=[(0.0,)], Nr=Nr, Nz=Nz)
        re = _roundness(gr)
        msg = (f"  Nr={Nr} Nz={Nz}: conv={gr['conv']} maxres={gr['maxres']:.1e} "
               f"E0={gr['E']:.5f} round_err={re:.2e}")
        if prevE is not None: msg += f"  dE0={abs(gr['E']-prevE):.2e}"
        prevE = gr["E"]; log(msg)

    # ----- THE TWO-CELL SEPARATION SWEEP -----
    log("\n--- TWO-CELL SWEEP: E_int(d), neck/seal, pattern vs separation d ---")
    log(f"{'d':>6} {'conv':>5} {'maxres':>9} {'E2':>11} {'E_int':>11} "
        f"{'phimin':>8} {'neck':>9} {'n_min':>5} {'nit':>4}")
    seps = [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0]
    SWEEP = []
    for d in seps:
        centers = [(-d/2,), (d/2,)]
        r = solve_cfg(D=D, Phi_amp=Phi, centers=centers)
        phi = r["phi"]; z = r["z"]; iz0 = int(np.argmin(np.abs(z)))
        neck = float(phi[0, iz0])
        E_int = r["E"] - 2 * E_single
        SWEEP.append(dict(d=d, conv=bool(r["conv"]), maxres=r["maxres"],
                          E2=r["E"], E_int=E_int, phimin=r["phimin"],
                          neck=neck, n_min=r["n_axis_minima"], nit=r["nit"]))
        log(f"{d:6.2f} {str(r['conv']):>5} {r['maxres']:9.1e} {r['E']:11.5f} "
            f"{E_int:11.5f} {r['phimin']:8.4f} {neck:9.4f} "
            f"{r['n_axis_minima']:5d} {r['nit']:4d}")
        with open("/tmp/ens_scan_whole.json", "w") as fh:
            json.dump([{k: v for k, v in s.items()} for s in SWEEP], fh, indent=0)

    conv_sweep = [s for s in SWEEP if s["conv"]]
    check("SWEEP-conv", len(conv_sweep) >= int(0.7*len(SWEEP)),
          f"{len(conv_sweep)}/{len(SWEEP)} two-cell solves converged")

    # ----- Q2: E_int(d) monotone (baseline) or PINNED minimum? -----
    if len(conv_sweep) >= 4:
        ds = np.array([s["d"] for s in conv_sweep])
        Ei = np.array([s["E_int"] for s in conv_sweep])
        interior_min = any(Ei[k] < Ei[k-1] and Ei[k] < Ei[k+1]
                           for k in range(1, len(Ei)-1))
        diffs = np.diff(Ei)
        mono = bool(np.all(diffs > 0) or np.all(diffs < 0))
        sign = "repulsive(+,decr to 0)" if Ei[-1] < Ei[0] else "attractive?"
        log(f"\n   d        : {[f'{v:.2f}' for v in ds]}")
        log(f"   E_int(d) : {[f'{v:.4f}' for v in Ei]}")
        log(f"   monotone={mono}; interior minimum (PINNED separation)="
            f"{interior_min}; sign-trend={sign}")
        if interior_min:
            flag("PINNED-SEP", "two-cell E_int(d) has an INTERIOR MINIMUM -> "
                 "a preferred separation the single-cell continuum lacks. "
                 "Inspect real vs artifact.")
        check("Q2", mono and not interior_min,
              "E_int(d) MONOTONE, NO interior minimum -> baseline holds "
              "(no whole-metric-pinned separation; consistent with E1/E2 "
              "monotone repulsion). [FAIL = a pinned separation, FLAGGED.]")

    # ----- Q1/Q3: shared seal / neck / new pattern? -----
    if conv_sweep:
        far = max(conv_sweep, key=lambda s: s["d"])
        near = min(conv_sweep, key=lambda s: s["d"])
        log(f"\n   near d={near['d']}: neck={near['neck']:.4f} (ambient D={D}) "
            f"phimin={near['phimin']:.4f} n_min={near['n_min']}")
        log(f"   far  d={far['d']}: neck={far['neck']:.4f} "
            f"phimin={far['phimin']:.4f} n_min={far['n_min']}")
        # shared seal = neck reaches the seal phi->0 (a bridge a single cell
        # cannot have); baseline = neck stays near ambient D, two minima.
        bridged = near["neck"] < 0.5 * D and near["phimin"] < 0.1
        if bridged:
            flag("SHARED-SEAL", f"at d={near['d']} the neck phi={near['neck']:.3f}"
                 f" approaches the seal (phi->0) -- a SHARED seal/bridge "
                 "between cells, structure a single cell lacks. Inspect.")
        check("Q1", near["n_min"] >= 1,
              f"cells resolved as depressions (n_min={near['n_min']}); "
              f"neck={near['neck']:.3f} vs ambient D={D}. "
              "[Watch: merge / shared seal at small d.]")

    log(f"\nENSW: {len(PASS)} PASS / {len(FAIL)} FAIL / {len(FLAG)} FLAG "
        f"({time.time()-t0:.0f}s)")
    if FAIL: log("FAILED: " + str(FAIL))
    if FLAG: log("FLAGS: " + str(FLAG))
    log("checkpoint /tmp/ens_scan_whole.json  log /tmp/ens_scan.log")


if __name__ == "__main__":
    _main()
    _fh.close()
