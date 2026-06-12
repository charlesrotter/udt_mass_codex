"""C1 + C3 + C5 verification runs (independent engine)."""
import numpy as np
from scipy.optimize import brentq
from v_engine import integrate, cstar, fmin_exact, gradP, GL

S3 = np.sqrt(3.0)
print("=== C1: classifier convention, ell<=1 ===")
cs1_abs = cstar(1.0, 1, 0.15, 0.30, fstop=0.02)
cs1_abs2 = cstar(1.0, 1, 0.15, 0.30, fstop=0.001, Tmax=150.0)
cs1_rel = cstar(1.0, 1, 0.15, 0.30, rel=0.02, Tmax=150.0)
print(f"c*_1 absolute fstop=0.02 : {cs1_abs:.6f}   (banked 0.206994)")
print(f"c*_1 absolute fstop=0.001: {cs1_abs2:.6f}  (insensitivity claim)")
print(f"c*_1 relative 0.02       : {cs1_rel:.6f}   (S1 claims 0.204644)")

# exhibit: near-threshold flow dipping in RELATIVE f but not ABSOLUTE
print("\nnear-threshold flows gamma=1 (between rel and abs c*):")
for c in (0.2050, 0.2055, 0.2060, 0.2065):
    sol, sealed, q = integrate(1.0, c, 1, fstop=1e-4, Tmax=250.0,
                               dense=True)
    ts = np.linspace(0, sol.t[-1], 30001)
    Z = sol.sol(ts)
    fm = np.array([fmin_exact(Z[:2, i])[0] for i in range(ts.size)])
    relv = fm/Z[0]
    print(f"  c={c:.4f}: sealed(abs 1e-4)={sealed}; min abs f_min="
          f"{fm.min():.4g} at t={ts[np.argmin(fm)]:.2f}; min rel="
          f"{relv.min():.4g}; rel<0.02 ever: {bool((relv < 0.02).any())}; "
          f"f_min(t_end={sol.t[-1]:.0f})={fm[-1]:.3g} "
          f"rising={fm[-1] > fm[-2]}")

print("\n=== C3: c* sequence (absolute classifier, fstop=0.02) ===")
cs2 = cstar(1.0, 2, 0.10, 0.30)
cs3 = cstar(1.0, 3, 0.08, 0.25)
print(f"c*: ell<=1 {cs1_abs:.6f}, ell<=2 {cs2:.6f}, ell<=3 {cs3:.6f}")
print("S1:        0.207001,      0.158948,      0.141644")
d1, d2 = cs2 - cs1_abs, cs3 - cs2
r = d2/d1
ait = cs3 + d2*r/(1 - r)
print(f"increments {d1:+.6f} {d2:+.6f}; r={r:.4f}; Aitken={ait:.5f} "
      f"(S1: 0.1319 +- 0.0097)")

print("\n=== C3-DECISIVE: ell<=4 threshold (geometric vs power-law) ===")
# geometric (r~0.36) predicts c*_4 ~ cs3 + r*d2; power-law p (from
# d2/d1 = (3/2)^-p) predicts c*_4 ~ cs3 + d2*(4/3)^-p
p = -np.log(d2/d1)/np.log(1.5)
pred_geo = cs3 + r*d2
pred_pow = cs3 + d2*(4/3.)**(-p)
print(f"p(power fit)={p:.3f}; predictions: geometric {pred_geo:.5f}, "
      f"power {pred_pow:.5f}")
cs4 = cstar(1.0, 4, 0.08, 0.25, Tmax=150.0)
d3 = cs4 - cs3
print(f"MEASURED c*_4 = {cs4:.6f}  (d3={d3:+.6f}; r23={d3/d2:.4f})")
# tail estimates with 4 terms
r2 = d3/d2
ait2 = cs4 + d3*r2/(1 - r2)
p2 = -np.log(d3/d2)/np.log(4/3.)
tail_pow = d3*sum((4./k)**p2 for k in range(5, 400))
print(f"4-term Aitken = {ait2:.5f}; power tail (p={p2:.3f}) limit ~ "
      f"{cs4 + tail_pow:.5f}")

print("\n=== C3: c=0.30 seal-locus rows, ell<=2 and ell<=3 ===")
for lmax, claim in ((2, dict(t_seal=2.169349, kap=0.736554)),
                    (3, dict(t_seal=2.013866, kap=0.689150))):
    sol, sealed, q = integrate(1.0, 0.30, lmax, fstop=0.02, dense=True)
    n = lmax + 1
    t_stop = sol.t_events[0][0]
    z = sol.sol(t_stop)
    mu, umin = fmin_exact(z[:n])
    Yp, _ = __import__('v_engine').Ymat(np.array([umin]), lmax)
    mu_t = float(z[n:] @ Yp[:, 0])
    t_seal = t_stop + mu/abs(mu_t)
    # last down-crossing of f_min = 1
    ts = np.linspace(1e-9, t_stop, 40001)
    fm = np.array([fmin_exact(sol.sol(t)[:n])[0] for t in ts])
    idx = np.where((fm[:-1] >= 1) & (fm[1:] < 1))[0]
    t_v = brentq(lambda t: fmin_exact(sol.sol(t)[:n])[0] - 1,
                 ts[idx[-1]], ts[idx[-1] + 1])
    zv = sol.sol(t_v)
    kap = S3*abs(zv[1])/zv[0]
    print(f"  ell<={lmax}: t_seal*={t_seal:.6f} (S1 {claim['t_seal']}); "
          f"kappa_cross={kap:.6f} (S1 {claim['kap']}); umin={umin:+.3f}")

print("\n=== C5: sealing-set monotonicity at NEW c values ===")
for c in (0.1435, 0.1650, 0.2500):
    row = []
    for lmax in (1, 2, 3, 4):
        _, sealed, _ = integrate(1.0, c, lmax, fstop=0.02, Tmax=150.0)
        row.append(sealed)
    mono = all(row[i] <= row[i + 1] for i in range(len(row) - 1))
    print(f"  c={c:.4f}: " + " ".join(
        f"l<={L}:{'SEAL' if s else 'SAT'}" for L, s in zip((1, 2, 3, 4), row))
        + f"   monotone={mono}")
