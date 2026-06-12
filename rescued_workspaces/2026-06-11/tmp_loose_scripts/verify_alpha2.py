import sympy as sp
t, r, th, ph = sp.symbols('t r theta phi_coord', real=True)
phi0 = sp.Function('phi0')(r)
h_tr  = sp.Function('h_tr')(r, th, ph)
h_tth = sp.Function('h_tth')(r, th, ph)

new_term = (sp.exp(2*phi0)/r**2)*(sp.diff(h_tr,th) - 2*h_tth*sp.diff(phi0,r) - sp.diff(h_tth,r))
new_exp = sp.expand(new_term)
co = sp.simplify(sp.diff(new_exp, sp.Derivative(h_tr,th)))
print("coeff of d_theta h_tr =", co)
print("equals e^{2phi0}/r^2 ?", sp.simplify(co - sp.exp(2*phi0)/r**2)==0)

# So: gravitomagnetic coeff of d_theta h_tr = 1 * e^{2phi0}/r^2
# scalar canonical (12.15.2): coeff of d_theta dphi = 2 * e^{2phi0}/r^2
# Same e^{2phi0}/r^2 metric structure, factor 2 difference in numeral.
