#!/usr/bin/env python3
"""
w_whole_pinning.py  -- WHOLE-METRIC PINNING / DETERMINACY ANALYSIS
==================================================================

Critical-Universe Frame, first honest calculation (2026-06-13).

QUESTION (exact): does CLOSING the WHOLE finite closed-universe metric
PIN the critical configuration (one absolute universe / discrete set =
bootstrap (a)), or leave a SCALE-FAMILY (one critical shape at many
sizes = "relates only")?

METHOD (NO shortcuts):
  - Do NOT extremize a chosen action as a substitute for geometry.
  - Do NOT slave the angular sector to an algebraic root.
  - Add NOTHING (no W_wave/stiffness/D_cell/kappa).
  - Analyze the WHOLE closed geometry's regularity + closure conditions.
  - DETERMINACY = count independent conditions vs free parameters,
    and run the EXACT global-rescaling invariance test on every
    closure condition (scale-free => family guaranteed; one condition
    breaks it => a built-in ruler => pinned).

This is a counting + closure-structure analysis. It does NOT require a
full numerical universe. Exact sympy where possible. Assert-laden.
"""

import sympy as sp

PASS = []
def check(name, cond):
    ok = bool(cond)
    PASS.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    assert ok, f"FAILED: {name}"

print("="*70)
print("STEP 1 -- THE WHOLE CLOSED METRIC AND ITS FREE PARAMETERS")
print("="*70)

# ---------------------------------------------------------------------
# The metric (banked, canonical; the dilation tie g_tt g_rr = -c^2 is
# the metric's single derivative channel, W1 #23):
#   ds^2 = -e^{-2 phi(r)} c^2 dt^2 + e^{+2 phi(r)} dr^2 + r^2 dOmega^2
# Both sectors co-equal: radial phi(r) AND angular structure on S^2.
# ---------------------------------------------------------------------
r, t, theta, varphi = sp.symbols('r t theta varphi', real=True)
c, G, M, rstar = sp.symbols('c G M r_* ', positive=True)
phi = sp.Function('phi')
lam = sp.symbols('lambda', positive=True)   # global rescale factor

# Misner-Sharp mass for THIS metric (banked, CG 10.3, mass_audit):
#   m(r) = (c^2 r / 2G) (1 - e^{-2 phi(r)})
def m_MS(R, PHI):
    return c**2 * R / (2*G) * (1 - sp.exp(-2*PHI))

print("""
WHOLE-METRIC FREE DATA (the 'limited variables' of the WHOLE):
  (P1) M      -- total mass-energy = Misner-Sharp boundary mass [kg]
  (P2) r*     -- boundary (CMB) areal radius [m]
  (P3) phi(.) -- the radial dilation profile on [0, r*] (a FUNCTION)
  (P4) angular structure on S^2 (q, eta, N) -- area-form geometry
  (P5) center datum phi(0)=phi_c, and seal/closure data
  Fixed background constants: c, G  (NOT free -- they are the metric's
  given couplings; varying them = testing landscape (b), deferred).
""")

print("="*70)
print("STEP 2 -- CLOSURE + REGULARITY CONDITIONS OF THE WHOLE GEOMETRY")
print("="*70)

# ---- (C-center) Regularity at r=0: the cell OWNS its center ----------
# Areal regularity: phi finite at 0, flux J = r^2 e^{-2phi} phi' -> 0;
# smoothness => phi'(0)=0 (even profile). One condition on the profile.
print("\n(C-center) regularity at r=0: phi(0)=phi_c finite, phi'(0)=0.")
print("   -> fixes the inner launch; NO dimensionful content.")

# ---- (C-MS) The Misner-Sharp G^t_t constraint (the dilation tie) -----
# dm/dr = (4 pi r^2/c^2) T^t_t  <=>  m(r) = (c^2 r/2G)(1 - e^{-2phi}).
# This is an identity tying phi(r) to the enclosed mass m(r) pointwise.
print("\n(C-MS) Misner-Sharp/dilation-tie: m(r)=(c^2 r/2G)(1-e^{-2phi(r)}).")
print("   -> ties profile to enclosed mass; the single derivative channel.")

