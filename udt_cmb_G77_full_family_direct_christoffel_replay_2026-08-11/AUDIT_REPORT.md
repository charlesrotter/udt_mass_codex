# G77 audit report — full-family direct-Christoffel replay

Date: 2026-08-11

Status: `PROVISIONAL_AWAITING_FRESH_ADVERSARIAL_REVIEW`

## Provisional landing

```text
FULL_FAMILY_DIRECT_REPLAY_AGREES
FOUR_ROWS_DIRECTLY_REFINED__G76_HISTORY_UNCHANGED
```

All `591/591` frozen G75 profiles and `1,514,142` level-4 rays were recomputed from the metric by a
direct-Christoffel route independent of the G76 Hamiltonian implementation. There are `590` strict
agreement rows, one registered agreement row, and zero cross-method unresolved rows. All four rows
that G76 retained as unresolved are numerically resolved by G77's higher direct time ladder.

## What was learned

The complete sampled whole-sky relation family is not an artifact of the G76 Hamiltonian code.
Direct metric geodesics reproduce the same endpoint maps, degree, orientation, and no-fold/no-hole
census across the entire frozen family. The earlier four-row caveat was ordinary time resolution
within the frozen G76 calculation, not evidence of a distinct geometric branch or pathology.

## Verification gates before external review

1. **Preregistered:** yes; commit `0d376014`, pushed before implementation or trajectory output.
2. **Full or bounded scope:** full `591/591` frozen family and full level-4 direction mesh; bounded
   to the supplied stationary axial metric and one observer/query.
3. **Independent load-bearing verification:** complete raw-artifact reconstruction plus an
   independent SciPy/DOP853 finite-difference-Christoffel panel spanning all eight strata and four
   former exceptions pass. Fresh external review remains pending.
4. **Premise audit:** complete in `PREMISE_LEDGER.tsv` and `COMPLETENESS_MAP.md`; no physical owner
   or observational selection is promoted.

## Decisive numbers

- direct profiles: `591`;
- direct rays: `1,514,142`;
- direct faces: `3,025,920`;
- classes: `590 STRONG_DIRECT_AGREEMENT`, `1 REGISTERED_DIRECT_AGREEMENT`;
- maximum direct/G76 endpoint chord: `2.0269360962840678e-05`;
- maximum null backward error: `2.85631585050794e-09`;
- maximum degree difference: `3.3306690738754696e-16`;
- negative signed faces: `0`;
- negative projected tangent maps: `0`;
- near-`1e-2` faces: `0`;
- former G76 unresolved rows refined by G77: `4/4`;
- independent SciPy-panel maximum chord: `4.7046525883627355e-06`;
- hostile catches: `8/8`.

## Limits

The direct replay is not a proof over all smooth profiles, all observer queries, the continuum
direction sphere, time-live complete metrics, generic ten-component coframes, physical CMB
sources, or observational spectra. It does not select any profile or turn a geometric relation map
into TT/TE/EE/BB data.

## Next gate

Transmit the sealed package to a fresh adversarial reviewer. Only after it independently checks the
metric-to-Christoffel route, raw array census, refinement semantics, and premise scope may G77 be
banked above provisional status.
