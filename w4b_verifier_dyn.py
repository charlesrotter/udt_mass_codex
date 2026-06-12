"""W4-B BLIND VERIFIER — attacks B (independent P3 spot reruns),
C (M2 dynamical edge), D (energy hygiene).

Fully independent dynamics machinery: own flow regeneration
(w4b_verifier_lib), own per-ray x-grids (Nx=1536, cubic-free t->x
inversion on an 8001-point t grid), NON-conservation-form stencil
(v_xx + (2f/r) v_x centered; ghost-node Neumann; the agent used a
conservation-form flux stencil), own RK4 at cfl 0.4, own energy
quadrature (trapezoid, centered v_x), own envelope/rate/FFT readouts.
Long-T slow-instability hunt: T_end = 36 x_max on the RING cells the
agent banked with POSITIVE late rates (+0.03..+0.07) — 3x the
catalog window.

Cells (claims under attack in parentheses):
  R1  M1 ON  k=-1     a=0.01  T=36xm  (RING durable; their trust cell)
  R2  M1 ON  k=2kc    a=0.01  T=36xm  (RING above band)
  R2b M1 ON  k=2kc    a=0.3   T=36xm  (amplitude-independence)
  R3  M1 ON  k=0.01   a=0.01  T=12xm  (GROW -> terminal collapse)
  R4  M1 ON  k=0.7kc  a=1e-4  T=12xm  (GROW rate inside band)
  R5  M1 OFF k=+1     a=0.01  bump    (settles onto displaced eq)
  R6  M1 OFF k=+1     a=0.01  eq+bump T=36xm (RING about shaped eq)
  R7  M1 OFF k=-1     a=0.3   T=36xm  (RING freq 13.122, positive rate)
  E1  M2 ON  k={0.95,1.05,1.15,1.25}kc a=1e-4 seal bump T=48xm (edge)
Energy drift recorded per run (kappa<0 scale pathology checked).
Log: /tmp/w4b_verifier_dyn.log; data /tmp/w4b_verifier_dyn.npz.
New file. 2026-06-12, verifier.
"""
import sys
import time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl


def log(*a):
    print(*a, flush=True)


class XGeo:
    """own per-ray x geometry from a verifier Member."""

    def __init__(self, mem, Nx=1536):
        Nu, Nt = mem.Nu, mem.Nt
        self.mem, self.Nx, self.Nu = mem, Nx, Nu
        self.u, self.wu, self.c = mem.u, mem.wu, mem.c
        self.xmax = mem.xmax
        self.xg = np.linspace(0, 1, Nx)[None, :] * self.xmax[:, None]
        self.dx = self.xg[:, 1] - self.xg[:, 0]
        self.t_of_x = np.empty((Nu, Nx))
        self.f = np.empty((Nu, Nx))
        self.fth2 = np.empty((Nu, Nx))
        for k in range(Nu):
            xs = mem.x_of_t[::-1, k]          # increasing
            ts = mem.tg[::-1]
            self.t_of_x[k] = np.interp(self.xg[k], xs, ts)
            self.f[k] = np.interp(self.t_of_x[k], mem.tg, mem.f[:, k])
            self.fth2[k] = np.interp(self.t_of_x[k], mem.tg,
                                     mem.fth2[:, k])
        self.r = np.exp(-self.t_of_x)
        self.a1 = 2 * self.f / self.r
        self.sc = self.c * self.fth2 / (16 * self.r**2)
        self.k_probe = int(np.argmax(self.fth2.sum(1)))
        self.i_probe = int(0.55 * Nx)


def bump(geo, amp, x0frac=0.55, sigfrac=0.10):
    g = 1 - geo.u**2
    g = g / np.max(np.abs(g))
    x0 = x0frac * geo.xmax[:, None]
    sg = sigfrac * geo.xmax[:, None]
    w0 = amp * g[:, None] * np.exp(-((geo.xg - x0) / sg)**2)
    return np.log1p(w0)


def source(v, geo, kappa, dcell):
    s = geo.sc / kappa
    if dcell:
        return s * (np.exp(v) - np.exp(-2 * v))
    return -s * np.exp(-2 * v)


def Vpot(v, geo, dcell):
    cf = geo.c * geo.fth2 / 8.0
    if dcell:
        return -cf * (np.exp(-2 * v) + 2 * np.exp(v) - 3)
    return -cf * (np.exp(-2 * v) - 1)


def energy(v, vt, geo, kappa, dcell):
    vx = np.gradient(v, axis=1) / geo.dx[:, None]
    dens = 2 * kappa * geo.r**2 * (vt**2 + vx**2) + Vpot(v, geo, dcell)
    Ek = np.trapz(dens, dx=1.0, axis=1) * geo.dx
    return float(geo.wu @ Ek)


