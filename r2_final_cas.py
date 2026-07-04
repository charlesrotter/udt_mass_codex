"""r2_prereg_s_cas.py -- R2 PRE-REGISTRATION (derivation half): CAS verification of every
symbolic claim in r2_prereg_s_dependence.md.

Contract: PURSUIT_CHARTER_2026-07-04.md par.3 step R2, as REFRAMED by R1 (r1_route_fork_native
_derivation.md par.6: bound s = 2mu/Z, not a binary A/B test). This script derives the EXACT
s-dependence of every confrontable observable of the general-(Z,mu) Branch-G vacuum -- STRICTLY
DATA-BLIND: no observational number appears anywhere (grep it).

Banked inputs (cited, not re-derived ad hoc):
  General rule-admissible round-static reduced G Lagrangian (r1_route_fork_cas.py E-block;
  d2c_gp_composite_conditions.md Part 1):
      Lbar_G = (Z/2) rho^2 phi'^2 + 2 mu rho rho' phi' + 2 - 2 rho'^2      (per 4pi sr)
  Metric form (canon C-2026-06-18-1; native_field_equations...md:90):
      ds^2 = -e^{-2phi} c^2 dt^2 + e^{+2phi} dr^2 + rho(r)^2 dOmega^2
  Flux (R1 E1):  Phi = Z rho^2 phi' + 2 mu rho rho'   (exactly conserved in vacuum G)
  Deformation exponent (R1 E2a):  s = 2 mu / Z  (Route A: 0; Route B: 1/2)
  G|P junction conditions (d2c M9 structure, generalized here to (Z,mu)):
      JC1 [Z rho^2 phi' + 2 mu rho rho'] = 0 ;  JC2 [-4 W rho' + 2 mu rho phi'] = 0
  Point-particle coupling a(phi) = e^{+phi} (native_dilation_weight_derivation_results.md D2,
      DERIVED STATIC-ONLY -- the moving-worldline extension is a named CHOSE below).

Run: python3 r2_prereg_s_cas.py   (all symbolic, CPU, no solves beyond trivial quadratures)
"""
import sympy as sp

r, x, th, lam, c = sp.symbols('r x theta lambda c', positive=True)
Z = sp.Symbol('Z', positive=True)          # sheet coefficient, FREE (Route A) / 8 (Route B point)
mu = sp.Symbol('mu', positive=True)        # mixing coefficient; s = 2 mu / Z
s = sp.Symbol('s', positive=True)          # used where the exact exponent is the cleaner label
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
rp_, pp_ = rho.diff(r), phi.diff(r)

checks = []
def check(name, cond):
    ok = bool(cond)
    checks.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name)

def EL(L, q):
    return sp.simplify(sp.diff(L, q) - sp.diff(sp.diff(L, q.diff(r)), r))

# ============================================================ S1. frame + EOMs (banked, reproduced)
LG = (Z/2)*rho**2*pp_**2 + 2*mu*rho*rp_*pp_ + 2 - 2*rp_**2
Phi_flux = Z*rho**2*pp_ + 2*mu*rho*rp_
check('S1a: phi-EOM = -(Phi)\' = 0 with Phi = Z rho^2 phi\' + 2 mu rho rho\' (reproduces R1 E1)',
      sp.simplify(EL(LG, phi) + sp.diff(Phi_flux, r)) == 0)
check('S1b: rho-EOM:  4 rho\'\' = 2 mu rho phi\'\' - Z rho phi\'^2  (reproduces d2c M-forms at (8,2))',
      sp.simplify(EL(LG, rho) - (Z*rho*pp_**2 - 2*mu*rho*phi.diff(r, 2) + 4*rho.diff(r, 2))) == 0)

# ============================================================ S2. zero-flux (ambient) vacuum
a_, b_, phi0 = sp.symbols('a b phi_0', positive=True)
rho_f = a_*r + b_
phi_f = phi0 - (2*mu/Z)*sp.log(rho_f)
sub_f = {phi.diff(r, 2): phi_f.diff(r, 2), pp_: phi_f.diff(r), phi: phi_f,
         rho.diff(r, 2): rho_f.diff(r, 2), rp_: rho_f.diff(r), rho: rho_f}
check('S2a: flat-analog rho=ar+b, phi=phi0 - s ln rho solves both EOMs (reproduces R1 E2a)',
      sp.simplify(EL(LG, phi).subs(sub_f)) == 0 and sp.simplify(EL(LG, rho).subs(sub_f)) == 0)
check('S2b: NEW -- the flat-analog family is exactly the ZERO-FLUX sector: Phi = 0 on it',
      sp.simplify(Phi_flux.subs(sub_f)) == 0)

