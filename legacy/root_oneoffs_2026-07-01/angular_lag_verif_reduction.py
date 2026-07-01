import sympy as sp
th,k,F = sp.symbols('theta kappa F', positive=True)
f = F*(1+k*sp.cos(th))
dens_dpf = sp.simplify(sp.diff(f,th)**2/(4*f))
print("dpf density f_theta^2/(4f):", dens_dpf)
print("  /(F k^2/4) =", sp.simplify(dens_dpf/(F*k**2/4)))
