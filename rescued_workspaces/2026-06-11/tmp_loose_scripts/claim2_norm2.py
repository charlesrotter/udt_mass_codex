import sympy as sp
# Remove the PHI' diagonal terms by substitution G = e^{alpha PHI} g, F = e^{alpha PHI} f.
r=sp.symbols('r',positive=True)
PHI=sp.Function('PHI')(r); PHIp=sp.diff(PHI,r)
k=sp.symbols('kappa'); m=sp.symbols('m'); E=sp.symbols('E')
g=sp.Function('g')(r); f=sp.Function('f')(r)
alpha=sp.symbols('alpha')
e1=sp.exp(PHI); e2=sp.exp(2*PHI); ea=sp.exp(alpha*PHI)
G=ea*g; Fn=ea*f
# original eqs:
eqG=sp.diff(G,r)-((PHIp-k/r)*G+(E*e2+m*e1)*Fn)
eqF=sp.diff(Fn,r)-((PHIp+k/r)*Fn-(E*e2-m*e1)*G)
eqG=sp.expand(eqG/ea); eqF=sp.expand(eqF/ea)
# choose alpha to kill PHIp*g and PHIp*f diagonal terms:
print("eqG (G=e^{aPHI}g):", sp.collect(sp.simplify(eqG), PHIp))
print("coeff of PHIp in eqG:", sp.simplify(eqG.coeff(PHIp)))
sol=sp.solve(eqG.coeff(PHIp),alpha)
print("alpha that removes PHIp diagonal:",sol)
# use alpha=1:
a=1
eqG1=sp.expand((sp.diff(sp.exp(PHI)*g,r)-((PHIp-k/r)*sp.exp(PHI)*g+(E*e2+m*e1)*sp.exp(PHI)*f))/sp.exp(PHI))
eqF1=sp.expand((sp.diff(sp.exp(PHI)*f,r)-((PHIp+k/r)*sp.exp(PHI)*f-(E*e2-m*e1)*sp.exp(PHI)*g))/sp.exp(PHI))
print("\nWith G=e^{PHI}g, F=e^{PHI}f:")
print("eqG1=0:", sp.simplify(eqG1))
print("eqF1=0:", sp.simplify(eqF1))
