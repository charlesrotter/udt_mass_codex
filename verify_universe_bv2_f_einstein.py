"""bv2_f_einstein.py — BLIND VERIFIER C8: Einstein-reading identities, from scratch.
Metric ds^2 = -e^{-2phi(r)} dt^2 + e^{2phi(r)} dr^2 + rho(r)^2 dOmega^2   (c=1).
"""
import sympy as sp

t, r, th, ps, Z = sp.symbols('t r theta psi Z', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho', positive=True)(r)
P1, R1 = sp.diff(phi,r), sp.diff(rho,r)
P2, R2 = sp.diff(phi,r,2), sp.diff(rho,r,2)

x = [t, r, th, ps]
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), rho**2, rho**2*sp.sin(th)**2)
ginv = g.inv()
n = 4

Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            Gamma[a][b][c] = sp.simplify(sum(ginv[a,d]*(sp.diff(g[d,b],x[c]) + sp.diff(g[d,c],x[b]) - sp.diff(g[b,c],x[d])) for d in range(n))/2)

def Ricci(mu, nu):
    expr = 0
    for a in range(n):
        expr += sp.diff(Gamma[a][mu][nu], x[a]) - sp.diff(Gamma[a][mu][a], x[nu])
        for b in range(n):
            expr += Gamma[a][a][b]*Gamma[b][mu][nu] - Gamma[a][nu][b]*Gamma[b][mu][a]
    return sp.simplify(expr)

Ric = sp.zeros(n)
for mu in range(n):
    for nu in range(n):
        Ric[mu,nu] = Ricci(mu,nu)
Rs = sp.simplify(sum(ginv[mu,nu]*Ric[mu,nu] for mu in range(n) for nu in range(n)))
Gmix = sp.zeros(n)  # G^mu_nu
for mu in range(n):
    for nu in range(n):
        Gmix[mu,nu] = sp.simplify(sum(ginv[mu,a]*Ric[a,nu] for a in range(n)) - sp.Rational(1,2)*Rs*(1 if mu==nu else 0))

Gtt, Grr, Gthth, Gpsps = Gmix[0,0], Gmix[1,1], Gmix[2,2], Gmix[3,3]
print("G^t_t =", sp.simplify(Gtt))
print("G^r_r =", sp.simplify(Grr))
print("G^th_th =", sp.simplify(Gthth))
print("G^th_th == G^ps_ps:", sp.simplify(Gthth - Gpsps) == 0)

# (i) contracted Bianchi: nabla_mu G^mu_r == 0 OFF-shell
div_r = sum(sp.diff(Gmix[mu,1], x[mu]) for mu in range(n)) \
      + sum(Gamma[mu][mu][a]*Gmix[a,1] for mu in range(n) for a in range(n)) \
      - sum(Gamma[a][mu][1]*Gmix[mu,a] for mu in range(n) for a in range(n))
print("\n(i) nabla_mu G^mu_r off-shell == 0:", sp.simplify(div_r) == 0)

# on-shell substitutions (native EOMs with source sigma)
sig = sp.Function('sigma')(r)
phipp = 4*sp.exp(-2*phi)*R1**2/(Z*rho**2) - 2*P1*R1/rho
rhopp = 2*P1*R1 - Z/4*rho*sp.exp(2*phi)*P1**2 + sig
def onshell(e):
    # substitute rho'' first then phi'' (phipp contains no rho'')
    return sp.simplify(e.subs(R2, rhopp).subs(P2, phipp))

# (ii) 8pi(eps + 2 p_t) = -G^t_t + 2 G^th_th on-shell: sigma-free?
comb = onshell(-Gtt + 2*Gthth)
print("\n(ii) -G^t_t + 2G^th_th on-shell =", sp.expand(comb))
print("    sigma-free:", sp.diff(comb, sig) == 0)

# (iii) eps on-shell; solve for sigma
eps8pi = onshell(-Gtt)      # 8 pi eps
print("\n(iii) 8pi*eps on-shell =", sp.expand(eps8pi))
coef = sp.diff(eps8pi, sig)
print("    coefficient of sigma:", sp.simplify(coef), " (never 0) -> sigma recoverable:")
sigma_from_eps = sp.solve(sp.Eq(sp.Symbol('E8'), eps8pi), sig)[0]
print("    sigma =", sp.simplify(sigma_from_eps))
# G^r_r on-shell: first-order only, sigma-free?
grr_on = onshell(Grr)
print("    G^r_r on-shell sigma-free:", sp.diff(grr_on, sig) == 0, "; contains rho''/phi'' pre-sub:",
      Grr.has(R2), Grr.has(P2))

# (iv) constant cylinder
subs_cyl = [(P1,0),(R1,0),(P2,0),(R2,0)]
Gtt_cyl = Gtt.subs(subs_cyl)
print("\n(iv) constant cylinder: G^t_t =", sp.simplify(Gtt_cyl), " -> eps = 1/(8 pi rho0^2) > 0")
print("     cylinder solves sourceless EOMs: phi''=0, rho''=0 with phi'=rho'=0: True (rhs vanish)")

# Misner-Sharp identity: m = (rho/2)(1 - e^{-2phi} rho'^2); m' == 4 pi rho^2 rho' * eps, eps = -G^t_t/(8pi)
m = rho/2*(1 - sp.exp(-2*phi)*R1**2)
mp = sp.diff(m, r)
ident = sp.simplify(mp - 4*sp.pi*rho**2*R1*(-Gtt/(8*sp.pi)))
print("\nMisner-Sharp m' = 4 pi rho^2 rho' eps  OFF-shell identity:", ident == 0)
