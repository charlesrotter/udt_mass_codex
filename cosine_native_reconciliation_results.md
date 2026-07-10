# RESULT — the round-cell cosine vs. the native two-player equation (reconciliation)

> **⚠ α-COEFF CORRECTED (2026-07-10):** any `+α·ξ·e^{αφ}·ρ²·I_r` below is WRONG — the anchor-verified coefficient is **`−(α/2)·ξ·e^{αφ}·ρ²·I_r`** (`verify_alpha_coeff_ANCHORED.py`; reproduces base φ-EOM + base ρ-EOM + T_AB). **SIGN-CRITICAL:** for α<0 the direct source is POSITIVE (SUPPORTS `I_r`), not draining. Any pre-grok reasoning here that relied on the old `+α` sign is **CONDITIONS-CHANGED** (see LIVE.md on grok).


**Date:** 2026-07-08 · **Author:** Claude Opus 4.8 (1M) with Charles. **Status: VERIFIED** (blind adversarial pass
below). Data-blind (no 1101/7.004/C/μ_g). Regime-scoped (see §Scope). Scripts: `cosine_reconciliation_check.py`
(derive), `verify_cosine_reconciliation.py` (independent blind re-derivation).

## Question
Is the banked "round-cell cosine" `e^{−φ/2} = A cos(kr)` (`ladder_lemmaD_sealing_amplitude_results.md`) a solution of the
**native two-player** scalar equation, or something else? This gates Thread A (the derived background): if the cosine IS
the native background, Thread A stands on it; if not, we need the actual native object.

## Result (three findings)

**1. The cosine is NOT a solution of the native two-player scalar equation — in any gauge.**
Substituting φ = −2 ln(A cos kr) into the areal Branch-P vacuum equation `(r²φ′)′ = (4/Z)e^{−2φ}` leaves a nonzero
residual: LHS grows like `k²r² sec²(kr)` toward the edge, RHS decays like `A⁴ cos⁴(kr)` — opposite behaviour, no
identity. Areal gauge ρ=r is itself inconsistent with the vacuum ρ-equation (forces `2φ′=(Z/4)r e^{2φ}φ′²`, which the
cosine violates). No positive-real ρ(r) makes the cosine φ satisfy even the φ-equation of the coupled system, let alone
both — so the cosine is not a coupled vacuum solution in any gauge.

**2. The cosine is a leading-order, cycle-averaged, ρ-frozen, MATTER-SOURCED reduction — self-declared as such.**
It solves the *flat harmonic* reduction `v″ = −k² v` (`v=e^{−φ/2}`, k²=κ²x_c) — no r²/ρ² geometric term, no `e^{−2φ}`
nonlinearity. The flux law `v′=−κ√(1−x_c v²)` is its first integral. Its own truncation ledger
(`ladder_lemmaD_sealing_amplitude_results.md:62-66`) names what is dropped: **cycle-averaging, ρ≈1 freeze, WKB (a′²
dropped), linear-U′, φ′²-source dropped**. Its source is matter: `s̃₁=U″(1)/4`, a **winding-potential** curvature — so
it is NOT a vacuum object. Consistent with the banked doc's own "leading-order / hypothesis-development instrument"
self-label (Taylor ruling). So this is not a contradiction uncovered — it is precisely what the cosine always was.

**3. The native two-player VACUUM system has NO finite `φ→∞` edge.**
Integrating the full coupled vacuum system outward from a finite core, over **932 initial conditions** (structured +
random, both signs of φ′,ρ′, Z∈[0.3,20], varied φ_c,ρ_c), **not one** reaches `v=e^{−φ/2}=0` at finite r. Structural
reason (robust): the φ-forcing `(4/Z)e^{−2φ}ρ′²/ρ² → 0` as φ→+∞, so nothing drives φ to +∞. **Vacuum fates split ~three
ways — φ-saturation (v finite), φ→−∞ runaway (v→∞), and ρ→0 collapse — but the redshift edge `v→0` is NEVER produced.**
(Wording corrected per verifier: the universal statement is "no finite `v→0`/`φ→+∞` edge," not "φ saturates," which is
only ~1/3 of fates.)

## What it means (the reframe — for the forward plan, not banked as physics)
The finite `φ→∞` edge — the `x_max` frame — is **not a vacuum/geometry feature; it is matter-sourced.** This dovetails
with the dimensional truism (a maximum *distance* cannot come from c,G alone — needs a mass) and with matter-as-scale-
breaker: vacuum UDT is scale-free and featureless, matter supplies both the scale and the edge. Consequence: Thread A
(the background) cannot be derived vacuum-first — it merges with Thread B (the φ-matter coupling). The forward test is
`matter_filled_background_closure_DESIGN.md`: whether the direct source `α·ξ·e^{αφ}ρ²I_r` (which GROWS with φ for α>0)
produces a finite edge, and whether closure pins a critical matter amount. **This meaning-layer is a LEAD; only findings
1–3 are the verified result.**

## Scope (regime + premises — this result is ONE tile)
Static · spherically-symmetric round φ(r),ρ(r) · Branch-P · **vacuum** (matter off). NOT covered: off-round shear,
Branch-G exterior, time-on. The field-equation form (`native_field_equations_constrained_two_player_results.md`) is
**DERIVED-but-NOT-yet-canon** (its line 6) — a carried caveat. "No finite edge" is scoped to vacuum Branch-P round
static; matter and other sectors are the open forward question, not foreclosed here.

**⚠ SCOPE NOTE (added 2026-07-08, provenance trace a9865905): Branch P is the CELL / MICROPHYSICS regime, NOT the
macro regime — so this result does NOT bear on whether the MACRO universe has a redshift edge.** The founding doc
(`native_field_equations_constrained_two_player_results.md` §6, commit f766478) explicitly maps Branch P to "finite
cell / microphysics" and proves it "intrinsically FINITE-DOMAIN" with no asymptotic vacuum; the macro/continuum regime
is a DIFFERENT native equation (Branch G, `(r²φ')'=0`). The two-player scalar equation is thus a PARTICLE-CELL tool;
the "no φ→∞ edge in its vacuum" was close to baked-in (Branch P is finite-domain by construction) and says nothing
about the macro. The macro universe has NEVER been solved directly from the native field equations — see
`macro_universe_native_MAP.md`. This result stands as a correct CELL-regime statement (cosine ≠ Branch-P native), no more.

## Verifier record (verifier-before-record)
Blind adversarial verifier, fresh zero-context, 2026-07-08 (agent af138cbaad30111c5). Independently re-derived C1–C4
with its own sympy + independent integration (`verify_cosine_reconciliation.py`); adversarially hunted for an edge
(932 ICs) and for a gauge making the cosine a coupled solution (none exists). Verdicts: **C1 CONFIRMED, C2 CONFIRMED,
C3 CONFIRMED (load-bearing; with the "no v→0 edge" rewording adopted above), C4 CONFIRMED.** No false pass, no sign/
factor error that flips a verdict. One fix owed and applied (C3 wording). Overall: SOUND to build the closure scan on.
