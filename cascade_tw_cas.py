"""tw_cas.py -- Task (a): the exact involution behind the twin ladder + its breaking, CAS.

Frame (banked): reduced Lagrangian in u = ln rho,
    L = e^{2u}[(Z/2) phi'^2 - 2 e^{-2phi} u'^2] + 2 - U(e^u),
risefall family at m:  U(rho) = 2 rho^m exp(-a(rho^2-1)),  dt := m/2 - a  (so a -> m-a is dt -> -dt).
Twin map (O(eps) shadow): T: (u, dt) -> (-u, -dt).
All series exact sympy; every truncation = explicit series order.
"""
import sympy as sp

u, dt, m, r = sp.symbols('u delta m r', real=True)
Z = sp.Symbol('Z', positive=True)
rho = sp.symbols('rho', positive=True)

a = m/2 - dt                                   # family parameter, dt = m/2 - a  (exact)
U = 2*rho**m*sp.exp(-a*(rho**2 - 1))           # risefall slice (banked, CHOSE)

print("="*100)
print("A1. Family derivatives at rho=1, exact polynomials in dt (parity split under dt -> -dt)")
print("="*100)
ders = {}
for k in range(1, 5):
    d = sp.simplify(sp.diff(U, rho, k).subs(rho, 1))
    d = sp.expand(d)
    ders[k] = d
    dodd = sp.expand((d - d.subs(dt, -dt))/2)
    dev  = sp.expand((d + d.subs(dt, -dt))/2)
    print(f"U^({k})(1) = {d}")
    print(f"   even part: {dev}")
    print(f"   odd  part: {dodd}")
st1 = sp.expand(ders[2]/4)
print("\ns1~ = U''(1)/4 =", st1, "   [expect 2dt^2 + dt - m; odd part = dt]")
assert sp.simplify(st1 - (2*dt**2 + dt - m)) == 0
print("check dt = U'(1)/4:", sp.simplify(ders[1]/4))

print()
print("="*100)
print("A2. chat3 = U'''(1)/(12|s1~|), chat4 = U''''(1)/(48|s1~|): exact series in dt about stuck pt")
print("="*100)
absst1 = -(st1)          # s1~ < 0 for small dt: |s1~| = m - dt - 2dt^2
c3 = ders[3]/(12*absst1)
c4 = ders[4]/(48*absst1)
c3s = sp.series(c3, dt, 0, 3).removeO()
c4s = sp.series(c4, dt, 0, 3).removeO()
print("chat3 =", sp.simplify(sp.expand(c3s)))
print("chat4 =", sp.simplify(sp.expand(c4s)))
c3_odd = sp.simplify(sp.expand((c3s - c3s.subs(dt, -dt))/2).coeff(dt, 1))
c4_odd = sp.simplify(sp.expand((c4s - c4s.subs(dt, -dt))/2).coeff(dt, 1))
print("d(chat3)/d(dt) at 0 =", c3_odd, "  -> m=3:", c3_odd.subs(m, 3))
print("d(chat4)/d(dt) at 0 =", c4_odd, "  -> m=3:", c4_odd.subs(m, 3))
# numeric check vs banked th2 table N=8 (dt=0.005875565, m=3): c3h=0.3222438, c4h=1.2504561
c3n = float(c3.subs({m: 3, dt: 0.005875565076078448}))
c4n = float(c4.subs({m: 3, dt: 0.005875565076078448}))
print(f"numeric at banked N=8 dt: chat3={c3n:.7f} (banked 0.3222438), chat4={c4n:.7f} (banked 1.2504561)")

print()
print("="*100)
print("A3. Potential twin mismatch  D(u,dt) = ln Ut(u,dt) - ln Ut(-u,-dt),  Ut(u)=U(e^u)  (exact series)")
print("="*100)
Ut = U.subs(rho, sp.exp(u))
lnU = sp.log(Ut/2)          # = m u - a (e^{2u}-1)
D = sp.expand(lnU - lnU.subs([(u, -u), (dt, -dt)], simultaneous=True))
Dser = sp.series(D, u, 0, 6).removeO()
print("D =", sp.expand(sp.simplify(Dser)))
print("   [expect 4*dt*u^2 - (4m/3)u^3 + (4dt/3)u^4 - (4m/15)u^5 ...; the u^3 term is dt-INDEPENDENT]")

