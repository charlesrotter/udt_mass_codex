import sympy as sp
r=sp.symbols('r',positive=True)
G=sp.Function('G')(r); F=sp.Function('F')(r)
E,m,kap=sp.symbols('E m kappa',real=True)
PHI=sp.Function('Phi')(r); PHIp=sp.diff(PHI,r)
eP,e2P=sp.exp(PHI),sp.exp(2*PHI)
# on-shell
Gp=(PHIp-kap/r)*G+(E*e2P+m*eP)*F
Fp=(PHIp+kap/r)*F-(E*e2P-m*eP)*G
# validated combo and trace
combo=-2*(kap*(F**2-G**2)/r+PHIp*(F**2+G**2)+m*eP*G*F)  # T^r_r - T^t_t
psibar=eP*(G**2-F**2)
# unknown Ttt(r); Trr=Ttt+combo; Tthth=(m psibar - Ttt-Trr)/2
Tt=sp.Function('Tt')(r)
Trr=Tt+combo
Tthth=(m*psibar-(Tt+Trr))/2
# full metric WITH sin^2 via theta, but radial divergence only needs the trace of christoffel and angular pieces.
th=sp.symbols('theta',positive=True)
g=sp.diag(-sp.exp(-2*PHI),sp.exp(2*PHI),r**2,r**2*sp.sin(th)**2)
gi=g.inv(); X=[sp.symbols('t'),r,th,sp.symbols('vph')]
def Ch(u,a,b):
    return sp.simplify(sum(gi[u,s]*(sp.diff(g[s,a],X[b])+sp.diff(g[s,b],X[a])-sp.diff(g[a,b],X[s])) for s in range(4))/2)
Tmix=[Tt,Trr,Tthth,Tthth]
# nabla_mu T^mu_r = d_r T^r_r + Gamma^mu_{mu r} T^r_r - Gamma^la_{mu r} T^mu_la
trace_ch=sum(Ch(mu,mu,1) for mu in range(4))
# - sum_{mu,la} Gamma^la_{mu r} T^mu_la ; T diagonal so la=mu
cross=-sum(Ch(mu,mu,1)*Tmix[mu] for mu in range(4))   # only diagonal Gamma^mu_{mu r} hits diagonal T
div=sp.diff(Trr,r)+trace_ch*Trr+cross
div=sp.simplify(div)
# solve ODE div=0 for Tt? first substitute on-shell G',F'
div=div.subs({sp.diff(G,r):Gp,sp.diff(F,r):Fp})
div=sp.simplify(div)
print("div as eqn in Tt, Tt':")
print(div)
# try Tt = -E e2P (G^2+F^2)
test=-E*e2P*(G**2+F**2)
res=div.subs(Tt,test).doit()
res=res.subs({sp.diff(G,r):Gp,sp.diff(F,r):Fp})
print("\nresidual with Tt=-E e2P(G^2+F^2):", sp.simplify(res))
