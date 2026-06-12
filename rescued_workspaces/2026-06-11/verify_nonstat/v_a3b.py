"""C-3b redone invariantly: which COORDINATE AXES lie inside the
positive (timelike) cone of the Class-B effective Hessian?
Hyperbolic propagation in T requires e_T . H_eff . e_T > 0 somewhere.
"""
import numpy as np
import sympy as sp

fL, AL = sp.symbols('fL AL', positive=True)
qS = sp.Symbol('qS', real=True)
vTs, vrs, vhs = sp.symbols('vTs vrs vhs', real=True)
D2L = AL/fL - qS**2
PL = AL*vrs**2 - 2*qS*vrs*vhs + vhs**2/fL
RL = fL*PL + D2L*vTs**2
QL = fL*PL - D2L*vTs**2
LB = -RL/sp.sqrt(fL*D2L)
vlist = (vTs, vrs, vhs)
H3 = sp.hessian(LB, vlist)
gq = [sp.diff(sp.diff(LB, qS), v) for v in vlist]
hqq = sp.diff(LB, qS, 2)
F_H3 = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), H3, 'numpy')
F_gq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), gq, 'numpy')
F_hqq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), hqq, 'numpy')
F_Q = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), QL, 'numpy')

rng = np.random.default_rng(31415926)
def qroot(fv, Av, vrv, vhv, vTv):
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

nL = 0
nT_pos = nr_pos = nh_pos = 0
for _ in range(8000):
    fv = float(np.exp(rng.uniform(np.log(0.05), np.log(20.0))))
    Av = float(np.exp(rng.uniform(np.log(0.05), np.log(20.0))))
    vrv, vhv, vTv = rng.normal(size=3)*10**rng.uniform(-1, 1, size=3)
    qv = qroot(fv, Av, vrv, vhv, vTv)
    if qv is None or Av/fv - qv**2 <= 1e-8:
        continue
    try:
        Hvv = np.array(F_H3(vTv, vrv, vhv, qv, fv, Av), float)
        gv = np.array(F_gq(vTv, vrv, vhv, qv, fv, Av), float)
        hq = float(F_hqq(vTv, vrv, vhv, qv, fv, Av))
    except Exception:
        continue
    if not np.isfinite(hq) or abs(hq) < 1e-10:
        continue
    He = Hvv - np.outer(gv, gv)/hq
    if not np.all(np.isfinite(He)):
        continue
    Qv = float(F_Q(vTv, vrv, vhv, qv, fv, Av))
    if Qv <= 0:
        continue
    nL += 1
    sc = np.abs(np.diag(He)).max()
    nT_pos += He[0, 0] > 1e-10*sc
    nr_pos += He[1, 1] > 1e-10*sc
    nh_pos += He[2, 2] > 1e-10*sc
print(f"Lorentzian (Q>0) samples: {nL}")
print(f"  e_T in positive cone: {nT_pos}   e_r: {nr_pos}   "
      f"e_theta: {nh_pos}")
ok = (nL > 3000 and nT_pos == 0 and nh_pos/nL > 0.99)
print(("PASS" if ok else "FAIL"),
      "C-3b' T axis is NEVER in the timelike cone; theta axis is "
      "(invariant axis test): hyperbolic march is ANGULAR, never T")
