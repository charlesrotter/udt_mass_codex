# ADVERSARIAL REVIEW 2 — D2 (scope / falsifiers / ledger honesty)

Date 2026-08-08 | branch grok | reviewer: R2 (Fable, independent of the derivation agent)
Brief: F-RETRO both directions / F-FREEZE / F-ONEHORSE / scope + ledger honesty. Hostile.
Read: PREREGISTRATION.md (frozen), DERIVATION_NOTES.md, derive_d2.py, run_output.txt, parent
MAP (owner rulings §0), D1 CONSOLIDATED (inheritance list). Machine run REPRODUCED fresh:
45/45 True. Spot-verified by hand (not trusted from the notes): the B4 Gaussian covariance
identity Cov(U²,V²)=2Cov²+4EU·EV·Cov → 2a⁴c²+4a²s²k_p²c; the fixed-cone assembly of the
depth law −(A_r+A_t/A)/(2A) (endpoint-only differentiation legal because the cone is fixed
by the observation event — checked); the A10 null eigenline (v0=v2=(sρ−1)/ρ² exactly); B6a's
log-form equivalence; and the branch-correctness of dλ_t/dμ²|₀ = 1/(ρ²s²−1) on BOTH sides of
ρs=1 by implicit differentiation (the machine window covers only s>1/ρ; the formula holds for
the causally-continuous branch on both sides — see A-3 below). Language/leakage grep: no
E-values, no angles, no floats, no O-A/O-B/O-D/O-E tokens (the only "D4" hits are the KEY-label
collision with the menu-item name — cosmetic, flagged A-7).

## F-RETRO, both directions (primary) — DOES NOT FIRE

(a) Over-deflation hunt: the machinery is AFFIRMED, not deflated — three channels derived with
exact block spectrum behind them; the native thresholds (μ_c, ρs=1, the fold) are named as
native, not buried. No suppression found. (b) O-C-rescue hunt: the 3-route honest-bounds list
was checked for curation. Route 1 (inheritance) honestly implies a GENTLE-FALL θ(z) drift of
any inherited feature — the notes do NOT mention that this matches O-A's prediction and sits
against the known E2 tension; nothing anywhere steers toward the reversed drift or any DESI
number (grep clean; K_FRETRO reproduced). The nuanced landing is DERIVED, not positioned.
Exhaustiveness: near-exhaustive; two amendments owed (A-1, A-2 below) — the D1 window-set
route omitted from the list, and one asserted-not-derived sub-claim inside route 2.

## F-FREEZE + the owner's no-freeze ruling — DOES NOT FIRE; AMENDED

All eight SS lines audited. SS1/SS3/SS6/SS7/SS8 sound; SS2's full-generality escape genuinely
routes through SS7's linear accumulation (B7) + B5. SS4's slowly-varying confinement to the
no-fold conclusion is GENUINE (the depth law itself needs no slow-variation). Findings:
- **A-4 (the sharpest find): the "EXACT for generic A(t,r), no slice" claim is CHART-ANSATZ-
  conditional and the ansatz is mis-tagged.** Time-live, the derivation assumes the lock FORM
  persists with a single function: ds² = −A(t,r)dt² + dr²/A(t,r) (+ the SS3 h term) — B=1/A
  with the SAME time-dependent A, g_tr=0. P-D2-1 tags this "D1 P-L1 inherited unchanged
  (THEORY, canon C-2026-08-06-1)" — but the canon's lock⇔areal-anchor equivalence (B=1/A ⟺
  G^t_t=G^r_r) is a STATIC statement; its time-live persistence is a CHOICE, not cited theory.
  Load-bearing: the exact depth law's FORM and the fold condition A_t=−A·A_r both ride it.
  AMEND: add ledger line SS9 (time-live lock-form ansatz: single A(t,r), B=1/A, g_tr=0 beyond
  the declared h; inheritance = generic B(t,r)/g_tr re-derivation) or retag P-D2-1 chose-with-
  theory; soften §7a/SS4 "no slice" to "no slice beyond the chart ansatz". Conclusion-changing?
  The qualitative verdict (smooth law, fold as free-data condition) plausibly survives generic
  B; the EXACT forms do not — that is exactly what a ledger line is for.
