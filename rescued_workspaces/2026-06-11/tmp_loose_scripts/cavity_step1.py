"""EXTERIOR-SOURCED CAVITY, step 1 (scratch, /tmp only):
(A) symbolic: nu(n) consistency x-form vs v-form, general (q,n)
(B) symbolic: mirror exterior = smooth odd continuation; E0 both sides;
    Delta phi' = 0; gamma_eff = (4-2n)(q/2 - p) general jump formula
(C) numeric: L0 = D_sqrt17 + q identity; screened thresholds
    D_3(lam)+q at lam=2,6; deficit factors vs gamma in {2q, q}
(D) screening-lift band: nu_ub from mu_eff <= 1.5e-3
"""
import sympy as sp
import mpmath as mp

PASS = 0; FAIL = 0
def check(label, ok):
    global PASS, FAIL
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    if ok: PASS += 1
    else: FAIL += 1

q, n, s, lam, x, p = sp.symbols('q n s lam x p', positive=True)
seff = q*(1-q)/2

# ---- (A) nu(n): x-form mass (4-2n)s vs v-form mass mu=(1-n)q(1-q) ----
# x-form indicial: a^2 + (1-2q)a - (4-2n)s = 0, disc_x = (1-2q)^2+4(4-2n)s
disc_x = sp.expand(((1-2*q)**2 + 4*(4-2*n)*seff))
# v-form: (y^2 v')' = mu v, indicial b(b+1)=mu, disc_v matched to nu:
disc_v = sp.expand(1 + 4*(1-n)*q*(1-q))
check("nu(n) consistency: x-form disc (1-2q)^2+4(4-2n)s == 1+4(1-n)q(1-q)"
      " (v-form), all q,n; nu = sqrt(1+4(1-n)q(1-q))/q",
      sp.simplify(disc_x - disc_v) == 0)
check("q=1/3 family: nu^2 = 17-8n (n=0: sqrt17, n=1: 3)",
      sp.simplify(disc_v.subs(q, sp.Rational(1,3))*9 - (17-8*n)) == 0)

# ---- (B) mirror exterior ----
# collar flow phi_xx + phi_x - 2 phi_x^2 = s with phi = (q/2) x solves it
phi_lin = q*x/2
res = sp.diff(phi_lin, x, 2) + sp.diff(phi_lin, x) - 2*sp.diff(phi_lin, x)**2
check("phi0 = (q/2)x solves phi_xx + phi_x - 2phi_x^2 = q(1-q)/2 on BOTH "
      "sides of x=0 (one global self-similar solution)",
      sp.simplify(res - seff) == 0)
# mirror map: phi_u(x) = -phi_m(-x). For phi_m = (q/2)x (x<0):
phi_m = q*x/2
phi_u = (-phi_m.subs(x, -x))
check("mirror canon map phi_univ(x) = -phi_matter(-x) reproduces (q/2)x "
      "exactly: the mirrored exterior IS the smooth continuation",
      sp.simplify(phi_u - q*x/2) == 0)
check("slope continuity: phi'(0+) = phi'(0-) = q/2 => Delta phi' = 0 "
      "(the banked kink Delta phi' = -q/2R was the VACUUM truncation)",
      sp.simplify(sp.diff(phi_u, x).subs(x, 0) - sp.Rational(1,2)*q) == 0)
# E0 on the exterior: phi0 = (q/2) ln(r/R), r>R: E0 = s/r^2 (same as int.)
r, R = sp.symbols('r R', positive=True)
phi0r = (q/2)*sp.log(r/R)
E0 = sp.diff(phi0r, r, 2) + 2*sp.diff(phi0r, r)/r - 2*sp.diff(phi0r, r)**2
check("exterior E0 = q(1-q)/(2 r^2) = s/r^2 > 0 (sourced medium, same "
      "supply both sides)", sp.simplify(E0 - seff/r**2) == 0)

# gamma_eff general jump formula: exterior slope p := R phi0'(R+)
# delta in E0: Delta phi' * delta(r-R), coefficient -(4-2n) r^2 f^2 in eq
uR, eps = sp.symbols('uR epsilon', positive=True)
dphi = (p - q/2)/R   # Delta phi' = (p - q/2)/R
delta_term = sp.integrate(-(4-2*n)*r**2*1*dphi*sp.DiracDelta(r-R)*uR,
                          (r, R-eps, R+eps))
