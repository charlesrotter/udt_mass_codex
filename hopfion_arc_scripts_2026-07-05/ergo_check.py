import sympy as sp
t,r,th,ps = sp.symbols('t r theta psi', real=True)
phi=sp.Function('phi')(r); rho=sp.Function('rho')(r)
c=sp.symbols('c',positive=True); N,om=sp.symbols('N omega',real=True)
# DIAGONAL native metric (no frame drag). omega lives ONLY in the matter phase chi=N psi+om t.
g=sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), rho**2, rho**2*sp.sin(th)**2)
print("g_tt =", g[0,0], "  -> sign depends on omega?", g[0,0].has(om))
print("norm of d_t Killing vector g_tt is INDEPENDENT of omega:", not g[0,0].has(om))
gi=g.inv()
print("g^tt =", sp.simplify(gi[0,0]))
print("g^psipsi =", sp.simplify(gi[3,3]))
# ergoregion = g_tt >= 0. Here g_tt=-e^{-2phi}c^2 < 0 ALWAYS. No ergoregion from omega in diagonal metric.
# B(r) bracket coefficient of sin^2 Theta:
B = N**2*gi[3,3] + om**2*gi[0,0]
print("\nB(r) = N^2 g^psipsi + om^2 g^tt =", sp.simplify(B))
print("B=0 is a MATTER-potential balance (winding vs spin), NOT g_tt sign change.")
