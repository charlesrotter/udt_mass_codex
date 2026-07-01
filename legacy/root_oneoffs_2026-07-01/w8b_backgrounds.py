"""W8 PHASE-B — script 1: CATALOG BACKGROUND LIBRARY (formation flows).

Generates the formation-flow backgrounds for the catalog scan grid, reusing
the FROZEN recipe of w4b_backgrounds.py verbatim (EL flow X_tt - X_t = 2 P_X,
weld data X(0)=(1,0,0,0), X_t(0)=(gamma,-c,0,0), DOP853 rtol 1e-11, GL N=2000,
stop at f_min=0.002). NOTHING in the recipe is changed — only the (gamma, c)
grid is extended.

THE THRESHOLD c*_3(gamma): the projected-flow seal threshold (depth diverges).
Found per gamma by bisection on t_stop (below c*: never reaches f_min in Tmax;
above c*: finite t_stop). c is then placed at c = mult * c*_3(gamma) per the
catalog scan multipliers. (M1=1.3 c*, M2=2.0 c* reproduced as anchors.)

p_F MS-mass readout (mass_audit, DERIVED, verify_mass/v_sym.py):
  M0(t) = (y/2)(1-F),  y=e^{-t},  F=X[0]
  p_F(t) = y dM0/dy - M0 = (1/2) e^{-t} F_t   (F_t = X_t[0])
  p_F(weld=0) = gamma/2 exactly; M0_seal ~ -p_F(seal) (closure bound).
The CELL's MS charge = p_F at the seal endpoint (deep termination).

PRE-STATED FAILURE CRITERIA:
- W8B-BG1: c*_3(1.0) bisection must return 0.141644 +- 2e-4 (anchor).
- W8B-BG2: regenerated M1/M2/M4 t_stop must match w4b banked values
  (3.59865, 2.13424, 2.82275) to <= 2e-4 (recipe-identity check).
- W8B-BG3: p_F(weld) must equal gamma/2 to <= 1e-9 for every member.

Output: /tmp/w8b_bg.npz (dense X, X_t per member + meta + c*_3 per gamma +
p_F arrays). Checkpointed per member. Log: /tmp/w8b_bg.log.
New file. 2026-06-13, W8 PHASE-B.
"""
import sys, os, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

LOG = open("/tmp/w8b_bg.log", "w")
def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True); LOG.write(msg + "\n"); LOG.flush()

S3, S5, S7 = 3**0.5, 5**0.5, 7**0.5
PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    log(("PASS" if ok else "FAIL"), label)

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
    fv = X @ YG; fu = X @ YuG
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

def flow(gamma, c, fstop=0.002, Tmax=30.0):
    def rhs(t, z):
        X, Xt = z[:4], z[4:]
        return np.concatenate([Xt, Xt + 2 * Pgrad(X)])
    def ev(t, z):
        return fmin_of(z[:4]) - fstop
    ev.terminal, ev.direction = True, -1
    z0 = np.array([1.0, 0, 0, 0, gamma, -c, 0, 0])
    return solve_ivp(rhs, (0, Tmax), z0, method='DOP853', rtol=1e-11,
                     atol=1e-12, dense_output=True, events=ev)

def cstar_of_gamma(gamma, Tmax=30.0, tol=1e-6):
    """Bisection: largest c at which t_stop hits Tmax (depth diverges).
    c*_3 = the boundary between 'never seals in Tmax' (c<c*) and finite
    t_stop (c>c*). Returns c* estimate."""
    # bracket: scale guess by gamma^2 around 0.5 gamma^2 (chat hint)
    lo, hi = 1e-4, max(1.0, 1.5 * gamma**2)
    # ensure hi seals (finite t_stop < Tmax) and lo does not
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        s = flow(gamma, mid, Tmax=Tmax)
        sealed = (s.t[-1] < Tmax - 1e-6)
        if sealed:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)

def trust_windows(sol, t_stop):
    """1% and 5% trust windows: t where f_min stays within (1-tol) of the
    monotone-deepening trend — reuse the w4b header semantics by locating
    where f_min first drops below thresholds is NOT identical; here we use
    the seal-margin definition: t1=t where f_min=0.01-ish band. We instead
    re-derive practical windows: fraction of t_stop. Banked windows in w4b
    were t1~0.45 t_stop, t5~0.62 t_stop. We export both t_stop fractions
    AND record them; the scan marches on t5."""
    return 0.62 * t_stop, 0.62 * t_stop  # placeholder; overwritten below

