# G141 audit report — endpoint calibration comparison has an algebraic ordered inverse

Date: 2026-08-17

Current grade: `VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS`

## Result first

On a supplied compatible regular calibrated endpoint family with one shared two-dimensional pair
carrier, the constructed calibration sign and inverse require no new field or preferred frame.
Each complete pair metric has a unique positive triangular clock/ruler calibration `R_i` in the
supplied basis. The relative calibration comparison is

\[
C_{BA}=R_BR_A^{-1}.
\]

It composes and reverses. Its reciprocal grading gives

\[
\delta_{AB}
=\tfrac12\log[(C_{BA})_{11}/(C_{BA})_{00}]
=\Phi_B-\Phi_A.
\]

The A-normalized relative metric `C_BA^T eta C_BA=R_A^-T h_B R_A^-1` has exactly
`phi_pair=delta_AB`. Thus order is supplied by target-minus-source endpoint calibration, not by
reversing an unoriented strip. Reciprocal ratios multiply, bounded positions Mobius-compose, and no
preferred potential origin is required.

## What changed

G140 remains correct: arbitrary full pair pullbacks do not automatically form one positional
network. G141 shows what an admitted network must be built from. Pair depths are not independent
edge magnitudes; they are differences of endpoint reciprocal states on one carried calibration
family. That construction makes cycle closure automatic.

The full orchestra is retained. It first forms every endpoint `h_i`; only then are `T_i,L_i,beta_i`
and the transition read. Exact removal controls show sensitivity to base shift, screen shear, mixing,
and angular endpoint embedding. The witness tests independent endpoint states, not a realized
common-event transition.

## Type boundary

Both `R_B R_A^-1` and the metric-matching map `R_B^-1 R_A` assume a shared pair-coordinate carrier.
They share the relevant inverse diagonal grading but generally not their full shift entry. Neither
is identified with G123's full four-dimensional chart map; that would require supplied endpoint
immersions and their derivatives.

The positive triangular factor is unique only in the supplied ordered calibrated pair basis.
Independent endpoint gauge changes alter `Phi_B-Phi_A`; matched calibration carry is load-bearing.
The current endpoint planes are pairwise distinct, so the finite witness cannot certify a physical
ambient transition. Its relative metric is constructed on the supplied carrier, not shown to be a
new complete physical pullback.

This result closes only the algebraic sign/inverse of the constructed calibration comparison after
a compatible endpoint family and calibration carry are supplied. Identification with the physical
observer-pair inverse/query remains `OPEN`. It does not derive the shared carrier, select that
family, or select the complete metric history.

## Evidence

- preregistered and pushed at `9b6003c2` before execution;
- exact production checks: 65/65;
- independent stdlib/Fraction replay: 40/40 (transition reconstruction numerical; rational metric,
  rank, sensitivity, and source checks exact);
- source hashes: 8/8;
- fresh adversarial review: `REPAIR_REQUIRED`;
- repair-only follow-up: `FOLLOWUP_PASS`.

## Bounded landing

```text
REGULAR_CALIBRATED_ENDPOINT_PAIR_METRICS_DERIVE_POSITIVE_TRIANGULAR_FACTORS__
SHARED_CARRIER_CALIBRATION_COMPARISONS_COMPOSE_AND_REVERSE__
RECIPROCAL_GRADING_EQUALS_TARGET_MINUS_SOURCE_ENDPOINT_PHI__
A_NORMALIZED_RELATIVE_TERMINAL_READOUT_EQUALS_ORDERED_PAIR_DEPTH__
ORDER_SUPPLIES_SIGN_WITHOUT_A_PREFERRED_ROOT__
COMPLETE_ORCHESTRA_REMAINS_UPSTREAM__
SHARED_CARRIER_FULL_CHART_PHYSICAL_FAMILY_HISTORY_XMAX_AND_GLOBAL_COMPLETION_OPEN
PHYSICAL_INVERSE_QUERY_IDENTIFICATION_OPEN
```
