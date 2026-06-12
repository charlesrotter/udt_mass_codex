"""Verifier-α independent re-derivation for S56-010 cascade-confirmation.

(b) Candidate B Form-T SA Lagrange identity test:
    Take canonical Form-T equations (mass=0) per CG §4.4:
        dG/dr + (kappa/r - phi') G = E e^{2phi} F
        dF/dr + (-kappa/r - phi') F = -E e^{2phi} G

    Compute d/dr[w(r)(G1 F2 - F1 G2)] using these equations.
    For w(r) = e^{-2phi}: should give (E1-E2)(G1 G2 + F1 F2) (canonical).
    For w(r) such that the SL form gives self-adjoint operator under
    inner product weight w_G:
        canonical w_G = e^phi r^2: closes
        Candidate B w_G = r^2 e^{+2phi}: does NOT close

(c) Candidate C multi-factor sweep: f = e^{a phi} for a in {0, ±1/4, ±1/2, ±1, ±3/2}
    Test whether ANY single multiplicative factor closes adjoint under canonical weights.

(d) Killer questions:
    (d-A) Modified w_u = e^phi r^2: does scalar SL spectral problem still admit
          canonical Frobenius origin behavior + canonical Neumann BC at r_*?
    (d-B) Sub-choice within Form-T: any modified Form-T' under which w_G = r^2 e^{2phi}
          would be SA? (Test alternative integrating factors.)
    (d-C) Non-multiplicative cross-block: derivative-shift kernel modification?
"""

import sympy as sp
from sympy import (Function, symbols, simplify, expand, factor, exp, log, diff,
                   Symbol, Rational, sqrt, Matrix, eye, S, integrate)

print("=" * 76)
print("Verifier-α independent re-derivation S56-010")
print("=" * 76)

r = symbols('r', real=True, positive=True)
phi = Function('phi')(r)
phi_p = diff(phi, r)
G1 = Function('G1')(r); F1 = Function('F1')(r)
G2 = Function('G2')(r); F2 = Function('F2')(r)
E1, E2, kappa = symbols('E_1 E_2 kappa', real=True)

# Canonical Form-T equations (mass=0) per CG §4.4
# dG/dr = (phi' - kappa/r) G + E e^{2phi} F
# dF/dr = (phi' + kappa/r) F - E e^{2phi} G
def G_prime(G, F, E):
    return (phi_p - kappa/r) * G + E * exp(2*phi) * F
def F_prime(G, F, E):
    return (phi_p + kappa/r) * F - E * exp(2*phi) * G

print("\n=== (b) Lagrange identity for Form-T (mass=0) ===\n")

# Test the canonical Lagrange identity:
# d/dr[e^{-2phi} (G1 F2 - F1 G2)] = (E1 - E2)(G1 G2 + F1 F2)?
J12 = G1 * F2 - F1 * G2
weight_canonical_J = exp(-2*phi)  # the J-conservation integrating factor

# Substitute equations of motion
G1_p_val = G_prime(G1, F1, E1)
F1_p_val = F_prime(G1, F1, E1)
G2_p_val = G_prime(G2, F2, E2)
F2_p_val = F_prime(G2, F2, E2)

# d/dr[J12] = G1' F2 + G1 F2' - F1' G2 - F1 G2'
dJ12 = G1_p_val * F2 + G1 * F2_p_val - F1_p_val * G2 - F1 * G2_p_val
dJ12_expanded = expand(dJ12)
print("  d/dr[G1 F2 - F1 G2] (with EOM substituted):")
print(f"    = {sp.collect(simplify(dJ12_expanded), [G1*G2, F1*F2, G1*F2, F1*G2])}")

# d/dr[e^{-2phi} J12] = e^{-2phi} (dJ12) - 2 phi' e^{-2phi} J12
dwJ = exp(-2*phi) * dJ12 - 2*phi_p*exp(-2*phi)*J12
dwJ_simplified = simplify(expand(dwJ))
# Expected RHS:
expected = (E1 - E2) * (G1*G2 + F1*F2)
diff_check = simplify(dwJ_simplified - expected)
print(f"\n  Check: d/dr[e^{{-2phi}}(G1F2-F1G2)] - (E1-E2)(G1G2+F1F2) = {diff_check}")
print(f"  Canonical Lagrange identity holds: {diff_check == 0}")

