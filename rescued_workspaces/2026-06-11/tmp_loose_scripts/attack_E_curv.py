"""Attack E: GR identity of the throat rho=sqrt(J+r^2), f=(alpha r+gamma)/rho.
Full curvature: Einstein tensor, Ricci scalar, Kretschmann; neck regularity;
comparison handles (Ellis/Bronnikov, RN expansion)."""
import sympy as sp

t, r, th, ph = sp.symbols("t r theta varphi", real=True)
al, ga, J = sp.symbols("alpha gamma J", positive=True)
coords = [t, r, th, ph]

rho = sp.sqrt(J + r**2)
f = (al*r + ga)/rho
g = sp.diag(-f, 1/f, rho**2, rho**2*sp.sin(th)**2)
ginv = g.inv()
n = 4
Gam = [[[sp.simplify(sum(ginv[l, m]*(sp.diff(g[m, i], coords[j])
        + sp.diff(g[m, j], coords[i]) - sp.diff(g[i, j], coords[m]))
        for m in range(n))/2) for j in range(n)] for i in range(n)] for l in range(n)]
Riem = {}
Ric = sp.zeros(n, n)
for i in range(n):
    for j in range(n):
        e = sum(sp.diff(Gam[l][i][j], coords[l]) - sp.diff(Gam[l][i][l], coords[j])
                for l in range(n))
        e += sum(Gam[l][l][m]*Gam[m][i][j] - Gam[l][j][m]*Gam[m][i][l]
                 for l in range(n) for m in range(n))
        Ric[i, j] = sp.simplify(e)
Rs = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n)))
Gmix = sp.simplify(ginv*(Ric - Rs/2*g))
print("Ricci scalar R =", sp.factor(sp.simplify(Rs)))
print("G^t_t =", sp.simplify(Gmix[0, 0]))
print("G^r_r =", sp.simplify(Gmix[1, 1]))
print("G^th_th =", sp.simplify(Gmix[2, 2]))
print("G^t_t - G^r_r =", sp.simplify(Gmix[0, 0] - Gmix[1, 1]))
print("NOT Ricci-flat (vacuum)?  R_tt =", sp.simplify(Ric[0, 0]) != 0)

# Kretschmann at the neck r=0 (use full Riemann)
def riemann_up(l, i, j, k):
    e = (sp.diff(Gam[l][i][k], coords[j]) - sp.diff(Gam[l][i][j], coords[k])
         + sum(Gam[l][j][m]*Gam[m][i][k] - Gam[l][k][m]*Gam[m][i][j]
               for m in range(n)))
    return sp.simplify(e)

K = sp.S.Zero
Rup = {}
for l in range(n):
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if j < k:
                    Rup[(l, i, j, k)] = riemann_up(l, i, j, k)
# K = R_abcd R^abcd
Rdown = {}
for (l, i, j, k), v in Rup.items():
    Rdown[(l, i, j, k)] = sp.simplify(sum(g[l, m]*0 for m in range(0)))  # placeholder
K = sp.S.Zero
for a_ in range(n):
    for b_ in range(n):
        for c_ in range(n):
            for d_ in range(n):
                if c_ < d_:
                    Rabcd = sp.simplify(sum(g[a_, l]*riemann_up(l, b_, c_, d_) for l in range(n)))
                    if Rabcd != 0:
                        Rupabcd = sp.simplify(sum(ginv[b_, m]*ginv[c_, p]*ginv[d_, q]*ginv[a_, s]*
                                                  sum(g[s, l]*riemann_up(l, m, p, q) for l in range(n))
                                                  for m in range(n) for p in range(n) for q in range(n) for s in range(n)))
                        K += 2*Rabcd*Rupabcd   # factor 2 for c<d antisymmetry
K = sp.simplify(K)
print("Kretschmann K =", sp.simplify(K))
print("K at neck r=0:", sp.simplify(K.subs(r, 0)))
print("R at neck r=0:", sp.simplify(Rs.subs(r, 0)))
print("R as r->oo:", sp.limit(Rs, r, sp.oo))

# asymptotics for alpha=1 (asymptotically unit-f): expand f and compare to RN
fser = sp.series(f.subs(al, 1), r, sp.oo, 4)
print("f(alpha=1) large-r series:", fser)
