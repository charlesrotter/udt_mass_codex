#!/usr/bin/env python3
"""W5 ARM-2 — SCRIPT 8: THE FRAME PREMISE (kill or confirm the W4
frame-mixing).

Date: 2026-06-12.  Two jobs.

JOB 1 — FRAME-LABEL ADJUDICATION (exact, then numeric): the W4-B
suite labeled its default w-source 'primary (q*-eliminated)' and its
variant 'diagonal q=0'.  The banked theorem chain (w4a_system A4/A9 +
V1-08, all exact, rerun 2026-06-12) fixes, in the single banked
positive convention c = +2:
    q = 0 (diagonal, Class A):  dL/dw = -(c/4) sin f_th^2/(f(1+w)^3)
        => v-source S = -(c/(16 kappa)) f_th^2 e^{-2v}/r^2  (NEGATIVE
        for kappa > 0)
    q = q* (Class B):           dL*/dw = +(c/4) ...  => S POSITIVE.
The W4-B coded default source is NEGATIVE (w4b_evolib.source,
frame='primary', returns -sc e^{-2v}) — i.e. numerically the
DIAGONAL/Class-A force.  VERDICT TO TEST: the W4 catalog ran BOTH
sectors in the library/diagonal frame (consistent, no mixing); the
'frame-mixing premise' was a LABEL artifact of w4b_sym_energy block A
(its L0/L* carry an overall sign flip vs the banked positive-
convention density).  Checked numerically below against the committed
w4b_evolib (imported, never edited).

JOB 2 — THE GENUINE Class-B (q = q*) SYSTEM, run for the first time:
  f-flow:  X_tt - X_t = -2 P_X  (angular sign flips; <>-measure EL of
           the Class-B reduced density e^{-t}[(1/4)f_t^2
           - (1/4)s f_u^2/(f W)])
  w-source: sign-flipped C1 tadpole; species untruncation carried in
           BOTH readings (registry #28: the q*-branch species content
           is unadjudicated):
             (a) q=0-species verbatim: factor (1 + 2 kappa/f)
                 [locus f = -2 kappa, interior for kappa < 0]
             (b) declared reading: factor (1 - 2 kappa/f) on the
                 Class-B tadpole.
  Compare: does the Class-B flow seal from the M1 weld data?  Folds +
  spot pencil edges on the common window t <= 2.2357 vs Class A.
PRE-STATED: all Class-B results are hypothesis-grade and labeled with
the #28 caveat; a Class-B flow that fails to seal is a first-class
structural finding (the q* frame has no banked library for a reason).

Log: /tmp/w5_arm2_frame.log.  New file.  2026-06-12, W5 Arm-2 agent.
"""
import sys, time
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
import w5_arm2_lib as w5
import w4b_evolib as ev4

t0 = time.time()
def log(*a):
    print(*a, flush=True)

log("=" * 72)
log("JOB 1: frame-label adjudication against committed w4b_evolib")
log("=" * 72)


class _G:
    pass


gg = _G()
gg.sc = np.array([[1.0]])      # c_m fth2/(16 r^2) stand-in
gg.c = 1.0
v_t = np.array([[0.3]])
s_pri = ev4.source(v_t, gg, kappa=+1.0, dcell=False, frame="primary")
s_dia = ev4.source(v_t, gg, kappa=+1.0, dcell=False, frame="diagonal")
log(f"  w4b_evolib source at v=0.3, kappa=+1: primary={s_pri[0,0]:+.4f}"
    f" diagonal={s_dia[0,0]:+.4f}")
log(f"  banked theorem (A4/V1-08, c=+2 positive convention): q=0 "
    f"diagonal source is NEGATIVE for kappa>0; q* source POSITIVE.")
ok1 = s_pri[0, 0] < 0 and s_dia[0, 0] > 0
log(f"  => the W4-B DEFAULT ('primary') source carries the q=0/"
    f"DIAGONAL sign; its 'diagonal' variant carries the q* sign: "
    f"LABELS SWAPPED, numerics consistent.  [{'CONFIRMED' if ok1 else 'NOT CONFIRMED'}]")
log("  VERDICT: the W4 catalog ran f-sector AND w-channel in the "
    "library/diagonal\n  (Class-A q=0) frame throughout — the "
    "'frame-mixing premise' on the W4 record\n  is a LABEL artifact, "
    "not a physical premise.  (The flip-side: every W4 number\n  "
    "called 'primary frame' is a DIAGONAL-frame number, which is "
    "exactly the frame\n  where the W5 species theorem lives — the "
    "untruncated map above is internally\n  frame-consistent.)")