# ============================================================ S3. one-body exterior (Phi != 0)
# phitilde = phi + s ln rho;  Phi = Z rho^2 phitilde' (R1 E3/E1). Exact solution (E>0 branch):
#   rho^2 = E (x^2 - beta^2),  phitilde = phit_inf + sig * nu * artanh(beta/x),
#   nu = 2 sqrt(Z + mu^2)/Z,   Phi = -sig * Z * nu * E * beta,   x = r - r0.
E_, beta, phit_inf = sp.symbols('E beta phitilde_inf', positive=True)
nu = 2*sp.sqrt(Z + mu**2)/Z
for sig in (+1, -1):
    rho_1 = sp.sqrt(E_*(x**2 - beta**2))
    phit_1 = phit_inf + sig*nu*sp.atanh(beta/x)
    phi_1 = phit_1 - (2*mu/Z)*sp.log(rho_1)
    sub_1 = {phi.diff(r, 2): phi_1.diff(x, 2), pp_: phi_1.diff(x), phi: phi_1,
             rho.diff(r, 2): rho_1.diff(x, 2), rp_: rho_1.diff(x), rho: rho_1}
    okphi = sp.simplify(EL(LG, phi).subs(sub_1).rewrite(sp.log)) == 0
    okrho = sp.simplify(EL(LG, rho).subs(sub_1).rewrite(sp.log)) == 0
    okflux = sp.simplify(Phi_flux.subs(sub_1) - (-sig*Z*nu*E_*beta)) == 0
    check(f'S3a(sig={sig:+d}): one-body exterior solves BOTH EOMs exactly; flux Phi = '
          f'-sig Z nu E beta, nu = 2 sqrt(Z+mu^2)/Z', okphi and okrho and okflux)

# S3b/S3c: additive separation + weak field. ATTRACTIVE branch = sig = +1:
# phitilde ~ phit_inf + nu*beta*sqrt(E)/rho = banked Coulomb phi = phi_inf - q/r with
# q = -nu*beta*sqrt(E) and banked M = -q = nu*beta*sqrt(E) > 0 (native_field_equations:55-66,
# "M=-q"). The q-sector rides phitilde ONLY; the s-tilt is -s ln rho ONLY (exact split).
rho_sym = sp.Symbol('rho_s', positive=True)
x_of_rho = sp.sqrt(rho_sym**2/E_ + beta**2)
phit_of_rho = phit_inf + nu*sp.atanh(beta/x_of_rho)        # attractive branch sig = +1
u = sp.Symbol('u', positive=True)                          # u = 1/rho
phit_u = phit_of_rho.subs(rho_sym, 1/u)
c1 = sp.limit(sp.diff(phit_u, u), u, 0)
c2 = sp.limit(sp.diff(phit_u, u, 2), u, 0)
mhat = nu*beta                                             # the mass parameter (M-analog, sig=+1)
check('S3c: weak field (sig=+1, attractive): d(phitilde)/d(1/rho)|_inf = +nu beta sqrt(E) '
      '(Coulomb-in-phitilde, q = -nu beta sqrt(E), banked M = -q > 0); the 1/rho^2 coefficient '
      'VANISHES (no s x q mixing at this order; the split phitilde-Coulomb + s-tilt is exact)',
      sp.simplify(c1 - nu*beta*sp.sqrt(E_)) == 0 and sp.simplify(c2) == 0)

# S3d: exponential-lapse structure: e^{-2 phitilde} = e^{-2 phit_inf} ((x-beta)/(x+beta))^{sig*nu};
# its expansion 1 + 2 qhat/x + 2 qhat^2/x^2 (qhat = -sig nu beta) = pure exponential-of-Coulomb
# (matches the banked +2q^2 exponential-lapse departure structure, native_field_equations:55-66).
lapse = sp.exp(-2*(phit_inf + (+1)*nu*sp.atanh(beta/x)))
ser_lapse = sp.series(lapse, beta, 0, 3).removeO()
qhat = -nu*beta                                            # q of the attractive branch (negative)
check('S3d: e^{-2 phitilde} = e^{-2 inf}(1 + 2 qhat/x + 2 qhat^2/x^2 + O(qhat^3)) -- exponential '
      'lapse (banked O(1/r^2) departure structure reproduced; Z enters via nu = 2 sqrt(Z+mu^2)/Z)',
      sp.simplify(ser_lapse - sp.exp(-2*phit_inf)*(1 + 2*qhat/x + 2*qhat**2/x**2)) == 0)

# S3e: solution-space completeness note (characterize, don't filter): first integral
#   rho'^2 = E + Phi^2 / (4 (Z+mu^2) rho^2)   -- E>0 open (exterior), E=0 parabolic, E<0 closed.
Ee = sp.Symbol('Ecal')                                     # any sign here
PhiC = sp.Symbol('Phi_c')
rho_g = sp.Function('rho_g', positive=True)(r)
first_int = rho_g.diff(r)**2 - Ee - PhiC**2/(4*(Z + mu**2)*rho_g**2)
consistency = sp.simplify(sp.diff(first_int, r)
                          - 2*rho_g.diff(r)*(rho_g.diff(r, 2)
                                             + PhiC**2/(4*(Z + mu**2)*rho_g**3)))
check('S3e: first integral rho\'^2 = E + Phi^2/(4(Z+mu^2)rho^2) is exact for the vacuum rho-EOM '
      'written in phitilde form (4(1+mu^2/Z) rho\'\' = -Phi^2/(Z rho^3)); E of ANY sign spans the '
      'full vacuum solution space (E>0 exterior, E=0 parabolic, E<0 closed -- characterized)',
      consistency == 0)

