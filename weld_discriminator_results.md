# Weld Discriminator Results

Status: working audit, not canonical.
Created: 2026-06-10.
Script: `native_weld_macro_discriminator.py` (18 sympy/numeric PASSes,
0 FAIL; new 2026-06-10, AMENDED SAME DAY per verifier agent
`a6ef46971a22e0069` — one factual correction to the verdict plus three
strengthening amendments, recorded below). Alters nothing existing; new
files only.

## Conditionality header (binding, per `macro_contamination_map.md`)

Every conclusion below is CONDITIONAL: *given the common pipeline*
(the S116 radial-correlation CMB pipeline with all flagged layers held
fixed as hypothetical). The asymmetric set — everything that differs
between the welds — is entirely GEOMETRY-grade (constraint form, H1
radial structure, weld-derived weight); no quarantined layer enters
asymmetrically. The sand layers (blackbody +1/4 coefficient, mu_g's
13, recycling drive) are common-mode by construction and were never
touched asymmetrically. Absolute amplitudes are NOT compared
(epsilon-class inputs); TT uses the geometry-clean -delta-phi
Sachs-Wolfe channel only. Profile/mu_g/r_CMB enter as DATA-FIT inputs;
the BAO comb scale and breathing envelope are INPUT-class.

## Headline: the weld discriminator is COMPLETE — verdict INDISTINGUISHABLE-AT-CURRENT-RECORD

That verdict IS the important result: **the metric's own weld is not
vetoed by the macro data.** The native algebraic weld (identically
`delta-T_tr = 0`, `f phi0' H1 = 2 d_t(dphi)`), swapped into the full
S116 CMB pipeline with everything else held common, reproduces the
Einstein-weld (`d_r(e^{-2phi0} H1) = 2 d_t(dphi)`) phenomenology to
~1% of the comb spacing.

The weld swap leaves a real, robust, phase-anchor-independent
differential signal of ~3 ell: the EE comb positions shift DOWN
(native vs Einstein; mean -2.89 ell baseline, range 2.6-4.2 ell over
coherence treatments and variants, direction universal). But the
recorded Planck interleaving PASS has 30-42 ell precision — the
record states it:

- `/home/udt-admin/UDT/SESSION_115_PROMPT.md` line 53: "EE interleaved
  positions matching Planck ~30 in ell (vs ~102 aligned)"
- `/home/udt-admin/UDT/SESSION_116_PROMPT.md` lines 36-37: "EE
  positions interleaved at TT-peak midpoints (mean|Delta-ell| 42 vs
  108)"

That is 10-14x coarser than the 2.9-ell differential, so the script's
own pre-registered downgrade clause FIRES. Both welds sit comfortably
inside the recorded pass band (-23.2 and -26.1 ell from the ideal
midpoints, Einstein and native respectively); the common-mode pipeline
bias (23 ell) is 8x the differential signal.

(The script's original same-day run printed "EINSTEIN PREFERRED —
WEAK" on the claim that the record states no position tolerance. That
claim was factually wrong; corrected same day per the verifier.)

## Findings

