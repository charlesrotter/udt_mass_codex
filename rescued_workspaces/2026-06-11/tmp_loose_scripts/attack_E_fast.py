"""Attack E (fast): curvature of the throat metric."""
import sympy as sp

t, r, th, ph = sp.symbols("t r theta varphi", real=True)
al, ga, J = sp.symbols("alpha gamma J", positive=True)
coords = [t, r, th, ph]
n = 4

rho = sp.sqrt(J + r**2)
f = (al*r + ga)/rho
g = sp.diag(-f, 1/f, rho**2, rho**2*sp.sin(th)**2)
ginv = g.inv()

Gam = [[[sp.simplify(sum(ginv[l, l]*(sp.diff(g[l, i], coords[j])
        + sp.diff(g[l, j], coords[i]) - sp.diff(g[i, j], coords[l]))/2
        for _ in [0])) for j in range(n)] for i in range(n)] for l in range(n)]
# (diagonal metric: only m=l term survives)

Riem = [[[[sp.S.Zero]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
for l in range(n):
    for i in range(n):
        for j in range(n):
            for k in range(j+1, n):
                e = (sp.diff(Gam[l][i][k], coords[j]) - sp.diff(Gam[l][i][j], coords[k])
                     + sum(Gam[l][j][m]*Gam[m][i][k] - Gam[l][k][m]*Gam[m][i][j]
                           for m in range(n)))
                e = sp.simplify(e)
                Riem[l][i][j][k] = e
                Riem[l][i][k][j] = -e

Ric = sp.Matrix(n, n, lambda i, j: sp.simplify(
    sum(Riem[l][i][l][j] for l in range(n))))
Rs = sp.simplify(sum(ginv[i, i]*Ric[i, i] for i in range(n)))
Gmix = sp.Matrix(n, n, lambda i, j: sp.simplify(
    ginv[i, i]*(Ric[i, j] - Rs/2*g[i, j]) if i == j else 0))
print("R =", sp.factor(Rs))
print("G^t_t =", sp.factor(sp.simplify(Gmix[0, 0])))
print("G^r_r =", sp.factor(sp.simplify(Gmix[1, 1])))
print("G^th_th =", sp.factor(sp.simplify(Gmix[2, 2])))
print("G^t_t - G^r_r =", sp.factor(sp.simplify(Gmix[0, 0] - Gmix[1, 1])))

# Kretschmann: K = R_{abcd}R^{abcd}; diagonal metric => R^{ab}_{cd} = ginv[b]*Riem
K = sp.S.Zero
for a_ in range(n):
    for b_ in range(n):
        for c_ in range(n):
            for d_ in range(n):
                Rabcd = g[a_, a_]*Riem[a_][b_][c_][d_]
                if Rabcd != 0:
                    Rup = ginv[a_, a_]*ginv[b_, b_]*ginv[c_, c_]*ginv[d_, d_]*Rabcd
                    K += Rabcd*Rup
K = sp.simplify(sp.expand(K))
print("Kretschmann K =", sp.factor(K))
print("K(r=0) =", sp.simplify(K.subs(r, 0)))
print("R(r=0) =", sp.simplify(Rs.subs(r, 0)))
print("K, R as r->oo:", sp.limit(K, r, sp.oo), sp.limit(Rs, r, sp.oo))
print("f(alpha=1) series:", sp.series((r + ga)/rho, r, sp.oo, 4))
# effective stress radial pressure vs energy density (G^t_t = -8pi rho_E etc.)
print("G^t_t + G^r_r =", sp.factor(sp.simplify(Gmix[0, 0] + Gmix[1, 1])))
