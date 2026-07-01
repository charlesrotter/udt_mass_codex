"""W5 ARM-2 ADVERSARIAL VERIFIER #3 — FRESH MEMBERS + INDEPENDENT
EDGE MACHINERY (refutation attempt of the domain-graded ratio break).

Date: 2026-06-12.  New file; never edits committed files.  Does NOT
import the claimant's w5_arm2_lib.  Imports ONLY the committed,
previously-verified w4b_verifier_lib (member flow / cstar_bisect /
chart conventions p = f e^{-t}, b = (f_th^2/f) e^{-t}).

CLAIM UNDER ATTACK (W5 untruncated species, TRUE units cc=2):
  OFF static: (p v')' = (1/(8k)) b (1 - 2k/f) e^{-2v}
  ON  static: (p v')' = (1/(8k)) b [(1-2k/f) e^{-2v} - e^{v}]
  dressed pencil: -(p psi')' - [(1/(4k))(1-2k/f) e^{-2vb}
                  + (1/(8k)) e^{vb}] b psi = w2 (e^{-3t}/f) psi
  BCs: Neumann (natural) at weld t=0, Dirichlet at inner cut t_b.
  kappa_s  = smallest kappa with all-ray OFF equilibria (existence at
             LARGE kappa; member edge set by the LAST ray to hold on,
             i.e. max over per-ray fold kappas).
  kappa_c' = largest kappa with min-over-rays dressed ON pencil
             eigenvalue < 0 (no ON equilibrium => "in band").
  Claimed: full-domain ratio ks/kc' member-DEPENDENT (1.349/1.585/
  1.591 on M1/M2/M4); t5-window ratio member-INDEPENDENT ~1.84;
  mechanism = flipped region f < 2k overlapping the b seal weight.

INDEPENDENT CHOICES (vs the claimant's w5_arm2_lib):
  - geometry evaluated from the flow DENSE OUTPUT directly on each
    window grid (no member-grid re-interpolation);
  - per-ray fold kappas by geometric ladder DOWN from large kappa +
    warm-started bisection (claimant: member-level log-bisection);
    member ks = max over rays — same object, different route;
  - own damped Newton, own FD/FEM assembly, own brackets;
  - trust cuts t1/t5 recomputed from scratch with an own 3-mode flow.

Verifier agent VB5 (fresh-member attack), 2026-06-12.
"""
import sys
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import solve_banded, eigh_tridiagonal

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl

LOG = open("/tmp/w5_arm2_verifier3_fresh.log", "a")


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    LOG.write(msg + "\n")
    LOG.flush()


# ------------------------------------------------------------ geometry
class Geo:
    """Per-ray t-chart geometry on [0, t_b] from the dense flow
    solution (no re-interpolation)."""

    def __init__(self, sol, t_b=None, Nt=4000, Nu=24):
        self.t_stop = float(sol.t_events[0][0])
        self.t_b = self.t_stop if t_b is None else float(t_b)
        assert self.t_b <= self.t_stop + 1e-12
        self.Nt, self.Nu = Nt, Nu
        self.tg = np.linspace(0.0, self.t_b, Nt)
        Z = sol.sol(self.tg)
        X = Z[:4].T
        un, wu = np.polynomial.legendre.leggauss(Nu)
        self.u, self.wu = un, wu
        Y, Yu = vl.Yr(un), vl.Yru(un)
        self.f = X @ Y                       # (Nt, Nu)
        fu = X @ Yu
        self.fth2 = (1 - un[None, :] ** 2) * fu ** 2
        et = np.exp(-self.tg)[:, None]
        self.p = self.f * et
        self.b = self.fth2 / self.f * et
        self.m = np.exp(-3 * self.tg)[:, None] / self.f


# --------------------------------------------- static equilibria (own)
def src_coef(geo, k, kappa, dcell, species=True):
    """returns (A, B) with RHS = A e^{-2v} - B e^{v} for ray k:
    A = (1/(8k)) b fac, B = (1/(8k)) b (dcell) else 0."""
    b = geo.b[:, k]
    f = geo.f[:, k]
    fac = (1.0 - 2.0 * kappa / f) if species else np.ones_like(f)
    A = b * fac / (8.0 * kappa)
    B = b / (8.0 * kappa) if dcell else np.zeros_like(b)
    return A, B


