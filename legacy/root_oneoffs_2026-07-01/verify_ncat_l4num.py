import sympy as sp, random
r,th=sp.symbols('r theta',real=True)
phi=sp.Symbol('phi',real=True); kap,k=sp.symbols('kappa k',positive=True)
Grs,Gts,Gs=sp.symbols('Gr Gt G',real=True)
mine = k**2*kap*(Grs**2*r**2 + Gts**2*sp.exp(2*phi))*sp.exp(-2*phi)*sp.sin(Gs)**2/(2*r**4*sp.sin(th)**2)
claim = (k**2*kap/2)*sp.sin(Gs)**2*(sp.exp(-2*phi)*Grs**2 + sp.exp(2*phi)*Gts**2/r**2)/r**2
random.seed(1)
for trial in range(5):
    subs={r:random.uniform(0.5,3), th:random.uniform(0.3,2.5), phi:random.uniform(-0.5,0.1),
          kap:1.0,k:2.0,Grs:random.uniform(-1,1),Gts:random.uniform(-1,1),Gs:random.uniform(0.1,3)}
    print(f"mine={float(mine.subs(subs)):.6f}  claim={float(claim.subs(subs)):.6f}")
