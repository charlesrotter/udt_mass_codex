import sympy as sp

r, t, th, ph, c, mu = sp.symbols('r t theta phi_a c mu', positive=True)
A = sp.Function('A')(r)
B = sp.Function('B')(r)

# General SSS metric: ds^2 = -A c^2 dt^2 + B dr^2 + r^2 dOmega^2
g = sp.diag(-A*c**2, B, r**2, r**2*sp.sin(th)**2)
gi = g.inv()
coords = [t, r, th, ph]
n = 4

# Christoffel
def christoffel(g, gi, coords):
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += gi[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
                Gamma[a][b][cc] = sp.simplify(s/2)
    return Gamma
Gamma = christoffel(g, gi, coords)

# Ricci
def ricci(Gamma, coords):
    R = sp.zeros(n,n)
    for a in range(n):
        for b in range(n):
            s = 0
            for cc in range(n):
                s += sp.diff(Gamma[cc][a][b], coords[cc]) - sp.diff(Gamma[cc][a][cc], coords[b])
                for d in range(n):
                    s += Gamma[cc][cc][d]*Gamma[d][a][b] - Gamma[cc][b][d]*Gamma[d][a][cc]
            R[a,b] = sp.simplify(s)
    return R
Ric = ricci(Gamma, coords)
Rs = sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))

# Einstein tensor mixed G^a_b
G_low = Ric - sp.Rational(1,2)*g*Rs
G_mixed = sp.simplify(gi*G_low)

Gtt = sp.simplify(G_mixed[0,0])
Grr = sp.simplify(G_mixed[1,1])
diff = sp.simplify(Gtt - Grr)
print("G^t_t - G^r_r =", diff)

# Claimed identity: -(AB)'/(r A B^2)
claim = sp.simplify(-sp.diff(A*B, r)/(r*A*B**2))
print("claimed -(AB)'/(rAB^2) =", claim)
print("MATCH (a):", sp.simplify(diff - claim)==0)
