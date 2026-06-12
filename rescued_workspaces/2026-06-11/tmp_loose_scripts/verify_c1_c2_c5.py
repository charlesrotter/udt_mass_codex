"""Blind adversarial verification: C1 (criticality/source share),
C2 (fork collapse identity + hybrid refutation), C5 (slot covariance,
weld-operator-as-bulk-Hessian). Independent recomputation, sympy.
Verifier 2026-06-11."""
import sympy as sp

y, q, lam, n, s = sp.symbols('y q lam n s', positive=True)
PASS = FAIL = 0
def check(label, ok):
    global PASS, FAIL
    PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL"), "|", label)

# ---------- C1 ----------
f0 = y**(-q)
sigma = sp.simplify(sp.diff(y**2 * sp.diff(f0, y), y))
check("C1a: (y^2 f0')' = -q(1-q) y^-q exactly",
      sp.simplify(sigma + q*(1-q)*y**(-q)) == 0)

phi0 = (q/2)*sp.log(y)   # f = e^{-2phi} => phi0 = (q/2) ln y
E0 = sp.diff(phi0, y, 2) + 2*sp.diff(phi0, y)/y - 2*sp.diff(phi0, y)**2
check("C1b: banked E0[phi0] = q(1-q)/(2 y^2) IDENTICALLY in q "
      "(so E0 = s/y^2 with s = q(1-q)/2 is the banked DEFINITION evaluated "
      "on the collar, not a value coincidence)",
      sp.simplify(E0 - q*(1-q)/(2*y**2)) == 0)

qf = sp.symbols('qf')   # unrestricted symbol so q=0 root is kept
sols = sp.solve(sp.Eq(qf*(1-qf)/2, qf/3), qf)
check("C1c: q(1-q)/2 = q/3 has solutions exactly {0, 1/3}",
      set(sols) == {sp.S(0), sp.Rational(1,3)})
check("C1d: at q=1/3, s = q(1-q)/2 = 1/9 = q/3",
      sp.Rational(1,3)*sp.Rational(2,3)/2 == sp.Rational(1,9))

# Relation sigma = -2 s y^{-q}: the factor-(1/2) normalization
check("C1e: sigma = -2 s y^-q with s = q(1-q)/2 (s := -sigma y^q / 2)",
      sp.simplify(sigma + 2*(q*(1-q)/2)*y**(-q)) == 0)

# ---------- C2: fork collapse identity ----------
a = sp.Function('a')(y)
eps = sp.symbols('eps')
sval = q*(1-q)/2
J = -sval * y**(-q)
c_n = J * f0**(1-n) / n            # criticality-fixed coupling

def jet(expr, order):
    ser = sp.series(sp.expand(expr), eps, 0, order+1).removeO()
    return sp.expand(ser).coeff(eps, order)

# phi-parametrization: f = f0 e^{-2 eps a}
f_phi = f0 * sp.exp(-2*eps*a)
L_phi = sp.Rational(1,4)*y**2*sp.diff(f_phi, y)**2 + c_n*f_phi**n
# f-parametrization: f = f0 + eps h, h = -2 f0 a  (linear substitution)
f_f = f0 + eps*(-2*f0*a)
L_f = sp.Rational(1,4)*y**2*sp.diff(f_f, y)**2 + c_n*f_f**n

diff2 = sp.simplify(jet(L_phi,2) - jet(L_f,2))
contact = sp.diff(-q*y**(1-2*q)*a**2, y)
check("C2a: jet2_phi[a] - jet2_f[-2 f0 a] = d/dy(-q y^{1-2q} a^2) "
      "PURE CONTACT, symbolic in BOTH n and q",
      sp.simplify(diff2 - contact) == 0)

# n -> 0 slot: source = J f0 ln f  (field-dep part of lim c_n f^n)
Lp0 = sp.Rational(1,4)*y**2*sp.diff(f_phi, y)**2 + J*f0*sp.log(f_phi)
Lf0 = sp.Rational(1,4)*y**2*sp.diff(f_f, y)**2 + J*f0*sp.log(f_f)
check("C2b: same identity for the n->0 (ln f) slot",
      sp.simplify(sp.simplify(jet(Lp0,2)-jet(Lf0,2)) - contact) == 0)

