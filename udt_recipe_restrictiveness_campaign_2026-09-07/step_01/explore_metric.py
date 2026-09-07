"""Exploration only: exact Ricci for a declared metric variation; no recipe claim."""
import json
import sympy as s

u,v,x,y=s.symbols('u v x y', real=True)
eps,kappa,d=s.symbols('epsilon kappa d', real=True)
coords=(u,v,x,y)
H=x**3-3*x*y**2+kappa*eps*v*y+d*eps**2*x**4
g=s.Matrix([[H,-1,0,eps*x**2],[-1,0,0,0],[0,0,1,0],[eps*x**2,0,0,1]])
gi=g.inv()
G=[[[s.expand(sum(gi[a,h]*(s.diff(g[h,c],coords[b])+s.diff(g[h,b],coords[c])-s.diff(g[b,c],coords[h])) for h in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
Ric=s.Matrix(4,4,lambda b,c:s.simplify(sum(s.diff(G[a][b][c],coords[a])-s.diff(G[a][a][c],coords[b])+sum(G[a][a][m]*G[m][b][c]-G[a][b][m]*G[m][a][c] for m in range(4)) for a in range(4))))
print(json.dumps({'sympy':s.__version__,'metric':str(g),'det':str(g.det()),'ricci_nonzero':{str((a,b)):str(Ric[a,b]) for a in range(4) for b in range(4) if Ric[a,b]!=0},'first_variation':str(Ric.diff(eps).subs(eps,0))},indent=2))
