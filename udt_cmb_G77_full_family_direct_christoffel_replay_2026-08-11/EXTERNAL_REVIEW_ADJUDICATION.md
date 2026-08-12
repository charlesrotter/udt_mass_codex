# G77 external-review adjudication

Date: 2026-08-11

External landing:

`VERIFIED_FULL_FAMILY_DIRECT_REPLAY__FOUR_G76_EXCEPTIONS_RESOLVED_IN_G77`

Correction list: `none`.

This additions-only layer accepts the cold review of the exact 41-file sealed intake. The
preregistered G77 calculation, raw arrays, provisional report, and immutable G75/G76 sources remain
unchanged historical evidence.

## What survived

The reviewer verified all `40/40` manifest-listed hashes before interpretation and independently
reproduced:

- the metric derivatives and contracted/full-Christoffel equivalence, with maximum acceleration
  difference `2.220446049250313e-15`;
- the live variable-`q_s` contribution: deleting it creates derivative error
  `2.6135152423045462`, while the complete analytic derivative agrees with finite differences to
  `8.78730865849775e-10`;
- the observer tetrad and null initial-direction map to `3.3306690738754696e-16` and
  `7.216449660063518e-16`, respectively;
- all `591` completed profiles, `1,514,142` crossed rays, and `3,025,920` face maps;
- `590 STRONG_DIRECT_AGREEMENT`, one `REGISTERED_DIRECT_AGREEMENT`, and zero unresolved rows;
- the sole registered row `G75_AM_S03_E100` at `2.0269360962840678e-05`;
- zero nonfinite/active rays, negative signed faces, negative projected orientations, or
  near-`1e-2` faces;
- all four higher-resolution G77 ladders, with zero crossing mismatch and approximately fourth-order
  convergence;
- the independent DOP853/full-Christoffel panel across all eight strata and every historical G76
  exception, with maximum endpoint chord `4.7046525883627355e-06` and null error
  `1.5370622830079839e-10`;
- all `8/8` hostile mutations.

The reviewer did not rerun the full 591-profile production integration. It instead verified its
sealed raw outputs completely and reran the independent representative panel. That is an explicitly
retained testing limitation, not a failing gate.

## Historical semantics

G76 remains immutable and correctly records four rows as unresolved under its frozen `512/1024`
time-step gate. G77 is a later, independent direct-Christoffel calculation whose `1024/2048/4096`
ladder resolves those same four identities. It does not rewrite the G76 result.

## Four evidence gates

1. Preregistered: **yes**, commit `0d376014`, pushed before implementation or trajectory output.
2. Full or bounded scope: **complete for all 591 rows and every level-4 direction of the frozen G75
   family**, bounded to one supplied stationary axial observer query.
3. Independently verified: **yes**, through complete raw reconstruction, a materially different
   SciPy/DOP853 finite-difference-Christoffel panel, and the sealed GPT-5.4 adversarial review.
4. Premises audited: **yes for this bounded numerical claim**; every physical owner remains open.

## Maximum justified conclusion

G77 verifies that the complete sampled G76 whole-sky endpoint family is not an artifact of its
Hamiltonian implementation. A direct metric-Christoffel route reproduces the frozen endpoint maps,
degree, orientation, and no-fold/no-hole census across the complete 591-profile sampled family, and
its higher direct time ladder resolves the four numerical exceptions retained by G76.

This remains a finite-mesh result for a supplied stationary axial family and observer query. It does
not establish continuum injectivity; select a physical profile, source, endpoint, scale, `R`, or
`X_max`; or derive polarization, bootstrap, action, matter, or a CMB observable.

