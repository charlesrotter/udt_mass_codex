"""AXIS 3: is the T-dependence a coordinate/gauge artifact?
Compute a coordinate invariant (Ricci scalar) of the dilation-tie 4-metric
with phi=phi(T,r) and check it carries genuine phi_T dependence.
If R depends on phi_T (not removable by T-reparam), the wave is physical.
Agent ns-verify 2026-06-13."""
import sympy as sp
T,r,th,ph = sp.symbols('T r theta phi_c', real=True)
phi = sp.Function('phi')(T,r)   # spherical, time-dependent
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords=[T,r,th,ph]
n=4
# Christoffels
Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for cc in range(n):
            s=0
            for d in range(n):
                s+=ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
            Gamma[a][b][cc]=sp.simplify(s/2)
# Ricci
Ric=[[0]*n for _ in range(n)]
for b in range(n):
    for d in range(n):
        s=0
        for a in range(n):
            s+=sp.diff(Gamma[a][b][d],coords[a])-sp.diff(Gamma[a][b][a],coords[d])
            for e in range(n):
                s+=Gamma[a][a][e]*Gamma[e][b][d]-Gamma[a][d][e]*Gamma[e][b][a]
        Ric[b][d]=sp.simplify(s)
Rscalar=0
for a in range(n):
    for b in range(n):
        Rscalar+=ginv[a,b]*Ric[a][b]
Rscalar=sp.simplify(Rscalar)
print("Ricci scalar R =", Rscalar)
phiTT=sp.Derivative(phi,T,2); phiT=sp.Derivative(phi,T)
print("\nR contains phi_TT?:", Rscalar.has(phiTT))
print("R contains phi_T (first)?:", Rscalar.has(phiT))
print("=> if YES, T-dependence is PHYSICAL curvature, not gauge.")
