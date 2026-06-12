import sympy as sp
r=sp.symbols('r',positive=True)
G=sp.Function('G')(r); F=sp.Function('F')(r)
PHI=sp.Function('PHI')(r)
E,m,k=sp.symbols('E m k',real=True)
e2=sp.exp(2*PHI); e1=sp.exp(PHI); pp=PHI.diff(r)

# target residuals (=0):
tgtG = sp.diff(G,r) - ((pp-k/r)*G + (E*e2+m*e1)*F)
tgtF = sp.diff(F,r) - ((pp+k/r)*F - (E*e2-m*e1)*G)

# Find Lagrangian by ansatz with free coefficients on each structure.
c1,c2,c3,c4,c5,c6,c7,c8=sp.symbols('c1 c2 c3 c4 c5 c6 c7 c8')
L = ( c1*(F*sp.diff(G,r)-G*sp.diff(F,r))
      + c2*pp*F*G
      + c3*(k/r)*(G**2 - F**2)
      + c4*(k/r)*G*F
      + c5*E*e2*(F**2 + G**2)
      + c6*E*e2*G*F
      + c7*m*e1*(G**2 - F**2)
      + c8*m*e1*G*F )
def EL(fld):
    return sp.diff(L,fld) - sp.diff(sp.diff(L,sp.diff(fld,r)),r)
ELG=sp.expand(EL(G)); ELF=sp.expand(EL(F))
# We want EL_G proportional to tgtG? EL eqs give the operator; require ELG = alpha*(combination).
# Simpler: require ELG == lam1*tgtG and ELF==lam2*tgtF won't hold (mixing). Instead require the
# EL system to be EQUIVALENT to target. Match coefficients of independent terms.
# Collect ELG in basis {G', F', G/r*k, F/r*k, E e2 G, E e2 F, m e1 G, m e1 F, pp G, pp F}
lam=sp.symbols('lam')
# Require ELF (which contains G') equals lam * tgtG  (since tgtG is the G' equation)
# and ELG (contains F') equals mu * tgtF.
mu=sp.symbols('mu')
eqs=[]
# ELF - lam*tgtG = 0 identically:
diffF=sp.expand(ELF - lam*tgtG)
diffG=sp.expand(ELG - mu*tgtF)
# extract coefficients
terms=[sp.diff(G,r),sp.diff(F,r),G/r,F/r,E*e2*G,E*e2*F,m*e1*G,m*e1*F,pp*G,pp*F]
sol_eqs=[]
for d in [diffF,diffG]:
    p=sp.Poly(d,*[sp.diff(G,r),sp.diff(F,r)])
# manual: gather by pattern via coeff
def coeffs(expr):
    d={}
    d['Gp']=expr.coeff(sp.diff(G,r))
    d['Fp']=expr.coeff(sp.diff(F,r))
    rem=sp.expand(expr - d['Gp']*sp.diff(G,r) - d['Fp']*sp.diff(F,r))
    d['kG']=rem.coeff(k*G/r); d['kF']=rem.coeff(k*F/r)
    d['EG']=rem.coeff(E*e2*G); d['EF']=rem.coeff(E*e2*F)
    d['mG']=rem.coeff(m*e1*G); d['mF']=rem.coeff(m*e1*F)
    d['pG']=rem.coeff(pp*G); d['pF']=rem.coeff(pp*F)
    return d
cF=coeffs(diffF); cG=coeffs(diffG)
for key,val in {**{('F',k2):v for k2,v in cF.items()},**{('G',k2):v for k2,v in cG.items()}}.items():
    if val!=0: sol_eqs.append(sp.Eq(val,0))
sol=sp.solve(sol_eqs,[c1,c2,c3,c4,c5,c6,c7,c8,lam,mu],dict=True)
print("solution(s):",sol)
