# H4 · N1 — General off-round transverse field equation + the −2𝒦 φ-source off-round (CF5 does NOT trip)

**Status: BANKED, blind-verified (2026-07-05). Armchair/CAS (sympy symbolic only; NO numerical solve, NO data,
no open decision taken).** Node N1 of `H4_backreaction_mass_MAP.md` (the first of the two derivation gaps the MAP
named). Deriver agent af67b40ca9908bac9; blind adversarial verifier a0287030e58746e8f (all 8 targets PASS —
independently re-derived on fully non-diagonal and surface-dependent h_AB the driver scripts never tested; no
error/missing term/smuggle). Provenance scripts committed: `h4_scripts/verify_offround_transverse.py`,
`verify_round_and_R2.py`, `vv_independent.py` (each re-runs to exact 0 / expected form).

## Headline (CF5 verdict)
**CF5 does NOT trip.** The Branch-P φ-source **−2𝒦** and the Branch-G exact cancellation **survive verbatim for a
general non-round (toroidal) transverse metric**. Roundness was NOT load-bearing for the STRUCTURE of the
n→h_AB→𝒦→φ backreaction channel; it fixed only the round-specific numerical *value* of the source (4e^{−2φ}/r²)
and the areal charge reading. The genuinely new off-round content is that the transverse equation is a full
symmetric **tensor** equation whose traceless/shear part the round one-scalar ρ-equation cannot carry.

