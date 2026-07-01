import sympy as sp
# Compute div_mu T^mu_r symbolically from the Hilbert stress of L2+L4 (round, radial),
# express as (coefficient)*(EL). The physically-correct matter EL is the one whose
# zero set = conservation. Compare its proportionality to (i) audited radial rhs,
# (ii) my from-scratch EL.
r=sp.symbols('r',positive=True); th,ps=sp.symbols('theta psi')
xi,kap=sp.symbols('xi kappa',positive=True)
a=sp.Function('a')(r); b=sp.Function('b')(r); Th=sp.Function('Theta')(r)
coords=[sp.symbols('t'),r,th,ps]
g=sp.diag(-sp.exp(2*a),sp.exp(2*b),r**2,r**2*sp.sin(th)**2)
ginv=g.inv()
sT,cT=sp.sin(Th),sp.cos(Th); sth,cth=sp.sin(th),sp.cos(th)
nA=[cT, sT*sth*sp.cos(ps), sT*sth*sp.sin(ps), sT*cth]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for mu in range(4):
 for nu in range(4):
  Gmn[mu,nu]=sum(dmu(nA[A],mu)*dmu(nA[A],nu) for A in range(4))
L2=-(xi/2)*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
SS=sp.MutableDenseNDimArray.zeros(4,4,4,4)
L4=0
for mu in range(4):
 for nu in range(4):
  for pp in range(4):
   for q in range(4):
    L4+=ginv[mu,pp]*ginv[nu,q]*(Gmn[mu,nu]*Gmn[pp,q]-Gmn[mu,q]*Gmn[pp,nu])
L4=-(kap/4)*L4
L=L2+L4
# T_{ab} = xi G_{ab} + kap [g^{nq} SS_{a n b q}]_sym + g_{ab} L,  SS=G_{ap}G_{nq}-G_{aq}G_{np}
SSt=sp.MutableDenseNDimArray.zeros(4,4,4,4)
for A in range(4):
 for nn in range(4):
  for B in range(4):
   for q in range(4):
    SSt[A,nn,B,q]=Gmn[A,B]*Gmn[nn,q]-Gmn[A,q]*Gmn[nn,B]
Cab=sp.zeros(4,4)
for A in range(4):
 for B in range(4):
  Cab[A,B]=sum(ginv[nn,q]*SSt[A,nn,B,q] for nn in range(4) for q in range(4))
Cab=(Cab+Cab.T)/2
Tlow=xi*Gmn+kap*Cab+g*L
Tmix=ginv*Tlow  # T^mu_nu
# Christoffels
Gam=[[[0]*4 for _ in range(4)] for _ in range(4)]
for al in range(4):
 for be in range(4):
  for ga in range(4):
   Gam[al][be][ga]=sum(ginv[al,de]*(dmu(g[de,be],ga)+dmu(g[de,ga],be)-dmu(g[be,ga],de)) for de in range(4))/2
# div_mu T^mu_nu = d_mu T^mu_nu + Gam^mu_mu_l T^l_nu - Gam^l_mu_nu T^mu_l
nu=1  # r component
div=0
for mu in range(4):
    div+=dmu(Tmix[mu,nu],mu)
    for l in range(4):
        div+=Gam[mu][mu][l]*Tmix[l,nu]-Gam[l][mu][nu]*Tmix[mu,l]
div=sp.simplify(div)
# substitute to symbols, factor out (Thpp - rhs)
Thpp=sp.Symbol('Thpp');Thp=sp.Symbol('Thp');ThS=sp.Symbol('ThS');ap=sp.Symbol('ap');bp=sp.Symbol('bp');B=sp.Symbol('B')
subs={sp.diff(Th,r,2):Thpp,sp.diff(Th,r):Thp,Th:ThS,sp.diff(a,r):ap,sp.diff(b,r):bp,sp.exp(2*b):B}
divs=sp.simplify(div.subs(subs))
# coefficient of Thpp in div:
cThpp=sp.simplify(sp.diff(divs,Thpp))
rhs_from_divT=sp.simplify(Thpp - divs/cThpp)  # the EL implied by conservation: Thpp = rhs
print("coeff of Thpp in divT:", cThpp)
# audited rhs:
s=sp.sin(ThS)
num=(-2*kap*r**2*s**2*Thp*ap+2*kap*r**2*s**2*Thp*bp-kap*r**2*sp.sin(2*ThS)*Thp**2
     +2*kap*B*s**3*sp.cos(ThS)-r**4*xi*Thp*ap+r**4*xi*Thp*bp-2*r**3*xi*Thp+r**2*xi*B*sp.sin(2*ThS))
den=r**2*(2*kap*s**2+r**2*xi)
rhs_audit=num/den
print("\n[conservation EL rhs] - [audited rhs]:", sp.simplify(rhs_from_divT - Thpp + rhs_audit*0 - (rhs_from_divT - Thpp)))
print("divT-implied rhs - audited rhs =", sp.simplify((Thpp-rhs_from_divT)*0 + (rhs_audit - (Thpp-(Thpp-divs/cThpp)))) )
# cleaner: rhs implied = divs/cThpp solved: Thpp - divs/cThpp =0 => rhs = Thpp - (Thpp-divs/cThpp)... just compute divs/cThpp set=0
rhs_cons=sp.solve(divs,Thpp)[0]
print("\nrhs_conservation - rhs_audit =", sp.simplify(rhs_cons - rhs_audit))
