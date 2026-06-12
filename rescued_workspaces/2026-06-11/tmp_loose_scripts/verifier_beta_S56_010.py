"""
Verifier-β (structural) — S56-010 INDEPENDENT re-derivation.

Strict policy: do NOT consult primary scripts cr_S56_010_*.py
or cr_S56_009_step2_crossblock_palette.py. Use only canonical UDT text
(CG §3.3, §4.5, §22.5 item 34) + S56-009 COMPOSITE_VERDICT (which
states the headline finding without the derivation chain).

Setup (canonical UDT content per CG):
  Scalar SL inner-product weight (matter sector, (b)-type per §3.3):
    w_u = r^2 e^{+2 phi}     (acts on chi field)
  Form-T physical Killing weight (gravity sector, (a)-type per §4.5):
    w_G = e^{+phi} r^2       (acts on G,F spinor radial pieces)
  Asymmetry (S56-009 Q-S2-3-b):
    w_u / w_G = e^{+phi}     -> structural obstruction to cross-block
                                  adjoint closure on unified Hessian.

Question: is the asymmetry vanishable by a multiplicative rescaling
chi = e^{a phi} u for some a? At what value of a?

Charter §3 verifier-β instruction asks me to test
  a in {0, +/-1/2, +/-1, +/-2}  at minimum.
"""

import sympy as sp

phi, r, a, b = sp.symbols('phi r a b', real=True)
af, bf, gf = sp.symbols('af bf gf', real=True)  # rescaling parameters

print("="*70)
print("VERIFIER-β INDEPENDENT DERIVATION — S56-010")
print("="*70)

# Canonical sector weights ----------------------------------------------
w_u_canonical = r**2 * sp.exp(2*phi)   # CG §3.3 scalar SL
w_G_canonical = sp.exp(phi) * r**2     # CG §4.5 Form-T Killing
asymmetry_canonical = sp.simplify(w_u_canonical / w_G_canonical)
print("\n[1] Canonical sector weights:")
print(f"    w_u (scalar, §3.3)      = {w_u_canonical}")
print(f"    w_G (spinor, §4.5)      = {w_G_canonical}")
print(f"    asymmetry w_u / w_G     = {asymmetry_canonical}")
print("    -> e^{+phi}, matches S56-009 Q-S2-3-b headline.")

# ----------------------------------------------------------------------
# (1) MULTIPLICATIVE RESCALING TEST: chi = e^{a phi} u
# ----------------------------------------------------------------------
print("\n" + "="*70)
print("[2] SINGLE-FIELD MULTIPLICATIVE RESCALING:  chi = e^{a phi} u")
print("="*70)
print("""
Convention: the scalar inner product is
    < chi_1, chi_2 >_u = ∫ chi_1^* chi_2  w_u  dr
                      = ∫ chi_1^* chi_2  r^2 e^{2 phi}  dr.

Substituting chi = e^{a phi} u (assume a real and phi(r) real background):
    chi_1^* chi_2 = e^{2 a phi} u_1^* u_2 ,
so the inner product re-expressed on u becomes
    < chi_1, chi_2 >_u = ∫ u_1^* u_2 · [e^{2 a phi} · r^2 e^{2 phi}] dr
                      = ∫ u_1^* u_2 · w_u^(rescaled) dr
with
    w_u^(rescaled) = r^2 e^{(2a+2) phi}.

The spinor weight is UNCHANGED by a scalar-side rescaling:
    w_G remains e^{+phi} r^2.

Cross-block adjoint closure requires equal weights on the two
sector inner products at the cross-block bilinear. The asymmetry is
    w_u^(rescaled) / w_G  =  r^2 e^{(2a+2) phi} / (r^2 e^{phi})
                          =  e^{(2a+1) phi}.

Vanishing of the asymmetry:
    (2a + 1) phi = 0  for all phi  =>  a = -1/2.
""")

# Mechanical sympy verification -----------------------------------------
chi_a = sp.exp(a*phi)  # rescaling factor in chi = e^{a phi} u
w_u_resc = w_u_canonical * chi_a**2     # |chi|^2 = |e^{a phi} u|^2
w_u_resc = sp.simplify(w_u_resc)
asym_resc = sp.simplify(w_u_resc / w_G_canonical)
print(f"  sympy:  w_u^(rescaled) = {w_u_resc}")
print(f"  sympy:  asymmetry      = {asym_resc}")

# Solve for asymmetry-vanishing a
sol = sp.solve(sp.Eq(asym_resc, 1), a)
print(f"  sympy solve(asymmetry=1, a) = {sol}")

