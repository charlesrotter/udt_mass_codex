# Audit report — complete reciprocal-representation extension census

Date: 2026-08-16  
Status: `VERIFIED_WITH_CAVEATS__REVIEWER_REPAIR_AND_CORRECTED_FOLLOWUP_VERIFIED`

## Landing

```text
CONSTANT_EXTENSION_CENSUS_COMPLETE
__BASE_ONLY_GATES_LEAVE_ONE_ACTIVE_SCREEN_DILATION_PARAMETER
__FULL_DETERMINANT_PAIRING_OR_EXTENDED_EXCHANGE_REMOVES_IT
__ORIENTED_SCREEN_ROTATION_IS_ZERO_ORDER_GAUGE
__NO_PHYSICAL_SCORE_SELECTED_BECAUSE_ACTIVE_EJ_CARRY_IS_UNOWNED
```

For a supplied pair-relative base/screen split, every structureless constant screen-covariant lift
of the founded reciprocal generator is

\[
H_{a,b}=\operatorname{diag}(-1,+1)\oplus(aI_2+b\epsilon).
\]

Full `O(2)` removes `b`. Base-only founded gates leave `a` free. Complete determinant one, a tested
complete direct-sum pairing, or either tested extension of exchange oddness removes `a`; oriented
screen reflection exchange may retain `b`, but `b` is invisible to the zero-order pair metric.

The nonzero `a` direction changes terminal pair geometry only after choosing an active placement
on `E` without a compensating `J` carry. The current foundation does not own that choice. The census
therefore narrows the possible score but does not derive one.

## Evidence

- `derive_representation_census.py`: exact symbolic centralizers, gates, finite family, and rational
  active/passive witness.
- `verify_representation_census_independent.py`: separate direct-matrix exponentials, group checks,
  active/passive replay, and four hostile mutations.
- Production exact source: `CENSUS_RESULT.json`.
- Independent numerical source: `INDEPENDENT_VERIFICATION.json`.
- Class and placement ledgers: `REPRESENTATION_CLASS_ATLAS.tsv` and `ACTIVE_PASSIVE_ATLAS.tsv`.

Independent maximum group residual is `2.7755575615628914e-16`; correct passive carry and screen
rotation metric residuals are exactly `0.0`. Hostile off-block, anisotropic-screen, omitted-`J`,
reflection, pairing, and exchange mutations all produce nonzero residuals.

The fresh external reviewer independently recovered the same bounded class and found no
active/passive type error. It did find one non-outcome-changing proof-script defect: the off-block
infinitesimal equations had been mistyped as eigenvalue-one equations. The code now uses
`epsilon C=0` and `A epsilon=0`, includes a finite-to-infinitesimal regression that rejects the old
mutant, and tests passive cancellation with a general nonidentity coframe. All corrected replays
pass. See `EXTERNAL_REVIEW_RAW.md` and `EXTERNAL_REVIEW_ADJUDICATION.md`.

## Evidence gates

1. Preregistered: yes, in the banked 2026-08-15 whiteboard package.
2. Full space: complete only for constant zero-order `O(2)`/`SO(2)`-covariant generators on a
   supplied regular pair split.
3. Independent verification: separate implementation and hostile mutations pass; the fresh blind
   review returned `VERIFIED_WITH_CAVEATS`; its bounded repairs were implemented and the corrected
   follow-up returned `REPAIRS_VERIFIED__ORIGINAL_LANDING_STANDS`.
4. Premise audit: internal ledger complete; repository premise verifier must pass after any registry
   update.

## Maximum conclusion

This is a complete bounded representation classification and a conditional active candidate
family. It is not a physical history, dynamics, regime score, angular sky map, observational fit,
bootstrap law, `X_max`, source, matter, action, or signalling result.
