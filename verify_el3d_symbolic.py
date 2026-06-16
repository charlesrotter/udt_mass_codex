# SYMBOLIC proof that the generated 3-D EL is the TRUE variation, stress-consistent:
# div_mu T^mu_nu = -EL * d_nu Theta  must hold IDENTICALLY (sympy), off-round.
import sympy as sp
t,r,th,ps=sp.symbols('t r theta psi',real=True)
xi,kap=sp.symbols('xi kappa',positive=True)
m=sp.Symbol('m',positive=True)
coords=[t,r,th,ps]
a=sp.Function('a')(r,th,ps); b=sp.Function('b')(r,th,ps)
c=sp.Function('c')(r,th,ps); d=sp.Function('d')(r,th,ps); Th=sp.Function('Theta')(r,th,ps)
glow=[-sp.exp(2*a),sp.exp(2*b),sp.exp(2*c)*r**2,sp.exp(2*d)*r**2*sp.sin(th)**2]
g=sp.diag(*glow); ginv=g.inv()
sT,cT=sp.sin(Th),sp.cos(Th); sth=sp.sin(th)
nA=[sT*sth*sp.cos(m*ps),sT*sth*sp.sin(m*ps),sT*sp.cos(th),cT]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for i in range(4):
 for j in range(4):
  Gmn[i,j]=sum(dmu(nA[A],i)*dmu(nA[A],j) for A in range(4))
L2=-(xi/2)*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
SS2=lambda A,nn,B,q: Gmn[A,B]*Gmn[nn,q]-Gmn[A,q]*Gmn[nn,B]
L4=-(kap/4)*sum(ginv[mm,pp]*ginv[nn,q]*SS2(mm,nn,pp,q) for mm in range(4) for nn in range(4) for pp in range(4) for q in range(4))
L=L2+L4
rootg=sp.exp(a+b+c+d)*r**2*sth
lag=rootg*L
EL=(sp.diff(sp.diff(lag,sp.diff(Th,r)),r)+sp.diff(sp.diff(lag,sp.diff(Th,th)),th)
    +sp.diff(sp.diff(lag,sp.diff(Th,ps)),ps)-sp.diff(lag,Th))/rootg
# Hilbert stress T_{ab} = -2 dL/dg^{ab} + g_{ab} L  -> mixed T^mu_nu
# build via dL/dginv
gi=sp.MatrixSymbol('gi',4,4)
# do directly: dL/dginv^{ab}; L depends on ginv through L2,L4. Use component diff.
giM=sp.Matrix(4,4,lambda i,j: ginv[i,j])
Tlow=sp.zeros(4,4)
for A in range(4):
 for B in range(4):
  dL=sp.diff(L2.subs(),) if False else None
# easier: T_{ab} = xi Gmn_ab + kap C_ab + g_ab L, C_ab = ginv^{nq} SS2(a,n,b,q)
C=sp.zeros(4,4)
for A in range(4):
 for B in range(4):
  C[A,B]=sum(ginv[n,q]*SS2(A,n,B,q) for n in range(4) for q in range(4))
C=(C+C.T)/2
Tlow=xi*Gmn+kap*C+g*L
Tmix=ginv*Tlow   # T^mu_nu = g^{mu a} T_{a nu}
# covariant divergence of mixed tensor (one test nu = r, the load-bearing one)
# Christoffel
Gam=[[[sp.S(0)]*4 for _ in range(4)] for _ in range(4)]
for l in range(4):
 for mu in range(4):
  for nu in range(4):
   Gam[l][mu][nu]=sp.Rational(1,2)*sum(ginv[l,k]*(sp.diff(g[k,mu],coords[nu])+sp.diff(g[k,nu],coords[mu])-sp.diff(g[mu,nu],coords[k])) for k in range(4))
def divT(nu):
    s=sp.S(0)
    for mu in range(4):
        s+=sp.diff(Tmix[mu,nu],coords[mu])
        for l in range(4):
            s+=Gam[mu][mu][l]*Tmix[l,nu]-Gam[l][mu][nu]*Tmix[mu,l]
    return s
import time
for nu,nm in [(1,'r'),(2,'th'),(3,'ps')]:
    t0=time.time()
    lhs=divT(nu)
    rhs=-EL*sp.diff(Th,coords[nu])
    diff=sp.simplify(lhs-rhs)
    print(f"nu={nm}: div_mu T^mu_nu - (-EL d_nu Th) = {diff}   ({time.time()-t0:.0f}s)")
