#!/usr/bin/env python3
"""W5 ARM-2 BLIND VERIFIER — SCRIPT 2: the convention finding and the
two-kappa_c-family reconciliation, independent machinery.

Date: 2026-06-12.  Verifier agent.  Imports ONLY the committed,
previously-verified w4b_verifier_lib member flow; all edge machinery
here is new and discretization-independent of the claimant's
(piecewise-linear FEM with CONSISTENT tridiagonal b-mass vs their
lumped trapz FD; own Newton; own bisection).

ADJUDICATIONS:
 U1 banked-unit lock: with cc = c_member my machinery must reproduce
    the VB4/banked full-domain edges (kc 0.070620/0.025560/0.009013,
    ks 0.13365/0.04863/0.01715) — confirms the banked numbers ARE
    member-unit numbers.
 U2 TRUE-unit edges (cc = 2): full-domain kc/ks must equal banked *
    (2/c_m): M1 0.767049/1.453149, M2 0.180450/0.343305,
    M4 0.198369/0.377401 (claim 3).
 U3 THE RECONCILIATION: frozen ON pencil kappa_c on the t1pc trust
    window in TRUE units must hit the W4-A/VA4 anchors
    {M1 0.01160, M2 0.00789, M4 0.00829} to <= 0.4% — i.e. the "two
    kappa_c families" of w4_results.md are ONE operator read in
    different units (B: member) and on different domains (A: t1pc).
 U4 untruncated headline: M1 full-domain OFF fold with the
    (1 - 2 kappa/f) factor = 0.915696 (claim 4's -37% shift).

Log: /tmp/w5_arm2_verifier2_units.log.  New file.
"""
import sys, time
import numpy as np
import scipy.linalg as sla
from scipy.linalg import solve_banded
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"VW5A2U-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

MEMBERS = {"M1": (1.0, 0.18413678), "M2": (1.0, 0.28328735),
           "M4": (0.5, 0.09087158)}
T1 = {"M1": 1.6383, "M2": 1.168, "M4": 1.7106}
BANKED = {"M1": (0.070620, 0.13365), "M2": (0.025560, 0.04863),
          "M4": (0.009013, 0.01715)}
VA4_KC = {"M1": 0.01160, "M2": 0.00789, "M4": 0.00829}

print("regenerating members (committed verifier-lib flow) ...", flush=True)
MEM = {t: vl.Member(g, c, Nu=24, Nt=4000) for t, (g, c) in MEMBERS.items()}


def ray_weights(mem, k, t_b, Nt=4000):
    tg = np.linspace(0.0, t_b, Nt)
    X = np.array([np.interp(tg, mem.tg, mem.X[:, i]) for i in range(4)]).T
    Y, Yu = vl.Yr(mem.u), vl.Yru(mem.u)
    f = X @ Y[:, k]
    fu = X @ Yu[:, k]
    fth2 = (1 - mem.u[k] ** 2) * fu ** 2
    et = np.exp(-tg)
    return tg, f, f * et, (fth2 / f) * et, np.exp(-3 * tg) / f


def mu1_ray(tg, p, b, fac=None):
    """min over psi (psi(t_b)=0, natural at 0) of
    Int p psi'^2 / Int (fac*b) psi^2  — FEM: midpoint p stiffness,
    CONSISTENT (h/6) tridiagonal mass on fac*b."""
    h = tg[1] - tg[0]
    N = len(tg)
    pm = 0.5 * (p[1:] + p[:-1])
    bb = b if fac is None else b * fac
    # stiffness (tridiag), nodes 0..N-1, Dirichlet at N-1 -> keep 0..N-2
    dK = np.zeros(N)
    dK[:-1] += pm / h
    dK[1:] += pm / h
    oK = -pm / h
    # consistent mass on bb: element e contributes h/12*(3 b_i + b_j)
    # to (i,i) etc. (linear interp of bb): use exact lin-lin integrals:
    bi, bj = bb[:-1], bb[1:]
    dM = np.zeros(N)
    dM[:-1] += h * (3 * bi + bj) / 12.0
    dM[1:] += h * (bi + 3 * bj) / 12.0
    oM = h * (bi + bj) / 12.0
    n = N - 1
    K = np.diag(dK[:n]) + np.diag(oK[: n - 1], 1) + np.diag(oK[: n - 1], -1)
    Mb = np.diag(dM[:n]) + np.diag(oM[: n - 1], 1) + np.diag(oM[: n - 1], -1)
    # mu1 = 1/theta_max of  Mb v = theta K v
    th = sla.eigh(Mb, K, eigvals_only=True,
                  subset_by_index=[n - 1, n - 1])[0]
    return 1.0 / th


