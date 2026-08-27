# G277 repair preregistration

Date: 2026-08-26

Trigger: fresh zero-context hostile review returned `VERIFIED-WITH-CAVEATS` and retained all four
bounded scientific conclusions while identifying five evidence defects.

## Frozen repairs

### R1 — seal the decisive primary sources

Add exact, hashed local copies of:

1. the official Pantheon+ `4_DISTANCES_AND_COVAR/README`;
2. the official `Pantheon+SH0ES_cosmosis_likelihood.py`.

The production and independent routes must verify their hashes and exact load-bearing statements:

- `CEPH_DIST` is the Cepheid-calculated absolute host distance;
- `IS_CALIBRATOR` identifies a host with an associated Cepheid distance;
- the full covariance includes Cepheid-host covariance;
- calibrator rows use Cepheid-host distances as the theory and thereby calibrate the SNe absolute
  magnitude.

### R2 — audit the actual covariance-weighted design

On the official likelihood row mask `(zHD > 0.01) OR IS_CALIBRATOR`, load the actual released
covariance and actual row types. Require:

1. exact dimension and finite entries;
2. maximum symmetry defect no larger than `1e-12` in absolute matrix units;
3. positive-definite Cholesky factorization;
4. actual unweighted design rank `2` for columns `[log_scale, shared_absolute_magnitude]` with
   calibrator rows `[0,1]` and flow rows `[1,1]`;
5. actual covariance-weighted Fisher rank `2`, with smallest-to-largest eigenvalue ratio greater
   than `1e-12`.

These checks certify only conditional structural identifiability inside the declared shared-SNe-
standardization model. They do not validate the transfer law or fit a scale.

### R3 — remove hardcoded independent classifications

The independent verifier must parse both sealed primary sources, the complete G79 type and thermal
ledgers, and the actual covariance. It must derive each classification from an explicit ownership
predicate rather than writing the expected class directly.

Use an implementation-distinct numerical route: production may use eigendecomposition of the
covariance-weighted Fisher matrix; independent verification must use Cholesky-whitened column
independence and a direct `2 x 2` determinant/condition check.

### R4 — replace vacuous hostile controls

Every hostile control must pass through a nontrivial typed acceptance predicate. Remove:

- unconditional `True` returns;
- phrase-anywhere checks;
- absence of a literal column name as a semantic proof.

Require eight explicit rejected overclaims, each failing a named criterion: independence,
nonzero weight, zero-point closure, same-object type, source ownership, dimensional type, populated
boundary, or global completion.

### R5 — regrade evidence language

The audit report must say `actual covariance-weighted design` only after R2 passes. External-source
semantics must cite the sealed sources. Hostile controls must be called overclaim controls unless a
genuine code mutation is actually applied.

## No-change contract

Repairs may not:

- inspect fit residuals or calculate a numerical scale;
- alter the candidate list or acceptance classes;
- change the metric, kernel, W5, transfer status, history, or `X_max` status;
- import `H0=70` as a UDT anchor;
- touch protected work.

## Acceptance

R1--R5 pass only if all source hashes, actual-design checks, implementation-distinct verification,
eight nonvacuous overclaim controls, no-write replay, premise verification, and repository purity
tests pass with the original bounded landing unchanged.
