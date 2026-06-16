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
# MY EL (variation of int sqrt(g) L): round limit, divide by rootg
rootg=sp.exp(a)*sp.exp(b)*r**2*sth
lag=rootg*L
ThR=sp.diff(Th,r)
EL_mine=(sp.diff(sp.diff(lag,ThR),r)-sp.diff(lag,Th))/rootg
Thp=sp.diff(Th,r)
print("MY EL identity: divT_r - (-EL_mine*Theta') =")
print(sp.simplify(divT + EL_mine*Thp))
