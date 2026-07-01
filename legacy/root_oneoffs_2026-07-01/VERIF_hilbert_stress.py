import sympy as sp
# Compute the TRUE Hilbert stress T_munu = -2/sqrt(g) d(sqrt(g)L)/dg^{munu} + ... 
# Actually T_munu = -2 dL/dg^{munu} + g_munu L  (L scalar, no metric-deriv coupling).
# Build L as a function of the INVERSE metric components treated as independent,
# then differentiate. Round limit. Check divT = -EL_mine * Theta'.
r=sp.symbols('r',positive=True); th,ps=sp.symbols('theta psi')
xi,kap=sp.symbols('xi kappa',positive=True)
a=sp.Function('a')(r); b=sp.Function('b')(r); Th=sp.Function('Theta')(r)
coords=[sp.symbols('t'),r,th,ps]
# treat ginv components as independent symbols gtt,grr,gthth,gpsps for differentiation
gI=sp.symbols('gItt gIrr gIth gIps')
sT,cT=sp.sin(Th),sp.cos(Th); sth,cth=sp.sin(th),sp.cos(th)
nA=[cT,sT*sth*sp.cos(ps),sT*sth*sp.sin(ps),sT*cth]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for m in range(4):
 for n in range(4):
  Gmn[m,n]=sum(dmu(nA[A],m)*dmu(nA[A],n) for A in range(4))
ginvS=sp.diag(*gI)  # diagonal inverse metric as independent symbols
L2=-(xi/2)*sum(ginvS[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
L4=0
for m in range(4):
 for n in range(4):
  for pp in range(4):
   for q in range(4):
    L4+=ginvS[m,pp]*ginvS[n,q]*(Gmn[m,n]*Gmn[pp,q]-Gmn[m,q]*Gmn[pp,n])
L4=-(kap/4)*L4
L=L2+L4
# T_{munu} = -2 dL/dg^{munu} + g_{munu} L  (diagonal). g_munu = 1/ginv.
gvals={gI[0]:-sp.exp(-2*a),gI[1]:sp.exp(-2*b),gI[2]:1/r**2,gI[3]:1/(r**2*sth**2)}
glow=[-sp.exp(2*a),sp.exp(2*b),r**2,r**2*sth**2]
Tlow=sp.zeros(4,4)
for i in range(4):
    Tlow[i,i]=(-2*sp.diff(L,gI[i])+glow[i]*L)
Tlow=Tlow.subs(gvals)
Lv=L.subs(gvals)
# mixed T^mu_nu = g^{mu mu} T_{mu nu}
ginvN=sp.diag(*[gvals[gI[i]] for i in range(4)])
Tmix=ginvN*Tlow
g=sp.diag(*glow)
Gam=[[[sum(ginvN[al,de]*(dmu(g[de,be],ga)+dmu(g[de,ga],be)-dmu(g[be,ga],de)) for de in range(4))/2 for ga in range(4)] for be in range(4)] for al in range(4)]
nu=1
divT=sum(dmu(Tmix[mu,nu],mu) for mu in range(4))
for mu in range(4):
 for l in range(4):
  divT+=Gam[mu][mu][l]*Tmix[l,nu]-Gam[l][mu][nu]*Tmix[mu,l]
# my EL
ginvD=sp.diag(*glow).inv()
L_field=L.subs(gvals)
rootg=sp.exp(a)*sp.exp(b)*r**2*sth
lag=rootg*L_field
ThR=sp.diff(Th,r)
EL_mine=(sp.diff(sp.diff(lag,ThR),r)-sp.diff(lag,Th))/rootg
Thp=sp.diff(Th,r)
print("Hilbert-stress divT_r - (-EL_mine*Theta') =", sp.simplify(divT + EL_mine*Thp))
