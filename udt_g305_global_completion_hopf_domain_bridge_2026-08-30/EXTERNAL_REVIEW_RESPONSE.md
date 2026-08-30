# Fresh external G305 adversarial response

The following is a faithful condensed record of the response. The exact returned file and full
transcript are identified by SHA-256 in `EXTERNAL_REVIEW_TRANSMISSION.md`.

## Findings

`REPAIRABLE_DEFECTS`

- The sealed package's own verifier is not replayable as delivered. `verify_package.py` resolves
  source hashes relative to the package parent and checks `REPO / row["path"]`, but the frozen-source
  rows in `SOURCE_SCOPE.tsv` omit the `frozen_sources/` prefix that the sealed intake actually uses.
  In an ephemeral `/work` copy, `verify_package.py` failed immediately on the first missing source
  path.
- The registered independent verification does not satisfy the preregistered independent-check
  scope. It does not independently check the positive overlap identities, omits any negative global
  pullback replay, and hardcodes the topology semantics.
- The hostile-control script is non-adversarial. It asserts a hardcoded all-false dictionary against
  itself and therefore cannot falsify an overclaim.

## Bounded scientific review

No geometry-level contradiction appeared in the core bounded claim. Manually re-deriving the
intake's equations reproduces the positive static pullback, regular global de Sitter pullback, and
overlap

`r = X cosh(T/X) sin(psi)` and `tanh(tau/X) = tanh(T/X)/cos(psi)`.

On that completion, `r=X` is a regular observer horizon rather than a material boundary, and
constant-`T` slices are intrinsic compact `S3`. The negative completion gives `H3` spatial slices
on the chosen causal universal cover, hence noncompact `R3`-type topology, and the zero sector is
flat `R3`. The explicit Hopf witness has unit norm and normalized integral `-1` in the frozen
orientation, with sign reversal under orientation flip only; the class is scale-blind and
slice-kinematically persistent on the explicit `R x S3` slicing. The null optical contraction is
zero for all signs and the full-sky Euler number is `2` for all signs, so those do not add a sign or
magnitude selector.

What is established is only the domain-side availability result. The package correctly leaves
physical map ownership, fixed physical target, frame-gauge-independent physical Hopf charge,
action, dynamics, stability, history selection, magnitude, mass, and physical `X_max` open. On the
G289 question, the needed physical frame/target independence is still not supplied.

## Checks run

- `verify_global_hopf_bridge_independent.py` passed: 459 checks, 18 finite-difference cases, maximum
  metric error `3.5904363926420046e-09`, normalized Hopf result `-1.0000000010280863`.
- `run_global_hopf_catches.py` returned `PASS 10/10`, but that result is not probative for the reason
  above.
- `verify_package.py` failed on source-path resolution.
- The production SymPy derivation was not rerun because SymPy was not sealed and review was limited
  to registered standard-library checks.

On the mandatory questions: `r=X` is proved as a regular observer horizon; intrinsic `S3` removes
the old compactification-boundary premise only for the positive standard completion; the metric
makes nontrivial classes available but does not select a physical `S3 -> S2` map; the Hopf integer
is not shown to have the physical frame/target independence G289 would need; zero and negative
sectors recover the same class only by extra asymptotic or quotient data; no result fixes the
positive magnitude or selects a history; and the positive-sign agreement with G17 is consilience
within the same positive geometry, not an independent selector.
