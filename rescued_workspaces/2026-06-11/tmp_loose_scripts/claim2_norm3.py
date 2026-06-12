import sympy as sp
r=sp.symbols('r',positive=True)
PHI=sp.Function('PHI')(r); PHIp=sp.diff(PHI,r)
k=sp.symbols('kappa'); m=sp.symbols('m')
g1,f1,g2,f2=[sp.Function(n)(r) for n in ['g1','f1','g2','f2']]
E1,E2=sp.symbols('E1 E2')
e1=sp.exp(PHI); e2=sp.exp(2*PHI)
def gp(g,f,E): return -k/r*g+(E*e2+m*e1)*f
def fp(g,f,E):  return  k/r*f-(E*e2-m*e1)*g
W=g1*f2-f1*g2
dW=sp.diff(W,r).subs({sp.diff(g1,r):gp(g1,f1,E1),sp.diff(f1,r):fp(g1,f1,E1),
                      sp.diff(g2,r):gp(g2,f2,E2),sp.diff(f2,r):fp(g2,f2,E2)})
dW=sp.simplify(sp.expand(dW))
print("d/dr(g1 f2 - f1 g2) =", sp.factor(dW))
print("\n=> coefficient of (E2-E1):", sp.simplify(sp.factor(dW)/(E2-E1)))
# Orthogonality: INT [d/dr W] = boundary=0 => INT (E2-E1) e^{2PHI}(g1 g2+f1 f2) dr=0
# => orthogonality weight is e^{2PHI}, in the g,f variables. Convert back to G,F: g=e^{-PHI}G etc:
print("\n=> weight in (g,f): e^{2PHI}.  Norm = INT e^{2PHI}(g^2+f^2) dr.")
print("   In G,F variables (G=e^{PHI}g => g=e^{-PHI}G): e^{2PHI}(g^2+f^2)=e^{2PHI}e^{-2PHI}(G^2+F^2)=(G^2+F^2).")
print("   *** So the conserved Dirac norm IS  INT (G^2+F^2) dr  -- EXACTLY the claim's measure (W=1)! ***")
