import sympy as sp
t,r,th,ps = sp.symbols('t r theta psi', real=True)
c=sp.symbols('c',positive=True); N,om=sp.symbols('N omega',real=True)
phi=sp.Function('phi')(r); rho=sp.Function('rho')(r); Th=sp.Function('Theta')(r)
coords=[t,r,th,ps]
# diagonal metric (j=0)
gi=sp.diag(-sp.exp(2*phi)/c**2, sp.exp(-2*phi), 1/rho**2, 1/(rho**2*sp.sin(th)**2))
chi=N*ps+om*t
n=sp.Matrix([sp.sin(Th)*sp.cos(chi),sp.sin(Th)*sp.sin(chi),sp.cos(Th)])
def dn(mu): return sp.Matrix([sp.diff(n[i],coords[mu]) for i in range(3)])
S=sp.Matrix(4,4,lambda a,b:(dn(a).T*dn(b))[0])
# L4 = (kappa/4)|omega_H1|^2 ; |omega_H1|^2 = 2*(X^2 - Y)/2 where standard skyrme:
# |dn wedge dn|^2 form:  T4 = g^{ac}g^{bd}(S_ab S_cd - S_ad S_cb)  (the l1 l2 combination *2)
T4=0
for a in range(4):
 for b in range(4):
  for cc in range(4):
   for d in range(4):
     T4+= gi[a,cc]*gi[b,d]*(S[a,b]*S[cc,d]-S[a,d]*S[cc,b])
T4=sp.simplify(T4)
print("|omega_H1|^2 (=g g (SS-SS)) =")
sp.pprint(sp.factor(T4))

# correct area-form invariant I2 = l1*l2 = 1/2( (tr GS)^2 - tr((GS)^2) )
M = sp.zeros(4,4)                 # M = G*S  (mixed)
for a in range(4):
  for b in range(4):
    M[a,b]=sum(gi[a,cc]*S[cc,b] for cc in range(4))
X = sp.simplify(sp.trace(M))
tr2 = sp.simplify(sp.trace(M*M))
I2 = sp.simplify((X**2 - tr2)/2)
print("\nX (=l1+l2) =", sp.simplify(X))
print("\nI2 (=l1*l2 = |omega_H1|^2/normalization) =")
sp.pprint(sp.factor(I2))
