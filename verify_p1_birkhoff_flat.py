import sympy as sp

t, r, th = sp.symbols('t r theta', real=True)
phi = sp.Function('phi')  # phi(t,r)
c = sp.symbols('c', positive=True)

# Held UDT round diagonal metric with time-dependent dilation
# ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
P = phi(t, r)
g = sp.diag(-sp.exp(-2*P)*c**2, sp.exp(2*P), r**2, r**2*sp.sin(th)**2)
coords = [t, r, th, sp.symbols('psi')]
ginv = g.inv()

def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(n):
                s = 0
                for e in range(n):
                    s += ginv[a,e]*(sp.diff(g[e,b],coords[d])+sp.diff(g[e,d],coords[b])-sp.diff(g[b,d],coords[e]))
                Gamma[a][b][d] = sp.simplify(s/2)
    return Gamma

G = christoffel(g, ginv, coords)
n=4
def ricci(G, coords):
    n=len(coords)
    R = sp.zeros(n,n)
    for b in range(n):
        for d in range(n):
            s=0
            for a in range(n):
                s += sp.diff(G[a][b][d], coords[a]) - sp.diff(G[a][b][a], coords[d])
                for e in range(n):
                    s += G[a][a][e]*G[e][b][d] - G[a][d][e]*G[e][b][a]
            R[b,d]=sp.simplify(s)
    return R

Ric = ricci(G, coords)
Rs = sp.simplify(sum(ginv[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
Gmunu = sp.zeros(n,n)
for i in range(n):
    for j in range(n):
        Gmunu[i,j]=sp.simplify(Ric[i,j]-sp.Rational(1,2)*g[i,j]*Rs)

Gtr = sp.simplify(Gmunu[0,1])
print("G_{t r} (lowered) =", Gtr)
print("G_{t r} / d_t phi =", sp.simplify(Gtr/sp.diff(P,t)))

# Now the static case: phi=phi(r). G_tt component => the radial structure eq.
phir = sp.Function('phi')(r)
gs = sp.diag(-sp.exp(-2*phir)*c**2, sp.exp(2*phir), r**2, r**2*sp.sin(th)**2)
ginvs = gs.inv()
Gs = christoffel(gs, ginvs, coords)
Rics = ricci(Gs, coords)
Rss = sp.simplify(sum(ginvs[i,j]*Rics[i,j] for i in range(n) for j in range(n)))
Gs_munu = sp.zeros(n,n)
for i in range(n):
    for j in range(n):
        Gs_munu[i,j]=sp.simplify(Rics[i,j]-sp.Rational(1,2)*gs[i,j]*Rss)
# vacuum: G^t_t = 0 etc. Use mixed
Gtt_mixed = sp.simplify(sum(ginvs[0,k]*Gs_munu[k,0] for k in range(n)))
print("static G^t_t =", Gtt_mixed)
# Schwarzschild-like equation
