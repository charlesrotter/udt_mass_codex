# G277 zero-context repair verification

Date: 2026-08-26

Verdict: `ACCEPT`

The repair-only reviewer verified:

1. R3 classifier fact vectors are derived from hashed source semantics and computed covariance and
   exact ranks. The expected-class table is a post-derivation assertion, not a classifier input.
2. R4 contains eleven controls that separately reach all nine registered criteria, including
   `source_owned`, `populated_boundary`, and `global_completion`; the package verifier enforces
   criterion coverage.
3. R5 reporting accurately describes the repairs and retains the conditional scope.
4. All 18 source hashes and registered no-write replays pass without changing the six durable
   artifacts.

The scientific landing is unchanged: the Pantheon+ Cepheid-host route is conditional rather than a
native G276 clock anchor; noncalibrator Pantheon+, DES, and their relative combination do not set an
absolute scale; `cmb_temp` remains untyped for scale; and no fit, numerical scale, history, kernel,
operational distance, or `X_max` was selected.

The reviewer made no file changes.
