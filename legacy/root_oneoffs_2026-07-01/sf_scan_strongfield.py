#!/usr/bin/env python3
"""
sf_scan_strongfield.py -- STRONG-FIELD / OFF-DIAGONAL whole-metric scan
=======================================================================
Queue-head step (b), STRONG-FIELD / OFF-DIAGONAL axis. Driver: Claude
(Opus 4.8). Date 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md. New file.

THE AXIS (solution_space_baseline.md, last table row): the documented
interior baseline (B1, registry #34/#36) -- round-cell Jacobian
NON-SINGULAR, angular operator pure damping, ONE round type -- was proven
in a TRUST WINDOW: modest depth (E/Um up to 6, exp(-2v)~16) and the
angular drive effectively OFF (only the dressed scalar operator, no live
off-diagonal). The named OPEN frontier: "the fully two-way, unfrozen,
strong-field off-diagonal (large shear, q-on, deep core toward phi->-inf)
solution is not mapped; whether documented invariants persist there is
open."

THIS SCAN, two complementary probes, BOTH on the metric's OWN derived
operators, NOTHING frozen/slaved/added, NO linearization as a result:

  PROBE 1 (SCALAR, STRONG FIELD). Reuse the EXACT wint two-way residual
    and existence-test (the metric's own e^{2v}-dressed angular operator +
    ON two-exponential source; v(m,theta) live both sectors). Push the
    partition energy E -- hence the core depth |v_min| and the
    nonlinearity exp(-2 v_min) -- FAR past the trust window (E/Um up to
    ~1000, exp(-2v) up to ~3000). Track the existence-test Jacobian
    min|eig| across this strong-field family. B1 says it never zeros in
    the trust window. DOES IT DEVELOP A ZERO / SIGN CHANGE AT STRONG FIELD
    (= a bifurcation = a distinct shaped type born deep in the core)?
    Linearization-validity is reported at every point (exp(-2 v_min)); we
    are NOT relying on any linearization -- the full nonlinear residual is
    solved and the Jacobian is the EXACT FD Jacobian of that residual.

  PROBE 2 (OFF-DIAGONAL LIVE). The metric's OWN derived reduced potential
    for the ell=1 off-diagonal / sheared class f = F(y)(1 + kappa cos th)
    (sourced_second_jet finding 6, verifier-confirmed to 1e-12):
        P(F,a) = (3 a^2 / 2F) G1(kappa),  a = F*kappa,
        G1(kappa) = (2 kappa + (kappa^2 - 1) L)/kappa^3,
        L = ln((1+kappa)/(1-kappa)).
    This carries the OFF-DIAGONAL (g_rtheta-type) shape amplitude kappa as
    a LIVE field co-equal with F -- the angular drive ON. The documented
    facts: (i) degree-1 homogeneity in f => EXACT rank-1 Hessian (one null
    = the scaling direction); (ii) kappa -> 1 is metric degeneration at
    finite depth; the trust window stops ~kappa 0.97. THE TEST: as we push
    field strength (kappa) up toward 1 (strong field / large shear), does
    the rank-1 Hessian DEVELOP A SECOND null or a NEGATIVE eigenvalue (a
    shaped bifurcation -- a distinct off-diagonal type), and does the
    derived phi-angular cross-block (V_a0gamma0 = -sqrt(15)kappa/3F,
    V_a1gamma1 = -sqrt(5)kappa/2F) reach a regime where it overturns the
    positive shape stiffness? We map the FULL reduced-potential Hessian
    eigenstructure across kappa in [0.01, 0.999] (the whole approach to
    the documented degeneration), well past the 0.97 trust edge.

GPU: V100 torch float64 for the broad strong-field eigensolve sweep
(PROBE 1's Jacobian spectra batched); CPU mpmath anchors. Heeds the
broadcast-Cholesky pitfall (we do dense eig, not triangular solves).
Honest negative reporting first-class. Log /tmp/sf_scan.log.
HYPOTHESIS-GRADE; flag for blind verifier.
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
import mpmath as mp

t0 = time.time()
_fh = open("/tmp/sf_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL, FLAG = [], [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    log(f"SF-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 72)
log("sf_scan_strongfield -- STRONG-FIELD / OFF-DIAGONAL whole-metric scan")
log("=" * 72)

try:
    import torch
    HAS_GPU = torch.cuda.is_available()
    DEV = torch.device("cuda" if HAS_GPU else "cpu")
    log(f"torch {torch.__version__} cuda={HAS_GPU} dev={DEV}")
except Exception as e:
    HAS_GPU = False; DEV = None
    log(f"no torch ({e}); CPU numpy only")

# =====================================================================
# Shared radial cell (the metric's own ON two-exponential well; banked
# w_whole_gm PART D / w_alg PART E; taken verbatim from wint, not invented).
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
        for _ in range(400):
            if g(b) > 0:
                return mp.findroot(g, (a, b), solver='bisect')
            a, b = b, b * mp.mpf('1.25')
            if abs(b) > 200: break
        return None
    vlo = bracket(-1); vhi = bracket(+1)
    if vlo is None or vhi is None: return None
    L = mp.quad(lambda v: 1 / mp.sqrt(max(2 * (E - U(v, Phi)),
                mp.mpf('1e-40'))), [vlo, vhi])
    return float(L), float(vlo), float(vhi)

# =====================================================================
# THE EXACT wint residual + jacobian (the metric's own EL; verbatim from
# wint_cell2d.py PART B, NOTHING changed -- we only drive it strong-field).
# =====================================================================
def residual(v, m, th, dm, dth, Phi_amp, vlo):
    Nm, Nth = v.shape
    vmm = np.zeros_like(v)
    vmm[1:-1, :] = (v[2:, :] - 2 * v[1:-1, :] + v[:-2, :]) / dm ** 2
    sinth = np.sin(th)[None, :]
    am = 0.5 * (sinth[:, 1:] + sinth[:, :-1])
    flux = am * (v[:, 1:] - v[:, :-1]) / dth
    ang = np.zeros_like(v)
    ang[:, 1:-1] = (flux[:, 1:] - flux[:, :-1]) / dth / sinth[:, 1:-1]
    vth = np.zeros_like(v)
    vth[:, 1:-1] = (v[:, 2:] - v[:, :-2]) / (2 * dth)
    A = np.exp(2.0 * v) * (ang - vth ** 2)
    F = vmm + A - Phi_amp * (np.exp(-2 * v) - np.exp(v))
    F[0, :] = v[0, :] - vlo            # center depth anchor (energy label)
    F[-1, :] = v[-1, :] - v[-2, :]     # outer Neumann turning point
    F[:, 0] = v[:, 0] - v[:, 1]        # axis Neumann
    F[:, -1] = v[:, -1] - v[:, -2]
    return F

def jac(v, m, th, dm, dth, Phi_amp, vlo, eps=1e-7):
    Nm, Nth = v.shape; N = Nm * Nth
    F0 = residual(v, m, th, dm, dth, Phi_amp, vlo).ravel()
    idx = np.arange(N).reshape(Nm, Nth)
    rows, cols, vals = [], [], []
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nm, Nth), dtype=bool)
            mask[ci::3, cj::3] = True
            vp = v.copy(); vp[mask] += eps
            dF = ((residual(vp, m, th, dm, dth, Phi_amp, vlo).ravel()
                   - F0) / eps).reshape(Nm, Nth)
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

def newton(v0, m, th, dm, dth, Phi_amp, vlo, itmax=200, tol=1e-10):
    v = v0.copy(); maxres = np.inf
    for nit in range(itmax):
        J, F0 = jac(v, m, th, dm, dth, Phi_amp, vlo)
        n0 = float(np.linalg.norm(F0))
        try:
            dv = spsla.spsolve(J, -F0).reshape(v.shape)
        except Exception:
            return v, maxres, nit, False
        if not np.all(np.isfinite(dv)):
            return v, maxres, nit, False
        lam = 1.0; ok = False
        for _ in range(50):
            tr = v + lam * dv
            if np.all(np.abs(tr) < 60):
                Ft = residual(tr, m, th, dm, dth, Phi_amp, vlo)
                if np.isfinite(Ft).all() and \
                        np.linalg.norm(Ft) < (1 - 1e-4 * lam) * n0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            maxres = float(np.max(np.abs(residual(
                v, m, th, dm, dth, Phi_amp, vlo)[1:-1, 1:-1])))
            return v, maxres, nit, maxres < 1e-8
        v = v + lam * dv
        maxres = float(np.max(np.abs(residual(
            v, m, th, dm, dth, Phi_amp, vlo)[1:-1, 1:-1])))
        if maxres < tol:
            return v, maxres, nit + 1, True
    return v, maxres, itmax, maxres < 1e-8

def solve2d(E_factor, Phi_amp=1.0, Nm=97, Nth=33):
    Phi_m = mp.mpf(Phi_amp)
    E = Umin(Phi_m) * mp.mpf(E_factor)
    res = cell_LE(E, Phi_m)
    if res is None: return dict(conv=False, why="below_well")
    L, vlo, vhi = res
    m = np.linspace(0.0, L, Nm); th = np.linspace(0.0, np.pi, Nth)
    dm = m[1] - m[0]; dth = th[1] - th[0]
    vr = np.zeros(Nm); vv = vlo; pp = 0.0; vr[0] = vv
    for i in range(1, Nm):
        def f(vv, pp): return pp, float(Phi_m)*(np.exp(-2*vv)-np.exp(vv))
        k1 = f(vv, pp); k2 = f(vv+dm/2*k1[0], pp+dm/2*k1[1])
        k3 = f(vv+dm/2*k2[0], pp+dm/2*k2[1]); k4 = f(vv+dm*k3[0], pp+dm*k3[1])
        vv += dm/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        pp += dm/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]); vr[i] = vv
    v0 = np.tile(vr[:, None], (1, Nth))
    v, maxres, nit, conv = newton(v0, m, th, dm, dth, float(Phi_m), vlo)
    th_var = float(np.max(np.std(v, axis=1)))
    return dict(E=float(E), L=L, vlo=vlo, vhi=vhi, conv=conv, maxres=maxres,
                nit=nit, th_var=th_var, v=v, m=m, th=th, dm=dm, dth=dth,
                vmin=float(v.min()), vmax=float(v.max()),
                nonlin=float(np.exp(-2*v.min())))

# =====================================================================
# PROBE 1 -- STRONG-FIELD existence test. Push E far past the trust window
# and watch the existence-test Jacobian min|eig|. GPU dense eig (batched
# over the family is impossible -- different N per E -- but each dense eig
# is GPU-accelerated). NOTHING frozen; full nonlinear solve at each E.
# =====================================================================
def _probe1():
    log("\n" + "=" * 72)
    log("PROBE 1 -- SCALAR STRONG FIELD: existence-test Jacobian min|eig|")
    log("  vs core depth. Baseline B1: non-singular in the TRUST window")
    log("  (E/Um<=6, nonlin<=16). We push to E/Um~1000 (nonlin~3000).")
    log("=" * 72)
    log(f"{'E/Um':>8} {'L':>9} {'v_min':>8} {'v_max':>8} {'nonlin':>11} "
        f"{'conv':>5} {'maxres':>9} {'th_var':>9} {'min|eig|':>11} {'sign':>5}")
    Efs = [1.1, 2.0, 4.0, 6.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0]
    rows = []
    for Ef in Efs:
        r = solve2d(Ef, Nm=97, Nth=33)
        if not r["conv"]:
            log(f"{Ef:8.1f}  (no converge: {r.get('why','newton')})")
            rows.append(dict(Ef=Ef, conv=False)); continue
        v = r["v"]; m = r["m"]; th = r["th"]; dm = r["dm"]; dth = r["dth"]
        vlo = r["vlo"]
        J, _ = jac(v, m, th, dm, dth, 1.0, vlo)
        Jd = J.toarray()
        if HAS_GPU:
            Jt = torch.tensor(Jd, dtype=torch.float64, device=DEV)
            ev = torch.linalg.eigvals(Jt).cpu().numpy()
        else:
            ev = np.linalg.eigvals(Jd)
        me = float(np.min(np.abs(ev)))
        allpos = bool(np.all(ev.real > 1e-9))
        allneg = bool(np.all(ev.real < -1e-9))
        sign = "+" if allpos else ("-" if allneg else "mix")
        rows.append(dict(Ef=Ef, conv=True, L=r["L"], vmin=r["vmin"],
                         vmax=r["vmax"], nonlin=r["nonlin"], maxres=r["maxres"],
                         th_var=r["th_var"], mineig=me, sign=sign))
        log(f"{Ef:8.1f} {r['L']:9.4f} {r['vmin']:8.3f} {r['vmax']:8.3f} "
            f"{r['nonlin']:11.2e} {str(r['conv']):>5} {r['maxres']:9.1e} "
            f"{r['th_var']:9.2e} {me:11.5f} {sign:>5}")
    conv = [x for x in rows if x.get("conv")]
    strong = [x for x in conv if x["nonlin"] > 16]   # past trust window
    log(f"\n  converged strong-field points (nonlin>16): {len(strong)}")
    if strong:
        mineigs = [x["mineig"] for x in strong]
        log(f"  strong-field min|eig| range: {min(mineigs):.5f} .. "
            f"{max(mineigs):.5f}")
        log(f"  trust-window (nonlin<=16) min|eig| range: "
            f"{min(x['mineig'] for x in conv if x['nonlin']<=16):.5f} .. "
            f"{max(x['mineig'] for x in conv if x['nonlin']<=16):.5f}")
        # FLAG if the Jacobian approaches a zero (bifurcation) at strong field
        approaching = [x for x in strong if x["mineig"] < 1e-3]
        if approaching:
            FLAG.append(("P1-zero", [(x["Ef"], x["mineig"]) for x in approaching]))
            log(f"  *** FLAG P1: min|eig| dropped below 1e-3 at strong field "
                f"(near-bifurcation): {[(x['Ef'], round(x['mineig'],6)) for x in approaching]}")
        anymix = [x for x in strong if x["sign"] == "mix"]
        if anymix:
            log(f"  NOTE: sign='mix' at {[x['Ef'] for x in anymix]} -- but the "
                "raw FD Jacobian carries BC-row spurious eigenvalues; the "
                "min|eig| MAGNITUDE is the reliable bifurcation diagnostic.")
    check("P1", len(conv) >= 7,
          f"{len(conv)}/{len(rows)} strong-field scalar solves converged; "
          "existence-test Jacobian mapped across the deep-core family")
    with open("/tmp/sf_probe1.json", "w") as fh:
        json.dump(rows, fh, indent=0, default=str)
    return rows

if __name__ == "__main__":
    _probe1()
    log(f"\nSF(probe1): {len(PASS)} PASS / {len(FAIL)} FAIL "
        f"({time.time()-t0:.0f}s)")
    _fh.close()
