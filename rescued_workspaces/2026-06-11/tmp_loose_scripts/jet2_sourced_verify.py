"""
Second jet of the FULL SOURCED system on the banked self-similar collar.
Scratch verification, 2026-06-11. No repo files touched.

Conventions (per unit solid angle, panel-verified rewrite):
  L_C1[f] = (1/4)[ y^2 f'^2 + lam * (delta f_ang)^2 / f ]   (collar y in (0,1])
  background f0 = y^-q, q symbolic (banked q = 1/3); phi0 = (q/2) ln y, f0 = exp(-2 phi0).
  s := q(1-q)/2  (banked source share; = 1/9 at q=1/3)

Source completion family (power slot):
  W_n(y,f) = c_n(y) f^n  with criticality  dW/df|_{f0} = J(y) = (1/2)(y^2 f0')' = -s y^-q
   => c_n = J f0^{1-n}/n  (n != 0);  n=0 means  W_0 = K(y) phi = -(K/2) ln f,  K = -2 f0 J = 2 s y^{-2q}.
  n=1  : f-slot (linear in f; zero 2nd jet in f-vars)
  n=0  : phi-slot (linear in phi; zero 2nd jet in phi-vars)
  n=-1 : 1/f-slot (the C1 angular term's own f-dependence; frozen angular-activation reading)
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
PASS = []
FAIL = []
def check(name, ok):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ") + name)

# ----------------------------------------------------------------------
# SYMBOLIC SECTION (general q)
# ----------------------------------------------------------------------
y, q, lam, n, e = sp.symbols('y q lamda n epsilon', positive=True)
nn = sp.Symbol('n')  # allow any real n
f0 = y**(-q)
phi0 = sp.Rational(1, 2) * q * sp.log(y)
s = q * (1 - q) / 2
J = -s * y**(-q)

# S1: f0 = exp(-2 phi0)
check("S1  f0 = exp(-2 phi0)", sp.simplify(f0 - sp.exp(-2 * phi0)) == 0)

# S2: off-shell residue and E0
res = sp.simplify(sp.diff(y**2 * sp.diff(f0, y), y) + 2 * s * y**(-q))
check("S2a (y^2 f0')' = -2 s y^-q  (= -q(1-q) y^-q)", res == 0)
E0 = sp.diff(phi0, y, 2) + 2 * sp.diff(phi0, y) / y - 2 * sp.diff(phi0, y)**2
check("S2b E0[phi0] = s/y^2  (banked E0 = s/r^2 reproduced from criticality data)",
      sp.simplify(E0 - s / y**2) == 0)

# S3: criticality of S_tot = S_C1 + S_src for the power family (radial EL; background spherical
#      so the angular term contributes nothing at first order)
F = sp.Function('F')(y)
c_n = J * f0**(1 - nn) / nn
L_rad = y**2 * sp.diff(F, y)**2 / 4
# EL operator: dL/dF - d/dy dL/dF'
def EL(L, F):
    return sp.diff(L, F) - sp.diff(sp.diff(L, sp.diff(F, y)), y)
# power slot, n != 0
L_src_n = c_n * F**nn
el = EL(L_rad + L_src_n, F)
el0 = el.subs(F, f0).doit()
# substitute the function by background: easier to recompute with explicit background
Fb = f0
el0 = (nn * c_n * Fb**(nn - 1) - sp.diff(y**2 * sp.diff(Fb, y), y) / 2)
check("S3a EL[S_C1+S_src_n](f0) = 0 for all n (power slot, symbolic q,n)",
      sp.simplify(el0) == 0)
# n = 0 (phi-linear): W_0 = -(K/2) ln f, K = 2 s y^-2q
K = 2 * s * y**(-2 * q)
el0_log = (-(K / 2) / Fb - sp.diff(y**2 * sp.diff(Fb, y), y) / 2)
check("S3b EL[S_C1 + K*phi](f0) = 0  (phi slot)", sp.simplify(el0_log) == 0)

# S4: second jets.
A = sp.Function('A')(y)   # phi-fluctuation:  f = f0 exp(-2 e A)
U = sp.Function('U')(y)   # f-fluctuation:    f = f0 + e U
mu = 2 * (1 - nn) * s     # claimed constant mass in the (1/4)-normalized f-form

# f-vars jet of the source: (1/2) W_ff U^2 = mu/4 U^2 ?
W_ff = nn * (nn - 1) * c_n * f0**(nn - 2)
check("S4a source 2nd jet in f-vars = (mu/4) U^2,  mu = 2(1-n)s",
      sp.simplify(W_ff / 2 - mu / 4) == 0)
# phi-vars jet of the source: expand W_n(f0 e^{-2eA}) to O(e^2): claim = -(n/2)*2s*y^{-2q} A^2... derive:
fe = f0 * sp.exp(-2 * e * A)
W_e = c_n * fe**nn
jet2_src_phi = sp.simplify(sp.diff(W_e, e, 2).subs(e, 0) / 2)
check("S4b source 2nd jet in phi-vars = -2 n s y^-2q A^2",
      sp.simplify(jet2_src_phi + 2 * nn * s * y**(-2 * q) * A**2) == 0)
# n=0 log slot: jet2 in phi-vars must vanish
W0_e = K * (phi0 + e * A)
check("S4c phi-slot source 2nd jet in phi-vars = 0",
      sp.simplify(sp.diff(W0_e, e, 2).subs(e, 0)) == 0)
# and n=0 in f-vars: -(K/2) ln(f0+eU): jet2 = K U^2/(4 f0^2) = (s/2) y^... = mu/4 with n=0
W0_f = -(K / 2) * sp.log(f0 + e * U)
jet2_0f = sp.simplify(sp.diff(W0_f, e, 2).subs(e, 0) / 2)
check("S4d phi-slot source 2nd jet in f-vars = (mu(0)/4)U^2 = (s/2) U^2",
      sp.simplify(jet2_0f - s * U**2 / 2) == 0)

# Full C1 jets (radial; angular mass added analytically: at O(e^2) the angular term is
#   f-vars: (lam/4) U^2 / f0 ;  phi-vars: lam f0 A^2   [|grad f|^2/f with grad f = -2 f grad a])
L_C1_phi = y**2 * sp.diff(fe, y)**2 / 4
jet2_C1_phi = sp.simplify(sp.diff(L_C1_phi, e, 2).subs(e, 0) / 2)
target_phi = (y**(2 - 2*q) * sp.diff(A, y)**2 - 4*q*y**(1 - 2*q) * A * sp.diff(A, y)
              + 2 * q**2 * y**(-2*q) * A**2)
check("S4e C1 radial 2nd jet (phi-vars) = y^{2-2q}A'^2 - 4q y^{1-2q}A A' + 2q^2 y^{-2q}A^2",
      sp.simplify(jet2_C1_phi - target_phi) == 0)

# S5: THE EXACT CHANGE-OF-VARIABLE IDENTITY, all n, all q:
#   jet2_phi[A] - jet2_f[-2 f0 A]  =  d/dy( -q y^{1-2q} A^2 )      (pure contact)
jet2_phi_tot = jet2_C1_phi + lam * f0 * A**2 + jet2_src_phi
Um = -2 * f0 * A
jet2_f_tot_of = (y**2 * sp.diff(Um, y)**2 / 4 + lam * Um**2 / (4 * f0)
                 + (mu / 4) * Um**2)
diff_bulk = sp.simplify(jet2_phi_tot - jet2_f_tot_of
                        - sp.diff(-q * y**(1 - 2*q) * A**2, y))
check("S5  jet2_phi[A] - jet2_f[-2 f0 A] = (d/dy)(-q y^{1-2q} A^2)  [contact only; ALL n, ALL q]",
      diff_bulk == 0)

# S5b: the SOURCELESS difference is bulk (panel's refutation), for contrast:
jet2_phi_nosrc = jet2_C1_phi + lam * f0 * A**2
jet2_f_nosrc_of = y**2 * sp.diff(Um, y)**2 / 4 + lam * Um**2 / (4 * f0)
diff_noscr = sp.simplify(jet2_phi_nosrc - jet2_f_nosrc_of
                         - sp.diff(-q * y**(1 - 2*q) * A**2, y))
check("S5b sourceless difference is NOT pure contact (panel refutation reproduced)",
      sp.simplify(diff_noscr) != 0 and sp.simplify(diff_noscr - 2*s*y**(-2*q)*A**2*2) is not None)
print("    sourceless bulk residue =", sp.simplify(diff_noscr), " (should be ~ 2q(1-q) y^-2q A^2)")

# S6: Bessel order. f-form EL: (y^2 u')' = (lam y^q + mu) u ; claim
#   u = y^{-1/2} I_nu( (2 sqrt(lam)/q) y^{q/2} ),  nu = sqrt(1+4 mu)/q
nu_s = sp.sqrt(1 + 4 * mu) / q
z = 2 * sp.sqrt(lam) / q * y**(q / 2)
u_b = y**(sp.Rational(-1, 2)) * sp.besseli(nu_s, z)
ode = sp.diff(y**2 * sp.diff(u_b, y), y) - (lam * y**q + mu) * u_b
check("S6  u = y^-1/2 I_nu(2 sqrt(lam)/q * y^{q/2}) solves the sourced f-form EL, nu = sqrt(1+4mu)/q",
      sp.simplify(ode.rewrite(sp.besseli).doit()) == 0)

# S6b: order values at q = 1/3:  nu^2 = (1+4mu)/q^2 = 9 + 8(1-n)*... = 17 - 8n
nu2_q13 = sp.simplify((1 + 4 * mu) / q**2).subs(q, sp.Rational(1, 3))
check("S6b nu^2 = 17 - 8n at q = 1/3  (n=1: 9; n=0: 17; n=-1: 25)",
      sp.simplify(nu2_q13 - (17 - 8 * nn)) == 0)

# S7: volume coupling no-go: sqrt(-g) per solid angle = r^2 (f-independent) under g_tt g_rr = -1
ff = sp.Symbol('f', positive=True)
g = sp.Matrix([[-ff, 0, 0, 0], [0, 1 / ff, 0, 0], [0, 0, y**2, 0], [0, 0, 0, y**2]])
check("S7  sqrt(-g) = y^2 (per solid angle, f-independent): volume coupling cannot source f",
      sp.simplify(sp.sqrt(-g.det()) - y**2) == 0)

# S8: Pi_f-channel coupling == f-linear modulo boundary: int h*(y^2 f'/2) = bdry - int (1/2)(y^2 h)' f...
h = sp.Function('h')(y)
integrand_diff = h * y**2 * sp.diff(F, y) / 2 - (sp.diff(h * y**2 * F / 2, y) - sp.diff(h * y**2, y) * F / 2)
check("S8  h*Pi_f density = d/dy(h y^2 f/2) - (1/2)(h y^2)' f  (== f-linear + contact)",
      sp.simplify(integrand_diff) == 0)

# S9: hybrid (fixed-metric) scheme: NOT a parametrization — first variation differs.
phi_e = phi0 + e * A
L_hyb = sp.exp(-2 * phi_e) * (f0 * sp.diff(phi_e, y)**2) * y**2   # radial part, metric frozen
el_hyb1 = sp.simplify(sp.diff(L_hyb, e).subs(e, 0))
# first variation density against A: el_hyb1 = (bulk EL).A + total derivative; compare with the
# full-phi first variation. Simpler invariant check: the hybrid jet-1 residual after adding the
# n=0 source (which makes the FULL system critical) is nonzero:
src0_e = K * (phi_e)          # phi-slot source
tot1 = sp.simplify(sp.diff(L_hyb + src0_e, e).subs(e, 0))
# extract bulk EL coefficient: write tot1 = P A + Q A' ; bulk residual = P - dQ/dy
Pc = tot1.coeff(A); Qc = tot1.coeff(sp.diff(A, y))
bulk_res_hyb = sp.simplify(Pc - sp.diff(Qc, y))
check("S9  hybrid scheme is OFF-SHELL even for the completed system (n=0): residual != 0",
      sp.simplify(bulk_res_hyb) != 0)
print("    hybrid jet-1 bulk residual (n=0 completion) =", sp.factor(sp.simplify(bulk_res_hyb)))

# S9b: hybrid second jets (record): mass and nu^2
jet2_hyb = sp.simplify(sp.diff(L_hyb, e, 2).subs(e, 0) / 2) + lam * f0 * A**2
t_h = sp.simplify(jet2_hyb - (y**(2-2*q)*sp.diff(A, y)**2 - 2*q*y**(1-2*q)*A*sp.diff(A, y)
                              + (q**2/2)*y**(-2*q)*A**2 + lam*y**(-q)*A**2))
check("S9b hybrid C1 jet = y^{2-2q}A'^2 - 2q y^{1-2q}A A' + (q^2/2) y^{-2q}A^2 + lam y^-q A^2",
      t_h == 0)
# after IBP of cross term: mass_hyb = q^2/2 + q(1-2q) = q(2-3q)/2 -> nu^2 = [(1-2q)^2+4 mass]/q^2
mass_hyb = sp.simplify(q**2/2 + q*(1-2*q))
nu2_hyb_0 = sp.simplify(((1-2*q)**2 + 4*mass_hyb)/q**2).subs(q, sp.Rational(1,3))
check("S9c hybrid + phi-slot source: nu^2 = 7 at q=1/3 (sourceless panel value, unchanged)",
      nu2_hyb_0 == 7)
# with f-slot source: phi-vars source jet adds -2 s y^-2q A^2 (n=1): mass -> q(2-3q)/2 - q(1-q)
mass_hyb_f = sp.simplify(mass_hyb - q*(1-q))
nu2_hyb_f = sp.simplify(((1-2*q)**2 + 4*mass_hyb_f)/q**2).subs(q, sp.Rational(1,3))
check("S9d hybrid + f-slot source: nu^2 = -1 at q=1/3 (oscillatory core; not Bessel-I class)",
      nu2_hyb_f == -1)

# S10: q(1-q)/2 = q/3  <=>  q in {0, 1/3}  (activation-law compatibility)
sols = sp.solve(sp.Eq(q*(1-q)/2, q/3), q)
check("S10 q(1-q)/2 = q/3 iff q in {0, 1/3}", sorted(sols) == [0, sp.Rational(1, 3)])

# ----------------------------------------------------------------------
# NUMERIC SECTION (q = 1/3): DtN closed forms vs independent ODE shooting
# ----------------------------------------------------------------------
qv = mp.mpf(1) / 3
sv = qv * (1 - qv) / 2

def Lambda_closed(nu, lm):
    """log-derivative u'(1)/u(1), f-normalization: sqrt(lam) I_{nu+1}/I_nu (6 sqrt lam) + (nu-3)/6"""
    z0 = 6 * mp.sqrt(lm)
    return mp.sqrt(lm) * mp.besseli(nu + 1, z0) / mp.besseli(nu, z0) + (nu - 3) / mp.mpf(6)