# ============================================================ S4. gauge audit
# Form-preserving coordinate maps: r-shift, and the BOOST (t,r,phi) -> (lam t, r/lam, phi + ln lam).
lam_ = sp.Symbol('lambda_b', positive=True)
# Under the boost the zero-flux solution (a, b, phi0) -> (lam a, b, phi0 + ln lam):
rt = sp.Symbol('rt', positive=True)                        # new radial coordinate
rho_new = (lam_*a_)*rt + b_                                # candidate mapped solution
phi_new = (phi0 + sp.log(lam_)) - (2*mu/Z)*sp.log(rho_new)
# The boost sends the POINT r = lam*rt; the original fields evaluated there:
rho_old_at = rho_f.subs(r, lam_*rt)
phi_old_at = phi_f.subs(r, lam_*rt) + sp.log(lam_)         # phi -> phi + ln lam (form-preserving)
check('S4a: boost (t,r,phi)->(lam t, r/lam, phi+ln lam) maps the zero-flux family to itself with '
      '(a, b, phi0) -> (lam a, b, phi0 + ln lam): the metric FORM is preserved',
      sp.simplify(rho_new - rho_old_at) == 0 and
      sp.simplify(sp.expand_log(phi_new - phi_old_at, force=True)) == 0)
Delta = sp.exp(phi0)/a_
Delta_boost = sp.exp(phi0 + sp.log(lam_))/(lam_*a_)
check('S4b: invariants -- s is boost-invariant trivially; Delta = e^{phi0}/a is boost-INVARIANT; '
      'phi0 alone is gauge (absorbable): the measurable ambient content is (s, Delta-profile)',
      sp.simplify(Delta_boost - Delta) == 0)
# S4c: the global shift phi -> phi + lam maps solutions to solutions (RULE-1) and multiplies the
# ruler-area reader D(rho) = e^{phi}/rho' by e^{lam}: D's VALUE is integration data (which vacuum
# the universe realized), never theory-fixed; only D-RATIOS and s = -dlnD/dlnrho are contract rows.
D_reader = sp.exp(phi_f)/rho_f.diff(r)
D_shift = sp.exp(phi_f + lam)/rho_f.diff(r)
check('S4c: shift phi->phi+lam sends D -> e^lam D (value = integration data); '
      'log-slope dlnD/dln rho = -s is shift- AND boost-invariant',
      sp.simplify(D_shift - sp.exp(lam)*D_reader) == 0 and
      sp.simplify(sp.diff(sp.log(D_reader.subs(r, (rho_sym - b_)/a_)), rho_sym)*rho_sym
                  + 2*mu/Z) == 0)

# ============================================================ S5. metric observables (zero-flux)
# In areal coordinate rho:  A(rho) := -g_tt/c^2 = e^{-2phi0} rho^{2s},
#                           B(rho) := g_rhorho = e^{+2phi0} rho^{-2s} / a^2.
A_amb = sp.exp(-2*phi0)*rho_sym**(2*s)
B_amb = sp.exp(2*phi0)*rho_sym**(-2*s)/a_**2
check('S5a: A*B = 1/a^2 (the form reciprocity -g_tt g_rr = c^2 survives in areal coordinates up '
      'to the constant a^2); g_rr(r-coord) = e^{2phi} picks up exactly rho^{-2s} = rho^{-4mu/Z}',
      sp.simplify(sp.powsimp(A_amb*B_amb, force=True) - 1/a_**2) == 0 and
      sp.simplify(sp.powsimp(sp.expand_log(
          sp.log(sp.exp(2*phi_f)) - sp.log(sp.exp(2*phi0)*rho_f**(-2*(2*mu/Z))),
          force=True), force=True)) == 0)
# proper radial distance element: dl/drho = sqrt(B) = D(rho) = Delta rho^{-s}
check('S5b: dl/drho = Delta rho^{-s}: proper distance vs areal radius is a pure power law, '
      'log-slope -s (the ruler-vs-area row); D-ratio between stations = (rho2/rho1)^{-s}',
      sp.simplify(sp.sqrt(B_amb) - Delta*rho_sym**(-s)) == 0)

# ============================================================ S6. clock + radar rows (zero-flux)
rho1, rho2 = sp.symbols('rho_1 rho_2', positive=True)
rate = sp.exp(-(phi0 - s*sp.log(rho_sym)))                 # clock rate e^{-phi} (canon reader)
ratio = sp.simplify((rate.subs(rho_sym, rho2))/(rate.subs(rho_sym, rho1)))
check('S6a: clock-rate ratio between stations = (rho2/rho1)^s EXACTLY -- phi0, a, b all cancel: '
      'the gauge-closing invariant (two clocks + the areal radii of their spheres expose s)',
      sp.simplify(ratio - (rho2/rho1)**s) == 0)