def newton_ray(geo, k, kappa, dcell, species=True, vinit=None,
               tol=1e-11, maxit=120):
    """damped Newton for (p v')' = A e^{-2v} - B e^{v},
    natural Neumann at t=0, Dirichlet v=0 at t_b.  Returns v or None."""
    h = geo.tg[1] - geo.tg[0]
    p = geo.p[:, k]
    N = geo.Nt
    pm = 0.5 * (p[1:] + p[:-1])
    A, B = src_coef(geo, k, kappa, dcell, species)
    w = np.full(N, h)
    w[0] = 0.5 * h                      # half cell at the weld
    v = np.zeros(N) if vinit is None else vinit.copy()
    for it in range(maxit):
        em2, ep1 = np.exp(-2 * v), np.exp(v)
        R = A * em2 - B * ep1
        F = np.zeros(N)
        F[1:-1] = (pm[1:] * (v[2:] - v[1:-1])
                   - pm[:-1] * (v[1:-1] - v[:-2])) / h \
            - w[1:-1] * R[1:-1]
        F[0] = pm[0] * (v[1] - v[0]) / h - w[0] * R[0]
        F[-1] = v[-1]
        dR = -2 * A * em2 - B * ep1     # dR/dv
        di = np.zeros(N)
        up = np.zeros(N)
        lo = np.zeros(N)
        di[1:-1] = -(pm[1:] + pm[:-1]) / h - w[1:-1] * dR[1:-1]
        up[1:-1] = pm[1:] / h
        lo[1:-1] = pm[:-1] / h
        di[0] = -pm[0] / h - w[0] * dR[0]
        up[0] = pm[0] / h
        di[-1] = 1.0
        ab = np.zeros((3, N))
        ab[0, 1:] = up[:-1]
        ab[1] = di
        ab[2, :-1] = lo[1:]
        try:
            dv = solve_banded((1, 1), ab, -F)
        except Exception:
            return None
        if not np.all(np.isfinite(dv)):
            return None
        step = float(np.max(np.abs(dv)))
        damp = 1.0 if step < 0.4 else 0.4 / step
        v = v + damp * dv
        if not np.all(np.isfinite(v)) or v.min() < -16 or v.max() > 40:
            return None
        if step * damp < tol:
            return v
    return None


def fold_ray_kappa(geo, k, dcell=False, species=True, khi=64.0,
                   rel=1e-8):
    """per-ray OFF existence edge in kappa: ladder DOWN from khi
    (exists) + warm bisection.  Returns (k_edge, v_at_edge) or
    (None, None) if no equilibrium even at khi."""
    v = newton_ray(geo, k, khi, dcell, species)
    if v is None:
        # climb up to find existence
        kk = khi
        for _ in range(8):
            kk *= 4.0
            v = newton_ray(geo, k, kk, dcell, species)
            if v is not None:
                khi = kk
                break
        if v is None:
            return None, None
    kgood, vgood = khi, v
    fac = 0.5
    while True:
        ktry = kgood * fac
        v2 = newton_ray(geo, k, ktry, dcell, species, vinit=vgood)
        if v2 is not None:
            kgood, vgood = ktry, v2
            continue
        if fac > 1.0 - 1e-9:
            break
        fac = np.sqrt(fac)
    lo_bad, hi_good = kgood * fac, kgood
    while (hi_good - lo_bad) / hi_good > rel:
        mid = np.sqrt(lo_bad * hi_good)
        v2 = newton_ray(geo, k, mid, dcell, species, vinit=vgood)
        if v2 is None:
            lo_bad = mid
        else:
            hi_good, vgood = mid, v2
    return 0.5 * (lo_bad + hi_good), vgood


def ks_member(geo, species=True):
    """member kappa_s = max over per-ray OFF fold kappas; returns
    (ks, critical ray, per-ray array)."""
    edges = np.full(geo.Nu, np.nan)
    for k in range(geo.Nu):
        e, _ = fold_ray_kappa(geo, k, dcell=False, species=species)
        edges[k] = np.nan if e is None else e
    kc = int(np.nanargmax(edges))
    return float(edges[kc]), kc, edges


