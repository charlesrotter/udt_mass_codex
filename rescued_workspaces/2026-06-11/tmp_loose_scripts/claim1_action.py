import sympy as sp
# Reconstruct a first-order action S[G,F,phi] whose EL eqs (in G,F) reproduce the Form-T system,
# then compute delta S/delta phi analytically and compare to the claimed source.
r=sp.symbols('r',positive=True)
G=sp.Function('G')(r); F=sp.Function('F')(r)
PHI=sp.Function('PHI')(r)
E,m,k,sigma=sp.symbols('E m k sigma',real=True)

# Target system:
#  G' = (PHI' - k/r)G + (E e^{2PHI}+ m e^{PHI})F
#  F' = (PHI' + k/r)F - (E e^{2PHI}- m e^{PHI})G
# A standard first-order (Dirac) Lagrangian (after angular integration) has the form
#   L = F G' - G F'  + (potential terms).  Let's posit:
#   L = (1/2)(F G' - G F')  - (k/r) G F  + PHI'? ...  We instead BUILD L by requiring EL match.
# Use general ansatz:
a,b,c,d = sp.symbols('a b c d')
e2=sp.exp(2*PHI); e1=sp.exp(PHI)
# Ansatz Lagrangian density:
L = ( sp.Rational(1,2)*(F*sp.diff(G,r)-G*sp.diff(F,r))
      - PHI.diff(r)*F*G                                   # PHI' coupling
      + (k/r)*sp.Rational(1,2)*(G**2 - F**2)              # kappa channel? sign tbd
      - sp.Rational(1,2)*E*e2*(F**2 + G**2)               # energy term
      + sp.Rational(1,2)*m*e1*(G**2 - F**2) )             # mass term
# EL wrt G: dL/dG - d/dr(dL/dG') =0
def EL(fld):
    return sp.diff(L,fld) - sp.diff(sp.diff(L,sp.diff(fld,r)),r)
ELG=sp.simplify(EL(G))
ELF=sp.simplify(EL(F))
print("EL_G =0 :", ELG)
print("EL_F =0 :", ELF)
