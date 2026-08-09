# RA2 ADVERSARIAL REVIEW 1 — full independent recompute + the triviality attack

Date 2026-08-09 | reviewer: fresh adversarial agent (Fable), zero derivation context |
Brief: recompute both phases with independent methods; quantify or kill the non-trivial
content. Script: scratchpad `ra2_recompute.py`, `shoot_Rform.py`, `umin_sens.py`,
`xw_check.py`, `center_bc_test.py` (bounded CPU, no monitors). `derive_ra2.py` opened only
AFTER the recompute, per brief.

## 1. Recompute verdict — the numbers REPRODUCE

- **m=0 low-k tables (all four LC regions):** reproduced by an independent method
  (R-form Prüfer/shooting, RK 1e-11, regular center branch R'→0, Dirichlet wall at their
  u_min=1e-5): R1 ω₁=1.08471 (banked 1.08471), R2 0.26335 (0.26337), R4 0.86614 (exact);
  banked first ratios 2.5082/2.7886/2.5691/2.4235 all confirmed. Witness percentages vs
  the measured first ratio (+2.83/+14.32/+5.32/−0.65/−45.46) all reproduce.
- **Wedge intrinsic channel (m=−1 QEP):** independent uniform-x companion linearization
  reproduces 2.41464 vs banked 2.41486 (0.1%); ratios 1:1.3313:… vs banked 1:1.3304:….
- **x_w:** 30-digit mpmath quadrature matches every banked π/x_w at their truncation.
- **Wall-truncation systematic (my strongest numerical attack, FAILED):** the x-form wall
  endpoint is regular (Q_c→0, finite x_w) and u_min=1e-5 chops ~6% of R2's true cavity
  length — but refining u_min 1e-5→1e-9 moves ρ₁ by ≤0.6% and β_k by ≤0.005: the banked
  band is truncation-stable. Grid/rmin variations likewise.
- **N4 (+1/2 wall-datum shift):** shift magnitude +0.5035 confirmed; their zero-mode-drop
  + interlacing handling checked in-code and consistent.
- **Phase-2 fit mechanics:** exact reproduction — a=310.07, β=−0.3063, residuals
  (5.5, 12.9, −25.4, 2.5, −8.6, 13.6, −0.5), max 25.4σ, per-peak β_k, odd/even means
  −0.3297/−0.2752. Unweighted LS, as coded.