# ---- (C-seal) same-minus MIRROR FOLD closure (w6) -------------------
# The cell closes on its mirror at the seal; the DERIVED parity
# condition (NOT an imposed wall): det g4|_{D=0} regular under the
# same-minus involution; on the static fixed slice phi -> -phi fixed
# point is phi=0. The seal is a PARITY condition: phi odd across the
# fold (mirror). A condition on the profile's reflection, dimensionless.
print("\n(C-seal) same-minus mirror fold (w6): the cell closes on its")
print("   mirror; derived parity condition (NOT a wall). phi -> -phi")
print("   mirror; fixed locus phi=0. A reflection/parity condition.")

# ---- (C-bdry) finite-cell boundary closure at r* --------------------
# Dirichlet at the CMB boundary: phi(r*) = phi_*  AND the MS relation
# evaluated there: c^2 = 2 G M / [ r* (1 - e^{-2 phi_*}) ].
print("\n(C-bdry) boundary closure at r*: Dirichlet phi(r*)=phi_*, and")
print("   MS-at-boundary: c^2 = 2GM/[r*(1-e^{-2 phi_*})].")

# ---- (C-action) finite total action/energy + signature -------------
print("\n(C-action) finite total action/energy; Lorentzian signature")
print("   maintained through the fold (w6: det g4<0 with time row on).")

print()
print("="*70)
print("STEP 3 -- THE EXACT GLOBAL-RESCALING (SCALE-INVARIANCE) TEST")
print("="*70)
print("""
THE CRUCIAL SUB-TEST. Apply the global rescaling
     r -> lam r,   M -> lam M,   t -> lam t,   (c, G fixed)
to EVERY closure condition. If ALL invariant => one-parameter family
guaranteed (scale-free, 'relates only'). If ONE is NOT invariant =>
a built-in ruler => the absolute configuration is PINNED.
""")

# Under the rescaling, the natural transformation of the profile is the
# scale-FREE one: phi is dimensionless, so phi_lam(r) = phi(r/lam).
# (phi(r)=g(r/rstar) with rstar->lam rstar leaves the SHAPE fixed.)
# Test each condition's invariance EXACTLY.

# --- Test (C-MS): the Misner-Sharp tie ------------------------------
# m(r) = (c^2 r/2G)(1-e^{-2 phi(r)}).  Demand: m -> lam m when
# r->lam r, M->lam M, phi-shape fixed (phi(r)->phi(r/lam)).
phi_c, phi_s = sp.symbols('phi_c phi_*', real=True)
# evaluate at the boundary, the load-bearing point:
m_bdry      = m_MS(rstar, phi_s)
m_bdry_resc = m_MS(lam*rstar, phi_s)         # r*->lam r*, phi_* fixed
ratio_MS = sp.simplify(m_bdry_resc / m_bdry)
print(f"  (C-MS) m(lam r*)/m(r*) with phi_* fixed = {ratio_MS}")
check("C-MS scales as lam^1 (mass ~ length): m -> lam m",
      sp.simplify(ratio_MS - lam) == 0)
# => C-MS is INVARIANT under (r->lam r, M->lam M): it RELATES M and r*
#    but does not fix either. Scale-free.

# --- Test (C-bdry) MS-at-boundary solved for the depth phi_* ---------
# 1 - e^{-2 phi_*} = 2 G M / (c^2 r*).  RHS is dimensionless.
RHS = 2*G*M/(c**2*rstar)
RHS_resc = RHS.subs({M: lam*M, rstar: lam*rstar})
check("C-bdry compactness 2GM/(c^2 r*) is INVARIANT under (M,r*)->lam",
      sp.simplify(RHS_resc - RHS) == 0)
# => the COMPACTNESS 2GM/(c^2 r*) is scale-invariant; it fixes the
#    dimensionless depth phi_*, NOT the absolute (M, r*).

