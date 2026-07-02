"""bv8 blind-verifier CAS: independent re-derivation of Claims A, B, C1, C2 (+H conservation).
System (as banked, taken from cell_solver_universe_T3.py rhs + docstring):
  phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + sigma,  sigma = (e^{2phi}/4) U'(rho)
  Phi   = Z rho^2 phi'
  H     = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho)
"""
import sympy as sp

r, Z, eps = sp.symbols("r Z varepsilon", positive=True)
phi = sp.Function("phi")(r)
rho = sp.Function("rho")(r)
U = sp.Function("U")

phip, rhop = phi.diff(r), rho.diff(r)

phipp_rhs = 4*sp.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
sigma = sp.exp(2*phi)/4 * U(rho).diff(rho)
rhopp_rhs = 2*phip*rhop - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*phip**2 + sigma

subs_eom = {phi.diff(r,2): phipp_rhs, rho.diff(r,2): rhopp_rhs}

print("="*80)
print("[0] H conservation on-shell (needed for B to hold at the seal given H(core)=0)")
H = sp.Rational(1,2)*Z*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 - 2 + U(rho)
dH = H.diff(r).subs(subs_eom)
dH = sp.simplify(dH)
print("   dH/dr on-shell =", dH, " -> PASS" if dH == 0 else " -> FAIL")

print("="*80)
print("[0b] Flux law Phi' = 4 e^{-2phi} rho'^2 (used implicitly by Claim A: Phi>=0 monotone)")
Phi = Z*rho**2*phip
dPhi = sp.simplify(Phi.diff(r).subs(subs_eom) - 4*sp.exp(-2*phi)*rhop**2)
print("   Phi' - 4e^{-2phi}rho'^2 =", dPhi, " -> PASS" if dPhi == 0 else " -> FAIL")

print("="*80)
print("[A] phi' = Phi/(Z rho^2) identity (definitional) and the bracket relation")
resA = sp.simplify(phip - Phi/(Z*rho**2))
print("   phi' - Phi/(Z rho^2) =", resA, " -> algebraic identity" if resA == 0 else " -> FAIL")
# Delta_phi = int phi' dr = (1/Z) int Phi/rho^2 dr = (q/Z) int (Phi/q)/rho^2 dr, q != 0.
# CAS content is trivial; requirement list is stated in the report.

print("="*80)
print("[B] Seal energy identity: at rho'_s=0, phi_s=0, H=0 ->  U(rho_s) = 2 - q^2/(2 Z rho_s^2)")
rho_s, q_s, phip_s = sp.symbols("rho_s q phip_s", positive=True)
H_seal = sp.Rational(1,2)*Z*rho_s**2*phip_s**2 - 2*sp.exp(-2*0)*0**2 - 2 + sp.Symbol("Us")
Us_from_H = sp.solve(sp.Eq(H_seal, 0), sp.Symbol("Us"))[0]
Us_sub = Us_from_H.subs(phip_s, q_s/(Z*rho_s**2))
target = 2 - q_s**2/(2*Z*rho_s**2)
print("   U(rho_s) from H=0 with q=Z rho_s^2 phi'_s :", sp.simplify(Us_sub))
print("   target 2 - q^2/(2Z rho_s^2) match:", sp.simplify(Us_sub - target) == 0)

print("="*80)
print("[C1] O(eps) expansion of the rho-EOM about rho = 1 + eps*u, phi background held")
u = sp.Function("u")(r)
dt, s1 = sp.symbols("deltatilde stilde1", real=True)      # U'(1+x) = 4 dt + 4 s1 x + O(x^2)
rho_lin = 1 + eps*u
Up_lin = 4*dt + 4*s1*(rho_lin - 1)                        # my absorbed form (factor 4 as in claim)
sigma_lin = sp.exp(2*phi)/4 * Up_lin
eom = rho_lin.diff(r,2) - (2*phip*rho_lin.diff(r)
                           - sp.Rational(1,4)*Z*rho_lin*sp.exp(2*phi)*phip**2 + sigma_lin)
