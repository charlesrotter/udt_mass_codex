import sympy as sp
y,q,t = sp.symbols('y q t', positive=True)
nn = sp.Symbol('n')
s = q*(1-q)/2; f0 = y**(-q); J = -s*y**(-q)
c_n = J*f0**(1-nn)/nn
gv, gd = sp.symbols('g gdot', positive=True)  # field value and t-derivative as symbols

# L_t(t, g, gdot) = (1/4) e^t gdot^2 + e^t c_n(e^t) g^n   -- explicit t only via coefficients
Lt = sp.Rational(1,4)*sp.exp(t)*gd**2 + (sp.exp(t)*c_n).subs(y, sp.exp(t))*gv**nn
dLt_expl = sp.diff(Lt, t)           # now a genuine explicit partial
bgv, bgd = sp.exp(-q*t), -q*sp.exp(-q*t)
leak_t = sp.powsimp(sp.expand(-dLt_expl.subs([(gv,bgv),(gd,bgd)])), force=True)
coef = sp.simplify(leak_t/sp.exp((1-2*q)*t))
solT = sp.solve(sp.Eq(coef,0), nn)
print("C7fix t-frame closure: n =", [sp.simplify(v) for v in solT])
print("C7fix matches y-frame n_A' = -2(1-q)/q:",
      sp.simplify(solT[0] + 2*(1-q)/q) == 0)
# direct cross-check: h_t = y h_y identically
F = sp.Function('F')(y)
h_y = sp.Rational(1,4)*y**2*sp.diff(F,y)**2 - c_n*F**nn
# h_t in y variables: gdot = y F', e^t = y:
h_t = (sp.Rational(1,4)*sp.exp(t)*gd**2 - (sp.exp(t)*c_n).subs(y,sp.exp(t))*gv**nn
      ).subs([(gd, y*sp.diff(F,y)), (gv, F), (t, sp.log(y))])
print("h_t = y*h_y identically:", sp.simplify(sp.expand(h_t - y*h_y)) == 0)
# value of h_tot on background at n = -2(1-q)/q is exactly zero:
hbg = sp.powsimp((sp.Rational(1,4)*y**2*sp.diff(f0,y)**2 - c_n*f0**nn), force=True)
print("h_tot[bg] coefficient:", sp.simplify(hbg/y**(-2*q)),
      "| zero at n=-2(1-q)/q:", sp.simplify((hbg/y**(-2*q)).subs(nn, -2*(1-q)/q)) == 0)