def kappa_c_frozen_ON(mem, t_b, cc=2.0, Nt=4000):
    """kappa_c = 3 cc/(16 mu1), member = max over rays."""
    best = -np.inf
    for k in range(mem.Nu):
        tg, f, p, b, m = ray_weights(mem, k, t_b, Nt)
        if np.max(b) <= 0:
            continue
        mu = mu1_ray(tg, p, b)
        best = max(best, 3 * cc / (16 * mu))
    return best


def newton_eq(tg, p, b, lam, fac=None, vinit=None, tol=1e-12, maxit=80):
    """(p v')' = lam * (fac*b) * e^{-2v}; v(t_b)=0, v'(0)=0."""
    h = tg[1] - tg[0]
    N = len(tg)
    pm = 0.5 * (p[1:] + p[:-1])
    bb = b if fac is None else b * fac
    v = np.zeros(N) if vinit is None else vinit.copy()
    for _ in range(maxit):
        e = np.exp(-2 * v)
        F = np.zeros(N)
        F[1:-1] = (pm[1:] * (v[2:] - v[1:-1])
                   - pm[:-1] * (v[1:-1] - v[:-2])) / h ** 2 \
            - lam * bb[1:-1] * e[1:-1]
        F[0] = pm[0] * (v[1] - v[0]) / (0.5 * h ** 2) - lam * bb[0] * e[0]
        F[-1] = v[-1]
        di = np.zeros(N); up = np.zeros(N); lo = np.zeros(N)
        di[1:-1] = -(pm[1:] + pm[:-1]) / h ** 2 + 2 * lam * bb[1:-1] * e[1:-1]
        up[1:-1] = pm[1:] / h ** 2
        lo[1:-1] = pm[:-1] / h ** 2
        di[0] = -pm[0] / (0.5 * h ** 2) + 2 * lam * bb[0] * e[0]
        up[0] = pm[0] / (0.5 * h ** 2)
        di[-1] = 1.0
        ab = np.zeros((3, N))
        ab[0, 1:] = up[:-1]
        ab[1, :] = di
        ab[2, :-1] = lo[1:]
        try:
            dv = solve_banded((1, 1), ab, -F)
        except Exception:
            return None
        if not np.all(np.isfinite(dv)):
            return None
        st = np.max(np.abs(dv))
        a = 1.0 if st < 0.5 else 0.5 / st
        v = v + a * dv
        if not np.all(np.isfinite(v)) or v.min() < -14 or v.max() > 30:
            return None
        if st * a < tol:
            return v
    return None


def kappa_s_member(mem, t_b, cc=2.0, species=False, Nt=4000):
    """OFF fold via per-member kappa bisection (exists above, fails
    below); source (p v')' = (cc/(16 k)) b (1-2k/f)^{species} e^{-2v}."""
    RAYS = []
    for k in range(mem.Nu):
        tg, f, p, b, m = ray_weights(mem, k, t_b, Nt)
        RAYS.append((tg, f, p, b))

    def exists(kap, warm=None):
        out = []
        for (tg, f, p, b), w0 in zip(RAYS, warm or [None] * len(RAYS)):
            fac = (1 - 2 * kap / f) if species else None
            v = newton_eq(tg, p, b, cc / (16 * kap), fac=fac, vinit=w0)
            if v is None:
                return None
            out.append(v)
        return out

    lo, hi = 1e-4, 400.0
    vhi = exists(hi)
    if vhi is None:
        return None
    if exists(lo) is not None:
        return np.inf
    warm = vhi
    for _ in range(46):
        mid = np.sqrt(lo * hi)
        v2 = exists(mid, warm)
        if v2 is None:
            lo = mid
        else:
            hi, warm = mid, v2
    return np.sqrt(lo * hi)


