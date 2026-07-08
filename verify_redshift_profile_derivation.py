"""
ADVERSARIAL verification of the claim:
  observer-equivalence (R1)  =>  dphi/ds = const = k  =>  phi(r) = -ln(1 - k r),
  1+z = 1/(1-kr), horizon at r=1/k with INFINITE proper distance.

Data-blind: k is a free scale; no 1101/7.004/lepton numbers used.
Independent re-derivation with sympy. Written to repo dir per task.
"""
import sympy as sp

r, s, k, C, phi = sp.symbols('r s k C phi', real=True)
kp = sp.symbols('k', positive=True)

print("="*70)
print("STEP 2 -- algebra: dphi/ds = k, ds = e^{phi} dr  =>  phi(r)")
print("="*70)
# ds = e^{phi} dr  (from g_rr = e^{2phi}, proper length dL = sqrt(g_rr) dr)
# dphi/dr = (dphi/ds)(ds/dr) = k * e^{phi}
phi_r = sp.Function('phi')
ode = sp.Eq(phi_r(r).diff(r), k*sp.exp(phi_r(r)))
print("ODE:  dphi/dr = k e^{phi}   ->", ode)
sol = sp.dsolve(ode, phi_r(r))
print("general solution:", sol)
# Apply BC phi(0)=0 by hand on the separated integral:  -e^{-phi} = k r + C
# BC: -e^0 = 0 + C -> C=-1  => e^{-phi}=1-kr
cand = -sp.log(1 - k*r)          # proposed phi(r)
lhs = sp.diff(cand, r)
rhs = k*sp.exp(cand)
print("check phi=-ln(1-kr) satisfies ODE:  dphi/dr - k e^phi =",
      sp.simplify(lhs - rhs))
print("BC phi(0):", sp.simplify(cand.subs(r,0)))
print("e^{-phi}  =", sp.simplify(sp.exp(-cand)), " (want 1-kr)")
print("1+z=e^phi =", sp.simplify(sp.exp(cand)), " (want 1/(1-kr))")

print()
print("="*70)
print("STEP 3 -- horizon r=1/k and proper distance to it")
print("="*70)
# horizon where phi->inf: e^{-phi}=1-kr=0 -> r=1/k
integrand = sp.exp(-sp.log(1-kp*r))    # e^{phi} = 1/(1-kr)
print("integrand e^{phi} = 1/(1-kr) =", sp.simplify(integrand))
s_of_r = sp.integrate(integrand, r)
print("indefinite proper distance s(r) =", sp.simplify(s_of_r))
proper = sp.integrate(integrand, (r, 0, 1/kp))
print("proper distance 0 -> 1/k  =", proper, " (want +oo)")
# also: dphi/ds=k  =>  s = phi/k, and phi->inf => s->inf  (cleanest statement)
print("cleanest: dphi/ds=k => s=phi/k; phi->inf => s->inf  (trivially divergent)")

print()
print("="*70)
print("STEP 4 -- guard vs de Sitter form phi=-1/2 ln(1-kr^2)")
print("="*70)
dS = -sp.Rational(1,2)*sp.log(1-k*r**2)
print("de Sitter phi =", dS, "  distinct function? ", sp.simplify(dS-cand)!=0)
# does de Sitter satisfy dphi/ds=const?  dphi/ds = e^{-phi} dphi/dr
dphi_ds_dS = sp.simplify(sp.exp(-dS)*sp.diff(dS, r))
print("de Sitter dphi/ds =", dphi_ds_dS, " (r-dependent => NOT homogeneous)")
dphi_ds_cand = sp.simplify(sp.exp(-cand)*sp.diff(cand, r))
print("candidate dphi/ds =", dphi_ds_cand, " (constant = k => homogeneous) OK")

print()
print("="*70)
print("STEP 1 -- the LOGIC.  Two readings of 'no privileged position'.")
print("="*70)
print("""(a) DOC's R1 as formalized (relrederiv §1a, lines 57-60): D depends only
    on Delta-phi = phi_B - phi_A  <=> shifting ALL phi by a constant leaves
    dilations unchanged (ADDITIVE GAUGE freedom of phi).  This constrains the
    phi-DEPENDENCE (=> exp FORM), NOT the spatial profile phi(r).
    TEST: does the LEGACY cubic satisfy (a) yet have non-constant dphi/ds?""")
mug = sp.symbols('mu_g', positive=True)
cubic = sp.Rational(3,2)*mug*r - sp.cos(sp.pi/5)*mug**2*r**2 + sp.Rational(2,3)*mug**3*r**3
dphi_ds_cubic = sp.simplify(sp.exp(-cubic)*sp.diff(cubic, r))
print("    legacy cubic dphi/ds =", dphi_ds_cubic)
print("    -> r-dependent, NOT constant. Yet g_tt=-e^{-2phi}c^2 (the exp form,")
print("       hence R1(a)) holds for it.  => R1(a) does NOT force dphi/ds=const.")
print("""
(b) STRONG homogeneity: the redshift-vs-PROPER-DISTANCE law z(delta) is the
    identical function for EVERY observer. Cauchy argument:
      1+z from observer at s0 to source at s0+delta = e^{phi(s0+delta)-phi(s0)}
      homogeneity: phi(s0+delta)-phi(s0) = psi(delta)  for all s0
      => phi(s+delta)=phi(s)+psi(delta); s=0: phi(delta)=psi(delta)
      => phi(s+delta)=phi(s)+phi(delta)  (additive Cauchy in PROPER distance)
      => phi(s)=k*s (regularity)  => dphi/ds=k. SOUND.""")
# symbolic Cauchy closure check in proper-distance variable
s0, d = sp.symbols('s0 delta', real=True)
psi = sp.Function('psi')
# if phi(s)=k s then increment depends only on delta:
inc = k*(s0+d) - k*s0
print("    check: phi=k*s gives increment", sp.simplify(inc), "= k*delta (s0-free) OK")
print("""
VERDICT step1: (b) is SOUND and uses the SAME functional-equation machinery as
    §1a, but in the PROPER-DISTANCE variable (physical, gauge-invariant). It
    requires a SEPARATE homogeneity postulate NOT contained in the doc's
    gauge-reading R1. Claiming it 'follows from R1' (the form-fixer) is an
    OVER-EXTENSION; claiming it follows from an added 'identical law for every
    observer in proper distance' postulate is CORRECT. Also note homogeneity
    stated in COORDINATE r would instead give phi=k*r (different) -> the result
    is tied to PROPER distance + the g_rr=e^{2phi} radial gauge.""")