def Lambda_shoot(nu, lm, y0=mp.mpf('1e-10'), terms=120):
    """independent verification: Frobenius seed + adaptive Taylor ODE integration of
       y^2 u'' + 2 y u' - (lam y^(1/3) + mu) u = 0,  mu = (nu^2/9 - 1)/4 ... from nu^2=(1+4mu)*9"""
    mu_ = (nu**2 * qv**2 - 1) / 4
    sP = (-1 + mp.sqrt(1 + 4 * mu_)) / 2
    # series u = y^sP * sum c_k y^(k/3), c_0 = 1, c_k = lam c_{k-1} / [ (sP+k/3)(sP+k/3+1) - mu_ ]
    cs = [mp.mpf(1)]
    for k in range(1, terms):
        ex = sP + mp.mpf(k) / 3
        cs.append(lm * cs[-1] / (ex * (ex + 1) - mu_))
    def useries(yy):
        t = yy**(mp.mpf(1) / 3)
        acc = mp.mpf(0)
        for k in reversed(range(len(cs))):
            acc = acc * t + cs[k]
        return yy**sP * acc
    def duseries(yy):
        t = yy**(mp.mpf(1) / 3)
        acc = mp.mpf(0)
        for k in reversed(range(len(cs))):
            acc = acc * t + cs[k] * (sP + mp.mpf(k) / 3)
        return yy**(sP - 1) * acc
    f = mp.odefun(lambda yy, w: [w[1], ((lm * yy**(mp.mpf(1)/3) + mu_) * w[0] - 2 * yy * w[1]) / yy**2],
                  y0, [useries(y0), duseries(y0)], tol=mp.mpf('1e-30'))
    u1, du1 = f(mp.mpf(1))
    return du1 / u1

