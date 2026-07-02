"""bv9_cas.py -- blind verifier CAS re-derivation of D1/D2/D3/D5 + family s1 formulas.
Own derivation; compares against the claimed coefficients. No claim text imported.
"""
import sympy as sp

ok = lambda name, expr: print(f"[{'PASS' if expr else 'FAIL'}] {name}")

# ---------------------------------------------------------------- symbols
r, phi, Z, C, s1, xc, x, Q, eps = sp.symbols('r phi Z C s1 x_c x Q epsilon', positive=True)
# s1 here denotes |s~1| (positive); the physical s~1 = -s1 in the oscillatory families.

print("="*70)
print("D1: cycle-average flux law")
print("="*70)
# u = a cos(theta), theta' = k, a = C e^{phi/2} Q^{-1/4}, k^2 = e^{2phi} Q
# <u'^2> over a cycle with slowly varying a,k:  u' ~= -a k sin(theta)
th = sp.symbols('theta')
a_env, k = sp.symbols('a k', positive=True)
mean_up2 = sp.integrate((a_env*k*sp.sin(th))**2, (th, 0, 2*sp.pi))/(2*sp.pi)
ok("<u'^2> = a^2 k^2 / 2", sp.simplify(mean_up2 - a_env**2*k**2/2) == 0)

# <Phi'> = 4 e^{-2phi} <u'^2>, with a^2 = C^2 e^{phi} Q^{-1/2}, k^2 = e^{2phi} Q
a2 = C**2*sp.exp(phi)/sp.sqrt(Q)
k2 = sp.exp(2*phi)*Q
mean_Phip = 4*sp.exp(-2*phi)*(a2*k2/2)
ok("<Phi'> = 2 C^2 e^{phi} sqrt(Q)", sp.simplify(mean_Phip - 2*C**2*sp.exp(phi)*sp.sqrt(Q)) == 0)

# d(Phi^2)/dphi = 2 Phi Phi' / phi' ; phi' = Phi/(Z rho^2), rho ~= 1  =>  = 2 Z Phi'
# => <d(Phi^2)/dphi> = 4 Z C^2 sqrt(Q) e^{phi};  with Q ~= s1 (=|s~1|):
claimed_D1 = 4*Z*C**2*sp.sqrt(s1)*sp.exp(phi)
mine_D1 = 2*Z*mean_Phip.subs(Q, s1)
ok("<d(Phi^2)/dphi> = 4 Z C^2 sqrt|s1| e^{phi}", sp.simplify(mine_D1 - claimed_D1) == 0)

# integrate from phi_c (Phi=0 there, inner fold phi'(0)=0) to phi:
Phi2 = sp.integrate(claimed_D1, phi)  # = 4 Z C^2 sqrt(s1) e^phi + const
Phi2_of_phi = 4*Z*C**2*sp.sqrt(s1)*(sp.exp(phi) - xc)
ok("Phi^2(phi) = 4 Z C^2 sqrt|s1| (e^phi - x_c)  [antiderivative check]",
   sp.simplify(sp.diff(Phi2_of_phi, phi) - claimed_D1) == 0 and
   Phi2_of_phi.subs(phi, sp.log(xc)) == 0)

print("="*70)
print("D2: phase integral Theta")
print("="*70)
# Theta = int k dr; dr = Z dphi / Phi (rho~=1); k = e^phi sqrt(Q) ~= e^phi sqrt(s1)
Phi_of_phi = sp.sqrt(Phi2_of_phi)          # 2 C sqrt(Z) s1^{1/4} sqrt(e^phi - x_c)
integrand = sp.exp(phi)*sp.sqrt(s1) * Z / Phi_of_phi
# substitute x = e^phi -> dphi = dx/x
integrand_x = integrand.subs(sp.exp(phi), x) / x
Theta_mine = sp.integrate(integrand_x, (x, xc, 1))
Theta_claim = sp.sqrt(Z)*s1**sp.Rational(1,4)*sp.sqrt(1-xc)/C
print("  Theta (mine, symbolic) =", sp.simplify(Theta_mine))
ok("Theta = sqrt(Z) |s1|^{1/4} sqrt(1-x_c) / C", sp.simplify(Theta_mine - Theta_claim) == 0)

print("="*70)
print("D3: double closure R1/R2 + exact-identity consistency")
print("="*70)
Qs = sp.symbols('Q_s', positive=True)
q = Phi_of_phi.subs(phi, 0)                 # q = Phi(phi=0)
q_expected = 2*C*sp.sqrt(Z)*s1**sp.Rational(1,4)*sp.sqrt(1-xc)
ok("q = 2 C sqrt(Z) |s1|^{1/4} sqrt(1-x_c)", sp.simplify(q - q_expected) == 0)

