import sympy as sp
# Static scalar field phi(r) only (no t-dependence): canonical scalar stress-energy T_tr
t,r,th,ph = sp.symbols('t r theta phi_c', real=True)
phi = sp.Function('phi')(r)   # static -> function of r only
mu = sp.symbols('mu', positive=True)
# canonical metric
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
x=[t,r,th,ph]
# scalar field psi(r) static
psi = sp.Function('psi')(r)
# T_{mu nu} = d_mu psi d_nu psi - 1/2 g_{mu nu}(g^ab d_a psi d_b psi + mu^2 psi^2)
dpsi=[sp.diff(psi,xx) for xx in x]
kin = sum(ginv[a,b]*dpsi[a]*dpsi[b] for a in range(4) for b in range(4))
T = sp.zeros(4,4)
for m in range(4):
    for n in range(4):
        T[m,n] = dpsi[m]*dpsi[n] - sp.Rational(1,2)*g[m,n]*(kin + mu**2*psi**2)
print("T_tr (static scalar) =", sp.simplify(T[0,1]))
# also time-derivative form: T_tr = d_t psi d_r psi (the AUDIT claim)
print("d_t psi * d_r psi    =", sp.diff(psi,t)*sp.diff(psi,r))
