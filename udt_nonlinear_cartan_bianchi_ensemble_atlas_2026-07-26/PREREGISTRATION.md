# Nonlinear Cartan/Bianchi ensemble atlas — preregistration

Date: 2026-07-26
Base: `8b13104a4f1af45af617d2aa50cd5fdacf4082af`
Mode: CPU-only exact metric/coframe audit

## Whole question

What exact nonlinear structure, Levi-Civita connection, curvature couplings,
and differential identities follow from the complete common-domain coframe,
and where do those local results persist, require another chart, or cease to
apply across the twelve preregistered finite-cell completion classes?

This is a metric-led map. It does not ask for a desired action, particle,
cosmology, carrier, source, density window, or field equation. It is the
nonlinear continuation of the metric-orchestra rehearsal, not a search for a
familiar dynamical mechanism.

## Exact bounded domain

On the regular toric interior of

```text
M = [x0_minus,x0_plus] x [0,L] x T2,
x0 = c_E t,
```

use the complete block-triangular orthonormal coframe

```text
theta0 = exp(-phi) dx0,
theta1 = exp(+phi) dx,
Theta  = D[(dy,dz)^T + S(dx0,dx)^T],

D = [[r, k r],
     [0,   q]],
r = exp(sigma/2-alpha),
q = exp(sigma/2+alpha).
```

All eight chart amplitudes `(phi,sigma,alpha,k,S10,S11,S20,S21)` are arbitrary
smooth functions of `(x0,x)`. No neutral-point expansion or linearization is
permitted. The metric is `g = -(theta0)^2 + (theta1)^2 + Theta^T Theta`.

The exact structural channels are frozen in `CHANNEL_UNIVERSE.tsv`. With
`E0,E1` the horizontal orthonormal derivatives on torus-invariant scalars,
the calculation will express

```text
d theta0,
d theta1,
d Theta = (dD D^-1) wedge Theta + D(dS),
```

then solve uniquely for the torsion-free metric-compatible connection and
calculate its curvature. Coframe integrability and the first and second
Bianchi identities are audited separately from physical equations.

## Bounded calculations

1. Derive all structure coefficients exactly and verify `d^2 theta^a=0`,
   including the right Maurer-Cartan relation for `dD D^-1`.
2. Solve all 24 independent Levi-Civita connection coefficients from zero
   torsion and metric compatibility without importing a gravitational action.
3. Calculate all 36 independent curvature two-form coefficients exactly as
   functions of the ten structural channels and their base derivatives.
4. Verify curvature antisymmetry, the torsion equation, coframe integrability,
   and both Bianchi identities by independent algebraic routes.
5. Catalogue every nonzero derivative and quadratic channel-family coupling;
   distinguish scalar/common-scale, reciprocal angular shape, shear, and both
   connection-curvature channels.
6. Test the exact local construction against all twelve frozen completion
   classes, recording regular-chart applicability, required chart change,
   gluing/monodromy conditions, singular strata, and genuinely uncovered
   cases without selecting a preferred universe.
7. Ask whether any identity supplies a physical response one-form or merely
   constrains the consistency of the chosen coframe representation.

## Required controls

- all registered channels and outputs covered exactly once;
- no unregistered field, source, action, or density introduced;
- exact torsion cancellation for all four coframe legs;
- exact metric antisymmetry of the connection and curvature;
- exact right Maurer-Cartan signs checked by direct matrix differentiation;
- exact first-Bianchi cancellation after coframe integrability;
- exact abstract second-Bianchi cancellation without component fitting;
- dependency census recomputed from full nonlinear expressions;
- old `dphi` causal `3+3` transport result distinguished from this full
  coframe ensemble audit; and
- all twelve completion classes classified once, including an explicit scope
  failure where the toric coframe is not globally available.

## Density sequencing

No density value is used in this audit. The user's authorized future density
protocol is frozen in `DENSITY_FUTURE_PROTOCOL.tsv`: a current Lambda-CDM
mass/energy-density estimate may later be used only as an
`IMPORTED_COMPARISON_ANCHOR`, with a broad `FREE_AND_EXPLORED` bracket around
it. It is not a UDT source, selector, or prior. That sweep remains blocked
until a native density-to-geometry response law and complete on-shell branch
have been defined and preregistered.

## Stop rules and maximum conclusion

The fail-closed contracts in `FALSIFICATION_CONTRACT.tsv` are frozen before
the algebra is run. Stop rather than fill a missing action, source, boundary
functional, density law, topology, or evolution equation by analogy.

The maximum conclusion is an exact nonlinear geometric response atlas on the
declared regular coframe domain plus a scoped completion-applicability map. It
may reveal geometric cross-couplings and consistency identities. It cannot
select an action, claim a matter source or mass emergence, tune a universe,
derive `X_max`, or convert off-shell geometry into dynamics.
