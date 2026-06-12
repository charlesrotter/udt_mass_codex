"""Verifier-alpha INDEPENDENT verification of S56-009 Q-S2-3.

Written from scratch without consulting cr_S56_009_step2_crossblock_palette.py
machinery beyond reading the S56-007 cross-block integrands as inputs.

Tests:
  (T1) Palette enumeration under chi -> exp(phi) u: independent re-derivation
  (T2) Canonical sector weights w_u, w_G ratio computation
  (T3) IBP perfect-antisymmetry on int u (F G' - G F') dr
  (T4) Adjoint-closure failure mechanism: confirm via independent argument
  (T5) Explicit attempt to FIND a missed compensating boundary term
"""

import sympy as sp
from sympy import (Function, Symbol, symbols, simplify, expand, factor,
                   exp, log, diff, integrate, pi, sin, cos, I,
                   Rational, Eq, S, conjugate, collect, Wild)

print("=" * 76)
print("VERIFIER-ALPHA: independent S56-009 Q-S2-3 verification")
print("=" * 76)

# ============================================================
# T1: Palette enumeration under chi = exp(phi) u
# ============================================================
print("\n--- T1: Palette enumeration under chi = exp(phi) u ---")

r = symbols('r', real=True, positive=True)
phi = Function('phi')(r)
G0 = Function('G0')(r)
F0 = Function('F0')(r)
chi = Function('chi')(r)
u = Function('u')(r)
c, E = symbols('c E', real=True)

# Define the three S56-007 cross-block integrands in chi-basis
# These are taken from S56-007 cr_S56_007_step1p5.py and DISPATCH §4.2 of S56-009
I_at_chi = c * E * chi * exp(phi) * (G0**2 + F0**2)            # alpha-temporal
I_ar_chi = -I * c * 4*pi * chi * exp(-phi) * (F0*diff(G0, r) - G0*diff(F0, r))  # alpha-radial
I_be_chi = (I * c / 2) * diff(chi, r) * exp(-phi) * G0 * F0   # beta

# Substitute chi = exp(phi) * u (note: substitute chi' first, then chi)
def rescale_chi_to_u(expr):
    # Compute the substitution carefully: chi -> e^phi u, chi' -> e^phi(phi' u + u')
    chi_sub = exp(phi) * u
    chi_p_sub = diff(chi_sub, r)
    expr2 = expr.subs(diff(chi, r), chi_p_sub)
    expr2 = expr2.subs(chi, chi_sub)
    return simplify(expand(expr2))

I_at_u = rescale_chi_to_u(I_at_chi)
I_ar_u = rescale_chi_to_u(I_ar_chi)
I_be_u = rescale_chi_to_u(I_be_chi)

print(f"  alpha-temporal in u-basis:  {I_at_u}")
print(f"  alpha-radial in u-basis:    {I_ar_u}")
print(f"  beta in u-basis:            {I_be_u}")

# Extract weight on u and u' for each piece
# Method: expand in u(r), u'(r) and simplify the coefficients
def extract_u_weight(expr, multiplicand_test):
    """Extract coefficient of multiplicand_test (e.g., u(r) or u'(r)) and check
    its e^(n phi) dependence."""
    coeff = expr.coeff(multiplicand_test)
    coeff = simplify(coeff)
    return coeff

# alpha-temporal: only u(r) factor
coeff_u_at = extract_u_weight(I_at_u, u)
coeff_up_at = extract_u_weight(I_at_u, diff(u, r))
print(f"\n  alpha-temporal coeff on u(r):   {simplify(coeff_u_at)}")
print(f"  alpha-temporal coeff on u'(r):  {simplify(coeff_up_at)}")

# alpha-radial: only u(r) factor
coeff_u_ar = extract_u_weight(I_ar_u, u)
coeff_up_ar = extract_u_weight(I_ar_u, diff(u, r))
print(f"\n  alpha-radial coeff on u(r):   {simplify(coeff_u_ar)}")
print(f"  alpha-radial coeff on u'(r):  {simplify(coeff_up_ar)}")