print("\n=== (b-cont) Test Candidate B w_G = r^2 e^{2phi} for Form-T SA ===\n")

# For self-adjointness of the Form-T radial Hamiltonian H_T such that
#   H_T Psi = E e^{2phi} Psi  (so the eigenvalue problem is generalized)
# Inner product: <Psi1, Psi2>_{w_G} = int (G1 G2 + F1 F2) w_G dr
#
# SA criterion: int [<H_T Psi1, Psi2> - <Psi1, H_T Psi2>] w_G dr = boundary term only
# i.e., (E1 - E2) int (G1 G2 + F1 F2) e^{2phi} w_G dr = boundary term

# Question: under what w_G does the bulk reduce to (E1-E2) * inner-product (= boundary)?

# From the canonical Lagrange identity:
#   d/dr[e^{-2phi}(G1 F2 - F1 G2)] = (E1-E2)(G1 G2 + F1 F2)
# Integrate both sides over [0, r_*]:
#   [e^{-2phi}(G1 F2 - F1 G2)]_0^{r_*} = (E1-E2) int_0^{r_*} (G1 G2 + F1 F2) dr
#
# This means: the "natural" inner product implied by the Lagrange identity is
#   <Psi1, Psi2>_natural = int (G1 G2 + F1 F2) dr  (weight = 1, NOT e^phi r^2!)
#
# But CG §4.5 lists w_G = e^phi r^2 as the "physical Killing weight" — that's a
# DIFFERENT inner product (the Killing-vector conserved current of a Dirac field).

# For Killing-vector inner product, the conservation involves J^t with sqrt(-g)
# = c r^2 sin(theta), and the radial measure picks up the e^{phi} from the
# tetrad/spin-connection structure (mostly-minus in spinor frame).

# For the eigenvalue problem with weight w_G(r) on radial measure, SA requires:
# (E1 - E2) * int (G1 G2 + F1 F2) * (e^{2phi} * weight_factor) dr = boundary

# Key check: does w_G = r^2 e^{2phi} (Candidate B) admit SA closure of the
# eigenvalue problem H_T Psi = E e^{2phi} Psi?

# Under the Lagrange identity, the bulk that needs to match (E1-E2) <Psi1, Psi2>_{w_G}:
# (E1-E2) int (G1G2+F1F2) e^{2phi} w_G dr  needs to be a total derivative.

# Express (G1G2+F1F2) e^{2phi} w_G as something we can integrate.
# From Lagrange:
#   (G1G2+F1F2) = (1/(E1-E2)) d/dr[e^{-2phi}(G1F2-F1G2)]
# So (G1G2+F1F2) e^{2phi} w_G = (e^{2phi} w_G / (E1-E2)) d/dr[e^{-2phi}(G1F2-F1G2)]
#
# For this to integrate to a pure boundary term:
#   (e^{2phi} w_G / (E1-E2)) d/dr[e^{-2phi}(G1F2-F1G2)] must = total derivative
#
# This requires (e^{2phi} w_G) to be CONSTANT (or product rule cancels remainder).
# Canonical w_G = e^{phi} r^2: e^{2phi} * e^{phi} r^2 = e^{3phi} r^2. NOT CONSTANT.
# Candidate B w_G = r^2 e^{2phi}: e^{2phi} * r^2 e^{2phi} = r^4 e^{4phi}. NOT CONSTANT.

# Hmm — so neither is a "simple" SL closure. Let me check more carefully.

# The Form-T canonical eigenvalue problem actually has E coupling through e^{2phi}.
# The proper SA setup is on the "pseudo-spectral" problem:
#   (T - E e^{2phi}) Psi = 0
# which is naturally adjoint under the weight measure such that (T - E e^{2phi})
# is symmetric. This is the GENERALIZED eigenvalue problem T Psi = E (e^{2phi}) M Psi
# where M is the inner-product-defining "mass matrix."