print()
print("="*100)
print("A4. The UNIQUE kinetic/flux-exact extension and where it breaks")
print("="*100)
# Class: u -> v(u), phi -> phi + g, r -> rt with drt = mu(u) dr, action-matching L~ drt = L dr.
# phi-kinetic: (Z/2) e^{2v} (dphi/drt)^2 drt = (Z/2) e^{2v} phi'^2 / mu dr  => e^{2v}/mu = e^{2u}
# u-kinetic:   e^{2v} v_u^2 / mu = e^{2u}     => v_u^2 = 1 => v = -u (twin branch), mu = e^{-4u}.
vu = -u
mu_meas = sp.exp(-4*u)
print("forced: v = -u, mu = dr~/dr = e^{-4u};  check flux Phi~ = Z e^{2v} dphi/dr~ = Z e^{2v} phi'/mu:")
flux_ratio = sp.simplify(sp.exp(2*vu)/mu_meas / sp.exp(2*u))
print("   Phi~/Phi =", flux_ratio, "  [1 = flux EXACTLY invariant]")
# potential+curvature sector: mismatch density
#   Delta(u,dt) = [2 - Ut(-u,-dt)] e^{-4u} - [2 - Ut(u,dt)]
Ut_m = Ut.subs([(u, -u), (dt, -dt)], simultaneous=True)
Delta = sp.expand((2 - Ut_m)*mu_meas - (2 - Ut))
Dser2 = sp.series(Delta, u, 0, 5).removeO()
Dser2 = sp.expand(sp.simplify(Dser2))
print("Delta(u,dt) potential-sector mismatch density (exact series):")
print("  ", sp.collect(Dser2, u))
for k in range(0, 5):
    ck = sp.expand(Dser2.coeff(u, k))
    if ck != 0:
        print(f"   u^{k}: {sp.simplify(ck)}")
print("   [NOTE: no O(u^0), O(u^1) term <=> U(rho_c)=2 closure aligns potential top with curvature 2;")
print("    leading breaking O(dt u^2) and O(m u^3) -- CANNOT be removed in this class]")

print()
print("="*100)
print("A5. O(eps) equation term parity (x = rho-1; grading x~eps, dt~eps, phi'^2~eps)")
print("="*100)
x = sp.Function('x')(sp.Symbol('r'))
rr = sp.Symbol('r')
phip = sp.Function('phip')(rr)   # phi'
e2p = sp.Symbol('e2phi', positive=True)
# EOM: rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)
Upr = sp.diff(U, rho)
Upx = sp.series(Upr.subs(rho, 1 + sp.Symbol('X')), sp.Symbol('X'), 0, 3).removeO()
print("U'(1+X) =", sp.expand(Upx), "  [= 4dt + 4 s1~ X + (U'''/2) X^2 + ...]")
print("O(eps):  x'' - 2 phi' x' + k^2 x = S,  k^2 = e^{2phi}[(Z/4)phi'^2 - s1~],  S = e^{2phi}[dt - (Z/4)phi'^2]")
print("parity under T (x->-x, dt->-dt):")
print("  k^2:  -s1~ = m - dt - 2dt^2:  even part m-2dt^2 OK;  ODD part -dt  -> T-BREAKING at O(dt/m) rel.")
print("  S:    dt-part flips (twin-consistent);  -(Z/4)phi'^2 part T-EVEN -> T-BREAKING at O(eps) source level.")
print("  U''' X^2/2 quad term: even part (4m+24dt^2)/2 X^2 -> T-BREAKING at O(eps^2) in EOM;")
print("                        odd part -12m dt X^2 flips (twin-consistent).")

print()
print("="*100)
print("A6. Lemma-2 identity (task c backbone): dG/dphi = 2G - 2Z rho rho_phi [2(2-U) - rho U'] (EXACT)")
print("="*100)
# From EOMs + H=0: Phi' = 4 e^{-2phi} rho'^2, rho'^2 = e^{2phi} W/2, W = Phi^2/(2Z rho^2)+U-2
Phi_ = sp.Symbol('Phi')
rho_ = sp.Symbol('rhov', positive=True)
Uf = sp.Function('Uf')
W = Phi_**2/(2*Z*rho_**2) + Uf(rho_) - 2
G = Phi_**2 - 2*Z*rho_**2*(2 - Uf(rho_))
print("G - 2Z rho^2 W =", sp.simplify(sp.expand(G - 2*Z*rho_**2*W)), " [0 => G = 2Z rho^2 W]")
# phi-flow: dPhi^2/dphi = 2 Phi Phi'/phi' ; Phi' = 2W (exact, since Phi'=4e^{-2phi}rho'^2 = 2W); phi' = Phi/(Z rho^2)
dPhi2 = sp.simplify(2*Phi_*2*W/(Phi_/(Z*rho_**2)))
print("dPhi^2/dphi =", sp.simplify(dPhi2), " [= 4 Z rho^2 W = 2G]")
rho_phi = sp.Symbol('rho_phi')
dG = sp.expand(dPhi2 - 2*Z*sp.diff(rho_**2*(2 - Uf(rho_)), rho_)*rho_phi)
claim = sp.expand(2*G - 2*Z*rho_*rho_phi*(2*(2 - Uf(rho_)) - rho_*sp.Derivative(Uf(rho_), rho_)))
print("dG/dphi - claim =", sp.simplify(dG - claim), " [0 = identity verified]")