def rhs(v, vt, geo, kappa, dcell):
    dx2 = geo.dx[:, None]**2
    lap = np.empty_like(v)
    lap[:, 1:-1] = (v[:, 2:] - 2 * v[:, 1:-1] + v[:, :-2]) / dx2
    lap[:, 0] = 0.0
    # Neumann ghost at outer: v_N = v_{N-2}
    lap[:, -1] = 2 * (v[:, -2] - v[:, -1]) / dx2[:, 0]
    grad = np.empty_like(v)
    grad[:, 1:-1] = (v[:, 2:] - v[:, :-2]) / (2 * geo.dx[:, None])
    grad[:, 0] = 0.0
    grad[:, -1] = 0.0
    dvt = lap + geo.a1 * grad + source(v, geo, kappa, dcell)
    dv = vt.copy()
    dv[:, 0] = 0.0          # inner (seal) Dirichlet
    dvt[:, 0] = 0.0
    return dv, dvt


def evolve(geo, v0, vt0, kappa, dcell, T_end, vref=None, cfl=0.4,
           tag=""):
    dT = cfl * float(np.min(geo.dx))
    n = int(np.ceil(T_end / dT))
    v, vt = v0.copy(), vt0.copy()
    vr = 0.0 if vref is None else vref
    stride = max(1, n // 6000)
    Ts, pr, env, Es = [], [], [], []
    term = None
    E0 = energy(v, vt, geo, kappa, dcell)
    for i in range(n):
        k1 = rhs(v, vt, geo, kappa, dcell)
        k2 = rhs(v + 0.5 * dT * k1[0], vt + 0.5 * dT * k1[1], geo,
                 kappa, dcell)
        k3 = rhs(v + 0.5 * dT * k2[0], vt + 0.5 * dT * k2[1], geo,
                 kappa, dcell)
        k4 = rhs(v + dT * k3[0], vt + dT * k3[1], geo, kappa, dcell)
        v = v + dT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        vt = vt + dT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if i % stride == 0:
            Ts.append((i + 1) * dT)
            pr.append(float((v - vr)[geo.k_probe, geo.i_probe]))
            env.append(float(np.max(np.abs(v - vr))))
            Es.append(energy(v, vt, geo, kappa, dcell))
        if i % 200 == 0:
            if not np.all(np.isfinite(v)):
                term = ("NONFINITE", (i + 1) * dT)
                break
            if v.min() <= np.log(0.05):
                term = ("COLLAPSE-", (i + 1) * dT)
                break
            if v.max() >= 8.0:
                term = ("COLLAPSE+", (i + 1) * dT)
                break
    Ts, pr, env, Es = map(np.array, (Ts, pr, env, Es))
    out = dict(T=Ts, probe=pr, env=env, E=Es, term=term, dT=dT)
    # readouts
    if len(env) > 20 and term is None:
        m = len(env)
        i1, i2, i3 = m // 4, m // 2, 3 * m // 4
        sl = np.polyfit(Ts[i3:], np.log(np.maximum(env[i3:], 1e-300)),
                        1)[0]
        # FFT of final 60%
        j = int(0.4 * m)
        d = pr[j:] - pr[j:].mean()
        F = np.abs(np.fft.rfft(d * np.hanning(len(d))))
        fr = np.fft.rfftfreq(len(d), d=Ts[j + 1] - Ts[j]) * 2 * np.pi
        top = np.argsort(F[1:])[::-1][:3] + 1
        drift = abs(np.median(Es[-m // 20:]) - np.median(Es[:m // 20]))
        scl = max(np.max(np.abs(Es)), 1e-300)
        out.update(rate=float(sl), env0=float(env[0]),
                   envmid=float(env[i2]), envfin=float(env[-1]),
                   envmax=float(env.max()),
                   freqs=[float(fr[t]) for t in top],
                   edrift_rel=float(drift / scl),
                   Escale=float(scl), E0=float(E0))
        log(f"[{tag}] T={Ts[-1]:.1f} env0/mid/fin/max="
            f"{env[0]:.3g}/{env[i2]:.3g}/{env[-1]:.3g}/{env.max():.3g}"
            f" late-rate={sl:+.4f} freqs={out['freqs']}"
            f" Edrift={out['edrift_rel']:.1e} (scale {scl:.3g})")
    else:
        gr = np.nan
        if len(env) > 10:
            m = len(env)
            gr = np.polyfit(Ts[m // 4:], np.log(np.maximum(
                env[m // 4:], 1e-300)), 1)[0]
        out.update(rate=float(gr))
        log(f"[{tag}] TERMINATED {term}; envmax="
            f"{env.max() if len(env) else np.nan:.3g} "
            f"growth-rate(2nd-3/4)={gr:+.4f}")
    return out


def veq_on_x(geo, kappa):
    """OFF static equilibrium per ray via the verifier's own t-space
    Newton, interpolated onto the x grid."""
    lam = geo.c / (16 * kappa)
    mem = geo.mem
    veq = np.empty((geo.Nu, geo.Nx))
    for k in range(geo.Nu):
        vk = vl.equilibrium_ray(mem, k, lam)
        if vk is None:
            return None
        veq[k] = np.interp(geo.t_of_x[k], mem.tg, vk)
    return veq


t00 = time.time()
log("regenerating members with the verifier flow ...")
memM1 = vl.Member(1.0, 0.18413678, Nu=24, Nt=8000)
memM2 = vl.Member(1.0, 0.28328735, Nu=24, Nt=8000)
g1 = XGeo(memM1)
g2 = XGeo(memM2)
xm1 = float(np.max(g1.xmax))
xm2 = float(np.max(g2.xmax))
kcM1 = 0.070620          # verifier's own converged value
kcM2 = 0.025560
log(f"M1 xmax={xm1:.4f} probe ray {g1.k_probe}; "
    f"M2 xmax={xm2:.4f} probe ray {g2.k_probe} "
    f"({time.time()-t00:.0f}s)")

OUT = {}

runs = [
    ("R1_ON_km1_a.01", g1, -1.0, True, 0.01, 36 * xm1, None),
    ("R2_ON_2kc_a.01", g1, 2 * kcM1, True, 0.01, 36 * xm1, None),
    ("R2b_ON_2kc_a.3", g1, 2 * kcM1, True, 0.3, 36 * xm1, None),
    ("R3_ON_k.01_a.01", g1, 0.01, True, 0.01, 12 * xm1, None),
    ("R4_ON_.7kc_a1e-4", g1, 0.7 * kcM1, True, 1e-4, 12 * xm1, None),
]
for tag, geo, kap, dc, amp, Tend, _ in runs:
    v0 = bump(geo, amp)
    r = evolve(geo, v0, np.zeros_like(v0), kap, dc, Tend, tag=tag)
    OUT[tag] = r

# R5/R6: OFF kappa=+1 with own equilibrium
veq1 = veq_on_x(g1, 1.0)
log(f"M1 OFF kappa=1 equilibrium: min v_eq = {veq1.min():.5f} "
    f"(claimed displacement ~ -0.033/kappa)")
v0 = veq1 * 0 + bump(g1, 0.01)
OUT["R5_OFF_k1_bumponly"] = evolve(g1, v0, np.zeros_like(v0), 1.0,
                                   False, 12 * xm1, vref=veq1,
                                   tag="R5_OFF_k1_bumponly(ref=eq)")
v0 = veq1 + bump(g1, 0.01)
OUT["R6_OFF_k1_eqbump"] = evolve(g1, v0, np.zeros_like(v0), 1.0,
                                 False, 36 * xm1, vref=veq1,
                                 tag="R6_OFF_k1_eqbump")
# R7: OFF kappa=-1 amp 0.3 long-T (banked RING freq 13.122 rate +0.03)
veqm1 = veq_on_x(g1, -1.0)
log(f"M1 OFF kappa=-1 equilibrium: min v_eq = {veqm1.min():.5f}")
v0 = bump(g1, 0.3)
OUT["R7_OFF_km1_a.3"] = evolve(g1, v0, np.zeros_like(v0), -1.0,
                               False, 36 * xm1, tag="R7_OFF_km1_a.3")
OUT["R7b_OFF_km1_a.3_refeq"] = evolve(
    g1, veqm1 + bump(g1, 0.3), np.zeros_like(v0), -1.0, False,
    36 * xm1, vref=veqm1, tag="R7b_OFF_km1_eq+bump_a.3")

# E1: the M2 edge (attack C)
log("=" * 72)
log("M2 DYNAMICAL EDGE (seal-weighted bump x0=0.15, amp 1e-4, "
    "T=48 xmax)")
log("=" * 72)
for fac in (0.95, 1.05, 1.15, 1.25):
    kap = fac * kcM2
    v0 = bump(g2, 1e-4, x0frac=0.15)
    r = evolve(g2, v0, np.zeros_like(v0), kap, True, 48 * xm2,
               tag=f"E1_M2_{fac:.2f}kc")
    OUT[f"E1_M2_{fac:.2f}kc"] = r

np.savez("/tmp/w4b_verifier_dyn.npz",
         **{f"{k}_{q}": np.asarray(v[q]) for k, v in OUT.items()
            for q in ("T", "probe", "env", "E") if q in v})
log(f"ALL RUNS DONE {time.time()-t00:.0f}s")
