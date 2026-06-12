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
# Guess the correct Ttt has an extra e^{2PHI} measure issue. Try the FRAME density without the e^{2PHI}:
# physical: coordinate T^t_t = -rho_coord. Let's parametrize Ttt = -E*(G^2+F^2)*e^{a*PHI} and also try
# forms with GF. Instead: SOLVE the ODE.
Tt=sp.Function('Tt')(r)
Trr=Tt+combo
Tthth=(m*psibar-(Tt+Trr))/2
th=sp.symbols('theta',positive=True)
g=sp.diag(-sp.exp(-2*PHI),sp.exp(2*PHI),r**2,r**2*sp.sin(th)**2)
gi=g.inv(); X=[sp.symbols('t'),r,th,sp.symbols('vph')]
def Ch(u,a,b):
    return sp.simplify(sum(gi[u,s]*(sp.diff(g[s,a],X[b])+sp.diff(g[s,b],X[a])-sp.diff(g[a,b],X[s])) for s in range(4))/2)
Tmix=[Tt,Trr,Tthth,Tthth]
trace_ch=sum(Ch(mu,mu,1) for mu in range(4))
cross=-sum(Ch(mu,mu,1)*Tmix[mu] for mu in range(4))
div=sp.diff(Trr,r)+trace_ch*Trr+cross
div=div.subs({sp.diff(G,r):Gp,sp.diff(F,r):Fp})
# This is Tt' + p(r) Tt = q(r). Extract:
div=sp.expand(div)
dTt=sp.diff(Tt,r)
# collect coefficient of Tt' (should be 1) and Tt
coeff_dTt=div.coeff(dTt)
rem=sp.simplify(div-coeff_dTt*dTt)
coeff_Tt=rem.coeff(Tt)
q=-sp.simplify(rem.subs(Tt,0))   # div = dTt + coeff_Tt*Tt - q =0 -> Tt'+coeff_Tt*Tt=q
print("coeff dTt:",sp.simplify(coeff_dTt)," coeff Tt:",sp.simplify(coeff_Tt))
# Try ansatz Tt = -E e2P (G^2+F^2) + correction*GF term. Test family:
a,b,c=sp.symbols('a b c')
ans = a*E*e2P*(G**2+F**2)+b*m*eP*G*F+c*PHIp # generic
# Instead just numerically check whether SOME standard form works: the Dirac coordinate energy density
# for THIS metric. Known: T^t_t = -(E) * (psi^dag psi)_coord. psi^dag psi with measure e^{-PHI}? 
# Try Ttt=-E*eP*(G^2+F^2):
for lbl,test in [("-E e2P(G^2+F^2)",-E*e2P*(G**2+F**2)),
                 ("-E eP(G^2+F^2)",-E*eP*(G**2+F**2)),
                 ("-E (G^2+F^2)",-E*(G**2+F**2)),
                 ("-E e3P(G^2+F^2)",-E*sp.exp(3*PHI)*(G**2+F**2))]:
    res=sp.simplify(div.subs(Tt,test).doit().subs({sp.diff(G,r):Gp,sp.diff(F,r):Fp}))
    print(f"  Ttt={lbl}: cons residual zero? {res==0}")
