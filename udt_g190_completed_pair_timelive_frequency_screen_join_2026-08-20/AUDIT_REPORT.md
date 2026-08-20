# G190 audit report

Date: 2026-08-20

## Current landing

```text
COMPLETED_PAIR_NULL_GERM_AND_TIMELIVE_FREQUENCY_SCREEN_JOINT_EVALUATOR_DERIVED_CONDITIONALLY
__DA_OF_Z_DESCENDS_ONLY_ON_MONOTONE_NONCAUSTIC_BRANCHES
__STATIC_G189_AND_LOCAL_G116_ARE_POST_RESULT_SPECIALIZATIONS
```

Final status:

```text
EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS
```

## What is new

The completed pair pullback gives an orthonormal clock/ruler frame and therefore two normalized
null directions. One ruler orientation selects the local outgoing germ. The same complete metric
then owns affine ray propagation, endpoint frequency contraction, quotient-screen curvature, and
the finite Jacobi map.

This replaces the need for a separately supplied `R(Z)` inside a time-live evaluation: the native
result is the parametric branch `lambda -> (Z,D)`. A single-valued `d_A(Z)` is a derived local
descent only when frequency is one-to-one and the screen is noncaustic.

## Gates passed

- preregistration before confirmatory implementation;
- exact symbolic pair-frame, geodesic, frequency, curvature, and Jacobi reconstruction;
- exact time-live witness;
- implementation-distinct 20,000-frame and 256-branch replay with 161,024 assertions;
- 15 hostile mutation/semantic catches;
- static G189 and local G116 post-result regressions;
- 10 immutable source hashes;
- 174-row current-premise verifier;
- 130 repository tests passed with one pre-existing expected failure;
- Python compilation and `git diff --check` passed.
- sealed `--no-write` replay passed with byte-identical intake tree before and after execution.

## Scope boundary

The theorem does not choose a complete metric history, observer population, later endpoint
intersection, or global branch. It does not derive emission, transfer, flux, luminosity, source
standardization, observations, `X_max`, action, dynamics, matter, mass, bootstrap, or signalling.
The G116 coefficient decomposition is not part of the derivation.

## External review

Fresh sealed `gpt-5.4` review returned `G190_ACCEPTED_WITH_STATED_BOUNDS`. It retained every
requested scientific and ownership claim, reran the no-write package successfully, and found no
repair item. The review's residual ceiling is only that it did not claim an exhaustive semantic
reread of all ten frozen upstream sources.