- **A-5**: SS5's non-Gaussian escape overstates. "Pointwise-map scale-covariance" needs
  ALL-ORDER scale invariance of the input (the μ² output 2-pt function is an input 4-pt
  object), which is STRONGER than D1 §1's two-point definition of featureless. One sentence
  in the SS5 inheritance column owed. (For Gaussian input the Hermite/positive-coefficient
  series plus B5 covers even the un-truncated λ_t map — the O(μ⁴) flag is safe.)
- **A-6**: KEY D4 is TRUE-BY-FORM (positivity decided by symbol declarations; the substantive
  content rides D1 K17/K18 + F4a/F4b). Label it per the D1 R1-V1 precedent.
- **A-3**: the "COINCIDE" claim (§2, causal-labeling window = real near window) and A6/A9b are
  machine-covered only on s>1/ρ (the w-parametrization). The s<1/ρ side holds for the
  causally-continuous branch (my implicit-diff check) but is asserted; state the branch
  convention and the s<1/ρ status in §2, or scope the sentence.

## F-ONEHORSE — DOES NOT FIRE

No comparative origin statements; no O-A/O-B/O-D/O-E content. The fold/caustic channel is
NOWHERE connected to D4/O-E (grep-verified) — correctly left for the matrix step. **A-7**
(cosmetic): the script's KEY names D1–D5 collide with the arc's step names D1/D4; harmless
in-package, rename-worthy if excerpted.

## Scope / excerpt hazards — AMENDED

- **A-8**: the §10 sentence "NO preferred angular scale arises natively" is quotable without
  its conditions (the paragraph is scope-stamped; the sentence is not). AMEND inline:
  "...arises natively (below the fold onset; declared sub-slices SS1–SS9; time-live lock-form
  chart)". Same for the §3 T1' bold verdict's last sentence.
- Threshold coincidence (elliptic edge = causal-labeling degeneration): DERIVED symbolically
  (A7–A10), not numerically observed — robust. Wonder-to-caution: dial DOWN one notch — this
  is the generic exceptional-point behavior of an η-pseudo-Hermitian block (eigenvector goes
  neutral where the real spectrum breaks), i.e. structural, not a coincidence. **A-9**: add
  that one-line generality note so the coincidence is not over-read.

## Debt service (D1's 7-item inheritance + review-added item) — one gap

(1) time-live pattern generation — SERVICED (T1', keys). (2) μ beyond the static stratum —
SERVICED (Block A exact). (3) tracer-phase — SERVICED (T3'; E1/E2 keys; the forced-phase
argument checked). (4) back-reaction — explicitly RE-INHERITED (SS6). (5) off-center
observers — implicitly re-inherited (banner/SS6); **A-10**: make it an explicit line.
(6) O-E geometries, (7) source-statistics origin — correctly left unowned (F-ONEHORSE).
**A-11 (the real debt gap)**: the review-added item AND prereg §1(iv) — "does the live map
move the window-break beyond the smooth dictionary drift?" — is serviced by ASSERTION only
(§5's echo of D1 §4(i); no KEY, no derivation). The likely answer is cheap (the break rides
Δℓ_p(bin)/r(z) through the NOW-time-live dictionary D2 + the O(μ²) per-direction modulation
— smooth, so "no, beyond a smooth per-direction modulation"), but it must be DERIVED or the
item explicitly re-inherited. AMEND either way.
Restatement disclosures: five in-script DECIDABLE-RESTATEMENT blocks covering six first-run
False keys — count consistent; each spot-checked genuinely equivalent (none weakens a claim);
the D3 "wrong construction, not wrong claim" disclosure is honest.

## VERDICT: **AMENDED**

No falsifier fires. F-RETRO clean both directions; F-ONEHORSE clean; F-FREEZE and scope clean
after amendments. Owed in place: A-1 (window-set route pointer in the honest-bounds list),
A-2 (tag the excursion-set scale-free sub-claim as riding SS5, asserted), A-3, A-4 (the
load-bearing one: SS9/P-D2-1 retag + "no slice" softening), A-5, A-6, A-8, A-9, A-10, A-11
(derive or re-inherit the window-break re-check). With these applied the package is honest,
reproducible, and lands where it claims to land. Ceiling: contributes to verified-LEAD only
jointly with R1; external bar travels. Not committed (owner's gate).

— R2, 2026-08-08.