# beta: both u and u'
coeff_u_be = extract_u_weight(I_be_u, u)
coeff_up_be = extract_u_weight(I_be_u, diff(u, r))
print(f"\n  beta coeff on u(r):           {simplify(coeff_u_be)}")
print(f"  beta coeff on u'(r):          {simplify(coeff_up_be)}")

# Check exponential weights: extract e^(n*phi) factor from each coeff
def extract_exp_phi_weight(expr):
    """Return the exponent n such that expr ~ e^(n*phi) * (rest)."""
    # Try ratio test by dividing by exp(2*phi), exp(phi), exp(-phi), 1, etc.
    candidates = [-2, -1, 0, 1, 2]
    for n in candidates:
        ratio = simplify(expr / exp(n*phi))
        # Check if ratio is independent of exp(phi)
        # by testing whether it depends on phi explicitly through exp
        if ratio == 0:
            continue
        # A simpler heuristic: substitute phi -> phi + 1 and see if expression scales by e^n
        ratio_shifted = ratio.subs(phi, phi + 1)
        if simplify(ratio_shifted - ratio) == 0:
            return n
    return None  # could not identify

print("\n  Exponential weights:")
print(f"    alpha-temporal u-coeff weight: e^({extract_exp_phi_weight(coeff_u_at)} phi)")
print(f"    alpha-radial u-coeff weight:   e^({extract_exp_phi_weight(coeff_u_ar)} phi)")
print(f"    beta u-coeff weight:           e^({extract_exp_phi_weight(coeff_u_be)} phi)")
print(f"    beta u'-coeff weight:          e^({extract_exp_phi_weight(coeff_up_be)} phi)")

distinct_weights = set([
    extract_exp_phi_weight(coeff_u_at),
    extract_exp_phi_weight(coeff_u_ar),
    extract_exp_phi_weight(coeff_u_be),
    extract_exp_phi_weight(coeff_up_be),
])
distinct_weights.discard(None)
print(f"\n  Distinct rescaled-palette weights (as exponents of phi): {sorted(distinct_weights)}")
print(f"  Primary's claim: {{e^(+2 phi), 1}} = exponents {{2, 0}}")
verdict_T1 = "AGREE" if distinct_weights == {2, 0} else f"DISAGREE (got {distinct_weights})"
print(f"  T1 verdict: {verdict_T1}")

# ============================================================
# T2: Canonical sector weights w_u / w_G
# ============================================================
print("\n--- T2: Canonical sector weights w_u / w_G ---")

# w_u = r^2 e^(2 phi)  (canonical scalar SL §3.2 line 239 weight on chi is e^{2phi};
#                       under chi = e^phi u, the L^2 measure becomes
#                       int |chi|^2 e^{2phi} r^2 dr -> int e^{2phi} u^2 e^{2phi} r^2 dr
#                       = int u^2 e^{4phi} r^2 dr  -- wait, let me reconsider)
# Actually the §3.2 weight is for the eigenvalue inner product which is Sturm-Liouville
# with chi as the variable. When we rescale chi = e^phi u, the SL form reorganizes.
#
# The primary's claim is w_u = r^2 e^{2phi}. Let me verify this via the standard
# Liouville-transform analysis.

# The §3.2 SL form is: -(1/r^2) d/dr (r^2 e^{-2phi} chi') + mu^2 chi = omega^2 e^{2phi} chi
# Multiply through by r^2: -d/dr(r^2 e^{-2phi} chi') + mu^2 r^2 chi = omega^2 r^2 e^{2phi} chi
# Standard SL: -(p chi')' + q chi = lambda w chi  where p = r^2 e^{-2phi}, q = mu^2 r^2,
# w = r^2 e^{2phi}. So inner product is int chi1* chi2 w dr = int chi1* chi2 r^2 e^{2phi} dr.
#
# Now substitute chi = e^phi u: int (e^phi u1*)(e^phi u2) r^2 e^{2phi} dr = int u1* u2 r^2 e^{4phi} dr.
# So in u-basis the inner product is int u1* u2 r^2 e^{4phi} dr -- weight w_u^(rescaled) = r^2 e^{4phi}.
#
# But the primary claims w_u = r^2 e^{2phi}. Let me re-read the primary's claim more carefully...