# Test grid
print("\n  Charter-required grid a in {0, ±1/2, ±1, ±2}:")
for a_val in [0, sp.Rational(-1,2), sp.Rational(1,2), -1, 1, -2, 2]:
    val = sp.simplify(asym_resc.subs(a, a_val))
    print(f"    a = {str(a_val):>5s}  ->  asymmetry = {val}")

# ----------------------------------------------------------------------
# Compare to S56-009 verifier-β report
# ----------------------------------------------------------------------
print("""
[3] CONFRONTATION with S56-009 verifier-β report:
    S56-009 verifier-β (per primary's S56-010 charter §3 quoting):
        "chi -> e^{a phi} u for various a, found w_u/w_G = e^{(1-2a)phi},
         vanishing only at a = 1/2 (Candidate A)."

    My independent derivation: asymmetry = e^{(2a+1) phi}, vanishing at a = -1/2.

    The two formulae have OPPOSITE signs in the dependence on a:
        S56-009: e^{(1-2a) phi}, zero at a = +1/2.
        S56-010: e^{(2a+1) phi}, zero at a = -1/2.

    Sign-tracking: the discrepancy is consistent with one party using
    chi = e^{a phi} u (rescale chi up by e^{a phi}, i.e. u = e^{-a phi} chi)
    and the other using u = e^{a phi} chi (rescale u up by e^{a phi}, i.e.
    chi = e^{-a phi} u). Under the convention swap a -> -a, my e^{(2a+1)phi}
    becomes e^{(-2a+1)phi} = e^{(1-2a)phi}, exactly matching S56-009.

    *** Both derivations land on the SAME PHYSICAL CANDIDATE: ***
    the rescaling that absorbs the sector asymmetry maps the scalar weight
    onto the spinor weight w_u^(rescaled) = e^{phi} r^2, which is
    *Candidate A* (scalar-inherits-spinor) per CG §22.5 item 34.
    Verify:
""")

a_kill = sp.Rational(-1, 2)  # under chi = e^{a phi} u convention
w_u_at_kill = sp.simplify(w_u_canonical * sp.exp(2*a_kill*phi))
print(f"    w_u^(rescaled) at a = {a_kill} (chi = e^{{a phi}} u convention):")
print(f"        = {w_u_at_kill}")
print(f"    Matches Candidate A (e^{{phi}} r^2)? {sp.simplify(w_u_at_kill - w_G_canonical) == 0}")

# Now under the OTHER convention u = e^{a phi} chi, i.e. chi = e^{-a phi} u
print("""
    Under convention u = e^{a phi} chi (S56-009 convention):
        substitute chi = e^{-a phi} u, so |chi|^2 = e^{-2a phi}|u|^2,
        asymmetry = e^{(-2a+1) phi} = e^{(1-2a) phi}, vanishing at a = +1/2.
        w_u^(rescaled) = r^2 e^{(2 - 2a) phi}|_{a=1/2} = r^2 e^{phi} = w_G.
        Same Candidate A target.
""")

# ----------------------------------------------------------------------
# (2) COUPLED RESCALING — chi -> f(phi) u, G -> h_G(phi) g, F -> h_F(phi) f_F
# ----------------------------------------------------------------------
print("="*70)
print("[4] COUPLED RESCALING: chi = f(phi) u, G = h_G(phi) g, F = h_F(phi) f_F")
print("="*70)
print("""
Independent multiplicative rescaling on each canonical field, all
parameterized as power-of-e^{phi}: f = e^{af phi}, h_G = e^{bf phi},
h_F = e^{gf phi}.

Scalar inner product on the new u-variable:
    < u_1, u_2 >_u^(new) = ∫ |f|^2 u_1^* u_2 w_u dr
                        = ∫ u_1^* u_2 r^2 e^{(2 af + 2) phi} dr

Spinor inner product on the new (g, f_F) variables (CG §4.5 Form-T uses
∫ (G^* G + F^* F) e^{phi} r^2 dr; symmetric in G,F and same weight):
    < (g_1, f_F1), (g_2, f_F2) >_G^(new) =
       ∫ [|h_G|^2 g_1^* g_2 + |h_F|^2 f_F1^* f_F2] e^{phi} r^2 dr.

For Form-T self-adjointness to PRESERVE its spectral structure
(charter pin P5 + CG §4.5 SA gate), we need the SAME weight on
both spinor components:  |h_G|^2 = |h_F|^2  =>  bf = ±gf.
Take the symmetric branch bf = gf for definiteness.

Spinor-side effective weight: e^{(2 bf + 1) phi} r^2.

Cross-block asymmetry on the new bases:
    asymmetry^(new) = e^{(2 af + 2) phi} / e^{(2 bf + 1) phi}
                    = e^{(2 af - 2 bf + 1) phi}.

Closure condition: 2 af - 2 bf + 1 = 0  =>  af - bf = -1/2.
""")

