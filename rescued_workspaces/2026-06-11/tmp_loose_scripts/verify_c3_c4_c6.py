"""Blind adversarial verification: C3 (invariant family / DtN offset),
C4 (L0 identity + weld operator mapping), C6 (no-gos and signs).
Independent: sympy symbolic + mpmath 40-digit ODE shooting (own mesh,
own Frobenius seed). Verifier 2026-06-11."""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
PASS = FAIL = 0
def check(label, ok):
    global PASS, FAIL
    PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL"), "|", label)

y, q, lam, mu, nu, n, eps = sp.symbols('y q lam mu nu n eps', positive=True)

# ---------- C3a: Bessel reduction, symbolic ----------
tau = 2*sp.sqrt(lam)/q
u = y**sp.Rational(-1,2) * sp.besseli(nu, tau*y**(q/2))
resid = sp.diff(y**2*sp.diff(u, y), y) - (lam*y**q + mu)*u
resid = resid.subs(mu, (q**2*nu**2 - 1)/4)   # claimed nu = sqrt(1+4mu)/q
resid_s = sp.besselsimp(sp.expand_func(sp.simplify(resid.doit())))
# fallback: 30-digit numeric residual at random irrational-ish points
fres = sp.lambdify((y, q, lam, nu), resid.doit(), modules='mpmath')
pts = [(mp.mpf('0.731'), mp.mpf('0.4'), mp.mpf('1.7'), mp.mpf('2.3')),
       (mp.mpf('1.42'), mp.mpf(1)/3, mp.mpf(2), mp.sqrt(17)),
       (mp.mpf('0.2'), mp.mpf(1)/3, mp.mpf('0.5'), mp.mpf(5)),
       (mp.mpf('2.5'), mp.mpf('0.27'), mp.mpf('11'), mp.mpf('1.1'))]
num_ok = all(abs(fres(*p)) < mp.mpf('1e-25') for p in pts)
check("C3a: u = y^{-1/2} I_nu(2 sqrt(lam)/q * y^{q/2}) solves "
      "(y^2 u')' = (lam y^q + mu) u with nu = sqrt(1+4mu)/q "
      "(symbolic-or-30-digit residual at 4 generic (y,q,lam,nu) points)",
      resid_s == 0 or num_ok)

# ---------- C3b: nu^2 = 17 - 8n at q = 1/3 ----------
nu2 = (1 + 4*(1-n)*q*(1-q))/q**2
nu2_q13 = sp.simplify(nu2.subs(q, sp.Rational(1,3)))
check("C3b: nu^2 = (1+4(1-n)q(1-q))/q^2 = 17 - 8n at q=1/3; "
      "n=1->3, n=0->sqrt17, n=-1->5",
      sp.simplify(nu2_q13 - (17 - 8*n)) == 0
      and nu2_q13.subs(n, 1) == 9 and nu2_q13.subs(n, 0) == 17
      and nu2_q13.subs(n, -1) == 25)

# mu values of the family: mu = (1-n)q(1-q); check vs nu relation
check("C3b': mu(n) = (1-n)q(1-q) consistent with nu(n): "
      "(q^2 nu^2 - 1)/4 = (1-n)q(1-q) identically",
      sp.simplify((q**2*nu2 - 1)/4 - (1-n)*q*(1-q)) == 0)

# ---------- C3c: DtN offset, symbolic via recurrence ----------
# u'/u at y=1 for u = y^{-1/2} I_nu(tau0 y^{q/2}):
#   = -1/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0)
# with I'_nu = I_{nu+1} + (nu/z) I_nu :
#   = sqrt(lam) I_{nu+1}/I_nu + (q nu - 1)/2     [since q tau0/2 = sqrt(lam)]
z = sp.symbols('z', positive=True)
rec = sp.besselsimp(sp.expand_func(sp.diff(sp.besseli(nu, z), z))
                    - (sp.besseli(nu+1, z) + (nu/z)*sp.besseli(nu, z)))
rec_num = all(abs(mp.diff(lambda x: mp.besseli(nv, x), zv)
                  - (mp.besseli(nv+1, zv) + nv/zv*mp.besseli(nv, zv)))
              < mp.mpf('1e-30')
              for nv in [mp.mpf('2.3'), mp.sqrt(17), mp.mpf(5)]
              for zv in [mp.mpf('0.7'), mp.mpf('8.49')])
check("C3c-i: recurrence I'_nu(z) = I_{nu+1}(z) + (nu/z) I_nu(z) "
      "(symbolic-or-30-digit at 6 points)", rec == 0 or rec_num)
up_over_u = sp.simplify(sp.diff(u, y)/u).subs(y, 1)
target = sp.sqrt(lam)*sp.besseli(nu+1, tau)/sp.besseli(nu, tau) + (q*nu-1)/2
check("C3c-ii: u'(1)/u(1) = sqrt(lam) I_{nu+1}(tau0)/I_nu(tau0) + (q nu-1)/2 "
      "exactly (the claimed D_nu offset), symbolic",
      sp.simplify(sp.expand_func(up_over_u - target)) == 0)

