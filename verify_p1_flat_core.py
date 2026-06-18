import sympy as sp
r = sp.symbols('r', positive=True)
phi = sp.Function('phi')
# 2 r phi' + e^{2phi} - 1 = 0.  Let u = e^{2phi} (=g_rr). Standard: this is Schwarzschild.
# Substitute m(r): e^{2phi}=1/(1-2m/r) is the usual Schwarzschild form for g_rr.
# Solve ODE directly.
ode = 2*r*phi(r).diff(r) + sp.exp(2*phi(r)) - 1
sol = sp.dsolve(ode, phi(r))
print("general solution:", sol)
# Express g_rr = e^{2phi}
for s in (sol if isinstance(sol, list) else [sol]):
    grr = sp.simplify(sp.exp(2*s.rhs))
    print("g_rr = e^{2phi} =", grr)