- **Instructive false alarm (mine):** my first solver (x-form, Dirichlet at r_min)
  disagreed by 10–17% in ω₁ — because the m=0 center is LIMIT-CIRCLE (−1/(4x²)) and
  truncation-Dirichlet converges (logarithmically) to a DIFFERENT self-adjoint extension
  than the regular branch. The banked choice (R bounded, R'→0; P-RA2-6 THEORY tag) is the
  declared and physically standard one, and the m=−1 channel (limit-point, no freedom)
  agreed across all my methods — confirming the diagnosis. Consequence recorded in §3(A4).

## 2. THE TRIVIALITY ATTACK — quantified (the headline)

**(a) The comb form is 100% generic.** Any 1D SL cavity with finite x_w gives ℓ_k ≈
ℓ_A(k+β) by Weyl asymptotics (my recompute: spacings/(π/x_w) = 1.001–1.002 by k=10–20 in
every channel). The mainstream's own peak parameterization ℓ_m ≈ ℓ_A(m − φ), φ ≈ 0.25, IS
this comb. "Matches a comb" carries zero UDT content.

**(b) The offset band is mostly Maslov-generic.** A Dirichlet wall + regular (ν=0 Bessel)
center gives β = −1/4 asymptotically for ANY such cavity (j_{0,k} = (k−1/4)π + O(1/k)).
My 7-cavity synthetic survey (same structural class, non-UDT potentials) scatters β over
≈ [−0.46, −0.09]. Quantities: banked band width 0.15 = **15% of the full Robin period**
(uniform-prior landing odds ~1-in-6.7); against the structural prior (spread ≈ 0.37 around
−1/4 seen across both the synthetic and UDT sets) the band covers ~40% — **landing odds
~1-in-2.5**. So the band membership is a real but WEAK discriminant, far from rigidity.

**(c) The UDT-specific increment, measured:** band center −0.335 sits −0.085 below the
generic Maslov −0.25 (the Q_c displacement); the data's global offset −0.3063 sits −0.056
below it. The UDT band center is ~2× closer to the data than the bare generic phase
(0.029 vs 0.056 in β). BUT the data's own unmodeled even/odd alternation is 0.055 in β —
**the claimed UDT-specific signal is the same size as the data structure the model cannot
produce.** Conclusion: the contact cannot yet discriminate UDT's cavity from ANY
regular-center/Dirichlet-wall cavity of the same symmetry class.

**(d) Ours-vs-theirs, exact epistemic statement:** β = −0.3063 and φ ≈ 0.25–0.31 are the
same number in different sign conventions. The claim "our band predicts where theirs
fits" is NOT sustainable: the mainstream also DERIVES φ ≈ 0.25 (+ per-peak corrections)
from photon-baryon driving (Hu & Sugiyama 1995; Doran/Lilley 2001) and additionally
derives the alternation and reaches measurement precision. The honest asymmetry is
smaller: our offset came from a blind-in-session derivation with the Robin freedom
demonstrably unspent; theirs from richer physics fit at full precision.

## 3. Attack outcomes 2–5

- **(2) Doublets:** banked fractional splittings 0.837/0.632/0.499 at the h₀=1/2 witness
  are ORDER-UNITY — any lit |m|>0 power at such h₀ destroys the single-comb structure,
  not decorates it. Parking visibility behind the source obstruction is legitimate in the
  letter, but the RA2-PARTIAL outcome must state the conditionality: the match assumes the
  backdrop effectively excites m≈0 (or h₀≪1 at the probed shells). Latent kill-switch,
  currently underweighted (amendment, not kill: h₀ is a witness value, underived).
- **(3) Dirichlet representative:** +1/2 shift verified; Robin freedom NOT spent (the LS
  fit is unconstrained; β landed in the Dirichlet band on its own). "Pre-declared" =
  declared in PHASE1_NOTES P-RA2-5 (blind file, mtime pre-Phase-2), NOT in the frozen
  prereg. Cap: file-blindness cannot blind an LLM agent to a famous target (φ≈0.25 is
  textbook); Dirichlet/Friedrichs has independent mathematical canonicity, so the choice
  stands, but "the strongest anti-tuning fact" phrasing should be tempered.
- **(4) F-RETRO:** mtime chain verified on disk (prereg 23:36:39 → pycache 23:52:16 →
  PHASE1_NOTES 23:55:51 → Phase-2 append 23:57:31 → run_output 23:57:38 → PHASE2
  23:58:16); token audit of PHASE1_NOTES.md and derive_ra2.py lines 1–290: CLEAN (one
  regex false positive: "310" inside the blind ratio 5.3101). Same-session ceiling stands.
- **(5) Freedom accounting:** the prose "parameters actually fitted = 1 (scale)"
  OVERSTATES — the script itself (correctly) calls it a "2-parameter comb fit"; β was
  fitted, then checked post-hoc against the pre-banked 0.15-wide window. Correct to:
  2 fitted parameters, one certified inside a blind-banked band. 6-channel look-elsewhere
  and the R4 1-of-5 trials factor: disclosed, honest. (A4) The m=0 CENTER branch is a
  second spent datum (a different extension moves ω₁ ~15%, the band by ~+0.05–0.1);
  it rides a THEORY tag (P-RA2-6) — legitimate, but it should be NAMED beside the wall
  datum wherever the band is quoted.

## 4. VERDICT

**SUSTAINED-AMENDED.** Every banked number reproduces under independent methods; the
ordering is machine-clean; the honest negatives (25σ, alternation, wedge mismatch,
obstructions) are first-class as claimed; RA2-PARTIAL is the right class. Required
amendments: (A1) the triviality quantification of §2 travels with the result — the
contact is ~generic-comb + Maslov phase, band-membership worth 1-in-2.5 to 1-in-6.7, and
the UDT-specific increment is currently the same size as the unmodeled alternation;
(A2) "1 fitted parameter" → 2-parameter fit, β band-checked; (A3) the m≈0-dominance
conditionality of the match stated in the outcome; (A4) the center-branch datum named;
(A5) anti-tuning language tempered per the LLM-prior cap. Not killed: the band is
narrower than ignorance, blind-banked, Robin-unspent, and the structural fact "UDT's LC
regions form a finite-x_w cavity whose regular-branch comb lands the measured offset
decile" survives adversarial recompute.

— Adversarial Review 1, 2026-08-09. NOT committed (per brief).