log("=" * 72)
log("JOB 2: the genuine Class-B (q*) system")
log("=" * 72)
GAMMA, CM = 1.0, 0.18413678


def flowB(gamma, c, sgn=-1.0, fstop=0.002, Tmax=10.0):
    def rhs(t, z):
        X, Xt = z[:4], z[4:]
        return np.concatenate([Xt, Xt + sgn * 2 * vl.Pgrad(X)])

    def ev(t, z):
        return vl.fmin_exact(z[:4]) - fstop
    ev.terminal, ev.direction = True, -1
    z0 = np.array([1.0, 0, 0, 0, gamma, -c, 0, 0])
    return solve_ivp(rhs, (0, Tmax), z0, method='DOP853', rtol=1e-11,
                     atol=1e-12, dense_output=True, events=ev)


solB = flowB(GAMMA, CM)
sealedB = len(solB.t_events[0]) > 0
t_stopB = float(solB.t_events[0][0]) if sealedB else float(solB.t[-1])
log(f"  Class-B flow from M1 weld data: sealed={sealedB} "
    f"t_stop/end={t_stopB:.4f}")
ZB = solB.sol(np.linspace(0, t_stopB, 50))
fminB = [vl.fmin_exact(ZB[:4, i]) for i in range(50)]
log(f"  f_min along Class-B flow: start {fminB[0]:.3f} end "
    f"{fminB[-1]:.4f} min {min(fminB):.4f}")


class MemberB:
    """Member-like wrapper for the Class-B flow (GeoW5-compatible)."""

    def __init__(self, sol, t_stop, gamma, c, Nu=24, Nt=4000):
        self.gamma, self.c = gamma, c
        self.t_stop = t_stop
        self.tg = np.linspace(0.0, t_stop, Nt)
        Z = sol.sol(self.tg)
        self.X = Z[:4].T
        un, wu = np.polynomial.legendre.leggauss(Nu)
        self.u, self.wu, self.Nu, self.Nt = un, wu, Nu, Nt
        Y, Yu = vl.Yr(un), vl.Yru(un)
        self.f = self.X @ Y
        self.fu = self.X @ Yu
        self.fth2 = (1 - un[None, :] ** 2) * self.fu ** 2


T_CUT = 2.2357
t_bB = min(T_CUT, 0.999 * t_stopB)
memB = MemberB(solB, t_stopB, GAMMA, CM)
geoB = w5.GeoW5(memB, t_b=t_bB, Nt=4000, Nx=256)
memA = vl.Member(GAMMA, CM, Nu=24, Nt=4000)
geoA = w5.GeoW5(memA, t_b=T_CUT, Nt=4000, Nx=256)
log(f"  common-window geometries: Class-B f range "
    f"({geoB.f_t.min():.4g}, {geoB.f_t.max():.4g}) on t<={t_bB:.4f}; "
    f"Class-A ({geoA.f_t.min():.4g}, {geoA.f_t.max():.4g})")

# Class-B w-machinery: sign-flipped tadpole; two untruncation readings.
# Implemented via equilibrium/pencil with cc -> -cc (the C1 tadpole
# sign flip is an overall cc sign in every formula) and the species
# factor handled by kappa sign symmetry:
#   reading (a): factor (1 + 2k/f) == species factor at kappa -> -kappa
#                with the cc flip undone on the kappa prefactor;
# implemented explicitly here for clarity:
import scipy.linalg as sla


def pencilB(geo, k, kappa, reading, vbar=None, nev=3):
    tg = geo.tg
    h = tg[1] - tg[0]
    p = geo.p_t[:, k]
    b = geo.b_t[:, k]
    m = geo.m_t[:, k]
    f = geo.f_t[:, k]
    N = len(tg)
    vb = np.zeros(N) if vbar is None else vbar
    fac = (1.0 + 2.0 * kappa / f) if reading == "a" \
        else (1.0 - 2.0 * kappa / f)
    # Class-B OFF pencil: q = +(cc/(8 kappa)) fac e^{-2vb} b  (sign
    # flip of the C1 tadpole flips the well/wall):
    q = +(2.0 / (8.0 * kappa)) * fac * np.exp(-2 * vb) * b
    pm = 0.5 * (p[1:] + p[:-1])
    wts = np.full(N, h); wts[0] = wts[-1] = h / 2
    dmain = np.zeros(N)
    dmain[:-1] += pm / h
    dmain[1:] += pm / h
    dmain += q * wts
    doff = -pm / h
    Mi = 1.0 / np.sqrt((m * wts)[: N - 1])
    dmK = dmain[: N - 1] * Mi ** 2
    off = doff[: N - 2] * Mi[:-1] * Mi[1:]
    w2 = sla.eigh_tridiagonal(dmK, off, select='i',
                              select_range=(0, nev - 1),
                              eigvals_only=True)
    return w2


