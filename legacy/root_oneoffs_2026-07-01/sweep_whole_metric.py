#!/usr/bin/env python3
"""
sweep_whole_metric.py -- THE COMPREHENSIVE WHOLE-METRIC SWEEP (r*, depth)
========================================================================
Driver: Claude (Opus 4.8, 1M ctx). Date 2026-06-13. New file (discipline).
Frame: CRITICAL_UNIVERSE_FRAME.md (governing). Charles's zoom-out order:
solve the WHOLE metric directly, both sectors live & simultaneous, across
the ENTIRE free-data plane (r*, depth), and MAP the emergent structure --
NOT a mechanism probe, NOT a single test, NOT a flow-chart trust-window
retreat. ADD NOTHING. SLAVE NOTHING.

THE METRIC'S OWN FIELD EQUATION (exact; verified wint_symcheck.py 3/3):
   ds^2 = -e^{-2phi}c^2 dt^2 + e^{+2phi}dr^2 + r^2 dOmega^2,  phi=phi(r,theta)
   Box_g phi = S(phi),
   Box_g phi = (1/r^2) d_r( r^2 e^{-2phi} phi_r )
             + (1/(r^2 sin th)) d_th( sin th e^{-2phi} phi_th )
             = r^{-2}e^{-2phi}[ r^2 phi_rr + 2 r phi_r - 2 r^2 phi_r^2 ]
               + r^{-2}[ phi_thth + cot th phi_th - phi_th^2 ]   (dressed)
   S(phi) = Phi (e^{-2phi} - e^{phi})    [the metric's OWN ON restoring
                                          content, w_alg PART E -- TAKEN].
   (Phi->0 recovers the bare metric EOM, registry #33.)
The e^{2phi}/r^2-dressed angular operator + the derived nonlinearity
-phi_th^2 are BOTH carried by the metric -- the phi-angular coupling
(Charles's standing hunch) appears for FREE. Nothing added.

PHYSICAL (r,theta) -- the chart the (r*,depth) plane lives in (NOT the
scale-free flow chart that bins r* out). Finite-cell canon C-2026-06-10-2:
the matter cell is INSIDE-OUT -- phi=0 at the OUTER interface r*, phi->+inf
toward the CORE (where f=e^{-2phi}->0 = the seal). BC LAYOUT:
   outer r=r*  : Dirichlet  phi(r*,theta) = 0     (the interface; r* swept)
   inner r=r_in: Dirichlet  phi(r_in,theta) = D   (the CORE DEPTH; swept;
                 the genuine partition/matter-content datum)
   axis th=0,pi: Neumann    phi_th = 0            (sphere regularity)
The two genuine FREE DATA are (r*, D). f_core = e^{-2D} -> 0 IS the seal.

THE SWEEP: r* across several decades; D across its full range (round AND
Legendre l=1..4 lobed seeds at every point); continuation in D warm-started
toward the seal; dual-grid at near-seal points (grid-independence = the
edge-vs-structure discriminant). Misner-Sharp m(r)=(c^2 r/2G)(1-e^{-2<phi>_th}),
compactness X=2Gm/(c^2 r*)=1-e^{-2<phi(r*)>}, theta-variance/lobe-persistence,
Ricci scalar, Kretschmann, and the FORM/UNFORM critical locus.

Convergence MANDATORY. DATA-BLIND. HYPOTHESIS-GRADE. Log /tmp/sweep.log.
"""
import sys, time, json, os
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
from scipy.integrate import solve_ivp
from multiprocessing import Pool

