import sympy as sp
r, th, c = sp.symbols('r theta c', positive=True)
P = sp.Function('phi')(r)
# UDT metric
A = sp.exp(-2*P); B = sp.exp(2*P)
g = sp.diag(-A*c**2, B, r**2, r**2*sp.sin(th)**2); gi=g.inv()
coords=[sp.symbols('t'),r,th,sp.symbols('ph')]; n=4
def chris(g,gi,co):
    G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=sum(gi[a,d]*(sp.diff(g[d,b],co[cc])+sp.diff(g[d,cc],co[b])-sp.diff(g[b,cc],co[d])) for d in range(n))
                G[a][b][cc]=sp.simplify(s/2)
    return G
Gm=chris(g,gi,coords)
Ric=sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        s=0
        for cc in range(n):
            s+=sp.diff(Gm[cc][a][b],coords[cc])-sp.diff(Gm[cc][a][cc],coords[b])
            for d in range(n):
                s+=Gm[cc][cc][d]*Gm[d][a][b]-Gm[cc][b][d]*Gm[d][a][cc]
        Ric[a,b]=sp.simplify(s)
Rs=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
Gmix=sp.simplify(gi*(Ric-sp.Rational(1,2)*g*Rs))
Gthth=sp.simplify(Gmix[2,2])
print("Metric-phi vacuum eqn G^theta_theta=0 :", Gthth, "= 0")
print(" -> NO mu^2 appears. (pure geometry; Schwarzschild branch)")
# vs the matter field eqn (Box_g - mu^2)phi=0 carries mu^2 explicitly.