# ------------------------------------------------------ dressed pencil
def pencil_lowest(geo, k, kappa, dcell, species=True, vbar=None):
    """lowest w2 of -(p psi')' + q psi = w2 m psi (FD, lumped mass,
    natural Neumann at weld, Dirichlet at t_b)."""
    h = geo.tg[1] - geo.tg[0]
    p = geo.p[:, k]
    b = geo.b[:, k]
    m = geo.m[:, k]
    f = geo.f[:, k]
    N = geo.Nt
    vb = np.zeros(N) if vbar is None else vbar
    fac = (1.0 - 2.0 * kappa / f) if species else np.ones(N)
    q = -(1.0 / (4.0 * kappa)) * fac * np.exp(-2 * vb) * b
    if dcell:
        q = q - (1.0 / (8.0 * kappa)) * np.exp(vb) * b
    pm = 0.5 * (p[1:] + p[:-1])
    w = np.full(N, h)
    w[0] = w[-1] = 0.5 * h
    dmain = np.zeros(N)
    dmain[:-1] += pm / h
    dmain[1:] += pm / h
    dmain += q * w
    doff = -pm / h
    M = m * w
    # Dirichlet at last node; symmetric scaling by 1/sqrt(M)
    Mi = 1.0 / np.sqrt(M[:-1])
    d = dmain[:-1] * Mi ** 2
    e = doff[:-1] * Mi[:-1] * Mi[1:]
    w2 = eigh_tridiagonal(d, e, select='i', select_range=(0, 0),
                          eigvals_only=True)
    return float(w2[0])


def w2min_dressed(geo, kappa, dcell=True, species=True, vinits=None):
    """min over rays of the dressed lowest pencil ev; None if any ray
    lacks an ON equilibrium ('in band').  Returns (w2min, vbars)."""
    vbars = np.zeros((geo.Nu, geo.Nt))
    for k in range(geo.Nu):
        vi = None if vinits is None else vinits[k]
        v = newton_ray(geo, k, kappa, dcell, species, vinit=vi)
        if v is None:
            return None, None
        vbars[k] = v
    w2s = [pencil_lowest(geo, k, kappa, dcell, species, vbar=vbars[k])
           for k in range(geo.Nu)]
    return min(w2s), vbars


def kc_member(geo, species=True, klo=1e-4, khi=50.0, nbis=34):
    """kappa_c' = largest kappa with w2min < 0 (None counts as <0)."""
    wlo, _ = w2min_dressed(geo, klo, species=species)
    whi, vhi = w2min_dressed(geo, khi, species=species)
    if not ((wlo is None or wlo < 0) and (whi is not None and whi >= 0)):
        log(f"    kc bracket FAILED: w2(lo)={wlo} w2(hi)={whi}")
        return None
    lo, hi = klo, khi
    vgood = vhi
    for _ in range(nbis):
        mid = np.sqrt(lo * hi)
        wm, vm = w2min_dressed(geo, mid, species=species, vinits=vgood)
        if wm is None or wm < 0:
            lo = mid
        else:
            hi = mid
            vgood = vm
    return float(np.sqrt(lo * hi))


# ------------------------------------------------------- flip overlap
def flip_overlap(geo, kappa, kray):
    """b-weight fraction with f < 2 kappa: (critical ray, all-ray
    wu-weighted)."""
    mask = geo.f < 2.0 * kappa
    bc = geo.b[:, kray]
    fr_ray = float(bc[mask[:, kray]].sum() / bc.sum())
    tot = (geo.b * geo.wu[None, :]).sum()
    flip = (geo.b * geo.wu[None, :])[mask].sum()
    return fr_ray, float(flip / tot)


# ------------------------------------------- trust cuts (own 3-mode)
XG, WG = vl.XG2000, vl.WG2000
Y3G, Yu3G = vl.YG2000[:3], vl.YuG2000[:3]
SG = vl.SG2000


def Pgrad3(X):
    fv = X @ Y3G
    fu = X @ Yu3G
    return (SG * (2 * fu * Yu3G / fv - fu * fu * Y3G / fv ** 2)) @ WG / 8.0


def fmin3(X3):
    return vl.fmin_exact(np.array([X3[0], X3[1], X3[2], 0.0]))


def flow3(gamma, c, fstop=0.002, Tmax=10.0):
    def rhs(t, z):
        X, Xt = z[:3], z[3:]
        return np.concatenate([Xt, Xt + 2 * Pgrad3(X)])

    def ev(t, z):
        return fmin3(z[:3]) - fstop
    ev.terminal, ev.direction = True, -1
    z0 = np.array([1.0, 0, 0, gamma, -c, 0])
    return solve_ivp(rhs, (0, Tmax), z0, method='DOP853', rtol=1e-11,
                     atol=1e-12, dense_output=True, events=ev)


