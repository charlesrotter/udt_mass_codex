# Adversarial Review B — attack the reframing; hunt OP-PARTIAL

Reviewer: independent adversarial pass (blind recompute, no derivation code imported).
Date: 2026-08-05. Target: `DERIVATION_NOTES.md` (LEAD/UNBANKED). **VERDICT: NARROW.**

---

## Q1 — Do banked global constraints fix the profile toward L? (the core hunt)

**Constraints in play (independently read):**
- Reciprocal lock `g_tt g_xx = -c^2`, `A = e^{-2phi}` — constrains FORM, not profile (agree w/ driver).
- Regularity at observer: `A(0)=1`, `A'(0)` finite.
- x_max asymptote (G14, `STATUS_AND_WORKFLOW.md`): `A -> 0` (`phi -> inf`) as `x -> X_max^-`,
  comparison dilation `exp|delta| -> inf`.
- Finite-cell / WR-L canon (C-2026-07-09-1a): the wall is a **causal horizon** — finite PROPER
  distance `∫dx/sqrt(A) < inf`, infinite OPTICAL reach `∫dx/A = inf`; finite-proper axiom kills
  the `α=2` power, `α=1` is the causal ceiling.

**Explicit counterexample that defeats OP-PARTIAL.** Take the driver's own H
(`r = X tanh phi`). In coordinate form `A_H(r) = (X-r)/(X+r)`. Check every banked global gate:
- Regularity: `A_H(0)=1`, `A_H'(0) = -2/X` finite. ✓
- x_max asymptote: `A_H -> 0` as `r -> X`, `phi -> inf`. ✓
- Near-wall exponent: `A_H ≈ (X-r)/(2X)` — **linear, β=1, identical to L's** `A_L=1-r/X`.
  So the finite-proper `α`-selector (kills β≥2) does **not** separate H from L either. ✓
- Finite proper: `∫₀^X sqrt((X+r)/(X-r)) dr` ~ `(X-r)^{-1/2}` near wall → finite. ✓
- Infinite optical (causal horizon): `∫₀^X (X+r)/(X-r) dr` ~ `2X/(X-r)` → log-divergent → inf. ✓

**H = (X-r)/(X+r) satisfies EVERY banked global constraint — regularity, x_max asymptote,
finite proper room, infinite optical / causal horizon — yet H ≠ L.** Therefore the banked
global constraints do **NOT** fix the profile toward L. Only P-opt (or SNe, see Q4) discriminates
L from H. The x_max frame's OWN text is the load-bearing corroboration: workflow gate #7 ("compare
profiles only as candidates; do not choose from endpoint behavior") and line ~73 ("passing the
asymptote is necessary but NOT sufficient; many functions share the limiting behavior"). The banked
global source explicitly disclaims profile-selection.

**BUT — the driver's wording "ANY profile A(x)" is too strong (this is the NARROW).** Once the
OTHER banked constraints are folded in, the admissible set is a CONSTRAINED FAMILY: monotone,
`A(0)=1`, `A -> 0` at `x_max`, near-wall exponent `β ∈ [1,2)`. That is real partial fixing —
just NOT toward L. So the honest statement is "P-opt selects L within a globally-constrained
family," not "the profile is free." This is a refinement of scope, not a move to OP-PARTIAL-toward-L.

## Q2 — Is P-opt more fundamental than "a generic law choice"? (over-flattening?)

Yes, the reframing over-flattens. `dl_opt = κ dphi` is a **rigid, codimension-∞** principle: one
constant κ (then identified with X) fixes the ENTIRE profile. That is categorically stronger than
"the orchestra's free parameter `a`," which is a genuine 1-parameter continuous DOF. Equating the
two hides that P-opt is an AXIOM-quality statement (light meters depth affinely), not a knob.
Fair to the driver: P-opt is still **underived** (tagged WORKING PRINCIPLE; equivalence-principle
GAP open), so it is not orchestra-forced — OP-INDEPENDENT survives. But "same class as the free
law parameter" understates its specificity. Refinement, not refutation.

## Q3 — Baseline check (misrepresentation?)

Independently verified against `simple_metric_L_native_optical_derive_results.md`,
`simple_metric_elegance_SNe_character_results.md`, `simple_metric_L_P_selection_derive_results.md`:
- `d_L/X = z(z+2)` — correct (full light + L). ✓
- `p_r = -ρ` — correct (`ρ=1/(4πXr), p_r=-ρ, p_t=-ρ/2`, Einstein readout). ✓
- `χ²/dof = 0.91` — REAL: Pantheon+ N=1580 full STAT+SYS, "linear ceiling z(z+2)" = 0.91 / RMS
  0.158; L's chart independently = **0.910** in the F(φ) table. ✓
- conditional-on-P-opt — correct (baseline header = LEAD/CONDITIONAL on P-opt). ✓
- **Minor imprecision:** driver calls it a "native SNe fit." The baseline is explicit that SNe is
  "character/clue, NOT used in the derive," and that L is merely BEST among named maps —
  `F=φ/(1+φ)` = 0.937 is very close. "Native SNe fit" slightly conflates the (SNe-free) derive with
  the separate SNe-character pass. Not a material misrepresentation.

## Q4 — Is the reframing SNe-shopping? (the smuggle hunt)

**Partly.** Bullets 1–2 are legitimate: "one law-selection gate, not two," and "the fit is a
prediction/test of law→profile (law→L ⇒ SNe native; law→other ⇒ prediction changes)." That is
data-as-test.
**Bullet 3 crosses the line.** "SNe DATA is informative about the law before the law is
derived... the law SHOULD yield ~A=1-r/X to keep the SNe agreement" makes the data-favored profile
a DESIGN TARGET for the undelivered law — textbook observing-vs-targeting drift. This bites
precisely because Q1 shows the global constraints do NOT select L but SNe DOES (H: 0.91 vs 2.17 is
the discriminator). Letting "SNe agreement" constrain the law hands the selection to the data.
Bullet 3 must be struck or restated as blind-derive-then-test.

---

## VERDICT: NARROW

- **OP-INDEPENDENT is NOT refuted to OP-PARTIAL-toward-L.** The explicit H = (X-r)/(X+r) passes
  every banked global gate yet ≠ L; the x_max frame itself says the asymptote is "not sufficient."
  Banked global constraints do **not** move the profile toward L.
- **Two real defects to fix before any bank:** (a) "ANY A(x)" overstates freedom — the true claim
  is "P-opt selects L within a globally-constrained family (monotone, A(0)=1, A→0 at x_max, β∈[1,2))";
  (b) reframing bullet-3 ("law should yield L to keep SNe agreement") smuggles targeting — strike it.
- P-opt is a rigid axiom, not a free knob — the flattening in the reframing understates it (harmless
  to the verdict but should be tightened).
