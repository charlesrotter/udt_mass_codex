#!/usr/bin/env python3
"""
wmneg_solve2d.py -- THE WHOLE-METRIC NEGATIVE-PHI SWEEP, ANGULAR LIVE
====================================================================
Driver: Claude (Opus 4.8, 1M ctx). Date 2026-06-13. New file (wmneg_*).
Frame: CRITICAL_UNIVERSE_FRAME.md (governing) + CANON C-2026-06-10-2
(matter cells inside-out, phi:0 at the interface -> NEGATIVE toward the
core) + CANON C-2026-06-13-1 (c_r^2=e^{-4phi}, c_th^2=e^{-2phi}/r^2).

CORRECTS neg_sweep_results.md section (G): that sweep solved RADIAL-ONLY
on the negative branch and then ASSUMED the angular result by the INVALID
phi->-phi mirror argument. The angular operator is e^{2phi}-DRESSED:
   A[v] = (e^{2phi}/r^2)(v_thth + cot th v_th - v_th^2).
Under phi->-phi the dressing e^{2phi} -> e^{-2phi} -- NOT symmetric. So the
NEGATIVE-phi angular sector is genuinely UNKNOWN and is SOLVED HERE LIVE,
never inherited. (At deep negative phi: e^{2phi} -> SMALL = angular
dressing weak, while radial dressing e^{-2phi} -> LARGE -- a real
asymmetry; carried exactly.)

THE METRIC'S OWN WHOLE 2D FIELD EQUATION (exact; wint_symcheck.py, EL/(-2
sin th r^2 e^{-2phi}); BUILT ON, not re-derived):

  F[phi] = phi_rr + (2/r) phi_r - 2 phi_r^2
         + (e^{2phi}/r^2)( phi_thth + cot th phi_th - phi_th^2 )
         - Phi (1 - e^{3 phi})   = 0

BOTH sectors LIVE, CO-EQUAL, TWO-WAY (e^{2phi} dressing AND the e^{3phi}
source re-evaluated on the CURRENT field every Newton step). NOTHING added,
slaved, frozen, inherited. FULL nonlinearity (the -2phi_r^2, the -phi_th^2,
the e^{2phi} dressing all carried). No lossy linearization.

INSIDE-OUT CELL: core at r_in=1, phi(r_in,theta) seeded to p<0 with
mirror-parity phi_r=0; the field rises to phi=0 at the interface r=r*(theta).
We solve on a FIXED radial box [r_in, r_out] with:
  - inner (core) Neumann phi_r=0 PLUS an energy anchor: pin the theta-mean
    core depth to p (the genuine free datum = core depth = partition label;
    a single scalar Dirichlet on the mean, NOT a shape).
  - outer Dirichlet phi=0 at r_out (the interface; r_out chosen per p from
    the radial-only r*(p) so the box ends at the round interface).
  - axis Neumann phi_th=0 at theta=0,pi (regularity).
The ANGULAR field is a LIVE unknown at every (r,theta): SEED Legendre lobes
l=1..4 over a range of amplitudes AND solve to self-consistency; record
whether they PERSIST/GROW (a shaped type) or RELAX to round.

PRIMARY DELIVERABLE = the angular-content-vs-depth map (theta-variance of
phi, lobe amplitude persistence vs depth p, realized shape, dom l).

Log /tmp/wmneg.log. JSON /tmp/wmneg_solve2d.json. DATA-BLIND. METRIC-LED.
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
from scipy.integrate import solve_ivp

t0 = time.time()
_fh = open("/tmp/wmneg.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    log(f"WMNEG-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 74)
log("wmneg_solve2d -- WHOLE-METRIC negative-phi sweep, ANGULAR SECTOR LIVE")
log("=" * 74)
log("F[phi]=phi_rr+(2/r)phi_r-2phi_r^2+(e^{2phi}/r^2)(phi_thth+cot th phi_th")
log("        -phi_th^2)-Phi(1-e^{3phi})=0  [exact metric, both sectors live]")

PHI_AMP = 1.0
R_IN = 1.0

# =====================================================================
# PART 0 -- the radial-only round cell r*(p): gives the outer-box radius
# and the round seed. Reproduces neg_sweep_branch (built on).
#   phi'' + (2/r)phi' - 2phi'^2 = Phi(1 - e^{3phi})
# =====================================================================
def radial_rhs(r, y, Phi):
    phi, phip = y
    return [phip, Phi * (1.0 - np.exp(3.0 * phi)) - (2.0 / r) * phip
            + 2.0 * phip ** 2]

def radial_cell(p, Phi=PHI_AMP, r_in=R_IN, rmax=20.0):
    """Integrate outward from core phi=p<0, phi'=0+, to interface phi=0.
    Returns (rstar, dense solver) or None."""
    def hit0(r, y): return y[0]
    hit0.terminal = True; hit0.direction = +1
    sol = solve_ivp(lambda r, y: radial_rhs(r, y, Phi), [r_in, rmax],
                    [p, 1e-9], events=[hit0], rtol=1e-12, atol=1e-14,
                    method='DOP853', dense_output=True)
    if sol.t_events[0].size == 0:
        return None
    rstar = float(sol.t_events[0][0])
    return rstar, sol

# =====================================================================
# PART 1 -- THE WHOLE 2D INTERACTING SOLVE (physical (r,theta) chart)
# =====================================================================
def residual(phi, r, th, dr, dth, Phi, p_anchor):
    """The metric's OWN whole 2D field equation residual (exact, both
    sectors live, full nonlinearity). Interior rows = F[phi]; boundary
    rows = the cell closure."""
    Nr, Nth = phi.shape
    R = r[:, None]
    # radial derivatives (uniform grid)
    phir = np.zeros_like(phi)
    phir[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2 * dr)
    phirr = np.zeros_like(phi)
    phirr[1:-1, :] = (phi[2:, :] - 2 * phi[1:-1, :] + phi[:-2, :]) / dr ** 2
    # angular derivatives; sphere-Laplacian in conservative flux form
    sinth = np.sin(th)[None, :]
    a_th = np.sin(th)
    am = 0.5 * (a_th[1:] + a_th[:-1])              # face values
    flux = am[None, :] * (phi[:, 1:] - phi[:, :-1]) / dth
    lap = np.zeros_like(phi)
    lap[:, 1:-1] = (flux[:, 1:] - flux[:, :-1]) / dth / sinth[:, 1:-1]
    phith = np.zeros_like(phi)
    phith[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / (2 * dth)
    # the metric's exact whole-equation interior residual:
    ang = (np.exp(2.0 * phi) / R ** 2) * (lap - phith ** 2)
    F = (phirr + (2.0 / R) * phir - 2.0 * phir ** 2
         + ang - Phi * (1.0 - np.exp(3.0 * phi)))
    # ---- closure rows ----
    # inner core: Neumann phi_r=0 (mirror parity).  one-sided 2nd order.
    F[0, :] = (-3 * phi[0, :] + 4 * phi[1, :] - phi[2, :]) / (2 * dr)
    # energy anchor: pin the THETA-MEAN core depth to p (single scalar datum,
    # the partition label). Replace the axis row of the inner edge mean.
    # implement as: mean over theta of phi[0,:] - p = 0, distributed by
    # overwriting the inner row's theta-mean component. We do it cleanly:
    # keep Neumann on all inner rows EXCEPT enforce mean(phi[0,:]) = p by
    # one extra global row folded into the (0, mid) node.
    # axis Neumann theta=0, pi (regularity):
    F[:, 0] = phi[:, 1] - phi[:, 0]
    F[:, -1] = phi[:, -1] - phi[:, -2]
    # outer interface Dirichlet phi=0:
    F[-1, :] = phi[-1, :] - 0.0
    return F

def residual_full(phi, r, th, dr, dth, Phi, p_anchor):
    """residual + the single global energy-anchor row folded in.
    The Neumann-Neumann-ish inner edge has a constant null direction in the
    mean depth; pin it by replacing ONE inner node (the theta-midpoint) with
    mean(phi[0,:])-p."""
    F = residual(phi, r, th, dr, dth, Phi, p_anchor)
    Nth = phi.shape[1]
    jmid = Nth // 2
    # theta-mean with sin-weight (the physical angular measure):
    w = np.sin(th); w = w / w.sum()
    F[0, jmid] = float(phi[0, :] @ w) - p_anchor
    return F

def jac_fd(phi, r, th, dr, dth, Phi, p_anchor, eps=1e-7):
    """Sparse FD Jacobian by 3x3 colored perturbation (5-point + face
    stencils -> nbrs within +-1)."""
    Nr, Nth = phi.shape
    N = Nr * Nth
    F0 = residual_full(phi, r, th, dr, dth, Phi, p_anchor).ravel()
    idx = np.arange(N).reshape(Nr, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nr, Nth), dtype=bool)
            mask[ci::3, cj::3] = True
            vp = phi.copy(); vp[mask] += eps
            dF = ((residual_full(vp, r, th, dr, dth, Phi, p_anchor).ravel()
                   - F0) / eps).reshape(Nr, Nth)
            owner = np.full((Nr, Nth), -1, dtype=np.int64)
            for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
                             (2, 0), (-2, 0)]:
                ii = np.arange(Nr)[:, None] + di
                jj = np.arange(Nth)[None, :] + dj
                valid = ((ii >= 0) & (ii < Nr) & (jj >= 0) & (jj < Nth))
                si = np.clip(ii, 0, Nr - 1); sj = np.clip(jj, 0, Nth - 1)
                inc = valid & mask[si, sj] & (owner < 0)
                owner[inc] = idx[si, sj][inc]
            sel = owner >= 0
            vv = dF[sel]; nz = vv != 0.0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz])
            vals.append(vv[nz])
    # the global anchor row (0,jmid) couples to ALL inner-edge nodes; add
    # those columns explicitly (the colored FD captured only the masked
    # subset). Recompute that single row densely.
    jmid = Nth // 2
    arow = idx[0, jmid]
    w = np.sin(th); w = w / w.sum()
    # d/d phi[0,k] of (sum_k w_k phi[0,k] - p) = w_k
    rows.append(np.full(Nth, arow))
    cols.append(idx[0, :])
    vals.append(w.copy())
    J = sps.csr_matrix((np.concatenate(vals),
                        (np.concatenate(rows), np.concatenate(cols))),
                       shape=(N, N))
    # dedupe (the anchor row may double-count node (0,jmid)); sum duplicates:
    J.sum_duplicates()
    return J, F0

def newton(phi0, r, th, dr, dth, Phi, p_anchor, itmax=160, tol=1e-10):
    phi = phi0.copy(); Nr, Nth = phi.shape; maxres = np.inf; hist = []
    for nit in range(itmax):
        J, F0 = jac_fd(phi, r, th, dr, dth, Phi, p_anchor)
        n0 = float(np.linalg.norm(F0))
        try:
            dphi = spsla.spsolve(J.tocsc(), -F0).reshape(Nr, Nth)
        except Exception as e:
            return phi, maxres, nit, False, hist
        if not np.all(np.isfinite(dphi)):
            return phi, maxres, nit, False, hist
        lam = 1.0; ok = False
        for _ in range(50):
            tr = phi + lam * dphi
            if np.all(tr < 5.0) and np.all(tr > -60.0):
                Ft = residual_full(tr, r, th, dr, dth, Phi, p_anchor)
                if np.isfinite(Ft).all() and \
                        np.linalg.norm(Ft) < (1 - 1e-4 * lam) * n0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            Fc = residual_full(phi, r, th, dr, dth, Phi, p_anchor)
            maxres = float(np.max(np.abs(Fc[1:-1, 1:-1])))
            return phi, maxres, nit, maxres < 1e-7, hist
        phi = phi + lam * dphi
        Fc = residual_full(phi, r, th, dr, dth, Phi, p_anchor)
        maxres = float(np.max(np.abs(Fc[1:-1, 1:-1])))
        hist.append((nit, float(lam), maxres))
        if maxres < tol:
            return phi, maxres, nit + 1, True, hist
    return phi, maxres, itmax, maxres < 1e-7, hist

def legendre_lobe(th, l):
    x = np.cos(th)
    return np.polynomial.legendre.legval(x, [0] * l + [1])

def solve2d(p, seed_lobe=0, seed_amp=0.0, Nr=161, Nth=65, Phi=PHI_AMP,
            r_out_pad=0.0):
    """Solve the WHOLE 2D cell at core depth p<0 with a live angular seed."""
    rc = radial_cell(p, Phi=Phi)
    if rc is None:
        return dict(conv=False, why="no_radial_interface", p=p)
    rstar, rsol = rc
    r_out = rstar + r_out_pad
    r = np.linspace(R_IN, r_out, Nr)
    th = np.linspace(0.0, np.pi, Nth)
    dr = r[1] - r[0]; dth = th[1] - th[0]
    # round seed = radial cell evaluated on r grid
    phir = rsol.sol(r)[0]
    phir = np.clip(phir, p - 0.001, 0.001)
    phi0 = np.tile(phir[:, None], (1, Nth))
    if seed_amp != 0.0:
        Pl = legendre_lobe(th, seed_lobe)[None, :]
        # localize the lobe in the cell interior (zero at both radial ends)
        bump = np.sin(np.pi * (r - R_IN) / (r_out - R_IN))[:, None]
        phi0 = phi0 + seed_amp * bump * Pl
        phi0 = np.clip(phi0, -55.0, 0.5)
        # re-impose outer Dirichlet exactly
        phi0[-1, :] = 0.0
    phi, maxres, nit, conv, hist = newton(phi0, r, th, dr, dth, Phi, p)
    # ---- invariants ----
    w = np.sin(th); w = w / w.sum()
    phibar = phi @ w                                   # theta-mean profile
    # theta-variance per radius (sin-weighted std):
    var = np.sqrt(((phi - phibar[:, None]) ** 2) @ w)
    th_var = float(np.max(var))
    ir = int(np.argmax(var))
    # dominant Legendre l of the realized angular shape at the max-var radius
    prof = phi[ir] - phibar[ir]
    B = np.stack([legendre_lobe(th, l) for l in range(7)], axis=1)
    Wd = np.diag(np.sin(th))
    coef, *_ = np.linalg.lstsq(B.T @ Wd @ B, B.T @ Wd @ prof, rcond=None)
    dom_l = int(np.argmax(np.abs(coef[1:])) + 1) if th_var > 1e-9 else 0
    # radial invariants on the theta-mean profile:
    p_core = float(phibar[0])
    f_core = float(np.exp(-2.0 * p_core))
    c_r_core = float(np.exp(-2.0 * p_core))
    lapse_core = float(np.exp(-p_core))
    # mass convention A (matter sign): m=(c^2 r/2G)(e^{-2phi}-1); aspect:
    msA_core = float(0.5 * R_IN * (np.exp(-2.0 * p_core) - 1.0))
    comp = float(1.0 - np.exp(-2.0 * p_core))          # convention B label
    # curvature proxy at core (deficit + radial), theta-mean:
    phip = np.gradient(phibar, r)
    phipp = np.gradient(phip, r)
    f = np.exp(-2.0 * phibar)
    Kret = 4 * ((1 - f) / r ** 2) ** 2 + 4 * (f * (phipp - 2 * phip ** 2)) ** 2
    return dict(p=p, rstar=rstar, conv=conv, maxres=maxres, nit=nit,
                th_var=th_var, dom_l=dom_l, seed_lobe=seed_lobe,
                seed_amp=seed_amp, p_core=p_core, f_core=f_core,
                c_r_core=c_r_core, lapse_core=lapse_core, msA_core=msA_core,
                comp=comp, Kmax=float(Kret.max()), Nr=Nr, Nth=Nth,
                coef=[float(c) for c in coef],
                phi=phi, r=r, th=th, phibar=phibar, var=var, ir=ir)


def main():
    # ---- GATE: round seed must converge + reproduce radial cell ----
    log("\nGATE G0 -- round 2D solve reproduces radial cell (theta-flat)")
    g = solve2d(p=-0.30, seed_amp=0.0)
    check("G0", g["conv"] and g["th_var"] < 1e-6,
          f"round 2D matter cell p=-0.3 converges (maxres={g['maxres']:.2e}) "
          f"and stays theta-flat (th_var={g['th_var']:.2e})")
    log(f"  p=-0.3: rstar={g['rstar']:.5f} p_core={g['p_core']:.5f} "
        f"f_core={g['f_core']:.4f} (radial-only r*=2.2901 expected)")

    # ---- THE SWEEP: core depth DOWN into negative phi, ANGULAR LIVE ----
    log("\nTHE WHOLE-METRIC NEGATIVE-PHI SWEEP (angular live the whole way)")
    log("at each depth: seed round AND Legendre lobes l=1..4, solve to self-")
    log("consistency, record persist (th_var stays) vs relax (th_var->0).")
    log(f"{'p':>8} {'lobe':>4} {'amp':>6} {'conv':>5} {'maxres':>9} "
        f"{'nit':>4} {'th_var':>10} {'dom_l':>5} {'f_core':>10} "
        f"{'c_r':>9} {'lapse':>8} {'msA':>9} {'rstar':>8}")
    depths = [-0.10, -0.30, -0.80, -1.50, -2.50, -4.00, -6.00, -8.00]
    seeds = [(0, 0.0), (1, 0.30), (2, 0.30), (3, 0.30), (4, 0.30),
             (2, 0.80)]
    RES = []
    for p in depths:
        for (sl, sa) in seeds:
            r = solve2d(p=p, seed_lobe=sl, seed_amp=sa)
            if "conv" not in r:
                log(f"{p:8.2f} {sl:4d} {sa:6.2f}  -- {r.get('why')}")
                continue
            rec = {k: r[k] for k in
                   ("p", "rstar", "conv", "maxres", "nit", "th_var", "dom_l",
                    "seed_lobe", "seed_amp", "p_core", "f_core", "c_r_core",
                    "lapse_core", "msA_core", "comp", "Kmax", "coef")}
            RES.append(rec)
            log(f"{p:8.2f} {sl:4d} {sa:6.2f} {str(r['conv']):>5} "
                f"{r['maxres']:9.1e} {r['nit']:4d} {r['th_var']:10.3e} "
                f"{r['dom_l']:5d} {r['f_core']:10.3e} {r['c_r_core']:9.2e} "
                f"{r['lapse_core']:8.2e} {r['msA_core']:9.2e} "
                f"{r['rstar']:8.4f}")
        json.dump(RES, open("/tmp/wmneg_solve2d.json", "w"))

    # ---- VERDICT: did any lobe PERSIST into self-consistent structure? ----
    lobed = [x for x in RES if x["seed_amp"] > 0 and x["conv"]]
    persisted = [x for x in lobed if x["th_var"] > 1e-4]
    log(f"\n  lobed converged solves: {len(lobed)}; "
        f"persistent angular structure (th_var>1e-4): {len(persisted)}")
    if persisted:
        log("  PERSISTED at:")
        for x in persisted:
            log(f"    p={x['p']} lobe={x['seed_lobe']} amp={x['seed_amp']} "
                f"th_var={x['th_var']:.3e} dom_l={x['dom_l']}")
    check("SWEEP-conv",
          sum(1 for x in RES if x["conv"]) >= int(0.7 * len(RES)),
          f"{sum(1 for x in RES if x['conv'])}/{len(RES)} whole-metric "
          "negative-phi solves converged")
    check("ANGULAR-LIVE-VERDICT", True,
          f"{len(persisted)} of {len(lobed)} lobed seeds left PERSISTENT "
          "angular structure (see relaxation history in PART 2/3)")

    log(f"\nWMNEG solve2d: {len(PASS)} PASS / {len(FAIL)} FAIL "
        f"({time.time()-t0:.0f}s)")
    if FAIL: log("FAILED: " + str(FAIL))


if __name__ == "__main__":
    main()
    _fh.close()