# ---------- C3d: independent ODE shooting (own Frobenius seed) ----------
def D_formula(nu_v, lam_v, q_v=mp.mpf(1)/3):
    t0 = 2*mp.sqrt(lam_v)/q_v
    return (mp.sqrt(lam_v)*mp.besseli(nu_v+1, t0)/mp.besseli(nu_v, t0)
            + (q_v*nu_v - 1)/2)

def D_shoot(nu_v, lam_v, q_v=mp.mpf(1)/3, y0=mp.mpf('1e-6')):
    """Solve (y^2 u')' = (lam y^q + mu) u from Frobenius seed
    u ~ y^alpha (1 + lam y^q/(q(2 alpha + 1 + q) ... )), alpha = (-1+q nu)/2,
    Friedrichs branch; return u'(1)/u(1)."""
    mu_v = (q_v**2*nu_v**2 - 1)/4
    al = (-1 + q_v*nu_v)/2
    # next Frobenius coefficient: u = y^al (1 + c1 y^q), plug in:
    # (al+q)(al+q+1) c1 - mu c1 = lam  => c1 = lam/((al+q)(al+q+1)-mu)
    c1 = lam_v/((al+q_v)*(al+q_v+1) - mu_v)
    u0 = y0**al*(1 + c1*y0**q_v)
    du0 = al*y0**(al-1)*(1+c1*y0**q_v) + y0**al*c1*q_v*y0**(q_v-1)
    def rhs(t, Y):
        uu, vv = Y  # v = y^2 u'
        return [vv/t**2, (lam_v*t**q_v + mu_v)*uu]
    sol = mp.odefun(rhs, y0, [u0, y0**2*du0], tol=mp.mpf('1e-30'))
    uf, vf = sol(mp.mpf(1))
    return vf/uf   # y=1: u'/u

for nu_v, name in [(mp.mpf(3), 'nu=3 (n=1)'),
                   (mp.sqrt(17), 'nu=sqrt17 (n=0)'),
                   (mp.mpf(5), 'nu=5 (n=-1)')]:
    for lam_v in [mp.mpf(1)/2, mp.mpf(2)]:
        a_ = D_shoot(nu_v, lam_v); b_ = D_formula(nu_v, lam_v)
        # an offset error (e.g. missing/extra (q nu - 1)/2 or nu/tau term)
        # would show at O(0.1); agreement to 1e-10 decisively excludes it
        check(f"C3d: ODE shooting vs offset formula, {name}, lam={float(lam_v)}: "
              f"|diff| = {mp.nstr(abs(a_-b_), 3)}", abs(a_-b_) < mp.mpf('1e-10'))

# banked cross-anchor: D_B(2) = 0.925083523113 (panel doc, nu=3) — offset 0
check("C3e: banked anchor D_B(2)=0.925083523113 reproduced by formula "
      "(zero offset at nu = 1/q = 3)",
      abs(D_formula(mp.mpf(3), mp.mpf(2)) - mp.mpf('0.925083523113'))
      < mp.mpf('1e-12'))

# ---------- C4a: L0 identity ----------
# banked: L0 = -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0), nu=sqrt17
# claim:  L0(lam) = D_sqrt17(lam) + q
qv = mp.mpf(1)/3
def L0_banked(lam_v):
    t0 = 2*mp.sqrt(lam_v)/qv
    nuv = mp.sqrt(17)
    Ip = (mp.besseli(nuv+1, t0) + nuv/t0*mp.besseli(nuv, t0))  # I'_nu
    return -(1-2*qv)/2 + (qv*t0/2)*Ip/mp.besseli(nuv, t0)
banked_vals = {2: '1.33835009', 6: '2.29931870', 12: '3.28396540'}
for lv, bv in banked_vals.items():
    l0 = L0_banked(mp.mpf(lv)); dq = D_formula(mp.sqrt(17), mp.mpf(lv)) + qv
    check(f"C4a: L0({lv}) = D_sqrt17({lv}) + 1/3 to 30+ digits "
          f"(|diff|={mp.nstr(abs(l0-dq),3)}); and matches banked {bv} "
          f"(L0={mp.nstr(l0, 10)})",
          abs(l0 - dq) < mp.mpf('1e-30') and abs(l0 - mp.mpf(bv)) < 1e-7)
# algebraic reason: -(1-2q)/2 = -1/2 + q; u'/u = -1/2 + (q tau0/2) I'/I;
# so L0 = u'/u + q = D_nu + q by C3c-ii.
L0_sym = -(1-2*q)/2 + (q*tau/2)*(sp.besseli(nu+1, tau)/sp.besseli(nu, tau)
                                 + nu/tau)
check("C4a': symbolic: L0 = D_nu(lam) + q for ALL q, lam, nu "
      "(pure I'->I_{nu+1} recurrence + (-1/2+q) split)",
      sp.simplify(L0_sym - (target + q)) == 0)

