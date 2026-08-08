# M3-AUDIT — blind adversarial review (2026-08-08)

Reviewer: blind adversarial review agent (Fable), fresh context, contract 2d9933d1.
Scope: grade logic, cheap-number recomputation from cached `audit_data/`, F-STEER
symmetry, F-FIX sweep, driver-failure handling. No recounting of pair blocks. Not committed
by reviewer.

## Numbers recomputed (own scripts, from cached jsons/blocks)

- **Bit-identity independently reconfirmed** (not trusting the stored `repro_check`):
  reassembled `assemble_union` w/σ from `blocks/` vs the M3 checkpoints for
  LRG 0.95–1.00 sys and QSO 1.85–2.00 sys — max|Δw| = 0.0, max|Δσ| = 0.0, all 40 bins.
- **B2 drop-one ranges**: 8.8° shell center range 0.503°–11.029° (report: 0.50–11.03),
  13 regions >1 bin = 9 NGC + 4 SGC (report: 13; 9+4), min Δχ² 15.6 > null-95 10.9.
  Control 2.359°–2.474°, max 0.36 bins, 0 regions >1 bin. QSO 1.85–2.00: max 23 bins,
  drop-NGC-13 → θ_b 0.0854° (below window floor), min Δχ² 8.89 < null-95 10.65
  (de-triggers). All reproduce. (Cosmetic: my bins-moved recompute with Δlnθ 0.0914
  gives 31.33 vs reported 31.05 — bin-width convention; the >1-bin counts are identical.)
- **B5 shifts**: all nine reproduce exactly from `b5_*.json` (θ +1.369%, −2.272%,
  +0.019%, +0.022%, +0.023%, +0.101%, +0.617%, −0.064%, −0.143%; A-shifts likewise).
- **B4 calls**: LRG 1.05–1.10 NGC 1.196° (19.75) vs SGC 2.839° (6.03 n.s., opposite
  sign, 9.6 bins off) — NGC-only confirmed. QSO 1.85–2.00 NGC 0.243° (7.34 n.s., +A)
  vs SGC 0.858° (10.79, −A) — sign+location disagreement confirmed. Control both caps
  significant, same sign, 0.45/0.29 bins from full — confirmed.
- **Drift note**: max |z̄−z_mid| = 0.0027 (QSO 0.95–1.10); max |Δθ| = 0.0098 bins;
  signs mixed (both ±). "Two orders too small, sign-incoherent" verdict reproduces.
- **B6**: grid best = 11.459° (last bin); constrained refit rails at 12.0°, Δχ² 9.77
  sys / 8.75 nosys < shell null-95 ≈ 10.9; unconstrained checkpoint 70.67°/71.05° with
  σ_b at the 1.5 cap, A_b −0.85. Window-edge-artifact reading confirmed.

**No number failed to reproduce.**

## Grade-logic adjudication (the attack surface)

**LRG 0.95–1.00 (8.8°) — GRADE-SUSTAINED (SELECTION-SUSPECT, 5/5).** The
instability≠selection objection was pressed and does not overturn: this target has two
genuinely LAYER-SPECIFIC flags, not just instability — B1 (the half-peak crossing
z≈0.973 measured INSIDE the shell, slopes 1.6–2.5× median, cap-asymmetric edge) and B5
(toggling a named selection weight moves the position past the M3-mirrored 1% bar).
B2/B3/B4 instability then corroborates rather than carries. Contract's ≥2-named-layer
standard met on B1+B5 alone. Honest residue the annotation should keep: min drop-one
Δχ² stays significant (15.6 > 10.9) — SOMETHING is there; it is its 8.8° position and
scale that are unconstrained. "Suspect," not "proven artifact," is the right strength.

**LRG 1.05–1.10 (1.17°) — GRADE-SUSTAINED (SELECTION-SUSPECT), with one correction to
the evidence prose.** B1 is layer-specific and strong (hard z=1.10 catalog boundary,
steepest slopes 3× median, NGC −13.0 vs SGC −7.2). B3's flag is valid as "absent from
the lo half" (lo max at 3.51°, 11.9 bins off). BUT the report's "the near-match sits in
the hi half" overstates: the hi-half max (0.918°) is itself 2.64 bins from the full-shell
1.169° — over the audit's own >2-bin displacement threshold. The bump matches NEITHER
half; "tracks the boundary half" is an interpretation, not a measurement. Flag stands
(absence in lo half suffices); the boundary-tracking language should be read as
directional only. B4 caveated flag consistent with the measured cap-asymmetric tail.
Minority sky evidence (B2 0.10 bins region-stable; B5 0.02% clean) is honestly carried
in the grade text. ≥2 named-layer-consistent flags met (B1 + B3, B4 caveated).

**QSO 1.85–2.00 (0.71°) — GRADE-AMENDED: SELECTION-SUSPECT → INCONCLUSIVE
(NOT-SKY-ROBUST annotation mandatory).** This is the review's one overturn-class
finding, on exactly the instability≠selection ground. Dissection of the three "hard
flags": B2's content (ONE region both moves the center 23 bins and kills the trigger;
min Δχ² 8.89 < null-95 10.65) is a noise-fragility signature, not layer-specific; B4's
content (NEITHER cap significant at the combined center — NGC 7.3 n.s., SGC 10.8
marginal elsewhere, signs opposite) is likewise what a noise-grab looks like — under
the named "cap-dependent selection depth" story the deeper cap should carry the
feature, and neither does. Only B5 (−2.27% under a named weight layer) is
layer-specific, and B1 explicitly found NO landmark ("smooth region"). That is ONE
layer-specific flag, below the contract's ≥2-consistent-with-a-NAMED-layer standard;
the audit itself called the naming "weakest" and recorded the fragile-noise-grab
alternative — that alternative is CO-EQUAL on this evidence, not minority. Honest
grade under the contract's three grades: INCONCLUSIVE, carrying the affirmative
finding NOT-SKY-ROBUST (B2 de-trigger + B4 cap disagreement + B5 sensitivity are all
verified). Downstream effect on the M3 caveat is UNCHANGED — the 0.71° hit stays
discounted either way; the amendment is attribution honesty, not direction.