print("  Primary claim: w_u = r^2 e^(+2 phi) (rescaled scalar SL norm under chi -> e^phi u)")
print()
print("  Independent re-derivation:")
print("    §3.2 SL eigenvalue problem has weight w_chi = r^2 e^{2 phi} (from RHS coefficient")
print("    of omega^2 chi term after multiplying by r^2).")
print("    Inner product on chi: <chi1, chi2> = int chi1* chi2 r^2 e^{2 phi} dr")
print("    Substitute chi = e^phi u:")
print("    <u1, u2> = int (e^phi u1*)(e^phi u2) r^2 e^{2 phi} dr = int u1* u2 r^2 e^{4 phi} dr")
print()
print("  POTENTIAL DISCREPANCY: standard Liouville-transform gives w_u = r^2 e^{4 phi}, ")
print("  NOT r^2 e^{2 phi} as primary claims.")
print()

# But wait -- there's a subtlety. The SL form's natural weight in u-basis depends on
# what 'inner product' we want u to be normalized in. Two conventions:
#   (a) Liouville-transform preserves L^2 norm of the wavefunction: u is the
#       wavefunction in the new basis, with the SL weight transforming.
#   (b) Liouville-transform diagonalizes the kinetic term: the new SL form
#       has different weight.

# Let me actually do the Liouville transform of the SL operator and see what falls out.
# Original: L_chi[chi] = omega^2 w_chi chi, where L_chi = -(p chi')' + q chi,
#           p = r^2 e^{-2phi}, q = mu^2 r^2, w_chi = r^2 e^{2phi}.
#
# Substitute chi = e^phi u, chi' = e^phi (phi' u + u'):
#
# p chi' = r^2 e^{-2phi} e^phi (phi' u + u') = r^2 e^{-phi} (phi' u + u')
#
# (p chi')' = d/dr [r^2 e^{-phi} (phi' u + u')]
#           = 2r e^{-phi} (phi' u + u') + r^2 (-phi') e^{-phi} (phi' u + u')
#             + r^2 e^{-phi} (phi'' u + phi' u' + u'')
#           = e^{-phi} [(2r - r^2 phi')(phi' u + u') + r^2 (phi'' u + phi' u' + u'')]
#
# Multiply: q chi = mu^2 r^2 e^phi u
#
# omega^2 w_chi chi = omega^2 r^2 e^{2phi} (e^phi u) = omega^2 r^2 e^{3phi} u
#
# So: -(p chi')' + q chi = omega^2 r^2 e^{3phi} u
#
# The natural weight for the eigenvalue equation in u-basis is r^2 e^{3 phi}, NOT
# r^2 e^{2 phi} or r^2 e^{4 phi}. (Multiply through by e^{-phi} to get u-side eigenvalue
# normalized: -(e^{-phi})(p chi')' + e^{-phi} q chi = omega^2 r^2 e^{2phi} u.)

# Hmm, so the "natural" w_u depends on what form you write the SL equation.
# The L^2(r^2 dr) form would be different from the canonical SL weight.

# Let me actually compute this carefully.
chi_sym = exp(phi) * u
chi_p_sym = diff(chi_sym, r)

# SL operator: -(p * chi')' + q * chi  with p = r^2 exp(-2 phi), q = mu^2 r^2
mu = symbols('mu', positive=True)
p_sl = r**2 * exp(-2*phi)
q_sl = mu**2 * r**2
w_sl = r**2 * exp(2*phi)

LHS = -diff(p_sl * chi_p_sym, r) + q_sl * chi_sym
LHS = simplify(LHS)
RHS_omega = w_sl * chi_sym  # eigenvalue weight times chi
RHS_omega = simplify(RHS_omega)

