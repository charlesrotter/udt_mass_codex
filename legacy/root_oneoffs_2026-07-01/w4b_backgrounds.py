"""W4 SOLVER AGENT B — script 2: BACKGROUND REGENERATION + ANCHOR VERIFY.

Regenerates the banked library members M1/M2/M4 per the frozen recipe
(rescued_workspaces/2026-06-11/verify_s2/v_lib.py conventions):
  f(y,u) = F + a1 Y1 + g2 Y2 + h3 Y3,  Y orthonormal (<Y_i Y_j> = delta),
  t = ln(1/y);  EL flow X_tt - X_t = 2 P_X,  P = (1/8) Int (1-u^2) f_u^2/f du
  weld data X(0) = (1,0,0,0), X_t(0) = (gamma, -c, 0, 0)
  DOP853 rtol 1e-11 atol 1e-12; Gauss-Legendre N = 2000;
  stop at absolute f_min = 0.002.
Members: M1 (gamma=1.0, c=0.18413678 = 1.3 c*_3), M2 (1.0, 0.28328735
= 2.0 c*_3), M4 (0.5, 0.09087158 = 2.0 c*_3(0.5)); threshold anchor
c*_3(1.0) = 0.141644 (declaration value, checked).

PRE-STATED FAILURE CRITERIA:
- B-F1: regenerated trajectories must match the banked bg_*.dat columns
  (F, a1, g2, h3 and f_min) to <= 5e-7 absolute everywhere and t_stop to
  <= 2e-4; else the recipe reading is wrong - STOP, nothing downstream.
- B-F2: c*_3 anchor: header c values / multiplier must equal 0.141644
  to <= 1e-5 (M1: /1.3; M2: /2.0) - else member identification wrong.

Output: /tmp/w4b_bg.npz (dense X(t), X_t(t) grids per member + params
+ trust windows from headers). Log: /tmp/w4b_bg.log. 2026-06-12, W4-B.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

S3, S5, S7 = 3**0.5, 5**0.5, 7**0.5
PASS, FAIL = [], []


def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
    assert ok, "FAILED: " + label


def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3 * u, (S5 / 2) * (3 * u * u - 1),
                     (S7 / 2) * (5 * u**3 - 3 * u)])


def Yru(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3 * np.ones_like(u), 3 * S5 * u,
                     (S7 / 2) * (15 * u * u - 3)])


XG, WG = np.polynomial.legendre.leggauss(2000)
YG, YuG = Yr(XG), Yru(XG)
SG = 1 - XG**2


def Pgrad(X):
    fv = X @ YG
    fu = X @ YuG
    return (SG * (2 * fu * YuG / fv - fu * fu * YG / fv**2)) @ WG / 8.0


def fmin_of(X, ngrid=601):
    ug = np.linspace(-1, 1, ngrid)
    fv = X @ Yr(ug)
    i = int(np.argmin(fv))
    lo, hi = max(i - 1, 0), min(i + 1, ngrid - 1)
    res = minimize_scalar(lambda u: float(X @ Yr(np.array([u]))[:, 0]),
                          bounds=(ug[lo], ug[hi]), method='bounded',
                          options={'xatol': 1e-12})
    return min(float(res.fun), fv[0], fv[-1])


def flow(gamma, c, fstop=0.002, Tmax=10.0):
    def rhs(t, z):
        X, Xt = z[:4], z[4:]
        return np.concatenate([Xt, Xt + 2 * Pgrad(X)])

    def ev(t, z):
        return fmin_of(z[:4]) - fstop
    ev.terminal, ev.direction = True, -1
    z0 = np.array([1.0, 0, 0, 0, gamma, -c, 0, 0])
    return solve_ivp(rhs, (0, Tmax), z0, method='DOP853', rtol=1e-11,
                     atol=1e-12, dense_output=True, events=ev)


MEMBERS = {
    'M1': dict(gamma=1.0, c=0.18413678, mult=1.3),
    'M2': dict(gamma=1.0, c=0.28328735, mult=2.0),
    'M4': dict(gamma=0.5, c=0.09087158, mult=None),  # c*_3(0.5) anchor n/a
}
CSTAR3 = 0.141644

out = {}
for tag, mm in MEMBERS.items():
    print("=" * 60, flush=True)
    print(f"{tag}: gamma={mm['gamma']} c={mm['c']}", flush=True)
    if mm['mult']:
        check(f"{tag} B-F2 c anchor: c/{mm['mult']} = c*_3(1.0) = 0.141644 "
              "(<=1e-5)", abs(mm['c'] / mm['mult'] - CSTAR3) < 1e-5)
    sol = flow(mm['gamma'], mm['c'])
    t_stop = sol.t[-1]
    # banked anchors
    hdr = open(f"/tmp/seal_s1/lib/bg_{tag}.dat").read(2500)
    t_stop_bank = float(hdr.split("f_min=0.002 at t_stop=")[1].split(";")[0])
    t1 = float(hdr.split("<1% t<")[1].split()[0])
    t5 = float(hdr.split("<5% t<")[1].split()[0])
    tseal = float(hdr.split("t_seal*(linear-layer extrap)=")[1].split(";")[0])
    dat = np.loadtxt(f"/tmp/seal_s1/lib/bg_{tag}.dat")
    check(f"{tag} B-F1a t_stop matches banked ({t_stop:.6f} vs "
          f"{t_stop_bank:.6f}, <=2e-4)", abs(t_stop - t_stop_bank) <= 2e-4)
    tq = np.clip(dat[:, 0], 0, t_stop)
    Z = sol.sol(tq)
    errX = np.max(np.abs(Z[:4].T - dat[:, 2:6]))
    fmin_re = np.array([fmin_of(Z[:4, i]) for i in range(0, len(tq),
                                                         max(1, len(tq)//40))])
    fmin_bank = dat[::max(1, len(tq)//40), 10][:len(fmin_re)]
    errF = np.max(np.abs(fmin_re - fmin_bank))
    check(f"{tag} B-F1b X(t) matches banked columns (max err {errX:.2e} "
          "<= 5e-7)", errX <= 5e-7)
    check(f"{tag} B-F1c f_min(t) matches banked (max err {errF:.2e} "
          "<= 5e-7)", errF <= 5e-7)
    # dense export grid
    tg = np.linspace(0.0, t_stop, 4097)
    Zg = sol.sol(tg)
    out[f"{tag}_t"] = tg
    out[f"{tag}_X"] = Zg[:4].T
    out[f"{tag}_Xt"] = Zg[4:].T
    out[f"{tag}_meta"] = np.array([mm['gamma'], mm['c'], t_stop, t1, t5,
                                   tseal])
    print(f"    t_stop={t_stop:.6f} trust<1%={t1} trust<5%={t5} "
          f"t_seal*={tseal}", flush=True)

np.savez("/tmp/w4b_bg.npz", **out)
print()
print("PASS:", len(PASS), " FAIL:", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
    raise SystemExit(1)
print("backgrounds banked to /tmp/w4b_bg.npz")
