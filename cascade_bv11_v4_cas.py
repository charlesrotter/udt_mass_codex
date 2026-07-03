"""bv11 V4: CAS spot checks on the breaking ledger (u = ln rho variables)."""
import sympy as sp

u, c, lam, q = sp.symbols("u c lambda q", real=True)
Z = sp.symbols("Z", positive=True)
r = sp.symbols("r")
phi = sp.Function("phi")(r)
uf = sp.Function("u")(r)
v = sp.Function("v")

print("== V4(i): kinetic-term matching ==")
# Kinetic terms of the reduced action in (u=ln rho, phi):
#   K1 = (Z/2) e^{2u} phi'^2 ,  K2 = 2 e^{2u-2phi} u'^2   (from H, rho = e^u)
# sanity: (Z/2) rho^2 phi'^2 = (Z/2) e^{2u} phi'^2 ; 2 e^{-2phi} rho'^2 = 2 e^{2u-2phi} u'^2
rho = sp.exp(uf)
chk0 = sp.simplify(2*sp.exp(-2*phi)*sp.diff(rho, r)**2 - 2*sp.exp(2*uf - 2*phi)*sp.diff(uf, r)**2)
print("  kinetic-term rewrite in u: residual =", chk0)

# Map: u -> v(u), phi -> phi + c, drt = mu(u) dr, action ratio lam (constant).
# K1: e^{2v} (phi'/mu)^2 * mu = lam e^{2u} phi'^2   =>  mu = e^{2v-2u}/lam
# K2: e^{2v-2(phi+c)} (v'(u) u'/mu)^2 * mu = lam e^{2u-2phi} u'^2
mu = sp.exp(2*v(u) - 2*u)/lam
lhsK2 = sp.exp(2*v(u) - 2*phi - 2*c) * v(u).diff(u)**2 / mu
rhsK2 = lam*sp.exp(2*u - 2*phi)
cond = sp.simplify(lhsK2/rhsK2)          # must equal 1  =>  v'^2 = e^{2c}
print("  K2/K1 compatibility  =>", sp.simplify(sp.Eq(cond, 1)), "  i.e. v'(u)^2 = e^{2c}")
sols = sp.dsolve(sp.Eq(v(u).diff(u)**2, sp.exp(2*c)), v(u))
print("  general solution:", sols)
# Pins: phi-anchor (phi(r_s)=0 and phi_c both pinned) => c=0; nontrivial branch => v'=-1;
# cylinder fixed point v(0)=0 => v=-u; mu(0)=1 => lam=1 => mu = e^{-4u}.
vv = -u
mu_pinned = (sp.exp(2*vv - 2*u)/lam).subs(lam, 1)
print("  pinned: v=-u, mu =", mu_pinned)
# Phi invariance: Phi~ = Z e^{2v} dphi~/drt = Z e^{-2u} (phi'/mu) = Z e^{2u} phi'
Phi_t = Z*sp.exp(2*vv)*(1/mu_pinned)
print("  Phi~/Phi = Z e^{2v} (phi'/mu) / (Z e^{2u} phi') =",
      sp.simplify(Phi_t/(Z*sp.exp(2*u))))

print("\n== V4(ii): mismatch density leading terms (m=3) ==")
dt = sp.symbols("deltatilde", real=True)
m = sp.Integer(3)
a = sp.Rational(3, 2) - dt
Ut = 2*sp.exp(m*u)*sp.exp(-a*(sp.exp(2*u) - 1))          # U(e^u), a = 3/2 - dt
Ut_tw = Ut.subs([(u, -u), (dt, -dt)], simultaneous=True) # twin: u->-u, dt->-dt
Delta = (2 - Ut_tw)*sp.exp(-4*u) - (2 - Ut)
ser = sp.series(Delta, u, 0, 5).removeO().expand()
poly = sp.Poly(ser, u)
for k in range(0, 5):
    print(f"  u^{k} coeff:", sp.simplify(poly.coeff_monomial(u**k) if k else poly.coeff_monomial(1)))
claim2 = 24*dt
claim3 = 32*dt**2 - 48*dt - 32*m*sp.Rational(1, 3)*1  # 32 dt^2 - 48 dt - 32 m/3
print("  claim u^2:", claim2, " match:", sp.simplify(poly.coeff_monomial(u**2) - claim2) == 0)
print("  claim u^3:", sp.expand(claim3), " match:",
      sp.simplify(poly.coeff_monomial(u**3) - claim3) == 0)