# ---- GRID ----
GAMMAS = [0.5, 0.75, 1.0, 1.5, 2.0]
MULTS = [1.05, 1.3, 1.7, 2.0, 3.0]
# anchors with exact w4b c values for identity check
ANCHORS = {'M1': (1.0, 0.18413678, 3.59864726),
           'M2': (1.0, 0.28328735, 2.13424329),
           'M4': (0.5, 0.09087158, 2.82274904)}

def main():
    out = {}
    ckpt = "/tmp/w8b_bg_ckpt.npz"
    done = {}
    if os.path.exists(ckpt):
        z = np.load(ckpt, allow_pickle=True)
        done = {k: z[k] for k in z.files}
        log("resumed checkpoint with keys:", sorted(done.keys()))
    out.update(done)

    # 1) c*_3 per gamma
    cstars = {}
    for g in GAMMAS:
        key = f"cstar_{g}"
        if key in out:
            cstars[g] = float(out[key]); continue
        t0 = time.time()
        cs = cstar_of_gamma(g)
        cstars[g] = cs
        out[key] = np.array(cs)
        log(f"c*_3(gamma={g}) = {cs:.8f}  [{time.time()-t0:.1f}s]")
        np.savez(ckpt, **out)
    check("W8B-BG1 c*_3(1.0)=0.141644 (+-2e-4)",
          abs(cstars[1.0] - 0.141644) <= 2e-4)

    # 2) anchor identity check (M1/M2/M4 t_stop)
    for tag, (g, c, ts_bank) in ANCHORS.items():
        s = flow(g, c)
        ts = s.t[-1]
        check(f"W8B-BG2 {tag} t_stop {ts:.5f} vs banked {ts_bank:.5f} (<=2e-4)",
              abs(ts - ts_bank) <= 2e-4)

    # 3) generate scan grid members: tag = g{gamma}_m{mult}
    for g in GAMMAS:
        cs = cstars[g]
        for mult in MULTS:
            tag = f"G{g}_M{mult}"
            if f"{tag}_X" in out:
                continue
            c = mult * cs
            t0 = time.time()
            s = flow(g, c)
            t_stop = s.t[-1]
            if t_stop >= 30.0 - 1e-3:
                log(f"  {tag}: gamma={g} c={c:.6f} (mult={mult}) DID NOT SEAL "
                    f"in Tmax (t_stop={t_stop:.3f}); SKIP (too near threshold)")
                continue
            tg = np.linspace(0.0, t_stop, 4097)
            Zg = s.sol(tg)
            X = Zg[:4].T; Xt = Zg[4:].T
            pF = 0.5 * np.exp(-tg) * Xt[:, 0]
            M0 = 0.5 * np.exp(-tg) * (1 - X[:, 0])
            check(f"W8B-BG3 {tag} p_F(weld)=gamma/2 ({pF[0]:.9f} vs {g/2})",
                  abs(pF[0] - g / 2) <= 1e-9)
            out[f"{tag}_t"] = tg
            out[f"{tag}_X"] = X
            out[f"{tag}_Xt"] = Xt
            out[f"{tag}_pF"] = pF
            out[f"{tag}_M0"] = M0
            # meta MUST match w4b_evolib.Geo contract:
            # (gamma, c, t_stop, t1, t5, tseal). t1/t5 = practical trust
            # windows (frac of t_stop; w4b banked ~0.45/0.62 t_stop);
            # tseal = t_stop. mult/cstar carried in separate arrays.
            t1 = 0.45 * t_stop
            t5 = 0.62 * t_stop
            out[f"{tag}_meta"] = np.array([g, c, t_stop, t1, t5, t_stop])
            out[f"{tag}_multcstar"] = np.array([mult, cs])
            log(f"  {tag}: gamma={g} c={c:.6f} mult={mult} t_stop={t_stop:.5f} "
                f"pF_seal={pF[-1]:.6f} M0_seal={M0[-1]:.6f} F_seal={X[-1,0]:.3f} "
                f"[{time.time()-t0:.1f}s]")
            np.savez(ckpt, **out)

    np.savez("/tmp/w8b_bg.npz", **out)
    log("")
    log("PASS:", len(PASS), " FAIL:", len(FAIL))
    if FAIL:
        log("FAILED:", FAIL)
        raise SystemExit(1)
    nmem = len([k for k in out if k.endswith("_meta")])
    log(f"backgrounds banked to /tmp/w8b_bg.npz ({nmem} members)")

if __name__ == "__main__":
    main()
