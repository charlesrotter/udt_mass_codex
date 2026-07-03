"""bv13 W5(iii): fixed-U homothety Jacobi residual.
Family: phi_lam(r) = phi(r/lam), rho_lam(r) = lam*rho(r/lam)  (direction g=-r phi', h=rho-r rho').
Claim: J_phi = 0 exactly; J_rho[h] = -(e^{2phi}/4)(rho U'' + U') on-shell.
Residual conventions: R_phi = phi'' - 4e^{-2phi}rho'^2/(Z rho^2) + 2 phi' rho'/rho
                      R_rho = rho'' - 2 phi' rho' + (Z/4) rho e^{2phi} phi'^2 - (e^{2phi}/4) U'(rho)
(so that R=0 is the banked EOM; J = d/dlam R[phi_lam,rho_lam] at lam=1, EOM substituted)
"""
import sympy as sp

r, lam = sp.symbols('r lambda', positive=True)
Z = sp.Symbol('Z', positive=True)
Uf = sp.Function('U')
phi = sp.Function('phi'); rho = sp.Function('rho')

s = r/lam
phl = phi(s)
rhl = lam*rho(s)

def Rphi(f, g):
    return sp.diff(f, r, 2) - 4*sp.exp(-2*f)*sp.diff(g, r)**2/(Z*g**2) + 2*sp.diff(f, r)*sp.diff(g, r)/g

def Rrho(f, g):
    return sp.diff(g, r, 2) - 2*sp.diff(f, r)*sp.diff(g, r) + (Z/4)*g*sp.exp(2*f)*sp.diff(f, r)**2 \
           - (sp.exp(2*f)/4)*sp.diff(Uf(g), g)

Jphi = sp.diff(Rphi(phl, rhl), lam).subs(lam, 1)
Jrho = sp.diff(Rrho(phl, rhl), lam).subs(lam, 1)

# EOM substitutions (background on-shell): phi'' and rho'' and their r-derivatives (3rd order)
x = sp.Symbol('x')
p2 = 4*sp.exp(-2*phi(r))*sp.diff(rho(r), r)**2/(Z*rho(r)**2) - 2*sp.diff(phi(r), r)*sp.diff(rho(r), r)/rho(r)
r2 = 2*sp.diff(phi(r), r)*sp.diff(rho(r), r) - (Z/4)*rho(r)*sp.exp(2*phi(r))*sp.diff(phi(r), r)**2 \
     + (sp.exp(2*phi(r))/4)*sp.diff(Uf(rho(r)), rho(r))

def on_shell(expr):
    # substitute 3rd derivatives first (obtained by differentiating the EOMs), then 2nd
    p3 = sp.diff(p2, r); r3 = sp.diff(r2, r)   # still contain 2nd derivatives; substitute below
    e = expr.subs({sp.diff(phi(r), r, 3): p3, sp.diff(rho(r), r, 3): r3})
    for _ in range(3):
        e = e.subs({sp.diff(phi(r), r, 2): p2, sp.diff(rho(r), r, 2): r2})
    return sp.simplify(e)

Jphi_os = on_shell(Jphi)
print("[W5iii] J_phi on-shell =", Jphi_os)
Jrho_os = on_shell(Jrho)
claim = -(sp.exp(2*phi(r))/4)*(rho(r)*sp.diff(Uf(rho(r)), rho(r), 2)*1 + sp.diff(Uf(x), x).subs(x, rho(r)))
# careful: rho U''(rho) + U'(rho)
U1 = sp.diff(Uf(x), x).subs(x, rho(r)); U2 = sp.diff(Uf(x), x, 2).subs(x, rho(r))
claim = -(sp.exp(2*phi(r))/4)*(rho(r)*U2 + U1)
print("[W5iii] J_rho on-shell - claim =", sp.simplify(Jrho_os - claim))
print("[W5iii] J_rho on-shell =", Jrho_os)

# contrast (drift check): the NAIVE pure-scaling direction (g,h)=(0,rho) --
phl2, rhl2 = phi(r), lam*rho(r)
Jrho2 = on_shell(sp.diff(Rrho(phl2, rhl2), lam).subs(lam, 1))
print("[W5iii contrast] pure rho-scaling J_rho =", Jrho2, "  (differs: U'-sign)")
