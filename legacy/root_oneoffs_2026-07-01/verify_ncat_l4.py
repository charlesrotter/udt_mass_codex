import sympy as sp
r,th=sp.symbols('r theta',real=True)
phi=sp.Symbol('phi',real=True); kap,k=sp.symbols('kappa k',positive=True)
Grs,Gts,Gs=sp.symbols('Gr Gt G',real=True)
# my L4:
mine = k**2*kap*(Grs**2*r**2 + Gts**2*sp.exp(2*phi))*sp.exp(-2*phi)*sp.sin(Gs)**2/(2*r**4*sp.sin(th)**2)
# claim L4:
claim = (k**2*kap/2)*sp.sin(Gs)**2*(sp.exp(-2*phi)*Grs**2 + sp.exp(2*phi)*Gts**2/r**2)/r**2
print("mine  =", sp.simplify(mine))
print("claim =", sp.simplify(claim))
print("ratio mine/claim =", sp.simplify(mine/claim))