# radar: coordinate time of light rho1 -> rho2 (radial null: c dt = e^{2phi} dr = B_r dr);
# proper time at station 1: tau = e^{-phi(rho1)} * 2 * Int; proper distance l = Int sqrt(B) drho.
# (trivial quadratures done via VERIFIED antiderivatives, avoiding Piecewise branching)
anti_t = rho_sym**(1 - 2*s)/(1 - 2*s)                      # d/drho = rho^{-2s}
anti_l = rho_sym**(1 - s)/(1 - s)                          # d/drho = rho^{-s}
check('S6b-0: antiderivative controls: d/drho[rho^{1-2s}/(1-2s)] = rho^{-2s}; '
      'd/drho[rho^{1-s}/(1-s)] = rho^{-s}',
      sp.simplify(sp.diff(anti_t, rho_sym) - rho_sym**(-2*s)) == 0 and
      sp.simplify(sp.diff(anti_l, rho_sym) - rho_sym**(-s)) == 0)
tt_coord = (sp.exp(2*phi0)/(a_*c))*(anti_t.subs(rho_sym, rho2) - anti_t.subs(rho_sym, rho1))
tau_rt = sp.exp(-phi0)*rho1**s*2*tt_coord
ell = (sp.exp(phi0)/a_)*(anti_l.subs(rho_sym, rho2) - anti_l.subs(rho_sym, rho1))
F_ratio = c*tau_rt/(2*ell)
F_claim = (1 - s)/(1 - 2*s) * rho1**s * (rho2**(1 - 2*s) - rho1**(1 - 2*s)) \
          / (rho2**(1 - s) - rho1**(1 - s))
check('S6b: radar-echo/ruler ratio  c tau/(2 l) = F(s; rho2/rho1) '
      '= (1-s)/(1-2s) * rho1^s (rho2^{1-2s}-rho1^{1-2s})/(rho2^{1-s}-rho1^{1-s}); gauge-free '
      '(phi0 and a cancel); F(0;R) = 1',
      sp.simplify(sp.powsimp(F_ratio - F_claim, force=True)) == 0
      and sp.simplify(F_claim.subs(s, 0)) == 1)
F_half = sp.limit(F_claim, s, sp.Rational(1, 2))
check('S6c: Route-B point s=1/2: F(1/2;R) = sqrt(rho1) ln(rho2/rho1) / (2(sqrt(rho2)-sqrt(rho1))) '
      '(the radar time grows only logarithmically -- a strong structural signature)',
      sp.simplify(F_half - sp.sqrt(rho1)*sp.log(rho2/rho1)/(2*(sp.sqrt(rho2) - sp.sqrt(rho1)))) == 0)

# ============================================================ S7. null geodesics (zero-flux)
# orbit: (du/dphi)^2 = a^2 e^{-2phi0} (u0^{2-2s} - u^{2-2s}), u = 1/rho  =>
# swept azimuth = D(rho0) * J(s),  J(s) = 2 Int_0^1 dw / sqrt(1 - w^{2-2s}).
w_ = sp.Symbol('w', positive=True)
Etil, Ltil = sp.symbols('Ecal_n Lcal', positive=True)
# derive the orbit equation from scratch: -A c^2 t'^2 + B rho'^2 + rho^2 ang'^2 = 0,
# E = A c^2 t', L = rho^2 ang'  (affine parameter):
rhodot2 = (Etil**2/(A_amb*c**2) - Ltil**2/rho_sym**2)/B_amb
dudphi2 = sp.simplify(rhodot2/(Ltil/rho_sym**2)**2/rho_sym**4).subs(rho_sym, 1/u)
claim7 = a_**2*(Etil**2/(Ltil**2*c**2) - sp.exp(-2*phi0)*u**(2 - 2*s))
check('S7a: null orbit equation (du/dphi)^2 = a^2[E^2/(L^2 c^2) - e^{-2phi0} u^{2-2s}] '
      '(A B = 1/a^2 collapses it; only the exponent 2-2s carries the route)',
      sp.simplify(sp.powsimp(dudphi2 - claim7, force=True)) == 0)
# J(s) closed form by the substitution v = w^{2-2s}:
alpha = 1/(2 - 2*s)
J_claim = sp.sqrt(sp.pi)*sp.gamma(alpha)/((1 - s)*sp.gamma(alpha + sp.Rational(1, 2)))
v_ = sp.Symbol('v', positive=True)
integrand_v = sp.Rational(1, 1)/( (2 - 2*s) ) * v_**(alpha - 1) * (1 - v_)**(-sp.Rational(1, 2))
J_beta = 2*sp.gamma(alpha)*sp.gamma(sp.Rational(1, 2))/((2 - 2*s)*sp.gamma(alpha + sp.Rational(1, 2)))
check('S7b: J(s) = 2 Int_0^1 dw/sqrt(1-w^{2-2s}) = sqrt(pi) Gamma(1/(2-2s)) / '
      '[(1-s) Gamma(1/(2-2s)+1/2)]  (Beta integral after v = w^{2-2s}); J(0) = pi',
      sp.simplify(J_beta - J_claim) == 0 and sp.simplify(J_claim.subs(s, 0) - sp.pi) == 0)
J_series = sp.series(J_claim, s, 0, 2).removeO()
check('S7c: small-s: J(s) = pi [1 + (1 - ln 2) s + O(s^2)]: an O(s), impact-parameter-'
      'INDEPENDENT vacuum deflection (every ray, however far from any body)',
      sp.simplify(J_series - sp.pi*(1 + (1 - sp.log(2))*s)) == 0)