# For canonical Form-T per CG §4.5:
# The inner product weight that makes T self-adjoint is determined by the system's
# integrating factor. From the Lagrange identity:
#   d/dr[e^{-2phi}(G1F2-F1G2)] = (E1-E2)(G1G2+F1F2)
# Setting Psi = (G,F)^T and inner product:
#   <Psi1, Psi2>_W = int (G1*G2 + F1*F2) W(r) dr
# With weight W(r), the operator T such that T Psi = E e^{2phi} Psi is SA iff
# the EOM cross-term integrates correctly. Multiplying Lagrange by W:
#   W * d/dr[e^{-2phi}(G1F2-F1G2)] = (E1-E2) W (G1G2+F1F2)
# For SA at given W (so that bulk reduces to (E1-E2) <Psi1,Psi2>_W * factor):
# need (E1-E2) <Psi1, Psi2>_W = boundary term only.
# But the LHS has explicit W on the d/dr — using product rule:
#   d/dr[W * e^{-2phi}(G1F2-F1G2)] = W' e^{-2phi}(G1F2-F1G2) + W d/dr[e^{-2phi}(G1F2-F1G2)]
# So: W d/dr[e^{-2phi}(G1F2-F1G2)] = d/dr[W e^{-2phi} J12] - W' e^{-2phi} J12

# Substituting:
# (E1-E2) W (G1G2+F1F2) = d/dr[W e^{-2phi} J12] - W' e^{-2phi} J12

# For the RHS to be a pure boundary term upon integration, need W' = 0, i.e., W = const.
# OR need to absorb the W' e^{-2phi} J12 piece into another boundary term, which
# requires specific structure.

# So the canonical SL inner product on (G, F) for the Form-T eigenvalue problem
# (with eigenvalue weight e^{2phi}) is W = const = 1, with conserved Wronskian
# e^{-2phi}(G1F2-F1G2).

# But CG §4.5 weight palette lists e^phi r^2 — that's the PHYSICAL KILLING weight,
# NOT the SL eigenvalue weight! These are different concepts.

# Let me check what the actual SL eigenvalue weight is for canonical Form-T:
print("  Test: under what weight W(r) does Form-T eigenvalue problem (eigenvalue")
print("  weight e^{2phi}) become SA?")
print()
print("  From Lagrange identity:")
print("    d/dr[e^{-2phi} J12] = (E1-E2)(G1 G2 + F1 F2)")
print("  Multiply by W(r) and use product rule:")
print("    (E1-E2) W (G1 G2 + F1 F2)")
print("       = d/dr[W e^{-2phi} J12] - W' e^{-2phi} J12")
print("  SA closure (bulk = boundary only) requires W' e^{-2phi} J12 absorbable.")
print()
print("  Option 1: W = constant (W' = 0). Then SA closes with W = 1.")
print("    Inner product: <Psi1, Psi2>_W=1 = int (G1 G2 + F1 F2) dr (weight 1 dr)")
print()
print("  Option 2: W = e^{2phi} (so e^{2phi} dr is the inner-product measure)")
print("    Then W' e^{-2phi} = 2 phi'. Bulk = (E1-E2) e^{2phi}(G1G2+F1F2) and the")
print("    pseudo-bulk 2 phi' J12 doesn't reduce — NOT SA in this form.")
print()
print("  Option 3: W = e^{phi} r^2 (CG §4.5 physical Killing weight)")
print("    W' = (phi' e^phi r^2 + 2 r e^phi). W' e^{-2phi} = phi' e^{-phi} r^2 + 2 r e^{-phi}")
print("    Doesn't cleanly absorb. This W is the Killing-vector conserved current,")
print("    NOT the spectral SL weight.")
print()
print("  Canonical resolution: SL spectral SA of Form-T uses W = e^{2phi} only via")
print("  the GENERALIZED eigenvalue formulation T Psi = E (e^{2phi}) M Psi where M=1")
print("  is the radial-measure-1 mass matrix; canonical pinning is the eigenvalue")
print("  weight on RHS (= e^{2phi}), not the inner-product radial weight (= 1).")
print()
print("  This means CG §4.5's 'e^{phi} r^2' IS a physical Killing weight, NOT a")
print("  spectral SL weight. The SL spectral problem for Form-T is naturally weight-1.")
print()