# ---------- C4b: weld operator mapping ----------
a = sp.Function('a')(y)   # delta-phi
uu = sp.Function('u')(y)
f0 = y**(-q); s_ = q*(1-q)/2; E0 = s_/y**2
weld = (sp.diff(y**2*f0**2*sp.diff(a, y), y) - 4*y**2*f0**2*E0*a
        - lam*f0*a)
weld_u = weld.subs(a, -uu/(2*f0)).doit()
targ = -(1/(2*y**q))*(sp.diff(y**2*sp.diff(uu, y), y)
                      - (lam*y**q + 2*s_)*uu)
check("C4b: banked weld static operator under dphi = -u/(2 f0) equals "
      "-(1/(2y^q))[(y^2 u')' - (lam y^q + 2s) u] EXACTLY (general q) "
      "=> mu = 2s = q(1-q) = the n=0 slot; nu = sqrt(1+4q(1-q))/q = sqrt17 "
      "at q=1/3", sp.simplify(weld_u - targ) == 0)
check("C4b': mu = 2s matches family mu(n)=(1-n)q(1-q) exactly at n=0",
      sp.simplify(2*s_ - (1-n)*q*(1-q)).subs(n, 0) == 0)

# ---------- C6a: volume element f-independence ----------
r, th, fE = sp.symbols('r theta f_E', positive=True)
g = sp.diag(-fE, 1/fE, r**2, r**2*sp.sin(th)**2)
check("C6a: -det g = r^4 sin^2(theta) exactly => sqrt(-g) = r^2 sin(theta) "
      "on 0<theta<pi, f-independent (g_tt g_rr = -1)",
      sp.simplify(-g.det() - r**4*sp.sin(th)**2) == 0
      and not (-g.det()).has(fE))

# ---------- C6b: Pi_f-channel pointwise identity ----------
h = sp.Function('h')(y); ff = sp.Function('f')(y)
lhs = h*y**2*sp.diff(ff, y)/2
rhs = sp.diff(h*y**2*ff/2, y) - sp.Rational(1,2)*sp.diff(h*y**2, y)*ff
check("C6b: h y^2 f'/2 = d/dy(h y^2 f/2) - (1/2)(h y^2)' f pointwise "
      "(Pi_f channel = f-linear + contact)", sp.simplify(lhs - rhs) == 0)

# ---------- C6c: n=1 halves the weld mass ----------
av = sp.Function('a')(y)
J = -s_*y**(-q)
src1 = J * f0*sp.exp(-2*eps*av)   # c_1 f with c_1 = J, f in phi-form
jet2_src = sp.expand(sp.series(src1, eps, 0, 3).removeO()).coeff(eps, 2)
check("C6c-i: n=1 source second jet in phi-form = -2 s f0^2 (dphi)^2 "
      "exactly", sp.simplify(jet2_src - (-2*s_*f0**2*av**2)) == 0)
# total L2 mass: bulk 4s y^{-2q} (C5b at phi0 collar) - 2s = 2s
# => operator mass -2s y^{-2q} = -4 r^2 f^2 E0_eff with E0_eff = s/(2 r^2)
E0_eff = sp.symbols('E0eff')
sol = sp.solve(sp.Eq(4*y**2*f0**2*E0_eff, (4*s_ - 2*s_)*y**(-2*q)), E0_eff)
check("C6c-ii: total n=1 mass (4s-2s) y^{-2q} = 4 r^2 f^2 E0_eff with "
      "E0_eff = s/(2 y^2) — exact halving", sp.simplify(sol[0]-s_/(2*y**2))==0)
# cross-check: the halved-E0 operator must map to mu = 0 (the n=1 / nu=3
# family), closing consistency with C3b:
weld_half = (sp.diff(y**2*f0**2*sp.diff(a, y), y)
             - 4*y**2*f0**2*(s_/(2*y**2))*a - lam*f0*a)
weld_half_u = sp.simplify(weld_half.subs(a, -uu/(2*f0)).doit()
                          + (1/(2*y**q))*(sp.diff(y**2*sp.diff(uu, y), y)
                                          - lam*y**q*uu))
check("C6c-iii: the E0_eff = s/2r^2 operator maps under dphi = -u/(2f0) to "
      "-(1/(2y^q))[(y^2 u')' - lam y^q u] => mu = 0, nu = 1/q = 3: exactly "
      "the n=1 family — halving claim consistent end-to-end",
      weld_half_u == 0)

# ---------- C6d: pointwise ordering D_3 < D_sqrt17 < D_5 ----------
for lam_v in [mp.mpf(1)/2, mp.mpf(2)]:
    d3 = D_formula(mp.mpf(3), lam_v)
    d17 = D_formula(mp.sqrt(17), lam_v)
    d5 = D_formula(mp.mpf(5), lam_v)
    check(f"C6d: lam={float(lam_v)}: D_3={mp.nstr(d3,10)} < "
          f"D_sqrt17={mp.nstr(d17,10)} < D_5={mp.nstr(d5,10)}",
          d3 < d17 < d5)

print(f"\nsubtotal: {PASS} PASS, {FAIL} FAIL")
