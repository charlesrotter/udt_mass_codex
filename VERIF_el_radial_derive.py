import sympy as sp
# Derive the radial EL from scratch in the round limit and compare to the
# audited radial theta_ddot_freed (claimed verified via div T=0).
r=sp.symbols('r',positive=True)
xi,kap=sp.symbols('xi kappa',positive=True)
th,ps=sp.symbols('theta psi',real=True)
a=sp.Function('a')(r); b=sp.Function('b')(r); Th=sp.Function('Theta')(r)
# round metric c=d=0
g=sp.diag(-sp.exp(2*a),sp.exp(2*b),r**2,r**2*sp.sin(th)**2)
ginv=g.inv()
sT,cT=sp.sin(Th),sp.cos(Th); sth,cth=sp.sin(th),sp.cos(th)
nA=[cT, sT*sth*sp.cos(ps), sT*sth*sp.sin(ps), sT*cth]
coords=[sp.symbols('t'),r,th,ps]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        Gmn[mu,nu]=sum(dmu(nA[A],mu)*dmu(nA[A],nu) for A in range(4))
L2=-(xi/2)*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
L4=0
for mu in range(4):
 for nu in range(4):
  for pp in range(4):
   for q in range(4):
    L4+=ginv[mu,pp]*ginv[nu,q]*(Gmn[mu,nu]*Gmn[pp,q]-Gmn[mu,q]*Gmn[pp,nu])
L4=-(kap/4)*L4
L=sp.simplify(L2+L4)
rootg=sp.exp(a)*sp.exp(b)*r**2*sth
lag=rootg*L
ThR=sp.diff(Th,r)
EL=sp.diff(sp.diff(lag,ThR),r)-sp.diff(lag,Th)
ELn=sp.simplify(EL/rootg)
# Now solve EL=0 for Theta'' and compare to audited rhs
Thpp=sp.Symbol('Thpp'); Thp=sp.Symbol('Thp'); ThS=sp.Symbol('ThS')
ap=sp.Symbol('ap'); bp=sp.Symbol('bp')
subs={sp.diff(Th,r,2):Thpp, sp.diff(Th,r):Thp, Th:ThS,
      sp.diff(a,r):ap, sp.diff(b,r):bp}
ELs=ELn.subs(subs)
# the round EL should be of the form K*(Thpp - rhs); solve
sol=sp.solve(ELs,Thpp)
rhs_mine=sp.simplify(sol[0])
# audited:
s=sp.sin(ThS); e2b=sp.exp(2*b)
# careful: substitute exp(2*b) symbol
B=sp.Symbol('B'); 
num=(-2*kap*r**2*s**2*Thp*ap + 2*kap*r**2*s**2*Thp*bp
     - kap*r**2*sp.sin(2*ThS)*Thp**2 + 2*kap*B*s**3*sp.cos(ThS)
     - r**4*xi*Thp*ap + r**4*xi*Thp*bp - 2*r**3*xi*Thp
     + r**2*xi*B*sp.sin(2*ThS))
den=r**2*(2*kap*s**2 + r**2*xi)
rhs_audit=num/den
rhs_mine_B=rhs_mine.subs(sp.exp(2*b),B)
diff=sp.simplify(rhs_mine_B - rhs_audit)
print("rhs_mine - rhs_audit (should be 0 if same EL):")
print(diff)
print("\nsimplified again:", sp.simplify(sp.expand_trig(diff)))