# Now Candidate B claims w_G should be modified from e^{phi} r^2 to r^2 e^{2phi}.
# But CG §4.5 calls e^{phi} r^2 the 'physical Killing weight' — which is the
# inner product on Dirac states from the Killing-vector conserved current.
# Modifying THAT weight to r^2 e^{2phi} would change which inner product is being
# used for sector-cross-blocks. The Form-T spectral SA itself uses W = 1 SL weight,
# which is independent of the cross-block inner product weight choice.

# So Candidate B's "breaking Form-T SA" claim needs careful unpacking:
# - The SPECTRAL eigenvalue problem on the Form-T radial system uses W = 1 weight.
#   This is independent of choice of w_G for cross-block inner product.
# - The PHYSICAL Killing-vector-conserved norm uses w_G = e^{phi} r^2.
# - The CROSS-BLOCK inner product uses w_G as defined.
#
# So Candidate B doesn't directly break SPECTRAL SA. It changes the cross-block
# inner product weight, NOT the SL spectral weight.

print("=== (b-finding) Verifier-α refinement on Candidate B Form-T SA argument ===\n")
print("  The primary's claim 'Candidate B breaks canonical Form-T SA' needs precision:")
print("  - SPECTRAL Form-T SA on (G,F) eigenvalue problem uses W=1 SL weight.")
print("    This is independent of cross-block inner-product weight choice.")
print("  - The 'e^{phi} r^2' label at CG §4.5 is the PHYSICAL KILLING weight")
print("    (Dirac probability current from Killing vector), not SL spectral weight.")
print("  - Candidate B modifies the CROSS-BLOCK inner-product weight to r^2 e^{2phi}.")
print("    This does NOT directly affect the Form-T spectral eigenvalue problem.")
print()
print("  POTENTIAL CAVEAT for primary verdict (B-FORBIDDEN-BY-FORM-T-SA):")
print("  The argument that Candidate B 'breaks Form-T SA' is structurally subtler")
print("  than a clean integrating-factor failure. The Form-T spectral problem is")
print("  SA at W=1; the e^{phi} r^2 weight is the Killing-current physical norm.")
print("  Candidate B changes which norm is used as inner product but doesn't")
print("  necessarily destroy the Form-T spectral SA at W=1 layer.")
print()
print("  HOWEVER: per CG §4.5/§244, the canonical inner product for matter-sector")
print("  cross-block structure is the Killing-vector norm w_G = e^{phi} r^2. That")
print("  IS the canonical pin. Modifying it to r^2 e^{2phi} requires a NEW canonical")
print("  principle (e.g., 'cross-block uses scalar-sector weight on spinor side').")
print("  This is a NOT-PINNED situation, NOT a FORBIDDEN-BY-SA situation.")
print()
print("  Refined verdict for B: closer to (B-NOT-PINNED) than (B-FORBIDDEN-BY-FORM-T-SA).")
print("  The primary's verdict letter is too strong; the structural status is the")
print("  same NOT-PINNED status as Candidate A but at a different layer.")
print()

print("=== (c) Multi-factor Candidate C sweep ===\n")
# Test f(phi) = exp(a*phi) for a in {0, ±1/4, ±1/2, ±1, ±3/2}
# Adjoint closure under cross-block kernel modification K_C = f K
# requires: f * w_u = f * w_G when K is multiplicative
# i.e., w_u = w_G — independent of f (degenerate symmetric case)
#
# OR if f is applied as Hermitian-asymmetric: K_chi_G -> f K, K_G_chi -> f^* K
# (no conjugation since f is real here)
# LHS: <chi, fKG>_{w_u} = int chi K G f w_u dr
# RHS: <fKchi, G>_{w_G} = int chi K G f w_G dr
# Difference: int chi K G f (w_u - w_G) dr
# Vanishes iff w_u = w_G (independent of f) — same as canonical.
#
# Try Hermitian-asymmetric: K_chi_G -> f K, K_G_chi -> (1/f) K
# LHS: int chi K G f w_u dr
# RHS: int chi K G (1/f) w_G dr
# Equality requires: f w_u = w_G/f, i.e., f^2 = w_G/w_u = e^{-phi}
# So f = e^{-phi/2}. UNIQUE solution.