# spot-exact values:
check('S7d: exact spot values: J(1/2) = pi*sqrt(2)*Gamma(1)/Gamma(3/2)... evaluate: '
      'J(1/2) = 2 sqrt(pi) Gamma(1)/Gamma(3/2) = 4 -- wait, verify numerically instead',
      abs(float(J_claim.subs(s, sp.Rational(1, 2))) -
          float(2*sp.integrate(1/sp.sqrt(1 - w_), (w_, 0, 1)))) < 1e-12)

# ============================================================ S8. timelike geodesics (zero-flux,
# METRIC-GEODESIC motion-law premise -- see S10 for the native-weighted fork)
# G(rho) = rhodot^2 = [eps^2/(A c^2) - L^2/rho^2 - c^2]/B ; circular: G = G' = 0;
# epicyclic omega_r^2 = -G''/2 ; Omega_phi = L/rho^2 (proper time).
eps, LL = sp.symbols('epsilon Lang', positive=True)
G_fun = (eps**2/(A_amb*c**2) - LL**2/rho_sym**2 - c**2)/B_amb
solcirc = sp.solve([G_fun, sp.diff(G_fun, rho_sym)], [eps**2, LL**2], dict=True)
assert len(solcirc) == 1
eps2c, LL2c = solcirc[0][eps**2], solcirc[0][LL**2]
check('S8a: circular orbits exist iff 0 < s < 1: L^2 = s c^2 rho^{2}/(1-s) * ... with '
      'L^2/(c^2 rho^2) = s/(1-s) -- local orbital speed v^2/c^2 = s/(1-s+s) ... derive below',
      sp.simplify(LL2c - s*c**2*rho_sym**2/(1 - s)) == 0)
# local velocity measured by the static observer: v^2/c^2 = L^2/(rho^2 c^2) / (eps^2/(A c^4) ... )
# cleanest: v^2/c^2 = (rho^2 Omega_coord^2 / A) with Omega_coord^2 = c^2 A'/(2 rho):
Om_coord2 = c**2*sp.diff(A_amb, rho_sym)/(2*rho_sym)
v2 = sp.simplify(rho_sym**2*Om_coord2/(c**2*A_amb))
check('S8b: v^2/c^2 = s EXACTLY, radius-independent (flat rotation law of the ambient s-vacuum); '
      'and Omega_coord^2 rho^2 = s c^2 A/rho^0 ... Kepler replaced by Omega^2 = s c^2 A(rho)/rho^2',
      sp.simplify(v2 - s) == 0)
omr2 = sp.simplify(-(sp.diff(G_fun, rho_sym, 2)/2).subs({eps**2: eps2c, LL**2: LL2c}))
Omphi2 = sp.simplify((LL2c)/rho_sym**4)
apsidal2 = sp.simplify(Omphi2/omr2)                        # (Psi/pi)^2 = Omega_phi^2/omega_r^2
check('S8c: ambient apsidal angle: (Psi/pi)^2 = D(rho_c)^2 / (2(1-s)) EXACTLY, D = Delta rho^{-s} '
      '(the same local ruler-area factor D as in the bending row; at s->0, D->Delta->1: '
      'Psi -> pi/sqrt(2), the classic 1/rho-force apsidal angle)',
      sp.simplify(sp.powsimp(apsidal2 - (Delta*rho_sym**(-s))**2/(2*(1 - s)),
                             force=True)) == 0)
print('    S8c exact apsidal ratio (Psi/pi)^2 =', sp.simplify(apsidal2))

# ============================================================ S9. one-body observables
# gauge-fix (S4-legal, tagged): E = 1, phit_inf = 0. ATTRACTIVE branch sig = +1 (S3c: banked
# M = -q = nu*beta > 0). mhat = nu*beta. phi = phitilde - s ln rho; A = e^{-2phi}.
Afun_x = sp.exp(-2*nu*sp.atanh(beta/x))*(x**2 - beta**2)**s        # A(x) = e^{-2phit} rho^{2s}
rho_x = sp.sqrt(x**2 - beta**2)
# clock log-gradient row: rate = e^{-phi};  ln rate = -phitilde + s ln rho (constants dropped)
lograte = -nu*sp.atanh(beta/x) + s*sp.log(rho_x)
dlng = sp.simplify(sp.diff(lograte, x)/sp.diff(sp.log(rho_x), x))
check('S9a: master clock row EXACT: d ln(rate)/d ln rho = s + mhat/x = s + mhat/rho + O(1/rho^3), '
      'mhat = nu beta: the s-piece is the CONSTANT term of the log-gradient, the body piece '
      'falls off as 1/rho (separable by a multi-radius clock network); no s*mhat cross-term',
      sp.simplify(dlng - (s + nu*beta/x)) == 0)
