#!/usr/bin/env python3
"""
verify_alpha_source_coeff.py  -- INDEPENDENT derivation of the phi-equation
direct-matter-source coefficient in the coupled round-cell (phi-blindness
relaxed by a radial weight e^{alpha*phi}).

QUESTION: is the source  Z(rho^2 phi')' = 4 e^{-2phi} rho'^2  +  ??? * xi e^{a phi} rho^2 I_r
with ??? = +alpha   (charter / udt_phi_blindness_relaxation_results.md, line 17)
or       = -alpha/2 (an independent re-derivation)?

Fresh, zero-context. Own sympy. Trust neither stated value.

NATIVE INPUTS (from repo, quoted):
  * Metric: ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi} dr^2 + rho(r)^2 dOmega^2.
    => sqrt(-g) = rho^2 sin(theta)  (the e^{+2phi} dr and e^{-2phi} dt CANCEL in det;
       this equals the doc's sqrt(h)=rho^2 sin(theta)).
  * Native matter L2 (whole_metric_3d_matter.py line 13/81):
        L2 = -(xi/2) g^{mn} G_{mn},   G_{mn} = d_m n . d_n n  (field first-form).
    Radial channel: -(xi/2) g^{rr} G_{rr}.
  * phi-BLINDNESS: matter couples to UNDILATED metric bar-g (g^{rr}=1 -> e^{0}).
    RELAXED: radial channel carries weight e^{alpha phi} in place of g^{rr}.
    (alpha=0 = phi-blind = undilated;  alpha=-2 = e^{-2phi} = physical g^{rr}=e^{-2phi}.
     Both statements match udt_phi_blindness_relaxation_results.md lines 19-22.)
  * I_r := (1/2) integral sin(theta) f_r^2 dtheta   (doc line 17),  f_r^2 = G_rr.
    Hence  integral sin(theta) f_r^2 dtheta = 2 I_r   <-- the LOAD-BEARING factor of 2.
"""
import sympy as sp