# ------------------------------------------------------------- U1 / U2
print("=" * 72)
print("U1/U2: full-domain edges, banked units and TRUE units")
print("=" * 72)
ok1, ok2 = True, True
for tag, (gam, cm) in MEMBERS.items():
    mem = MEM[tag]
    t_b = mem.t_stop
    kcB, ksB = BANKED[tag]
    kc_m = kappa_c_frozen_ON(mem, t_b, cc=cm)
    ks_m = kappa_s_member(mem, t_b, cc=cm, species=False)
    d1 = abs(kc_m - kcB) / kcB
    d2 = abs(ks_m - ksB) / ksB
    ok1 &= d1 < 5e-3 and d2 < 5e-3
    kc_t = kappa_c_frozen_ON(mem, t_b, cc=2.0)
    ks_t = kappa_s_member(mem, t_b, cc=2.0, species=False)
    e1 = abs(kc_t - kcB * 2 / cm) / (kcB * 2 / cm)
    e2 = abs(ks_t - ksB * 2 / cm) / (ksB * 2 / cm)
    ok2 &= e1 < 5e-3 and e2 < 5e-3
    print(f"  {tag}: banked-unit kc={kc_m:.6f} ({d1:.1e})  ks={ks_m:.6f}"
          f" ({d2:.1e}) | TRUE kc={kc_t:.6f} ks={ks_t:.6f} "
          f"ratio={ks_t/kc_t:.5f} (vs banked*2/c: {e1:.1e},{e2:.1e})")
check("U1", ok1, "my FEM/Newton machinery reproduces the BANKED edges "
      "with cc = c_member: the banked W4-B numbers are member-unit "
      "numbers (convention finding code-confirmed numerically)")
check("U2", ok2, "TRUE-unit edges = banked * (2/c_member): claim-3 "
      "TRUE-unit table confirmed on independent discretization")

# ------------------------------------------------------------------ U3
print("=" * 72)
print("U3: THE RECONCILIATION — t1pc TRUE-unit kc vs the W4-A anchors")
print("=" * 72)
ok3 = True
for tag in MEMBERS:
    mem = MEM[tag]
    kc1 = kappa_c_frozen_ON(mem, T1[tag], cc=2.0)
    kc1b = kappa_c_frozen_ON(mem, T1[tag], cc=2.0, Nt=8000)
    rel = abs(kc1 - VA4_KC[tag]) / VA4_KC[tag]
    conv = abs(kc1 - kc1b) / kc1b
    ok3 &= rel <= 4e-3
    print(f"  {tag}: kc(t1pc, TRUE) = {kc1:.6f}  [VA4 anchor "
          f"{VA4_KC[tag]}]  rel {rel:.2%}  (Nt doubling {conv:.1e})")
check("U3", ok3, "the W4-A 'pencil family' anchors ARE the same frozen "
      "ON operator read on the t1pc window in TRUE units (<= 0.4%): "
      "w4_results.md's 'two kappa_c families on different operators' "
      "is REFUTED — one operator, two unit/domain conventions")

# ------------------------------------------------------------------ U4
print("=" * 72)
print("U4: untruncated M1 full-domain OFF fold (claim-4 headline)")
print("=" * 72)
ksW5 = kappa_s_member(MEM["M1"], MEM["M1"].t_stop, cc=2.0, species=True)
rel = abs(ksW5 - 0.915696) / 0.915696
check("U4", rel < 5e-3,
      f"M1 untruncated fold = {ksW5:.6f} (claim 0.915696, rel "
      f"{rel:.1e}); W4-trunc was 1.453: the -37% shift is real on "
      "independent machinery")

print(f"\nVW5A2 UNITS: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if not FAIL else 1)
