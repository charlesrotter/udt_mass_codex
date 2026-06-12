import sympy as sp

r = sp.symbols('r', positive=True)
A = sp.Function('A')(r)
B = sp.Function('B')(r)
c = sp.symbols('c', positive=True)
th = sp.symbols('theta')

# General SSS metric: ds^2 = -A c^2 dt^2 + B dr^2 + r^2 dOmega^2
g = sp.diag(-A*c**2, B, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords = sp.symbols('t r theta phi')

def christoffel(g, ginv, coords):
    n=4
    Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n):
                    s+=ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
                Gamma[a][b][cc]=sp.simplify(s/2)
    return Gamma

G=christoffel(g,ginv,coords)
n=4
# Ricci
Ric=sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        s=0
        for cc in range(n):
            s+=sp.diff(G[cc][a][b],coords[cc])-sp.diff(G[cc][a][cc],coords[b])
            for d in range(n):
                s+=G[cc][cc][d]*G[d][a][b]-G[cc][b][d]*G[d][a][cc]
        Ric[a,b]=sp.simplify(s)
Rs=sp.simplify(sum(ginv[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
# Einstein mixed G^mu_nu
Gmix=sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        Ein=Ric[a,b]-sp.Rational(1,2)*g[a,b]*Rs
        s=sum(ginv[a,d]*(Ric[d,b]-sp.Rational(1,2)*g[d,b]*Rs) for d in range(n))
        Gmix[a,b]=sp.simplify(s)

Gtt=Gmix[0,0]
Grr=Gmix[1,1]
diff=sp.simplify(Gtt-Grr)
print("G^t_t - G^r_r =", diff)

# Claimed: -(AB)'/(r A B^2)
claim = -sp.diff(A*B,r)/(r*A*B**2)
print("claim          =", sp.simplify(claim))
print("difference (should be 0):", sp.simplify(diff-claim))