# (r^2 f^2 u')' integrates to R^2 Delta u'; sum = 0:
du = sp.symbols('Deltauprime')
sol = sp.solve(sp.Eq(R**2*du + delta_term, 0), du)[0]
gamma_eff = sp.simplify(-sol*R/uR)
check("general shell strength: gamma_eff = -R Delta u'/u = "
      "(4-2n)(q/2 - p), p = R phi0'(R+)  [n=0,p=0 -> 2q banked; "
      "n=1,p=0 -> q; p=q/2 (mirror) -> 0 for ALL n]",
      sp.simplify(gamma_eff - (4-2*n)*(q/2 - p)) == 0
      and gamma_eff.subs({n: 0, p: 0}) == 2*q
      and gamma_eff.subs({n: 1, p: 0}) == q
      and sp.simplify(gamma_eff.subs(p, q/2)) == 0)

# ---- (C) numerics: thresholds ----
mp.mp.dps = 40
qb = mp.mpf(1)/3
def D_nu(nu, lam):
    t0 = 6*mp.sqrt(lam)   # tau0 = 2 sqrt(lam)/q at q=1/3
    return mp.sqrt(lam)*mp.besseli(nu+1, t0)/mp.besseli(nu, t0) \
        + (qb*nu - 1)/2
def L0_closed(nu, lam):
    t0 = 6*mp.sqrt(lam)
    Ip = (mp.besseli(nu-1, t0) + mp.besseli(nu+1, t0))/2
    return -(1-2*qb)/2 + (qb*t0/2)*Ip/mp.besseli(nu, t0)

nu17 = mp.sqrt(17)
for lamv, ref in ((2, mp.mpf('1.33835009')), (6, mp.mpf('2.29931870')),
                  (12, mp.mpf('3.28396540'))):
    a = L0_closed(nu17, lamv); b = D_nu(nu17, lamv) + qb
    check(f"identity L0(lam={lamv}) = D_sqrt17 + q  ({mp.nstr(a,10)}); "
          f"matches banked {mp.nstr(ref,9)}",
          abs(a-b) < mp.mpf('1e-35') and abs(a-ref) < mp.mpf('1e-7'))

g3 = {}
for lamv in (2, 6, 12):
    g3[lamv] = D_nu(3, lamv) + qb
check(f"screened static threshold gamma_c = D_3(2)+q = "
      f"{mp.nstr(g3[2],10)} (brief: 1.258417)",
      abs(g3[2] - mp.mpf('1.258417')) < mp.mpf('5e-7'))
print(f"   D_3(6)+q  = {mp.nstr(g3[6],10)}   D_3(12)+q = {mp.nstr(g3[12],10)}")

# deficits, vacuum exterior, no-flux BC (best case), two shell readings
for lamv in (2, 6):
    gc = g3[lamv]
    print(f"   lam={lamv}: gamma_c={mp.nstr(gc,9)};"
          f" deficit vs 2q={mp.nstr(gc/(2*qb),7)}x;"
          f" vs q (wholesale-screened shell)={mp.nstr(gc/qb,7)}x")
check("corrected deficit (bulk-screened-only shell gamma=2q, lam=2): "
      f"{mp.nstr(g3[2]/(2*qb),8)}x (was 2.0075x)",
      abs(g3[2]/(2*qb) - mp.mpf('1.88762')) < mp.mpf('1e-4'))

# ---- (D) lifting band ----
mu_ub = mp.mpf('1.5e-3')
nu_ub = mp.sqrt(1 + 4*mu_ub)/qb
band2 = D_nu(nu_ub, 2) + qb
band6 = D_nu(nu_ub, 6) + qb
print(f"   lifting band: nu_eff in [3, {mp.nstr(nu_ub,8)}]; "
      f"gamma_c(2) in [{mp.nstr(g3[2],9)}, {mp.nstr(band2,9)}] "
      f"(width {mp.nstr(band2-g3[2],3)}); "
      f"gamma_c(6) in [{mp.nstr(g3[6],9)}, {mp.nstr(band6,9)}]")
check("lifting band is tiny: gamma_c shift from mu_eff <= 1.5e-3 is "
      "< 2e-3 at lam=2 (threshold re-grade robust to the lift)",
      band2 - g3[2] < mp.mpf('2e-3'))

# monotonicity of D_nu in nu (ordering D_3 < D_sqrt17, pointwise)
check("ordering D_3(lam) < D_sqrt17(lam) at lam=2,6 (screening LOWERS "
      "the threshold)",
      all(D_nu(3, l) < D_nu(nu17, l) for l in (2, 6)))

print(f"\nSTEP1: {PASS} PASS / {FAIL} FAIL")
import sys; sys.exit(1 if FAIL else 0)