def trust_cuts(gamma, c, sol4):
    """t1 (1%), t5 (5%) cuts of |fmin_ell2/fmin_ell3 - 1| (the bg
    library criterion), own implementation."""
    s3 = flow3(gamma, c)
    tstop3 = (float(s3.t_events[0][0]) if len(s3.t_events[0])
              else float(s3.t[-1]))
    tstop4 = float(sol4.t_events[0][0])
    tmax = min(tstop3, tstop4)
    tg = np.linspace(1e-6, tmax * 0.99999, 6000)
    f3 = np.array([fmin3(s3.sol(t)[:3]) for t in tg])
    f4 = np.array([vl.fmin_exact(sol4.sol(t)[:4]) for t in tg])
    dev = np.abs(f3 / f4 - 1.0)
    cuts = {}
    for lab, thr in (("t1", 0.01), ("t5", 0.05)):
        idx = np.where(dev > thr)[0]
        if len(idx) == 0:
            cuts[lab] = None
            continue
        i = idx[0]
        if i == 0:
            cuts[lab] = float(tg[0])
        else:
            a = (thr - dev[i - 1]) / (dev[i] - dev[i - 1])
            cuts[lab] = float(tg[i - 1] + a * (tg[i] - tg[i - 1]))
    return cuts["t1"], cuts["t5"]


# ------------------------------------------------------------ drivers
def member_block(name, gamma, c, sol, t_b, Nt=4000, do_double=True):
    """full edge set on one (member, window)."""
    geo = Geo(sol, t_b=t_b, Nt=Nt)
    t0 = time.time()
    ks, kray, edges = ks_member(geo)
    t1 = time.time()
    kc = kc_member(geo)
    t2 = time.time()
    fr_ray, fr_all = flip_overlap(geo, ks, kray)
    ratio = ks / kc if kc else np.nan
    log(f"  {name}: t_b={geo.t_b:.4f} Nt={Nt}")
    log(f"    ks={ks:.6f} (critical ray {kray}, u={geo.u[kray]:+.4f}) "
        f"[{t1-t0:.1f}s]")
    log(f"    kc'={kc:.6f} [{t2-t1:.1f}s]  RATIO ks/kc'={ratio:.4f}")
    log(f"    flip overlap (b-weight frac, f<2ks): ray={fr_ray:.4f} "
        f"all={fr_all:.4f}")
    out = dict(ks=ks, kc=kc, ratio=ratio, kray=kray,
               fr_ray=fr_ray, fr_all=fr_all, edges=edges)
    if do_double:
        geo2 = Geo(sol, t_b=t_b, Nt=2 * Nt)
        e2, _ = fold_ray_kappa(geo2, kray)
        log(f"    [grid] ks critical-ray fold Nt={2*Nt}: {e2:.6f} "
            f"(rel dev {abs(e2-edges[kray])/edges[kray]:.2e})")
        out["ks_dbl"] = e2
    return out


CLAIMS = {
    ("M1", "full"): (0.915696, 0.678857, 1.349),
    ("M1", "t5"): (0.076078, 0.041396, 1.838),
    ("M2", "full"): (0.255321, 0.161096, 1.585),
    ("M2", "t5"): (0.044942, 0.024358, 1.845),
    ("M4", "full"): (0.282425, 0.177554, 1.591),
    ("M4", "t5"): (0.045333, 0.024529, 1.848),
}


