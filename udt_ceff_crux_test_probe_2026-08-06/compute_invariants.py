"""Static invariant reduction: show a_mu = grad(ln V) with V = Killing-norm (a g-scalar),
and R_{mu nu} u^mu u^nu is a pure-metric invariant. float-free sympy. SCOPED: this metric class.
"""
import sympy as sp

x, c = sp.symbols('x c', real=True, positive=True)
phi = sp.Function('phi')(x)
coords = None

# 2D core (t,x) suffices for the static reduction argument; transverse block only rescales.
t = sp.symbols('t', real=True)
coords = [t, x]
n = 2
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi))
ginv = g.inv()

# Killing vector xi = d_t ; its norm-squared V2 = -g(xi,xi) = -g_tt  (a scalar: norm of a
# metric-singled-out vector field).  V = e^{-phi} c.
V2 = -g[0,0]
V = sp.sqrt(V2)
lnV = sp.simplify(sp.log(V))
grad_lnV_low = [sp.simplify(sp.diff(lnV, coords[i])) for i in range(n)]
print("V^2 = -g_tt =", sp.simplify(V2))
print("ln V =", lnV)
print("grad_mu ln V =", grad_lnV_low)   # expect (0, -phi')  == a_mu

# Christoffels (2D)
def christoffel(g, ginv, coords):
    n=len(coords); Gam=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=sum(ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])
                      -sp.diff(g[b,cc],coords[d])) for d in range(n))
                Gam[a][b][cc]=sp.simplify(s/2)
    return Gam
Gam=christoffel(g,ginv,coords)

# u
norm=sp.sqrt(-g[0,0]); uup=[1/norm,0]; udn=[sp.simplify(sum(g[a,b]*uup[b] for b in range(n))) for a in range(n)]

# acceleration again (2D) to confirm a_mu = grad_mu ln V
nab=[[sp.simplify(sp.diff(udn[mu],coords[nu])-sum(Gam[l][nu][mu]*udn[l] for l in range(n)))
      for nu in range(n)] for mu in range(n)]
a_low=[sp.simplify(sum(uup[nu]*nab[mu][nu] for nu in range(n))) for mu in range(n)]
print("a_mu =", a_low)
print("a_mu - grad ln V =", [sp.simplify(a_low[i]-grad_lnV_low[i]) for i in range(n)])

# Ricci tensor
def riemann(Gam,coords):
    n=len(coords)
    R=[[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    term=sp.diff(Gam[a][d][b],coords[cc])-sp.diff(Gam[a][cc][b],coords[d])
                    term+=sum(Gam[a][cc][e]*Gam[e][d][b]-Gam[a][d][e]*Gam[e][cc][b] for e in range(n))
                    R[a][b][cc][d]=sp.simplify(term)
    return R
Rie=riemann(Gam,coords)
Ric=[[sp.simplify(sum(Rie[a][b][a][d] for a in range(n))) for d in range(n)] for b in range(n)]
Rscalar=sp.simplify(sum(ginv[b,d]*Ric[b][d] for b in range(n) for d in range(n)))
Ruu=sp.simplify(sum(Ric[mu][nu]*uup[mu]*uup[nu] for mu in range(n) for nu in range(n)))
print("Ricci scalar R =", Rscalar)
print("R_{mu nu} u^mu u^nu =", Ruu)

# a^2
a_up=[sp.simplify(sum(ginv[i,j]*a_low[j] for j in range(n))) for i in range(n)]
a2=sp.simplify(sum(a_up[i]*a_low[i] for i in range(n)))
print("a^mu a_mu =", a2)

# box(ln V) = g^{mu nu} nabla_mu nabla_nu lnV -- to show a-divergence is g-scalar
# and demonstrate a2 = |grad lnV|^2 (a pure metric scalar of the Killing-norm field)
grad2=sp.simplify(sum(ginv[i,j]*grad_lnV_low[i]*grad_lnV_low[j] for i in range(n) for j in range(n)))
print("|grad ln V|^2 =", grad2, " ; equals a^2 ->", sp.simplify(grad2-a2)==0)
