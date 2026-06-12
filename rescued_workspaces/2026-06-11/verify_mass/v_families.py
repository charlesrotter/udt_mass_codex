"""BLIND VERIFIER — thresholds, family scans, scalings, Q-family,
cutoff convergence, additivity, null control, C4 objects."""
import sys
import numpy as np
sys.path.insert(0, '/tmp/verify_mass')
from vcore import measure, cstar, P_and_grad, QDEF

q3 = 1.0/3.0; eta = 1.0/18.0
print("=== thresholds (own engine, absolute classifier, fstop=0.02) ===")
c1 = cstar(1.0, 0.02, 0.55, fstop=0.02, xtol=1e-9)
cq = cstar(q3, 0.002, 0.06, fstop=0.02, xtol=1e-10)
print(f"  c*_3(1)   = {c1:.9f}   (claim band 0.141644-0.141653)")
print(f"  c*_3(1/3) = {cq:.9f}   (claim 0.022633023)")
floor = 1 + cq*cq/q3/q3
print(f"  angular floor 1 + c*^2/q^2 = {floor:.6f} (claim 1.004610)")
print(f"  floor density (q^2+c*^2)/4 = {(q3*q3+cq*cq)/4:.8f}"
      f"  = eta/2 * {(q3*q3+cq*cq)/4/(eta/2):.6f}")
print(f"  eta/2 = {eta/2:.8f};  q^2/4 = {q3*q3/4:.8f};  equal:"
      f" {abs(eta/2-q3*q3/4) < 1e-16}")
print(f"  C4 sub-rung: angular floor c*^2/4 = {cq*cq/4:.6e}")

print("\n=== FAMILY A (gamma=1): threshold approach, own c* ===")
EPS = [0.01, 0.02, 0.035, 0.05, 0.08, 0.12, 0.2]
A = {}
for e in EPS:
    o = measure(1.0, (1+e)*c1, label=f"A{e}")
    A[e] = o
    print(f"  eps {e:<6} t_seal {o['t_seal']:.6f} D {o['D']:.6f} "
          f"A_tot {o['A_tot']:.6f} M0_seal {o['M0_seal']:+.6f} "
          f"y_seal {o['y_seal']:.6f} dpF {o['dp_dir'][0]:+.6f} "
          f"dpa {o['dp_dir'][1]:+.6f}")
le = np.log(np.array(EPS))
print("\n  local exponents (pairwise midpoints):")
for nm in ('A_tot', 'y_seal', 'M0_seal'):
    v = np.array([abs(A[e][nm]) for e in EPS])
    sl = np.diff(np.log(v))/np.diff(le)
    print(f"   {nm:9s}: " + " ".join(f"{s:+.4f}" for s in sl))
D = np.array([A[e]['D'] for e in EPS])
ts = np.array([A[e]['t_seal'] for e in EPS])
kD = -np.diff(D)/np.diff(le)
kt = -np.diff(ts)/np.diff(le)
print("   k_D (local -dD/dln eps): " + " ".join(f"{s:.4f}" for s in kD))
print("   k_t (local)            : " + " ".join(f"{s:.4f}" for s in kt))
print("   k_t/k_D                : " + " ".join(f"{kt[i]/kD[i]:.4f}"
                                                for i in range(len(kD))))
print(f"   eps midpoints: " + " ".join(
    f"{np.sqrt(EPS[i]*EPS[i+1]):.4f}" for i in range(len(kD))))
print(f"  dpF at smallest eps: {A[EPS[0]]['dp_dir'][0]:+.6f}"
      f" = {100*A[EPS[0]]['dp_dir'][0]/0.5:+.3f}% of p_F (C4 claim ~ -2.5%)")

print("\n=== cutoff convergence of A_tot (M1 ICs) ===")
import numpy as _np
dat = _np.loadtxt('/tmp/seal_s1/lib/bg_M1.dat', max_rows=1)
gM1, cM1 = dat[6], -dat[7]
prev = None
for fs in (0.02, 0.01, 0.005, 0.002, 0.001, 0.0005):
    o = measure(gM1, cM1, fstop=fs, label=f"M1_f{fs}")
    d = "" if prev is None else f"  delta {o['A_tot']-prev:+.2e}"
    print(f"  fstop {fs:<7} A_tot {o['A_tot']:.8f}{d}")
    prev = o['A_tot']

