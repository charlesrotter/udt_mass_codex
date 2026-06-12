import sympy as sp
import itertools
# Form-T radial Dirac RHS (operator sees PHI). Write d/dr[G,F] = rhs.
r,k,E,m = sp.symbols('r kappa E m', real=True)
PHI = sp.Function('PHI')(r); PHIp = sp.diff(PHI,r)
e1=sp.exp(PHI); e2=sp.exp(2*PHI)
def rhs(G,F,PHIp,e1,e2,E,m,k):
    dG=(PHIp-k/r)*G+(E*e2+m*e1)*F
    dF=(PHIp+k/r)*F-(E*e2-m*e1)*G
    return dG,dF
G,F=sp.symbols('G F')
# ORIGINAL system: dG,dF as above
dG0,dF0=rhs(G,F,PHIp,e1,e2,E,m,k)

print("φ→−φ sends the OPERATOR PHI→−PHI, i.e. e^{2PHI}→e^{−2PHI}, e^{PHI}→e^{−PHI}, PHI'→−PHI'.")
print("Binding needs e^{2PHI}>1 (PHI>0); the mirror has e^{−2PHI}<1 (PHI<0) -> the BINDING sheet maps to the")
print("NON-binding sheet. So the mirror cannot pair the bound spectrum with itself unless a companion transform")
print("(E→±E, m→±m, κ→±κ, G↔F, signs) restores the SAME binding operator. Search for it:\n")

# After φ→-φ: PHIp->-PHIp, e1->1/e1, e2->1/e2
me1,me2,mPHIp = 1/e1, 1/e2, -PHIp
found=[]
for sE,sm,sk,swap,sg,sf in itertools.product([1,-1],[1,-1],[1,-1],[0,1],[1,-1],[1,-1]):
    # candidate new fields
    if swap: Gn,Fn = sg*F, sf*G
    else:    Gn,Fn = sg*G, sf*F
    # build mirrored RHS with transformed params, in terms of (G,F)
    dGn,dFn = rhs(Gn,Fn,mPHIp,me1,me2,sE*E,sm*m,sk*k)
    # we need d/dr of (Gn,Fn) to match rhs structure -> compare d(Gn)/dr vs dGn etc.
    # d(sg*G)/dr = sg*dG0 ; d(sf*F)/dr=sf*dF0 ; if swap, d(sg*F)/dr=sg*dF0, d(sf*G)/dr=sf*dG0
    if swap:
        lhsG, lhsF = sg*dF0, sf*dG0
    else:
        lhsG, lhsF = sg*dG0, sf*dF0
    ok = sp.simplify(lhsG-dGn)==0 and sp.simplify(lhsF-dFn)==0
    if ok:
        found.append((sE,sm,sk,'swap' if swap else 'noswap',sg,sf))
print("Exact symmetries of the Form-T under φ→−φ + companion transform (E,m,κ signs; G/F swap+signs):")
if found:
    for t in found: print("   E→%+d E, m→%+d m, κ→%+d κ, %s, G→%+dG/F, F→%+dF/G"%(t[0],t[1],t[2],t[3],t[4],t[5]))
else:
    print("   NONE.")
print()
print("Interpretation: if a symmetry exists with E→−E it = charge conjugation (matter↔antimatter); with E→+E")
print("it = an exact degeneracy/pairing; if NONE, φ→−φ is NOT a symmetry of the binding Dirac (no new instrument).")
