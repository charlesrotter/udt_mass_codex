# V1 — Finite-domain carrier virial identity (DERIVATION RECORD)

**Date:** 2026-07-16 · **Dispatch:** `UDT_H3_BOUNDARY_VIRIAL_CLOSURE_BEFORE_F_DISPATCH.md` §3
**Status of the continuum identity: DERIVED** (from the stated carrier functional; no GR input).
**Status of its application to the numerical box: TO BE TESTED** (V2/V3/V4 of the same dispatch).
**CAS verifier:** `verify_virial_identity_cas.py` (sympy; verdict recorded in its output).
**Observing or targeting:** derivation of an identity; no target number. DATA-BLIND.
**NOT claimed:** an exact lattice Noether theorem for the one-sided discretization (V3 tests
convergence of the surface construction, not an assumed discrete identity); any infinite-volume limit.

## 1. Setup

Energy density (ξ, κ constants; n : R³ → S², n·n = 1):

  ℰ = ℰ₂ + ℰ₄,  ℰ₂ = (ξ/2) X,  ℰ₄ = (κ/4) Y,
  X = ∂_k n·∂_k n,  Y = F_kl F_kl,  F_ij = n·(∂_i n × ∂_j n).

Constrained Euler–Lagrange residual (unconstrained gradient plus multiplier):

  ℛ̂_a = δE/δn_a = −ξ Δn_a + (κ/2) F_kl (∂_k n × ∂_l n)_a + κ ∂_i( F_ik (n × ∂_k n)_a ) ;
  (the middle term is NORMAL for unit fields, since ∂_k n × ∂_l n ∥ n; it drops under the
  tangential projection and under contraction with ∂_j n)   ℛ_a = ℛ̂_a − (n_b ℛ̂_b) n_a ,
  [CORRECTED 2026-07-16: the first CAS pass caught a wrong sign on the divergence term and the
  omitted normal term — the momentum ∂ℒ₄/∂(∂_i n_a) = −κ F_ik (n×∂_k n)_a, so −∂_i(momentum)
  enters with PLUS sign. (T2') failed until corrected; production numerics were never affected
  (they use the audited grad_noNull, not this formula).]
  so that ℛ̂_a = ℛ_a + λ n_a with λ = n_b ℛ̂_b. An exact critical point has ℛ = 0 (λ free).

## 2. The spatial stress

Under an infinitesimal spatial translation δn = −ε_j ∂_j n, the standard current construction on the
stated functional gives

  𝒯_ij = ξ ( ∂_i n·∂_j n − ½ δ_ij X ) + κ ( F_ik F_jk − ¼ δ_ij Y ).

**Trace (pure index algebra, CAS-verified):**

  𝒯_ii = ξ( X − (3/2) X ) + κ( F_ik F_ik − (3/4) Y ) = −(ξ/2) X + (κ/4) Y = −ℰ₂ + ℰ₄ ≡ S.   (T1)

## 3. Translation identity and the multiplier drop

Direct differentiation (CAS-verified on generic constrained fields) gives, for ANY smooth unit field,

  ∂_i 𝒯_ij = − ℛ̂_a ∂_j n_a = − ℛ_a ∂_j n_a − λ n_a ∂_j n_a.   (T2)

**Multiplier drop:** n_a ∂_j n_a = ½ ∂_j (n·n) = ½ ∂_j (1) = 0, so the λ-term vanishes identically:

  ∂_i 𝒯_ij = − ℛ_a ∂_j n_a.   (T2′)

For an exact stationary solution (ℛ = 0): ∂_i 𝒯_ij = 0.

**Sign convention (fixed and CAS-verified):** ℛ̂ is the FUNCTIONAL GRADIENT (δE/δn, so that
E[n+δn] − E[n] = ∫ ℛ̂_a δn_a + O(δn²)), and (T2) carries the minus sign as written. All numerical
residual-work terms below use this convention; `grad_noNull` returns the discrete ∂E/∂n_site, i.e.
site-integrated ℛ̂ (ℛ̂ dV per site).

## 4. Finite-domain virial identity

Multiply (T2′) by x_j and integrate over a finite domain Ω, using
x_j ∂_i 𝒯_ij = ∂_i (x_j 𝒯_ij) − 𝒯_jj and the divergence theorem:

  ∫_Ω 𝒯_ii dV = ∮_∂Ω x_j 𝒯_ij ν_i dS + ∫_Ω x_j ℛ_a ∂_j n_a dV.

With (T1), for a finite domain,

  ┌─────────────────────────────────────────────────────────────────┐
  │  E₄ − E₂ = ∫_Ω S dV = B_∂Ω + W_res ,                            │
  │  B_∂Ω ≡ ∮_∂Ω x_j 𝒯_ij ν_i dS ,   W_res ≡ ∫_Ω x_j ℛ_a ∂_j n_a dV │
  └─────────────────────────────────────────────────────────────────┘

(W_res = 0 for an exact critical point; the numerical tests carry it explicitly because the saved
fields are critical only to the certified gate ‖g_f‖.)

## 5. Consequence for the conditional mass readout

With G's conditional lapse identity M_N⁽⁰⁾ = 2E₄ = (E₂+E₄) + (E₄−E₂):

  ┌───────────────────────────────────────────────┐
  │  M_N⁽⁰⁾ = E_carrier + B_∂Ω   (+ W_res)        │
  └───────────────────────────────────────────────┘

under the conditional EH lapse premise. **Only if B_∂Ω → 0 in a controlled isolated limit** does
M_N⁽⁰⁾ = E_carrier follow. The −2.7% virial gap measured in G is, by this identity, exactly the
boundary dilation-stress term (plus the small residual work) of the pinned L=6 box — WORKING
hypothesis, tested in V2–V4; not assumed.

## 6. What the identity does NOT establish

- Nothing here derives the carrier or its coupling from the native UDT action (carrier = POSIT).
- The identity is continuum; the one-sided site discretization need not admit an exact local
  Noether current — V3 therefore tests grid CONVERGENCE of the surface construction.
- No statement about the L → ∞ limit is made; V4 is a bounded scout, not a limit proof.