af_sym, bf_sym = sp.symbols('af bf', real=True)
w_u_new = w_u_canonical * sp.exp(2*af_sym*phi)
w_G_new = w_G_canonical * sp.exp(2*bf_sym*phi)
asym_new = sp.simplify(w_u_new / w_G_new)
print(f"  sympy:  asymmetry^(new) = {asym_new}")
sol2 = sp.solve(sp.Eq(2*af_sym - 2*bf_sym + 1, 0), af_sym)
print(f"  sympy solve(closure, af) = {sol2}")

print("""
  The coupled-rescaling family is a ONE-PARAMETER family of solutions
  parameterized by bf (or equivalently af = bf - 1/2). Three sub-cases:

   (i) bf = 0, af = -1/2:  spinor unchanged, scalar absorbs e^{-phi/2}.
       Resulting w_u = e^{phi} r^2 = w_G  ->  Candidate A.

  (ii) af = 0, bf = 1/2:   scalar unchanged, spinor absorbs e^{+phi/2}.
       Resulting w_G = e^{2phi} r^2 = w_u_canonical  ->  Candidate B.

 (iii) af = -1/4, bf = 1/4: BOTH fields absorb half the asymmetry.
       Resulting w_u = w_G = e^{(3/2) phi} r^2.
       This is a NEW candidate weight not in {Candidate A, B}!
       BUT this neither matches w_u_canonical nor w_G_canonical, so it
       breaks BOTH §3.3 AND §4.5 canonical inheritance simultaneously.
       Equivalent to "Candidate D" but at single-multiplicative
       parameterization level — collapses into the same canonical-pinning
       gap as Candidates A, B, C: NO canonical UDT principle pins
       (af, bf) in the family af = bf - 1/2.

   ALL THREE sub-cases face the same missing-pinning-postulate at
   canonical-content layer.

  Critical structural check: case (ii) (spinor side rescaling with
  bf = 1/2) is constrained by the SA gate above to bf = ±gf. Taking
  gf = +1/2 = bf is fine (single-multiplicative on both spinor radials).
  Taking gf = -1/2 (anti-symmetric branch) breaks Form-T's symmetric
  G,F structure -- this is forbidden by CG §4.5 spectral SA. So
  only the symmetric coupled rescaling family closes in a structurally
  consistent way. NO new escape route beyond candidates A, B, and the
  intermediate (a = b - 1/2) family.
""")

# ----------------------------------------------------------------------
# (3) KILLER-QUESTION: NON-MULTIPLICATIVE PERTURBATION
# ----------------------------------------------------------------------
print("="*70)
print("[5] KILLER-QUESTION: non-multiplicative chi -> chi + alpha(phi') G_0")
print("="*70)
print("""
Idea: additive perturbation depending on the background spinor radial G_0.
Effect on |chi|^2 in inner product:
    |chi + alpha G_0|^2 = |chi|^2 + 2 Re[alpha chi^* G_0] + |alpha G_0|^2.

The cross-term 2 Re[alpha chi^* G_0] is BILINEAR in (chi, G_0), which
amounts to a CROSS-FIELD (not single-field) inner-product modification.
But:

 (i) The original asymmetry w_u/w_G = e^{+phi} is at the LEADING
     |chi|^2 term, NOT the cross term. Additive perturbations leave
     the leading-order weight on |chi|^2 untouched.

 (ii) An additive perturbation alpha(phi') G_0 with G_0 a SOLUTION of
      the Form-T equation depends on the background mode being mixed
      in. This is field-dependent (background-state-dependent) and
      thus not an inner-product modification at the kinematic-Hilbert-
      space level — it's a MIXING that alters which states are
      "chi-only" vs "spinor-only". This breaks the sector partition
      itself (CG §22.3.5 (b)-type vs §241/§242 sector architecture),
      which is even MORE structural than the asymmetry it tries to
      dissolve.

 (iii) Verifier-γ S56-009 already covered this type of move under
       "frame-change" (KQ3) and "off-diagonal/J-product inner product"
       (KQ1) categories. Additive background-field mixing is a
       sub-species of the J-product / mixed-Hilbert-space construction.

  -> No new escape route at canonical-content layer.
""")

