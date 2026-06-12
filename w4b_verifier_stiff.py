"""W4-B BLIND VERIFIER — stiff-cell adjudication + spectral rates.

(a) The agent's catalog reports UNRESOLVED-STIFF (integrator failure,
unbanked) at kappa = +-1e-3 D_cell ON. Claim 2 nevertheless says
"0 < kappa < kappa_c GROWS -> terminal collapse" and "kappa < 0 RINGS
at all |kappa|". Adjudicate both deep-|kappa| cells with an IMPLICIT
integrator (scipy Radau, dense FD Jacobian) on the most-unstable ray
(rays decouple exactly on frozen f), Nx = 320.
(b) Spectral rate predictions sqrt(-omega^2_min) at 0.7 kc and 0.25 kc
on the dominant ray (t-variable FEM with the r^2 mass matrix) for
comparison against the verifier's measured nonlinear growth rates.
Log: /tmp/w4b_verifier_stiff.log. New file. 2026-06-12, verifier.
"""
import sys
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl


def log(*a):
    print(*a, flush=True)


mem = vl.Member(1.0, 0.18413678, Nu=24, Nt=8000)
K = 21                       # dominant ray (verifier edges)
xs = mem.x_of_t[::-1, K]
ts = mem.tg[::-1]
Nx = 320
xg = np.linspace(0, xs[-1], Nx)
dx = xg[1] - xg[0]
t_x = np.interp(xg, xs, ts)
f = np.interp(t_x, mem.tg, mem.f[:, K])
fth2 = np.interp(t_x, mem.tg, mem.fth2[:, K])
r = np.exp(-t_x)
a1 = 2 * f / r
sc = mem.c * fth2 / (16 * r**2)
xmax = xs[-1]
log(f"ray {K}: xmax={xmax:.4f}, max sc = {sc.max():.3f} "
    f"(stiff freq at |kappa|=1e-3 ~ sqrt(3*sc/1e-3) = "
    f"{np.sqrt(3*sc.max()/1e-3):.0f})")


def run_ray(kappa, amp, T_end, tag):
    v0 = np.log1p(amp * np.exp(-((xg - 0.55 * xmax)
                                 / (0.10 * xmax))**2))
    v0[0] = 0.0
    y0 = np.concatenate([v0, np.zeros(Nx)])

    def rhs(t, y):
        v, vt = y[:Nx], y[Nx:]
        lap = np.empty(Nx)
        lap[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / dx**2
        lap[0] = 0.0
        lap[-1] = 2 * (v[-2] - v[-1]) / dx**2
        gr = np.empty(Nx)
        gr[1:-1] = (v[2:] - v[:-2]) / (2 * dx)
        gr[0] = gr[-1] = 0.0
        S = sc / kappa * (np.exp(v) - np.exp(-2 * v))
        dvt = lap + a1 * gr + S
        dv = vt.copy()
        dv[0] = 0.0
        dvt[0] = 0.0
        return np.concatenate([dv, dvt])

    def ev_dn(t, y):
        return np.min(y[:Nx]) - np.log(0.05)
    ev_dn.terminal = True

    def ev_up(t, y):
        return np.max(y[:Nx]) - 8.0
    ev_up.terminal = True
    t0 = time.time()
    s = solve_ivp(rhs, (0, T_end), y0, method='Radau', rtol=1e-8,
                  atol=1e-10, events=[ev_dn, ev_up], dense_output=True,
                  max_step=0.5)
    tq = np.linspace(0, s.t[-1], 1200)
    Z = s.sol(tq)
    env = np.max(np.abs(Z[:Nx]), axis=0)
    term = None
    if len(s.t_events[0]):
        term = ("COLLAPSE-", float(s.t_events[0][0]))
    if len(s.t_events[1]):
        term = ("COLLAPSE+", float(s.t_events[1][0]))
    m = len(env)
    sl = np.polyfit(tq[3 * m // 4:],
                    np.log(np.maximum(env[3 * m // 4:], 1e-300)), 1)[0]
    pr = Z[int(0.55 * Nx)]
    j = int(0.4 * m)
    d = pr[j:] - pr[j:].mean()
    F = np.abs(np.fft.rfft(d * np.hanning(len(d))))
    fr = np.fft.rfftfreq(len(d), d=tq[1] - tq[0]) * 2 * np.pi
    pk = float(fr[np.argmax(F[1:]) + 1])
    log(f"[{tag}] kappa={kappa:+.4g}: T_reached={s.t[-1]:.3f}/{T_end} "
        f"term={term} env0={env[0]:.3g} envmax={env.max():.3g} "
        f"envfin={env[-1]:.3g} late-rate={sl:+.3f} freq~{pk:.1f} "
        f"({time.time()-t0:.0f}s, {s.nfev} fev)")
    return term, env


log("=" * 72)
log("(a) STIFF CELLS, D_cell ON, dominant ray, implicit Radau")
log("=" * 72)
run_ray(+1e-3, 0.01, 7.2, "stiff k=+1e-3 a=.01")
run_ray(-1e-3, 0.01, 2.0, "stiff k=-1e-3 a=.01")
run_ray(+1e-2, 0.01, 7.2, "k=+1e-2 a=.01 (reval said COLLAPSE+)")

log("=" * 72)
log("(b) spectral rates on the dominant ray (t-FEM, r^2 mass)")
log("=" * 72)
h = mem.tg[1] - mem.tg[0]
p = mem.p[:, K]
b = mem.b[:, K]
mw = np.exp(-3 * mem.tg) / mem.f[:, K]     # r^2 weight in t
pm = 0.5 * (p[1:] + p[:-1])
N = mem.Nt
dmain = np.zeros(N)
dmain[:-1] += pm / h
dmain[1:] += pm / h
doff = -pm / h
wts = np.full(N, h)
wts[0] = wts[-1] = h / 2
A = diags([doff[:-1], dmain[:-1], doff[:-1]], [-1, 0, 1],
          format='csc')
Bm = diags([(b * wts)[:-1]], [0], format='csc')
Mm = diags([(mw * wts)[:-1]], [0], format='csc')
KC_RAY = 0.0706205
for fac in (0.25, 0.5, 0.7, 0.85, 0.95):
    kap = fac * KC_RAY
    Op = (A - (3 * mem.c / (16 * kap)) * Bm).tocsc()
    w2 = eigsh(Op, k=1, M=Mm, sigma=None, which='SA',
               return_eigenvectors=False)[0]
    rate = np.sqrt(max(-w2, 0.0))
    log(f"  kappa = {fac:.2f} kc: omega^2_min = {w2:+.4f} "
        f"-> predicted linear rate {rate:.4f}")
log("done.")
