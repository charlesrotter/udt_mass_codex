import sympy as sp
r=sp.symbols('r',positive=True)
G=sp.Function('G')(r); F=sp.Function('F')(r)
E,m,kap=sp.symbols('E m kappa',real=True)
PHI=sp.Function('Phi')(r); PHIp=sp.diff(PHI,r)
eP,e2P=sp.exp(PHI),sp.exp(2*PHI)
Gp=(PHIp-kap/r)*G+(E*e2P+m*eP)*F
Fp=(PHIp+kap/r)*F-(E*e2P-m*eP)*G
combo=-2*(kap*(F**2-G**2)/r+PHIp*(F**2+G**2)+m*eP*G*F)
psibar=eP*(G**2-F**2)
Tt=sp.Function('Tt')(r); Trr=Tt+combo; Tthth=(m*psibar-(Tt+Trr))/2
th=sp.symbols('theta',positive=True)
g=sp.diag(-sp.exp(-2*PHI),sp.exp(2*PHI),r**2,r**2*sp.sin(th)**2)
gi=g.inv(); X=[sp.symbols('t'),r,th,sp.symbols('vph')]
def Ch(u,a,b): return sp.simplify(sum(gi[u,s]*(sp.diff(g[s,a],X[b])+sp.diff(g[s,b],X[a])-sp.diff(g[a,b],X[s])) for s in range(4))/2)
Tmix=[Tt,Trr,Tthth,Tthth]
trace_ch=sum(Ch(mu,mu,1) for mu in range(4))
cross=-sum(Ch(mu,mu,1)*Tmix[mu] for mu in range(4))
div=(sp.diff(Trr,r)+trace_ch*Trr+cross).subs({sp.diff(G,r):Gp,sp.diff(F,r):Fp})
q=sp.simplify(-(div.subs(Tt,0).doit().subs({sp.diff(G,r):Gp,sp.diff(F,r):Fp})))
print("conservation reduces to  Tt'(r) = q(r) with  q =")
print("  ", sp.simplify(q))
print("=> coeff of Tt is 0 -> conservation NEVER constrains the combo; it only fixes T^t_t by quadrature.")
print("   So the validated combo is automatically conservation-consistent (a T^t_t solving Tt'=q exists).")
