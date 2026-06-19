"""
B1_mass_charge_identities.py
=============================
ALGEBRAIC DERIVE + PROVENANCE AUDIT (TRACK B / STEP B1).
Agent: claude-opus-4-8[1m], 2026-06-19.  NOT canon.  Do NOT commit.

Purpose: EXACT symbolic verification (sympy, no grid/box/cutoff) of the
candidate "mass = dilation cost of the charge" identities pulled from the
corpus, and an explicit test of WHERE the chain closes natively vs where it
depends on an unaudited/imported object.

DATA-BLIND: no lepton wall numbers, no empirical mass/ratio loaded anywhere.

Everything here is a CHECK of corpus-stated relations, NOT a fit.
"""
import sympy as sp

print("="*70)
print("B1 mass<->charge algebraic identity checks (exact, no numerics-as-instrument)")
print("="*70)

# ----------------------------------------------------------------------
# Block 1: the area-form charge ladder N -> q -> eta (all DERIVED, banked)
# ----------------------------------------------------------------------
N = sp.symbols('N', positive=True, integer=True)

# Two independent locks claimed to force N=3 (h1_types_results.md):
#   Lock 1 (epsilon-singlet):  C(N,3) = 1  -> unique at N=3
#   Lock 2 (two-form operator): C(N^2,2) = 4 N^2  ->  N^2-1 = 8 -> N=3
binom = sp.binomial
lock1 = sp.Eq(binom(N,3), 1)
lock2 = sp.Eq(binom(N**2,2), 4*N**2)

sol1 = [s for s in sp.solve(binom(N,3)-1, N) if s==sp.Integer(3) or True]
# solve lock2 as a polynomial: N^2(N^2-1)/2 = 4N^2 -> N^2-1=8 (N!=0)
lock2_poly = sp.simplify(binom(N**2,2) - 4*N**2)
roots2 = sp.solve(sp.Eq(lock2_poly,0), N)
print("\n[1] N=3 locks")
print("  Lock1  C(N,3)=1 at N=3 ?     ", sp.binomial(3,3)==1, " (and C(2,3)=",sp.binomial(2,3),", C(4,3)=",sp.binomial(4,3),")")
print("  Lock2  C(N^2,2)=4N^2 roots:  ", roots2, " -> N=3 is the positive-integer root")
print("  Lock2 reduces to N^2-1=8:    ", sp.simplify(sp.binomial(N**2,2)/( N**2) - 4))  # = (N^2-1)/2 - 4 -> 0 at N^2=9

# q and eta as exact functions of N
q_of_N   = 1 - sp.Rational(2,1)/N           # q = 1 - 2/N
eta_of_N = q_of_N/6                          # eta = q/6
print("\n[2] charge ladder as exact functions of N")
print("  q(N)   = 1 - 2/N           -> q(3)   =", sp.nsimplify(q_of_N.subs(N,3)))
print("  eta(N) = q/6               -> eta(3) =", sp.nsimplify(eta_of_N.subs(N,3)))
print("  s(N)   = q^2                -> s(3)  =", sp.nsimplify((q_of_N**2).subs(N,3)))

# eta also claimed = 2/dim(Lambda^2 End(H1)) = 2/C(N^2,2); check N=3
eta_dim = 2/binom(N**2,2)
print("  eta via 2/dim Lambda^2End: ", sp.nsimplify(eta_dim.subs(N,3)),
      " == q/6 at N=3 ?", sp.simplify(eta_dim.subs(N,3)-eta_of_N.subs(N,3))==0)
# DOES the dim-formula equal q/6 for GENERAL N?  (N-specificity / TEST-B flavour)
print("  eta_dim == q/6 for general N ?", sp.simplify(eta_dim - eta_of_N)==0,
      "  (if False: the two eta-formulas agree ONLY at N=3 -> N-specific)")

# selector echo: q^2/4 == eta/2  iff q=1/3 (mass_audit 37-39) -- show it is NOT new info
q = sp.symbols('q', positive=True)
echo = sp.Eq(q**2/4, (q/6)/2)
print("\n[3] selector-echo (mass_audit): q^2/4 = (q/6)/2  solves to q =",
      sp.solve(q**2/4 - (q/6)/2, q), " -> the '1/36 triple' is q=1/3 restated (ZERO new weight)")

# ----------------------------------------------------------------------
# Block 2: Misner-Sharp mass as the dilation cost, EXACT closed form
# ----------------------------------------------------------------------
# m(r) = (c^2 r/2G)(1 - e^{-2 phi(r)})   [udt_canonical_geometry; macro stack]
# In the reduced weld variables (mass_audit:50): m(y,u) = (y/2)(1 - f),  f = e^{-2phi}
c, G, r, phi, y = sp.symbols('c G r phi y', positive=True)
f = sp.exp(-2*phi)
m_MS = (c**2 * r /(2*G))*(1 - f)
print("\n[4] Misner-Sharp mass (exact closed form in phi):")
print("  m(r) =", m_MS, "   = (c^2 r/2G)(1 - e^{-2 phi})")
print("  reduced weld form m(y,u) = (y/2)(1-f) :",
      sp.simplify(m_MS.subs({c:1,G:1,r:y}) - (y/2)*(1-f))==0)

