import sympy as sp
r=sp.symbols('r',positive=True); th,ps=sp.symbols('theta psi')
xi,kap=sp.symbols('xi kappa',positive=True)
a=sp.Function('a')(r); b=sp.Function('b')(r); Th=sp.Function('Theta')(r)
coords=[sp.symbols('t'),r,th,ps]
g=sp.diag(-sp.exp(2*a),sp.exp(2*b),r**2,r**2*sp.sin(th)**2)
ginv=g.inv()
sT,cT=sp.sin(Th),sp.cos(Th); sth,cth=sp.sin(th),sp.cos(th)
nA=[cT,sT*sth*sp.cos(ps),sT*sth*sp.sin(ps),sT*cth]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for m in range(4):
 for n in range(4):
  Gmn[m,n]=sum(dmu(nA[A],m)*dmu(nA[A],n) for A in range(4))
L2=-(xi/2)*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
L4=0
for m in range(4):
 for n in range(4):
  for pp in range(4):
   for q in range(4):
    L4+=ginv[m,pp]*ginv[n,q]*(Gmn[m,n]*Gmn[pp,q]-Gmn[m,q]*Gmn[pp,n])
L4=-(kap/4)*L4
L=L2+L4
Cab=sp.zeros(4,4)
for X in range(4):
 for B2 in range(4):
  Cab[X,B2]=sum(ginv[nn,q]*(Gmn[X,B2]*Gmn[nn,q]-Gmn[X,q]*Gmn[nn,B2]) for nn in range(4) for q in range(4))
Cab=(Cab+Cab.T)/2
Tlow=xi*Gmn+kap*Cab+g*L
Tmix=ginv*Tlow
Gam=[[[sum(ginv[al,de]*(dmu(g[de,be],ga)+dmu(g[de,ga],be)-dmu(g[be,ga],de)) for de in range(4))/2 for ga in range(4)] for be in range(4)] for al in range(4)]
nu=1
divT=sum(dmu(Tmix[mu,nu],mu) for mu in range(4))
for mu in range(4):
 for l in range(4):
  divT+=Gam[mu][mu][l]*Tmix[l,nu]-Gam[l][mu][nu]*Tmix[mu,l]
divT=sp.simplify(divT)

# committed EL via exec with sympy backend
src=open('axisym_matter_el.py').read()
src='\n'.join(ln for ln in src.split('\n') if not ln.strip().startswith('import numpy') and not ln.strip().startswith('from numpy'))
ns={'np':sp,'exp':sp.exp,'sin':sp.sin,'cos':sp.cos,'sqrt':sp.sqrt,'tan':sp.tan}
exec(src,ns)
ELfun=ns['matter_el_resid']
Z=sp.Integer(0)
ap,bp,Thp,Thpp,app,bpp=sp.diff(a,r),sp.diff(b,r),sp.diff(Th,r),sp.diff(Th,r,2),sp.diff(a,r,2),sp.diff(b,r,2)
EL_comm=ELfun(r,th, a,b,Z,Z,Th, ap,bp,Z,Z,Thp, Z,Z,Z,Z,Z, app,bpp,Z,Z,Thpp, Z,Z,Z,Z,Z, Z,Z,Z,Z,Z, xi,kap)
EL_comm=sp.simplify(EL_comm)
print("EL_committed (round) =", EL_comm)
ratio=sp.simplify(divT/EL_comm)
print("\n*** div_mu T^mu_r / EL_committed (round) = ***")
print(ratio)
# If ratio is a smooth nonzero function (no Theta'' in it), the EL is the correct
# conservation law (same zero set). If it depends on Thpp etc nontrivially, mismatch.
print("\nfree symbols of ratio:", ratio.free_symbols)
print("\nDoes ratio contain Theta'' ?", Thpp in ratio.free_symbols or sp.diff(Th,r,2) in ratio.atoms(sp.Derivative))

print("\n=== KEY IDENTITY CHECK: divT_r = - EL * Theta_r ? ===")
Thp_=sp.diff(Th,r)
test1=sp.simplify(divT - (-EL_comm*Thp_))
print("divT - (-EL_committed * Theta') =", test1)
test2=sp.simplify(divT - (EL_comm*Thp_))
print("divT - (+EL_committed * Theta') =", test2)
# also my own EL:
import importlib.util
