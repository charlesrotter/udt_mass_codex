import sympy as sp
t,r,th,ps = sp.symbols('t r theta psi', real=True)
c   = sp.symbols('c', positive=True)
eps = sp.symbols('epsilon')                 # linearization bookkeeping in j
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
j   = sp.Function('j')(r)
coords=[t,r,th,ps]

# metric with small off-diagonal g_tpsi = eps*j(r)*sin^2 th
gtpsi = eps*j*sp.sin(th)**2
g = sp.Matrix([
 [-sp.exp(-2*phi)*c**2, 0, 0, gtpsi],
 [0, sp.exp(2*phi), 0, 0],
 [0, 0, rho**2, 0],
 [gtpsi, 0, 0, rho**2*sp.sin(th)**2]])
gi = g.inv()

# Christoffel, Ricci
def christ(gi,g):
    G=[[[0]*4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
     for b in range(4):
      for cc in range(4):
        s=0
        for d in range(4):
          s+= gi[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
        G[a][b][cc]=sp.Rational(1,2)*s
    return G
G=christ(gi,g)
def Ric(G):
    R=sp.zeros(4,4)
    for b in range(4):
     for d in range(4):
       s=0
       for a in range(4):
         s+=sp.diff(G[a][b][d],coords[a])-sp.diff(G[a][b][a],coords[d])
         for e in range(4):
           s+=G[a][a][e]*G[e][b][d]-G[a][d][e]*G[e][b][a]
       R[b,d]=s
    return R
Ric=Ric(G)
Rsc=sp.simplify(sum(gi[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
# Einstein tensor lower t-psi, linear in eps
Gtps = Ric[0,3]-sp.Rational(1,2)*g[0,3]*Rsc
Gtps_lin = sp.series(sp.simplify(Gtps), eps, 0, 2).removeO()
Gtps_lin = sp.simplify(sp.diff(Gtps_lin,eps)*1)  # coefficient of eps^1 (linear part; eps^0 is 0)
print("G_{t psi} (coeff of eps, i.e. linear-in-j native operator):")
print(sp.simplify(Gtps_lin))
