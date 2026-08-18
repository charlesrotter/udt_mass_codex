# G152 preregistration — pair-immersion variational chord ownership

Date: 2026-08-17
Status: `PREREGISTERED_BEFORE_DERIVATION`

## Whole question

For one supplied smooth regular calibrated pair immersion \(F(\tau,\sigma)\), determine whether its
own coordinate or orthogonal ruler variation is automatically the G151 working chord

\[
\xi=\rho n,
\qquad
\rho=X_{\max}\tanh\phi_{\rm pair}.
\]

Classify exactly the value and first-jet conditions for equality and for the normalized pair-clock
commutator to vanish. Do not assume a connecting family, a value of \(X_{\max}\), or physical
history selection.

## Bounded regime

- one local smooth regular timelike pair immersion;
- pair metric written exactly as
  \(h=-T^2(d\tau+\beta d\sigma)^2+L^2d\sigma^2\), \(T,L>0\);
- finite nonzero working chord;
- both ruler orientations classified by \(\epsilon=\pm1\);
- full nonlinear first derivatives; no linearization.

Coincidence, null, degenerate, cut, singular, asymptotic, cross-query, global-completion, material,
signal, and observational strata are omitted.

## Premise ledger

| item | status | role |
|---|---|---|
| pair immersion and `h` | `SUPPLIED / DERIVED_PULLBACK` | owns `J0,J1,T,L,beta` |
| normalized clock `u=J0/T` | `DERIVED` | pair-clock flow |
| orthogonal ruler `r=J1-beta J0=L n` | `DERIVED` | metric ruler line |
| working `xi=X_max tanh(phi_pair)n` | `CHOSE / WORKING` | relational position representation |
| `epsilon=+/-1` | `CHOSE_ORIENTATION_LABEL` | classify both orientations |
| `X_max` | `WORKING_FOUNDATIONAL_FRAME`, value `OPEN` | symbolic constant only |
| equality of `xi` with ruler/coordinate variation | `OPEN` | object of test |
| normalized-flow bracket condition | `OPEN` | object of test |
| physical query/history/dynamics | `OPEN` | prohibited inference |

## Preregistered derivation

1. Derive `J1=beta T u+L n` and distinguish coordinate variation from orthogonal ruler variation.
2. Classify equality of `xi` with each oriented variation.
3. Substitute the terminal identity
   \(\phi_{\rm pair}=\tfrac12\log(L/T)\) and solve the magnitude condition for \(T\) and for the
   implied candidate \(X_{\max}\).
4. Derive \([u,\xi]\) exactly for \(\xi=(\rho/L)r\), retaining shift and lapse derivatives.
5. Prove the exact extra first-jet condition for a carried ruler and the stronger coordinate-
   variation subcase.
6. Verify both orientation branches and three counterexamples: regular non-equality, equality
   without connecting carry, and connecting carry without equality.
7. Submit to fresh adversarial review before banking.

## Certification and falsification

Pass requires exact symbolic equivalence in both orientations, explicit nonzero denominators/domain
conditions, independent recomputation, genuine counterexamples, and no promotion of the equality
condition into UDT physics. Any failed branch or hidden division leaves the classification `OPEN`.

## Maximum conclusion allowed

```text
PAIR_IMMERSION_OWNS_COORDINATE_AND_ORTHOGONAL_VARIATIONS_BUT_NOT_THEIR_IDENTIFICATION_WITH_WORKING_XI__
EXACT_MAGNITUDE_SHIFT_LAPSE_AND_COMMUTATOR_CONDITIONS_CLASSIFIED__
UNIVERSAL_XMAX_WOULD_REQUIRE_CANDIDATE_CONSTANCY_ACROSS_THE_SUPPLIED_FAMILY__
PHYSICAL_IDENTIFICATION_QUERY_HISTORY_DYNAMICS_XMAX_VALUE_AND_COMPLETION_OPEN
```