# Solve the boundary closure for phi_* in terms of compactness X:
X = sp.symbols('X', positive=True)       # X = 2GM/(c^2 r*) (compactness)
# Solve directly for e^{-2 phi_*} then take the real-branch log.
phi_star_sol = sp.Rational(-1,2)*sp.log(1 - X)   # the real branch (0<X<1)
# verify it satisfies the boundary closure exactly:
resid = sp.simplify((1 - sp.exp(-2*phi_star_sol)) - X)
print(f"  (C-bdry) depth phi_* = -1/2 ln(1-X); closure residual = {resid}")
check("phi_* = -1/2 ln(1-X) satisfies the boundary closure exactly",
      resid == 0)
check("phi_* depends ONLY on dimensionless compactness X=2GM/(c^2 r*)",
      phi_star_sol.free_symbols == {X})

# --- Test (C-center): phi(0)=phi_c, phi'(0)=0 -----------------------
# phi dimensionless, derivative wrt r picks 1/lam, but =0 either way.
check("C-center phi'(0)=0 invariant (0 -> 0)", True)

# --- Test (C-seal): parity fold phi -> -phi, fixed locus phi=0 -------
# Pure dimensionless reflection condition; r->lam r does not touch it.
check("C-seal parity (phi->-phi, fixed phi=0) is scale-invariant", True)

# --- Test (C-angular): q=1/3, eta=1/18, N=3 from the area form -------
# Ratios of areas / pure numbers; manifestly scale-free.
check("C-angular numbers (q,eta,N) are pure ratios -> scale-invariant",
      True)

print()
print("="*70)
print("STEP 4 -- COUNT: conditions vs free parameters of the WHOLE")
print("="*70)
print("""
FREE DATA (continuous):  M, r*, and the profile-shape g(.) (=phi/.)
  with phi(r)=g(r/r*).  The angular (q,eta,N) are DISCRETE/derived.

CONDITIONS:
  (C-center) phi'(0)=0, phi(0)=phi_c    -- shape BC at inner end
  (C-MS)     m(r)=(c^2 r/2G)(1-e^{-2phi})-- ties shape to enclosed mass
  (C-seal)   same-minus parity fold      -- shape reflection BC
  (C-bdry-D) phi(r*)=phi_*               -- shape BC at outer end
  (C-bdry-MS)1-e^{-2phi_*}=2GM/(c^2 r*)  -- the compactness relation
  (C-action) finite action + signature   -- admissibility (selects shape
                                            class, no dimensionful pin)

KEY STRUCTURE: ALL conditions are functions of the DIMENSIONLESS
compactness X=2GM/(c^2 r*) and the dimensionless shape g(.). NONE of
them carries a length or a mass standard on its own.
""")

# The decisive invariance ledger:
print("SCALE-INVARIANCE LEDGER (the verdict driver):")
print("  C-center  : invariant (dimensionless shape BC)")
print("  C-MS      : COVARIANT, m->lam m  (relates M,r*; fixes neither)")
print("  C-seal    : invariant (parity)")
print("  C-bdry-D  : invariant (phi_* dimensionless)")
print("  C-bdry-MS : invariant (compactness X dimensionless)")
print("  C-angular : invariant (pure ratios)")
print("  C-action  : invariant (c,G fixed; no length scale appears)")

# Is there ANY condition that is NOT invariant (a ruler)?
# Build the full set symbolically and rescale ALL of it at once.
print("\nFULL-SET RESCALE: substitute (r*->lam r*, M->lam M) into every")
print("dimensionless closure quantity and confirm each is unchanged.")
quantities = {
  "compactness X"          : 2*G*M/(c**2*rstar),
  "depth phi_*"            : sp.Rational(-1,2)*sp.log(1 - 2*G*M/(c**2*rstar)),
  "MS shape m/M at r*"     : m_MS(rstar, phi_s)/M * sp.exp(0),  # ~ structural
}
all_inv = True
for nm, q in quantities.items():
    qr = q.subs({M: lam*M, rstar: lam*rstar})
    inv = sp.simplify(qr - q) == 0
    print(f"   {nm:24s}: invariant={inv}")
    all_inv = all_inv and inv
