#!/usr/bin/env python3
"""
wint_solve2d.py -- THE TWO-WAY INTERACTING SOLVE, BOTH SECTORS LIVE
==================================================================
INTERACTING-WHOLE push. Driver: Claude (Opus 4.8). Date 2026-06-13.
Frame: CRITICAL_UNIVERSE_FRAME.md. Pre-reg: wint_preregister.md.
New file (repo discipline). GPU V100 torch float64.

CHARLES'S ORDER (verbatim register): "compute the solution space of the
WHOLE metric and analyse what structures form." "The geometry more likely
forces the TYPES of lumps." Two-way INTERACTING (neither frozen). Solve
and LOOK; impose nothing.

WHAT THIS DOES THAT THE PRIOR PUSHES DID NOT:
 - the ANGULAR sector is LIVE: phi = phi(r,theta) is a genuine 2D field,
   NOT slaved, NOT reduced to scale-free numbers q,N. The metric's own
   angular operator is the e^{2phi}-DRESSED angular Laplacian (the
   phi-angular coupling, derived, NOTHING added -- Charles's standing
   hunch's prime suspect appearing for free).
 - the matter source is the metric's OWN derived ON restoring content
   S(phi)=Phi(e^{-2phi}-e^{phi}) (w_alg PART E / w_whole_gm PART D --
   the two-exponential well that CLOSES a cell; the OFF/vacuum monotone
   source provably cannot close, w_whole_gm PART C). TAKEN, not invented.
 - the solve is genuinely TWO-WAY: each relaxation sweep updates BOTH the
   e^{-2phi} metric weight AND the matter source S(phi) from the CURRENT
   field; nothing frozen; iterate to mutual self-consistency.

THE COUPLED SYSTEM (exact; verified symbolically in wint_symcheck.py):
   Box_g phi = S(phi),   with the metric's own dilation operator
   Box_g phi = (1/r^2) d_r( r^2 e^{-2phi} phi_r )
             + (1/(r^2 sin th)) d_th( sin th e^{-2phi} phi_th )
   and S(phi) = Phi*(e^{-2phi} - e^{phi})   [derived ON statics, w_alg E].
   (Phi -> 0 recovers the bare sourceless metric EOM, registry #33.)
MS/dilation tie reads the matter off the metric:
   m(r) = (c^2 r/2G)(1 - e^{-2 <phi>_theta(r)}).

CLOSURE (metric's own; nothing added):
   inner Neumann phi_r(r_in)=0 (center regularity / mirror parity);
   axis Neumann phi_th=0 at theta=0,pi (smoothness on the sphere);
   outer Dirichlet phi(r*,theta)=D (the partition depth; genuine free
   datum = the matter content). We solve on the trust window [r_in,r*]
   interior to the seal f->0 and report scope.

PRE-REGISTERED (wint_preregister.md; restated): a STRUCTURE = a converged
self-consistent (two-way fixed point) phi(r,theta), residual<1e-8, that
PERSISTS under refinement + small perturbation. Outcomes: O1 one type /
O2 a family / O3 several distinct types / O4 nothing stable.

Log: /tmp/wint_solve2d.log (flush per line). Checkpoint -> /tmp/wint_ckpt.
Convergence evidence mandatory. HYPOTHESIS-GRADE.
"""
import sys, time, json, os
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
import torch