# the EXACT "dilation cost" reading: the mass is literally (geom radius)/2
# times the DEFICIT of the dilation factor f=e^{-2phi} from unity.
# 1 - e^{-2phi} is the dilation cost; phi is the dilation potential.
# trapping/seal saturation: m = y/2 exactly as f->0 (mass_audit:54)
print("  seal limit f->0 (phi->+inf): m ->", sp.limit(m_MS.subs({c:1,G:1,r:y}), phi, sp.oo),
      " = y/2 (saturates trapping bound) -- EXACT")

# ----------------------------------------------------------------------
# Block 3: the bridge that B1 NEEDS -- does m close as a function of the
# topological charge N alone?  Test the candidate Q = 2 p_F = gamma = q.
# ----------------------------------------------------------------------
# Corpus chain (mass_audit:18-43, ensembles:36-40):
#   public charge Q = 2 p_F,  p_F = gamma/2  ->  Q = gamma
#   at mirror-matched MONOPOLE driving:  gamma = q  (FORCED monopole-sector only)
#   q = 1 - 2/N = 1/3 at N=3
# So IF gamma=q holds beyond the monopole sector, Q = q = 1 - 2/N : an EXACT
# functional of the topological charge N -> DISCRETE because N is.
gamma = sp.symbols('gamma', positive=True)
Q_charge = 2*(gamma/2)                       # Q = 2 p_F, p_F = gamma/2
print("\n[5] public-charge bridge")
print("  Q = 2 p_F, p_F = gamma/2  ->  Q =", sp.simplify(Q_charge), "= gamma")
print("  monopole lock gamma = q = 1 - 2/N  -> Q(N) =", (1 - sp.Rational(2,1)/N))
print("  Q(N=3) =", (1 - sp.Rational(2,1)/N).subs(N,3),
      "  DISCRETE because N is an integer (cohomology degree)")

# BUT: is p_F (hence the MS mass) actually = gamma, or only the *driving*=q?
# mass_audit:48  a(0) = (gamma^2 + c^2)/4   (weld action, NOT the mass)
# mass_audit:47  virial boundary term = gamma/4
# The MASS p_F is the y dM0/dy - M0 jet functional; gamma=q is the DRIVING.
# So Q=gamma ties the *charge label* to q, but the dimensionful MS MASS m
# still carries the scale (c^2 r/2G) and depends on the full phi(r), which is
# NOT fixed by N alone.  Make that explicit:
print("\n[6] OBSTRUCTION test: does m depend on phi(r) beyond the charge N?")
print("  m = (c^2 r/2G)(1 - e^{-2 phi(r)}) requires phi(r) AND a radius r.")
print("  N/q/eta fix the SLOPE of ln f at the collar (d ln f = -q d ln r),")
print("  i.e. phi(r) ~ (q/2) ln r + const near the seal, but the OVERALL")
print("  normalisation (the additive const of phi, the seal radius) is NOT")
print("  fixed by N.  -> a dimensionful prefactor remains free.")
# symbolic collar profile: d ln f = -q d ln r  =>  f = (r/r0)^{-q}  =>
# phi = -(1/2) ln f = (q/2) ln(r/r0).   m then:
r0 = sp.symbols('r0', positive=True)
f_collar = (r/r0)**(-q)                       # from d ln f = -q d ln r
phi_collar = -sp.Rational(1,2)*sp.log(f_collar)
m_collar = (c**2*r/(2*G))*(1 - f_collar)
print("  collar profile f=(r/r0)^{-q}, phi=(q/2)ln(r/r0):")
print("    m_collar =", sp.simplify(m_collar))
print("    -> still carries r, r0, c^2/G : NOT a pure function of N.")

# ----------------------------------------------------------------------
# Block 4: additivity-over-depth -- the banked REFUTATION (mass_audit:58-62)
# ----------------------------------------------------------------------
print("\n[7] additivity-over-depth: REFUTED in corpus (mass_audit:58-62).")
print("  'no plateau; last e-fold carries ~64%; A_tot diverges ~eps^{-1.3};")
print("   log-mass is NOT a bulk functional.'  -> a clean ADDITIVE charge->mass")
print("   accumulation (which a discrete-ladder mass formula would need) does")
print("   NOT hold for the bulk action object.  The MS mass p_F DOES converge")
print("   at threshold (eps^0), but as a WELD-JET functional, not a charge sum.")

print("\n" + "="*70)
print("DONE.  See B1_mass_dilation_cost_results.md for the audit + read.")
print("="*70)
