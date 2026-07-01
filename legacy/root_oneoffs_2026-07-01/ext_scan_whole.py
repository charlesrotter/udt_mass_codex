#!/usr/bin/env python3
"""
ext_scan_whole.py -- THE EXTERIOR / MEDIUM SIDE OF THE WHOLE METRIC
===================================================================
OPEN-ENDED METRIC-LED exploration (HANDOFF queue head, step b, EXTERIOR
axis). Driver: Claude (Opus 4.8, 1M). Date 2026-06-13. Frame:
CRITICAL_UNIVERSE_FRAME.md. New file (repo discipline; ext_scan_* only).
Reuses the metric's OWN derived operators from wint_solve2d.py /
wint_cell2d.py (the dilation-weighted box + the derived ON source +
the derived e^{2phi}-dressed angular nonlinearity). Adds NOTHING,
slaves NOTHING, freezes NOTHING. Both sectors LIVE on the EXTERIOR.

CONVENTION (banked): f = e^{-2 phi}.
  - matter-cell INTERIOR: f < 1  =>  phi > 0  (#34/#36 = pure damping
    PROVEN ABOUT ROUND, zero gradient).
  - EXTERIOR / universe-side MEDIUM: f > 1  =>  phi < 0. This is a
    DIFFERENT regime. The prior exterior doc banked the FORMATION law
    c*=chat*gamma^2 (chat=0.498912, formed depth DIVERGES at threshold)
    and a SHUT linear-binding window (E0>0 global, repulsive kernel) --
    but BOTH were computed on a SMOOTH/MIRRORED background or in the
    1D radial connection problem. The medium's defining feature is its
    intrinsic MONOPOLE GRADIENT gamma (the dilation gradient that shapes
    cells). The #34/#36 "pure damping" theorem is ABOUT ROUND (zero
    gradient). NOBODY HAS TESTED the angular stiffness sign on a
    GRADIENT-CARRYING exterior background with both sectors live.

THE BASELINE (documented; departures from THIS are candidates):
  B1. interior round cell = ONE TYPE, smooth E-continuum (#33/#34).
  B2. angular sector = PURE DAMPING about round: linearize -v_th^2
      about round (v_th=0) => 0; angular gap POSITIVE (#36).
  B3. exterior formation threshold c*=chat gamma^2, formed depth
      diverges at threshold (exterior_cavity).
  B4. linear-binding window SHUT: E0>0 global, dressed kernel
      repulsive (exterior_cavity, theorem-grade on mirror background).
  B5. cohomological area form / exact transgression at the seal (#36);
      absolute scale-free (#32).

WHAT THIS SCANS (exterior, undocumented axes):
  PART A. The exterior whole-metric solution map: solve Box_g phi=S(phi)
     with BOTH sectors live on the EXTERIOR domain (phi<0, f>1), sweep
     the medium gradient (boundary depths spanning the f>1 region) and
     angular seeds. Map turns, theta-variation, MS aspect.
  PART B. THE ANGULAR-STIFFNESS SIGN ON A GRADIENT BACKGROUND (the
     genuine departure from B2). The #36 damping theorem linearized the
     angular nonlinearity -e^{2v} v_th^2 ABOUT ROUND. On the exterior
     the background carries a live RADIAL gradient phi_r != 0 AND, near
     the cell-medium interface, an ANGULAR gradient. Compute the angular
     Jacobian (the second variation of the whole-metric angular operator)
     about the SELF-CONSISTENT exterior background and read its smallest
     eigenvalue's SIGN across the medium-gradient sweep. A SIGN CHANGE =
     the exterior medium destabilizes the round shape = a NEW TYPE born
     in the medium that the interior damps away. (B2 says interior gap
     is positive; the question is whether the EXTERIOR gap stays positive
     as the medium gradient grows toward the formation threshold.)
  PART C. THE THRESHOLD c*=chat gamma^2 AS A PHASE BOUNDARY. The prior
     doc banked formed depth DIVERGING at c*. Map the invariants
     (compactness X, MS aspect, angular gap) as the configuration is
     driven toward and (where solvable) ACROSS the threshold. Does the
     character change at c* -- continuum vs pinned, gap sign, turn count?

DISCIPLINE: EXPLORATION, not mass-matching. No lepton-wall comparison.
No interior retreat. Native verbs. Convergence evidence mandatory.
Honest negative reporting first-class. Each flagged anomaly self-graded
real / artifact / documented.

GPU: V100 torch float64 for the eigen-sweeps; numpy/scipy Newton for the
nonlinear solves (same machinery as wint_solve2d, robust). Log
/tmp/ext_scan.log (flush per line).
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
import torch

torch.set_default_dtype(torch.float64)
DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
t0 = time.time()
_fh = open("/tmp/ext_scan.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
FLAG = []
def flag(tag, what, evidence, grade):
    FLAG.append((tag, what, evidence, grade))
    log(f"  *** FLAG {tag}: {what}")
    log(f"      evidence: {evidence}")
    log(f"      self-grade: {grade}")

log("=" * 72)
log(f"ext_scan_whole -- EXTERIOR/MEDIUM whole-metric  device={DEV}")
log(f"torch={torch.__version__}")
log("=" * 72)

# =====================================================================
# The metric's OWN operators (TAKEN verbatim from wint_solve2d, numpy
# engine; NOTHING added). Box_g phi = dilation-weighted 2D Laplacian;
# S(phi)=Phi(e^{-2phi}-e^{phi}) the derived ON source.
# =====================================================================
def _box_np(phi, r, th, dr, dth):
    w = np.exp(-2.0 * phi)
    R = r[:, None]; sinth = np.sin(th)[None, :]
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

def _residual_np(phi, r, th, dr, dth, Din, Dout, Phi_amp, inner='dir'):
    """Exterior closure: the MEDIUM is the f>1 region BETWEEN the
    cell-medium interface (inner, at smaller r, the cell side, depth Din)
    and the universe-side (outer, depth Dout). Both Dirichlet = the medium
    is DRIVEN by its two boundaries (the gradient is the medium's defining
    content -- the monopole dilation gradient gamma is Din-Dout over the
    span). Axis Neumann in theta. inner='neu' option = mirror-parity inner.
    """
    Nr, Nth = phi.shape
    F = _box_np(phi, r, th, dr, dth) - Phi_amp * (np.exp(-2 * phi)
                                                  - np.exp(phi))
    if inner == 'dir':
        F[0, :] = phi[0, :] - Din
    else:
        F[0, :] = phi[0, :] - phi[1, :]
    F[-1, :] = phi[-1, :] - Dout
    F[:, 0] = phi[:, 0] - phi[:, 1]
    F[:, -1] = phi[:, -1] - phi[:, -2]
    return F

def _jacobian_np(phi, r, th, dr, dth, Din, Dout, Phi_amp, inner='dir',
                 eps=1e-7):
    Nr, Nth = phi.shape; N = Nr * Nth
    F0 = _residual_np(phi, r, th, dr, dth, Din, Dout, Phi_amp, inner).ravel()
    idx = np.arange(N).reshape(Nr, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nr, Nth), dtype=bool)
            mask[ci::3, cj::3] = True
            ph = phi.copy(); ph[mask] += eps
            dF = ((_residual_np(ph, r, th, dr, dth, Din, Dout, Phi_amp,
                                inner).ravel() - F0) / eps).reshape(Nr, Nth)
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
            sel = owner >= 0; vv = dF[sel]; nz = vv != 0.0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz])
            vals.append(vv[nz])
    J = sps.csr_matrix((np.concatenate(vals),
                        (np.concatenate(rows), np.concatenate(cols))),
                       shape=(N, N))
    return J, F0

def _newton(phi0, r, th, dr, dth, Din, Dout, Phi_amp, inner='dir',
            itmax=200, tol=1e-11, verbose=False):
    phi = phi0.copy(); Nr, Nth = phi.shape; maxres = np.inf; hist = []
    for nit in range(itmax):
        J, F0 = _jacobian_np(phi, r, th, dr, dth, Din, Dout, Phi_amp, inner)
        nF0 = float(np.linalg.norm(F0))
        try:
            dphi = spsla.spsolve(J, -F0).reshape(Nr, Nth)
        except Exception:
            return phi, maxres, nit, False, hist
        if not np.all(np.isfinite(dphi)):
            return phi, maxres, nit, False, hist
        lam = 1.0; ok = False
        for _ in range(50):
            trial = phi + lam * dphi
            if np.all(np.abs(trial) < 60):
                Ft = _residual_np(trial, r, th, dr, dth, Din, Dout,
                                  Phi_amp, inner)
                if np.isfinite(Ft).all() and \
                        np.linalg.norm(Ft) < (1 - 1e-4 * lam) * nF0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            maxres = float(np.max(np.abs(_residual_np(
                phi, r, th, dr, dth, Din, Dout, Phi_amp, inner)[2:-2, 2:-2])))
            return phi, maxres, nit, maxres < 1e-8, hist
        phi = phi + lam * dphi
        maxres = float(np.max(np.abs(_residual_np(
            phi, r, th, dr, dth, Din, Dout, Phi_amp, inner)[2:-2, 2:-2])))
        hist.append((nit, float(lam), maxres))
        if verbose: log(f"    it={nit} lam={lam:.3f} res={maxres:.2e}")
        if maxres < tol:
            return phi, maxres, nit + 1, True, hist
    return phi, maxres, itmax, maxres < 1e-8, hist


def solve_ext(Din, Dout, Phi_amp, seed_lobe=0, seed_amp=0.0,
              r_in=1.0, r_star=6.0, Nr=193, Nth=97, inner='dir',
              verbose=False):
    """Solve the WHOLE metric on the EXTERIOR/medium domain. The medium is
    the f>1 region driven by inner depth Din (cell-interface side) and
    outer depth Dout (universe side). Both sectors live: angular seeded
    by seed_lobe/seed_amp (INITIAL data only; solver settles freely)."""
    r = np.linspace(r_in, r_star, Nr)
    th = np.linspace(0.0, np.pi, Nth)
    dr = r[1] - r[0]; dth = th[1] - th[0]
    # initial data: linear ramp Din->Dout across the medium + optional lobe
    ramp = np.linspace(Din, Dout, Nr)[:, None]
    phi = np.tile(ramp, (1, Nth))
    if seed_amp != 0.0:
        x = np.cos(th)
        Pl = np.polynomial.legendre.legval(x, [0] * seed_lobe + [1])[None, :]
        rb = (r[:, None] - r_in) / (r_star - r_in)
        bump = np.exp(-((rb - 0.4) / 0.2) ** 2)
        phi = phi + seed_amp * bump * Pl
    phi, maxres, nit, conv, hist = _newton(
        phi, r, th, dr, dth, Din, Dout, Phi_amp, inner, verbose=verbose)
    wth = np.sin(th); wth = wth / wth.sum()
    phibar = phi @ wth
    msr = 0.5 * r * (1.0 - np.exp(-2.0 * phibar))
    dphi = np.gradient(phibar, r)
    turns = int(np.sum(np.diff(np.sign(dphi)) != 0))
    th_var = float(np.max(np.std(phi, axis=1)))
    ir = int(np.argmax(np.std(phi, axis=1)))
    prof = phi[ir] - phi[ir].mean()
    x = np.cos(th)
    B = np.stack([np.polynomial.legendre.legval(x, [0] * l + [1])
                  for l in range(7)], axis=1)
    Wd = np.diag(np.sin(th))
    coef, *_ = np.linalg.lstsq(B.T @ Wd @ B, B.T @ Wd @ prof, rcond=None)
    dom_l = int(np.argmax(np.abs(coef[1:])) + 1) if th_var > 1e-9 else 0
    # f>1 fraction: where phi<0 (f=e^{-2phi}>1)
    fgt1 = float(np.mean(phibar < 0.0))
    Xc = float(np.max(np.abs(1 - np.exp(-2 * phibar))))   # compactness reach
    return dict(Din=Din, Dout=Dout, Phi=Phi_amp, seed_lobe=seed_lobe,
                seed_amp=seed_amp, conv=conv, maxres=maxres, nit=nit,
                turns=turns, th_var=th_var, dom_l=dom_l, fgt1=fgt1, Xc=Xc,
                phibar_in=float(phibar[0]), phibar_out=float(phibar[-1]),
                phibar_min=float(phibar.min()), phibar_max=float(phibar.max()),
                ms_out=float(msr[-1]), ms_max=float(np.max(np.abs(msr))),
                coef=[float(c) for c in coef], inner=inner,
                phi=phi, r=r, th=th, phibar=phibar, dr=dr, dth=dth)


def angular_gap(phi, r, th, dr, dth, Din, Dout, Phi_amp, inner='dir',
                k=6):
    """THE KEY DIAGNOSTIC (PART B). The smallest-magnitude eigenvalues of
    the whole-metric Jacobian about the converged EXTERIOR background,
    RESTRICTED to angular (theta-dependent, l>=1) perturbations -- i.e.
    the second variation of the metric's own e^{2phi}-dressed angular
    operator INCLUDING the -e^{2phi} v_th^2 nonlinearity, linearized about
    the GRADIENT-CARRYING exterior background (NOT about round).
    A NEGATIVE eigenvalue with an l>=1 eigenvector = the round shape is
    UNSTABLE in the medium = a NEW (shaped) type is born. B2 says this gap
    is POSITIVE about round; here we read its sign on the EXTERIOR.
    Uses torch on GPU for the dense eigensolve of the interior block."""
    J, _ = _jacobian_np(phi, r, th, dr, dth, Din, Dout, Phi_amp, inner)
    Nr, Nth = phi.shape
    Jd = torch.tensor(J.toarray(), device=DEV)
    # symmetrize for a real spectrum read (the FD Jacobian is nearly sym;
    # we read the symmetric part's spectrum = the second-variation form).
    Js = 0.5 * (Jd + Jd.T)
    ev = torch.linalg.eigvalsh(Js).cpu().numpy()
    # the angular gap: we want the eigenvalues whose eigenvectors carry
    # l>=1 angular content. Compute the full spectrum (interior is modest)
    # and ALSO project: identify the smallest eigenvalue whose eigenvector
    # has nonzero theta-variation.
    evals, evecs = torch.linalg.eigh(Js)
    evals = evals.cpu().numpy(); evecs = evecs.cpu().numpy()
    # angular content of each eigenvector (std over theta, averaged over r)
    ang_content = []
    for i in range(evecs.shape[1]):
        V = evecs[:, i].reshape(Nr, Nth)
        ang_content.append(float(np.mean(np.std(V[2:-2, 2:-2], axis=1))))
    ang_content = np.array(ang_content)
    # eigenvalues with substantial angular content
    is_ang = ang_content > 0.3 * ang_content.max() if ang_content.max() > 0 \
        else np.zeros(len(evals), dtype=bool)
    ang_evals = evals[is_ang]
    # the angular gap = the angular eigenvalue closest to zero (its SIGN
    # decides stability of the round shape on this background)
    if len(ang_evals):
        i_gap = int(np.argmin(np.abs(ang_evals)))
        gap = float(ang_evals[i_gap])
        # most-negative angular eigenvalue (the strongest instability if any)
        gap_neg = float(np.min(ang_evals))
    else:
        gap = float(evals[np.argmin(np.abs(evals))]); gap_neg = gap
    return dict(gap=gap, gap_neg=gap_neg, ev_min=float(evals.min()),
                ev_absmin=float(evals[np.argmin(np.abs(evals))]),
                n_neg=int(np.sum(evals < -1e-9)),
                n_ang=int(is_ang.sum()))


# =====================================================================
# PART A -- the exterior whole-metric solution map.
# =====================================================================
def part_A():
    log("\n" + "=" * 72)
    log("PART A -- EXTERIOR whole-metric solution map (both sectors live)")
    log("Convention f=e^{-2phi}; EXTERIOR=f>1=phi<0. Medium driven by")
    log("inner depth Din (cell side) & outer Dout (universe side); the")
    log("MEDIUM GRADIENT gamma ~ (Dout-Din)/span is the medium's content.")
    log("=" * 72)
    log(f"{'Din':>6} {'Dout':>6} {'Phi':>5} {'s_l':>4} {'s_a':>6} {'conv':>5} "
        f"{'maxres':>9} {'turns':>5} {'th_var':>9} {'dom_l':>4} {'fgt1':>5} "
        f"{'Xc':>7} {'ms_out':>8}")
    RES = []
    # sweep the EXTERIOR: phi<0 boundaries (f>1). Din near 0 (interface,
    # f~1), Dout < 0 (deep medium, f>1) AND Dout>0 cases for contrast.
    # The medium gradient grows as |Dout-Din| grows.
    for Din in [0.0, -0.2, -0.5]:
        for Dout in [-0.2, -0.5, -1.0, -2.0]:
            for Phi in [0.0, 0.3, 1.0, 3.0]:
                for (sl, sa) in [(0, 0.0), (1, 0.15), (2, 0.15)]:
                    r = solve_ext(Din, Dout, Phi, seed_lobe=sl, seed_amp=sa)
                    rec = {k: r[k] for k in
                           ("Din", "Dout", "Phi", "seed_lobe", "seed_amp",
                            "conv", "maxres", "turns", "th_var", "dom_l",
                            "fgt1", "Xc", "ms_out", "phibar_min",
                            "phibar_max", "coef")}
                    RES.append(rec)
                    log(f"{Din:6.2f} {Dout:6.2f} {Phi:5.1f} {sl:4d} {sa:6.2f} "
                        f"{str(r['conv']):>5} {r['maxres']:9.1e} "
                        f"{r['turns']:5d} {r['th_var']:9.2e} {r['dom_l']:4d} "
                        f"{r['fgt1']:5.2f} {r['Xc']:7.3f} {r['ms_out']:8.4f}")
            with open("/tmp/ext_scan_A.json", "w") as fh:
                json.dump(RES, fh, indent=0)
    nconv = sum(1 for x in RES if x["conv"])
    log(f"\n  PART A: {nconv}/{len(RES)} exterior solves converged.")
    # departure check: any persistent angular structure (th_var large)?
    pers = [x for x in RES if x["conv"] and x["seed_amp"] > 0
            and x["th_var"] > 1e-4]
    log(f"  exterior solves with PERSISTENT angular structure "
        f"(th_var>1e-4): {len(pers)}")
    if pers:
        for x in pers[:8]:
            log(f"    Din={x['Din']} Dout={x['Dout']} Phi={x['Phi']} "
                f"seed_l={x['seed_lobe']} th_var={x['th_var']:.3e} "
                f"dom_l={x['dom_l']}")
        flag("A-PERSIST",
             "exterior angular structure PERSISTS (interior damps it, #34)",
             f"{len(pers)} converged exterior solves keep th_var>1e-4 from "
             "a lobed seed; interior baseline relaxes to th_var<1e-7",
             "candidate -- verify vs grid artifact in PART B (gap sign)")
    else:
        log("  -> exterior also relaxes lobed seeds to round (B2-consistent "
            "at the seed level; the decisive test is the GAP SIGN, PART B).")
    return RES


# =====================================================================
# PART B -- the angular-stiffness sign on the gradient-carrying exterior.
# THE GENUINE DEPARTURE FROM B2 (which proved the gap positive ABOUT ROUND).
# =====================================================================
def part_B():
    log("\n" + "=" * 72)
    log("PART B -- ANGULAR-STIFFNESS SIGN on the GRADIENT-carrying EXTERIOR")
    log("B2 proved the angular gap POSITIVE about ROUND (zero gradient).")
    log("Here: read the gap SIGN about the SELF-CONSISTENT exterior")
    log("background as the medium gradient grows. A SIGN FLIP = a shaped")
    log("type born in the medium that the interior damps away.")
    log("=" * 72)
    log(f"{'Din':>6} {'Dout':>6} {'Phi':>5} {'grad':>7} {'conv':>5} "
        f"{'ang_gap':>11} {'gap_neg':>11} {'n_neg':>6} {'n_ang':>6} "
        f"{'sign':>5}")
    REC = []
    # CONTROL first: interior (phi>0) round background, gap should be > 0.
    log("  -- CONTROL (interior, phi>0, near-round): expect gap > 0 (B2)")
    rc = solve_ext(Din=0.5, Dout=0.5, Phi_amp=1.0, seed_amp=0.0,
                   inner='dir')
    if rc["conv"]:
        gc = angular_gap(rc["phi"], rc["r"], rc["th"], rc["dr"], rc["dth"],
                         0.5, 0.5, 1.0, 'dir')
        log(f"  CONTROL interior flat phi=0.5: ang_gap={gc['gap']:.4e} "
            f"gap_neg={gc['gap_neg']:.4e} n_neg={gc['n_neg']} "
            f"n_ang={gc['n_ang']}")
    # EXTERIOR sweep: drive the medium gradient.
    for Din in [0.0, -0.2, -0.5]:
        for Dout in [-0.5, -1.0, -2.0, -3.0]:
            for Phi in [0.0, 1.0, 3.0]:
                r = solve_ext(Din, Dout, Phi, seed_amp=0.0)
                if not r["conv"]:
                    log(f"{Din:6.2f} {Dout:6.2f} {Phi:5.1f} "
                        f"{(Dout-Din)/5.0:7.3f}  FAIL (no convergence)")
                    continue
                g = angular_gap(r["phi"], r["r"], r["th"], r["dr"], r["dth"],
                                Din, Dout, Phi, 'dir')
                grad = (Dout - Din) / (r["r"][-1] - r["r"][0])
                sign = "+" if g["gap"] > 1e-9 else ("-" if g["gap"] < -1e-9
                                                    else "0")
                REC.append(dict(Din=Din, Dout=Dout, Phi=Phi, grad=grad,
                                **{k: g[k] for k in g}))
                log(f"{Din:6.2f} {Dout:6.2f} {Phi:5.1f} {grad:7.3f} "
                    f"{str(r['conv']):>5} {g['gap']:11.4e} "
                    f"{g['gap_neg']:11.4e} {g['n_neg']:6d} {g['n_ang']:6d} "
                    f"{sign:>5}")
        with open("/tmp/ext_scan_B.json", "w") as fh:
            json.dump([{k: v for k, v in d.items()} for d in REC],
                      fh, indent=0)
    # verdict
    neg = [d for d in REC if d["gap"] < -1e-7]
    negstrong = [d for d in REC if d["gap_neg"] < -1e-6]
    if neg:
        flag("B-GAPFLIP",
             "the angular gap goes NEGATIVE on the exterior (B2 holds only "
             "about round; the medium gradient destabilizes the round shape)",
             f"{len(neg)} exterior backgrounds with ang_gap<0; "
             f"min ang_gap={min(d['gap'] for d in REC):.4e}",
             "candidate -- MUST verify vs FD-Jacobian artifact (closure-row "
             "eigenvalues) and grid refinement in PART D")
    elif negstrong:
        flag("B-NEGANG",
             "some angular eigenvalues negative though the gap-to-zero is "
             "positive (mixed angular spectrum on the exterior)",
             f"{len(negstrong)} backgrounds with a negative angular "
             f"eigenvalue; most-negative={min(d['gap_neg'] for d in REC):.4e}",
             "candidate -- check whether these are closure-row artifacts")
    else:
        log("\n  -> PART B: angular gap stays POSITIVE across the exterior "
            "medium-gradient sweep. B2 (pure damping) EXTENDS to the "
            "gradient-carrying exterior. No shaped type born in the medium.")
    return REC


# =====================================================================
# PART C -- the formation threshold c*=chat gamma^2 as a phase boundary.
# Map invariants as the configuration is driven toward larger medium
# gradient (the analog of approaching the threshold). Does CHARACTER
# change -- compactness continuum vs a pinned value, turn count, gap sign?
# =====================================================================
def part_C():
    log("\n" + "=" * 72)
    log("PART C -- THRESHOLD as a PHASE BOUNDARY: invariants vs medium")
    log("gradient. Prior doc: formed depth DIVERGES at c*=chat gamma^2.")
    log("Map compactness Xc, ms_out, turns, ang_gap as |grad| grows;")
    log("look for a character change (pinning, divergence, sign flip).")
    log("=" * 72)
    log(f"{'Dout':>7} {'grad':>7} {'conv':>5} {'maxres':>9} {'Xc':>8} "
        f"{'ms_out':>9} {'ms_max':>9} {'turns':>5} {'fgt1':>5} "
        f"{'ang_gap':>11}")
    REC = []
    Din = 0.0
    # drive the universe-side deeper and deeper into f>1 (the medium
    # gradient = the analog of the driving gamma); finer near large grad.
    for Dout in [-0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -4.0, -5.0, -6.0,
                 -8.0, -10.0]:
        r = solve_ext(Din, Dout, Phi_amp=1.0, seed_amp=0.0, Nr=257, Nth=97)
        grad = (Dout - Din) / (r["r"][-1] - r["r"][0])
        if not r["conv"]:
            log(f"{Dout:7.2f} {grad:7.3f}  FAIL maxres={r['maxres']:.2e}")
            continue
        g = angular_gap(r["phi"], r["r"], r["th"], r["dr"], r["dth"],
                        Din, Dout, 1.0, 'dir')
        REC.append(dict(Dout=Dout, grad=grad, Xc=r["Xc"], ms_out=r["ms_out"],
                        ms_max=r["ms_max"], turns=r["turns"], fgt1=r["fgt1"],
                        ang_gap=g["gap"], gap_neg=g["gap_neg"],
                        maxres=r["maxres"]))
        log(f"{Dout:7.2f} {grad:7.3f} {str(r['conv']):>5} "
            f"{r['maxres']:9.1e} {r['Xc']:8.4f} {r['ms_out']:9.4f} "
            f"{r['ms_max']:9.4f} {r['turns']:5d} {r['fgt1']:5.2f} "
            f"{g['gap']:11.4e}")
    with open("/tmp/ext_scan_C.json", "w") as fh:
        json.dump(REC, fh, indent=0)
    # is the compactness a CONTINUUM (B-consistent) or does it PIN/saturate?
    if len(REC) >= 4:
        Xs = [d["Xc"] for d in REC]
        # monotone & non-saturating => continuum; plateau => pinning
        dX = [Xs[i + 1] - Xs[i] for i in range(len(Xs) - 1)]
        log(f"\n  Xc sequence: {['%.4f' % x for x in Xs]}")
        log(f"  dXc steps:   {['%.4f' % d for d in dX]}")
        gaps = [d["ang_gap"] for d in REC]
        log(f"  ang_gap seq: {['%.3e' % gg for gg in gaps]}")
        # ms divergence?
        ms = [d["ms_max"] for d in REC]
        log(f"  ms_max seq:  {['%.3f' % m for m in ms]}")
        # character-change tests
        signflip = any(gaps[i] * gaps[i + 1] < 0 for i in range(len(gaps) - 1))
        if signflip:
            flag("C-GAPSIGN",
                 "the angular gap CHANGES SIGN as the medium gradient grows",
                 f"ang_gap sequence crosses zero: {['%.2e'%g for g in gaps]}",
                 "candidate -- verify in PART D (refinement + closure check)")
        # turn count change = new radial structure (a lump appearing)
        turns = [d["turns"] for d in REC]
        if len(set(turns)) > 1:
            flag("C-TURNS",
                 "the radial turn count CHANGES across the gradient sweep "
                 "(new radial structure appearing in the medium)",
                 f"turns sequence: {turns}",
                 "candidate -- verify vs grid resolution in PART D")
        else:
            log(f"  turn count constant ({turns[0]}) -> no new radial "
                "structure; medium stays monotone (B-consistent).")
    return REC


# =====================================================================
# PART D -- VERIFY flagged anomalies: closure-row artifact control +
# grid refinement. The FD Jacobian's closure rows (Dirichlet/Neumann)
# inject eigenvalues that are NOT physical second-variation modes; we
# control for them by reading the gap on the INTERIOR block only, and we
# refine the grid on any flagged background.
# =====================================================================
def part_D(B_REC, C_REC):
    log("\n" + "=" * 72)
    log("PART D -- VERIFY: closure-row artifact control + grid refinement")
    log("=" * 72)
    # pick the most-negative-gap exterior background (if any), else the
    # deepest medium, and refine + re-read the gap with interior-only block.
    cand = None
    pool = [d for d in (B_REC or []) if "gap" in d]
    if pool:
        cand = min(pool, key=lambda d: d["gap"])
    if cand is None:
        log("  no PART B records; refining the deepest PART C medium.")
        Din, Dout, Phi = 0.0, -6.0, 1.0
    else:
        Din, Dout, Phi = cand["Din"], cand["Dout"], cand["Phi"]
        log(f"  refining the extreme-gap background: Din={Din} Dout={Dout} "
            f"Phi={Phi} (ang_gap was {cand['gap']:.4e})")
    log(f"{'Nr':>5} {'Nth':>5} {'conv':>5} {'ang_gap':>12} "
        f"{'gap_int':>12} {'n_neg':>6}")
    prev = None
    for (Nr, Nth) in [(129, 65), (193, 97), (289, 145)]:
        r = solve_ext(Din, Dout, Phi, seed_amp=0.0, Nr=Nr, Nth=Nth)
        if not r["conv"]:
            log(f"{Nr:5d} {Nth:5d}  FAIL")
            continue
        g = angular_gap(r["phi"], r["r"], r["th"], r["dr"], r["dth"],
                        Din, Dout, Phi, 'dir')
        # interior-only gap: rebuild the Jacobian and strike the closure
        # rows/cols (i in {0,Nr-1}, j in {0,Nth-1}) before the eigensolve.
        J, _ = _jacobian_np(r["phi"], r["r"], r["th"], r["dr"], r["dth"],
                            Din, Dout, Phi, 'dir')
        Jd = J.toarray()
        idx = np.arange(Nr * Nth).reshape(Nr, Nth)
        keep = np.ones((Nr, Nth), dtype=bool)
        keep[0, :] = keep[-1, :] = keep[:, 0] = keep[:, -1] = False
        kid = idx[keep]
        Jint = Jd[np.ix_(kid, kid)]
        Jint_s = 0.5 * (Jint + Jint.T)
        evi = np.linalg.eigvalsh(torch.tensor(Jint_s,
                                 device=DEV).cpu().numpy()
                                 if False else Jint_s)
        # interior angular gap: smallest eigenvalue whose eigenvector
        # carries angular content
        ev, evec = np.linalg.eigh(Jint_s)
        Vfull = np.zeros((Nr, Nth, len(ev)))
        # map interior eigvecs back to grid to measure angular content
        angc = np.zeros(len(ev))
        for i in range(len(ev)):
            Vg = np.zeros((Nr, Nth)); Vg[keep] = evec[:, i]
            angc[i] = np.mean(np.std(Vg[2:-2, 2:-2], axis=1))
        isang = angc > 0.3 * angc.max() if angc.max() > 0 else \
            np.zeros(len(ev), bool)
        gap_int = float(ev[isang][np.argmin(np.abs(ev[isang]))]) \
            if isang.any() else float(ev[np.argmin(np.abs(ev))])
        msg = (f"{Nr:5d} {Nth:5d} {str(r['conv']):>5} {g['gap']:12.4e} "
               f"{gap_int:12.4e} {int(np.sum(ev<-1e-9)):6d}")
        if prev is not None:
            msg += f"  d(gap_int)={abs(gap_int-prev):.2e}"
        prev = gap_int
        log(msg)
    log("\n  INTERPRETATION: if the full-Jacobian gap is negative but the")
    log("  INTERIOR-BLOCK gap is positive and converges under refinement,")
    log("  the negativity was a CLOSURE-ROW ARTIFACT (not physical). If")
    log("  BOTH are negative and grid-stable, the medium instability is")
    log("  REAL.")


def _main():
    A = part_A()
    B = part_B()
    C = part_C()
    part_D(B, C)
    log("\n" + "=" * 72)
    log(f"ext_scan COMPLETE ({time.time()-t0:.0f}s). FLAGS: {len(FLAG)}")
    for (tag, what, ev, gr) in FLAG:
        log(f"  [{tag}] {what}  ({gr})")
    if not FLAG:
        log("  NO FLAGS: exterior baseline HOLDS across the scanned region.")
    log("logs /tmp/ext_scan.log  json /tmp/ext_scan_{A,B,C}.json")


if __name__ == "__main__":
    _main()
    _fh.close()
