"""BLIND VERIFIER — N2 claim A3: character of the evolution system.

C-1: reduced EOM on the exact (moving-spherical) branch, my own EL.
C-2: principal symbol ellipticity.
C-3: Class-B mixed-type partition by Q=0 — my own scan (own RNG, own
     Schur elimination, plus identification of the timelike direction).
"""
import numpy as np
import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
def zc(e):
    return sp.cancel(sp.together(e)) == 0

# ---------------- C-1: reduced EOM (my own EL) ----------------------
T, rr = sp.symbols('T r', positive=True)
c = sp.Symbol('c', positive=True)
ff = sp.Function('f', positive=True)(T, rr)
L = -Ra(1, 8)*c*rr**2*(sp.diff(ff, rr)**2 + sp.diff(ff, T)**2/ff**2)
EL = (sp.diff(sp.diff(L, sp.diff(ff, T)), T)
      + sp.diff(sp.diff(L, sp.diff(ff, rr)), rr) - sp.diff(L, ff))
phi = sp.Function('phi', real=True)(T, rr)
ELphi = sp.simplify(EL.subs(ff, sp.exp(-2*phi)).doit())
target = (rr**2*sp.diff(phi, T, 2)
          + sp.diff(rr**2*sp.exp(-4*phi)*sp.diff(phi, rr), rr)
          + 2*rr**2*sp.exp(-4*phi)*sp.diff(phi, rr)**2)
ratio = sp.simplify(sp.cancel(sp.together(ELphi/target)))
print("    EL/target =", ratio)
check("C-1 my EL of L_red == (c/2) e^{2 phi} [r^2 phi_TT + (r^2 f^2 "
      "phi_r)' + 2 r^2 f^2 phi_r^2]  (positive multiple)",
      sp.simplify(ratio - c*sp.exp(2*phi)/2) == 0)
# static limit -> (r^2 f')' = 0 -> f = C + a/r
f0 = sp.Function('f0', positive=True)(rr)
ELst = sp.simplify(EL.subs(ff, f0).doit())
Cc, av = sp.symbols('C a_v', positive=True)
check("C-1b static limit: f = C + a/r solves it",
      sp.simplify(ELst.subs(f0, Cc + av/rr).doit()) == 0)

# ---------------- C-2: principal symbol -----------------------------
f, vT, vr = sp.symbols('f vT vr', positive=True, real=True)
Lred = -(rr**2)*(vr**2 + vT**2/f**2)/8     # drop c, s_th > 0
H = sp.hessian(Lred, (vT, vr))
ev = [sp.simplify(H[0, 0]), sp.simplify(H[1, 1]), sp.simplify(H[0, 1])]
check("C-2 Hessian = -(1/4) r^2 diag(1/f^2, 1): NEGATIVE DEFINITE -> "
      "quasilinear ELLIPTIC in (T,r); no real characteristics",
      zc(ev[0] + rr**2/(4*f**2)) and zc(ev[1] + rr**2/4) and ev[2] == 0)
# linearization around static f0(r): modes dphi = e^{kT} u(r) demand
# k^2 = sigma_n of a Sturm-Liouville problem, sigma_n -> +infinity:
# Hadamard ill-posedness of the T-Cauchy problem is the statement that
# the growth-rate set {sqrt(sigma_n)} is unbounded. (analytic; the
# numeric demo is in v_a4.py)

# ---------------- C-3: Class-B partition, my own scan ----------------
fL, AL = sp.symbols('fL AL', positive=True)
qS = sp.Symbol('qS', real=True)
vTs, vrs, vhs = sp.symbols('vTs vrs vhs', real=True)
D2L = AL/fL - qS**2
PL = AL*vrs**2 - 2*qS*vrs*vhs + vhs**2/fL
RL = fL*PL + D2L*vTs**2
QL = fL*PL - D2L*vTs**2
# eliminated L on the Q>0 branch (sign convention: L ~ -R/sqrt(fD2));
# stationary equations and Hessian signatures are what we scan.
LB = -RL/sp.sqrt(fL*D2L)
vlist = (vTs, vrs, vhs)
H3 = sp.hessian(LB, vlist)
gq = [sp.diff(sp.diff(LB, qS), v) for v in vlist]
hqq = sp.diff(LB, qS, 2)
F_H3 = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), H3, 'numpy')
F_gq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), gq, 'numpy')
F_hqq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), hqq, 'numpy')
F_Q = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), QL, 'numpy')

