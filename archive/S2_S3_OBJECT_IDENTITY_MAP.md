# MAP — Settle the S²-vs-S³ object identity (before P2)

**Mode:** MAP (no compute). **Status:** for Charles's steer; settling is GATED on his go.
**NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-19 (LATE+).
Gates P2 (the matter EL is built on the answer). Frame whole + premise ledger + the contaminated
history made visible, so the prior failure mode is not repeated.

---

## 0. THE QUESTION — stated precisely (two facets, do not conflate)

"S² vs S³" is really TWO questions that the record has sometimes blurred:

- **(A) The native CHARGE carrier** — what carries N=3, q=1/3, η=1/18. **SETTLED = S²/π₂** (the
  area form ω_H1 = ε_abc n_a dn_b ∧ dn_c on a unit 3-vector). CANON C-2026-06-14-1; #61
  (blind-verified) confirmed the native current is genuinely S²/π₂, blind to a 4th component, and
  that "S³ DERIVED" was unearned. **This facet is not re-opened.**

- **(B) The native OBJECT / matter-field target space** — does the metric's matter field live on
  **S² (a unit 3-vector, π₂)**, or does the native action **SOURCE a 4th component**, making the
  field an **S³/SU(2) (π₃, Skyrme-type)** object? **THIS is open** (scoped-open since #61) and is
  what P2 needs settled, because the 3-D matter EL is built on the field's actual target space.

The decisive form of (B): **is the 4th component a SOURCED dynamical DOF (⇒ S³), or a
passenger/gauge/redundant direction (⇒ S²)?**

## 1. WHAT IS SETTLED / OPEN / CONTAMINATED (the honest state)

**Settled (native, blind-verified):** the CHARGE is S²/π₂ (A above); the native current is blind to
n_4; the bulk EOM is solved by Θ=π/2 as a CONSTANT; #50 gives no SU(3) connection; a sized L2+L4
soliton exists (m=1).

**Open (the hinges of B):**
- Is the 4th component **sourced**? (fourth_component_sourced_results.md, 2026-06-18 — left open.)
- The **texture**: the naive S² 3-vector hedgehog n=(sinΘ sinθ cos mψ, …, cosΘ) carries a cos θ
  TEXTURE in its stress (coupled_tl_s2_derive, this session) — the diagonal mass sector is
  carrier-robust (S²==S³) but the TANGENTIAL stress/EL differ. Is the texture intrinsic to the
  native object or an artifact of this particular embedding/ansatz?
- Does the matter cell **reach r=0**? (r_core=0.05 is a CHOSEN cutoff, #61; affects m=1's endpoint,
  not the m-ladder import verdict.)

**Contaminated history (the tripwire to NOT repeat):** the prior attempt to settle (B)
(fourth_component_sourced_results.md) reached a clean verdict — "the 4th component is a PASSENGER ⇒
S² ⇒ the catalog is an import" — that **DID NOT SURVIVE its blind verifier**: it committed a
**slice→frame inflation** ("the EOM PERMITS Θ=π/2" was inflated to "the object IS S²"). PERMITS ≠
DEMANDS. Settling (B) honestly requires showing what the metric **DEMANDS**, not merely permits.

## 2. PREMISE LEDGER

| # | Choice | Default | CHOSE / DERIVED | Risk / guard |
|---|---|---|---|---|
| OI-action | the action that decides the target space | native L2+L4 on the unit field (canon) | DERIVED (canon) | settle from THIS action; do not import a Skyrme L4 normalization or a π₃ term. |
| OI-4th | whether n_4 is a sourced DOF | TBD — the question | must be DERIVED, not assumed | **the crux.** Show the native action SOURCES (or does not source) a dynamical 4th component. Avoid "permits" → "is" (the #61-verifier slice→frame inflation). |
| OI-import | S³/π₃/Skyrme provenance | suspect = import | provenance-AUDIT | algebraic-objects-can-be-imports: is "S³" ever DERIVED from the metric, or always carried in via the Skyrme/baryon BC (#61)? |
| OI-texture | the cos θ tangential structure | TBD | DERIVE the actual stress | is the texture intrinsic to the native S² object or an ansatz artifact (e.g. of the mψ embedding)? |
| OI-core | r→0 reach | r_core cutoff today | scope-honest | resolve or scope; affects m=1 endpoint only. |
| OI-demands | the bar | DEMANDS, not permits | binding | the lesson from the failed prior verdict. A settle stands only if it shows necessity, with a blind verifier. |

## 3. HOW TO SETTLE IT (proposed — metric-led, algebraic, provenance-audited)

Largely SYMBOLIC (sympy-exact), targeted small numerics only as checks, blind-verified. NOT a big
solver build (this is a clean algebraic question — UDT's strong suit).

1. **The target-space question (OI-4th, the crux):** from the native L2+L4 action, write the most
   general unit field (allow a live 4th component), derive its EOM, and ask: does the action
   **source** the 4th component (a non-trivial dynamical equation forcing it on ⇒ S³), or is it
   unsourced / pure-gauge / redundant (⇒ S²)? Show DEMANDS, not permits (state the necessity, or
   the genuine bifurcation if the action admits both).
2. **Provenance audit (OI-import):** trace every place "S³/π₃/Skyrme" enters — confirm whether it
   is ever metric-DERIVED or always imported (the Skyrme BC #61). Confirm the area-form charge's
   native target is uniquely S².
3. **Texture reconciliation (OI-texture):** derive the actual angular stress of the native object;
   determine whether the cos θ texture is intrinsic or an artifact of the embedding.
4. **r→0 (OI-core):** resolve or honestly scope.
5. **Blind verifier** aimed hardest at any "is" that rests on a "permits" (the prior failure), and
   at any imported algebraic object dressed as native.

OUTCOME shape: either (S²) the native object is the unit 3-vector and the texture/EL is derived for
it (P2 proceeds on S²) ; or (S³) the metric genuinely sources a 4th component (P2's matter field is
S³, and the catalog/import story re-opens on native footing); or (BIFURCATION) the action admits
both and the selector is named. Any outcome is a clean result that unblocks P2.

## 4. SMUGGLED-FRAME / RISK CHECK

- This is METRIC-LED ("what target space does the native action demand?"), not catalog-driven —
  good. The main risk is repeating the **permits→is** inflation; the "DEMANDS" bar + verifier guard it.
- Second risk: importing S³ (Skyrme/π₃) as if native — the provenance audit guards it.
- It is the RIGHT thing to settle before P2: P2's matter EL depends on the target space, and
  settling it algebraically is cheap and clean (no box-control/conditioning sand).
- Honest limit: if the action genuinely admits both (a bifurcation), "settle" becomes "name the
  bifurcation + its selector" — still a clean unblock, not a failure.