## 1. The general transverse field equation (δS_geo/δh_AB)
Radial-ADM: r is the evolution parameter, lapse N=e^{φ}, zero shift, K_AB = ½e^{−φ}∂_r h_AB, 𝒦 = K_AB K^AB − K².
Varying S_geo = ∫ c√h[(Z_φ/2)φ'² + R^{(2)}[h] + W_χ𝒦] w.r.t. h_AB (define E^{AB} ≡ (2/√h) δS_geo/δh_AB):
```
E^{AB} =  (Z_φ/2) φ'² h^{AB}                                   ← measure (isotropic pressure)
        + W_χ [ ½ h^{AB}𝒦 − 2 K^{AC}K_C^{B} + 2 K K^{AB} ]    ← extrinsic, algebraic (DeWitt)
        − ∂_r π^{AB},   π^{AB} = √h W_χ e^{−φ}(K^{AB} − K h^{AB})   ← extrinsic, momentum
      = − T^{AB}   (matter source, T^{AB} ≡ (2/√h) δS_m/δh_AB, φ-blind)
```
(Verifier-corrected coefficients: the algebraic DeWitt terms are `½h^{AB}𝒦 − 2K^{AC}K_C^B + 2KK^{AB}`, matched
component-by-component — incl. the symmetric off-diagonal, factor-of-2 correct — against a direct EL variation of
a NON-diagonal h(r)=[[P,S],[S,Q]]; all differences identically 0.)
- **R^{(2)}[h] exerts ZERO local stress.** In 2D the Einstein tensor G^{(2)}_{AB} ≡ 0 identically (CAS-verified on
  a fully general non-round 2-metric), and √h R^{(2)} = Gauss–Bonnet (∫ = 4πχ). So R^{(2)} fixes only the
  transverse **topology** (S² vs torus) — no local source. (This is the precise sense of "boundary/topological in 2D.")
- **π^{AB} is EXACTLY the JC2 seal momentum** (`seal_matching_junction_results.md:32,79`) — an independent
  cross-check that the transverse momentum conjugate to h_AB is the same object; passed (up to the overall c).

## 2. The φ-source generalizes off-round (the CF5 mechanism)
The one carrying fact: K_AB = ½e^{−φ}∂_r h_AB puts exactly ONE factor e^{−φ} on every K from the longitudinal
normal (g^{rr}=e^{−2φ}), independent of transverse shape, and K is ultralocal in the surface coordinates (only
r-derivatives of h). Hence, writing 𝒦 = e^{−2φ}𝒦̂[h] with 𝒦̂ built from h_AB, ∂_r h_AB only:
```
∂𝒦/∂φ = −2𝒦   for ANY h_AB   (CAS-verified on a fully general non-diagonal h_AB(r,x,y))
```
Therefore in ∂_r(√h Z_φ φ') = √h ∂(W_χ𝒦)/∂φ:
- **Branch G** (W_χ=e^{2φ}): W_χ𝒦 = 𝒦̂[h] is φ-free for general h ⇒ ∂(e^{2φ}𝒦)/∂φ = 0 ⇒ **(√h Z_φ φ')' = 0**
  (exact cancellation survives off-round).
- **Branch P** (W_χ=1): **∂_r(√h Z_φ φ') = −2√h 𝒦 = −2√h e^{−2φ} 𝒦̂[h]** — the −2𝒦 source with 𝒦 the general
  (non-round) invariant. Round is the special case 𝒦̂ = −2/r² ⇒ source 4e^{−2φ}.

**Scope note (verifier, load-bearing for N2):** for φ=φ(r) with a surface-*dependent* h, the physical reduced
radial ODE carries the **surface-INTEGRATED** source ∫√h 𝒦 d²x — the pointwise −2𝒦 is the density; the averaging
over the transverse surface is exactly the N2 far-field/multipole work (properly deferred, not done here).
The "P has no asymptotic vacuum" discriminator (`native_field_equations_...:122-129`) is **round-AMBIENT-specific**
(RHS = fixed const 4e^{−2φ_∞}); a **localized** toroidal source has COMPACT support, so it does NOT inherit that
obstruction — a localized P-object on the N=0 background is well-defined. (Supports the MAP's read-surface-in-bulk
default C(a).)

## 3. The backreaction chain + the sign-varying source (CF1 left OPEN for N4)
Clean identity: 𝒦 = K_AB K^AB − K² = **−2 det(K^A_B) = −2 k₁k₂** (k₁,k₂ the principal radial-expansion rates;
round k₁=k₂ ⇒ 𝒦<0). Chain:
```
localized toroidal T^{AB} →[§1]→ localized non-round h_AB deformation →[𝒦=−2det K]→ localized 𝒦[h]
   →[§2, Branch P]→ localized φ-source −2𝒦
```
A localized transverse stress generically gives 𝒦 ≠ 0 on a compact region ⇒ a nonzero LOCAL φ-source. **But the
sign is not fixed:** over the toroidal core one principal direction expands while the orthogonal one contracts
(k₁k₂<0 ⇒ 𝒦>0), flipping the local source sign relative to the round case — so −2𝒦 is a **localized distribution
of VARYING sign**. Whether it integrates to a **nonzero net far-field monopole δq (a mass) or cancels to δq=0
(CF1)** cannot be read off a sign-varying integrand — it needs the N4 solve on the actually-resolved hopfion
h_AB. **CF1 is correctly LEFT OPEN; N1 does not (and must not) decide it.**

## 4. Roundness audit
| corpus use of round h_AB=r²Ω | does the general equation depend on it? |
|---|---|
| ρ=r theorem | round-only; off-round, ρ is replaced by the full h_AB tensor — general eq does not use it |
| source value Z_φ(r²φ')'=4e^{−2φ} | round-only VALUE; the −2𝒦 STRUCTURE generalizes (§2) |
| K=2e^{−φ}/r, 𝒦=−2e^{−2φ}/r² | round-only values; general 𝒦=−2det(K^A_B) |
| areal charge q=(r²φ')_seal | round-only (√h∝r²); general needs Π_φ=√h Z_φ φ' (MAP ledger already flags) |
| "P has no asymptotic vacuum" discriminator | **round-AMBIENT-specific** — does NOT forbid a compact-support localized P-object (§2) |
| e^{2φ}/4 matter weight (was "needs re-confirmation") | **CONFIRMED NATIVE** by the round reduction — Branch-P-SPECIFIC (see caveat) |
| one-scalar ρ-equation | **does NOT generalize** — off-round is a symmetric tensor E^{AB} (≤3 components); the toroidal source excites the traceless/SHEAR part the round ansatz cannot carry — this is N1's genuinely new content |

Round-reduction consistency check (both routes): E^{AB} reduces to ρ''_matter = (e^{2φ}/4)(ξρI_r − κN²I_4θ/ρ³) =
`round_matter_reduction_results.md:19` exactly (CAS diff = 0). The e^{2φ}/4 weight emerges as 1/(4e^{−2φ}) from the
GEOMETRIC W_χ𝒦√h term (NOT inserted on the φ-blind matter side) ⇒ confirmed native.

## Scope caveats the doc carries (honesty, verifier-required — not defects)
1. **"Off-round" = an arbitrary transverse 2-metric h_AB, WITHIN the ledgered metric FORM:** block-diagonal
   (g_{rA}=0, built into K_AB=½e^{−φ}∂_r h_AB) and φ LONGITUDINAL (φ=φ(r)). A genuinely toroidal backreacting
   config could in principle excite a radial SHIFT (g_{rA}≠0) or angular φ-dependence (φ=φ(r,x)), which is
   OUTSIDE N1's scope. Already ledgered in the MAP ("metric FORM — CHOSE"; "φ longitudinal"); N4 must NOT silently
   inherit full-3-metric generality.
2. **The e^{2φ}/4 weight-confirmation is Branch-P-SPECIFIC** (Branch G gives a different weight) and rides on the
   φ-blind-matter premise (DERIVED-conditional on R1+P5, per the MAP ledger). Fine for H4 (P-only); do NOT quote
   branch-agnostic.

## Provenance / discipline
No GR minimal coupling (G=8πT never written); the transverse equation comes purely from varying the NATIVE
action, matter entering only as δS_m/δh_AB. Schwarzschild appears in the corpus only as a far-field REFERENCE
(matches O(1/r), departs at O(1/r²)) — lane #2, not a source law. Derived for general anisotropic h FIRST, then
reduced to round as a check (not the reverse). Both branches kept symbolic; no seal/branch/ξ/κ/Z_φ decision taken.
CF5 settled (does not trip); CF1 left open for N4. Next node = **N2** (far-field / multipole reduction of the
localized non-round source: does ∫√h 𝒦 give an effective monopole δφ-well read on a bulk read-surface — frame C(a);
settle whether net δq can be ≠ 0).