a_seal = C/Qs**sp.Rational(1,4)             # a(phi=0) = C e^{0/2} Q_s^{-1/4}
# R1: eliminate C via q
C_from_q = sp.solve(sp.Eq(sp.Symbol('q_v', positive=True), q_expected), C)[0]
R1_mine = a_seal.subs(C, C_from_q)
qv = sp.Symbol('q_v', positive=True)
R1_claim = qv/(2*sp.sqrt(Z*(1-xc))*(s1*Qs)**sp.Rational(1,4))
ok("R1: a_seal = q/[2 sqrt(Z(1-x_c)) (|s1| Q_s)^{1/4}]", sp.simplify(R1_mine - R1_claim) == 0)

# R2: eliminate C via Theta
Th = sp.Symbol('Theta', positive=True)
C_from_Th = sp.solve(sp.Eq(Th, Theta_claim), C)[0]
R2_mine = a_seal.subs(C, C_from_Th)
R2_claim = sp.sqrt(Z*(1-xc))*(s1/Qs)**sp.Rational(1,4)/Th
ok("R2: a_seal = sqrt(Z(1-x_c)) (|s1|/Q_s)^{1/4} / Theta", sp.simplify(R2_mine - R2_claim) == 0)

# Consistency: exact seal identity U(rho_s) = 2 - q^2/(2 Z rho_s^2), expand about rho_s = 1+u_s:
# U(1+u) = 2 + 4*dt*u + 2*s~1*u^2 (U'(1)=4dt, U''(1)=4 s~1 = -4 s1)
u_s, dt = sp.symbols('u_s delta_t', real=True)
lhs = 2 + 4*dt*u_s - 2*s1*u_s**2
rhs = 2 - qv**2/(2*Z*(1+u_s)**2)
# leading order (dt -> 0, rho_s -> 1): 2 s1 u_s^2 = q^2/(2Z)  =>  |u_s| = q/(2 sqrt(Z s1))
us_lead = sp.sqrt(qv**2/(4*Z*s1))
ok("exact-identity O(eps): |u_s| = q / (2 sqrt(Z |s1|))",
   sp.simplify(sp.expand((2 - lhs.subs(dt,0)) - qv**2/(2*Z)).subs(u_s, us_lead)) == 0)
# R1 with x_c -> 0, Q_s -> s1 must equal that:
R1_limit = R1_claim.subs([(xc, 0), (Qs, s1)])
ok("R1(x_c->0, Q_s->|s1|) == q/(2 sqrt(Z |s1|))  [the U''-structure check]",
   sp.simplify(R1_limit - qv/(2*sp.sqrt(Z*s1))) == 0)

# cancellation: q at fixed (Z, Theta):  q = 2 Z sqrt(s1) (1-x_c) / Theta
q_at_fixed_Theta = q_expected.subs(C, C_from_Th)
ok("q = 2 Z sqrt|s1| (1-x_c) / Theta  (q prop sqrt|s1| at fixed Z,N,theta0)",
   sp.simplify(q_at_fixed_Theta - 2*Z*sp.sqrt(s1)*(1-xc)/Th) == 0)

print("="*70)
print("D5a: averaged interior e^{-phi/2} = sqrt(1101) cos(kappa sqrt(x_c) r)")
print("="*70)
# slow system: phi'^2 = Phi^2/(Z rho^2)^2 ~= Phi^2/Z^2 = (4 C^2 sqrt(s1)/Z)(e^phi - x_c)
# define beta^2 = 4 C^2 sqrt(s1)/Z ; try v = e^{-phi/2} = cos(w r)/sqrt(x_c)
beta, kap = sp.symbols('beta kappa', positive=True)
w = sp.symbols('omega', positive=True)
v = sp.cos(w*r)/sp.sqrt(xc)
phi_of_r = -2*sp.log(v)
resid = sp.diff(phi_of_r, r)**2 - beta**2*(sp.exp(phi_of_r) - xc)
resid = sp.simplify(resid.rewrite(sp.cos))
print("  residual(w generic) =", sp.simplify(resid))
resid_at = sp.simplify(resid.subs(w, beta*sp.sqrt(xc)/2))
ok("solves slow system iff omega = (beta/2) sqrt(x_c), i.e. kappa = beta/2 = C|s1|^{1/4}/sqrt(Z)",
   resid_at == 0)
# and kappa relation to Theta: beta/2 = C s1^{1/4}/sqrt(Z)
ok("kappa = C |s1|^{1/4} / sqrt(Z)",
   sp.simplify(sp.sqrt(4*C**2*sp.sqrt(s1)/Z)/2 - C*s1**sp.Rational(1,4)/sp.sqrt(Z)) == 0)