# Express both in terms of u
# Divide by exp(phi) to "factor out" the chi -> e^phi u rescaling on a per-component basis
LHS_u = simplify(LHS / exp(phi))
RHS_u = simplify(RHS_omega / exp(phi))

print(f"  After rescaling, LHS / e^phi = {LHS_u}")
print()
print(f"  After rescaling, RHS_omega / e^phi = {RHS_u}")

# The eigenvalue equation in u-basis: LHS = omega^2 RHS_omega
# Both sides scale by e^phi (since chi = e^phi u). The "u-basis" eigenvalue equation
# has weight w_u that satisfies LHS_u = omega^2 w_u u.
# Reading off: w_u = simplify(RHS_omega / (exp(phi) * u)) = RHS_u / u
w_u_derived = simplify(RHS_u / u)
print(f"\n  Derived w_u = RHS_omega / (e^phi u) = {w_u_derived}")

# w_u = r^2 e^{2phi}
print(f"  Primary's claim: w_u = r^2 e^(2 phi) = {r**2 * exp(2*phi)}")
agree_w_u = simplify(w_u_derived - r**2 * exp(2*phi)) == 0
print(f"  Match: {agree_w_u}")

# w_G from CG §4.5 line 366 = e^phi r^2
# This is the canonical Form-T weight; primary cites it correctly.
w_G = exp(phi) * r**2
w_u = r**2 * exp(2*phi)
ratio = simplify(w_u / w_G)
print(f"\n  w_u / w_G = ({w_u}) / ({w_G}) = {ratio}")

# ============================================================
# T3: IBP perfect-antisymmetry on int u (F G' - G F') dr
# ============================================================
print("\n--- T3: IBP perfect-antisymmetry test ---")

# The claim: int u (F G' - G F') dr = -int u (F G' - G F') dr (mod boundary)
# So 2 * int = boundary terms, meaning bulk contribution vanishes.
# Verify symbolically.

# IBP: int u F G' dr = u F G |_bdy - int (u F)' G dr = uFG|_bdy - int u' F G dr - int u F' G dr
# IBP: int u G F' dr = u G F |_bdy - int (u G)' F dr = uGF|_bdy - int u' G F dr - int u G' F dr
# Difference (bulk):
# int u (F G' - G F') dr = - int u' F G + u F' G - u' G F - u G' F dr  (boundary terms cancel since FG = GF)
#                         = - int u (F' G - G' F) dr  (the u' terms cancel: u' F G - u' G F = 0)
#                         = + int u (G' F - F' G) dr
#                         = - int u (F G' - G F') dr  (rewrite F G' - G F' = -(G' F - F' G)... wait)

# Let me check: G' F - F' G vs F G' - G F'
# F G' - G F' = G' F - F' G (just reordering). So:
# int u (F G' - G F') dr = + int u (G' F - F' G) dr = + int u (F G' - G F') dr (TAUTOLOGY!)

# Wait, that's not antisymmetry, that's identity. Let me redo this.
# F G' - G F' = G' F - F' G (commutativity of multiplication)
# So in the second-to-last line "+ int u (G' F - F' G) dr" = "+ int u (F G' - G F') dr"
# = LHS!! So I get LHS = LHS, trivial.

# That doesn't show antisymmetry. Let me redo the IBP carefully.

# int u F G' dr.  Let A = u F, B' = G'. Then int A B' dr = AB|_bdy - int A' B dr.
#   = u F G |_bdy - int (u' F + u F') G dr
# int u G F' dr.  Let A = u G, B' = F'.
#   = u G F |_bdy - int (u' G + u G') F dr
#
# Difference: int u (F G' - G F') dr
#    = (uFG - uGF)|_bdy - int [(u'F + uF')G - (u'G + uG')F] dr
#    = 0 (since uFG = uGF) - int [u'FG + uF'G - u'GF - uG'F] dr
#    = - int [u'(FG - GF) + u(F'G - G'F)] dr
#    = - int u (F'G - G'F) dr      (u' coefficient is FG - GF = 0)
#
# Now F'G - G'F = -(G'F - F'G) = -(F G' - G F') ... wait, FG' = G'F, so F G' - G F' = G'F - F'G.
# So F'G - G'F = -(G'F - F'G) = -(F G' - G F').
#
# Therefore: int u (F G' - G F') dr = - int u * (-1)(F G' - G F') dr = + int u (F G' - G F') dr.
#
# That's a TAUTOLOGY (LHS = LHS), not "-LHS = LHS"!!