def main():
    log("=" * 72)
    log("W5 ARM-2 VERIFIER #3 (fresh members + independent machinery)")
    log(time.strftime("%Y-%m-%d %H:%M:%S"))
    log("=" * 72)

    # ---------------- TASK 1: validate machinery on M1 (+M2, M4 cheap)
    log("\n[T1] MACHINERY VALIDATION on claimed members")
    claimed_members = [("M1", 1.0, 0.18413678, 2.2357),
                       ("M2", 1.0, 0.28328735, 1.5313),
                       ("M4", 0.5, 0.09087158, 2.1312)]
    res = {}
    for name, g, c, t5 in claimed_members:
        sol = vl.flow(g, c)
        log(f" member {name}: gamma={g} c={c} "
            f"t_stop={float(sol.t_events[0][0]):.6f}")
        for win, tb in (("full", None), ("t5", t5)):
            r = member_block(f"{name}/{win}", g, c, sol, tb,
                             do_double=(name == "M1"))
            res[(name, win)] = r
            ck = CLAIMS[(name, win)]
            dks = abs(r["ks"] - ck[0]) / ck[0]
            dkc = abs(r["kc"] - ck[1]) / ck[1]
            ok = "PASS" if (dks <= 1e-2 and dkc <= 1e-2) else "FAIL"
            log(f"    vs CLAIM ks={ck[0]} kc'={ck[1]}: "
                f"rel dev ks={dks:.2e} kc={dkc:.2e}  -> {ok}")

    # ---------------- TASK 2: trust-cut criterion validation + fresh
    log("\n[T2] TRUST-CUT CRITERION validation on M1/M2/M4")
    bank = {"M1": (1.6383, 2.2357), "M2": (1.1680, 1.5313),
            "M4": (1.7106, 2.1312)}
    for name, g, c, _ in claimed_members:
        sol = vl.flow(g, c)
        t1c, t5c = trust_cuts(g, c, sol)
        b1, b5 = bank[name]
        log(f"  {name}: own t1={t1c:.4f} (bank {b1}, "
            f"dev {abs(t1c-b1)/b1*100:.2f}%), own t5={t5c:.4f} "
            f"(bank {b5}, dev {abs(t5c-b5)/b5*100:.2f}%)")

    log("\n[T2b] FRESH MEMBERS via cstar_bisect")
    cs1 = vl.cstar_bisect(1.0, 0.10, 0.20)
    log(f"  c*(1.0) = {cs1:.6f}  (anchor 0.141644, "
        f"dev {abs(cs1-0.141644)/0.141644:.2e})")
    cs05 = vl.cstar_bisect(0.5, 0.02, 0.10)
    log(f"  c*(0.5) = {cs05:.6f}  (bg-header implies 0.045436)")
    # bracket for gamma=2: try wide
    lo2, hi2 = 0.15, 0.80
    if vl.sealed(2.0, lo2, rtol=1e-9):
        lo2 = 0.02
    if not vl.sealed(2.0, hi2, rtol=1e-9):
        hi2 = 2.0
    cs2 = vl.cstar_bisect(2.0, lo2, hi2)
    log(f"  c*(2.0) = {cs2:.6f}")

    fresh = [("F1", 1.0, 1.6 * cs1), ("F2", 0.5, 3.0 * cs05),
             ("F3", 2.0, 1.5 * cs2)]

    # ---------------- TASK 3: fresh-member edges
    log("\n[T3] FRESH MEMBER EDGES (full + t5)")
    table = []
    for name, g, c in fresh:
        sol = vl.flow(g, c)
        ts = float(sol.t_events[0][0])
        t1c, t5c = trust_cuts(g, c, sol)
        log(f" member {name}: gamma={g} c={c:.6f} t_stop={ts:.6f} "
            f"t1={t1c:.4f} t5={t5c:.4f}")
        rfull = member_block(f"{name}/full", g, c, sol, None)
        rt5 = member_block(f"{name}/t5", g, c, sol, t5c)
        table.append((name, g, c, t1c, t5c, rfull, rt5))

    log("\n[T3] SUMMARY TABLE (fresh members)")
    log(" name  gamma  c        c/c*   t1      t5      | "
        "ks_full   kc_full   R_full  ovl(ray/all) | "
        "ks_t5     kc_t5     R_t5    ovl(ray/all)")
    cstars = {"F1": cs1, "F2": cs05, "F3": cs2}
    for name, g, c, t1c, t5c, rf, r5 in table:
        log(f" {name}   {g:.1f}  {c:.6f} {c/cstars[name]:.2f}  "
            f"{t1c:.4f}  {t5c:.4f} | "
            f"{rf['ks']:.6f}  {rf['kc']:.6f}  {rf['ratio']:.4f} "
            f"({rf['fr_ray']:.3f}/{rf['fr_all']:.3f}) | "
            f"{r5['ks']:.6f}  {r5['kc']:.6f}  {r5['ratio']:.4f} "
            f"({r5['fr_ray']:.3f}/{r5['fr_all']:.3f})")

    log("\nDONE main verifier (arclength attack in separate script).")


if __name__ == "__main__":
    main()