nu_list = {'n=+1 (f-slot)   ': mp.mpf(3),
           'n= 0 (phi-slot) ': mp.sqrt(17),
           'n=-1 (1/f-slot) ': mp.mpf(5)}
lam_list = {'lam=2  (H1/E1)': mp.mpf(2), 'lam=1/2 (M1)': mp.mpf(1) / 2}

print()
for nm, nu in nu_list.items():
    for lnm, lm in lam_list.items():
        c = Lambda_closed(nu, lm)
        sh = Lambda_shoot(nu, lm)
        ok = abs(c - sh) < mp.mpf('1e-12')
        check("N1  DtN closed form == ODE shooting  [%s %s]  (%s)" % (nm.strip(), lnm, mp.nstr(c, 16)), ok)

# N2: panel anchors (nu = 3 family)
D32 = Lambda_closed(mp.mpf(3), mp.mpf(2))
B32 = mp.besseli(4, 6 * mp.sqrt(2)) / mp.besseli(3, 6 * mp.sqrt(2))
check("N2a panel anchor D_B(2) = 0.925083523113", abs(D32 - mp.mpf('0.925083523113')) < mp.mpf('1e-12'))
check("N2b panel anchor B_C1 = I4/I3(6 sqrt2) = 0.654132832357", abs(B32 - mp.mpf('0.654132832357')) < mp.mpf('1e-12'))