# ----------------------------------------------------------------------
# (4) KILLER-QUESTION: phi'-DERIVATIVE SIMILARITY TRANSFORM
# ----------------------------------------------------------------------
print("="*70)
print("[6] KILLER-QUESTION: derivative-operator similarity transform")
print("="*70)
print("""
Idea: similarity transform U with U not a simple multiplicative phi-power
but involving d/dr or phi'(r) operators, e.g. U = exp(c · phi'(r) d/dr).

Action on inner product:
    < U^{-1} chi_1, U^{-1} chi_2 >_u  vs  < chi_1, chi_2 >_u.

For this to be a UNITARY transformation that closes adjoint without
modifying canonical sector inner products:
    U^dagger = U^{-1} on (L²_{w_u}, L²_{w_G}) jointly.

Two structural blockers:

 (a) U = exp(c phi' d/dr) is an INTERTWINER between L² spaces with
     phi-dependent measures. For U^dagger = U^{-1} on L²_{w_u},
     need to incorporate the d/dr * w_u' / w_u correction
     (chain rule on the measure). Similarly for L²_{w_G}.
     The CONDITIONS for joint unitarity force a SPECIFIC functional
     relationship between phi(r), w_u(r), w_G(r). The asymmetry
     w_u/w_G = e^{phi} feeds back into this constraint, and the
     constraint becomes self-referential.

 (b) Even if such U exists, it ACTS NON-LOCALLY on chi (it is a
     differential operator), which conflicts with the canonical
     §22.3.5 sector partition where (b)-type matter fields are
     LOCAL test fields. A non-local rescaling of the matter sector
     amounts to a canonical-content extension by definition — same
     status as Candidate C "ad-hoc" kernel factor.

 (c) Verifier-γ S56-009 covered "similarity-transform" explicitly as
     KQ category. The derivative-similarity sub-class is a sub-species,
     and at canonical-content layer reduces to either Candidate A/B/C
     or to a non-canonical extension.

  -> No new escape route at canonical-content layer.
""")

# ----------------------------------------------------------------------
# (5) KILLER-QUESTION: FRAME-DEPENDENT INNER PRODUCT
# ----------------------------------------------------------------------
print("="*70)
print("[7] KILLER-QUESTION: frame-dependent (e.g. conformal-frame) inner product")
print("="*70)
print("""
UDT canonical content (per S56-009 verifier-γ KQ3 + §22.3.5):
single metric, single tetrad, (b)-type test-field convention IS
UDT's matter-frame. There is NO Jordan/Einstein frame degeneracy.

If one POSTULATES a conformal-frame transformation g_munu -> Omega^2 g_munu
with Omega = e^{c phi}, the canonical UDT metric is mapped OUT OF the
admissible set defined by VR §240 C1 uniqueness theorem. Specifically:

  - g_munu is uniquely determined by F_kin(phi) = c · e^{-2 phi}
    via VR §240 1st-order ODE F'_kin + 2 F_kin = 0.
  - Conformally rescaled g_munu satisfies a DIFFERENT ODE, and is
    not in the C1 admissibility map per §240.4.

Therefore "conformal-frame analog" is NOT a canonical-content move
at UDT — it is canonical-extension territory and is RULED OUT by
VR §240 uniqueness theorem at action level.

Verifier-γ S56-009 KQ3 already established this: frame-change route
is structurally vacuous at UDT canonical content.

  -> No new escape route at canonical-content layer.
""")

