import sympy as sp

theta, phi = sp.symbols('theta phi', real=True)

def Y(l,m):
    return sp.Ynm(l,m,theta,phi).expand(func=True)

for (l,m) in [(1,0),(2,1)]:
    Ylm = Y(l,m)
    integrand = (Ylm*sp.conjugate(Ylm)).rewrite(sp.cos)
    val = sp.integrate(sp.integrate(integrand*sp.sin(theta),(phi,0,2*sp.pi)),(theta,0,sp.pi))
    print((l,m), "INT|Y|^2 dOmega =", sp.simplify(val))