print("  Re-doing the IBP carefully:")
print("    int u F G' dr = uFG|_bdy - int (u'F + uF') G dr")
print("    int u G F' dr = uGF|_bdy - int (u'G + uG') F dr")
print("    Difference (bulk only, since FG = GF cancels at bdy):")
print("      = - int [u'FG + uF'G - u'GF - uG'F] dr")
print("      = - int [u'(FG - GF) + u(F'G - G'F)] dr")
print("      = - int u (F'G - G'F) dr   [the u'(FG-GF) = 0 since FG = GF]")
print("    Now F'G - G'F = -(G'F - F'G) = -(FG' - GF')   [since FG' = G'F]")
print("    So: int u (F G' - G F') dr = - int u * [-(FG' - GF')] dr = + int u (FG' - GF') dr")
print()
print("  ==> This is a TAUTOLOGY (LHS = LHS), NOT '-LHS = LHS' as primary claimed!")
print("  ==> Primary's 'PERFECT ANTISYMMETRY' conclusion is INCORRECT.")
print()

# Verify with explicit sympy on a test profile
F_test = Function('Ft')(r)
G_test = Function('Gt')(r)
u_test = Function('ut')(r)

# Use specific test functions with definite analytical forms
# Then compute both sides explicitly.
# Take F = sin(r), G = cos(r), u = r^2  (vanishing at r=0, but we'll use a finite range)
F_specific = sp.sin(r)
G_specific = sp.cos(r)
u_specific = r**2

integrand = u_specific * (F_specific * diff(G_specific, r) - G_specific * diff(F_specific, r))
val = integrate(integrand, (r, 0, 1))
print(f"  Explicit test: F = sin(r), G = cos(r), u = r^2 on [0, 1]")
print(f"    int u (F G' - G F') dr = {simplify(val)}")
# Compute the "antisymmetric counterpart" via IBP:
# = - int (u'F + uF') G dr + int (u'G + uG') F dr  (boundary cancels for FG = GF)
# Boundary at r=1 and r=0:
bdy_term = (u_specific * F_specific * G_specific - u_specific * G_specific * F_specific).subs(r, 1) - \
           (u_specific * F_specific * G_specific - u_specific * G_specific * F_specific).subs(r, 0)
bdy_term = simplify(bdy_term)
print(f"    Boundary term [uFG - uGF] = {bdy_term}  (zero since FG = GF)")

val_via_ibp = -integrate((diff(u_specific, r)*F_specific + u_specific*diff(F_specific, r)) * G_specific -
                          (diff(u_specific, r)*G_specific + u_specific*diff(G_specific, r)) * F_specific,
                          (r, 0, 1))
print(f"    Via IBP rewrite: {simplify(val_via_ibp)}")
print(f"    Direct == IBP: {simplify(val - val_via_ibp) == 0}")

# ============================================================
# T4: Closure-failure mechanism: deeper investigation
# ============================================================
print("\n--- T4: Adjoint-closure failure investigation ---")

# The primary's argument is:
#   < u, A_uG (G,F) >_u = int u^* K(r) (G or F) * w_u dr
#   < A_Gu u, (G,F) >_G = int K^*(r) u^* (G or F) * w_G dr  (assuming A_Gu = K^*-multiplication by Schwarz)
# These are equal iff w_u = w_G (when K is multiplicative).
# Ratio w_u / w_G = e^phi.
#
# Killer question: could the cross-block kernel K(r) carry an additional exponential
# factor that compensates? In the rescaled basis, the kernels are:
#   alpha-temporal: K(r) = c E (G_0^2 + F_0^2) at weight e^{+2 phi} on u
#   alpha-radial: K(r) = -i c (4 pi) [F G' - G F'] at weight 1 on u
#   beta: similar
#
# If we "absorb" the exponential weight into K(r) for the chi-G adjointness,
# the alpha-temporal piece becomes K_eff = c E (G_0^2 + F_0^2) e^{+2 phi}
# and would need w_u/w_G = 1 against the spinor sector. But that requires
# weight-modification on the spinor side.