rng = np.random.default_rng(987654321)   # my own seed
def qroot_static_connected(fv, Av, vrv, vhv, vTv):
    c3 = vTv**2
    c1 = fv*Av*vrv**2 + vhv**2 - (Av/fv)*vTv**2
    c0 = -2*Av*vrv*vhv
    if c3 < 1e-300:
        return -c0/c1 if c1 != 0 else None
    rts = np.roots([c3, 0.0, c1, c0])
    rts = [z.real for z in rts if abs(z.imag) < 1e-9*max(1.0, abs(z))]
    if not rts:
        return None
    qstat = 2*Av*vrv*vhv/(fv*Av*vrv**2 + vhv**2)
    return min(rts, key=lambda z: abs(z - qstat))

sigs = {}
n_tot = n_match = 0
n_plus_is_vh = 0
n_plus_tot = 0
for _ in range(6000):
    fv = float(np.exp(rng.uniform(np.log(0.05), np.log(20.0))))
    Av = float(np.exp(rng.uniform(np.log(0.05), np.log(20.0))))
    vrv, vhv, vTv = rng.normal(size=3)*10**rng.uniform(-1, 1, size=3)
    qv = qroot_static_connected(fv, Av, vrv, vhv, vTv)
    if qv is None or Av/fv - qv**2 <= 1e-8:
        continue
    try:
        Hvv = np.array(F_H3(vrv*0+vTv, vrv, vhv, qv, fv, Av), float)
        gvec = np.array(F_gq(vTv, vrv, vhv, qv, fv, Av), float)
        hq = float(F_hqq(vTv, vrv, vhv, qv, fv, Av))
    except Exception:
        continue
    if not np.isfinite(hq) or abs(hq) < 1e-10:
        continue
    Heff = Hvv - np.outer(gvec, gvec)/hq
    if not np.all(np.isfinite(Heff)):
        continue
    w, V = np.linalg.eigh(Heff)
    if np.min(np.abs(w)) < 1e-9*np.max(np.abs(w)):
        continue
    sig = tuple(int(np.sign(x)) for x in w)
    sigs[sig] = sigs.get(sig, 0) + 1
    n_tot += 1
    Qv = float(F_Q(vTv, vrv, vhv, qv, fv, Av))
    ok = (Qv > 0 and sig == (-1, -1, 1)) or (Qv < 0 and sig == (-1, -1, -1))
    n_match += ok
    if sig == (-1, -1, 1):
        n_plus_tot += 1
        # direction of the + eigenvalue: is it vh(theta)-dominated?
        vplus = V[:, 2]
        if abs(vplus[2]) == np.max(np.abs(vplus)):
            n_plus_is_vh += 1
print("    signatures:", sigs)
print(f"    sgn(Q) classification: {n_match}/{n_tot}")
print(f"    + eigenvector theta-dominated: {n_plus_is_vh}/{n_plus_tot}")
check("C-3a Class-B is mixed type partitioned EXACTLY by Q=0: "
      "Q>0 -> (-,-,+) Lorentzian; Q<0 -> definite (elliptic) "
      "[my own scan, own seed]", n_tot > 3000 and n_match == n_tot)
check("C-3b in the Lorentzian region the + (timelike) direction is "
      "theta-dominated in the large majority of samples (theta marches; "
      "T never does)", n_plus_tot > 500
      and n_plus_is_vh/max(n_plus_tot, 1) > 0.9)

print()
print("PASS", len(PASS), "FAIL", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