print()
print("="*100)
print("A7. Per-node quadrature: odd parts. P_half = pi*E*[2+15/16 c3^2-3/2 c3+3/4 c4] + pi*(3/2) c3 dhat")
print("="*100)
E_, dh_ = sp.symbols('E dhat')
Br = 2 + sp.Rational(15, 16)*c3s**2 - sp.Rational(3, 2)*c3s + sp.Rational(3, 4)*c4s
Br_odd = sp.expand((Br - Br.subs(dt, -dt))/2)
Br_odd_lin = sp.simplify(Br_odd.coeff(dt, 1))
print("d(Bracket)/d(dt)|_0 =", sp.simplify(Br_odd_lin), "  -> m=3:", sp.nsimplify(Br_odd_lin.subs(m, 3)),
      "=", float(Br_odd_lin.subs(m, 3)))
print("dhat = dt/|s1~|  (tilt of W/(2|s1~|) about cylinder; PURELY ODD in dt up to |s1~|(dt))")
print("off-channel theta0 term: (N+1)*(3/2)*chat3*dt/|s1~|  [flips ENTIRELY between twins]")
offN8 = 9*sp.Rational(3, 2)*c3*dt/absst1
offn = float(offN8.subs({m: 3, dt: 0.005875565076078448}))
print(f"numeric N=8 below: off = {offn:.7f} rad/pi ... = {offn:.7f} (banked off_pi = 0.0085371) ")

print()
print("="*100)
print("A8. Bottom system parity: gamma = 4 dt^2/(Z s1~^2 x_c^2) -- odd correction through s1~(dt)")
print("="*100)
gam_ratio = sp.simplify((st1.subs(dt, -dt)/st1)**2)
gr = sp.series(gam_ratio, dt, 0, 3).removeO()
print("gamma(+dt)/gamma(-dt) at equal |dt| = [s1~(-dt)/s1~(dt)]^2 =", sp.expand(gr))
print("  [= 1 + 4dt/m + O(dt^2): the bottom system is even in dt ONLY through gamma;")
print("   gamma itself carries a T-ODD relative correction 4dt/m from s1~'s odd part (the U''-family term).")
print("   The dropped phi'^2-source in the bottom ODE is T-EVEN (breaks oddness) at ~1% (banked ledger).]")

print()
print("="*100)
print("A9. Equal-N twin condition through the closure (gamma_A = gamma_B): exact relation")
print("="*100)
# |dt_A|/|s1(-|dt_A|)| = |dt_B|/|s1(+|dt_B|)|  -> solve for x=|dt_A| in series of b=|dt_B|
b, xx = sp.symbols('b x', positive=True)
s1p = m - b - 2*b**2      # |s1~| below at dt=+b
s1m = m + xx - 2*xx**2    # |s1~| above at dt=-x
k2, k3 = sp.symbols('k2 k3')
ans = b + k2*b**2 + k3*b**3
resid = sp.expand((ans*s1p - b*s1m.subs(xx, ans)))
sol2 = sp.solve(sp.expand(resid).coeff(b, 2), k2)[0]
sol3 = sp.solve(sp.expand(resid.subs(k2, sol2)).coeff(b, 3), k3)[0]
xser = sp.expand(b + sol2*b**2 + sp.simplify(sol3)*b**3)
print("|dt_A| =", xser, "  [expect b + 2b^2/m + ...]")
print("=> midpoint (a_A + a_B)/2 - m/2 = (|dt_A|-|dt_B|)/2 = b^2/m + O(b^3);  in d-units: Dd = d^2 (m=3)")