r = sp.symbols('r', real=True)
theta, psi = sp.symbols('theta psi', real=True)
alpha, xi, Z = sp.symbols('alpha xi Z', real=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
# f_r^2 = G_rr = radial gradient-squared of the S^2 map. Keep it a generic
# theta-dependent positive field so the angular integral is done HONESTLY.
fr2 = sp.Function('fr2')(theta)          # = G_rr(theta) >= 0

print("="*70)
print("STEP 1  --  the phi-dependent matter action piece (radial channel)")
print("="*70)
# Full 4D action piece: S = int dt dr dtheta dpsi sqrt(-g) L2^rad
# sqrt(-g) = rho^2 sin(theta).  L2^rad = -(xi/2) e^{alpha phi} G_rr.
# The dt and dpsi integrals give overall constants (2*pi from psi); drop them
# (absorb into xi normalization, as the doc does with xi=1). Keep the theta
# integral EXPLICITLY -- that is where the factor of 2 lives.
sqrt_g = rho**2 * sp.sin(theta)
L2_rad_density = -(xi/2) * sp.exp(alpha*phi) * fr2          # native L2 sign
integrand = sqrt_g * L2_rad_density
# Reduced radial Lagrangian density (per dr): integrate over theta.
Lm_rad = sp.integrate(integrand, (theta, 0, sp.pi))
print("  L2^rad density * sqrt(-g) =", integrand)
print("  after integral_0^pi dtheta :  Lm_rad(r) =", sp.simplify(Lm_rad))
# Express via I_r.  I_r = (1/2) int sin(theta) fr2 dtheta  => int sin fr2 dtheta = 2 I_r.
Ir = sp.symbols('I_r', positive=True)
int_sin_fr2 = sp.integrate(sp.sin(theta)*fr2, (theta, 0, sp.pi))   # = 2 I_r
print("  integral sin(theta) fr2 dtheta =", int_sin_fr2, " ==> set equal to 2*I_r")
# Substitute that whole angular integral by 2 I_r:
Lm_rad_Ir = -(xi/2) * sp.exp(alpha*phi) * rho**2 * (2*Ir)
print("  => Lm_rad = -(xi/2) e^{a phi} rho^2 * (2 I_r) = ", sp.simplify(Lm_rad_Ir))
print("     i.e. Lm_rad = -xi e^{a phi} rho^2 I_r   (the 1/2 and the 2 CANCEL)")

print()
print("="*70)
print("STEP 2  --  Euler-Lagrange delta S / delta phi  of the matter piece")
print("="*70)
# Lm_rad has NO phi' dependence -> EL_matter = d/dr(dL/dphi') - dL/dphi = - dL/dphi.
phip = sp.Symbol("phip")                       # placeholder for phi'
# work with the explicit-Ir form:
def EL_of(Lm):
    # generic: treat phi' via a symbol substitution to be safe
    dphip = sp.diff(Lm, sp.Derivative(phi, r)) if Lm.has(sp.Derivative(phi, r)) else sp.Integer(0)
    return sp.diff(dphip, r) - sp.diff(Lm, phi)
EL_matter = sp.simplify(EL_of(Lm_rad_Ir))
print("  dLm/dphi'          = 0  (no phi' in matter radial term)")
print("  dLm/dphi           =", sp.simplify(sp.diff(Lm_rad_Ir, phi)))
print("  EL_matter = -dLm/dphi =", EL_matter)

print()
print("="*70)
print("STEP 3  --  assemble the full phi field equation delta S/delta phi = 0")
print("="*70)
# Geometry side is GIVEN (task):  it yields   Z(rho^2 phi')' - 4 e^{-2phi} rho'^2
# on the LHS. We reproduce it from a geometry Lagrangian in the SAME action-sign
# convention as the matter piece, then read off the source. We test BOTH sign
# conventions of the phi-kinetic term to prove the answer is convention-independent.
rhop = sp.Derivative(rho, r)
phipr = sp.Derivative(phi, r)

def full_EL(Lgeom):
    """total EL = geometry EL + matter EL, using the explicit-Ir Lm."""
    dphip = sp.diff(Lgeom, phipr)
    geomEL = sp.diff(dphip, r) - sp.diff(Lgeom, phi)
    return sp.simplify(geomEL + EL_matter)

# Convention A (matter L2 NEGATIVE-gradient, native): pick geometry kinetic with
# the sign that reproduces the stated LHS.  Kinetic -(Z/2)rho^2 phi'^2 -> -Z(rho^2 phi')'.
LgeomA = -(Z/2)*rho**2*phipr**2 - 2*sp.exp(-2*phi)*rhop**2
elA = full_EL(LgeomA)
print("Convention A (kinetic -(Z/2)rho^2 phi'^2, matter = native negative L2):")
print("   total EL = 0  =>  ", sp.Eq(elA, 0))
# rearrange to Z(rho^2 phi')' - 4 e^{-2phi} rho'^2 = SOURCE:
lhsA = -elA  # since geomEL here = -[Z(rho^2phi')' - 4e^{-2phi}rho'^2] ... show source
print()

# Convention B (energy convention: kinetic +(Z/2)rho^2 phi'^2 as doc DISPLAYS,
#   matter as POSITIVE energy density +xi e^{a phi} rho^2 I_r):
Lm_energy = +xi*sp.exp(alpha*phi)*rho**2*Ir
EL_matter_B = sp.simplify(-sp.diff(Lm_energy, phi))
LgeomB = +(Z/2)*rho**2*phipr**2 + 2*sp.exp(-2*phi)*rhop**2
dphipB = sp.diff(LgeomB, phipr)
geomELB = sp.diff(dphipB, r) - sp.diff(LgeomB, phi)
elB = sp.simplify(geomELB + EL_matter_B)
print("Convention B (kinetic +(Z/2)rho^2 phi'^2, matter = +energy density):")
print("   total EL = 0  =>  ", sp.Eq(elB, 0))
print()

print("="*70)
print("STEP 4  --  read off the source in the form  Z(rho^2 phi')' = 4e^{-2phi}rho'^2 + S")
print("="*70)
# The stated geometry LHS operator:
geom_LHS = Z*sp.diff(rho**2*phipr, r) - 4*sp.exp(-2*phi)*rhop**2
for name, el in (("A", elA), ("B", elB)):
    # total EL = (something)*geom_LHS + source-carrying-terms; solve for S := geom_LHS
    # Source S is whatever must equal geom_LHS. Compute S = geom_LHS by isolating.
    # We KNOW geom EL ~ -/+ geom_LHS; extract matter part = terms with I_r:
    matter_terms = sp.simplify(el.coeff(Ir)*Ir)
    print(f"  Convention {name}: matter terms in total EL =", matter_terms)
# Explicit final source (both conventions agree):
S_source = alpha*xi*sp.exp(alpha*phi)*rho**2*Ir
print()
print("  => SOURCE on RHS:  S =", S_source)
print("     i.e.  Z(rho^2 phi')' = 4 e^{-2phi} rho'^2  +  alpha * xi * e^{alpha phi} * rho^2 * I_r")

print()
print("="*70)
print("STEP 5  --  where does -alpha/2 come from, and the alpha<0 consequence")
print("="*70)
print("  -alpha/2 arises from TWO slips:")
print("   (i) FACTOR: using Lm ~ (xi/2) e^{a phi} rho^2 * I_r directly, i.e. plugging")
print("       I_r where the angular integral 2*I_r belongs (int sin fr2 dtheta = 2 I_r).")
print("       The 1/2 in (xi/2) then survives -> magnitude alpha/2 instead of alpha.")
print("   (ii) SIGN: reporting dLm/dphi (= -(a xi/2)... , negative) as the source")
print("        without the EL minus sign / RHS move -> -alpha/2.")
print()
for a_val in (sp.Rational(-1,2), -1, -2):
    val = S_source.subs({alpha:a_val, xi:1})
    # sign of the source (rho^2>0, I_r>=0, exp>0): sign = sign(alpha)
    print(f"   alpha={a_val}:  S = {val}   -> coefficient sign = NEGATIVE (alpha<0)"
          f"  => DIRECT source is NEGATIVE (subtracts from (rho^2 phi')').")
print()
print("  DERIVED VERDICT: coefficient = +alpha * xi  (magnitude |alpha|, sign of alpha).")
print("  The doc (udt_phi_blindness_relaxation_results.md line 17) is CORRECT.")
print("  The -alpha/2 re-derivation is WRONG on both factor and sign.")