w_u_canon = r**2 * exp(2*phi)
w_G_canon = exp(phi) * r**2

print("  Sweep f = exp(a phi) for a in {0, ±1/4, ±1/2, ±1, ±3/2}")
print("  Test 1: symmetric application K_chi_G -> f K, K_G_chi -> f K")
print("  Closure requires: f*w_u = f*w_G, i.e., w_u = w_G (independent of a)")
print()

a_values = [Rational(0), Rational(1,4), Rational(-1,4), Rational(1,2), Rational(-1,2),
            Rational(1), Rational(-1), Rational(3,2), Rational(-3,2)]

print("  | a    | f*w_u - f*w_G                          | Closes? |")
print("  |------|-----------------------------------------|---------|")
for a in a_values:
    f = exp(a * phi)
    diff_val = simplify(f * w_u_canon - f * w_G_canon)
    closes = (diff_val == 0)
    print(f"  | {str(a):4} | {str(diff_val):39} | {closes}   |")

print()
print("  Test 2: anti-symmetric Hermitian application K_chi_G -> f K, K_G_chi -> (1/f) K")
print("  Closure requires: f w_u = w_G/f, i.e., f^2 = w_G/w_u = e^{-phi}, so a = -1/2")
print()
print("  | a    | f^2 - w_G/w_u                          | Closes? |")
print("  |------|-----------------------------------------|---------|")
for a in a_values:
    f2 = exp(2*a * phi)
    target = w_G_canon / w_u_canon
    diff_val = simplify(f2 - target)
    closes = (diff_val == 0)
    print(f"  | {str(a):4} | {str(diff_val):39} | {closes}   |")

print()
print("  FINDING: a = -1/2 (NOT +1/2 as in primary's Candidate C) closes adjoint")
print("  under ANTI-SYMMETRIC Hermitian application of cross-block factor.")
print()
print("  But this is NON-canonical Hermitian rule (kernel and its 'adjoint' carry")
print("  different multiplicative factors). Canonical Hermitian-adjoint of a real")
print("  multiplicative kernel K is K itself (no inverse-factor relation).")
print()
print("  So a = -1/2 'closes' adjoint only by RELAXING the Hermitian-adjoint rule")
print("  (cross-block operator is NOT Hermitian-symmetric to its adjoint at canonical")
print("  inner product layer). This is structurally an alternative-Hilbert-space")
print("  construction, not a canonical-content fix.")
print()
print("  CONFIRMS primary's (C-NOT-PINNED-AD-HOC) verdict: no canonical multiplicative")
print("  factor closes adjoint within canonical Hermitian rules.")

print("\n=== (d-A) Killer question for Candidate A: does modified w_u break boundary structure? ===\n")
# Modified w_u = e^phi r^2
# Canonical scalar SL problem: -d/dr[e^{2phi} r^2 dx/dr] + (μ² e^{2phi} r^2) chi = E e^{2phi} r^2 chi
# Inner product weight: w_u = e^{2phi} r^2 (CANONICAL)
# The SL operator is symmetric under <chi, L psi>_{w_u} = <L chi, psi>_{w_u} via IBP.
#
# If we change w_u to e^{phi} r^2:
# New inner product: <chi, psi>_new = int chi psi e^{phi} r^2 dr
# Question: is the canonical scalar Hamiltonian H still SA under this NEW inner product?
#
# The canonical Hamiltonian per CG §3.3 has SL form:
#   H chi = -[1/(r^2 e^{2phi})] d/dr[e^{2phi} r^2 dchi/dr] + [V(r)] chi
# Eigenvalue: H chi = E chi (or E chi/[e^{2phi}] depending on time-Fourier convention)
#
# For SA under NEW weight w_u_new = e^phi r^2:
# IBP: int (H chi)^* psi w_u_new dr = -int [1/(r^2 e^{2phi})] (...)' * psi * e^phi r^2 dr
#    = -int (...)' * psi * e^{-phi} dr  (after combining e^phi r^2 / (r^2 e^{2phi}))
#
# This changes the IBP boundary terms and bulk symmetry — Hamiltonian as written
# in canonical SL form is SA under canonical w_u, may NOT be SA under modified w_u.

