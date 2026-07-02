# Lemma D: the sealing amplitude DERIVED at leading order — the ladder's amplitude belongs to (Z, N) alone

**Date:** 2026-07-02. **Derivation agent:** `af837d03b6e3c7c7e` (CAS 10/10, 4 IVP shots, no fits —
the STOP-rule against tuning to 0.092 was armed and never tripped). **Blind adversarial
verifier:** agent `a131282b03455b001` (own CAS re-derivation of every coefficient, own tables
from banked JSONs incl. own symbolic s̃₁ per family, own re-shoots + direct Θ measurement;
derivation scripts on avoid-list; 4 shots). **Verdict: D1–D5 ALL CONFIRMED; no factor-of-2,
sign, or Z error anywhere; the U″-consistency check closes EXACTLY** (R1 reduces at O(ε) to the
separately-banked exact Theorem B — the anti-echo cross-check neither agent could tune).
Scripts: `cascade_lemD_*.py`, `cascade_bv9_*.py`. **Status: DERIVED-AT-LEADING-ORDER**
(hypothesis-development instrument per the Taylor ruling; truncation ledger below; ONE
second-order channel named and open). Scope: round-static Branch-P reduction, potential-only
φ-blind slices, banked cell pins.

## The result (verified forms; verifier corrections folded in)

With x_c ≡ e^{φ_c} = 1/1101, Q ≡ (Z/4)φ'² − s̃₁ (s̃₁ = U''(1)/4 < 0 in the oscillatory
families), envelope a = C·e^{φ/2}Q^{−1/4} (banked):

- **Closed slow system:** ⟨d(Φ²)/dφ⟩ = 4ZC²√|s̃₁|·e^{φ} ⟹ **Φ² = 4ZC²√|s̃₁|(e^{φ} − x_c)**.
  [Cycle-averaged law: instantaneous Φ²/(e^{φ}−x_c) oscillates ±5–12% in the tail; AT THE
  ρ'-NODES it is constant to ≤5% with monotone O(ε) drift — the qualifier is mandatory.]
- **Phase integral:** Θ ≡ ∫₀^{r_s} k dr = √Z·|s̃₁|^{1/4}·√(1−x_c)/C (the e^{φ} in k exactly
  absorbed by the flux measure). Node condition: **Θ = (N+1)π + θ₀.**
- **Double closure (launch-free + phase forms):**
  **R1: a_seal = q/[2√(Z(1−x_c))·(|s̃₁|Q_s)^{1/4}]** (≡ Theorem B at O(ε) — exact reduction);
  **R2: a_seal = √(Z(1−x_c))·(|s̃₁|/Q_s)^{1/4}/Θ ≈ √Z/[(N+1)π + θ₀].**
- **THE CANCELLATION (the mechanism of Stage-C universality):** s̃₁ cancels between phase and
  flux closure — it survives in a_seal only through (|s̃₁|/Q_s)^{1/4} (≤0.2% on banked rungs) —
  and lands entirely in the charge: **q = 2Z√|s̃₁|(1−x_c)/Θ, i.e. q ∝ √|s̃₁| at fixed (Z,N).**
  One derivation explains BOTH halves of the Stage-C primary table: ρ_s sheds the matter
  (amplitude owned by Z,N) while q keeps it (the ~35% q-spread IS the √|s̃₁| spread).
  Verifier's own table: q/√|s̃₁| spread across five Z=8 families = 2.62% (N=5) → **0.45%
  (N=11)** vs 33.6–35.1% raw.
- **The anchor's role resolved:** Δφ nearly cancels out of a_seal (only x_c corrections + Θ) —
  the e^{Δφ/2}=√1101 amplifier is EATEN BY THE FLUX BUDGET; the anchor sets q's scale and the
  phase, not the sealing amplitude.
- **Exact interior (beyond WKB):** on the averaged background the bottom solves in closed form
  **e^{−φ/2} = √1101·cos(κ√x_c·r)**, κ = C|s̃₁|^{1/4}/√Z; in the phase coordinate the O(ε)
  equation is the UNIVERSAL one-parameter ODE g'' − [2ζ/(ζ²+s²)]g' + g = 0 with
  **s = Θ√x_c/√(1−x_c)** [verifier-corrected coefficient; 0.045% at this anchor, exact form
  matters], elementary tail basis u_J = sin z − z cos z, u_Y = cos z + z sin z (exact in the
  tail limit; ρ'-nodes exactly π-spaced — measured on re-shot rungs: 1.000π–1.027π).

## Numeric verdict (verifier's own numbers)

- Z-TEST (no family input): predicted |ρ_s−1|(N=8): Z=8 0.0964 vs banked 0.0920 (+4.8%);
  Z=1 0.0344 vs 0.0345 (−0.2%); Z-ratio predicted 2.807 vs banked 2.671 (+5.1%). **Passes at
  the few-% level with the √Z/Θ(Z) scaling — not naive √8.**
- The Z=8 residual is PARITY-ALTERNATING and is quantitatively the dropped O(ε) source offset:
  adding u_p = [δ̃−(Z/4)φ'_s²]/Q_s brings even-N errors to −0.2…−0.8% (odd-N over-corrects
  +2–3%). An identified truncation term, not a broken coefficient.
- θ₀ measured DIRECTLY off trajectories (the defensible number; θ₀-inferred-from-q is unstable):
  **+0.3209π (Z=8, N=8), +0.2533π (Z=1, N=8)** — vs the universal-ODE leading launch 0.067π.

## THE ONE OPEN CHANNEL (named; bounded next step)
The O(1) phase excess θ₀ ≈ 0.32π/0.25π vs derived 0.067π sits at SECOND-ORDER averaging:
O(a²Θ) secular phase from ⟨ρ⁻²⟩ backreaction + U''' anharmonic phase (both flagged truncations;
decays ∝~1/N as they predict: even-N θ₀ 0.30→0.11 over N=8→22). Until it closes, a_seal
carries the ±5% parity-scale residual. This — not family data — is the remaining gap.

## Truncation ledger (complete; from the derivation, verifier-checked)
linear-U' (drops U'''u²/2, ~10% at N=8, parity-odd — the visible residual split); ρ≈1 in Φ and
⟨ρ⁻²⟩ (O(a) local, O(a²Θ) secular — the open channel); a'² dropped (WKB-small); Q≈|s̃₁| inside
integrals (≤0.7–2%, exact Q_s kept at the seal); φ'²-source dropped in the bottom ODE (~1%);
stuck-point s̃₁ (~0.2–0.5%); bottom drift vs averaged flux (1.5% of budget, measured).

## Consequence for the record
ρ_s(N)-universality: **OBSERVED (blind-verified) + MECHANISM DERIVED at leading order** —
Theorems A/B exact + Structure C at O(ε) + Lemma D's closure with exact family cancellation.
The ladder's amplitude is a property of (Z, N) and the anchor's x_c alone; the matter enters
q as √|s̃₁| and nothing else at this order. Remaining: the second-order θ₀ derivation
(bounded); everything above it is closed.
