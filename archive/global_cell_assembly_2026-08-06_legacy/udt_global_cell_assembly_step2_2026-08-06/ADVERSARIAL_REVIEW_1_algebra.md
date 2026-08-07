# ADVERSARIAL REVIEW 1 — algebra / at-source verification (Step 2 survivor-closure admissibility)

Date: 2026-08-06. Reviewer: fresh-context adversarial agent (independent recompute; NO step-2 code
imported — `ADVERSARIAL_REVIEW_1_recompute.py`, stdout `ADVERSARIAL_REVIEW_1_STDOUT.txt`, all
checks PASS; the one apparent FAIL, A6e, is a sympy log-branch artifact, resolved exact by
`expand_log(force)` + 50 numeric spot checks). Target: `DERIVATION_NOTES.md` (215 lines) vs
`PREREGISTRATION.md`. Instruction: attack the two named load-bearing steps (the monotone spine;
B-freeness), then the L-placement, then re-run the witness independently. NOT committed by me.

## 1. The monotone spine (fold-CONSTRAINS) — **CONFIRMED**

Re-derived from scratch from the source Lagrangian L = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2
(verified verbatim at `udt_two_mirror_rigidity_regrade_2026-08-06/REGRADE_REPORT.md` R1):

- **Flux identity** [A1]: (Zρ²φ')' − 4e^{−2φ}ρ'² ≡ the φ-EL, exactly, ρ''-free. Independent of
  the step-2 script's derivation.
- **Source-blindness** [A2]: symbolic identity — ANY matter term L_m(ρ, ρ', r) with no φ/φ'
  dependence contributes 0 to the φ-EL. There is NO source escape within S: the banked S
  ("arbitrary φ-blind source S(r) in the ρ-equation ONLY", R1 verbatim) excludes φ'-dependent
  matter by definition; a φ'-dependent L_m would evade the identity but is Step-1's fork-2
  premise-level escape, not an in-S one. Hunted; none found.
- **Geometry at source — the inner even core is REAL**: `universe_cell_fold_jc_sigma_results.md`
  :37-38 ("Even fold (inner, r_c): ... stationarity ALONE ... pins φ'(r_c)=ρ'(r_c)=0, values
  φ_c, ρ_c free") and `flux_sealed_universe_cell_miniMAP.md` :11-12 ("inner turning sphere
  (mirror: φ'_c = ρ'_c = 0, ρ_c > 0)"). The step-2 citation is faithful; caveat 2 (inner closure
  itself a CHOSE, OC2 germ freedom) is honestly carried.
- **The cuts follow exactly.** Φ(r_c)=0 (from φ'(r_c)=0) + Φ' ≥ 0 ⇒ Φ ≥ 0 ⇒ sign(φ') = sign(Z)
  pointwise (ρ² > 0); anchor Δφ = ln(1101) > 0 ⇒ Z > 0 forced; q = Φ(r_s) = ∫4e^{−2φ}ρ'² with
  q = 0 ⇔ ρ' ≡ 0 ⇔ Δφ = 0, so the anchor forces q > 0 and ρ' ≢ 0. The flat-then-strictly-rising
  claim is exact: Φ(r) > 0 strictly for r > r* (r* the sup of the initial ρ'≡0 segment), since
  Φ(r) is the integral of a nonneg integrand not identically zero on [r_c, r]. CUT-4 (ρ'(r_s)=0
  ⇒ Φ'(r_s)=0; q slaved to the bulk profile) is immediate from the identity. φ-slaving (CUT-1):
  the φ-IVP from (−ln(1101), 0) is unique given ρ (Lipschitz RHS, a-priori bound e^{−2φ} ≤ 1101²
  from φ' ≥ 0) — confirmed.
- **Sign-branch escape hunt**: the flipped EL-sign convention (regrade C7) mirrors everything
  (Φ non-increasing, Z < 0 forced, same monotone φ) — no escape; caveat 4 covers it.
- **Route-B escape hunt** [A4]: re-derived with the regrade-C6 mixing term 4ρρ'φ' at GENERAL Z:
  (Zρ²φ' + 4ρρ')' − 4e^{−2φ}ρ'² ≡ the Route-B φ-EL — same nonnegative RHS, confirming caveat 5.
  Both fold ends zero Φ_B. HONEST SHARPENING (finding, not break): under Route B the pointwise
  φ-monotone form of CUT-2/CUT-3 is NOT derived (only φ + (4/Z)ln ρ non-decreasing — φ itself
  could in principle dip where ρ rises), and Z > 0 is not anchor-forced by this squeeze (it is
  law-forced instead: the regrade records Route B forcing Z=8). Caveat 5 says this; the §IV
  LANDED TABLE row does not visibly carry it. AMEND (cosmetic): the fold row should read
  "S2-CONSTRAINS (CUT-1..4, Route-A form; Route-B modified per caveat 5)".
- **§I.1 IVT existence, each inequality re-checked by hand**: (a) φ' ≥ 0 ⇒ e^{−2φ} ≤ 1101² ⇒ Φ
  bounded ⇒ no blow-up: exact. (c) under φ ≤ 0: Cauchy–Schwarz Φ(r) ≥ 4(ρ(r)−ρ_c)²/r; ρ ≥ 2ρ_c
  ⇒ φ' ≥ 1/(Zr); s(r) ≥ (r/L)² via sin x ≥ (2/π)x; r₁ ≤ L/√ε; D ≥ (1/Z)ln(L/r₁) ≥ (ln ε)/(2Z);
  contradiction threshold ε > 1101^{2Z} = e^{2Z ln 1101}: every step exact as written. IVT sound
  (continuity from smooth parameter dependence + the a-priori bound). Numerically D(ε) is
  monotone over probes [0.001, 1.0] with a single crossing — consistent.

**Verdict cell 1: fold-CONSTRAINS CONFIRMED** (with the cosmetic Route-B table rider above).

## 2. B-freeness (glue-ADMITS-ALL) — **CONFIRMED at the posed level; one precision rider owed**

At source (`udt_p4_seam_closure_derivation_2026-07-30/EXACT_DERIVATION.md` K6c, :79-80,
:179-184): the glue leaves δS_seam = (q/2)δρ ≠ 0 unless a seam functional B with B'(ρ_s) = q/2
is added ("solved exactly; nonclosure certified"); B is "precisely the underived differentiable
finite-cell boundary action, the 07-18 OPEN gate". Verified: the citation is faithful; the
one-point condition B'(ρ_s) = q/2 is solvable for ANY (q, ρ_s) (linear B suffices, C¹, finite —
no hidden sign/finiteness/well-posedness cut found; K6c itself certifies well-posedness once B
is present); no pin on φ(r_s), ρ(r_s), or ρ'(r_s) appears at source. The B ≡ 0 ⇒ q = 0 ⇒
dead-class point is correctly carried at action level (§II.3(b)). The one-way q-slaving note
(a) is correct and honestly anti-interlock.

**The one substantive rider (AMEND, does not flip the cell as posed):** ADMITS-ALL is the
B-UNFIXED (theory-class) reading — correct here because B is at-source a FREE/OPEN object, so
each admitted configuration may carry its own B. But for any FIXED B (i.e. if/when the 07-18
gate is closed and B is DERIVED), the natural BC q[ρ] = 2B'(ρ_s[ρ]) becomes ONE scalar codim-1
cut on the anchored profile class — comparable in size to the anchor cut itself — and the glue
cell flips to S2-CONSTRAINS(codim-1). §II.3(b) states B-must-exist but NOT this fixed-B
flip-condition; it should travel with the table so Step 3+ cannot quietly lean on ADMITS-ALL
after a B derivation lands. Q2c as prereg-posed (closure = generic glue with B open) lands
ADMITS-ALL: sustained.

## 3. The L-lead placement — **CONFIRMED both cells** (one honesty note)

- [A5a] φ_L' = 1/(2(X−r)) ≠ 0 for every finite X: violation (i) exact.
- [A5b] Flux-identity residual under φ_L at ANY ρ'(r₀)=0 point = Zρ²/(2(X−r₀)²) ≠ 0 — recomputed
  independently (ρ'' left arbitrary; it cancels): ρ' = 0 is impossible at any point within S, so
  BOTH ρ-pins fail. Violations (ii)/(iii) exact. Honesty note (already admitted at §I.4): "(iii)
  = (ii) at the seam" — the count is 2 independent facts stated at 3 loci, not 3 independent
  facts. Cosmetic.
- [A6a-d] Bulk quadrature re-derived FROM SCRATCH (substitute φ_L, u = ρ'/ρ, m = X−r): my
  independently-derived quadratic matches 4(m/X)u² − (Z/m)u − Z/(2m²) = 0 exactly; discriminant
  Z²/m² + 8Z/(mX) > 0 (Z>0); root product −ZX/(8m³) < 0 ⇒ two real nonzero roots of opposite
  sign; the identity is FIRST-order in ρ, so the u₊ branch integrates to an exact bulk solution
  ρ₊ = ρ_c exp∫u₊ > 0 on any compact [r_c, r_s] ⊂ (0, X) (u₊ bounded there). Δφ_L =
  (1/2)ln((X−r_c)/(X−r_s)) exact [A6e, resolved]. Z<0 discriminant can indeed go negative [A6f].
- **Rescue-limit citations check out**: X → ∞ is canon-blocked (CANON.md C-2026-06-10-2 :33
  "There is no spatial infinity"); the free-core inner end is the fold-doc's own "different
  class" (`universe_cell_fold_jc_sigma_results.md` :65-66). Both faithful.

**Verdict cells 3/4: L-outside-fold CONFIRMED (3 exact violations, counted honestly as 2
independent facts); L-inside-glue-bulk CONFIRMED (exclusion entirely via the inner end).**

## 4. The witness shoot — **CONFIRMED, independently reproduced**

Own integrator (scipy RK45 adaptive, rtol 1e-11 — different method, step control, and root
finder from the step-2 fixed-step RK4 + bisection), Z = 8, L = 1, ρ_c = 1, sin² family:
**ε* = 0.011032, q = 73.689783, |φ(r_s)| < 3e-14** — matches the claimed ε* ≈ 0.011032,
q ≈ 73.69 to all printed digits; tolerance-robust (Δε* ~ 2e-12 across rtol 1e-9/1e-11).
Genericity probe (NOT in the step-2 script): a second, independent profile family (smoothstep
r²(3−2r), both ρ-pins met) also carries the anchor at ε* = 0.011074, q = 72.497 — existence is
not tuned to the sine family. D(ε) monotone across probes; single crossing.

## Per-cell verdicts

| Cell | Verdict |
|---|---|
| fold-CONSTRAINS | **CONFIRMED** (cosmetic amend: carry the Route-B caveat-5 rider in the table row) |
| glue-ADMITS-ALL | **CONFIRMED as posed** (amend: add the fixed-B flip-condition rider — any derived B ⇒ codim-1 cut ⇒ CONSTRAINS) |
| L-outside-fold | **CONFIRMED** (3 exact violations; honest count = 2 independent facts) |
| L-inside-glue (bulk) | **CONFIRMED** (boundary-excluded-not-bulk-excluded; rescue limits verified canon-blocked / out-of-geometry) |
| witness | **CONFIRMED** (independently reproduced to all digits; + genericity via a second family) |

**Overall: S2-MIXED SUSTAINED** (no load-bearing step broken; two precision riders owed to the
landed table, neither changing a verdict as prereg-posed). F-STEER spot-check from this side:
the anti-spine cell (ADMITS-ALL) is reported plainly and the pro-spine attributions (§I.3
"honest attribution") are accurate — most constraining power is S + the inner fold, the odd
fold's marginal cut is CUT-4; no steer detected in the algebra. All conditional on the verbatim
S-caveat; ratio-level; Route-A primary. NOT committed by the reviewer.