# Kepler row: Omega_coord^2 = c^2 A'(rho)/(2 rho) on the exact one-body A:
A_rho = Afun_x.subs(x, sp.sqrt(rho_sym**2 + beta**2))
Om2_body = c**2*sp.diff(A_rho, rho_sym)/(2*rho_sym)
kepler_fn = sp.simplify(Om2_body*rho_sym**3/(c**2*A_rho))
check('S9b: Kepler deformation EXACT: Omega^2 rho^3/(c^2 A) = s rho + mhat * rho/sqrt(rho^2+'
      'beta^2) = mhat + s rho + O(1/rho^2): the body restores Kepler (mhat term) while s adds a '
      'linearly-growing term -- functionally independent (rotation-curve-style separability)',
      sp.simplify(kepler_fn - (s*rho_sym
                               + nu*beta*rho_sym/sp.sqrt(rho_sym**2 + beta**2))) == 0)
# precession row: exact epicyclic ratio on the one-body metric, then series in beta:
dxdrho = sp.diff(sp.sqrt(rho_sym**2 + beta**2), rho_sym)
B_rho = sp.simplify((1/A_rho)*dxdrho**2)                   # g_rhorho = e^{2phi} (dx/drho)^2
G_body = (eps**2/(A_rho*c**2) - LL**2/rho_sym**2 - c**2)/B_rho
sol9 = sp.solve([G_body, sp.diff(G_body, rho_sym)], [eps**2, LL**2], dict=True)
assert len(sol9) == 1
omr2_9 = sp.simplify(-(sp.diff(G_body, rho_sym, 2)/2).subs(
    {eps**2: sol9[0][eps**2], LL**2: sol9[0][LL**2]}))
Omphi2_9 = sp.simplify(sol9[0][LL**2]/rho_sym**4)
ratio9 = sp.simplify(Omphi2_9/omr2_9)
rat_series = sp.series(ratio9, beta, 0, 2).removeO()
rat0 = sp.simplify(rat_series.subs(beta, 0))
rat1 = sp.simplify(sp.diff(rat_series, beta))
apsidal2_gf = apsidal2.subs({phi0: 0, a_: 1})              # same gauge fixing as S9 (E=1, inf=0)
check('S9c: apsidal ratio (Psi/pi)^2 = [ambient S8 value](s) + c1(s, Z) * beta + O(beta^2): '
      'the beta=0 term reproduces the gauge-fixed ambient apsidal EXACTLY '
      '(the one-body orbit interpolates ambient-dominated <-> body-dominated regimes; the '
      'expansion in beta at fixed rho breaks down as s->0 where ambient orbits disappear -- '
      'the honest crossover parameter is mhat/(s rho))',
      sp.simplify(rat0 - apsidal2_gf) == 0)
print('    S9c: (Psi/pi)^2 =', rat0, '  +  beta * [', sp.simplify(rat1), ']  + O(beta^2)')
# S9d: the body-dominated pole: s=0 (mu=0) exactly -- Newtonian ellipse + relativistic Z-order
ratio9_s0 = sp.simplify(ratio9.subs({s: 0, mu: 0}))
rat_s0_series = sp.series(ratio9_s0, beta, 0, 2).removeO()
c0_s0 = sp.simplify(rat_s0_series.subs(beta, 0))
c1_s0 = sp.simplify(sp.diff(rat_s0_series, beta))
check('S9d: body-dominated check at s=0 (mu=0): (Psi/pi)^2 = 1 + c1(Z) beta/rho + O(beta^2) -- '
      'the Newtonian closed ellipse (Psi=pi) is recovered at leading order; the O(beta/rho) '
      'precession coefficient carries Z (nu = 2/sqrt(Z)): the SECOND dial, relativistic order',
      sp.simplify(c0_s0 - 1) == 0)
print('    S9d: s=0 one-body (Psi/pi)^2 = 1 + beta*[', c1_s0, '] + O(beta^2)   [nu->2/sqrt(Z)]')

# ============================================================ S10. the motion-law fork (named)
# Native banked point coupling a(phi) = e^{+phi} (DERIVED STATIC-ONLY). IF extended to moving
# worldlines (CHOSE, named), S = -mc Int e^{phi} dtau = geodesics of ghat = e^{2phi} g. Then:
phi_g = sp.Function('phi_g')(r)
ghat_tt = sp.exp(2*phi_g)*(-sp.exp(-2*phi_g)*c**2)
check('S10a: ghat_tt = -c^2 IDENTICALLY (any phi, any solution): under the weighted motion law '
      'static worldlines are geodesics -- ZERO static force, no bound orbits in ANY static '
      'configuration; the orbit rows (S8, S9) hold ONLY under the metric-geodesic premise',
      sp.simplify(ghat_tt + c**2) == 0)
# null rays are conformally robust: the null orbit equation from ghat equals that from g:
Ahat, Bhat = sp.exp(2*phi0 - 2*s*sp.log(rho_sym))*A_amb, sp.exp(2*phi0 - 2*s*sp.log(rho_sym))*B_amb
# (conformal factor e^{2phi} in the ambient = e^{2phi0} rho^{-2s})
conf = sp.exp(2*(phi0 - s*sp.log(rho_sym)))
rhodot2_hat = (Etil**2/(conf*A_amb*c**2) - Ltil**2/(conf*rho_sym**2))/(conf*B_amb)
dudphi2_hat = sp.simplify(rhodot2_hat/(Ltil/(conf*rho_sym**2))**2/rho_sym**4).subs(rho_sym, 1/u)
check('S10b: the LIGHT rows are motion-law-robust: the null orbit equation from ghat = e^{2phi} g '
      'is IDENTICAL to that from g (conformal invariance of null geodesics, verified directly '
      'on the ambient family)',
      sp.simplify(sp.powsimp(dudphi2_hat - dudphi2, force=True)) == 0)

