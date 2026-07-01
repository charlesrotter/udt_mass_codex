import sympy as sp
# Compare committed C_ab stress vs true Hilbert stress, L4 sector, round limit.
r=sp.symbols('r',positive=True); th,ps=sp.symbols('theta psi')
xi,kap=sp.symbols('xi kappa',positive=True)
a=sp.Function('a')(r); b=sp.Function('b')(r); Th=sp.Function('Theta')(r)
coords=[sp.symbols('t'),r,th,ps]
sT,cT=sp.sin(Th),sp.cos(Th); sth,cth=sp.sin(th),sp.cos(th)
nA=[cT,sT*sth*sp.cos(ps),sT*sth*sp.sin(ps),sT*cth]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for m in range(4):
 for n in range(4):
  Gmn[m,n]=sum(dmu(nA[A],m)*dmu(nA[A],n) for A in range(4))
glow=[-sp.exp(2*a),sp.exp(2*b),r**2,r**2*sth**2]
g=sp.diag(*glow); ginv=g.inv()
# --- committed C_ab stress (from whole_metric_3d_matter / matter_stress_t) ---
SS=lambda m,n,pp,q: Gmn[m,n]*Gmn[pp,q]-Gmn[m,q]*Gmn[pp,n]  # SS_{m n pp q}? note index order
# committed: SS_{mnpq}=G_{mp}G_{nq}-G_{mq}G_{np}; C_ab=g^{nq}SS_{a n b q}
SS2=lambda A,nn,B,q: Gmn[A,B]*Gmn[nn,q]-Gmn[A,q]*Gmn[nn,B]
Cab=sp.zeros(4,4)
for A in range(4):
 for B in range(4):
  Cab[A,B]=sum(ginv[nn,q]*SS2(A,nn,B,q) for nn in range(4) for q in range(4))
Cab=(Cab+Cab.T)/2
# L for the g_ab L term
L2=-(xi/2)*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
L4=-(kap/4)*sum(ginv[m,pp]*ginv[n,q]*SS2(m,n,pp,q) for m in range(4) for n in range(4) for pp in range(4) for q in range(4))
L=L2+L4
Tlow_comm=xi*Gmn+kap*Cab+g*L
# --- true Hilbert stress ---
gI=sp.symbols('gItt gIrr gIth gIps'); ginvS=sp.diag(*gI)
L2s=-(xi/2)*sum(ginvS[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
L4s=-(kap/4)*sum(ginvS[m,pp]*ginvS[n,q]*SS2(m,n,pp,q) for m in range(4) for n in range(4) for pp in range(4) for q in range(4))
Ls=L2s+L4s
gvals={gI[0]:1/glow[0],gI[1]:1/glow[1],gI[2]:1/glow[2],gI[3]:1/glow[3]}
Tlow_hilb=sp.zeros(4,4)
for i in range(4):
    Tlow_hilb[i,i]=(-2*sp.diff(Ls,gI[i])+glow[i]*Ls).subs(gvals)
print("T_munu committed - T_munu Hilbert (diagonal), simplified:")
for i in range(4):
    df=sp.simplify(Tlow_comm[i,i]-Tlow_hilb[i,i])
    print(f"  ({i},{i}): {df}")
# off-diagonal of committed (round=0 expected)
print("  committed off-diag (1,2):", sp.simplify(Tlow_comm[1,2]))