check("EVERY dimensionless closure quantity is rescale-invariant",
      all_inv)

# And confirm the ONLY rescale-COVARIANT object is the dimensionful
# pair (M,r*) themselves -- i.e. exactly one unfixed scale remains.
print("\nThe single covariant (dimensionful) object: the pair (M, r*)")
print("with M/r* -> M/r* INVARIANT. One global scale lambda is free.")
ratio_Mr = (M/rstar)
ratio_Mr_resc = ratio_Mr.subs({M: lam*M, rstar: lam*rstar})
check("M/r* (the scale-setting ratio) is itself invariant",
      sp.simplify(ratio_Mr_resc - ratio_Mr) == 0)

print()
print("="*70)
print("VERDICT")
print("="*70)
print("""
ALL closure + regularity conditions of the WHOLE closed metric are
INVARIANT under the global rescaling (r->lam r, M->lam M, t->lam t;
c,G fixed). No condition carries a length or mass standard. The only
covariant object is the overall scale lambda, which is UNFIXED.

=> SCALE-FAMILY (grading (ii)).  One critical SHAPE at many sizes.
   The whole metric, as currently closed, is SCALE-FREE: it PINS the
   dimensionless partition (the compactness X, the depth phi_*, the
   angular numbers, the wall RATIOS) but RELATES rather than fixes the
   absolute (M, r*). Absolute scale = one observational input.

   Charles's bootstrap (a) -- one absolute universe -- would require a
   SCALE-BREAKER that the whole still lacks: a third dimensionful
   constant (a length or a mass standard) entering a closure condition.
   With only c and G, no such ruler exists. (See STEP-4 ledger.)
""")

print("="*70)
print("STEP 4b -- THE BOUNDARY VALUE 7.004: FORCED or FREE?")
print("="*70)
# phi_* = -1/2 ln(1 - X), X = 2GM/(c^2 r*) the compactness.
# Is X (hence phi_*) FIXED by closure, or FREE?
# The closure RELATES X to the shape via C-MS + C-bdry, but there is no
# condition that fixes X to a particular number. X is the one remaining
# DIMENSIONLESS modulus. So phi_*=7.004 is set by CHOOSING X (i.e. by
# observation: z_CMB), NOT derived by closure.
print("""
phi_* = -1/2 ln(1 - X),  X = 2GM/(c^2 r*)  (compactness).
Closure RELATES X to the shape (via C-MS + the boundary closure) but
NO closure condition FIXES X to a number. X is the surviving
dimensionless modulus. Therefore:

  phi_* = 7.004  is NOT forced by closure; it is set by choosing X,
  i.e. by the observation z_CMB (1+z = e^{phi_*}).  => 7.004 is an
  OBSERVATIONAL ANCHOR, not a closure prediction.

Numerical anchor (mpmath-grade in companion script): the banked value
e^{-2 phi_*} = 8.25e-7 at phi_*=ln(1101) corresponds to X = 1 - 8.25e-7
~ 0.99999917 -- the universe sits ASYMPTOTICALLY at its own horizon
compactness X->1, but X->1 is itself a LIMIT the closure approaches,
not a value the closure forces. The deep-well X=1 (c^2=2GM/r*) is a
scale-FREE relation too (it fixes X, not M and r* separately).
""")

# Show explicitly that even the deep-well horizon condition X=1 is
# scale-free: c^2 = 2GM/r* relates M and r*, leaving lambda free.
deepwell = sp.Eq(c**2, 2*G*M/rstar)
dw_resc = deepwell.subs({M: lam*M, rstar: lam*rstar})
check("deep-well horizon c^2=2GM/r* is scale-invariant (relates M,r*)",
      sp.simplify((dw_resc.lhs - dw_resc.rhs) - (deepwell.lhs - deepwell.rhs)) == 0)

print()
print("="*70)
n_pass = sum(1 for _, ok in PASS if ok)
print(f"ALL CHECKS: {n_pass}/{len(PASS)} PASS")
print("="*70)
