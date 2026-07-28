# Metric-natural joint-selector possibility/no-go audit — preregistration

Date: 2026-07-28

Base commit: `e7ea5936eaecbab626db0f30e12a8be4630b5dd7`

Base tree: `cad25e08302b9e6ed3809b1774d0d82af1848a2a`

Status: `PREREGISTERED_BEFORE_NEW_NO_GO_DERIVATION`

## Whole question

Can a continuous, single-valued, observer-covariant natural construction on the full admitted
class of complete time-oriented Lorentzian metrics/coframes extend the founded reciprocal pair into
all of the following without extra relational or branch data?

1. a physical observer-query/comparison law with nontrivial additive signed depth where the founded
   reciprocal structure is nontrivial;
2. a finite full-frame reciprocal response, including transverse/mixing behavior; and
3. a globally compatible reduction/section with descent and causal-stratum behavior.

If not, what is the exact no-go scope, what conditional reduced-structure routes remain, and what is
the smallest extra datum required at each blocked layer?

This is a metric-led possibility/no-go audit. It is not a search for a desirable universe or a
license to select one branch.

## Input categories kept separate

The audit must not confuse five different domains:

```text
I0: metric/coframe plus orientations only;
I1: I0 plus an observer query (event and unit timelike direction at each endpoint);
I2: I0 plus a supplied observer line/congruence;
I3: I0 plus a supplied ordered observer/ruler pair;
I4: I0 plus supplied path, signed depth, and complete frames.
```

An output cannot be called metric-selected when it was supplied in its input category. A physical
law may act on all observer queries without selecting a preferred observer; the audit must test that
query-valued route separately from preferred-frame selection.

## Preregistered theorem tests

The exact obligations are frozen in `THEOREM_OBLIGATIONS.tsv`. The load-bearing tests are:

- full Lorentz-isotropy: whether a non-scalar reciprocal generator can be natural without a
  reduction of the orthonormal frame bundle;
- observer-query character: whether a continuous additive scalar character of the full connected
  Lorentz comparison group can be nontrivial;
- position-dependent escape: whether an additive base cocycle requires a separately derived scalar
  potential or one-form;
- observer-line reduction: what `SO(3)` equivariance forces when only a timelike line is supplied;
- ordered-pair reduction: what `SO(2)` screen equivariance leaves free when a clock/ruler pair is
  supplied;
- global descent: whether local reductions extend through holonomy, symmetric, null, zero, and
  type-changing strata without supplied completion data.

The stationary Killing-norm hybrid is the positive partial control. The complete arbitrary-real-
`lambda` `R x S3` family, arbitrary endpoint cocycles, symmetry-enhanced Lorentzian controls, and
nontrivial holonomy are the negative controls.

## Premise ledger

- founded reciprocal pair and additive one-dimensional character: `pinned-by-THEORY`;
- observer covariance/no preferred macro frame: `pinned-by-THEORY`;
- complete Lorentzian metric/coframe class: `free-and-explored`;
- actual observer queries: `free-and-explored` in I1, not silently selected;
- observer line, ruler line, path, depth, `lambda`, screen isotropy, trace, completion, and interface:
  `free-and-explored` or explicitly supplied in their named input category;
- stationarity and `R x S3`: `pinned-by-HABIT` nowhere; they are bounded controls only;
- strong local CSN: inactive and unavailable as a selector;
- `c_E` and `G_obs`: observed anchors, not representation selectors;
- co-presence and bootstrap: working interpretations, not equations;
- action, source, carrier, matter, density, boundary functional, `Xmax`, dynamics, and observations:
  excluded.

## Falsification and certification

A universal no-go is certified only if an admitted symmetry control blocks at least one required
output for every single-valued continuous natural construction in the stated category. A
conditional construction survives only with every additional datum named.

The result must fail closed if it:

- mistakes “no preferred observer” for “no law on observer queries”;
- assumes a scalar depth must be a character of the full Lorentz group when it also depends on base
  position, without testing that separate cocycle route;
- treats the trivial scalar character as a nontrivial UDT depth;
- calls a supplied observer line, ruler, path, potential, or coframe metric-derived;
- uses full Lorentz commutant results after a structure-group reduction without recomputing the
  reduced commutant;
- promotes the conditional `lambda=+1`, `lambda=-1`, or arbitrary-`lambda` strata to universal;
- equates local selection with global descent;
- uses an action, field equation, bootstrap, matter, density, or desired phenomenology to repair a
  kinematic obstruction.

Production and independent implementations must separately reconstruct all commutant ranks,
derived-algebra/character results, reduced stabilizer families, and counterexamples. Every catch in
`FALSIFICATION_CONTRACT.tsv` must be exercised.

## Outcome classes and maximum conclusion

Exactly one primary outcome is allowed:

- `UNIVERSAL_METRIC_NATURAL_JOINT_SELECTOR_DERIVED`;
- `UNIVERSAL_SINGLE_VALUED_METRIC_NATURAL_JOINT_SELECTOR_NO_GO_ON_FULL_CLASS`;
- `CONDITIONAL_REDUCED_STRUCTURE_SELECTOR_FAMILY_ONLY`;
- `NO_GO_PREMISES_INSUFFICIENT_STOP`; or
- `FOUNDATIONAL_CONFLICT_STOP`.

The maximum conclusion is a kinematic existence/no-go theorem on the stated category plus exact
conditional escape routes. It cannot select an on-shell branch, action, source, carrier, boundary,
density, mass, `Xmax`, dynamics, prediction, or canon.