# N3: weld anchors: L0 = Lambda_phi-normalized log-derivative = Lambda_f + q  with nu = sqrt(17)
for lm, banked in [(2, '1.33835009'), (6, '2.29931870'), (12, '3.28396540')]:
    L0 = Lambda_closed(mp.sqrt(17), mp.mpf(lm)) + qv
    ok = abs(L0 - mp.mpf(banked)) < mp.mpf('2e-8')
    check("N3  weld L0(lam=%d) = %s  (banked %s):  L0 = Lambda_{sqrt17} + q  EXACT" % (lm, mp.nstr(L0, 10), banked), ok)
# the banked L0 closed form, for identity confirmation:
def L0_banked(nu, lm):
    tau0 = 2 * mp.sqrt(lm) / qv
    Ip = (mp.besseli(nu - 1, tau0) + mp.besseli(nu + 1, tau0)) / 2
    return -(1 - 2 * qv) / 2 + (qv * tau0 / 2) * Ip / mp.besseli(nu, tau0)
ok = all(abs(L0_banked(mp.sqrt(17), mp.mpf(lm)) - (Lambda_closed(mp.sqrt(17), mp.mpf(lm)) + qv)) < mp.mpf('1e-25')
         for lm in (2, 6, 12))
check("N3b banked L0 closed form == Lambda_f-normalized + q (identity, 25+ digits)", ok)

