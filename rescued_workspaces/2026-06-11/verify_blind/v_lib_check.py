"""C7: library integrity. Re-integrate M1 and M2 jets with my engine,
compare profiles on the file's own t-grid; recheck shell figures and
conventions for M2 (kappa_cross) and M1.
"""
import numpy as np
from scipy.optimize import brentq
from v_engine import integrate, fmin_exact, Ymat

S3 = np.sqrt(3.0)

def load(tag):
    d = np.loadtxt(f"/tmp/seal_s1/lib/bg_{tag}.dat")
    hdr = open(f"/tmp/seal_s1/lib/bg_{tag}.dat").read().split("\n")[:7]
    return d, hdr

for tag, gam, c, trust1 in (("M1", 1.0, 0.18413678, 1.6383),
                            ("M2", 1.0, 0.28328735, 1.1680)):
    d, hdr = load(tag)
    t, y, F, a1, g2, h3 = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    fmin_f, umin_f = d[:, 10], d[:, 11]
    sol, sealed, q = integrate(gam, c, 3, fstop=0.002, dense=True, Nq=1500,
                               rtol=1e-11, atol=1e-13)
    assert sealed
    t_stop = sol.t_events[0][0]
    # compare on the file grid up to my t_stop
    selA = t <= min(trust1, t_stop)             # stated 1% trust region
    selB = t <= t_stop                          # entire file
    Z = sol.sol(t[selB])
    mine = Z[:4].T
    theirs = d[selB][:, 2:6]
    # relative error on f_min and on the 4 amplitudes (where nonzero)
    fm_mine = np.array([fmin_exact(Z[:4, i])[0] for i in range(Z.shape[1])])
    relf = np.abs(fm_mine - fmin_f[selB])/np.abs(fmin_f[selB])
    relF = np.abs(mine[:, 0] - theirs[:, 0])/np.abs(theirs[:, 0])
    print(f"{tag}: t_stop(mine)={t_stop:.6f} vs file {hdr[3].split('t_stop=')[1].split(';')[0]}")
    print(f"  whole-file  max rel diff: F {relF.max():.2e}; "
          f"f_min {relf.max():.2e}  (claim <1% in trust region; this is "
          f"the SAME truncation so should be ~solver tol)")
    iA = np.where(selA[selB])[0]
    print(f"  trust-region(1%) max rel diff: F {relF[iA].max():.2e}; "
          f"f_min {relf[iA].max():.2e}")
    # u_min column sanity
    um = np.array([fmin_exact(Z[:4, i])[1] for i in range(Z.shape[1])])
    print(f"  u_min agreement: max|diff| = {np.abs(um - umin_f[selB]).max():.2e}")
    # shell figures: t_v, kappa_cross
    ts = np.linspace(1e-9, t_stop, 40001)
    fm = np.array([fmin_exact(sol.sol(tt)[:4])[0] for tt in ts])
    idx = np.where((fm[:-1] >= 1) & (fm[1:] < 1))[0]
    t_v = brentq(lambda tt: fmin_exact(sol.sol(tt)[:4])[0] - 1,
                 ts[idx[-1]], ts[idx[-1] + 1])
    zv = sol.sol(t_v)
    kap = S3*abs(zv[1])/zv[0]
    Fc = zv[0]
    # t_seal extrapolation from cutoff
    z = sol.sol(t_stop)
    v = np.sqrt(2*np.arange(4) + 1.0)
    mu, mu_t = float(z[:4] @ v), float(z[4:] @ v)
    t_seal = t_stop + mu/abs(mu_t)
    print(f"  shell: t_v={t_v:.6f}, kappa_cross={kap:.6f}, F_cross={Fc:.4f}, "
          f"t_seal*={t_seal:.6f}")
    print(f"  file : {hdr[5][2:]}")
    print()

# trust-region INDEPENDENT check for M2: my own ell<=2 vs ell<=3 1% locus
print("M2 trust-region re-derivation (ell<=2 vs ell<=3 f_min, 1%):")
sol3, _, _ = integrate(1.0, 0.28328735, 3, fstop=0.002, dense=True, Nq=1500)
sol2, _, _ = integrate(1.0, 0.28328735, 2, fstop=0.002, dense=True, Nq=1500)
tc = min(sol3.t_events[0][0], sol2.t_events[0][0])
tg = np.linspace(1e-6, tc*(1 - 1e-9), 3001)
f3 = np.array([fmin_exact(sol3.sol(tt)[:4])[0] for tt in tg])
f2 = np.array([fmin_exact(sol2.sol(tt)[:3])[0] for tt in tg])
rel = np.abs(f2 - f3)/np.abs(f3)
bad = np.where(rel > 0.01)[0]
t1pc = tg[bad[0]] if len(bad) else tc
bad5 = np.where(rel > 0.05)[0]
t5pc = tg[bad5[0]] if len(bad5) else tc
print(f"  my 1% locus t={t1pc:.4f} (file: 1.1680); 5% locus t={t5pc:.4f} "
      f"(file: 1.5313)")