t0 = time.time()
LOG = "/tmp/sweep.log"
_fh = open(LOG, "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

# =====================================================================
# THE METRIC'S OWN OPERATOR (physical r,theta), conservative flux form.
# Box_g phi = (1/r^2) d_r(r^2 e^{-2phi} phi_r)
#           + (1/(r^2 sinth)) d_th(sinth e^{-2phi} phi_th)
# The dilation weight e^{-2phi} is from the CURRENT phi every step (two-way).
# =====================================================================
def box_np(phi, r, th, dr, dth):
    w = np.exp(-2.0 * phi)
    R = r[:, None]
    sinth = np.sin(th)[None, :]
    a_r = (R ** 2) * w
    am_r = 0.5 * (a_r[1:, :] + a_r[:-1, :])
    flux_r = am_r * (phi[1:, :] - phi[:-1, :]) / dr
    div_r = np.zeros_like(phi)
    div_r[1:-1, :] = (flux_r[1:, :] - flux_r[:-1, :]) / dr / (R[1:-1] ** 2)
    a_th = sinth * w
    am_th = 0.5 * (a_th[:, 1:] + a_th[:, :-1])
    flux_th = am_th * (phi[:, 1:] - phi[:, :-1]) / dth
    div_th = np.zeros_like(phi)
    div_th[:, 1:-1] = (flux_th[:, 1:] - flux_th[:, :-1]) / dth \
        / (R ** 2 * sinth)[:, 1:-1]
    return div_r + div_th

def residual_np(phi, r, th, dr, dth, D, Phi_amp):
    """F = Box_g phi - S(phi). Closure rows overwrite F:
       outer Dirichlet phi(r*)=0 ; inner Dirichlet phi(r_in)=D ; axis Neumann.
    The inner end carries the CORE DEPTH D (the swept matter content); the
    outer end is the physical interface at r*. NOTHING added."""
    F = box_np(phi, r, th, dr, dth) - Phi_amp * (np.exp(-2 * phi)
                                                 - np.exp(phi))
    F[-1, :] = phi[-1, :] - 0.0          # outer interface  phi(r*)=0
    F[0, :] = phi[0, :] - D              # inner core depth phi(r_in)=D
    F[:, 0] = phi[:, 0] - phi[:, 1]      # axis Neumann theta=0
    F[:, -1] = phi[:, -1] - phi[:, -2]   # axis Neumann theta=pi
    return F

def jacobian_np(phi, r, th, dr, dth, D, Phi_amp, eps=1e-7):
    """Sparse Jacobian by 3x3-colored finite differences (5-point stencil)."""
    Nr, Nth = phi.shape
    N = Nr * Nth
    F0 = residual_np(phi, r, th, dr, dth, D, Phi_amp).ravel()
    idx = np.arange(N).reshape(Nr, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nr, Nth), dtype=bool)
            mask[ci::3, cj::3] = True
            ph = phi.copy(); ph[mask] += eps
            dF = ((residual_np(ph, r, th, dr, dth, D, Phi_amp).ravel()
                   - F0) / eps).reshape(Nr, Nth)
            owner = np.full((Nr, Nth), -1, dtype=np.int64)
            for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                si = np.clip(np.arange(Nr)[:, None] + di, 0, Nr - 1)
                sj = np.clip(np.arange(Nth)[None, :] + dj, 0, Nth - 1)
                valid = ((np.arange(Nr)[:, None] + di >= 0)
                         & (np.arange(Nr)[:, None] + di < Nr)
                         & (np.arange(Nth)[None, :] + dj >= 0)
                         & (np.arange(Nth)[None, :] + dj < Nth))
                inc = valid & mask[si, sj] & (owner < 0)
                owner[inc] = idx[si, sj][inc]
            sel = owner >= 0
            vv = dF[sel]; nz = vv != 0.0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz])
            vals.append(vv[nz])
    J = sps.csr_matrix((np.concatenate(vals),
                        (np.concatenate(rows), np.concatenate(cols))),
                       shape=(N, N))
    return J, F0

