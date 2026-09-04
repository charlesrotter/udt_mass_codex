# G338 preregistration — explicit Taub completed-pair finite-time readout

Date: 2026-09-03
Status: preregistered before production code or result artifacts

## Frozen question and regime

Use the complete G323/G324 Ricci-flat compact Taub/Kasner metric for proper time `T>0`. Choose an
arbitrary reference slice `T0>0`, an arbitrary initially unit spatial direction, and an arbitrary
finite rapidity. Extend the initial normal--spatial pair by the inherited commuting/Lie carry
already typed in G333--G337. Derive the full pair metric and then apply G176 W1 normalization.

After quotienting the repeated transverse plane by its exact rotational symmetry, let
`rho in [0,1]` be the initial squared longitudinal direction fraction, `z in R` the finite
rapidity, and `u=T/T0>0`. No value of `rho`, `z`, `T0`, the Taub parameter, or a lattice period is
selected.

## Candidate algebra to test

Define the carried spatial squared-length ratio

```text
G(u,rho)=rho*u^(-2/3)+(1-rho)*u^(4/3).
```

With `c=cosh(z)` and `s=sinh(z)`, the candidate complete pair matrix is

```text
h00=-c^2+G*s^2
h01=(G-1)*s*c
h11=-s^2+G*c^2
det(h)=-G.
```

On the regular timelike stratum `Delta=c^2-G*s^2>0`, the candidate W1 outputs are

```text
T_pair=sqrt(Delta)
L_sigma=sqrt(G/Delta)
m=sqrt(G)
beta=-(G-1)*s*c/Delta
L_s=1/sqrt(Delta)
beta_s=beta/sqrt(G)
Phi=-1/2*log(Delta)
chi=tanh(Phi)=(1-Delta)/(1+Delta).
```

These displayed formulas are preregistered candidates made visible during mapping. The derivation
must reconstruct them from the metric and pair pullback; string substitution is not evidence.

## Required classifications

1. Cover analytically all `u>0`, all `rho in [0,1]`, and all finite real `z`, subject only to the
   derived pair-timelike condition `Delta>0`; samples are controls, not coverage.
2. Keep the full pair matrix, determinant/ruler density, shift, terminal `Phi`, and `chi` separate.
3. At `z=0`, determine whether terminal `Phi` can be blind while the ruler density changes.
4. Classify the initially silent direction from the exact first derivative of `G` at `u=1` and
   determine its finite-time behavior without Taylor truncation.
5. Distinguish a `Delta=0` boundary of the declared carried pair from a spacetime singularity,
   causal boundary, physical horizon, or `X_max`.
6. Recheck the Kasner/Ricci-flat identity and initial first/second response independently of the
   pair formulas.

## Candidate landings

- **A:** `EXPLICIT_LAWFUL_TAUB_DEVELOPMENT_CARRIES_NATIVE_COMPLETED_PAIR_RESPONSE_FOR_FINITE_TIME__ZERO_BOOST_TERMINAL_BLINDNESS_COEXISTS_WITH_NONTRIVIAL_RULER_DENSITY__INITIAL_SILENCE_CAN_TURN_ON_EXACTLY__NO_OCCUPANCY_OR_SCALE_SELECTION`.
- **B:** `EXPLICIT_METRIC_EVOLVES_BUT_COMPLETED_RECIPROCAL_NORMALIZATION_ERASES_ALL_FINITE_TIME_PAIR_CHANGE`.
- **C:** `DECLARED_INHERITED_PAIR_GERM_HAS_NO_NONZERO_REGULAR_TIME_INTERVAL`.

Land on the strongest statement supported without retuning.

## Certification and falsification contract

Production must use exact rational/formal-power algebra and derive the pullback, determinant, W1
decomposition, initial jets, silent stratum, and representative regular-domain controls. An
implementation-distinct verifier may use separate direct matrices and high-precision finite
differences but may not import production code or read its output. Hostile checks must catch at
least: a wrong Kasner exponent, a dropped transverse channel, determinant-one imposed before W1,
shift deletion, raw pre-W1 depth substituted for W1 `Phi`, zero-boost blindness promoted to no
response, pair-boundary promotion to spacetime horizon, a selected direction/boost, and a
scale/`X_max` promotion.

Maximum grade before fresh external review is
`INDEPENDENTLY_VERIFIED_DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_REVIEW`.
