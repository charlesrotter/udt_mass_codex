# G333 preregistration — metric-native initial pair response

Date: 2026-09-03
Status: `PREREGISTERED_BEFORE_OUTCOME_EXECUTION`

## Question and scope

On every G332 datum in the strict real branch, derive rather than fit the initial normal-response
endomorphism

```text
H^i_j = (1/2) gamma^(ik) L_n gamma_kj = -K^i_j
```

Post-review notation clarification, which changes no frozen candidate or acceptance gate: whenever
this package writes `H(v,v)`, it means the bilinear contraction
`gamma(Hv,v)=(1/2)(L_n gamma)(v,v)`.

and its value on every unit separation direction `v`. Decompose it invariantly into trace and
trace-free parts. Evaluate the complete supplied pair germ spanned by the unit normal `n` and `v`.
Classify which first-jet channels are visible in the complete pair metric and which are visible in
the terminal scalar in this declared germ.

## Pinned, free, and omitted choices

- `pinned-by-THEORY_CONDITIONAL`: G310/G312 bounded equation, G315 sign convention
  `K=-(1/2)L_n gamma`, and the exact G332 data family.
- `free-and-explored`: every unit direction through `mu in [0,1]`, both square-root branches, both
  signs of admissible `C`, unequal/equal positive weights, and fixed finite connected `Lambda`.
- `CHOSE_GAUGE_PRESENTATION_CONTROL`: Gaussian normal coordinates at the initial slice. Lapse and
  shift are not physical data.
- `OMITTED_OPEN`: later time, eigengap/orbit persistence, nonlinear stability, occupancy, matter,
  mass, sources, action, observational transfer, absolute scale, and physical `X_max`.

## Exact checks

The production derivation must verify:

1. `H=-K^sharp` from the registered sign convention.
2. Horizontal and vertical rates from the invariant projector `P=xi tensor xi_flat`.
3. Trace, trace-free eigenvalues, shear norm, and reconstruction of `H`.
4. The all-direction formula as a function of `mu` and its endpoint/interior controls.
5. Both G332 algebraic branches and the Hamiltonian identity, without choosing a sign.
6. Equal-weight constant-curvature and unequal-weight nonconstant-curvature controls.
7. No dependence on orbit period, rationality, Hopf quotient, or fibre normalization.
8. For the supplied normal--spatial germ, the complete pair spatial-length derivative agrees with
   `gamma(Hv,v)` while the proper-normal clock entry has zero first derivative in Gaussian
   presentation.
9. Terminal `Phi=-1/2 log(-h_00)` is consequently blind to this particular first spatial strain,
   without promoting that scoped fact into a theorem about every physical pair germ.

An implementation-distinct verifier must reconstruct the rate algebra without importing production
code or reading its result. Hostile mutations must catch at least: wrong sign, dropped `b`, wrong
trace, wrong shear coefficient, branch collapse, lapse promoted to physics, terminal scalar falsely
called complete, and topology inserted into the response.

## Falsification and classification contract

- Land `COMMON_ONLY` only if the exact directional difference vanishes identically on both branches.
- Land `METRIC_2_PLUS_1` only if a nonzero invariant trace-free channel is proved and reconstructed.
- Land `TOPOLOGY_REQUIRED` only if some response formula cannot be written from local
  `(gamma,K,n,v)` data.
- Land `PAIR_TERMINAL_COMPLETE` only if the terminal scalar reconstructs every first-jet rate.
- Otherwise land `COMPLETE_PULLBACK_STRONGER` with the exact missing channel stated.
- Any residual failure, branch omission, hidden physical pin, or shared-code false independence
  limits the result to `LEAD` or `OPEN`.

## Maximum grade

`DERIVED_CONDITIONAL_BOUNDED`, pending independent and fresh adversarial verification. No result may
select a topology, a history, a datum, or an observational scale.
