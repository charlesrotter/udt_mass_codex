# G240 preregistration — metric null-image cluster census

Date: 2026-08-23

## Whole question

For one **supplied** smooth complete Lorentz metric history, observer event/frame, source-incidence
domain, and locally finite regular null relation, does the query “count every regular null image”
remove G239's arbitrary branch-weight freedom? Equivalently: does the metric relation itself induce
the observed one-point intensity and same-parent sibling-pair measure of a Poisson parent process?

This is an observing question. It does not target a BOSS curve, feature, scale, sign, or amplitude.

## Declared regime

- smooth time-oriented Lorentzian four-manifold with a **supplied** complete metric history;
- one supplied observer event and calibrated sky frame;
- one supplied measurable source-parent space and incidence map;
- all regular past-null branches satisfying that incidence query are counted once;
- the branch relation is measurable and locally finite/proper on the tested stratum;
- caustic/critical and infinite-image strata are characterized as omitted/open, not rejected;
- the parent population is a homogeneous or general Poisson control with supplied intensity measure;
- no absorption, selection function, radiative transfer, detector threshold, or source luminosity is
  inserted.

## Metric-led versus template-led

Metric-led geometry: null branches, observed sky directions, branch multiplicity, and regular
Jacobi maps come from the supplied metric/query. Standard point-process counting and factorial
moment identities are used only as mathematical evaluators. The Poisson parent is a declared
control hypothesis, not a UDT derivation.

## Candidate theorem

Let `R_x` be the finite set of regular observed images of parent `x`, and let

```text
C_x = sum_{y in R_x} delta_y
```

be its unit-multiplicity image counting measure. For a Poisson parent process of intensity `mu`,
the candidate identities are

```text
nu_1(A) = integral C_x(A) mu(dx)
nu_2(A x B) = nu_1(A) nu_1(B) + Sigma_sib(A x B)
Sigma_sib(A x B)
  = integral sum_{y,z in R_x; y != z} 1_A(y) 1_B(z) mu(dx).
```

Consequences to test:

1. branch labels and arbitrary branch weights disappear from the all-image query;
2. one image per parent gives `Sigma_sib=0` exactly;
3. positive-measure multi-image parents give positive total ordered sibling mass
   `integral m(x)(m(x)-1) mu(dx)`;
4. G239's normalized remainder remains
   `Gamma_sib=Sigma_sib/(N^2+S)-[S/(N^2+S)] P tensor P`;
5. the construction is covariant under source/sky reparameterization and invariant under branch
   relabeling.

## Premise/choice ledger

- supplied complete metric history: `CONDITIONAL_INPUT`, not selected;
- observer event/frame and source incidence: `CONDITIONAL_QUERY_INPUT`;
- all-regular-image census: `CHOSE_QUERY_PROTOCOL`;
- unit image multiplicity: `DERIVED` from counting once after that query is chosen;
- Poisson parent measure: `CHOSE_CONTROL_HYPOTHESIS`;
- null relation/Jacobi maps: `DERIVED_CONDITIONAL` from the supplied metric/query;
- point-process factorial-moment calculation: `STANDARD_MATHEMATICAL_EVALUATOR`;
- survey reference and BOSS outcomes: absent.

## Omitted sectors and limits

Critical caustics, nonproper/infinite image sets, image coherence, extinction, detector selection,
native transfer, non-Poisson sources, source evolution, source luminosity, a selected physical
history, `X_max`, action, matter, bootstrap, and all observational outcomes remain open. The result
will be one regular all-image-query tile, not a complete cosmology.

## Preregistered verification contract

Before any verdict is banked:

1. derive the measure identities without choosing a sky profile;
2. independently enumerate at least 2,000 exact finite parent/image configurations;
3. verify one-image cancellation, multi-image sibling mass, normalization, branch relabeling, and
   source/sky pushforward covariance;
4. reproduce the exact G239 two-cell `+/-1/12` control;
5. catch at least these hostile mutations: silently select one branch; insert arbitrary branch
   weights; omit siblings; include image self-pairs; normalize by `N^2`; call Poisson a UDT law;
   promote a regular-stratum density through a caustic; open BOSS outcomes; insert P1, `X_max`, a
   fitted coefficient, or a protected payload;
6. run the 222-row premise verifier and the full repository test suite;
7. obtain a fresh read-only adversarial review before live-premise integration.

## Falsification and maximum conclusion

The candidate is refuted if direct finite configuration averaging disagrees with the proposed
factorial-moment identities, if the result depends on branch labels, or if a multi-image parent
cannot be represented without an inserted free weight.

Maximum positive conclusion:

```text
ALL_REGULAR_NULL_IMAGE_QUERY_REMOVES_ARBITRARY_BRANCH_WEIGHTS_CONDITIONALLY
__METRIC_RELATION_INDUCES_IMAGE_INTENSITY_AND_SIBLING_PAIR_MEASURE_ON_A_SUPPLIED_HISTORY
__PHYSICAL_HISTORY_SOURCE_MEASURE_TRANSFER_CRITICAL_STRATA_AND_OBSERVATIONAL_ANCHOR_OPEN
```

No BAO/CMB origin, BOSS prediction, physical source law, history selector, feature scale,
`X_max`, or UDT validation may follow.