- **D1 — radial structure (the welds' genuine difference).** The
  Einstein H1 is CUMULATIVE (finite `W^EE` at r->0); the native H1 is
  LOCAL (raw native weight has a `~(2/phi0_c)/r` interior tail).
  After the Tolman measure both effective EE kernels are
  boundary-dominated: r50 = 9.001 (Einstein) vs 8.972 Gpc (native);
  widths (r84-r16) 0.404 vs 0.487 Gpc. Honesty softening (verifier):
  the V^2-based D1 statistic is weakly (log) rmin-dependent for the
  native weld — practically negligible (rmin x2 moves r50/peaks by
  <~1e-3) — but plain "integrable in C_ell" was too strong.
- **D2 — the 3-ell EE comb downshift, with full robustness battery.**
  Matched-peak shift native-vs-Einstein: mean -2.89 ell at baseline
  (Lc = r_CMB/ell). Battery: grid doubling, coherence x1/2 and x2,
  rmin doubling, envelope-power alternative, source (a)/(b), comb
  spacing/midpoint reference, and (verifier amendment) the comb-phase
  anchor slid over 17 phases spanning one full spacing — in-script
  range [-3.03, -2.84] ell, every matched principal peak negative at
  every anchor (verifier's independent integrator: [-4.00, -3.74],
  same universality). The shift is a fractional-r effect of the weld
  swap, not a phase artifact. Coherence-treatment sensitivity: 2.9
  ell at Lc = r_CMB/ell, 3.8-4.2 ell in the Limber/short-coherence
  limit; direction universal. Caveat: specific to the PRINCIPAL
  sin^2-comb peaks — secondary-harmonic features can shift oppositely.
  Margin honesty: per-variant spreads combine in quadrature to 1.99
  ell < 2.89 signal — survives, but the margin is < 2x (doubled
  spread flips the formal comparison).
- **D3 — both welds ell-flat in R(ell) = C^EE/(ell^4 C^TT):** slopes
  +0.033 (Einstein) vs +0.029 (native) — both inside the S116 record
  range (+0.02..+0.05); differential 0.004, far below spread.
- **D4 — effective comb scale:** ell_eff = 297*r50/r_CMB = 291.7
  (Einstein) vs 290.8 (native).
- **Structural suppression verified.** Kernel mass interior to 5 Gpc:
  1.3e-5 (Einstein) vs 1.4e-3 (native). The welds differ O(1)-6x
  POINTWISE in the interior (1-5 Gpc), yet the observable residue is
  ~1% of the comb spacing: the weld difference lives where the Tolman
  boundary factor `e^{phi0}` (1101 at r_CMB) exponentially suppresses
  the projection weight.

## Consequences

1. **Adopting the NATIVE weld at macro scope is empirically permitted
   at current record level.** The Einstein import is not empirically
   required by the channels tested; the foundational question "which
   weld is true" cannot be settled by the existing CMB record.
2. **A FUTURE sharper test is precisely specified — a banked
   falsifiable differential prediction.** The EE principal comb
   positions at few-ell precision (an actual Planck-likelihood
   position fit) would discriminate: the native weld predicts the EE
   comb sits ~3 ell LOWER relative to TT midpoints than the Einstein
   weld predicts.
3. **All conclusions conditional on the common pipeline** per the
   contamination map: the sand layers are common-mode and were never
   touched asymmetrically.
4. **Honest scope: differential only.** Nothing here validates the
   pipeline absolutely; the common-mode bias (23 ell from ideal
   midpoints) is the pipeline's own crudeness, 8x the weld signal.

## Verifier record (agent `a6ef46971a22e0069`)

- All setup checks re-derived; D1/D2 reproduced independently (own
  grids/integrators): mean shift -2.93 vs script -2.89; Limber -3.80.
- The phase-anchor attack was run and SURVIVED: 17 anchors, all
  matched peaks negative — now in-script as D2c.
- The error-budget comparison was stress-tested: quadrature 1.99 <
  2.89 survives; doubled spread flips — margin < 2x, now stated
  in-script.
- The verdict-logic attack SUCCEEDED: the record tolerance exists
  (S115 ~30 ell, S116 mean 42) and the script's no-tolerance claim
  was factually wrong; the strict-rules verdict is INDISTINGUISHABLE,
  which the same-day amendment implements.
- Structural suppression verified with kernel-mass ratios (1.3e-5 vs
  1.4e-3 interior to 5 Gpc).

## Next targets

1. **Tier-D coefficient derivation** — the queue's other half (the
   transfer-ladder functional against the six wall numbers);
   micro-sector, sand-free per the contamination map.
2. **The banked differential prediction** (consequence 2) awaits any
   future few-ell Planck EE comb-position analysis.
3. **Ensembles parked** per STATE (the orchestra route; genuinely new
   machinery).
