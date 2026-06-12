"""BLIND VERIFIER — exact on-axis Kretschmann via symbolic theta->0 limit
with f(y,theta) = a(y) + b(y) theta^2 (smooth axis), then flow check."""
import sympy as sp
import numpy as np

T, y, th, ph = sp.symbols('T y theta phi')
a = sp.Function('a')(y)
b = sp.Function('b')(y)
fF = a + b*th**2
gdd = sp.diag(-fF, 1/fF, y**2, y**2*sp.sin(th)**2)
xs = [T, y, th, ph]
guu = sp.diag(-1/fF, fF, 1/y**2, 1/(y**2*sp.sin(th)**2))
Gam = [[[sum(guu[a_, d]*(sp.diff(gdd[d, b_], xs[c]) + sp.diff(gdd[d, c],
        xs[b_]) - sp.diff(gdd[b_, c], xs[d])) for d in range(4))/2
        for c in range(4)] for b_ in range(4)] for a_ in range(4)]
Riem = [[[[sp.diff(Gam[a_][b_][d], xs[c]) - sp.diff(Gam[a_][b_][c], xs[d])
           + sum(Gam[a_][e][c]*Gam[e][b_][d] - Gam[a_][e][d]*Gam[e][b_][c]
                 for e in range(4))
           for d in range(4)] for c in range(4)] for b_ in range(4)]
        for a_ in range(4)]
Rdddd = [[[[sum(gdd[a_, e]*Riem[e][b_][c][d] for e in range(4))
            for d in range(4)] for c in range(4)] for b_ in range(4)]
         for a_ in range(4)]
K = sp.Integer(0)
for a_ in range(4):
    for b_ in range(4):
        for c in range(4):
            for d in range(4):
                t1 = Rdddd[a_][b_][c][d]
                if t1 == 0:
                    continue
                K += t1**2*guu[a_, a_]*guu[b_, b_]*guu[c, c]*guu[d, d]
print("series K in theta...")
Kser = sp.series(K, th, 0, 1).removeO()
Kax = sp.simplify(sp.limit(Kser, th, 0))
print("K_axis =", Kax)

A, A1, A2, B, B1 = sp.symbols('A A1 A2 B B1', real=True)
sub = {sp.Derivative(a, (y, 2)): A2, sp.Derivative(a, y): A1,
       sp.Derivative(b, y): B1, a: A, b: B}
KaxS = Kax.xreplace(sub)
print("\nK_axis(A,A1,A2,B,B1) =", sp.simplify(KaxS))

# seal limit: A -> 0 with everything else fixed: leading f^2 K = A^2 K
lead = sp.limit(sp.expand(KaxS*A**2), A, 0)
print("\nf^2 K as f_pole=A -> 0 (all else fixed) =", sp.simplify(lead))
print("claim law 2 f_u^2/y^4 with f_u = -2B:  ", sp.simplify(8*B**2/y**4))

Kfun = sp.lambdify((y, A, A1, A2, B, B1), KaxS, 'numpy')

import sys
sys.path.insert(0, '/tmp/verify_mass')
from vcore import measure, QDEF, P_and_grad, Y1P, Y1PP

o = measure(1.0, 0.18413678, label='M1')
sol, t_stop = o['sol'], o['t_stop']
print("\nfull on-axis K vs limit law along M1 (own flow, exact axis limit):")
for tv in [0.6*t_stop, 0.8*t_stop, 0.95*t_stop, 0.99*t_stop, t_stop]:
    z = sol.sol(min(tv, t_stop))
    X, Xt = z[0:4], z[4:8]
    _, gP = P_and_grad(X, QDEF)
    Xtt = Xt + 2*gP
    yv = np.exp(-tv)
    Av = float(X @ Y1P)
    fu = float(X @ Y1PP)
    A1v = -float(Xt @ Y1P)/yv
    A2v = float((Xtt + Xt) @ Y1P)/yv**2
    Bv = -fu/2
    # b(y) = -f_u(y,1)/2 ; db/dy = -(1/2) d f_u/dy = +(Xt@Y1PP)/(2y)
    B1v = float(Xt @ Y1PP)/(2*yv)
    Kv = Kfun(yv, Av, A1v, A2v, Bv, B1v)
    lim2 = 2*fu*fu/yv**4
    print(f"  t={tv:.4f} f_pole={Av:.5f}: f^2K={Av*Av*Kv:.6e}  "
          f"law={lim2:.6e}  ratio={Av*Av*Kv/lim2:.6f}")