def newton2d(phi0, r, th, dr, dth, D, Phi_amp, itmax=200, tol=1e-10):
    phi = phi0.copy(); Nr, Nth = phi.shape; maxres = np.inf; hist = []
    for nit in range(itmax):
        J, F0 = jacobian_np(phi, r, th, dr, dth, D, Phi_amp)
        nF0 = float(np.linalg.norm(F0))
        try:
            dphi = spsla.spsolve(J, -F0).reshape(Nr, Nth)
        except Exception:
            return phi, maxres, nit, False, hist, None
        if not np.all(np.isfinite(dphi)):
            return phi, maxres, nit, False, hist, None
        lam = 1.0; ok = False
        for _ in range(50):
            trial = phi + lam * dphi
            if np.all(np.abs(trial) < 80):
                Ft = residual_np(trial, r, th, dr, dth, D, Phi_amp)
                if np.isfinite(Ft).all() and \
                        np.linalg.norm(Ft) < (1 - 1e-4 * lam) * nF0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            maxres = float(np.max(np.abs(
                residual_np(phi, r, th, dr, dth, D, Phi_amp)[1:-1, 1:-1])))
            return phi, maxres, nit, maxres < 1e-7, hist, J
        phi = phi + lam * dphi
        maxres = float(np.max(np.abs(
            residual_np(phi, r, th, dr, dth, D, Phi_amp)[1:-1, 1:-1])))
        hist.append((nit, float(lam), maxres))
        if maxres < tol:
            return phi, maxres, nit + 1, True, hist, J
    return phi, maxres, itmax, maxres < 1e-7, hist, J

