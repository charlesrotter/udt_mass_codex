# G254 preregistration — complete time-live solver closure audit

Date: 2026-08-24

## Whole question

Do the currently owned UDT founding, completed-pair, complete-coframe, null/Jacobi, Cartan, and
network relations define a closed evolution problem for a complete Lorentz metric, modulo
diffeomorphism and frame gauge, or do they only evaluate a supplied smooth time-dependent metric?

This is `METRIC_LED`. It asks what equations are already owned. It does not target a cosmology,
profile, observational fit, `X_max`, particle, source, or familiar field equation.

## Three-stage gate

1. **Algebraic/differential closure audit.** Classify every candidate relation as a definition,
   identity, evaluator, gauge condition, or nonidentity ambient-history equation. Count independent
   metric functions and any owned evolution restrictions after gauge.
2. **Reduced time-live solve.** Proceed only if stage 1 exposes an owned nonidentity residual and a
   justified symmetry reduction. Derive the reduced ODE/PDE without adding a physical boundary
   condition or selecting a desired branch.
3. **Nonspherical/GPU formulation.** Proceed only if stage 2 has a well-posed continuum system and
   passes raw-residual and convergence gates. GPU work may change numerical method only.

Failure of a gate stops later stages. An undefined residual must not be replaced by an imported
Einstein equation, chosen action, observational loss, or arbitrary evolution rule.

## Preregistered closure criterion

Stage 1 returns `OWNED_TIMELIVE_SYSTEM_CLOSES` only if the frozen sources contain at least one
diffeomorphism-natural, nonidentity equation that restricts the ambient metric history rather than:

- defining the connection, curvature, pullback, ruler calibration, transport, or readout;
- holding for every smooth Lorentz metric by tensor calculus;
- reconstructing a supplied metric from supplied valued relations; or
- fixing only coordinates, coframe gauge, query calibration, or branch labels.

The positive result must identify the unknowns, principal differential order, constraints,
evolution equations, gauge freedom, and freely specifiable data. Otherwise the registered return is
`NO_OWNED_TIMELIVE_RESIDUAL__ODE_AND_GPU_SOLVES_NOT_YET_DEFINED`.

## Preregistered counterfamily

Use arbitrary smooth functions in the already registered G211 family

```text
g[Omega,q,b,H_A]
 = exp(2 Omega) [-f dt^2 + exp(2 q) h_A(dx+b dt,dx+b dt)].
```

The family is a diagnostic control, not a proposed universe. The audit will test whether each
owned relation either evaluates every regular member or actually rejects at least one member for a
nonidentity physical reason. At minimum, arbitrary analytic `Omega(t,x)` and `q(t,x)` controls must
be separated from coordinate gauge by scalar invariants or fixed calibrated pair readouts.

## Premise exclusions

No observational value or outcome; P1; G116/G189; Lambda-CDM; GR field equation; EH, `C^2`, or other
action; source, matter, bootstrap, or Maxwell law; boundary condition; numerical or physical
`X_max`; protected package; fitted profile; post-readout angular factor; or selected G204/G205
family may enter as a closure equation.

## Certification and falsification

- exact source hashes frozen in `SOURCE_MANIFEST.tsv`;
- premise status frozen in `PREMISE_LEDGER.tsv`;
- production classification and an independent source-first implementation must agree;
- hostile controls must catch reclassifying a definition/identity/evaluator as dynamics, deleting
  arbitrary-function witnesses, importing an action or Einstein equation, or launching a solver
  with no residual;
- a fresh read-only adversarial review is required before banking a scientific landing.

## Maximum conclusion

A negative result means only that the frozen active corpus does not yet own a complete time-live
residual. It is not a no-go for UDT, a proof that no global relation law exists, or evidence for a
particular new law. A positive result licenses only the explicitly derived bounded reduced solve;
it does not select initial data, boundary data, observer population, or an observed universe.