eom = sp.expand(eom)
c0 = eom.coeff(eps, 0)
c1 = eom.coeff(eps, 1)
c2 = sp.simplify(eom - c0 - eps*c1)
print("   O(1) residual (must be treated as source; vanishes iff dt = (Z/4)phi'^2):")
print("      ", sp.simplify(c0))
print("   O(eps) equation (=0):")
print("      ", sp.collect(sp.expand(c1), [u.diff(r,2), u.diff(r), u]))
print("   higher-order remainder:", c2, "(exact: U' truncated at linear)")
# put in claimed form  u'' - 2 phi' u' + k^2 u = source
k2 = -sp.simplify(c1.coeff(u) )   # c1 = u'' - 2phi'u' - (coef)u  form check
lhs = u.diff(r,2) - 2*phip*u.diff(r)
resform = sp.simplify(c1 - (lhs - (2*phip*u.diff(r) - 2*phip*u.diff(r))) )
uppc = c1.coeff(u.diff(r,2)); upc = c1.coeff(u.diff(r)); uc = c1.coeff(u)
print("   coefficients:  u'':", uppc, "   u':", sp.simplify(upc), "   u:", sp.simplify(uc))
print("   => k^2(r) = -[u-coeff] =", sp.simplify(-uc))
print("   => full O(eps) balance: u'' - 2phi'u' + k^2 u = -(1/eps)*O(1)residual =")
print("      source S(r) =", sp.simplify(-c0), " /eps   (S = e^{2phi}[ (Z/4)phi'^2 - dt ] ... sign check below)")
print("      -c0 =", sp.simplify(-c0))

print("="*80)
print("[C2] substitution u = e^{phi} w : is the u' term eliminated IDENTICALLY?")
w = sp.Function("w")(r)
S = sp.Function("S")(r)
k2s = sp.Function("k2")(r)
expr = (sp.exp(phi)*w).diff(r,2) - 2*phip*(sp.exp(phi)*w).diff(r) + k2s*(sp.exp(phi)*w)
expr = sp.expand(expr/sp.exp(phi))
expr = sp.collect(sp.simplify(expr), [w.diff(r,2), w.diff(r), w])
print("   e^{-phi} * [LHS(u=e^phi w)] =", expr)
wp_coeff = sp.simplify(expr.coeff(w.diff(r)))
print("   coefficient of w' :", wp_coeff, " -> ELIMINATED" if wp_coeff == 0 else " -> NOT eliminated")
w_coeff = sp.simplify(expr.coeff(w))
print("   coefficient of w  :", w_coeff)
print("   => w-equation:  w'' + [k^2 + phi'' - phi'^2] w = e^{-phi} S")

print("="*80)
print("[C1-num] risefall slice m=3: dt, s1 in my normalization U'(1+x)=4dt+4s1 x")
a, m, x = sp.symbols("a m x", positive=True)
Urf = 2*(1+x)**m*sp.exp(-a*((1+x)**2 - 1))
Uprf = sp.diff(Urf, x)
dt_val = sp.simplify(Uprf.subs(x, 0)/4)
s1_val = sp.simplify(sp.diff(Uprf, x).subs(x, 0)/4)
print("   dt =", dt_val, "   [m=3:", sp.simplify(dt_val.subs(m,3)), "; at a=1.5(1-d): dt = (3/2)d ]")
print("   s1 =", sp.factor(s1_val), "  [m=3, a=3/2:", sp.simplify(s1_val.subs({m:3,a:sp.Rational(3,2)})), "]")
dcheck = sp.simplify(dt_val.subs({m: 3, a: sp.Rational(3,2)*(1-sp.Symbol('d'))}))
print("   dt(m=3, a=1.5(1-d)) =", dcheck)
