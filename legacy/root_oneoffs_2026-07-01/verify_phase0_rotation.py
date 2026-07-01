"""
B1 check: off-diagonal g_{t psi} = eps w(t,r,theta) rotation perturbation.
Confirm (a) the freezing constraints relax (G_tr=0 etc at O(eps)),
(b) d_t-carrying eqs factor, (c) HONESTLY: nontrivial joint existence unshown.
"""
import sympy as sp

t, r, th, ps, eps = sp.symbols('t r theta psi epsilon', real=True)
w = sp.Function('w')(t, r, th)
x = [t, r, th, ps]

g = sp.zeros(4, 4)
g[0, 0] = -1
g[1, 1] = 1
g[2, 2] = r**2
g[3, 3] = r**2*sp.sin(th)**2
g[0, 3] = eps*w
g[3, 0] = eps*w

ginv = g.inv()

def christoffel(g, ginv, x):
    n = len(x); Gam = [[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], x[cc]) + sp.diff(g[d, cc], x[b]) - sp.diff(g[b, cc], x[d]))
                Gam[a][b][cc] = s/2
    return Gam

Gam = christoffel(g, ginv, x)

def ricci(Gam, x):
    n = len(x); Ric = sp.zeros(n, n)
    for a in range(n):
        for b in range(n):
            s = 0
            for cc in range(n):
                s += sp.diff(Gam[cc][a][b], x[cc]) - sp.diff(Gam[cc][a][cc], x[b])
                for d in range(n):
                    s += Gam[cc][cc][d]*Gam[d][a][b] - Gam[cc][a][d]*Gam[d][b][cc]
            Ric[a, b] = s
    return Ric

Ric = ricci(Gam, x)
Rscal = sum(ginv[a, b]*Ric[a, b] for a in range(4) for b in range(4))

def lin(expr):
    ser = sp.series(expr, eps, 0, 2).removeO()
    return sp.simplify(sp.diff(ser, eps).subs(eps, 0))

names = ['t', 'r', 'th', 'ps']
for (a, b) in [(0,1),(0,2),(1,2),(0,3),(1,3),(2,3)]:
    Gab = Ric[a, b] - sp.Rational(1,2)*g[a, b]*Rscal
    print(f"G_{names[a]}{names[b]} =", lin(Gab))