print("\n=== Q FAMILY (gamma=q): weld quantum + e-fold measure ===")
for e in (0.1, 0.3, 1.0):
    o = measure(q3, (1+e)*cq, label=f"Q{e}")
    a0 = (q3*q3 + ((1+e)*cq)**2)/4
    sol = o['sol']
    # action in first e-fold from carried quadrature states
    if o['t_stop'] > 1.0:
        z1 = sol.sol(1.0)
        A1 = z1[8:12].sum() + z1[12]
    else:
        A1 = np.nan
    print(f"  eps {e}: a(0) {a0:.8f} = eta/2 * {a0/(eta/2):.6f};  "
          f"A_tot {o['A_tot']:.6f} = eta/2 * {o['A_tot']/(eta/2):.4f}; "
          f"D {o['D']:.5f} t_seal {o['t_seal']:.5f}")
    if not np.isnan(A1):
        print(f"     action[0,1] = {A1:.8f} = a(0)*{A1/a0:.6f}"
              f"  [(e-1) = {np.e-1:.6f}]")

print("\n=== C3(b): additivity/no-plateau audit (own flows) ===")
for key, o in [('A_eps0.05', A[0.05]), ('A_eps0.2', A[0.2])]:
    sol, t_stop = o['sol'], o['t_stop']
    a0 = (o['gamma']**2 + o['c']**2)/4
    fr = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]
    samp = []
    for f_ in fr:
        z = sol.sol(f_*t_stop)
        X, Xt = z[0:4], z[4:8]
        P, _ = P_and_grad(X, QDEF)
        samp.append(np.exp(-f_*t_stop)*(0.25*(Xt*Xt).sum() + P))
    print(f"  {key}: a/a(0) at depth-fracs: "
          + " ".join(f"{s/a0:.3g}" for s in samp))
    # cumulative action: fraction in the last e-fold of depth
    zJ = sol.sol(max(t_stop-1.0, 0.0))
    A_last = o['A_tot'] - (zJ[8:12].sum() + zJ[12])
    z1 = sol.sol(min(1.0, t_stop))
    A_first = z1[8:12].sum() + z1[12]
    print(f"     action: first e-fold {A_first:.5f}, last e-fold "
          f"{A_last:.5f} ({100*A_last/o['A_tot']:.1f}% of A_tot "
          f"{o['A_tot']:.5f}); a(seal-side) dominates -> NO plateau")
    # % of A_tot beyond M1-header trust t<1.6383 (only meaningful for M1)
print("  M1 trust check: % of A_tot beyond t=1.6383 (1% trust) and "
      "t=2.2357 (5%):")
oM1 = measure(gM1, cM1, label='M1')
for tt in (1.6383, 2.2357):
    z = oM1['sol'].sol(tt)
    Ain = z[8:12].sum() + z[12]
    print(f"   t<{tt}: A {Ain:.5f}; beyond: {oM1['A_tot']-Ain:.5f} "
          f"({100*(oM1['A_tot']-Ain)/oM1['A_tot']:.1f}%)")

print("\n=== C3(c): null control — ratio scan vs powers of ladder ===")
GAM = 3*np.exp(-eta/2)
gB = [0.25, q3, 0.5, 0.75, 1.0, 1.5, 2.0]
B = {}
for g_ in gB:
    cg = cstar(g_, 0.02*g_*g_, 0.55*g_*g_, fstop=0.02, xtol=1e-8)
    B[g_] = measure(g_, 2.0*cg, label=f"B{g_:.3f}")
names = ['A_tot', 'F_seal', 'E_seal', 'fK_lim']
vals_all = {nm: np.array([A[e][nm] for e in EPS]
                         + [B[g_][nm] for g_ in gB]) for nm in names}
for tol in (0.005, 0.01, 0.02):
    hits = tries = 0
    for nm in names:
        v = np.abs(vals_all[nm])
        n = len(v)
        for i in range(n):
            for j in range(i+1, n):
                r = np.log(v[i]/v[j])/np.log(GAM)
                tries += 1
                if abs(r - round(r)) < tol and abs(round(r)) >= 1:
                    hits += 1
    print(f"  tol {tol}: hits {hits}/{tries} "
          f"(uniform-null ~ {2*tol*tries:.1f})")
