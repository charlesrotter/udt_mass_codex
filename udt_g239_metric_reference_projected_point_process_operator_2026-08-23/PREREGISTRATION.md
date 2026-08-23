# G239 preregistration — metric/reference-projected point-process operator

Date: 2026-08-23

Status: `PREREGISTERED_BEFORE_OPERATOR_DERIVATION__BOSS_OUTCOMES_CLOSED`

## Whole question

For one **supplied** continuous complete metric history, one supplied observer-sky query, and one
explicit featureless source-population hypothesis, derive the exact expectation of the frozen
observer-coordinate Landy--Szalay readout after the metric clock/screen map and the survey random
reference have both acted.

The bounded discriminator is:

> Can a metric-generated, angle-dependent observation Jacobian leave a nonzero reference-projected
> two-point pattern even when the source process is homogeneous Poisson, and exactly when must that
> pattern vanish?

This is an operator derivation. It does not inspect a BOSS curve or select a metric history.

## Exact frame

- **Whole frame:** one observer, one observed-redshift shell, the full observer sky or a declared
  survey window, and all supplied regular null branches reaching that shell.
- **Metric-led:** the supplied complete metric and null query determine clock and screen/Jacobi
  maps before any catalogue readout.
- **Borrowed readout:** normalized Landy--Szalay pair counting is an observational estimator, not
  UDT dynamics.
- **Source premise:** homogeneous Poisson emission/source events are a
  `CHOSE_OBSERVATIONAL_HYPOTHESIS` used only as a featureless control.
- **Reference premise:** the official random catalogue represents the released survey footprint
  and completeness. It is not promoted to a physical source law or a metric-transformed source
  reference.

## Typed objects

Let `S` be the supplied source-event domain and `O` the observer-coordinate shell. A branch-labelled
metric observation relation consists of maps `Psi_b:S_b->O` and nonnegative supplied branch weights.
Its pushforward one-point measure is `nu_1`. The source factorial pair measure is `mu_2`; its
branchwise pushforward is `nu_2`. The normalized survey reference is `Q`. For each angular bin the
frozen estimator supplies a symmetric nonnegative pair kernel `K`.

For the featureless control, source events are Poisson and branch population is required to
factorize, so the observed factorial pair measure is `nu_2=nu_1 tensor nu_1`. This implication must
be proved rather than assumed.

## Preregistered exact identities

Writing `P=nu_1/nu_1(O)` and using normalized pair measures, the candidate identity is

```text
w_K = [<K,PxP> - 2<K,PxQ> + <K,QxQ>] / <K,QxQ>
    = <K,(P-Q)x(P-Q)> / <K,QxQ>.
```

If `P` is absolutely continuous with respect to `Q`, with normalized density `f=dP/dQ`, the
candidate equivalent form is

```text
w_K = integral K(o1,o2)[f(o1)-1][f(o2)-1] dQ(o1)dQ(o2)
      / integral K(o1,o2)dQ(o1)dQ(o2).
```

These formulas are preregistered targets, not yet results.

## Gates

1. **Exact estimator algebra:** independently recover the quadratic mismatch identity with exact
   arithmetic and catch the sign/normalization mutations.
2. **Pushforward typing:** derive the observed one- and two-point measures from the supplied
   branch-labelled metric relation; do not call a Jacobi matrix a populated measure.
3. **Poisson/factorization gate:** prove that an independently mapped Poisson source remains
   factorized. Any connected observed-pair term must be separately displayed.
4. **Reference cancellation:** prove `w_K=0` when `P=Q`; prove that an angularly constant radial
   multiplier cancels after normalization.
5. **Metric-response survival:** exhibit one exact positive nonconstant response and one angular
   bin kernel with nonzero `w_K`, without using any observational outcome.
6. **General connected decomposition:** if `nu_2` contains a connected remainder, separate it from
   the one-point/reference mismatch term.
7. **No outcome leakage:** reject BOSS values, feature locations, covariance arrays, P1, `X_max`,
   Lambda-CDM distances, fitted coefficients, post-readout orchestra terms, and protected inputs.

## Preregistered landings

- `REFERENCE_PROJECTED_METRIC_INTENSITY_OPERATOR_DERIVED_CONDITIONALLY`
- `IDEAL_MATCHED_REFERENCE_CANCELS_ALL_FACTORIZED_METRIC_RESPONSE`
- `NONFACTORIZING_PAIR_OR_BRANCH_STRUCTURE_REQUIRED`
- `TYPE_OR_ALGEBRA_FAILURE__NO_FORWARD_OPERATOR`

The first landing requires an exact nonzero witness when the fixed survey reference differs from
the metric-pushed intensity. The second applies if every lawful reference is forced to equal the
metric-pushed one-point measure. The third applies if factorized response cancels for the actual
reference semantics. More than one qualified theorem may hold on different declared reference
types.

## Omitted/open scope

- selection or valuation of the continuous physical metric history;
- ownership of observer/source incidence or null-branch population;
- a UDT source, matter, emission, radiative-transfer, or galaxy-formation law;
- caustic multiplicity beyond supplied finite branch sums;
- finite-catalogue bias and covariance beyond the frozen borrowed estimator;
- all BOSS outcome values and all feature/scale interpretations;
- `X_max`, action, bootstrap, mass, signalling, CMB, and cosmological prediction.

## Certification contract

- Use exact rational finite-dimensional witnesses and an independent implementation.
- Verify every source hash and save machine-readable results.
- Include hostile mutations for sign, normalization, constant response, matched-reference
  cancellation, connected-term omission, source-law promotion, outcome opening, and inserted
  feature/scale.
- Run `python3 verify_current_scientific_premises.py` before banking any verdict.
- Maximum claim: a conditional reference-projected point-process evaluator and its exact
  cancellation/survival criteria. No UDT validation or BOSS prediction follows.

