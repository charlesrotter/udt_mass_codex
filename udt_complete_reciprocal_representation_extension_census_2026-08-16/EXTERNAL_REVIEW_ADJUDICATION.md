# External review adjudication

Date: 2026-08-16  
Review landing: `VERIFIED_WITH_CAVEATS`  
Current status: `REPAIRS_VERIFIED__ORIGINAL_LANDING_STANDS`

## Accepted findings

The reviewer independently reconstructed the bounded classification:

- `SO(2)` leaves `H_b direct_sum (a I_2+b epsilon)`;
- `O(2)` removes `b`;
- no constant off-block intertwiner or screen shear survives the declared covariance;
- complete determinant, the tested complete pairing, and both registered exchange lifts remove
  `a`;
- `b` cancels from the zero-order pair metric;
- a chosen active left action with fixed `J` can make `a` observable, while exact passive or
  compensated carry removes it.

The reviewer found no hidden active/passive type error and accepted the package's bounded ownership
language and conditional Jacobi/Riccati next step.

## Accepted defect

The production script had encoded the off-block infinitesimal covariance equations as

```text
(epsilon-I) C=0,
A (epsilon-I)=0,
```

rather than the correct equations

```text
epsilon C=0,
A epsilon=0.
```

Both systems happen to have only the zero solution for the real two-dimensional screen, so the
reported class was unchanged. The proof implementation was nevertheless wrong and required repair.

## Implemented repairs

1. `derive_representation_census.py` now solves the correct infinitesimal equations.
2. Its exact JSON records the equations and proves the old eigenvalue-one mutation is a distinct
   map.
3. `verify_representation_census_independent.py` finite-differences the full screen action and
   checks that it differentiates to `epsilon C` and `-A epsilon`.
4. The independent verifier explicitly rejects the old eigenvalue-one mutation.
5. Passive cancellation is now tested with a general nonidentity complete coframe, not only
   `E=I`.
6. Production, independent, source-manifest, and package replays pass after regeneration.

## Adjudicated conclusion

The external criticism changes the evidentiary implementation, not the mathematical landing. The
maximum justified statement remains a complete classification only within the constant zero-order
`O(2)`/`SO(2)`-screen-covariant class on a supplied regular pair split. It does not select the
physical orchestra score or authorize fitting `a`.

## Corrected follow-up

The first follow-up invocation looked for the root `REVIEW_SCOPE.json` inside the package directory
and stopped without inspecting the repairs. The sealed intake itself was intact. A fresh retry on
the same authorized intake was explicitly directed to the root scope file, verified all 25 listed
payload hashes, replayed the package, and returned:

```text
REPAIRS_VERIFIED__ORIGINAL_LANDING_STANDS
```

See `EXTERNAL_FOLLOWUP_REVIEW_RAW.md`. The procedural first stop is not treated as a scientific
negative because it evaluated no repair.