# =====================================================================
# CURVATURE INVARIANTS (numeric, from FD derivatives of the converged phi)
# Metric: g_tt=-f, g_rr=1/f, g_thth=r^2, g_phph=r^2 sin^2 th ; f=e^{-2phi}.
# Diagonal but theta-dependent => angular cross terms are the FINGERPRINT
# of genuine angular structure (vanish for a round cell).
# We compute the Ricci scalar from the field eqn trace identity and the
# areal-deficit term, and a Kretschmann proxy from the dominant sectional
# curvatures (radial-time, areal-deficit, angular-cross). These are
# DIAGNOSTICS for WHERE curvature concentrates (seal/axis/lobe), reported
# honestly as proxies, not exact closed forms (those are heavy & not needed
# for a concentration map).
# =====================================================================
def curvature_diag(phi, r, th, dr, dth):
    R = r[:, None]; f = np.exp(-2.0 * phi)
    # interior centered derivatives
    pr = np.zeros_like(phi); prr = np.zeros_like(phi)
    pr[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2 * dr)
    prr[1:-1, :] = (phi[2:, :] - 2 * phi[1:-1, :] + phi[:-2, :]) / dr ** 2
    pth = np.zeros_like(phi); pthth = np.zeros_like(phi)
    pth[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / (2 * dth)
    pthth[:, 1:-1] = (phi[:, 2:] - 2 * phi[:, 1:-1] + phi[:, :-2]) / dth ** 2
    cot = (np.cos(th) / np.maximum(np.sin(th), 1e-12))[None, :]
    # Ricci scalar: field-eqn operator part + areal deficit (2/r^2)(1-f).
    # On a converged solution the operator part = the source S; we report
    # the assembled R_Ric to map concentration (sign convention internal).
    box_like = f * (prr + (2 / R) * pr - 2 * pr ** 2) \
        + (1 / R ** 2) * (pthth + cot * pth - pth ** 2)
    deficit = (2.0 / R ** 2) * (1.0 - f)
    R_Ric = -2.0 * box_like + deficit
    # Kretschmann proxy: sum of squared dominant sectional curvatures.
    k_rt = (f * (prr - 2 * pr ** 2)) ** 2                 # radial-time
    k_def = ((1.0 - f) / R ** 2) ** 2                     # areal deficit
    k_rad = (f * pr / R) ** 2                             # radial-areal
    k_ang = (f * pth / R ** 2) ** 2                       # ANGULAR cross
    K = 4 * k_rt + 4 * k_def + 8 * k_rad + 8 * k_ang
    return R_Ric, K, k_ang

# =====================================================================
# THE RADIAL BACKBONE by INWARD SHOOTING (well-conditioned; avoids the
# Bratu/Liouville BVP turning-point pathology). Integrate the radial field
# equation  phi'' = Phi(1-e^{3phi}) - (2/r)phi' + 2 phi'^2  inward from the
# interface r* (phi=0) with shooting slope g=phi'(r*); bisect g so that
# phi(r_in)=D. Returns the radial profile, or None if the cell hits the
# SEAL inside the domain (f->0 = NO static cell exists = the form/unform
# boundary). This is the metric's own radial sector; nothing added.
# =====================================================================
def radial_shoot(r, r_star, D, Phi):
    def rhs(rr, y):
        phi, phip = y
        return [phip, Phi * (1 - np.exp(3 * phi)) - (2 / rr) * phip
                + 2 * phip ** 2]
    r_in = r[0]
    def at_in(g):
        sol = solve_ivp(rhs, [r_star, r_in], [0.0, g], dense_output=True,
                        rtol=1e-10, atol=1e-12, method='Radau')
        if not sol.success or abs(sol.t[-1] - r_in) > 1e-6:
            return None, None
        return sol.y[0, -1], sol
    # scan shooting slope (more negative -> deeper); find first g with phi>=D
    prev = None; best = None
    for g in np.linspace(-1e-3, -20.0, 600):
        v, sol = at_in(g)
        if v is None:
            break
        if v >= D:
            best = (g, sol); break
        prev = (g, sol)
    if best is None or prev is None:
        return None              # cannot reach depth D before the seal
    a, b = prev[0], best[0]; ls = best[1]
    for _ in range(60):
        m = 0.5 * (a + b); v, sol = at_in(m)
        if v is None:
            b = m; continue
        if v < D:
            a = m
        else:
            b = m; ls = sol
    return ls.sol(r)[0]

# =====================================================================
# ONE (r*, D) SOLVE -- two-way self-consistent, both sectors live.
# Seed = the inward-shot radial backbone (round) + optional Legendre lobe;
# then the FULL 2D damped-Newton settles both sectors self-consistently.
# =====================================================================
def solve_point(r_in, r_star, D, Phi_amp, seed_lobe=0, seed_amp=0.0,
                Nr=161, Nth=49, warm=None):
    r = np.linspace(r_in, r_star, Nr)
    th = np.linspace(0.0, np.pi, Nth)
    dr = r[1] - r[0]; dth = th[1] - th[0]
    if warm is not None and warm.shape == (Nr, Nth):
        phi = warm.copy()
    else:
        vr = radial_shoot(r, r_star, D, Phi_amp)
        if vr is None:
            # the radial cell does not exist at this (r*,D): the SEAL is
            # reached inside the domain -> UNFORMED (no static solution).
            return dict(r_in=r_in, r_star=r_star, D=D, Phi=Phi_amp,
                        seed_lobe=seed_lobe, seed_amp=seed_amp, Nr=Nr,
                        Nth=Nth, conv=False, exists=False, maxres=np.inf,
                        nit=0, th_var=0.0, dom_l=0, X_star=0.0, ms_max=0.0,
                        comp_max=0.0, f_core=0.0, turns=0, Rmax=0.0,
                        Kmax=0.0, kang_max=0.0, Kloc=0.0, vbar_min=0.0,
                        vbar_max=0.0, coef=[0.0] * 7), None
        phi = np.tile(vr[:, None], (1, Nth))
    if seed_amp != 0.0:
        costh = np.cos(th)
        Pl = np.polynomial.legendre.legval(
            costh, [0] * seed_lobe + [1])[None, :]
        rb = (r - r_in)[:, None] / (r_star - r_in)
        bump = np.exp(-((rb - 0.5) / 0.22) ** 2)
        phi = phi + seed_amp * bump * Pl
    phi, maxres, nit, conv, hist, J = newton2d(
        phi, r, th, dr, dth, D, Phi_amp)
    # ---- invariants (sin-theta weighted theta average) ----
    wth = np.sin(th); wth = wth / wth.sum()
    vbar = phi @ wth                       # <phi>_theta(r)
    th_var = float(np.max(np.std(phi, axis=1)))
    # dominant angular harmonic at the most-varying radius
    ir = int(np.argmax(np.std(phi, axis=1)))
    prof = phi[ir] - phi[ir].mean()
    x = np.cos(th)
    B = np.stack([np.polynomial.legendre.legval(x, [0] * l + [1])
                  for l in range(7)], axis=1)
    Wd = np.diag(np.sin(th))
    coef, *_ = np.linalg.lstsq(B.T @ Wd @ B, B.T @ Wd @ prof, rcond=None)
    dom_l = int(np.argmax(np.abs(coef[1:])) + 1) if th_var > 1e-9 else 0
    # Misner-Sharp at the interface r*:  X = 1 - e^{-2 <phi(r*)>}
    X_star = float(1 - np.exp(-2 * vbar[-1]))   # =0 by BC (interface phi=0)
    # the MS mass profile and its MAX (the cell's gravitating content):
    ms_prof = 0.5 * r * (1 - np.exp(-2 * vbar))   # = G m / c^2 (geom units)
    ms_max = float(np.max(ms_prof))
    # compactness of the FILLED cell: 2Gm/(c^2 r) along the profile, max
    comp_prof = 1 - np.exp(-2 * vbar)
    comp_max = float(np.max(comp_prof))
    # seal proximity: f_core = min_theta e^{-2 phi(r_in)}
    f_core = float(np.min(np.exp(-2 * phi[0, :])))
    # does <phi> have a radial TURN (a lump interior) vs monotone ramp?
    dvbar = np.diff(vbar)
    turns = int(np.sum(np.diff(np.sign(dvbar + 1e-30)) != 0))
    R_Ric, K, k_ang = curvature_diag(phi, r, th, dr, dth)
    Rmax = float(np.nanmax(np.abs(R_Ric[1:-1, 1:-1])))
    Kmax = float(np.nanmax(np.abs(K[1:-1, 1:-1])))
    kang_max = float(np.nanmax(np.abs(k_ang[1:-1, 1:-1])))
    # where curvature concentrates (radial index of K max, 0=core .. 1=intf)
    iK = int(np.unravel_index(np.nanargmax(np.abs(K[1:-1, 1:-1])),
                              K[1:-1, 1:-1].shape)[0]) + 1
    Kloc = float(iK / (Nr - 1))
    out = dict(r_in=r_in, r_star=r_star, D=D, Phi=Phi_amp,
               seed_lobe=seed_lobe, seed_amp=seed_amp, Nr=Nr, Nth=Nth,
               conv=bool(conv), exists=True, maxres=maxres, nit=nit,
               th_var=th_var, dom_l=dom_l, X_star=X_star,
               ms_max=ms_max, comp_max=comp_max, f_core=f_core,
               turns=turns, Rmax=Rmax, Kmax=Kmax, kang_max=kang_max,
               Kloc=Kloc, vbar_min=float(vbar.min()),
               vbar_max=float(vbar.max()),
               coef=[float(c) for c in coef])
    return out, phi

# Jacobian min|eig| (existence / bifurcation test) -- reuse the assembled J.
def min_eig(phi, r, th, dr, dth, D, Phi_amp):
    J, _ = jacobian_np(phi, r, th, dr, dth, D, Phi_amp)
    Jd = J.toarray()
    ev = np.linalg.eigvals(Jd)
    i0 = int(np.argmin(np.abs(ev)))
    allpos = bool(np.all(ev.real > 1e-9)); allneg = bool(np.all(ev.real < -1e-9))
    sign = "+" if allpos else ("-" if allneg else "mix")
    return float(abs(ev[i0])), sign


# =====================================================================
# DRIVER: the (r*, D) plane, continuation in D, seeds round+lobed, dual-grid.
# =====================================================================
def _depth_continuation(args):
    """One r* column: warm-started continuation up in depth D, round seed.
    Returns the list of round-cell records (the backbone of the map)."""
    r_in, r_star, Phi, Dlist = args
    recs = []; warm = None
    for D in Dlist:
        rec, phi = solve_point(r_in, r_star, D, Phi, seed_amp=0.0, warm=warm)
        recs.append(rec)
        if rec["conv"]:
            warm = phi
        else:
            warm = None   # lost the cell; reseed next depth
    return recs

def main():
    log("=" * 74)
    log("sweep_whole_metric -- the (r*, depth) plane, both sectors live")
    log("=" * 74)
    Phi = 1.0
    r_in = 1.0
    # r* across DECADES (the cell size); r_in fixed at 1 (the core radius),
    # so r*/r_in spans the cell aspect from ~thin to ~3 decades.
    r_stars = [1.5, 2.0, 3.0, 5.0, 10.0, 30.0, 100.0, 300.0, 1000.0]
    # depth D (core matter content): from shallow to deep-toward-seal.
    Dlist = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0]

    # -------- BACKBONE: round-cell continuation over the whole plane --------
    log("\n[1] ROUND-CELL BACKBONE: continuation in depth across r* decades")
    log(f"{'r*':>7} {'D':>6} {'conv':>5} {'maxres':>9} {'f_core':>10} "
        f"{'comp':>7} {'ms_max':>9} {'turns':>5} {'Kmax':>10} {'Kloc':>5} "
        f"{'th_var':>9}")
    jobs = [(r_in, rs, Phi, Dlist) for rs in r_stars]
    with Pool(min(len(jobs), os.cpu_count())) as pool:
        cols = pool.map(_depth_continuation, jobs)
    BACK = []
    for col in cols:
        for rec in col:
            BACK.append(rec)
            log(f"{rec['r_star']:7.1f} {rec['D']:6.2f} "
                f"{str(rec['conv']):>5} {rec['maxres']:9.1e} "
                f"{rec['f_core']:10.2e} {rec['comp_max']:7.4f} "
                f"{rec['ms_max']:9.3f} {rec['turns']:5d} "
                f"{rec['Kmax']:10.2e} {rec['Kloc']:5.2f} "
                f"{rec['th_var']:9.1e}")
    json.dump(BACK, open("/tmp/sweep_backbone.json", "w"))

    # -------- FORM/UNFORM LOCUS: the deepest convergent D at each r* -------
    log("\n[2] FORM/UNFORM CRITICAL LOCUS: deepest convergent depth per r*")
    log(f"{'r*':>7} {'D_max_conv':>10} {'f_core@max':>11} {'comp@max':>9} "
        f"{'next_D_fails':>12}")
    locus = []
    for col in cols:
        conv = [r for r in col if r["conv"]]
        if not conv:
            log(f"{col[0]['r_star']:7.1f}   (no convergent depth)")
            continue
        Dmax = max(c["D"] for c in conv)
        rec = [c for c in conv if c["D"] == Dmax][0]
        nxt = [c for c in col if c["D"] > Dmax]
        nd = nxt[0]["D"] if nxt else None
        locus.append((rec["r_star"], Dmax, rec["f_core"], rec["comp_max"], nd))
        log(f"{rec['r_star']:7.1f} {Dmax:10.2f} {rec['f_core']:11.2e} "
            f"{rec['comp_max']:9.4f} {str(nd):>12}")
    json.dump(locus, open("/tmp/sweep_locus.json", "w"))

    # -------- ANGULAR PERSISTENCE: seed lobes l=1..4 across the plane ------
    log("\n[3] ANGULAR PERSISTENCE: seed Legendre l=1..4 (amp 0.3) at "
        "representative (r*,D); does any lobe PERSIST (th_var>1e-4)?")
    log(f"{'r*':>7} {'D':>6} {'lobe':>5} {'conv':>5} {'th_var':>10} "
        f"{'dom_l':>5} {'maxres':>9}")
    ang = []
    ang_pts = [(2.0, 1.0), (2.0, 3.0), (3.0, 2.0), (5.0, 3.0),
               (10.0, 4.0), (30.0, 5.0), (100.0, 6.0)]
    ajobs = []
    for (rs, D) in ang_pts:
        for lobe in [1, 2, 3, 4]:
            ajobs.append((r_in, rs, D, Phi, lobe))
    def _ang(a):
        r_in_, rs_, D_, Phi_, lobe_ = a
        rec, _ = solve_point(r_in_, rs_, D_, Phi_, seed_lobe=lobe_,
                             seed_amp=0.3)
        return rec
    with Pool(min(len(ajobs), os.cpu_count())) as pool:
        arecs = pool.map(_ang, ajobs)
    for rec in arecs:
        ang.append(rec)
        log(f"{rec['r_star']:7.1f} {rec['D']:6.2f} {rec['seed_lobe']:5d} "
            f"{str(rec['conv']):>5} {rec['th_var']:10.2e} "
            f"{rec['dom_l']:5d} {rec['maxres']:9.1e}")
    persisted = [a for a in ang if a["conv"] and a["th_var"] > 1e-4]
    log(f"\n  lobed solves converged: {sum(1 for a in ang if a['conv'])}/"
        f"{len(ang)}; PERSISTENT angular (th_var>1e-4): {len(persisted)}")
    json.dump(ang, open("/tmp/sweep_angular.json", "w"))

    # -------- EXISTENCE / BIFURCATION: Jacobian min|eig| over the plane ----
    log("\n[4] EXISTENCE TEST: round-cell Jacobian min|eig| over (r*,D) "
        "(a zero eig = a shaped type is born = bifurcation)")
    log(f"{'r*':>7} {'D':>6} {'conv':>5} {'min|eig|':>11} {'sign':>5}")
    eigs = []
    epts = [(2.0, d) for d in [0.5, 1.0, 2.0, 3.0, 4.0]] + \
           [(rs, 2.0) for rs in [3.0, 10.0, 100.0, 1000.0]]
    for (rs, D) in epts:
        rec, phi = solve_point(r_in, rs, D, Phi, seed_amp=0.0, Nr=97, Nth=33)
        if not rec["conv"]:
            log(f"{rs:7.1f} {D:6.2f} {'F':>5}     (no cell)")
            continue
        r = np.linspace(r_in, rs, 97); th = np.linspace(0, np.pi, 33)
        me, sign = min_eig(phi, r, th, r[1] - r[0], th[1] - th[0], D, Phi)
        eigs.append((rs, D, me, sign))
        log(f"{rs:7.1f} {D:6.2f} {'T':>5} {me:11.5f} {sign:>5}")
    json.dump(eigs, open("/tmp/sweep_eigs.json", "w"))

    # -------- GRID INDEPENDENCE: edge-vs-structure at near-seal points -----
    log("\n[5] GRID INDEPENDENCE (edge vs structure): dual-grid at the "
        "deepest convergent points (does the result move under refinement?)")
    log(f"{'r*':>7} {'D':>6} {'grid':>10} {'conv':>5} {'comp':>7} "
        f"{'f_core':>10} {'th_var':>9} {'Kloc':>5}")
    gi = []
    # pick the deepest convergent (r*,D) from a few columns
    gpts = []
    for col in cols:
        conv = [r for r in col if r["conv"]]
        if conv:
            Dmax = max(c["D"] for c in conv)
            gpts.append((col[0]["r_star"], Dmax))
    gpts = gpts[:5]
    for (rs, D) in gpts:
        row = []
        for (Nr, Nth) in [(161, 49), (321, 97)]:
            rec, _ = solve_point(r_in, rs, D, Phi, seed_amp=0.0,
                                 Nr=Nr, Nth=Nth)
            row.append(rec)
            log(f"{rs:7.1f} {D:6.2f} {f'{Nr}x{Nth}':>10} "
                f"{str(rec['conv']):>5} {rec['comp_max']:7.4f} "
                f"{rec['f_core']:10.2e} {rec['th_var']:9.1e} "
                f"{rec['Kloc']:5.2f}")
        gi.append([row[0], row[1]])
    json.dump(gi, open("/tmp/sweep_grid.json", "w"))

    log(f"\nDONE ({time.time()-t0:.0f}s). checkpoints in /tmp/sweep_*.json  "
        "log /tmp/sweep.log")
    return BACK, locus, ang, eigs, gi


if __name__ == "__main__":
    main()
    _fh.close()
