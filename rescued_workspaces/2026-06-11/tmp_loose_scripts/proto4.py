import sympy as sp

q, lam, rho = sp.symbols("q lam rho", positive=True)
W = sp.Function("W", real=True)(rho)
s_tie = q*(1-q)/2
p = -(1-2*q)/2
tau0sq = 4*lam/q**2
nu2 = (1+4*q*(1-q))/q**2

u = rho**p * W
lhs = sp.diff(rho**(2-2*q)*sp.diff(u, rho), rho) \
    - (lam*rho**(-q) + 4*s_tie*rho**(-2*q))*u
# Bessel operator tau^2 w'' + tau w' - (tau^2+nu^2) w rewritten via W(rho),
# tau = tau0 rho^{q/2}:
#   tau w'  = (2/q) rho W'
#   tau^2 w'' = (4/q^2)[rho^2 W'' + (1 - q/2) rho W'] - wait check sign
bess = (sp.Rational(4,1)/q**2*(rho**2*sp.diff(W,rho,2) + (1-q/2)*rho*sp.diff(W,rho))
        + sp.Rational(2,1)/q*rho*sp.diff(W,rho)
        - (tau0sq*rho**q + nu2)*W)
target = rho**(p-2*q)*(q**2/4)*bess
print(sp.simplify(lhs - target))
# nu at q=1/3
print(sp.simplify(sp.sqrt(nu2.subs(q, sp.Rational(1,3))) - sp.sqrt(17)))