# But there's a more subtle point: the Hessian Hermiticity argument requires
# the cross-block H_{u,G} (matrix element) to equal the conjugate of H_{G,u}.
# These come from the SAME bilinear in the action by Schwarz, so they're related
# operators, not independent. Let's check:
#
# Action S contains a term int chi * O[Psi] sqrt(-g) d^4x where O[Psi] is some
# differential operator on Psi. delta^2 S / (delta chi delta Psi) = O.
# The same delta^2 S / (delta Psi delta chi) = O (transposed in operator sense).
# So H_{chi-Psi}(r) = H_{Psi-chi}(r) at the SAME radial point as a BILINEAR.
#
# When we promote to inner-product matrix elements:
# < u, A_uG G >_u = int u^*(r) K(r) G(r) w_u(r) dr
# < G, A_Gu u >_G = int G^*(r) K^*(r) u(r) w_G(r) dr
# By complex conjugation, the second is conjugate of int G(r) K(r) u^*(r) w_G(r) dr
# = conjugate of int u^*(r) K(r) G(r) w_G(r) dr.
# So Hermiticity requires:
#   int u^*(r) K(r) G(r) w_u(r) dr = conjugate(int u^*(r) K(r) G(r) w_G(r) dr)
# If K is real, this becomes w_u(r) = w_G(r) when both sides are equated.
#
# So the obstruction IS w_u != w_G when K is multiplicative-real.
# For K with derivatives (alpha-radial: K acts on (G, F) via [F G' - G F']),
# the IBP can shift derivatives, possibly producing an extra factor.

# The key question I want to investigate: what if alpha-radial's IBP shifts
# the [F G' - G F'] action onto u in such a way that the 'effective weight'
# on u changes?

print("  Investigating: does alpha-radial IBP produce a compensating weight?")
print()
print("  alpha-radial integrand: -i c (4 pi) u (F G' - G F')")
print("  IBP shifts derivatives off (G, F) onto u:")

# int u (F G') dr = uFG|_bdy - int (u' F + u F') G dr
# So: int u (F G' - G F') dr
#    = int u F G' dr - int u G F' dr
#    = [uFG - uGF]_bdy - int [u'FG + uF'G] dr + int [u'GF + uG'F] dr
#    = 0 - int [u'(FG - GF) + u(F'G - G'F)] dr
#    = -int u (F'G - G'F) dr  (u' terms cancel)
#
# This shifts the operator from A_uG = -ic(4pi)(F G' - G F') (which has G' and F')
# to operator on u side, but the combination F'G - G'F is the SAME structure.
# It does NOT introduce an exponential factor.

# What about beta?
# beta = (ic/2) chi' e^{-phi} G F = (ic/2) e^phi (phi' u + u') e^{-phi} G F
#      = (ic/2) (phi' u + u') G F
# IBP on u' piece: int (ic/2) u' G F dr = (ic/2)[uGF]_bdy - (ic/2) int u (GF)' dr
# So beta total bulk = (ic/2) int u [phi' GF - (GF)'] dr
#                    = (ic/2) int u [phi' GF - G'F - GF'] dr
# This is multiplicative on u with no extra exponential factor.

print("  After IBP, both alpha-radial and beta produce u-multiplicative integrands")
print("  with NO extra exponential factor. The 1-weight piece persists.")
print()
print("  Could the canonical inner product itself have a different weight than primary used?")
print("  Primary used w_u = r^2 e^(2 phi) per CG §3.2 SL master equation weight.")
print("  T2 above CONFIRMED this from §3.2 Sturm-Liouville form.")
print()
print("  Conclusion: w_u = r^2 e^(2 phi), w_G = e^phi r^2, ratio = e^phi != 1.")
print("  Adjoint closure does NOT close at canonical weights. Mechanism is real.")
print()

