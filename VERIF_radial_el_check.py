import sympy as sp
# Is the audited radial EL (theta_ddot_freed / radial_Bfree_soliton) the CORRECT one?
# Compare its implied (Thpp - rhs) to my correct EL (round), via the identity.
r=sp.symbols('r',positive=True); th,ps=sp.symbols('theta psi')
xi,kap=sp.symbols('xi kappa',positive=True)
a=sp.Function('a')(r); b=sp.Function('b')(r); Th=sp.Function('Theta')(r)
coords=[sp.symbols('t'),r,th,ps]
glow=[-sp.exp(2*a),sp.exp(2*b),r**2,r**2*sp.sin(th)**2]
g=sp.diag(*glow); ginv=g.inv()
sT,cT=sp.sin(Th),sp.cos(Th); sth=sp.sin(th)
nA=[cT,sT*sth*sp.cos(ps),sT*sth*sp.sin(ps),sT*sp.cos(th)]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for m in range(4):
 for n in range(4):
  Gmn[m,n]=sum(dmu(nA[A],m)*dmu(nA[A],n) for A in range(4))
L2=-(xi/2)*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
SS2=lambda A,nn,B,q: Gmn[A,B]*Gmn[nn,q]-Gmn[A,q]*Gmn[nn,B]
L4=-(kap/4)*sum(ginv[m,pp]*ginv[n,q]*SS2(m,n,pp,q) for m in range(4) for n in range(4) for pp in range(4) for q in range(4))
L=L2+L4
rootg=sp.exp(a)*sp.exp(b)*r**2*sth
lag=rootg*L
EL_mine=sp.simplify((sp.diff(sp.diff(lag,sp.diff(Th,r)),r)-sp.diff(lag,Th))/rootg)
# my EL solved for Thpp:
Thpp=sp.Symbol('Thpp');Thp=sp.Symbol('Thp');ThS=sp.Symbol('ThS');ap=sp.Symbol('ap');bp=sp.Symbol('bp');B=sp.Symbol('B')
sub={sp.diff(Th,r,2):Thpp,sp.diff(Th,r):Thp,Th:ThS,sp.diff(a,r):ap,sp.diff(b,r):bp,sp.exp(2*b):B}
ELs=EL_mine.subs(sub)
rhs_mine=sp.simplify(sp.solve(ELs,Thpp)[0])
# audited radial rhs:
s=sp.sin(ThS)
num=(-2*kap*r**2*s**2*Thp*ap+2*kap*r**2*s**2*Thp*bp-kap*r**2*sp.sin(2*ThS)*Thp**2
     +2*kap*B*s**3*sp.cos(ThS)-r**4*xi*Thp*ap+r**4*xi*Thp*bp-2*r**3*xi*Thp+r**2*xi*B*sp.sin(2*ThS))
den=r**2*(2*kap*s**2+r**2*xi)
rhs_audit=num/den
print("CORRECT rhs (mine) - audited radial rhs =")
print(sp.simplify(rhs_mine-rhs_audit))