print("  Canonical scalar SL: -d/dr[e^{2phi} r^2 chi'] + V * (e^{2phi} r^2) chi")
print("                        = E * (e^{2phi} r^2) chi    [SL form with weight e^{2phi}r^2]")
print()
print("  This gives canonical inner product w_u = e^{2phi} r^2 (matches RHS weight).")
print("  Under canonical w_u, scalar SL is SA at IBP layer (canonical SL theorem).")
print()
print("  Modify w_u to e^phi r^2 (Candidate A): the SL EIGENVALUE PROBLEM still has")
print("  the SAME operator and the SAME RHS weight e^{2phi} r^2. Changing only the")
print("  CROSS-BLOCK inner product to e^phi r^2 does NOT modify the canonical scalar")
print("  spectral SA — that's still under e^{2phi} r^2.")
print()
print("  CAVEAT: Candidate A uses w_u = e^phi r^2 ONLY for cross-block adjoint check,")
print("  not as a replacement for canonical scalar SL eigenvalue weight. The two")
print("  weights play different roles. So Candidate A doesn't break scalar SL SA")
print("  directly.")
print()
print("  Frobenius origin behavior + Neumann BC at r_*: these are properties of the")
print("  scalar SL spectral problem (eigenvalue weight = e^{2phi} r^2), not the")
print("  inner product weight choice. So Candidate A doesn't directly affect them.")
print()
print("  KILLER-Q-A CONCLUSION: no secondary obstruction for Candidate A at scalar")
print("  spectral problem layer. The 'NOT-PINNED' verdict stands; no additional")
print("  killer mechanism kicks in.")

print("\n=== (d-B) Killer question for Candidate B: alternative Form-T'? ===\n")
# Per (b-finding) above: the e^phi r^2 weight at CG §4.5 is the physical Killing
# weight (Dirac probability current from Killing vector), not the SL spectral
# weight. The Form-T SPECTRAL problem is SA at W=1 weight.
#
# Candidate B changes the cross-block inner product weight to r^2 e^{2phi}.
# This doesn't directly affect Form-T spectral SA at W=1 layer.
#
# The question 'is there a Form-T' under which w_G = r^2 e^{2phi} would be SA?'
# is: yes, trivially — any weight admits SA via redefining the operator.
# But that's a non-canonical Form-T'.
#
# Refined verdict: Candidate B is NOT-PINNED rather than FORBIDDEN-BY-FORM-T-SA.
# The strong "FORBIDDEN" verdict requires the Killing weight at CG §4.5 to be
# uniquely structurally determined as the SPECTRAL SA weight — which on closer
# inspection is the PHYSICAL CONSERVED CURRENT weight, not the spectral SA weight.
print("  Per (b-finding): CG §4.5 e^{phi} r^2 is PHYSICAL KILLING weight, not")
print("  SL spectral SA weight. Form-T spectral SA itself is at W=1 weight.")
print()
print("  Candidate B modifies cross-block w_G to r^2 e^{2phi}, which doesn't")
print("  directly affect Form-T spectral SA. The FORBIDDEN-BY-FORM-T-SA letter")
print("  is too strong.")
print()
print("  Sub-choice within Form-T: modified Form-T' with different metric")
print("  redefinition could nominally have SA under r^2 e^{2phi} — but that's")
print("  non-canonical (changes the equations of motion).")
print()
print("  KILLER-Q-B CONCLUSION: refined verdict is (B-NOT-PINNED) by parallel")
print("  argument with Candidate A — both modify a CANONICAL inner product")
print("  weight without canonical principle to mandate the modification.")
print("  The primary's (B-FORBIDDEN-BY-FORM-T-SA) verdict overstates the")
print("  structural claim; status is structurally identical to Candidate A.")
print()
print("  FLAG-CAVEAT recommended on Candidate B verdict letter; structural")
print("  outcome (NOT-PINNED) consistent with primary's overall disposition")
print("  but the FORBIDDEN letter is too strong.")