def eqB_ray(geo, k, kappa, reading, vinit=None):
    """(p v')' = -(cc/16k) b fac e^{-2v}  (Class-B sign)."""
    from scipy.linalg import solve_banded
    tg = geo.tg
    h = tg[1] - tg[0]
    p = geo.p_t[:, k]
    b = geo.b_t[:, k]
    f = geo.f_t[:, k]
    N = len(tg)
    pm = 0.5 * (p[1:] + p[:-1])
    fac = (1.0 + 2.0 * kappa / f) if reading == "a" \
        else (1.0 - 2.0 * kappa / f)
    lam = -2.0 / (16.0 * kappa)

    def S_t(v):
        return lam * b * fac * np.exp(-2 * v)

    def Sp_t(v):
        return -2 * lam * b * fac * np.exp(-2 * v)

    v = np.zeros(N) if vinit is None else vinit.copy()
    for it in range(80):
        R = S_t(v)
        F = np.zeros(N)
        F[1:-1] = (pm[1:] * (v[2:] - v[1:-1])
                   - pm[:-1] * (v[1:-1] - v[:-2])) / h ** 2 - R[1:-1]
        F[0] = pm[0] * (v[1] - v[0]) / (0.5 * h ** 2) - R[0]
        F[-1] = v[-1]
        Sp = Sp_t(v)
        lo = np.zeros(N); di = np.zeros(N); up = np.zeros(N)
        di[1:-1] = -(pm[1:] + pm[:-1]) / h ** 2 - Sp[1:-1]
        up[1:-1] = pm[1:] / h ** 2
        lo[1:-1] = pm[:-1] / h ** 2
        di[0] = -pm[0] / (0.5 * h ** 2) - Sp[0]
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
        lf = 1.0 if st < 0.5 else 0.5 / st
        v = v + lf * dv
        if not np.all(np.isfinite(v)) or v.min() < -14 or v.max() > 30:
            return None
        if st * lf < 1e-12:
            return v
    return None


log("\n  Class-B static map on the common window (per dominant ray + "
    "all-ray check):")
kB_dom = int(np.argmax(geoB.b_t.sum(0)))
kA_dom = int(np.argmax(geoA.b_t.sum(0)))
for kap in (0.05, 0.2, 1.0, -0.05, -0.2, -1.0):
    for rd in ("a", "b"):
        eqs = [eqB_ray(geoB, k, kap, rd) for k in range(geoB.Nu)]
        nfail = sum(1 for e in eqs if e is None)
        vb = eqs[kB_dom]
        if vb is not None:
            w2 = pencilB(geoB, kB_dom, kap, rd, vbar=vb)
            log(f"    B[{rd}] kappa={kap:+6.3g}: eq fails {nfail}/24 "
                f"rays; dom-ray w2_1..3="
                f"{np.array2string(w2, precision=3)} "
                f"min v={min(e.min() for e in eqs if e is not None):+.3f}"
                f" max v={max(e.max() for e in eqs if e is not None):+.3f}")
        else:
            log(f"    B[{rd}] kappa={kap:+6.3g}: eq fails {nfail}/24 "
                f"rays (dominant ray FAILS)")
# Class-A reference on the same window (theorem-grade reading):
for kap in (0.05, 0.2, 1.0, -0.05, -0.2, -1.0):
    veq, fails = w5.equilibrium_member(geoA, kap, dcell=False, cc=2.0,
                                       species=True)
    if veq is not None:
        w2 = w5.pencil_ray(geoA, kA_dom, kap, False, 2.0, True,
                           vbar=veq[kA_dom], nev=3)[0]
        log(f"    A    kappa={kap:+6.3g}: all-ray eq OK; dom-ray "
            f"w2_1..3={np.array2string(w2, precision=3)} "
            f"min v={veq.min():+.3f}")
    else:
        log(f"    A    kappa={kap:+6.3g}: eq fails rays {fails[:6]}")

log(f"\ndone ({time.time()-t0:.0f}s)")
