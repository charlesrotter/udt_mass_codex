import sympy as sp
# What is the PHYSICALLY-CORRECT Dirac normalization measure on this metric?
# Conserved Dirac probability: Q = INT_Sigma j^mu dSigma_mu, j^mu = psibar gamma^mu psi.
# On a t=const slice: Q = INT j^t sqrt(-g) d^3x  (with appropriate lapse handling).
# Actually conserved charge: Q = INT_{t=const} j^t sqrt(-g) d^3x. j^t = e^t_a psibar gamma^a psi.
# Vierbein e^0=e^{-PHI}dt => e^t_0 = e^{PHI} (inverse). j^t = e^{PHI} psibar gamma^0 psi
#   = e^{PHI} psi^dagger psi (since psibar gamma^0 = psi^dagger).
# sqrt(-g)=r^2 sin th. d^3x = dr dth dph. Angular normalized => radial measure:
#   Q_radial = INT e^{PHI} (psi^dagger psi)_radial * r^2 dr.
# Now psi^dagger psi radial in Form-T: the upper/lower radial fns. The Form-T (G,F) are usually
# defined to ABSORB the r and frame factors so that psi^dagger psi r^2 ~ (G^2+F^2) OR ~ e^{?}(G^2+F^2).
# This is the load-bearing question. Let's determine it from the requirement that the Form-T system
# be the EIGENVALUE problem of a self-adjoint operator in its natural measure -- i.e. find the weight
# rho(r) such that the operator H with H(G,F)=E(G,F)-ish is symmetric in INT rho (G^2+F^2) dr.

# From the system:
#  G' = (PHI'-k/r)G + (E e^{2PHI}+m e^{PHI})F
#  F' = (PHI'+k/r)F - (E e^{2PHI}-m e^{PHI})G
# Write as E-eigenproblem. Isolate E:
#  from row1: E e^{2PHI} F = G' -(PHI'-k/r)G - m e^{PHI}F
#  from row2: E e^{2PHI} G = -(F' -(PHI'+k/r)F + m e^{PHI}G)
# So E e^{2PHI}(G^2+F^2)... multiply row1 by F, row2 by G... let's find the conserved measure:
# The standard Dirac eigenproblem  H psi = E W psi  has weight W=e^{2PHI} here (the E e^{2PHI} factor).
# Self-adjointness weight = e^{2PHI}? Let's test: is INT e^{2PHI}(G^2+F^2) dr the conserved norm under
# E-evolution? Check the Wronskian-type identity for two energies E1,E2.
r=sp.symbols('r',positive=True)
PHI=sp.Function('PHI')(r); PHIp=sp.diff(PHI,r)
k=sp.symbols('kappa'); m=sp.symbols('m')
G1,F1,G2,F2=[sp.Function(n)(r) for n in ['G1','F1','G2','F2']]
E1,E2=sp.symbols('E1 E2')
e2=sp.exp(2*PHI); e1=sp.exp(PHI)
def G_(G,F,E): return (PHIp-k/r)*G+(E*e2+m*e1)*F
def F_(G,F,E): return (PHIp+k/r)*F-(E*e2-m*e1)*G
# Consider d/dr[ G1 F2 - F1 G2 ] and see what weight emerges.
W = G1*F2 - F1*G2
dW = sp.diff(W,r).subs({sp.diff(G1,r):G_(G1,F1,E1),sp.diff(F1,r):F_(G1,F1,E1),
                        sp.diff(G2,r):G_(G2,F2,E2),sp.diff(F2,r):F_(G2,F2,E2)})
dW=sp.simplify(sp.expand(dW))
print("d/dr(G1 F2 - F1 G2) =", dW)
# factor (E1-E2):
print("\ncoefficient of (E1-E2):", sp.simplify(dW/(E1-E2)) if (E1-E2)!=0 else None)