# first jets agree for all n (criticality): delta S_src/delta f = J at f0
check("C2c: n-independent source first jet: n c_n f0^{n-1} = J for all n",
      sp.simplify(n*c_n*f0**(n-1) - J) == 0)

# sourceless residue: bulk-only difference is NOT contact; residue q(1-q)
Lp_b = sp.Rational(1,4)*y**2*sp.diff(f_phi, y)**2
Lf_b = sp.Rational(1,4)*y**2*sp.diff(f_f, y)**2
diffb = sp.simplify(jet(Lp_b,2) - jet(Lf_b,2))
# write as A(y) a^2 + B(y) (a^2)'; contact iff A = B'
A = sp.simplify(diffb.subs(sp.Derivative(a, y), 0)).coeff(a**2)
B = sp.expand(diffb).coeff(sp.Derivative(a, y))/ (2*a)  # coeff of (a^2)'=2aa'
residue = sp.simplify(A - sp.diff(B, y))
check("C2d: bulk-only jet2 difference has NON-contact residue exactly "
      "q(1-q) y^{-2q} a^2 (cancelled only by the criticality source jet)",
      sp.simplify(residue - q*(1-q)*y**(-2*q)) == 0)

# ---------- C2: hybrid (fixed-metric) refutation ----------
# Corpus def (native_weld_status_derivation.py build_L docstring): metric
# factors frozen at background; scalar slots (e^{-2phi} weight + gradients)
# varied.  Radial density: L_hyb = y^2 * f0 * e^{-2phi} * phi'^2
phi_h = phi0 + eps*a
L_hyb_bulk = y**2 * f0 * sp.exp(-2*phi_h) * sp.diff(phi_h, y)**2
# normalize: at eps=0 must equal bulk background density y^2 phi0'^2 f0^2
check("C2e: hybrid background density = y^2 phi0'^2 f0^2 (normalization)",
      sp.simplify(jet(L_hyb_bulk,0) - y**2*sp.diff(phi0,y)**2*f0**2) == 0)

# hybrid FIRST jet + (n-independent) source first jet in phi:
#   dS_src/dphi = -2 f0 * J  -> linear term  -2 f0 J * a
j1 = jet(L_hyb_bulk, 1) - 2*f0*J*a
# Euler-Lagrange residual of the linear functional: coeff(a) - d/dy coeff(a')
c_a = sp.expand(j1).coeff(a)
c_ap = sp.expand(j1).coeff(sp.Derivative(a, y))
el1 = sp.simplify(c_a - sp.diff(c_ap, y))
check("C2f: HYBRID jet-1 bulk residual = +(q^2/2) y^{-2q} under EVERY "
      "completion (source first jet is n-independent) — background not "
      "stationary in the hybrid prescription",
      sp.simplify(el1 - q**2/2 * y**(-2*q)) == 0)

# hybrid second jet -> SL mass; mu_hyb = -q^2/2 -> nu^2 = (1-2q^2)/q^2 = 7
j2 = jet(L_hyb_bulk, 2)
# L2 = K a'^2 + C a a' + M a^2 ; after IBP mass = M - (C/2)'
K2 = sp.expand(j2).coeff(sp.Derivative(a,y), 2)
C2_ = sp.expand(j2).coeff(sp.Derivative(a,y), 1).coeff(a)
M2 = sp.expand(j2).coeff(a, 2).subs(sp.Derivative(a,y), 0)
M_eff = sp.simplify(M2 - sp.diff(C2_/2, y))   # coeff of a^2 after IBP
check("C2g: hybrid kinetic weight = y^2 f0^2 (same as licensed jets)",
      sp.simplify(K2 - y**2*f0**2) == 0)