**LRG 1.00–1.05 (thread ctrl, 2.44°) — GRADE-SUSTAINED (SKY-ROBUST).** Strongest
evidence in the battery: 0.36-bin region stability at min Δχ² 40.9, same center both
z-halves, independently significant in BOTH caps at the same sign/center, 0.02% zfail.
Adversarial scenario hunt: a selection artifact passing all five would need a
cap-symmetric, region-uniform, z-uniform, zfail- AND sys-insensitive layer operating
at 2.4° (WEIGHT_SYS already varied at M3; fiber-collision geometry is at arcmin
scale). No plausible named layer fits; the scenario space is thin. The control-shell
argument is used at its correct, modest strength — "steep dN/dz alone does not
manufacture flags" (indeed the control's edge slopes −8.9/−11.0 are STEEPER than the
8.8° shell's −5.8/−8.9) — it is NOT stretched to "therefore the outliers' layers are
proven"; no overreach found.

**LRG 0.70–0.75 — GRADE-SUSTAINED (SKY-ROBUST), caveat load-bearing.** Earned on a
weaker standard than the control: "no selection-positive evidence in any powered
test" (B2 clean but margin thin 11.1 vs 10.0; B3 unpowered — the 2.37° bump appears
in NEITHER half's max; B4 SGC n.s.). The distinction from QSO 1.10–1.25's
INCONCLUSIVE is real and justified (this shell survives every drop-one and has a
significant same-center NGC fit; that one de-triggers and has neither cap
significant), but any downstream consumer should read this SKY-ROBUST as
power-limited, per the audit's own inline caveats.

**QSO 0.95–1.10 — GRADE-SUSTAINED (SKY-ROBUST)**, same power-limited caveat class
(NGC-dominant; SGC same-sign near-center n.s.; B2/B5 clean and powered).

**LRG 0.90–0.95 — GRADE-SUSTAINED (INCONCLUSIVE).** Honest: only caveated flags, both
readings (z-localized sky vs thinning-onset) genuinely open; position region/weight
stable. Not convenient — this is a thread shell declined acquittal.

**QSO 1.10–1.25 — GRADE-SUSTAINED (INCONCLUSIVE).** Honest, not convenient: every
powered test consistent, but drop-one de-triggers (8.9 < 10.4 verified) and neither
cap is individually significant; "underpowered" is the correct call.

**LRG 0.75–0.80 (70.7°) — GRADE-SUSTAINED (fitter window-edge artifact).** Grid best
at the last bin + rail-at-12.0° below null-95 + σ-cap-pinned A_b −0.85 unconstrained
tail + runaway in both caps: over-determined. B6 was contract-sanctioned; no F-FIX
issue (the banked M3 record, already non-load-bearing, is untouched).

## Falsifier + process checks

- **F-STEER: DISCHARGED.** b1/b2b4/b3/b5 outputs exist for all 9 targets (27 jsons +
  b1 covering all nine); identical machinery per target via `audit_lib` single code
  path; two thread shells not acquitted; the control faced and passed the full
  battery. Threshold application spot-checked for evenness across thread/outlier
  (B3 no-flag calls on thread shells trace to the "strong in the other half"
  requirement failing, not to leniency).
- **F-FIX: DISCHARGED.** Grep sweep of package code+json: no corrected/reweighted/
  revised banked number anywhere; all recomputes are graded diagnostics; B6's
  constrained number is contract-authorized report-only.
- **F-IMPORT-LCDM:** no fiducial imports sighted in the audit path (access via
  v_bao under authorize; drift note uses the SNe-fitted P1 curve as stated context).
- **Driver-failure handling: LEGITIMATE.** `driver_log.txt` ends at
  LRG_0.750_0.800_nozfail_NGC RR2 (16:00:02); the RR3 npz exists in `blocks/`; its
  META records only RR3 in `t_pieces_s` (357.6 s — consistent with a foreground rerun
  of exactly the missing piece via the same `compute_cap_blocks` path); the completed
  unit feeds `b5_LRG_0.75_0.80.json` (70.67→70.57, reproduced). Same code path, no
  count fabricated.

## VERDICT: **SUSTAINED-AMENDED**

Eight of nine grades sustained (one with an evidence-prose correction on LRG
1.05–1.10's B3 "boundary-half" language). One amendment owed: **QSO 1.85–2.00
SELECTION-SUSPECT → INCONCLUSIVE (NOT-SKY-ROBUST)** — the named-layer standard (≥2
layer-specific flags) is not met; selection-vs-noise is undecided; downstream
discounting of the 0.71° hit unchanged. Every load-bearing number checked reproduced
exactly; bit-identity independently reconfirmed on two targets. The synthesis and
drift-direction verdicts stand as written.

Reviewer: blind adversarial review agent (Fable), 2026-08-08. Bounded (~12 min compute,
cached blocks reused, no pair recounting). Not committed by reviewer per instruction.