print("="*70)
print("D5b: universal phase-coordinate ODE + z_c")
print("="*70)
# From my derivation: u_zz - (phi'/k) u_z + u = src/k^2, and with the averaged interior,
# phi'/k = 2 zeta / (zeta^2 + s^2), s = sqrt(s1) sqrt(x_c) / kappa.
# Verify symbolically via w-parameterization:
kapv = sp.symbols('kappa_v', positive=True)
wv = sp.symbols('w_v')                      # w = kappa sqrt(x_c) r
T = sp.tan(wv)
phi_w = sp.log(xc) - 2*sp.log(sp.cos(wv))   # e^phi = x_c sec^2 w
dphidr = sp.diff(phi_w, wv)*kapv*sp.sqrt(xc)         # dw/dr = kappa sqrt(x_c)
k_of_w = sp.sqrt(s1)*sp.exp(phi_w)
zeta = sp.sqrt(s1)*xc/(kapv*sp.sqrt(xc))*T           # int k dr = sqrt(s1) x_c tan(w)/(kappa sqrt(x_c))
s_par = sp.sqrt(s1)*sp.sqrt(xc)/kapv
expr = dphidr/k_of_w - 2*zeta/(zeta**2 + s_par**2)
ok("phi'/k == 2 zeta/(zeta^2 + s^2) with s = sqrt|s1| sqrt(x_c)/kappa",
   sp.simplify(sp.trigsimp(expr)) == 0)
# z_c claim: s = Theta sqrt(x_c). Mine: s = sqrt(s1) sqrt(xc)/kappa, kappa = C s1^{1/4}/sqrt(Z)
s_mine = (sp.sqrt(s1)*sp.sqrt(xc)/(C*s1**sp.Rational(1,4)/sp.sqrt(Z)))
zc_claim = Theta_claim*sp.sqrt(xc)
ratio = sp.simplify(s_mine/zc_claim)
print("  s_mine / (Theta sqrt(x_c)) =", ratio, " (claim exact would be 1)")
ok("z_c = Theta sqrt(x_c) up to factor 1/sqrt(1-x_c) [0.05%% at x_c=1/1101]",
   sp.simplify(ratio - 1/sp.sqrt(1-xc)) == 0)

# tail ODE solutions
z = sp.symbols('z', positive=True)
ode = lambda g: sp.diff(g, z, 2) - (2/z)*sp.diff(g, z) + g
uJ = sp.sin(z) - z*sp.cos(z)
uY = sp.cos(z) + z*sp.sin(z)
ok("u_J = sin z - z cos z solves tail ODE exactly", sp.simplify(ode(uJ)) == 0)
ok("u_Y = cos z + z sin z solves tail ODE exactly", sp.simplify(ode(uY)) == 0)
ok("u_J' = z sin z  (rho'-nodes at z = n pi, pi-spaced)",
   sp.simplify(sp.diff(uJ, z) - z*sp.sin(z)) == 0)
ok("u_Y' = z cos z  (rho'-nodes at z = (n+1/2) pi, pi-spaced)",
   sp.simplify(sp.diff(uY, z) - z*sp.cos(z)) == 0)
# also the FULL ODE with the 2z/(z^2+zc^2) coefficient: check tail solutions are NOT exact
# for finite z_c (so the pi-spacing is asymptotic only)
zcv = sp.symbols('z_c0', positive=True)
ode_full = lambda g: sp.diff(g, z, 2) - (2*z/(z**2 + zcv**2))*sp.diff(g, z) + g
res_full = sp.simplify(ode_full(uJ))
print("  full-ODE residual of u_J (should be nonzero, O(z_c^2)):", sp.simplify(res_full))

print("="*70)
print("family s~1 = U''(1)/4 formulas (own sympy derivation)")
print("="*70)
rho, m_, a_, k_, b_ = sp.symbols('rho m a k b', positive=True)
U_A1 = 2*rho**m_*sp.exp(-a_*(rho**2 - 1))
U_A2 = 2*rho**2*sp.exp(-a_*(rho**k_ - 1))
U_A3 = 2*rho**2*(1 + b_)/(1 + b_*rho**4)
for name, U, par in (("A1", U_A1, (m_, a_)), ("A2", U_A2, (k_, a_)), ("A3", U_A3, (b_,))):
    Up1 = sp.simplify(sp.diff(U, rho).subs(rho, 1))
    Upp1 = sp.simplify(sp.diff(U, rho, 2).subs(rho, 1))
    print(f"  {name}: U'(1) = {Up1}   U''(1) = {sp.expand(Upp1)}   s~1 = {sp.simplify(Upp1/4)}")
# stuck values
print("  A1 stuck a=m/2: s~1 =", sp.simplify((sp.diff(U_A1, rho, 2).subs(rho,1)/4).subs(a_, m_/2)))
print("  A2 stuck a=2/k: s~1 =", sp.simplify((sp.diff(U_A2, rho, 2).subs(rho,1)/4).subs(a_, 2/k_)))
print("  A3 stuck b=1  : s~1 =", sp.simplify((sp.diff(U_A3, rho, 2).subs(rho,1)/4).subs(b_, 1)))