# operator: d(y^2 f0^2 a')' - M_eff a ; map a = -(1/2) y^q u =>
# mu = M_eff*y^{2q} - q(1-q)   [derived in C4 mapping algebra]
mu_hyb = sp.simplify(M_eff*y**(2*q) - q*(1-q))
check("C2h: hybrid mu = -q^2/2  =>  nu^2 = (1+4mu)/q^2 = (1-2q^2)/q^2 "
      "= 7 at q=1/3 (matches banked panel 'fixed-metric hybrid nu=sqrt7' "
      "— reconstruction confirmed against corpus)",
      mu_hyb == -q**2/2 and
      sp.simplify(((1+4*mu_hyb)/q**2).subs(q, sp.Rational(1,3))) == 7)

# mu_hyb not in licensed family at any q-independent n:
nsol = sp.solve(sp.Eq((1-n)*q*(1-q), -q**2/2), n)
check("C2i: no q-independent n matches the hybrid (n = (2-q)/(2(1-q)), "
      "q-dependent; = 5/4 at q=1/3)",
      len(nsol) == 1 and sp.simplify(nsol[0] - (2-q)/(2-2*q)) == 0
      and nsol[0].subs(q, sp.Rational(1,3)) == sp.Rational(5,4))

# ---------- C5 ----------
# (i) slot covariance of first jets: dS/dphi = -2 f dS/df for any S[f]
phi, k = sp.symbols('phi k')
fsym = sp.exp(-2*phi)
ok_pow = sp.simplify(sp.diff(fsym**k, phi) + 2*fsym*(k*fsym**(k-1))) == 0
ok_log = sp.simplify(sp.diff(sp.log(fsym), phi) + 2*fsym*(1/fsym)) == 0
check("C5a: chain rule d/dphi F(e^{-2phi}) = -2 f F'(f) for F = f^k "
      "(all k) and F = ln f (first jets slot-covariant; the whole "
      "licensed family)", ok_pow and ok_log)

# (ii) THE ATTACK: banked weld operator == SOURCELESS bulk Hessian in phi
# variables for GENERAL phi0 (no source ever varied).
P0 = sp.Function('P0')(y)              # general background phi0(y)
f0g = sp.exp(-2*P0)
phig = P0 + eps*a
Lg = y**2 * sp.diff(phig, y)**2 * sp.exp(-4*phig)   # sourceless C1 radial
j2g = jet(Lg, 2)
Kg = sp.expand(j2g).coeff(sp.Derivative(a,y), 2)
Cg = sp.expand(j2g).coeff(sp.Derivative(a,y), 1).coeff(a)
Mg = sp.expand(j2g).coeff(a, 2).subs(sp.Derivative(a,y), 0)
Mg_eff = sp.simplify(Mg - sp.diff(Cg/2, y))
E0g = sp.diff(P0, y, 2) + 2*sp.diff(P0, y)/y - 2*sp.diff(P0, y)**2
check("C5b: sourceless phi-Hessian mass = +4 y^2 f0^2 E0[phi0] for GENERAL "
      "phi0  => the banked weld operator d(r^2f^2 dphi')' - 4r^2f^2 E0 dphi "
      "is EXACTLY the sourceless bulk second jet in phi-variables: a "
      "second-jet object with ZERO source variation = the n=0 completion",
      sp.simplify(Mg_eff - 4*y**2*f0g**2*E0g) == 0)
check("C5c: kinetic weight y^2 f0^2 (matches banked d_r(r^2 f^2 d_r dphi))",
      sp.simplify(Kg - y**2*f0g**2) == 0)
check("C5d: E0 is the sourceless EL residual: EL_phi[sourceless] = "
      "-2 y^2 f0^2 E0 (so E0 != 0 marks an OFF-SHELL background for the "
      "sourceless action — the Hessian there is parametrization-ambiguous)",
      sp.simplify((sp.diff(Lg, eps).subs(eps,0).coeff(a)
                   - sp.diff(sp.expand(sp.diff(Lg, eps).subs(eps,0))
                             .coeff(sp.Derivative(a,y)), y))
                  + 2*y**2*f0g**2*E0g) == 0)

print(f"\nTOTAL: {PASS} PASS, {FAIL} FAIL")