# N4: RECORD VALUES, 12 digits
print()
print("== RECORD VALUES (12 digits) ==")
print("nu orders: 3,  sqrt(17) = %s,  5" % mp.nstr(mp.sqrt(17), 13))
for nm, nu in nu_list.items():
    for lnm, lm in lam_list.items():
        z0 = 6 * mp.sqrt(lm)
        B = mp.besseli(nu + 1, z0) / mp.besseli(nu, z0)
        D = Lambda_closed(nu, lm)
        print("  %s %s :  B = %s   D = %s" % (nm, lnm, mp.nstr(B, 13), mp.nstr(D, 13)))
print("  source dressing shifts (hardening relative to nu=3 family):")
for lnm, lm in lam_list.items():
    d17 = Lambda_closed(mp.sqrt(17), lm) - Lambda_closed(mp.mpf(3), lm)
    d5 = Lambda_closed(mp.mpf(5), lm) - Lambda_closed(mp.mpf(3), lm)
    print("    %s:  D_sqrt17 - D_3 = %s ;  D_5 - D_3 = %s" % (lnm, mp.nstr(d17, 13), mp.nstr(d5, 13)))
# ordering check
ok = all(Lambda_closed(mp.mpf(3), lm) < Lambda_closed(mp.sqrt(17), lm) < Lambda_closed(mp.mpf(5), lm)
         for lm in (mp.mpf(1)/2, mp.mpf(1), mp.mpf(2), mp.mpf(6)))
check("N4  ordering D_3 < D_sqrt17 < D_5 at lam in {1/2,1,2,6}", ok)

# N5: weld-threshold consequence numbers (record): L0 with nu = 3 (f-slot completion family)
print()
for lm in (2, 6, 12):
    print("  L0-analog, f-slot family (nu=3),  lam=%d :  %s" % (lm, mp.nstr(Lambda_closed(mp.mpf(3), mp.mpf(lm)) + qv, 13)))
for lm in (2,):
    print("  L0-analog, 1/f-slot family (nu=5), lam=%d :  %s" % (lm, mp.nstr(Lambda_closed(mp.mpf(5), mp.mpf(lm)) + qv, 13)))

print()
print("TOTAL: %d PASS, %d FAIL" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
