#!/usr/bin/env python3
"""
wcc_closed_cell.py -- THE WHOLE CLOSED CELL: interior + seal mirror-fold
closure SOLVED TOGETHER, both phi(r,theta) and the angular sector live.
=======================================================================
WHOLE-CLOSED-CELL push. Driver: Claude (Opus 4.8). Date 2026-06-13.
Frame: CRITICAL_UNIVERSE_FRAME.md. New file (repo discipline; wcc_*).
Reuses (does NOT edit) the verified machinery: the wint two-way residual
(the metric's own e^{2v}-dressed angular operator + ON two-exponential
source), and the w7a/w6 DERIVED mirror-fold parity closure.

THE QUESTION (the genuine open edge flagged by wint_results section vi #1,
and never solved): the BULK interior solve damps every angular shape to
round (registry #34) and its Jacobian is non-singular (no bifurcation in
the trust window). But that solve closed the outer end at a TRUST-WINDOW
Neumann turning point -- it never imposed the SEAL mirror-fold parity
closure on the LIVE DIFFERENTIAL angular field. W7 imposed the crease BC
but with angular entering ALGEBRAICALLY only (its own scope note). Nobody
has put the live differential angular field phi(r,theta) TOGETHER with the
mirror-fold parity closure at the seal. That intersection is exactly
Charles's prime suspect (phi-angular coupling) meeting the only place
structure can live (the closure). THIS PUSH SOLVES THAT.

THE DERIVED CLOSURE (w6 + w7a, theorem-grade, NOTHING added):
  The seal = D=0 crease = fixed surface of the same-minus involution
  sigma:(a,b)->(-a,-b). Crease normal datum rho = b - f q a is ODD under
  sigma. The mirror quotient glues cell onto mirror across rho=0. PARITY
  DICHOTOMY at the crease:
     sigma-EVEN sector (static shape)        -> NEUMANN  (d_n delta = 0)
     sigma-ODD  sector (f_T-driven amplitude) -> DIRICHLET (delta = 0)
  Both towers present; sigma fixes the parity within each.

HOW THE SEAL IS HANDLED (per the task, and per w6/w7): the seal is a
CLOSURE (a boundary/matching/parity condition), NOT a march through D=0.
We do NOT integrate a dynamical solution through the singular crease. We
impose the derived parity BC at the seal as the OUTER closure of the BVP,
the way the mirror-fold theorem and the area form already do.

THE BVP (posed once, solved here):
  field:   v(m,theta), the dressed dilation phi in the flow chart (m,theta)
  interior: v_mm + e^{2v}(v_thth + cot th v_th - v_th^2)
              = Phi(e^{-2v} - e^{v})            (metric's own EL, wint (star))
  inner closure (center / mirror parity): v_m=0 turning point, energy E
  axis closure (sphere regularity): v_th=0 at theta=0,pi
  OUTER SEAL closure (the new object): mirror-fold parity at the crease,
     in EACH branch:
        EVEN branch  -> Neumann   d_m v = 0  at the seal
        ODD  branch  -> Dirichlet (anti-symmetric) v - v_seal = 0
  free data: partition energy E.

DELIVERABLE (analyze the structures the CLOSED object supports):
  PART A: pose + closure self-consistency checks (exact where it bites).
  PART B: the CLOSED-CELL ANGULAR OPERATOR spectrum about the round cell,
          under BOTH parity branches -- does the seal closure support
          angular modes (zero/sign-changing eigenvalues = a shaped type
          can be born) that the bulk-Neumann closure forbids? This is the
          sharp structural test. Compare bulk-Neumann vs seal-parity.
  PART C: full nonlinear CLOSED solve, lobed seeds, BOTH branches -- do
          shaped configurations persist when closed at the seal?
  PART D: the topological/area-form content of the parity-ODD sector at
          the crease (the H1 object lives here) -- characterize, don't
          invent or count to integers.

DISCIPLINE: NO mass-number matching, NO clean-integer/generation hunting
(registry #35 rejected {3,5,7}), NO invented sectors. Analyze what the
closed object supports. Log /tmp/wcc_closed_cell.log flush-per-line.
HYPOTHESIS-GRADE; flag for blind verifier.
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
import mpmath as mp

t0 = time.time()
_fh = open("/tmp/wcc_closed_cell.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL, NOTE = [], [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    log(f"WCC-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 72)
log("wcc_closed_cell -- the WHOLE CLOSED CELL: interior + seal mirror-fold")
log("=" * 72)

# =====================================================================
# Shared radial cell objects (the metric's own ON two-exponential well;
# banked w_whole_gm PART D / w_alg PART E; taken, not invented).
# =====================================================================
mp.mp.dps = 30
def U(v, Phi): return Phi / 2 * mp.exp(-2 * v) + Phi * mp.exp(v)
def Umin(Phi): return mp.mpf('1.5') * Phi
def cell_LE(E, Phi):
    Um = Umin(Phi)
    if E <= Um: return None
    g = lambda v: U(v, Phi) - E
    def bracket(sgn):
        a = mp.mpf('0'); b = sgn * mp.mpf('0.01')
        for _ in range(200):
            if g(b) > 0:
                return mp.findroot(g, (a, b), solver='bisect')
            a, b = b, b * mp.mpf('1.3') if abs(b) < 50 else b
            if abs(b) > 60: break
        return None
    vlo = bracket(-1); vhi = bracket(+1)
    if vlo is None or vhi is None: return None
    L = mp.quad(lambda v: 1 / mp.sqrt(max(2 * (E - U(v, Phi)),
                mp.mpf('1e-40'))), [vlo, vhi])
    return float(L), float(vlo), float(vhi)

# =====================================================================
# THE CLOSED-CELL RESIDUAL. Identical interior to wint (the metric's own
# EL, verified there), but the OUTER closure is the MIRROR-FOLD PARITY BC,
# selectable EVEN (Neumann) or ODD (Dirichlet), per w7a. The inner end is
# the center turning point (energy anchor v=vlo). This is the only change
# from wint: the seal is closed by the DERIVED parity BC, not a
# trust-window Neumann.
# =====================================================================
def residual(v, m, th, dm, dth, Phi_amp, vlo, vseal, branch):
    """branch in {'even','odd','bulkN'}.
    even   = mirror-fold sigma-EVEN  -> Neumann d_m v=0 at seal (sym fold)
    odd    = mirror-fold sigma-ODD   -> Dirichlet v=vseal at seal (antisym)
    bulkN  = the wint trust-window Neumann (CONTROL = the bulk closure)."""
    Nm, Nth = v.shape
    vmm = np.zeros_like(v)
    vmm[1:-1, :] = (v[2:, :] - 2 * v[1:-1, :] + v[:-2, :]) / dm ** 2
    # metric's own e^{2v}-dressed angular operator (wint_symcheck verified):
    #   A = e^{2v}[(1/sin)d_th(sin d_th v) - v_th^2]
    sinth = np.sin(th)[None, :]
    a_th = sinth
    am = 0.5 * (a_th[:, 1:] + a_th[:, :-1])
    flux = am * (v[:, 1:] - v[:, :-1]) / dth
    ang = np.zeros_like(v)
    ang[:, 1:-1] = (flux[:, 1:] - flux[:, :-1]) / dth / sinth[:, 1:-1]
    vth = np.zeros_like(v)
    vth[:, 1:-1] = (v[:, 2:] - v[:, :-2]) / (2 * dth)
    A = np.exp(2.0 * v) * (ang - vth ** 2)
    F = vmm + A - Phi_amp * (np.exp(-2 * v) - np.exp(v))
    # inner closure: center depth anchor = v_min(E) (mirror parity center):
    F[0, :] = v[0, :] - vlo
    # OUTER SEAL closure (the new object):
    if branch == 'even' or branch == 'bulkN':
        F[-1, :] = v[-1, :] - v[-2, :]         # Neumann d_m v = 0
    elif branch == 'odd':
        F[-1, :] = v[-1, :] - vseal            # Dirichlet (antisym fold)
    else:
        raise ValueError(branch)
    # axis Neumann (sphere regularity):
    F[:, 0] = v[:, 0] - v[:, 1]
    F[:, -1] = v[:, -1] - v[:, -2]
    return F

def jac(v, m, th, dm, dth, Phi_amp, vlo, vseal, branch, eps=1e-7):
    Nm, Nth = v.shape
    N = Nm * Nth
    F0 = residual(v, m, th, dm, dth, Phi_amp, vlo, vseal, branch).ravel()
    idx = np.arange(N).reshape(Nm, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nm, Nth), dtype=bool)
            mask[ci::3, cj::3] = True
            vp = v.copy(); vp[mask] += eps
            dF = ((residual(vp, m, th, dm, dth, Phi_amp, vlo, vseal,
                            branch).ravel() - F0) / eps).reshape(Nm, Nth)
            owner = np.full((Nm, Nth), -1, dtype=np.int64)
            for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                si = np.clip(np.arange(Nm)[:, None] + di, 0, Nm - 1)
                sj = np.clip(np.arange(Nth)[None, :] + dj, 0, Nth - 1)
                valid = ((np.arange(Nm)[:, None] + di >= 0)
                         & (np.arange(Nm)[:, None] + di < Nm)
                         & (np.arange(Nth)[None, :] + dj >= 0)
                         & (np.arange(Nth)[None, :] + dj < Nth))
                inc = valid & mask[si, sj] & (owner < 0)
                owner[inc] = idx[si, sj][inc]
            sel = owner >= 0
            vv = dF[sel]; nz = vv != 0.0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz])
            vals.append(vv[nz])
    return sps.csr_matrix((np.concatenate(vals),
                          (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)), F0

def newton(v0, m, th, dm, dth, Phi_amp, vlo, vseal, branch,
           itmax=150, tol=1e-10):
    v = v0.copy(); maxres = np.inf; hist = []
    for nit in range(itmax):
        J, F0 = jac(v, m, th, dm, dth, Phi_amp, vlo, vseal, branch)
        n0 = float(np.linalg.norm(F0))
        try:
            dv = spsla.spsolve(J, -F0).reshape(v.shape)
        except Exception:
            return v, maxres, nit, False, hist
        if not np.all(np.isfinite(dv)):
            return v, maxres, nit, False, hist
        lam = 1.0; ok = False
        for _ in range(40):
            tr = v + lam * dv
            if np.all(np.abs(tr) < 40):
                Ft = residual(tr, m, th, dm, dth, Phi_amp, vlo, vseal,
                              branch)
                if np.isfinite(Ft).all() and \
                        np.linalg.norm(Ft) < (1 - 1e-4 * lam) * n0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            maxres = float(np.max(np.abs(residual(
                v, m, th, dm, dth, Phi_amp, vlo, vseal, branch)[1:-1, 1:-1])))
            return v, maxres, nit, maxres < 1e-8, hist
        v = v + lam * dv
        maxres = float(np.max(np.abs(residual(
            v, m, th, dm, dth, Phi_amp, vlo, vseal, branch)[1:-1, 1:-1])))
        hist.append((nit, lam, maxres))
        if maxres < tol:
            return v, maxres, nit + 1, True, hist
    return v, maxres, itmax, maxres < 1e-8, hist

def radial_seed(E_factor, Phi_amp, Nm):
    Phi_m = mp.mpf(Phi_amp)
    E = Umin(Phi_m) * mp.mpf(E_factor)
    res = cell_LE(E, Phi_m)
    if res is None: return None
    L, vlo, vhi = res
    m = np.linspace(0.0, L, Nm)
    dm = m[1] - m[0]
    vr = np.zeros(Nm); vv = vlo; pp = 0.0; vr[0] = vv
    for i in range(1, Nm):
        def fdyn(vv, pp): return pp, float(Phi_m) * (np.exp(-2*vv) - np.exp(vv))
        k1 = fdyn(vv, pp)
        k2 = fdyn(vv + dm/2*k1[0], pp + dm/2*k1[1])
        k3 = fdyn(vv + dm/2*k2[0], pp + dm/2*k2[1])
        k4 = fdyn(vv + dm*k3[0], pp + dm*k3[1])
        vv += dm/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        pp += dm/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        vr[i] = vv
    return dict(L=L, vlo=vlo, vhi=vhi, m=m, dm=dm, vr=vr, E=float(E))

def solve_closed(E_factor, branch, Phi_amp=1.0, seed_lobe=0, seed_amp=0.0,
                 Nm=129, Nth=49):
    seed = radial_seed(E_factor, Phi_amp, Nm)
    if seed is None: return dict(conv=False, why="below_well")
    L, vlo, vhi, m, dm, vr = (seed['L'], seed['vlo'], seed['vhi'],
                              seed['m'], seed['dm'], seed['vr'])
    th = np.linspace(0.0, np.pi, Nth); dth = th[1] - th[0]
    vseal = float(vr[-1])  # the round-cell seal value (for the odd-Dirichlet)
    v0 = np.tile(vr[:, None], (1, Nth))
    if seed_amp != 0.0:
        x = np.cos(th)
        Pl = np.polynomial.legendre.legval(x, [0]*seed_lobe + [1])[None, :]
        bump = np.exp(-((m / L - 0.5) / 0.25) ** 2)[:, None]
        v0 = v0 + seed_amp * bump * Pl
    v, maxres, nit, conv, hist = newton(
        v0, m, th, dm, dth, float(Phi_amp), vlo, vseal, branch)
    th_var = float(np.max(np.std(v, axis=1)))
    ir = int(np.argmax(np.std(v, axis=1)))
    prof = v[ir] - v[ir].mean()
    x = np.cos(th)
    B = np.stack([np.polynomial.legendre.legval(x, [0]*l + [1])
                  for l in range(7)], axis=1)
    Wd = np.diag(np.sin(th))
    coef, *_ = np.linalg.lstsq(B.T @ Wd @ B, B.T @ Wd @ prof, rcond=None)
    dom_l = int(np.argmax(np.abs(coef[1:])) + 1) if th_var > 1e-9 else 0
    wth = np.sin(th); wth = wth / wth.sum(); vbar = v @ wth
    X = float(1 - np.exp(-2 * vbar.max()))
    return dict(E=seed['E'], L=L, branch=branch, seed_lobe=seed_lobe,
                seed_amp=seed_amp, conv=conv, maxres=maxres, nit=nit,
                th_var=th_var, dom_l=dom_l, X=X,
                coef=[float(c) for c in coef], v=v, m=m, th=th,
                vlo=vlo, vseal=vseal, dm=dm, dth=dth)


# =====================================================================
def _partA():
    log("\nPART A -- pose + closure self-consistency")
    # the round cell must converge and stay round in the bulkN control:
    g = solve_closed(2.0, 'bulkN', seed_amp=0.0)
    check("A0", g["conv"] and g["th_var"] < 1e-7,
          f"round cell converges in the BULK-NEUMANN control "
          f"(maxres={g['maxres']:.1e}, th_var={g['th_var']:.1e}) -- the "
          "wint interior reproduced as the control")
    # the EVEN seal branch (Neumann) must also admit the round cell:
    ge = solve_closed(2.0, 'even', seed_amp=0.0)
    check("A1", ge["conv"] and ge["th_var"] < 1e-7,
          f"round cell converges under the mirror-fold EVEN (Neumann) seal "
          f"closure (maxres={ge['maxres']:.1e}, th_var={ge['th_var']:.1e})")
    # the ODD seal branch (Dirichlet at vseal): round cell sits at vseal
    # by construction, so it must also be a fixed point:
    go = solve_closed(2.0, 'odd', seed_amp=0.0)
    check("A2", go["conv"] and go["th_var"] < 1e-7,
          f"round cell converges under the mirror-fold ODD (Dirichlet) seal "
          f"closure (maxres={go['maxres']:.1e}, th_var={go['th_var']:.1e})")
    return g, ge, go


# =====================================================================
# PART B -- THE DECISIVE STRUCTURAL TEST: the CLOSED-CELL ANGULAR
# OPERATOR spectrum about the round cell, under EACH seal closure.
# We linearize the full 2D residual about the converged round cell and
# compute the eigenvalues of the Jacobian restricted to ANGULAR (dom_l>=1)
# perturbations -- i.e. project out the round (l=0) directions and ask
# whether the closed operator has a zero/sign-changing mode (a shaped type
# can be born) that the bulk-Neumann closure forbids.
#
# The clean invariant: the smallest eigenvalue of the SYMMETRIZED angular
# stiffness. In the bulk (wint) it is bounded away from 0 (no bifurcation).
# Does the seal closure (even/odd) lower or zero it?
# =====================================================================
def angular_spectrum(r0, n_report=8):
    """Linearize about the converged round cell r0; return the eigenvalues
    of the Jacobian most associated with ANGULAR (theta-varying) modes.
    We compute the full Jacobian, then measure each eigenvector's angular
    content (variance across theta) and report the eigenvalues of the
    angularly-active modes, smallest |Re| first."""
    v = r0["v"]; m = r0["m"]; th = r0["th"]
    dm = r0["dm"]; dth = r0["dth"]; vlo = r0["vlo"]; vseal = r0["vseal"]
    branch = r0["branch"]; Nm, Nth = v.shape
    J, _ = jac(v, m, th, dm, dth, 1.0, vlo, vseal, branch)
    Jd = J.toarray()
    ev, evec = np.linalg.eig(Jd)
    # angular content of each eigenvector: variance across theta of the
    # reshaped mode (drop the boundary rows that are pure BC closure):
    ang_content = np.zeros(len(ev))
    for k in range(len(ev)):
        w = np.real(evec[:, k]).reshape(Nm, Nth)
        interior = w[1:-1, 1:-1]
        if np.linalg.norm(interior) < 1e-14:
            ang_content[k] = 0.0; continue
        # fraction of the mode's power in theta-varying part:
        thmean = interior.mean(axis=1, keepdims=True)
        ang_content[k] = (np.linalg.norm(interior - thmean)
                          / np.linalg.norm(interior))
    # angularly-active eigenvalues: ang_content > 0.5 (dominantly angular)
    ang_mask = ang_content > 0.5
    ang_ev = ev[ang_mask]
    if len(ang_ev) == 0:
        return dict(min_abs_ang=np.inf, n_ang=0, ang_ev=[],
                    all_min_abs=float(np.min(np.abs(ev))),
                    any_neg_ang=False)
    order = np.argsort(np.abs(ang_ev))
    ang_ev = ang_ev[order]
    return dict(min_abs_ang=float(np.min(np.abs(ang_ev))),
                n_ang=int(len(ang_ev)),
                ang_ev=[complex(x) for x in ang_ev[:n_report]],
                all_min_abs=float(np.min(np.abs(ev))),
                any_neg_ang=bool(np.any(np.real(ang_ev) < -1e-7)))


def _partB():
    # SUPERSEDED NOTE: this PART B reads eigenvalue SIGNS off the raw
    # non-symmetric FD Jacobian, which carries spurious complex/negative
    # eigenvalues from the BC rows ("any neg ang" fired even in the bulk
    # control wint proved stable). The TRUSTWORTHY version is
    # wcc_seal_spectrum.py (symmetric part Js=(J+J^T)/2, real spectrum,
    # angular-restricted, blind-verified). The min|eig| comparison below is
    # still informative (odd seal stiffens: 0.39 vs 0.035), but the SIGN
    # reading here is NOT reliable -- use wcc_seal_spectrum for the verdict.
    log("\nPART B -- CLOSED-CELL ANGULAR OPERATOR SPECTRUM (the decisive test)")
    log("  [SUPERSEDED by wcc_seal_spectrum.py: symmetric, sign-reliable]")
    log("  Does the SEAL mirror-fold closure support an angular mode the")
    log("  BULK-NEUMANN closure damps away? Compare min|angular eig| and")
    log("  sign across branches and the E-family.")
    log(f"{'E/Um':>6} {'branch':>7} {'n_ang':>6} {'min|ang eig|':>13} "
        f"{'any neg ang':>12} {'all min|eig|':>13}")
    rows = []
    for Ef in [1.3, 2.0, 3.0, 4.0]:
        for branch in ['bulkN', 'even', 'odd']:
            r0 = solve_closed(Ef, branch, seed_amp=0.0, Nm=81, Nth=41)
            if not r0["conv"]:
                log(f"{Ef:6.2f} {branch:>7}  (no converge)"); continue
            sp_ = angular_spectrum(r0)
            rows.append(dict(E=Ef, branch=branch, **{
                k: sp_[k] for k in ('min_abs_ang', 'n_ang', 'any_neg_ang',
                                    'all_min_abs')}))
            log(f"{Ef:6.2f} {branch:>7} {sp_['n_ang']:6d} "
                f"{sp_['min_abs_ang']:13.6f} "
                f"{str(sp_['any_neg_ang']):>12} {sp_['all_min_abs']:13.6f}")
    # the structural verdict:
    bulk = [x for x in rows if x['branch'] == 'bulkN']
    even = [x for x in rows if x['branch'] == 'even']
    odd = [x for x in rows if x['branch'] == 'odd']
    bulk_min = min((x['min_abs_ang'] for x in bulk), default=np.inf)
    even_min = min((x['min_abs_ang'] for x in even), default=np.inf)
    odd_min = min((x['min_abs_ang'] for x in odd), default=np.inf)
    any_neg = any(x['any_neg_ang'] for x in rows)
    log(f"\n  bulkN min|ang eig| over E = {bulk_min:.6f}")
    log(f"  even  min|ang eig| over E = {even_min:.6f}")
    log(f"  odd   min|ang eig| over E = {odd_min:.6f}")
    log(f"  any angular eigenvalue went NEGATIVE (instability/new type) "
        f"in ANY branch: {any_neg}")
    # record the structural finding (NOT a pass/fail of a target -- a
    # measurement). The test PASSES if it produces a clean comparison.
    check("B-meas", len(rows) >= 6,
          "closed-cell angular spectra computed across branches and E "
          "(this is a MEASUREMENT of what the closure supports)")
    NOTE.append(("B-bulk_min", bulk_min))
    NOTE.append(("B-even_min", even_min))
    NOTE.append(("B-odd_min", odd_min))
    NOTE.append(("B-any_neg", any_neg))
    return rows


# =====================================================================
# PART C -- FULL NONLINEAR CLOSED SOLVE, lobed seeds, BOTH parity
# branches. Does a shaped configuration PERSIST when closed at the seal?
# =====================================================================
def _partC():
    log("\nPART C -- nonlinear CLOSED solve, lobed seeds, EACH seal branch")
    log(f"{'E/Um':>6} {'branch':>7} {'lobe':>4} {'amp':>5} {'conv':>5} "
        f"{'maxres':>9} {'th_var':>10} {'dom_l':>5} {'X':>8}")
    rows = []
    for Ef in [1.6, 3.0]:
        for branch in ['even', 'odd', 'bulkN']:
            for (sl, sa) in [(1, 0.30), (2, 0.30), (3, 0.30)]:
                r = solve_closed(Ef, branch, seed_lobe=sl, seed_amp=sa,
                                 Nm=97, Nth=41)
                if 'conv' not in r: continue
                rows.append({k: r.get(k) for k in
                             ('E', 'branch', 'seed_lobe', 'seed_amp',
                              'conv', 'maxres', 'th_var', 'dom_l', 'X')})
                log(f"{Ef:6.2f} {branch:>7} {sl:4d} {sa:5.2f} "
                    f"{str(r['conv']):>5} {r['maxres']:9.1e} "
                    f"{r['th_var']:10.2e} {r['dom_l']:5d} {r['X']:8.4f}")
    persisted = [x for x in rows if x['conv'] and x['th_var'] > 1e-4]
    log(f"\n  lobed CLOSED solves that PERSISTED with angular structure "
        f"(th_var>1e-4): {len(persisted)} / {sum(1 for x in rows if x['conv'])}")
    for x in persisted:
        log(f"    PERSISTED: E={x['E']:.3f} branch={x['branch']} "
            f"seed_l={x['seed_lobe']} th_var={x['th_var']:.3e} "
            f"dom_l={x['dom_l']}")
    check("C-meas", len(rows) >= 6,
          "nonlinear closed lobed solves run across branches "
          "(measurement of persistence under the seal closure)")
    NOTE.append(("C-n_persisted", len(persisted)))
    NOTE.append(("C-n_conv", sum(1 for x in rows if x['conv'])))
    return rows, persisted


# =====================================================================
def _main():
    g, ge, go = _partA()
    Brows = _partB()
    Crows, persisted = _partC()
    log("\n" + "=" * 72)
    log("WCC SUMMARY")
    log("=" * 72)
    for k, v in NOTE:
        log(f"  {k} = {v}")
    log(f"\nWCC: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
    if FAIL: log("FAILED: " + str(FAIL))
    out = dict(notes=dict(NOTE), B=Brows,
               C=[{k: x[k] for k in x if k != 'coef'} for x in Crows])
    with open("/tmp/wcc_closed_cell.json", "w") as fh:
        json.dump(out, fh, indent=0, default=str)
    log("checkpoint /tmp/wcc_closed_cell.json  log /tmp/wcc_closed_cell.log")


if __name__ == "__main__":
    _main()
    _fh.close()