# ----------------------------------------------------------------------
# (6) ADDITIONAL CANDIDATE PRINCIPLES (per S56-010 Q-S010-5)
# ----------------------------------------------------------------------
print("="*70)
print("[8] ADDITIONAL PRINCIPLES (action-Schwarz, gauge-identity, dilation,")
print("    minimal-coupling, maximal-symmetry) — primary's S56-010 audit")
print("="*70)
print("""
Re-verifying primary's claim that NONE of these candidate principles
selects Candidate A/B/C at canonical-content layer:

 (a) Action-Schwarz uniqueness (§98a precedent): action-Schwarz is a
     GLOBAL inequality on the unified action functional; it does NOT
     mandate a specific local sector-weight. CONSISTENT with primary.
     Note (#27 sub-pattern at advisor-output scope, S55 audit Caveat 1):
     do NOT confuse action-Schwarz with operator-SA. Action-Schwarz
     gives a positivity/coercivity constraint but does not pin a
     unitarity sector-weight selector. CONFIRMED NOT-PINNING.

 (b) Gauge-identity g_tt g_rr = -c^2 analog for inner product:
     the metric-component identity is at the PRIMARY metric layer
     (CG §1.2). Its analog "w_u w_G = (something canonical)" would
     have to be derived from CG §3.3 + §4.5 jointly. But §3.3 and
     §4.5 derive their weights from INDEPENDENT metric origins
     (g^tt vs e_a^t). Their product
       w_u · w_G = r^4 e^{3 phi}
     is not e^{0} (= 1 analog) and not e^{2 phi} (CMB ratio analog).
     No canonical principle pins this product. CONFIRMED NOT-PINNING.

 (c) Dilation-invariance under (r, t) -> (lambda r, lambda t):
     check how w_u and w_G scale under this rigid dilation.
     w_u = r^2 e^{2 phi(r)}: r^2 -> lambda^2 r^2, and phi(r) is
     a r-dependent function so phi(lambda r) is non-trivially
     rescaled. NOT a rigid dilation invariant of the metric.
     w_G = e^{phi(r)} r^2: same story.
     UDT does not have a rigid dilation symmetry (the metric is
     position-dependent, the cosmological r_* and CMB anchors set a
     scale). Dilation-invariance is structurally vacuous for UDT.
     CONFIRMED NOT-PINNING.

 (d) Minimal-coupling principle: the canonical scalar §3.3 derivation
     IS minimal-coupling on (b)-type matter; the canonical Form-T
     §4.5 IS minimal-coupling on (a)-type spinor. Both weights are
     ALREADY produced by the minimal-coupling principle. So
     minimal-coupling does not select between A/B/C — both canonical
     weights are minimal. CONFIRMED NOT-PINNING (if anything,
     minimal-coupling FORBIDS modifying either canonical weight).

 (e) Maximal-symmetry preference: UDT has SO(3) spatial isotropy +
     time-translation + parity. Both w_u and w_G respect all of
     these. Modified weights from Candidates A, B, C also respect
     all of these (as long as modification is in r, phi, not in
     theta/varphi/t). Maximal-symmetry does not discriminate.
     CONFIRMED NOT-PINNING.

 -> Primary's analysis on additional candidate principles is CORRECT.
    AGREE-WITH-PRIMARY at all five additional categories.
""")

# ----------------------------------------------------------------------
# Final summary
# ----------------------------------------------------------------------
print("="*70)
print("[9] VERDICT SUMMARY")
print("="*70)
print("""
1. Independent alternative-rescaling derivation: AGREE WITH PRIMARY at
   PHYSICAL-RESULT layer; flagged sign-convention discrepancy with
   S56-009 verifier-β arithmetic (a = +1/2 vs my a = -1/2 are the
   same point under chi <-> u substitution; both pin Candidate A as
   the multiplicative-rescaling closure point). Worth a F-flag note
   but does NOT change the verdict.

2. Coupled rescaling extension: identifies a ONE-PARAMETER family
   af = bf - 1/2 with three named cases:
       (i)  Candidate A (af=-1/2, bf=0)
       (ii) Candidate B (af=0,  bf=+1/2)
       (iii) NEW: intermediate (af=-1/4, bf=+1/4) collapsing
             both weights to e^{(3/2)phi} r^2.
   Case (iii) is structurally subsumed under verifier-γ S56-009's
   "similarity-transform" category; equivalent to Candidate-D-like
   at single-multiplicative parameterization. NO NEW escape route
   at canonical-content layer (still missing pinning postulate).

3. Killer-questions (non-multiplicative, derivative-similarity,
   frame-dependent): all subsume under verifier-γ S56-009's existing
   five categories. NO new escape route at canonical-content.

4. Additional candidate principles (action-Schwarz, gauge-identity-
   analog, dilation, minimal-coupling, maximal-symmetry): primary's
   audit is correct. NONE pin Candidate A/B/C at canonical-content.

5. Verdict recommendation: AGREE-WITH-PRIMARY (S56-S010-LANDS-CERTIFIED)
   with FLAG-CAVEAT noting (a) the sign-convention discrepancy with
   S56-009 verifier-β arithmetic for canonical-record clarity, and
   (b) the intermediate coupled-rescaling case (iii) as worth
   tagging in canonical-content for completeness (even though
   structurally subsumed).

6. Confidence: HIGH on the structural conclusion that canonical
   UDT principles do not select among Candidate A/B/C at current
   canonical content; HIGH on the cascade-confirmation principle's
   value-add (sign-convention catch is exactly the kind of
   secondary-arithmetic catch that #27 pattern monitoring expects).
""")

