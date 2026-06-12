import sympy as sp
r=sp.symbols('r',positive=True)
G=sp.Function('G')(r); F=sp.Function('F')(r)
PHI=sp.Function('PHI')(r)
E,m,k=sp.symbols('E m k',real=True)
e2=sp.exp(2*PHI); e1=sp.exp(PHI); pp=PHI.diff(r)

# General antisym + symmetric ansatz
c1,c2,c3,c4,c5,c6,c7,c8=sp.symbols('c1:9')
L = ( c1*(F*sp.diff(G,r)-G*sp.diff(F,r))
      + c2*pp*F*G + c3*(k/r)*(G**2 - F**2) + c4*(k/r)*G*F
      + c5*E*e2*(F**2 + G**2) + c6*E*e2*G*F
      + c7*m*e1*(G**2 - F**2) + c8*m*e1*G*F )
def EL(fld):
    return sp.expand(sp.diff(L,fld) - sp.diff(sp.diff(L,sp.diff(fld,r)),r))
ELG=EL(G); ELF=EL(F)

# Target equations (each =0):
tgtG = sp.expand(sp.diff(G,r) - ((pp-k/r)*G + (E*e2+m*e1)*F))   # the G' eq
tgtF = sp.expand(sp.diff(F,r) - ((pp+k/r)*F - (E*e2-m*e1)*G))   # the F' eq

# Strategy: ELG=0 is the equation obtained by varying G; it should be (a multiple of) the F' eq
#   because varying G yields the equation containing F' (Dirac structure). Let's just check which.
# Build dictionary of monomials and match ELG to a*tgtF and ELF to b*tgtG.
a,b=sp.symbols('a b')
mons=[sp.diff(G,r),sp.diff(F,r),G/r,F/r,e2*G,e2*F,e1*G,e1*F,pp*G,pp*F]
def vec(expr):
    expr=sp.expand(expr)
    out=[]
    tmp=expr
    # peel known monomials
    for mn,coef in [(sp.diff(G,r),1),(sp.diff(F,r),1)]:
        out.append(expr.coeff(mn)); 
    out.append(expr.coeff(k*G/r)); out.append(expr.coeff(k*F/r))
    out.append(expr.coeff(E*e2*G)); out.append(expr.coeff(E*e2*F))
    out.append(expr.coeff(m*e1*G)); out.append(expr.coeff(m*e1*F))
    out.append(expr.coeff(pp*G)); out.append(expr.coeff(pp*F))
    return out

eqs=[]
for x,y in zip(vec(ELG - a*tgtF), [0]*10): eqs.append(sp.Eq(x,0))
for x,y in zip(vec(ELF - b*tgtG), [0]*10): eqs.append(sp.Eq(x,0))
eqs=[e for e in eqs if e!=True]
sol=sp.solve(eqs,[c1,c2,c3,c4,c5,c6,c7,c8,a,b],dict=True)
print("sol:",sol)
