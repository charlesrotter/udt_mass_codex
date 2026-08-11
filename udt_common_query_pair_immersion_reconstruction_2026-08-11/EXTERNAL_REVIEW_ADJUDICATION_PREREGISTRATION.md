# External-review adjudication preregistration

Date: 2026-08-11

Parent package commit: `7cce1745`

External review SHA-256:

```text
15be3d0aeed9a8e24cf4e54bdd0ad0c1aa3bce6b31856cbbc52f9b6e4d91c33a
```

External verdict: `VERIFIED_WITH_CAVEATS`.

## Findings accepted before calculation

1. Q2 Codazzi remains `NUMERICALLY_UNRESOLVED`; the existing independent verifier did not test it.
2. The existing independent verifier independently reconstructs the metrics, surfaces, Gauss terms,
   Jacobi balance, and curvature generators, but it reads the production loop norms. Its loop check
   is therefore only partially independent.
3. The provisional primary and secondary landings survive subject to those two explicit evidence
   limits.

The sealed `REVIEW_MANIFEST.tsv`, the transmitted intake, prior production returns, preregistrations,
and all previous verifier outputs are immutable historical evidence. They will not be rewritten.

## Frozen correction question

Can a fresh implementation, importing neither production nor prior verifier code and reading no
production loop rows:

1. resolve the Q2 Codazzi identity on the same `TL_P2` Fermi immersion using higher-order finite
   differences and a separately implemented integration path; and
2. regenerate the smallest Q2 normal loop and recover its curvature-generator limit without the
   production `orthogonal_polar` transport?

## Frozen geometry and scope

- Query: exactly `Q2_TL_FERMI` from the original preregistration.
- Metric witness, field formulas, initial point, initial inverse-coframe clock/ruler, and local tile:
  unchanged.
- No Q1 recomputation is required except any exact algebra control needed to type-check the script.
- CPU only. No action, source, matter, bootstrap, selector, CMB, signalling, or physical-regime claim.

## Independent numerical method

- New standalone script; no import from `solve_common_query.py` or
  `verify_common_query_independent.py`.
- Duplicate the frozen time-live coframe formula explicitly.
- Construct the observer/ruler and Fermi surface with a separately written fixed-step classical RK4
  integrator using step at most `1.25e-4`.
- Use centered five-point first derivatives for the higher-jet Codazzi calculation.
- Test outer query-coordinate scales, in this fixed order:
  `0.008`, `0.004`, `0.002`, `0.001`.
- Use metric derivative step `1e-5` and ambient-curvature derivative step `5e-4`, with a second
  curvature control at `2.5e-4`.
- Regenerate the Q2 normal loop at half-width `0.01` using its independently reconstructed normal
  connection and fixed path subdivisions `16`, `32`, and `64`; no polar projection is allowed.
- Report raw matrices, norms, scale sequences, loop quadrature differences, and source versions.

## Frozen classifications

### Q2 Codazzi

- `INDEPENDENTLY_CERTIFIED` only if the final two residuals are both below `5e-6` and either decrease
  by at least `1.5` or agree within a factor of `1.5`, while the curvature-step control changes the
  final residual by less than `2e-6`.
- `IDENTITY_REFUTED_ON_DECLARED_NUMERICS` only if residuals remain above `5e-4` with no convergence
  and the algebra/sign audit independently confirms the implementation.
- otherwise `NUMERICALLY_UNRESOLVED`.

### Independent normal loop

- `INDEPENDENTLY_REGENERATED` only if the `32` to `64` subdivision difference is below `1e-8`, the
  loop return is nonidentity above `1e-7`, the loop/area rate agrees with the independent normal
  curvature norm within `2e-3` relative, and the result is within `2e-3` relative of the frozen
  production normal-loop norm.
- otherwise `NUMERICALLY_UNRESOLVED`; no mechanism or retuning may be introduced.

## Maximum conclusion

At most, this pass may remove one or both numerical caveats from the already bounded two-query
geometric classification. It cannot strengthen the result into a universal query rule, preferred
path, dynamics, action, source, matter, bootstrap, or observational result.