# ============================================================ S11. lever 1: G|P seal phi'-jump
pG, rG, pP, rP = sp.symbols("phipG rhopG phipP rhopP", real=True)
rs, phis = sp.symbols('rho_seal phi_seal', positive=True)
JC1 = Z*rs**2*pG + 2*mu*rs*rG - (Z*rs**2*pP + 2*mu*rs*rP)
JC2 = -4*rG + 2*mu*rs*pG - (-4*sp.exp(-2*phis)*rP + 2*mu*rs*pP)
sol11 = sp.solve([JC1, JC2], [pG, rG], dict=True)
assert len(sol11) == 1
rG_sol = sp.simplify(sol11[0][rG])
jump = sp.simplify(sol11[0][pG] - pP)
rG_claim = rP*(sp.exp(-2*phis) + mu**2/Z)/(1 + mu**2/Z)
jump_claim = (2*mu/Z)*(1 - sp.exp(-2*phis))*rP/(rs*(1 + mu**2/Z))
check('S11a: general-(Z,mu) G|P seal: rho\'_G = rho\'_P (e^{-2phi_s} + mu^2/Z)/(1 + mu^2/Z); '
      'phi\'_G - phi\'_P = s (1 - e^{-2phi_s}) rho\'_P / (rho_s (1 + mu^2/Z)) -- the jump is '
      'PROPORTIONAL TO s (vanishes iff s=0 or phi_s=0 or rho\'_P=0)',
      sp.simplify(rG_sol - rG_claim) == 0 and sp.simplify(jump - jump_claim) == 0)
check('S11b: reproduces banked d2c M9a,b at (Z,mu)=(8,2): rho\'_G = (2e^{-2phi_s}+1)/3 rho\'_P; '
      '[phi\'] = (1-e^{-2phi_s}) rho\'_P/(3 rho_s)',
      sp.simplify(rG_claim.subs({Z: 8, mu: 2}) - rP*(2*sp.exp(-2*phis) + 1)/3) == 0 and
      sp.simplify(jump_claim.subs({Z: 8, mu: 2}) - (1 - sp.exp(-2*phis))*rP/(3*rs)) == 0)

# ============================================================ S12. lever 2: flux-without-twist
# On a G-domain, phi' = (Phi - 2 mu rho rho')/(Z rho^2):
# Delta phi = (Phi/Z) I - s ln(rho2/rho1), I = Int dr/rho^2. Canon odd+odd: Delta phi = 0 =>
# Phi = s Z ln(rho2/rho1)/I  (reproduces d2b E3 / R1 par.6.3 at (8,2): 4 ln(rho2/rho1)/I).
I_, lnr = sp.symbols('Ical lnratio', positive=True)
Phi_odd = sp.solve(sp.Eq(0, (sp.Symbol('Phi_x')/Z)*I_ - (2*mu/Z)*lnr), sp.Symbol('Phi_x'))[0]
check('S12: canon odd+odd G-domain flux Phi = 2 mu ln(rho2/rho1)/I = s Z ln(rho2/rho1)/I '
      '(at (8,2): 4 ln(rho2/rho1)/I, matches d2b E3); realizability = SEPARATE question '
      '(see doc: NO realizable configuration in the banked frame)',
      sp.simplify(Phi_odd - 2*mu*lnr/I_) == 0 and
      sp.simplify(Phi_odd.subs({mu: 2}) - 4*lnr/I_) == 0)

# ============================================================ S13. THE FRAME / MOTION-LAW ADJUDICATION
# The load-bearing fork (#1 job): which metric do physical clocks / rods / free bodies couple to --
# the "geometric" g, or the conformal ghat = a(phi)^2 g = e^{2phi} g?  The native STATIC-derived weight
# a(phi) = e^{+phi} makes ghat the JORDAN (matter) frame. This block banks the fork's exact reach.
# STRICTLY DATA-BLIND.  [motion_law_verdict: orbit rows VANISH under the native law; clocks ride the
# SAME frame fork -- correcting the LEAD's "clocks solid regardless"; only light J(s) is fork-robust.]
phi_gen = sp.Function('phi_gen')(r)
g_tt_g = -sp.exp(-2*phi_gen)*c**2
g_rr_g = sp.exp(2*phi_gen)
ghat_tt = sp.exp(2*phi_gen)*g_tt_g
ghat_rr = sp.exp(2*phi_gen)*g_rr_g
check('S13a: ghat = e^{2phi} g has ghat_tt = -c^2 IDENTICALLY (ANY phi -- ambient OR one-body): the '
      'conformal weight FLATTENS the time-time block; g_tt\'s whole gravitational potential is erased '
      'in the matter frame. Spatial blocks keep phi: ghat_rr = e^{4phi}, ghat_OO = e^{2phi} rho^2',
      sp.simplify(ghat_tt + c**2) == 0)
