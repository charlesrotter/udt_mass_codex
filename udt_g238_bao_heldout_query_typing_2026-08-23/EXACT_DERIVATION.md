# G238 exact derivation — no-refit BAO query typing

Date: 2026-08-23

## 1. Result

```text
QUERY_TYPING_INCOMPLETE__NO_OUTCOME_OPENING
__FROZEN_SNE_STATE_DOES_NOT_DETERMINE_CONTINUOUS_METRIC_OR_SCREEN_HISTORY
__COMPLETE_METRIC_EVALUATORS_REMAIN_LIVE_CONDITIONALLY
__TWO_SOURCE_POPULATION_AND_REFERENCE_FORWARD_MAP_OPEN
```

This is a type/ownership result. No BOSS outcome, curve, mode, covariance value, feature, or scale
was opened to obtain it.

## 2. Exact objects on the two sides

G237 freezes a processed one-source radial state

\[
\mathcal S_{12}=\{(\phi_i,R_i),C_R\}_{i=0}^{11}
\]

up to one relative normalization. It explicitly supplies no interpolation, derivative, absolute
scale, complete metric history, null-branch population, or screen history.

The BOSS observable is a two-source, reference-projected angular statistic. Schematically its
expectation requires

\[
(g,\mathcal Q,\mathcal B,\mu_1,\mu_2,q)
\longmapsto
\Psi_g
\longmapsto
(\Psi_g)_*\mu_1,(\Psi_g\times\Psi_g)_*\mu_2
\longmapsto
w_q(\vartheta),
\]

where `g` is a complete metric history, `Q` the observer/source query, `B` populated branch data,
`mu_1` and `mu_2` the source one- and two-point measures, `q` the survey reference measure, and
`Psi_g` the full observation map. The BOSS contracts own the catalogue estimator and reference
semantics, not the preceding physical inputs.

## 3. Finite-state nonuniqueness theorem

Parse the decimal spellings of the twelve frozen G237 knots as exact rationals. Let the first and
last be `a` and `b`, and normalize the actual knots by

\[
u_i=\frac{\phi_i-a}{b-a},\qquad i=0,\ldots,11.
\]

No exact uniform-spacing premise is used. The stored decimal knots are nearly uniform, but the
proof uses their actual supplied values.

Define

\[
q(u)=\prod_{i=0}^{11}(u-u_i).
\]

Because every frozen `R_i` is positive, there is a polynomial `L_0(u)` interpolating
`log R_i`. Therefore

\[
R_\epsilon(u)=\exp[L_0(u)+\epsilon q(u)]
\]

is positive and smooth for every real `epsilon`, and exactly

\[
R_\epsilon(u_i)=R_i
\]

at every frozen knot. At the exact midpoint of the first two actual normalized roots,

\[
u_*=\frac{u_0+u_1}{2}
=\frac{1048457443726290}{23066063761978381},
\]

exact rational arithmetic gives

\[
q(u_*)\approx-1.0695688651039815\times10^{-6},
\]

\[
q'(u_*)\approx2.7786587003665664\times10^{-5},
\qquad
q''(u_*)\approx4.226911258802683\times10^{-4}.
\]

The exact integer numerators and denominators are recorded in `DERIVATION_RESULT.json`; all three
are nonzero. Consequently the identical frozen G237 state admits infinitely many positive smooth
continuations with different between-knot values, first derivatives, and second derivatives.

This directly blocks every proposed carry that needs a continuous radial profile or its jets. For
example, the same-history spherical tilted-screen curvature contrast already derived in G127
contains `phi'` and `phi''`; G188's complete-coframe Jacobi equation requires the metric curvature
along a whole supplied branch. G237 supplies neither object.

The theorem does not say that no physical continuation exists. It says that selecting one from the
frozen state would be an added interpolation/profile premise and hence a refit or scaffold unless
owned independently.

## 4. What the metric-native corpus does own

The later metric corpus genuinely improves the old G126 boundary:

- G127/G128 show that radial and tilted angular response can emerge from one supplied metric
  history, without an appended angular coefficient.
- G188 derives the full screen/Jacobi evaluator from a supplied complete metric and supplied affine
  null branch.
- G221 derives the complete-coframe null clock chord; screen and mixing enter before reciprocal
  readout.
- G226 derives the conditional clock/screen phase interlock on supplied composable null edges.

Thus the orchestra need not be bolted on afterward. But these are evaluators. None turns the eleven
G237 relative radial numbers into the complete continuous history required by the evaluator.

## 5. The independent two-source obstruction

Even a fully supplied one-source observation map `Psi_g` does not determine the BOSS two-point
statistic. A forward prediction needs the source pair measure.

If `mu_2` is the source two-point measure, the observed pair measure is

\[
\nu_2=(\Psi_g\times\Psi_g)_*\mu_2
\]

with branch sums and weights when `Psi_g` is multivalued. The Landy--Szalay combination compares
this measure with data-reference and reference-reference pair measures. Therefore:

- a source-free geometric map does not populate galaxy pairs;
- a one-point Jacobian does not determine `mu_2`;
- a product of two Jacobi matrices is not by itself a physical pair measure;
- branch duplication or noninjectivity requires explicit branch population and matching;
- the survey random catalogue owns footprint/reference semantics, not a physical source law.

A homogeneous or Poisson source hypothesis could be tested later, but it is a new, explicit
observational hypothesis. It is not derived by the metric and is not silently inserted here.

## 6. Reference-projection boundary

G126 remains decisive on the exact central-spherical query: its screen is radial and angle
preserving, and an ideal per-depth reference removes the pure radial multiplier. Therefore the
frozen radial state alone cannot generate the nontrivial BOSS angular curve.

The lawful route is a nonspherical/displaced complete-history query whose angular differential
survives the actual survey reference projection. G127/G128 prove that such metric-native angular
response can exist conditionally. They do not value it from G237 or populate the source pairs.

## 7. Why the BOSS outcomes stay closed

Opening R2--R5 now could only tempt one to choose:

- an interpolation between G237 knots;
- a nonspherical metric continuation;
- branch weights;
- a source pair measure;
- an angular feature, mode, covariance grid, or scale;

because it improves agreement. That would violate the no-refit contract. The correct scientific
return is therefore to stop before outcome inspection.

## 8. Smallest next constructive object

The missing bridge is not another scalar fit. It is a separately preregistered, complete
observer-sky point-process query consisting of:

1. one continuous complete metric history independently owned or anchored outside BOSS;
2. one observer and source-event incidence rule;
3. its populated null branches and weights;
4. the metric-derived clock and Jacobi maps on those branches;
5. an explicit source one-/two-point hypothesis;
6. the frozen BOSS selection/reference operator.

Only then can the frozen G237 state serve as a no-refit cross-channel constraint. If an
observational anchor is used to determine the missing continuous history, it must be separated
from the BOSS confirmation subset before outcomes are opened.

## 9. Maximum conclusion

G238 proves that the current metric-native evaluator is coherent and upstream-complete **once a
continuous metric/query/branch input is supplied**, but the frozen G237 state is not that input and
does not determine it. The BOSS query is therefore not yet evaluable without new, explicit
structure. No negative about UDT or positive claim about BAO follows.