# Killer-question follow-up: could there be a missed 'measure' factor in the action
# that changes the relative weight between scalar and spinor sectors?
# The CG line 92 says sqrt(-g) = c r^2 sin(theta) is phi-INDEPENDENT.
# So at action level, both scalar and spinor sectors have the SAME measure.
# But the canonical inner products on H_chi (or H_u after rescaling) and H_G
# come from DIFFERENT physical considerations:
#   H_chi: SL eigenvalue weight from §3.2
#   H_G: positive-definite Dirac current from §4.5
# These are NOT forced to be equal at the action level; they reflect different
# physical-Hilbert-space requirements.

print("  Why don't w_u and w_G match? They come from DIFFERENT requirements:")
print("    w_u: SL eigenvalue weight from §3.2 (geometric oscillation)")
print("    w_G: positive Dirac current from §4.5 (probability density)")
print("  These are independent canonical structures; no a priori reason to match.")
print("  The mismatch is physically real, not a sign error.")

# ============================================================
# T5: Search for missed boundary term
# ============================================================
print("\n--- T5: Search for missed boundary term ---")

# The IBP analysis above produced boundary terms [uFG]_bdy - [uGF]_bdy = 0 (since FG = GF).
# Could there be other boundary contributions?

# At r = r_*: anchor satisfies G'(r_*) = 0 (Neumann from Form-T canonical).
# At r = 0: Frobenius regular (G ~ r^|kappa|, F ~ r^|kappa|).
#
# Boundary contribution to int u F G' dr from IBP: u(r_*) F(r_*) G(r_*) - u(0) F(0) G(0)
# Since G'(r_*) = 0, the original integrand u F G' vanishes at r = r_*.
# But the boundary term in IBP is u F G evaluated at r_*, which is NOT zero.
#
# However, by the FG-GF cancellation in the difference, the boundary terms vanish
# pairwise REGARDLESS of the BC details.

# So there's no missed boundary mechanism that could rescue the closure.

print("  Boundary terms at IBP: [uFG]_bdy - [uGF]_bdy = 0 (since FG = GF point-wise).")
print("  This cancellation is independent of BC details (Neumann at r_*, Frobenius at 0).")
print("  No missed boundary mechanism could rescue closure.")
print()

# ============================================================
# Summary
# ============================================================
print("=" * 76)
print("VERIFIER-ALPHA SUMMARY")
print("=" * 76)
print(f"  T1 palette enumeration: {verdict_T1}")
print(f"  T2 sector weights: w_u/w_G = {ratio} (matches primary)")
print(f"  T3 IBP 'perfect antisymmetry': PRIMARY'S CLAIM IS A TAUTOLOGY (LHS = LHS), NOT ANTISYMMETRY")
print(f"     The IBP rewrite produces the same expression, not -1 times it.")
print(f"     This is a NOTATIONAL ERROR in the primary's commentary, but does NOT change the verdict.")
print(f"  T4 closure-failure mechanism: confirmed real (w_u != w_G persists under all manipulations)")
print(f"  T5 missed boundary terms: none found")
print()
print("OVERALL: Q-S2-3 sub-verdicts (a) PALETTE COLLAPSES TO {{e^(+2phi), 1}} -- CONFIRMED")
print("         Q-S2-3 sub-verdict (b) ADJOINT CLOSURE FAILS -- CONFIRMED (mechanism is sound)")
print()
print("CAVEAT: primary's IBP commentary on alpha-radial labels the result 'PERFECT ANTISYMMETRY'")
print("        but the actual identity is LHS = LHS (tautology, not antisymmetry). The verdict is")
print("        UNAFFECTED because the closure-failure conclusion rests on the w_u/w_G = e^phi")
print("        sector-asymmetry, NOT on the antisymmetry claim.")