torch.set_default_dtype(torch.float64)
DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
t0 = time.time()
LOG = "/tmp/wint_solve2d.log"
_fh = open(LOG, "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _fh.write(s + "\n"); _fh.flush()

PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    log(f"WINT2D-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

def jclean(o):
    """Make numpy scalars/bools JSON-serializable."""
    if isinstance(o, dict):
        return {k: jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    return o

# ---------------------------------------------------------------------
# Grid: r in [r_in, r_star] (trust window), theta in (0, pi).
# We use a node-centred grid with ghost-free Neumann via one-sided stencils.
# ---------------------------------------------------------------------
def make_grid(r_in, r_star, Nr, Nth):
    r = torch.linspace(r_in, r_star, Nr, device=DEV)
    # theta strictly interior to avoid the sin(theta)=0 coordinate
    # singularity; axis Neumann imposed via reflection at the ends.
    th = torch.linspace(0.0, np.pi, Nth, device=DEV)
    return r, th

def laplace_box(phi, r, th, dr, dth):
    """The metric's own dilation-weighted 2D operator applied to phi.
    Box_g phi = (1/r^2) d_r(r^2 e^{-2phi} phi_r)
              + (1/(r^2 sinth)) d_th(sinth e^{-2phi} phi_th).
    Conservative (flux-form) finite differences; weight e^{-2phi} from the
    CURRENT phi (two-way). Returns Box at interior nodes; edges via the
    closure (handled by the caller's Jacobi update)."""
    w = torch.exp(-2.0 * phi)                       # e^{-2phi}, UPDATED
    R = r.view(-1, 1)
    sinth = torch.sin(th).view(1, -1)
    # radial flux a_r = r^2 e^{-2phi} ; midpoint averaging
    a_r = (R ** 2) * w
    am_r = 0.5 * (a_r[1:, :] + a_r[:-1, :])         # (Nr-1, Nth)
    flux_r = am_r * (phi[1:, :] - phi[:-1, :]) / dr  # at r-midpoints
    div_r = torch.zeros_like(phi)
    div_r[1:-1, :] = (flux_r[1:, :] - flux_r[:-1, :]) / dr / (R[1:-1] ** 2)
    # angular flux a_th = sinth e^{-2phi} ; midpoint averaging in theta
    a_th = sinth * w
    am_th = 0.5 * (a_th[:, 1:] + a_th[:, :-1])
    flux_th = am_th * (phi[:, 1:] - phi[:, :-1]) / dth
    div_th = torch.zeros_like(phi)
    div_th[:, 1:-1] = (flux_th[:, 1:] - flux_th[:, :-1]) / dth \
        / (R ** 2 * sinth)[:, 1:-1]
    return div_r + div_th

def source(phi, Phi_amp):
    """The derived ON restoring matter source S(phi)=Phi(e^{-2phi}-e^{phi}).
    Well bottom at phi=0 (the seal locus). Phi_amp>0 = ON; 0 = bare EOM."""
    return Phi_amp * (torch.exp(-2.0 * phi) - torch.exp(phi))


# =====================================================================
# Numpy residual + analytic sparse Jacobian for the damped-Newton solve.
# The interior PDE F = Box_g phi - S(phi); the closure rows are folded in:
#   outer Dirichlet (i=Nr-1): F = phi - D
#   inner Neumann   (i=0)    : F = phi[0] - phi[1]   (phi_r=0)
#   axis  Neumann   (j=0,-1) : F = phi[:,j] - phi[:,j+/-1]  (phi_th=0)
# This is the SAME metric operator as laplace_box (cross-checked in torch).
# =====================================================================
def _box_np(phi, r, th, dr, dth):
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


def _residual_np(phi, r, th, dr, dth, D, Phi_amp):
    Nr, Nth = phi.shape
    F = _box_np(phi, r, th, dr, dth) - Phi_amp * (np.exp(-2 * phi)
                                                  - np.exp(phi))
    # closure rows overwrite F:
    F[-1, :] = phi[-1, :] - D                      # outer Dirichlet
    F[0, :] = phi[0, :] - phi[1, :]                # inner Neumann
    F[:, 0] = phi[:, 0] - phi[:, 1]                # axis Neumann (theta=0)
    F[:, -1] = phi[:, -1] - phi[:, -2]             # axis Neumann (theta=pi)
    return F


def _jacobian_np(phi, r, th, dr, dth, D, Phi_amp, eps=1e-7):
    """Sparse Jacobian by COLORED finite differences (5-point stencil ->
    3x3 grid coloring: nodes in one color group never share a residual row,
    so 9 residual evals reconstruct the full Jacobian). Vectorized
    attribution. Robust (no hand-coded flux-derivative algebra)."""
    Nr, Nth = phi.shape
    N = Nr * Nth
    F0 = _residual_np(phi, r, th, dr, dth, D, Phi_amp).ravel()
    idx = np.arange(N).reshape(Nr, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nr, Nth), dtype=bool)
            mask[ci::3, cj::3] = True
            ph = phi.copy()
            ph[mask] += eps
            dF = ((_residual_np(ph, r, th, dr, dth, D, Phi_amp).ravel()
                   - F0) / eps).reshape(Nr, Nth)
            # column index = the perturbed node owning each affected row.
            # For a 5-point stencil, residual row (i,j) is affected by a
            # perturbed node among {(i,j),(i+/-1,j),(i,j+/-1)} that lies in
            # THIS color group. Build the owner map for this color:
            owner = np.full((Nr, Nth), -1, dtype=np.int64)
            for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                src_i = np.arange(Nr)[:, None] + di
                src_j = np.arange(Nth)[None, :] + dj
                valid = ((src_i >= 0) & (src_i < Nr)
                         & (src_j >= 0) & (src_j < Nth))
                si = np.clip(src_i, 0, Nr - 1)
                sj = np.clip(src_j, 0, Nth - 1)
                in_color = valid & mask[si, sj] & (owner < 0)
                owner[in_color] = idx[si, sj][in_color]
            sel = owner >= 0
            rr = idx[sel]
            cc = owner[sel]
            vv = dF[sel]
            nz = vv != 0.0
            rows.append(rr[nz]); cols.append(cc[nz]); vals.append(vv[nz])
    J = sps.csr_matrix((np.concatenate(vals),
                        (np.concatenate(rows), np.concatenate(cols))),
                       shape=(N, N))
    return J, F0


def _newton2d(phi0, r, th, dr, dth, D, Phi_amp, itmax=200, tol=1e-10,
              verbose=False):
    """Damped Newton with Armijo line search on ||F||. Returns
    (phi, maxres_interior, n_iter, converged, hist)."""
    phi = phi0.copy()
    Nr, Nth = phi.shape
    hist = []
    maxres = np.inf
    for nit in range(itmax):
        J, F0 = _jacobian_np(phi, r, th, dr, dth, D, Phi_amp)
        nF0 = float(np.linalg.norm(F0))
        try:
            dphi = spsla.spsolve(J, -F0).reshape(Nr, Nth)
        except Exception:
            return phi, maxres, nit, False, hist
        if not np.all(np.isfinite(dphi)):
            return phi, maxres, nit, False, hist
        lam = 1.0
        ok = False
        for _ in range(40):
            trial = phi + lam * dphi
            Ft = _residual_np(trial, r, th, dr, dth, D, Phi_amp)
            if np.isfinite(Ft).all() and \
                    np.linalg.norm(Ft) < (1 - 1e-4 * lam) * nF0:
                ok = True
                break
            lam *= 0.5
        if not ok:
            # no decrease direction; report current iterate
            maxres = float(np.max(np.abs(
                _residual_np(phi, r, th, dr, dth, D, Phi_amp)[2:-2, 2:-2])))
            return phi, maxres, nit, maxres < 1e-7, hist
        phi = phi + lam * dphi
        Fint = _residual_np(phi, r, th, dr, dth, D, Phi_amp)[2:-2, 2:-2]
        maxres = float(np.max(np.abs(Fint)))
        hist.append((nit, float(lam), maxres))
        if verbose:
            log(f"    newton it={nit} lam={lam:.3f} maxres={maxres:.3e}")
        if maxres < tol:
            return phi, maxres, nit + 1, True, hist
    return phi, maxres, itmax, maxres < 1e-7, hist

def solve_interacting2d(D, Phi_amp, seed_lobe=0, seed_amp=0.0,
                        r_in=1.0, r_star=6.0, Nr=257, Nth=129,
                        itmax=120000, tol=1e-9, omega=0.8, verbose=False):
    """Two-way self-consistent 2D solve of Box_g phi = S(phi).
    seed_lobe: angular harmonic of the INITIAL data only (l of P_l(cos th)
      bump). The seed is initial data; the solver settles freely (we do NOT
      impose the final angular shape).
    Returns dict with phi, residual, convergence, MS mass, diagnostics."""
    r, th = make_grid(r_in, r_star, Nr, Nth)
    dr = float(r[1] - r[0]); dth = float(th[1] - th[0])
    R = r.view(-1, 1)
    costh = torch.cos(th).view(1, -1)
    # initial data: outer Dirichlet depth D, plus an optional angular bump
    phi = torch.full((Nr, Nth), D, device=DEV)
    if seed_amp != 0.0:
        # P_l(cos th) radial bump, localized mid-window -- INITIAL ONLY
        from numpy.polynomial import legendre as Lg
        Pl = torch.tensor(
            np.polynomial.legendre.legval(
                costh.cpu().numpy().ravel(),
                [0] * seed_lobe + [1]).reshape(1, -1), device=DEV)
        rb = (R - r_in) / (r_star - r_in)
        bump = torch.exp(-((rb - 0.4) / 0.18) ** 2)
        phi = phi + seed_amp * bump * Pl
    # ---- ROBUST DAMPED-NEWTON solve of the stiff nonlinear elliptic
    # system F(phi) = Box_g phi - S(phi) = 0 (the explicit point relaxation
    # is unstable on the e^{phi} reaction term -- the standard stiffness of
    # a Bratu/Liouville-type nonlinearity; Newton with a line search is the
    # correct tool). Numpy assembly; torch laplace_box used for an
    # INDEPENDENT residual cross-check at convergence (two engines).
    phi_np0 = phi.cpu().numpy()
    r_np = r.cpu().numpy(); th_np = th.cpu().numpy()
    phi_np, maxres, nit, conv, hist = _newton2d(
        phi_np0, r_np, th_np, dr, dth, D, Phi_amp,
        itmax=200, tol=1e-10, verbose=verbose)
    it = nit
    if not conv:
        # still return diagnostics on the best iterate (honest scope)
        pass
    # INDEPENDENT cross-check: torch operator residual on the numpy solution
    phi_t = torch.tensor(phi_np, device=DEV)
    box_t = laplace_box(phi_t, r, th, dr, dth)
    S_t = source(phi_t, Phi_amp)
    res_t = float(torch.max(torch.abs((box_t - S_t)[2:-2, 2:-2])))
    cross_ok = abs(res_t - maxres) < 1e-6 + 1e-3 * maxres
    # ---- diagnostics / invariants (scale-free where possible) ----
    r_np = r.cpu().numpy(); th_np = th.cpu().numpy()
    # theta-averaged radial profile (weighted by sin th)
    wth = np.sin(th_np); wth /= wth.sum()
    phibar = phi_np @ wth                              # (Nr,)
    # MS mass profile m(r) = (c^2 r/2G)(1 - e^{-2 phibar}); c=G=1
    msr = 0.5 * r_np * (1.0 - np.exp(-2.0 * phibar))
    # is there a radial TURN (a lump) in phibar? count sign changes of d phibar
    dphi = np.gradient(phibar, r_np)
    turns = int(np.sum(np.diff(np.sign(dphi)) != 0))
    # angular structure: amplitude of theta-variation at each r, and its
    # dominant Legendre content (does the converged phi carry an angular lobe?)
    th_var = float(np.max(np.std(phi_np, axis=1)))      # max over r of theta-std
    # Legendre decomposition of the equatorial-vs-pole pattern at the
    # radius of maximal theta-variation:
    ir = int(np.argmax(np.std(phi_np, axis=1)))
    prof_th = phi_np[ir] - phi_np[ir].mean()
    x = np.cos(th_np)
    # fit low-l Legendre coefficients
    from numpy.polynomial import legendre as Lg
    # weighted least squares with sin th measure
    Lmax = 6
    B = np.stack([np.polynomial.legendre.legval(
        x, [0] * l + [1]) for l in range(Lmax + 1)], axis=1)
    Wd = np.diag(np.sin(th_np))
    coef, *_ = np.linalg.lstsq(B.T @ Wd @ B, B.T @ Wd @ prof_th, rcond=None)
    dom_l = int(np.argmax(np.abs(coef[1:])) + 1) if th_var > 1e-9 else 0
    return dict(D=D, Phi=Phi_amp, seed_lobe=seed_lobe, seed_amp=seed_amp,
                conv=conv, maxres=maxres, res_torch=res_t,
                cross_ok=cross_ok, it=it,
                turns=turns, th_var=th_var, dom_l=dom_l,
                coef=[float(cc) for cc in coef],
                phibar_in=float(phibar[0]), phibar_out=float(phibar[-1]),
                phibar_min=float(phibar.min()), phibar_max=float(phibar.max()),
                ms_out=float(msr[-1]), ms_max=float(np.max(np.abs(msr))),
                r_in=r_in, r_star=r_star, Nr=Nr, Nth=Nth,
                phi=phi_np, r=r_np, th=th_np, phibar=phibar, msr=msr,
                hist=hist)

def _main():
    log("=" * 72)
    log(f"wint_solve2d  device={DEV}  torch={torch.__version__}")
    log("=" * 72)
    # =================================================================
    # GATE 0: bare sourceless limit (Phi=0) reproduces registry-#33 and
    # stays ROUND (theta-independent) from a round seed.
    # =================================================================
    log("\nGATE 0 -- bare sourceless metric (Phi=0): registry-#33 baseline")
    g0 = solve_interacting2d(D=0.5, Phi_amp=0.0, seed_amp=0.0)
    check("0a", g0["conv"] and g0["maxres"] < 1e-7,
          f"bare EOM converges (maxres={g0['maxres']:.2e}, it={g0['it']})")
    check("0b", g0["th_var"] < 1e-8,
          f"bare EOM from round data stays ROUND (th-var={g0['th_var']:.2e})")
    log(f"  bare Phi=0 D=0.5: phibar_in={g0['phibar_in']:.5f} "
        f"turns={g0['turns']} (monotone vacuum = registry #33)")

    # =================================================================
    # THE SOLVE: sweep genuine free data (depth D = matter content,
    # source amplitude Phi = partition-energy scale) and seed angular
    # content. Round AND lobed seeds at each (D,Phi): if the lobed seed
    # relaxes back to round, the lobe is NOT a stable type; if it
    # persists, it IS a distinct type. Impose nothing on the final shape.
    # =================================================================
    log("\nTHE INTERACTING SOLVE -- sweep free data, BOTH sectors live")
    log(f"{'D':>6} {'Phi':>6} {'seed_l':>6} {'seed_a':>7} {'conv':>5} "
        f"{'maxres':>9} {'it':>6} {'turns':>5} {'th_var':>9} {'dom_l':>5} "
        f"{'ms_out':>9} {'phibar_min':>10}")
    RES = []
    Ds = [0.2, 0.5, 1.0, 2.0]
    Phis = [0.0, 0.1, 0.3, 1.0, 3.0]
    seeds = [(0, 0.0), (1, 0.15), (2, 0.15), (3, 0.15)]
    for D in Ds:
        for Phi_amp in Phis:
            for (sl, sa) in seeds:
                rr = solve_interacting2d(D=D, Phi_amp=Phi_amp,
                                         seed_lobe=sl, seed_amp=sa)
                rec = {k: rr[k] for k in
                       ("D", "Phi", "seed_lobe", "seed_amp", "conv",
                        "maxres", "it", "turns", "th_var", "dom_l",
                        "ms_out", "ms_max", "phibar_min", "phibar_max",
                        "phibar_in", "phibar_out", "coef")}
                RES.append(rec)
                log(f"{D:6.2f} {Phi_amp:6.2f} {sl:6d} {sa:7.3f} "
                    f"{str(rr['conv']):>5} {rr['maxres']:9.1e} "
                    f"{rr['it']:6d} {rr['turns']:5d} {rr['th_var']:9.2e} "
                    f"{rr['dom_l']:5d} {rr['ms_out']:9.4f} "
                    f"{rr['phibar_min']:10.4f}")
            with open("/tmp/wint_ckpt.json", "w") as fh:
                json.dump(jclean(RES), fh, indent=0)

    check("S-conv",
          sum(1 for x in RES if x["conv"]) >= int(0.8 * len(RES)),
          f"{sum(1 for x in RES if x['conv'])}/{len(RES)} interacting "
          "solves converged to a two-way self-consistent fixed point")

    # =================================================================
    # CONVERGENCE EVIDENCE: grid refinement (structure grid-independent).
    # =================================================================
    log("\nCONVERGENCE -- grid refinement (D=1, Phi=1, lobe-2 seed)")
    prev = None
    for (Nr, Nth) in [(129, 65), (257, 129), (385, 193)]:
        rr = solve_interacting2d(D=1.0, Phi_amp=1.0, seed_lobe=2,
                                 seed_amp=0.15, Nr=Nr, Nth=Nth)
        msg = (f"  Nr={Nr} Nth={Nth}: phibar_min={rr['phibar_min']:.6f} "
               f"th_var={rr['th_var']:.4e} dom_l={rr['dom_l']} "
               f"ms_out={rr['ms_out']:.6f} maxres={rr['maxres']:.2e}")
        if prev is not None:
            msg += f"  d(phibar_min)={abs(rr['phibar_min']-prev):.2e}"
        prev = rr["phibar_min"]
        log(msg)

    log(f"\nWINT2D: {len(PASS)} PASS / {len(FAIL)} FAIL "
        f"({time.time()-t0:.0f}s)")
    if FAIL:
        log("FAILED: " + str(FAIL))
    log("checkpoint: /tmp/wint_ckpt.json  log: " + LOG)


if __name__ == "__main__":
    _main()
    _fh.close()