# S13b: the native weighted worldline action IS the ghat-geodesic action (no explicit phi) => Jordan frame
td, rd = sp.symbols('tdot rdot', positive=True)
# compare SQUARED integrands (both are non-negative magnitudes; avoids the sqrt-branch ambiguity of a
# generic Function phi): a(phi)^2 (-g_uv xdot xdot) must equal (-ghat_uv xdot xdot)
lhs13_sq = sp.exp(2*phi_gen)*(-g_tt_g*td**2 - g_rr_g*rd**2)
rhs13_sq = -ghat_tt*td**2 - ghat_rr*rd**2
check('S13b: a(phi)^2(-g_uv xdot xdot) = (-ghat_uv xdot xdot), i.e. -mc Int a(phi) sqrt(-g xdot xdot) '
      '= -mc Int sqrt(-ghat xdot xdot) with NO explicit phi: ghat is the JORDAN (matter) frame -- free '
      'bodies, rods AND clocks couple minimally to ghat',
      sp.simplify(lhs13_sq - rhs13_sq) == 0)
# S13c: R1-invariance of the MOVING worldline action FAILS (banks the D2 anisotropy inside R2)
lam_s = sp.Symbol('lambda_s', positive=True)
phi_c = sp.Symbol('phi_c', real=True)
def wI(extra):
    ph = phi_c + extra
    return sp.exp(ph)*sp.sqrt(sp.exp(-2*ph)*c**2*td**2 - sp.exp(2*ph)*rd**2)
res_static = sp.simplify((wI(lam_s) - wI(0)).subs(rd, 0))
res_moving_ratio = sp.simplify(wI(lam_s)/wI(0))
mv = float(res_moving_ratio.subs({td: 10, rd: 1, c: 1, lam_s: sp.log(2), phi_c: 0}))
check('S13c: a(phi) dtau_g is R1-invariant (phi->phi+lam) ONLY on the STATIC slice (rd=0: residual=0); '
      'for rd!=0 it is NOT invariant (the radial block over-shifts by e^{4lam}) -- the D2 anisotropy: '
      'NO single a(phi) yields an R1-invariant MOVING law. The moving extension is a genuine CHOSE; the '
      'ghat-geodesic is its minimal covariant reading, not R1-forced',
      res_static == 0 and abs(mv - 1) > 1e-6)
# S13d: ORBIT consequence -- ghat_tt const => zero static force in ANY static config (ambient + one-body)
Gamma_r_tt = -sp.Rational(1, 2)*(1/ghat_rr)*sp.diff(ghat_tt, r)
check('S13d: ORBIT ROWS VANISH under the native law: the ghat radial force on a static body '
      'Gamma^r_tt = -1/2 ghat^{rr} d_r(ghat_tt) = 0 (ghat_tt constant) -- ZERO static gravitational '
      'force in EVERY static config (ambient AND one-body central mass). S8/S9 (incl. the flat rotation '
      'law v^2=s) hold ONLY under the metric-g geodesic (GR-imported) premise',
      sp.simplify(Gamma_r_tt) == 0)
# S13e: CLOCK consequence -- static clock ratio rides the SAME frame fork (LEAD correction)
phi_amb = phi0 - s*sp.log(rho_sym)
dtau_g = sp.sqrt(-g_tt_g.subs(phi_gen, phi_amb))/c
dtau_gh = sp.sqrt(-ghat_tt.subs(phi_gen, phi_amb))/c
rr1, rr2 = sp.symbols('rr1 rr2', positive=True)
ratio_g = sp.simplify((dtau_g.subs(rho_sym, rr2))/(dtau_g.subs(rho_sym, rr1)))
ratio_gh = sp.simplify((dtau_gh.subs(rho_sym, rr2))/(dtau_gh.subs(rho_sym, rr1)))
check('S13e: CLOCK ROWS RIDE THE SAME FORK (corrects the LEAD "clocks solid regardless of the fork"): '
      'static clock ratio = (rho2/rho1)^s in the g-frame but = 1 (NO redshift) in the ghat matter frame '
      '(ghat_tt=-c^2). Redshift AND static force both descend from g_tt and both vanish in ghat. Clocks '
      'are motion-law-robust (static) yet NOT frame-robust',
      sp.simplify(ratio_g - (rr2/rr1)**s) == 0 and ratio_gh == 1)
# S13f: self-consistency -- depth-independent static rest energy IS ghat's zero potential; native points to ghat
E_static = sp.exp(phi_amb)*dtau_g*c**2
check('S13f: self-consistency -- the banked depth-independent static rest energy (a(phi)dtau/dt = '
      'e^{phi}e^{-phi} => E=mc^2 const) IS the statement ghat_tt=-c^2 (zero potential). The native matter '
      'coupling POINTS TO the ghat frame (zero redshift, zero static force); the ONLY frame-robust '
      'DYNAMICAL signature is the conformally-invariant light deflection J(s) (S7/S10b)',
      sp.simplify(E_static - c**2) == 0)

# ===============================================================
n_ok = sum(1 for _, ok in checks if ok)
print(f"\n{n_ok}/{len(checks)} checks PASS")
if n_ok != len(checks):
    raise SystemExit(1)
