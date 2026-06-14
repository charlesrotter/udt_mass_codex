"""
UDT source analysis.
Result: the metric g_tt*g_rr = -c^2 forces G^t_t = G^r_r identically,
i.e. p_r = -rho. A canonical radial scalar cannot source this; the matter
must be of global-monopole / radial-gauge (topological, angular) type.
Vacuum limit (rho=0) -> Schwarzschild. Run requires sympy, numpy, scipy.
"""
import sympy as sp, numpy as np

# ---- symbolic: prove G^t_t = G^r_r and read off rho, p_r, p_th ----
t,r,th = sp.symbols('t r theta', real=True); f=sp.Function('phi')
phi=f(r); A=sp.exp(-2*phi); B=sp.exp(2*phi)
g=sp.diag(-A,B,r**2,r**2*sp.sin(th)**2); gi=g.inv(); co=[t,r,th,sp.Symbol('p')]
Ga=[[[sp.simplify(sum(gi[a,d]*(sp.diff(g[d,b],co[c])+sp.diff(g[d,c],co[b])
     -sp.diff(g[b,c],co[d])) for d in range(4))/2) for c in range(4)]
     for b in range(4)] for a in range(4)]
Ric=sp.zeros(4)
for b in range(4):
  for d in range(4):
    s=0
    for a in range(4):
      s+=sp.diff(Ga[a][b][d],co[a])-sp.diff(Ga[a][b][a],co[d])
      for e in range(4): s+=Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
    Ric[b,d]=sp.simplify(s)
Rs=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
Gm=sp.simplify(gi*(Ric-sp.Rational(1,2)*g*Rs))
print("G^t_t - G^r_r =", sp.simplify(Gm[0,0]-Gm[1,1]), " (=> p_r = -rho)")
print("rho   = -G^t_t   =", sp.simplify(-Gm[0,0]))
print("p_th  =  G^th_th =", sp.simplify(Gm[2,2]))
print("vacuum (rho=0):  2 r phi' + e^{2phi} - 1 = 0  ->  e^{-2phi}=1-rs/r (Schwarzschild)")

# ---- numeric: cavity + discrete bound-mode mechanism (illustrative) ----
a,s=1.2,1.0
phin =lambda x:-a*np.exp(-x**2/(2*s**2))
phipp=lambda x: a/s**2*(1-x**2/s**2)*np.exp(-x**2/(2*s**2))
from scipy.linalg import eigh_tridiagonal
def tower(l=0,m2=0.2,rmax=14,N=4000):
    x=np.linspace(1e-4,rmax,N);dr=x[1]-x[0]
    U=np.exp(2*phin(x))*(m2+l*(l+1)/x**2)+phipp(x)
    w2,_=eigh_tridiagonal(2/dr**2+U,-1/dr**2*np.ones(N-1))
    return np.array([v for v in w2 if v<(m2 if m2>0 else 0)-1e-9])
print("\nIllustrative cavity bound tower (l=0, m^2=0.2):", np.round(tower(),4))
print("NOTE: shallow toy well -> few levels. Real ladder needs the N=3 hedgehog")
print("profile solved in the UDT background (regular core -> vacuum, shooting).")