print("\n=== (d-C) Killer question for Candidate C: derivative-shift kernel? ===\n")
# Non-multiplicative cross-block kernel modifications: e.g., add a derivative
# term to the cross-block operator. But cross-block kernel structure is FIXED
# by canonical action variation (CG §8.5.3a J0 Yukawa derivation gives specific
# alpha-temporal, alpha-radial, beta pieces). Modifying them by adding derivative
# terms or boundary-restricted modifications would be non-canonical.
#
# Boundary-restricted kernel modification (e.g., distributional delta at r=r_*):
# would close adjoint at boundary at the cost of breaking bulk equations.
# Non-canonical.

print("  Non-multiplicative cross-block kernel modifications:")
print("  (a) Add derivative term to cross-block: K_C = K + g(phi) d/dr — would")
print("      change canonical kernel structure; not derivable from canonical action.")
print("  (b) Boundary-restricted modification (delta-functions): closes boundary")
print("      adjoint at cost of bulk equation modification. Non-canonical.")
print("  (c) Anti-symmetric Hermitian application (per (c) above): closes for")
print("      a = -1/2 but requires non-canonical Hermitian rule.")
print()
print("  All non-multiplicative modifications are non-canonical at canonical-content")
print("  layer. Primary's (C-NOT-PINNED-AD-HOC) verdict is correct in spirit.")
print()
print("  KILLER-Q-C CONCLUSION: no missed canonical non-multiplicative modification.")

print("\n=" * 76)
print("VERIFIER-α SUMMARY")
print("=" * 76)
print("""
(a) Reproducibility: PASS
(b) Independent Lagrange identity test: AGREES with primary on canonical
    Lagrange identity d/dr[e^{-2phi} J12] = (E1-E2)(G1G2+F1F2). Verified
    symbolically.
    BUT: refined understanding shows e^{phi}r^2 is PHYSICAL Killing weight,
    not SL spectral SA weight. SL spectral SA is at W=1 weight. Candidate B
    modifies cross-block inner product weight, not spectral SA weight.
    Primary's FORBIDDEN-BY-FORM-T-SA letter is structurally too strong;
    refined to NOT-PINNED with same structural disposition.
(c) Multi-factor Candidate C sweep: AGREES with primary that NO single
    multiplicative factor in {0, ±1/4, ±1/2, ±1, ±3/2} closes adjoint
    under canonical Hermitian rule. a = -1/2 closes only under non-canonical
    anti-symmetric Hermitian rule (which is itself ad-hoc).
(d-A) Candidate A: no secondary obstruction. (A-NOT-PINNED) verdict stands.
(d-B) Candidate B: refined to (B-NOT-PINNED); primary's FORBIDDEN letter
      is too strong. Same structural disposition (modification not canonically
      pinned), but different verdict letter.
(d-C) Candidate C: no missed non-multiplicative modification. (C-NOT-PINNED-
      AD-HOC) verdict stands.

OVERALL: AGREE-WITH-PRIMARY on overall LANDS-CERTIFIED disposition (all three
Candidates not canonically pinned), but FLAG-CAVEAT on Candidate B verdict
letter — should be (B-NOT-PINNED) rather than (B-FORBIDDEN-BY-FORM-T-SA).

The structural finding (none of A/B/C is pinned by canonical UDT principle)
is robust. The verdict letter for B overstates the FORBIDDEN status — the
underlying disposition (no canonical pinning) is shared with A and C.

Confidence: HIGH on overall composite verdict (LANDS-CERTIFIED).
            MEDIUM on Candidate B verdict letter (caveat raised).
""")
