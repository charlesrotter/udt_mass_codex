"""BLIND VERIFIER — full Kretschmann from scratch; Schwarzschild check;
then the on-axis seal limit law on a real flow (own engine)."""
import sympy as sp
import numpy as np

T, y, th, ph = sp.symbols('T y theta phi')
fF = sp.Function('f')(y, th)
gdd = sp.diag(-fF, 1/fF, y**2, y**2*sp.sin(th)**2)
xs = [T, y, th, ph]
guu = gdd.inv()
Gam = [[[sp.simplify(sum(guu[a, d]*(sp.diff(gdd[d, b], xs[c])
        + sp.diff(gdd[d, c], xs[b]) - sp.diff(gdd[b, c], xs[d]))
        for d in range(4))/2) for c in range(4)] for b in range(4)]
       for a in range(4)]
Riem = [[[[sp.diff(Gam[a][b][d], xs[c]) - sp.diff(Gam[a][b][c], xs[d])
           + sum(Gam[a][e][c]*Gam[e][b][d] - Gam[a][e][d]*Gam[e][b][c]
                 for e in range(4))
           for d in range(4)] for c in range(4)] for b in range(4)]
        for a in range(4)]
Rdddd = [[[[sum(gdd[a, e]*Riem[e][b][c][d] for e in range(4))
            for d in range(4)] for c in range(4)] for b in range(4)]
         for a in range(4)]
K = sp.Integer(0)
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                t1 = Rdddd[a][b][c][d]
                if t1 == 0:
                    continue
                K += t1*guu[a, a]*guu[b, b]*guu[c, c]*guu[d, d]*t1
                # metric diagonal => raising is diagonal
K = sp.simplify(K)

# --- Schwarzschild check ---
M = sp.symbols('M', positive=True)
fs = 1 - 2*M/y
Ksch = K.subs(fF, fs).doit()
reps = {sp.Derivative(fF, y): sp.diff(fs, y),
        sp.Derivative(fF, (y, 2)): sp.diff(fs, y, 2),
        sp.Derivative(fF, th): 0, sp.Derivative(fF, (th, 2)): 0,
        sp.Derivative(fF, y, th): 0, fF: fs}
Ksch = sp.simplify(K.xreplace(reps))
print("Schwarzschild K =", Ksch, " (expect 48 M^2/y^6):",
      sp.simplify(Ksch - 48*M**2/y**6) == 0)

# --- generic-symbol form for numerics ---
f0s, fys, fths, fyys, fthths, fyths = sp.symbols(
    'f0 fy fth fyy fthth fyth', real=True)
def dmap(d):
    cnt = {y: 0, th: 0}
    for v, n in d.variable_count:
        cnt[v] += n
    key = (cnt[y], cnt[th])
    return {(1, 0): fys, (2, 0): fyys, (0, 1): fths, (0, 2): fthths,
            (1, 1): fyths}[key]
repl = {d: dmap(d) for d in K.atoms(sp.Derivative)}
repl[fF] = f0s
Ksym = K.xreplace(repl)
assert not Ksym.atoms(sp.Derivative), "unreplaced derivatives remain"
Kfun = sp.lambdify((y, th, f0s, fys, fths, fyys, fthths, fyths),
                   Ksym, 'numpy')
import pickle
with open('/tmp/verify_mass/K_own.pkl', 'wb') as fh:
    pickle.dump(sp.srepr(Ksym), fh)

# --- exact symbolic axis limit, mpmath high precision, ordered limits ---
print("\naxis-config exact ordered limit (th->0 first, then F0->0), no")
print("radial derivs:")
F0sym, Gsym = sp.symbols('F0 G', positive=True)
Kax = Ksym.subs({fys: 0, fyys: 0, fths: 2*Gsym*th, fthths: 2*Gsym,
                 fyths: 0, f0s: F0sym + Gsym*th**2})
Kax0 = sp.limit(Kax, th, 0)
lead = sp.limit(sp.expand(Kax0*F0sym**2), F0sym, 0)
print("  f^2 K ->", sp.simplify(lead), " ; claim-law 2 f_u^2/y^4 = 8 G^2/y^4")

# --- full-K on a real flow (own engine) ---
import sys
sys.path.insert(0, '/tmp/verify_mass')
from vcore import measure, QDEF, P_and_grad, Y1P, Y1PP

o = measure(1.0, 0.18413678, label='M1')   # library M1 ICs
sol = o['sol']
t_stop = o['t_stop']
print("\nfull-K vs limit law along M1 (own flow), th=1e-6:")
for tv in [0.6*t_stop, 0.8*t_stop, 0.95*t_stop, 0.99*t_stop, t_stop]:
    z = sol.sol(min(tv, t_stop))
    X, Xt = z[0:4], z[4:8]
    _, gP = P_and_grad(X, QDEF)
    Xtt = Xt + 2*gP
    yv = np.exp(-tv)
    f0 = float(X @ Y1P)
    fu = float(X @ Y1PP)
    fuy = -float(Xt @ Y1PP)/yv
    fy = -float(Xt @ Y1P)/yv
    fyy = float((Xtt + Xt) @ Y1P)/yv**2
    thv = 1e-6
    fv = f0 - fu*thv**2/2
    fth = -fu*thv
    fthth = -fu
    fyth = -fuy*thv
    Kv = Kfun(yv, thv, fv, fy, fth, fyy, fthth, fyth)
    lim2 = 2*fu*fu/yv**4
    lim4 = 4*fu*fu/yv**4
    print(f"  t={tv:.4f} f_pole={f0:.5f}: f^2K={f0*f0*Kv:.6e}  "
          f"/(2fu^2/y^4)={f0*f0*Kv/lim2:.4f}  /(4fu^2/y^4)={f0*f0*Kv/lim4:.4f}")
